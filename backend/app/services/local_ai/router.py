"""
Local Model Router — picks the right local model per task, with optional
"racing" (run two small candidates in parallel and keep the better answer).

This is a safe, conservative interpretation of the model-racing pattern
seen in projects like G0DM0D3: no jailbreak prompts, no liberation layer.
We only use it to A/B two candidate local models for complex tasks and
pick the one whose response scores higher on a cheap length/format
heuristic (or on router-picked preferences).

If no local model is available, the router gracefully signals "unavailable"
so upstream code can fall back to the cloud LLM stack.
"""
from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass
from typing import Optional

from app.services.local_ai.catalog import (
    LocalModelSpec,
    ServerTier,
    TaskKind,
    detect_server_tier,
    pick_model_for_task,
)
from app.services.local_ai.client import OllamaChatResult, OllamaClient, get_local_client

logger = logging.getLogger(__name__)

# ── Task mapping from Dealix agent task-strings to TaskKind ────────

_TASK_STRING_MAP: dict[str, TaskKind] = {
    # router-ish
    "fast_classify": TaskKind.ROUTER,
    "lead_score": TaskKind.ROUTER,
    "intent_detect": TaskKind.ROUTER,
    "sentiment": TaskKind.ROUTER,
    "tag": TaskKind.ROUTER,
    "text_classification": TaskKind.ROUTER,

    # general / drafting
    "arabic_summarization": TaskKind.MULTILINGUAL,
    "internal_drafting": TaskKind.GENERAL,
    "translation": TaskKind.MULTILINGUAL,
    "entity_extraction": TaskKind.GENERAL,
    "data_cleaning": TaskKind.GENERAL,
    "followup_plan": TaskKind.GENERAL,

    # reasoning
    "research": TaskKind.REASONER,
    "strategy": TaskKind.REASONER,
    "complex_reasoning": TaskKind.REASONER,

    # coder
    "coding": TaskKind.CODER,
    "code_review_simple": TaskKind.CODER,
    "integration": TaskKind.CODER,
    "debug": TaskKind.CODER,
}


@dataclass
class RouteDecision:
    """Explain which local model was selected and why."""
    model: Optional[LocalModelSpec]
    tier: ServerTier
    task: TaskKind
    reason: str
    available: bool

    def to_dict(self) -> dict:
        return {
            "model": self.model.ollama_tag if self.model else None,
            "tier": self.tier.value,
            "task": self.task.value,
            "reason": self.reason,
            "available": self.available,
        }


# ── Router ─────────────────────────────────────────────────────────

def _env_flag(name: str, default: bool = False) -> bool:
    val = os.environ.get(name, "").strip().lower()
    if not val:
        return default
    return val in {"1", "true", "yes", "on"}


class LocalModelRouter:
    """
    High-level router used by Dealix agents to run tasks on local models.

    Features:
      • tier-aware model picking (delegates to catalog.pick_model_for_task)
      • env-based overrides (LOCAL_LLM_DEFAULT_MODEL, _ROUTER_MODEL, _CODER_MODEL)
      • optional "race": run two candidate models in parallel and keep the better
      • graceful fallback: returns success=False when no local model is usable
    """

    def __init__(
        self,
        client: Optional[OllamaClient] = None,
        *,
        prefer_arabic: bool = True,
    ):
        self.client = client or get_local_client()
        self.prefer_arabic = prefer_arabic
        self._capacity = detect_server_tier()
        self.default_model = os.environ.get("LOCAL_LLM_DEFAULT_MODEL", "").strip() or None
        self.router_model = os.environ.get("LOCAL_LLM_ROUTER_MODEL", "").strip() or None
        self.coder_model = os.environ.get("LOCAL_LLM_CODER_MODEL", "").strip() or None
        self.reasoner_model = os.environ.get("LOCAL_LLM_REASONER_MODEL", "").strip() or None

    # ── enablement ──────────────────────────────────────────────

    def is_enabled(self) -> bool:
        return _env_flag("LOCAL_LLM_ENABLED", default=False)

    async def is_available(self) -> bool:
        """Enabled + daemon responds + at least one model tag present."""
        if not self.is_enabled():
            return False
        if not await self.client.health():
            return False
        models = await self.client.list_models()
        return bool(models)

    # ── selection ───────────────────────────────────────────────

    def resolve_task(self, task_string: str) -> TaskKind:
        return _TASK_STRING_MAP.get(task_string, TaskKind.GENERAL)

    def _env_tag_for(self, task: TaskKind) -> Optional[str]:
        if task == TaskKind.ROUTER and self.router_model:
            return self.router_model
        if task == TaskKind.CODER and self.coder_model:
            return self.coder_model
        if task == TaskKind.REASONER and self.reasoner_model:
            return self.reasoner_model
        return self.default_model

    def decide(self, task: TaskKind) -> RouteDecision:
        env_tag = self._env_tag_for(task)
        if env_tag:
            return RouteDecision(
                model=LocalModelSpec(
                    ollama_tag=env_tag,
                    family=env_tag.split(":", 1)[0],
                    approx_size_gb=0.0,
                    min_ram_gb=0.0,
                    tier=self._capacity.tier,
                    tasks=(task,),
                    arabic_quality=3,
                    english_quality=3,
                    notes="Explicit env override",
                ),
                tier=self._capacity.tier,
                task=task,
                reason="env override",
                available=True,
            )

        spec = pick_model_for_task(
            task,
            self._capacity.tier,
            prefer_arabic=self.prefer_arabic,
        )
        if spec is None:
            return RouteDecision(
                model=None,
                tier=self._capacity.tier,
                task=task,
                reason="no catalogued model fits this tier",
                available=False,
            )
        return RouteDecision(
            model=spec,
            tier=self._capacity.tier,
            task=task,
            reason="catalog pick",
            available=True,
        )

    # ── run ─────────────────────────────────────────────────────

    async def run(
        self,
        task: str,
        prompt: str,
        *,
        system: str = "",
        temperature: float = 0.3,
        max_tokens: int = 1024,
        json_mode: bool = False,
        race: bool = False,
    ) -> OllamaChatResult:
        """
        Execute a task against the best local model. If `race=True` and a
        second candidate model is catalogued for this tier, run both in
        parallel and return the better-scored response.
        """
        if not self.is_enabled():
            return OllamaChatResult(
                model="(disabled)",
                content="",
                latency_ms=0,
                success=False,
                error="LOCAL_LLM_ENABLED is off",
            )
        if not await self.client.health():
            return OllamaChatResult(
                model="(offline)",
                content="",
                latency_ms=0,
                success=False,
                error="Ollama daemon is not reachable",
            )

        task_kind = self.resolve_task(task)
        primary_decision = self.decide(task_kind)
        if not primary_decision.available or primary_decision.model is None:
            return OllamaChatResult(
                model="(none)",
                content="",
                latency_ms=0,
                success=False,
                error=primary_decision.reason,
            )

        messages = [{"role": "user", "content": prompt}]
        primary_tag = primary_decision.model.ollama_tag

        if not race:
            return await self.client.chat(
                model=primary_tag,
                messages=messages,
                system=system or None,
                temperature=temperature,
                max_tokens=max_tokens,
                json_mode=json_mode,
            )

        # Race a second candidate if one exists and differs from primary.
        from app.services.local_ai.catalog import MODEL_CATALOG
        alternates = [
            m for m in MODEL_CATALOG
            if task_kind in m.tasks
            and m.ollama_tag != primary_tag
            and self._capacity.tier.value in {
                t.value for t in ServerTier if t.value <= self._capacity.tier.value
            }
        ]
        if not alternates:
            return await self.client.chat(
                model=primary_tag, messages=messages, system=system or None,
                temperature=temperature, max_tokens=max_tokens, json_mode=json_mode,
            )
        alt = alternates[0]

        primary_task = self.client.chat(
            model=primary_tag, messages=messages, system=system or None,
            temperature=temperature, max_tokens=max_tokens, json_mode=json_mode,
        )
        alt_task = self.client.chat(
            model=alt.ollama_tag, messages=messages, system=system or None,
            temperature=temperature, max_tokens=max_tokens, json_mode=json_mode,
        )
        a, b = await asyncio.gather(primary_task, alt_task, return_exceptions=False)
        winner = _pick_better_result(a, b)
        logger.info(
            "local race: %s vs %s → winner=%s",
            primary_tag, alt.ollama_tag, winner.model,
        )
        return winner


def _pick_better_result(a: OllamaChatResult, b: OllamaChatResult) -> OllamaChatResult:
    """
    Lightweight evaluator used for racing. Prefers the successful response;
    among successes, prefers the one with more content but less filler.
    """
    if a.success and not b.success:
        return a
    if b.success and not a.success:
        return b
    if not a.success and not b.success:
        # Both failed — return the one with the lower latency (likely a real error).
        return a if a.latency_ms <= b.latency_ms else b

    def quality(r: OllamaChatResult) -> float:
        text = r.content.strip()
        if not text:
            return 0.0
        length = len(text)
        # Penalize suspiciously short or absurdly long responses.
        if length < 40:
            return length * 0.5
        # Diminishing returns past ~1500 chars.
        base = min(length, 1500) + (length - 1500) * 0.1 if length > 1500 else length
        # Structured responses (JSON/markdown lists) slightly preferred.
        if text.startswith("{") or text.startswith("["):
            base *= 1.05
        if "\n- " in text or "\n* " in text or "\n1." in text:
            base *= 1.03
        return base

    return a if quality(a) >= quality(b) else b


# ── Module-level singleton ─────────────────────────────────────────

_router: Optional[LocalModelRouter] = None


def get_local_router() -> LocalModelRouter:
    global _router
    if _router is None:
        _router = LocalModelRouter()
    return _router
