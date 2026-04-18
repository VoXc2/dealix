"""
Dealix — BaseEngagementAgent
=============================
Abstract base class for all channel agents.

Every channel (WhatsApp, Email, LinkedIn, SMS, Voice) must extend this class
and implement `send`, `receive`, and optionally override `reply`.

Design principles:
  - Settings injected via constructor (no magic globals)
  - Memory is pluggable (SQLite default, Redis optional)
  - Compliance checks run before every outbound send
  - Observability hooks log every interaction
  - Rate limiting + exponential-backoff retry built-in
"""

from __future__ import annotations

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, time as dtime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

logger = logging.getLogger("dealix.engagement.base")


# ─────────────────────────────────────────────────────────────
# Enums
# ─────────────────────────────────────────────────────────────

class ChannelType(str, Enum):
    WHATSAPP = "whatsapp"
    EMAIL = "email"
    LINKEDIN = "linkedin"
    SMS = "sms"
    VOICE = "voice"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"


class MessageDirection(str, Enum):
    INBOUND = "in"
    OUTBOUND = "out"


class LeadStage(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    REPLIED = "replied"
    QUALIFIED = "qualified"
    DEMO_SCHEDULED = "demo_scheduled"
    PROPOSAL_SENT = "proposal_sent"
    NEGOTIATING = "negotiating"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"
    UNSUBSCRIBED = "unsubscribed"


class DeliveryStatus(str, Enum):
    QUEUED = "queued"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    RATE_LIMITED = "rate_limited"
    COMPLIANCE_BLOCKED = "compliance_blocked"


# ─────────────────────────────────────────────────────────────
# Data models
# ─────────────────────────────────────────────────────────────

class AgentContext(BaseModel):
    """Contextual metadata passed to every agent operation."""
    lead_id: str | None = None
    lead_phone: str | None = None
    lead_email: str | None = None
    lead_name: str | None = None
    company_name: str | None = None
    sector: str | None = None
    city: str | None = None
    stage: LeadStage = LeadStage.NEW
    opt_in: bool = True                 # PDPL / WhatsApp policy compliance
    locale: str = "ar-SA"
    timezone_offset: int = 3            # UTC+3 (Saudi Arabia)
    extra: dict[str, Any] = Field(default_factory=dict)


class IncomingMessage(BaseModel):
    """Normalised inbound message from any channel."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    channel: ChannelType
    from_address: str                   # phone, email, linkedin urn, etc.
    body: str
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    provider_message_id: str | None = None
    profile_name: str | None = None
    media_urls: list[str] = Field(default_factory=list)
    raw_payload: dict[str, Any] = Field(default_factory=dict)


class DeliveryReceipt(BaseModel):
    """Result of an outbound send operation."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    channel: ChannelType
    to: str
    status: DeliveryStatus
    provider_message_id: str | None = None
    sent_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    error: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


# ─────────────────────────────────────────────────────────────
# Settings
# ─────────────────────────────────────────────────────────────

class EngagementSettings(BaseSettings):
    """
    Shared settings for all engagement agents.
    Values come from environment variables (or .env).
    """

    # LLM
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # Database
    dealix_db: str = "dealix_engagement.db"

    # Redis (optional)
    redis_url: str = "redis://localhost:6379/0"

    # Twilio (WhatsApp + SMS)
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_whatsapp_number: str = ""   # e.g. whatsapp:+14155238886
    twilio_sms_number: str = ""

    # SendGrid (Email)
    sendgrid_api_key: str = ""
    sendgrid_from_email: str = "noreply@dealix.ai"
    sendgrid_from_name: str = "Dealix"

    # Unipile (LinkedIn)
    unipile_api_key: str = ""
    unipile_dsn: str = ""

    # Compliance
    quiet_hours_start: int = 22         # 22:00 local time
    quiet_hours_end: int = 8            # 08:00 local time
    rate_limit_per_minute: int = 10
    rate_limit_per_hour: int = 100
    max_retry_attempts: int = 3
    retry_base_delay: float = 1.0       # seconds

    model_config = {"env_file": ".env", "extra": "ignore"}


# ─────────────────────────────────────────────────────────────
# Compliance helper
# ─────────────────────────────────────────────────────────────

@dataclass
class ComplianceResult:
    allowed: bool
    reason: str = ""


def check_compliance(
    context: AgentContext,
    settings: EngagementSettings,
) -> ComplianceResult:
    """
    Run pre-send compliance checks:
      1. Opt-in status (PDPL / Meta / LinkedIn ToS)
      2. Quiet-hours window (UTC+3)
      3. Do-not-contact flag
    """
    if not context.opt_in:
        return ComplianceResult(
            allowed=False,
            reason="Lead has not opted in — PDPL compliance block",
        )

    # Quiet hours check
    utc_hour = datetime.now(timezone.utc).hour
    local_hour = (utc_hour + context.timezone_offset) % 24
    qs = settings.quiet_hours_start
    qe = settings.quiet_hours_end
    if qs > qe:
        # wraps midnight
        in_quiet = local_hour >= qs or local_hour < qe
    else:
        in_quiet = qs <= local_hour < qe

    if in_quiet:
        return ComplianceResult(
            allowed=False,
            reason=f"Quiet hours ({qs}:00–{qe}:00 local). Message queued.",
        )

    if context.stage == LeadStage.UNSUBSCRIBED:
        return ComplianceResult(
            allowed=False,
            reason="Lead is unsubscribed — do not contact",
        )

    return ComplianceResult(allowed=True)


# ─────────────────────────────────────────────────────────────
# Rate-limiter (in-process token bucket — replace with Redis in prod)
# ─────────────────────────────────────────────────────────────

@dataclass
class _RateLimiter:
    max_per_minute: int = 10
    max_per_hour: int = 100
    _minute_tokens: float = field(init=False)
    _hour_tokens: float = field(init=False)
    _last_minute_refill: float = field(init=False)
    _last_hour_refill: float = field(init=False)

    def __post_init__(self) -> None:
        self._minute_tokens = float(self.max_per_minute)
        self._hour_tokens = float(self.max_per_hour)
        self._last_minute_refill = time.monotonic()
        self._last_hour_refill = time.monotonic()

    def consume(self) -> bool:
        """Return True if a token was consumed, False if rate-limited."""
        now = time.monotonic()

        # Refill minute bucket
        elapsed_min = now - self._last_minute_refill
        self._minute_tokens = min(
            float(self.max_per_minute),
            self._minute_tokens + elapsed_min * (self.max_per_minute / 60),
        )
        self._last_minute_refill = now

        # Refill hour bucket
        elapsed_hr = now - self._last_hour_refill
        self._hour_tokens = min(
            float(self.max_per_hour),
            self._hour_tokens + elapsed_hr * (self.max_per_hour / 3600),
        )
        self._last_hour_refill = now

        if self._minute_tokens >= 1 and self._hour_tokens >= 1:
            self._minute_tokens -= 1
            self._hour_tokens -= 1
            return True
        return False


# ─────────────────────────────────────────────────────────────
# BaseEngagementAgent (ABC)
# ─────────────────────────────────────────────────────────────

class BaseEngagementAgent(ABC):
    """
    Abstract base for every Dealix engagement channel agent.

    Subclasses MUST implement:
      - send(to, message, context) -> DeliveryReceipt
      - receive(payload) -> IncomingMessage

    Subclasses MAY override:
      - reply(incoming) -> str  (default uses LLMGateway)
      - channel property
    """

    channel: ChannelType  # must be set by subclass

    def __init__(
        self,
        settings: EngagementSettings,
        memory: "ConversationMemory | None" = None,
        llm: "LLMGateway | None" = None,
    ) -> None:
        self.settings = settings
        self._memory = memory
        self._llm = llm
        self._rate_limiter = _RateLimiter(
            max_per_minute=settings.rate_limit_per_minute,
            max_per_hour=settings.rate_limit_per_hour,
        )
        self._log = logging.getLogger(f"dealix.engagement.{self.channel}")

    # ── Lazy accessors ──────────────────────────────────────

    @property
    def memory(self) -> "ConversationMemory":
        if self._memory is None:
            from .memory import ConversationMemory
            self._memory = ConversationMemory(db_path=self.settings.dealix_db)
        return self._memory

    @property
    def llm(self) -> "LLMGateway":
        if self._llm is None:
            from .llm import LLMGateway
            self._llm = LLMGateway(settings=self.settings)
        return self._llm

    # ── Abstract interface ───────────────────────────────────

    @abstractmethod
    async def send(
        self, to: str, message: str, context: AgentContext
    ) -> DeliveryReceipt:
        """Send a message to the given address via this channel."""

    @abstractmethod
    async def receive(self, payload: dict[str, Any]) -> IncomingMessage:
        """Parse a raw incoming webhook payload into a normalised IncomingMessage."""

    # ── Default reply logic (LLM-powered) ───────────────────

    async def reply(self, incoming: IncomingMessage) -> str:
        """
        Generate a reply for an IncomingMessage using the LLM gateway.
        Override per-channel for custom logic.
        """
        history = await self.memory.get_history(
            channel=self.channel.value,
            address=incoming.from_address,
            limit=10,
        )
        prompt_key = f"{self.channel.value}_inbound_ar"
        system_prompt = self.llm.get_system_prompt(prompt_key)
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": incoming.body})

        response = await self.llm.chat(messages=messages)
        return response

    # ── High-level send_with_guards ──────────────────────────

    async def send_with_guards(
        self, to: str, message: str, context: AgentContext
    ) -> DeliveryReceipt:
        """
        Wraps `send` with:
          1. Compliance check
          2. Rate-limit check
          3. Exponential-backoff retry
          4. Observability logging
          5. Lead + message persistence
        """
        # 1. Compliance
        compliance = check_compliance(context, self.settings)
        if not compliance.allowed:
            self._log.warning("Compliance block [%s]: %s", to, compliance.reason)
            receipt = DeliveryReceipt(
                channel=self.channel,
                to=to,
                status=DeliveryStatus.COMPLIANCE_BLOCKED,
                error=compliance.reason,
            )
            await self._observe(receipt, context)
            return receipt

        # 2. Rate limit
        if not self._rate_limiter.consume():
            self._log.warning("Rate limit hit sending to %s", to)
            receipt = DeliveryReceipt(
                channel=self.channel,
                to=to,
                status=DeliveryStatus.RATE_LIMITED,
                error="Rate limit exceeded",
            )
            await self._observe(receipt, context)
            return receipt

        # 3. Retry loop
        last_error: str = ""
        for attempt in range(1, self.settings.max_retry_attempts + 1):
            try:
                receipt = await self.send(to, message, context)
                await self._persist_outbound(to, message, receipt, context)
                await self._observe(receipt, context)
                return receipt
            except Exception as exc:  # noqa: BLE001
                last_error = str(exc)
                delay = self.settings.retry_base_delay * (2 ** (attempt - 1))
                self._log.error(
                    "Send attempt %d/%d failed for %s: %s. Retrying in %.1fs",
                    attempt, self.settings.max_retry_attempts, to, exc, delay,
                )
                if attempt < self.settings.max_retry_attempts:
                    await asyncio.sleep(delay)

        # All retries exhausted
        receipt = DeliveryReceipt(
            channel=self.channel,
            to=to,
            status=DeliveryStatus.FAILED,
            error=f"All {self.settings.max_retry_attempts} retries failed: {last_error}",
        )
        await self._observe(receipt, context)
        return receipt

    # ── Lead persistence hook ────────────────────────────────

    async def _persist_outbound(
        self,
        to: str,
        body: str,
        receipt: DeliveryReceipt,
        context: AgentContext,
    ) -> None:
        """Save outbound message + upsert lead in memory."""
        try:
            await self.memory.upsert_lead(
                channel=self.channel.value,
                address=to,
                name=context.lead_name,
                company=context.company_name,
                sector=context.sector,
                stage=context.stage.value,
            )
            await self.memory.save_message(
                channel=self.channel.value,
                address=to,
                direction=MessageDirection.OUTBOUND.value,
                body=body,
                provider_message_id=receipt.provider_message_id,
            )
        except Exception as exc:  # noqa: BLE001
            self._log.error("Failed to persist outbound message: %s", exc)

    async def persist_inbound(
        self,
        incoming: IncomingMessage,
        context: AgentContext | None = None,
    ) -> None:
        """Save inbound message + upsert lead in memory."""
        try:
            await self.memory.upsert_lead(
                channel=self.channel.value,
                address=incoming.from_address,
                name=incoming.profile_name,
            )
            await self.memory.save_message(
                channel=self.channel.value,
                address=incoming.from_address,
                direction=MessageDirection.INBOUND.value,
                body=incoming.body,
                provider_message_id=incoming.provider_message_id,
            )
        except Exception as exc:  # noqa: BLE001
            self._log.error("Failed to persist inbound message: %s", exc)

    # ── Observability hook ───────────────────────────────────

    async def _observe(
        self,
        receipt: DeliveryReceipt,
        context: AgentContext,
    ) -> None:
        """
        Log every outbound interaction for observability.
        Extend or replace with PostHog / Sentry / custom sink as needed.
        """
        self._log.info(
            "channel=%s to=%s status=%s lead_id=%s company=%s",
            self.channel.value,
            receipt.to,
            receipt.status.value,
            context.lead_id,
            context.company_name,
        )

    # ── Utility ──────────────────────────────────────────────

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} channel={self.channel.value}>"
