"""
Dealix — EngagementOrchestrator
=================================
Takes a Lead + a Playbook and manages the full outreach sequence:

  1. Determine which channel to use (preference order + opt-in + availability)
  2. Generate the correct message via LLM
  3. Send via the appropriate channel agent (with guards)
  4. Record the step in memory
  5. Schedule the next step (returns next_step_at)
  6. Respect compliance (quiet hours, opt-in, rate limits)

Usage:
    settings = EngagementSettings()
    memory = ConversationMemory(db_path=settings.dealix_db)
    await memory.init()
    llm = LLMGateway(settings=settings)

    orchestrator = EngagementOrchestrator(settings=settings, memory=memory, llm=llm)
    playbook = Playbook.from_yaml("playbooks/ecommerce_outbound.yaml")
    lead = Lead(
        id="lead_001",
        name="Ahmed Al-Rashid",
        company="متجر الأفق",
        phone="+966512345678",
        email="ahmed@alofuq.com",
    )
    result = await orchestrator.run_step(lead=lead, playbook=playbook, step_index=0)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml

from .base import (
    AgentContext,
    ChannelType,
    DeliveryReceipt,
    DeliveryStatus,
    EngagementSettings,
    LeadStage,
)
from .memory import ConversationMemory
from .llm import LLMGateway

logger = logging.getLogger("dealix.engagement.orchestrator")


# ─────────────────────────────────────────────────────────────
# Data models
# ─────────────────────────────────────────────────────────────

@dataclass
class Lead:
    """Minimal lead model for the orchestrator."""
    id: str
    name: str
    company: str | None = None
    sector: str | None = None
    city: str | None = None
    phone: str | None = None
    email: str | None = None
    linkedin_urn: str | None = None
    stage: LeadStage = LeadStage.NEW
    opt_in: bool = True
    extra: dict[str, Any] = field(default_factory=dict)

    def to_context(self) -> AgentContext:
        return AgentContext(
            lead_id=self.id,
            lead_phone=self.phone,
            lead_email=self.email,
            lead_name=self.name,
            company_name=self.company,
            sector=self.sector,
            city=self.city,
            stage=self.stage,
            opt_in=self.opt_in,
        )

    def preferred_address(self, channel: ChannelType) -> str | None:
        """Return the address (phone/email/urn) for the given channel."""
        return {
            ChannelType.WHATSAPP: self.phone,
            ChannelType.SMS:      self.phone,
            ChannelType.VOICE:    self.phone,
            ChannelType.EMAIL:    self.email,
            ChannelType.LINKEDIN: self.linkedin_urn,
        }.get(channel)


@dataclass
class PlaybookStep:
    """A single step in a playbook sequence."""
    channel: ChannelType
    delay_days: int                       # days after previous step (0 = immediate)
    prompt_key: str                       # LLM prompt key (e.g. "whatsapp_outbound_ar")
    message_template: str | None = None   # optional static template (skips LLM if set)
    condition: str | None = None          # optional condition (e.g. "no_reply")
    max_retries: int = 1


@dataclass
class Playbook:
    """Ordered sequence of engagement steps."""
    name: str
    description: str
    target_sector: str
    steps: list[PlaybookStep]
    channel_priority: list[ChannelType] = field(
        default_factory=lambda: [
            ChannelType.WHATSAPP,
            ChannelType.EMAIL,
            ChannelType.LINKEDIN,
            ChannelType.SMS,
        ]
    )

    @classmethod
    def from_yaml(cls, path: str | Path) -> "Playbook":
        """Load a playbook from a YAML file."""
        with open(path, encoding="utf-8") as f:
            data: dict[str, Any] = yaml.safe_load(f)

        steps = [
            PlaybookStep(
                channel=ChannelType(s["channel"]),
                delay_days=s.get("delay_days", 0),
                prompt_key=s.get("prompt_key", "whatsapp_outbound_ar"),
                message_template=s.get("message_template"),
                condition=s.get("condition"),
                max_retries=s.get("max_retries", 1),
            )
            for s in data.get("steps", [])
        ]

        channel_priority = [
            ChannelType(c) for c in data.get(
                "channel_priority",
                ["whatsapp", "email", "linkedin", "sms"],
            )
        ]

        return cls(
            name=data["name"],
            description=data.get("description", ""),
            target_sector=data.get("target_sector", "general"),
            steps=steps,
            channel_priority=channel_priority,
        )

    @classmethod
    def from_dir(cls, directory: str | Path) -> list["Playbook"]:
        """Load all playbooks from a directory."""
        playbooks: list[Playbook] = []
        for path in sorted(Path(directory).glob("*.yaml")):
            try:
                playbooks.append(cls.from_yaml(path))
            except Exception as exc:  # noqa: BLE001
                logger.error("Failed to load playbook %s: %s", path, exc)
        return playbooks


@dataclass
class StepResult:
    """Result of executing a single playbook step."""
    step_index: int
    channel: ChannelType
    receipt: DeliveryReceipt | None
    success: bool
    next_step_at: datetime | None       # when to execute step_index + 1
    error: str | None = None


# ─────────────────────────────────────────────────────────────
# EngagementOrchestrator
# ─────────────────────────────────────────────────────────────

class EngagementOrchestrator:
    """
    Manages multi-step omnichannel engagement sequences.

    Dependency-injected:
        settings: EngagementSettings
        memory:   ConversationMemory
        llm:      LLMGateway
        agents:   dict mapping ChannelType → BaseEngagementAgent (optional)
    """

    def __init__(
        self,
        settings: EngagementSettings,
        memory: ConversationMemory,
        llm: LLMGateway,
        agents: dict[ChannelType, Any] | None = None,
    ) -> None:
        self.settings = settings
        self.memory = memory
        self.llm = llm
        self._agents = agents or {}

    def register_agent(self, channel: ChannelType, agent: Any) -> None:
        """Register a channel agent. Can be called after construction."""
        self._agents[channel] = agent

    # ── Main entry points ────────────────────────────────────

    async def run_step(
        self,
        lead: Lead,
        playbook: Playbook,
        step_index: int = 0,
    ) -> StepResult:
        """
        Execute a single playbook step for a lead.

        Returns a StepResult including when the next step should be scheduled.
        """
        if step_index >= len(playbook.steps):
            return StepResult(
                step_index=step_index,
                channel=ChannelType.WHATSAPP,
                receipt=None,
                success=False,
                next_step_at=None,
                error="Step index out of range — playbook complete",
            )

        step = playbook.steps[step_index]
        channel = self._resolve_channel(lead, step, playbook)

        if channel is None:
            return StepResult(
                step_index=step_index,
                channel=step.channel,
                receipt=None,
                success=False,
                next_step_at=None,
                error="No available channel for lead (check opt-in + contact info)",
            )

        address = lead.preferred_address(channel)
        if not address:
            return StepResult(
                step_index=step_index,
                channel=channel,
                receipt=None,
                success=False,
                next_step_at=None,
                error=f"No address for channel {channel.value}",
            )

        # Generate message
        message = await self._compose_message(lead, step)

        # Send via channel agent
        agent = self._agents.get(channel)
        if agent is None:
            return StepResult(
                step_index=step_index,
                channel=channel,
                receipt=None,
                success=False,
                next_step_at=None,
                error=f"No agent registered for channel {channel.value}",
            )

        context = lead.to_context()
        receipt = await agent.send_with_guards(address, message, context)

        success = receipt.status in (DeliveryStatus.SENT, DeliveryStatus.QUEUED)

        # Calculate when to run next step
        next_step_at: datetime | None = None
        if success and step_index + 1 < len(playbook.steps):
            next_step = playbook.steps[step_index + 1]
            next_step_at = datetime.now(timezone.utc) + timedelta(
                days=next_step.delay_days
            )

        # Update lead stage
        if success and context.stage == LeadStage.NEW:
            await self.memory.update_stage(
                channel=channel.value,
                address=address,
                stage=LeadStage.CONTACTED.value,
            )

        logger.info(
            "Playbook %s step %d/%d → %s → %s: %s",
            playbook.name,
            step_index + 1,
            len(playbook.steps),
            channel.value,
            lead.name,
            receipt.status.value,
        )

        return StepResult(
            step_index=step_index,
            channel=channel,
            receipt=receipt,
            success=success,
            next_step_at=next_step_at,
        )

    async def run_full_playbook(
        self,
        lead: Lead,
        playbook: Playbook,
        stop_on_reply: bool = True,
    ) -> list[StepResult]:
        """
        Execute all steps synchronously (for testing / manual runs).
        In production, use run_step() with a task scheduler (ARQ / Celery).

        WARNING: This blocks between steps using asyncio.sleep(delay_days * 86400).
        For production, schedule each step individually via a task queue.
        """
        results: list[StepResult] = []
        for i in range(len(playbook.steps)):
            result = await self.run_step(lead=lead, playbook=playbook, step_index=i)
            results.append(result)
            if not result.success:
                break
            # In production: schedule next step at result.next_step_at
            # Here we just record what would happen
        return results

    # ── Channel resolution ───────────────────────────────────

    def _resolve_channel(
        self,
        lead: Lead,
        step: PlaybookStep,
        playbook: Playbook,
    ) -> ChannelType | None:
        """
        Decide which channel to use.

        Priority:
          1. Use the step's specified channel if the lead has an address for it.
          2. Fall back to playbook's channel_priority order.
          3. Return None if no channel is viable.
        """
        # Try the step's preferred channel first
        preferred = step.channel
        if lead.preferred_address(preferred) and preferred in self._agents:
            return preferred

        # Fall back by priority
        for ch in playbook.channel_priority:
            if lead.preferred_address(ch) and ch in self._agents:
                return ch

        return None

    # ── Message composition ──────────────────────────────────

    async def _compose_message(self, lead: Lead, step: PlaybookStep) -> str:
        """
        Generate the message for this step.
        Uses static template if provided, otherwise calls LLM.
        """
        if step.message_template:
            # Simple template substitution
            try:
                return step.message_template.format(
                    name=lead.name or "",
                    company=lead.company or "",
                    sector=lead.sector or "",
                    city=lead.city or "",
                )
            except KeyError:
                return step.message_template

        # LLM generation
        system_prompt = self.llm.compose_prompt("system_base_ar", step.prompt_key)
        lead_context = (
            f"العميل: {lead.name} | الشركة: {lead.company} | "
            f"القطاع: {lead.sector} | المدينة: {lead.city}"
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"اكتب رسالة تواصل للـ {step.prompt_key.replace('_', ' ')} "
                    f"لهذا العميل:\n{lead_context}"
                ),
            },
        ]
        return await self.llm.chat(messages=messages, max_tokens=300)
