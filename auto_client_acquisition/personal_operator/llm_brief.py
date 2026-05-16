"""LLM-driven daily brief generator (Track C2 of 30-day plan).

Augments the existing `build_daily_brief` (deterministic) with an
LLM-summarized founder-tone Markdown narrative. Falls back gracefully
to the deterministic version when:
  - No LLM API key configured
  - LLM call times out / rate-limited
  - Insufficient real data (returns "insufficient_data" status)

Per Master Plan §V.B #2 — this closes the gap between today's stub
brief and a true "smart enough to run with API keys" operator.

Hard rules:
  - NEVER invents leads, customers, revenue, or events
  - Reads from existing Wave 3 data sources (proof_ledger, approvals,
    inbound queue) — no scraping, no synthesis from external sources
  - All output is Markdown (renderable in customer-portal + WhatsApp)
  - Budget: max 600 input tokens + 300 output tokens per call
  - Reduced motion / accessibility: brief is text-only, no images
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

logger = logging.getLogger(__name__)

# Token budget per Master Plan §IV.D (cost discipline)
MAX_INPUT_TOKENS = 600
MAX_OUTPUT_TOKENS = 300
LLM_TIMEOUT_SECONDS = 8.0


@dataclass(frozen=True)
class LLMBrief:
    """LLM-generated narrative on top of deterministic brief."""

    headline: str
    narrative: str
    next_action: str
    data_status: str  # "live" | "insufficient_data" | "fallback"
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    duration_ms: int = 0
    model_used: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "headline": self.headline,
            "narrative": self.narrative,
            "next_action": self.next_action,
            "data_status": self.data_status,
            "generated_at": self.generated_at.isoformat(),
            "duration_ms": self.duration_ms,
            "model_used": self.model_used,
        }


SYSTEM_PROMPT_AR = """\
أنت مساعد المؤسس Sami في Dealix. مهمّتك: تلخيص حالة الشركة في تقرير يوميّ
مختصر، بصيغة سعوديّة خليجيّة، Markdown، صادق، بدون مبالغة.

قواعد إلزاميّة:
1. لا تخترع leads أو عملاء أو أرقام إيراد. استخدم فقط ما يُعطى لك.
2. لا تستخدم كلمات: "نضمن"، "10x"، "revolutionary"، "guaranteed".
3. كل رقم SAR يجب أن يكون مدعوماً بـ evidence_id من البيانات المُعطاة.
4. الجواب: 3 أقسام فقط — Headline (سطر)، Narrative (3-5 جمل)، Next Action (سطر).
5. لو البيانات قليلة، قل "insufficient_data" وأعطِ next action واحد محدّد.
"""


def _format_input_data(
    proof_events: list[dict[str, Any]] | None,
    pending_approvals: list[dict[str, Any]] | None,
    inbound_count: int,
) -> str:
    """Compact data summary for the LLM. Stays well under MAX_INPUT_TOKENS."""
    proof_count = len(proof_events or [])
    l5_count = sum(
        1 for e in (proof_events or []) if (e.get("level") or "").upper() == "L5"
    )
    approval_count = len(pending_approvals or [])
    sample_approvals = (pending_approvals or [])[:3]

    lines = [
        f"- Proof events (آخر 24 ساعة): {proof_count} (منها L5: {l5_count})",
        f"- موافقات معلّقة: {approval_count}",
        f"- inbound queue: {inbound_count}",
    ]
    if sample_approvals:
        lines.append("\nأبرز الموافقات المعلّقة:")
        for a in sample_approvals:
            mode = a.get("mode") or a.get("action_type") or "approval"
            title = (a.get("title") or a.get("summary_ar") or "—")[:80]
            lines.append(f"  • [{mode}] {title}")
    return "\n".join(lines)


async def _call_llm(system_prompt: str, user_input: str) -> tuple[str, str]:
    """Call LLM router. Returns (text, model_used). Raises on failure."""
    try:
        from core.llm.base import Message
        from core.llm.router import get_router
    except ImportError as exc:
        raise RuntimeError(f"LLM router unavailable: {exc}") from exc

    router = get_router()
    messages = [
        Message(role="system", content=system_prompt),
        Message(role="user", content=user_input),
    ]
    response = await asyncio.wait_for(
        router.complete(
            messages=messages,
            max_tokens=MAX_OUTPUT_TOKENS,
            temperature=0.3,
        ),
        timeout=LLM_TIMEOUT_SECONDS,
    )
    return response.content, getattr(response, "model", "unknown")


def _parse_brief(text: str) -> tuple[str, str, str]:
    """Parse LLM output into (headline, narrative, next_action)."""
    headline = ""
    narrative = ""
    next_action = ""
    current_section = None
    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line:
            continue
        lower = line.lower()
        if lower.startswith("headline") or line.startswith("##"):
            current_section = "headline"
            headline = line.split(":", 1)[-1].lstrip("# ").strip()
            continue
        if lower.startswith("narrative") or "narrative" in lower[:20]:
            current_section = "narrative"
            content = line.split(":", 1)[-1].strip()
            if content and content != line.split(":", 1)[0]:
                narrative = content
            continue
        if lower.startswith("next action") or "next_action" in lower:
            current_section = "next_action"
            next_action = line.split(":", 1)[-1].strip()
            continue
        if current_section == "narrative":
            narrative = (narrative + " " + line).strip()
        elif current_section == "next_action":
            next_action = (next_action + " " + line).strip()
        elif not headline:
            headline = line
        elif not narrative:
            narrative = line
        elif not next_action:
            next_action = line
    if not headline and text:
        headline = text.split("\n", 1)[0][:120]
    if not narrative:
        narrative = text[:400]
    if not next_action:
        next_action = "راجع pending approvals في /decisions.html"
    return headline, narrative, next_action


def _fallback_brief(
    proof_events: list[dict[str, Any]] | None,
    pending_approvals: list[dict[str, Any]] | None,
    inbound_count: int,
) -> LLMBrief:
    """Deterministic fallback when LLM unavailable. Honest + safe."""
    proof_count = len(proof_events or [])
    approval_count = len(pending_approvals or [])
    has_data = proof_count > 0 or approval_count > 0 or inbound_count > 0
    if not has_data:
        return LLMBrief(
            headline="لا بيانات حقيقيّة بعد",
            narrative=(
                "لم تُسجَّل proof events أو موافقات أو inbound في آخر 24 ساعة. "
                "هذا متوقّع قبل أوّل pilot. ركّز على warm intros يدوية مع موافقة صريحة."
            ),
            next_action=(
                "ابدأ بـ warm-intro واحد يدوي مع موافقة صريحة، ثم جرّب POST "
                "/api/v1/leads لتوليد Decision Passport (diagnostic أوّلي)"
            ),
            data_status="insufficient_data",
            duration_ms=0,
            model_used=None,
        )
    bits = []
    if proof_count:
        bits.append(f"{proof_count} proof event")
    if approval_count:
        bits.append(f"{approval_count} موافقة معلّقة")
    if inbound_count:
        bits.append(f"{inbound_count} رسالة inbound")
    return LLMBrief(
        headline="ملخّص اليوم — fallback mode",
        narrative=(
            f"عندك: {' · '.join(bits)}. (LLM غير متاح، عرض deterministic.)"
        ),
        next_action=(
            f"راجع {approval_count} موافقة في /decisions.html"
            if approval_count
            else "افتح Customer Portal لتحديث البيانات"
        ),
        data_status="fallback",
        duration_ms=0,
        model_used=None,
    )


async def generate_llm_brief(
    proof_events: list[dict[str, Any]] | None = None,
    pending_approvals: list[dict[str, Any]] | None = None,
    inbound_count: int = 0,
) -> LLMBrief:
    """Generate a founder-tone daily brief.

    Always returns a valid LLMBrief — never raises.
    Tries LLM first; falls back to deterministic on any failure.
    """
    start = time.monotonic()
    user_input = _format_input_data(proof_events, pending_approvals, inbound_count)

    try:
        text, model = await _call_llm(SYSTEM_PROMPT_AR, user_input)
        headline, narrative, next_action = _parse_brief(text)
        duration_ms = int((time.monotonic() - start) * 1000)
        return LLMBrief(
            headline=headline,
            narrative=narrative,
            next_action=next_action,
            data_status="live",
            duration_ms=duration_ms,
            model_used=model,
        )
    except (TimeoutError, asyncio.TimeoutError):
        logger.warning("daily_brief_llm_timeout")
    except Exception as exc:  # noqa: BLE001 — graceful fallback always
        logger.warning("daily_brief_llm_failed: %s", exc)

    brief = _fallback_brief(proof_events, pending_approvals, inbound_count)
    return brief


async def fetch_recent_proof_events(window_hours: int = 24) -> list[dict[str, Any]]:
    """Pull last 24h proof events from in-memory ledger.

    Returns [] if proof_ledger module is unavailable in this environment
    (e.g. during static-site smoke tests).
    """
    try:
        from auto_client_acquisition.proof_ledger import recent_events  # type: ignore
    except ImportError:
        return []
    cutoff = datetime.now(UTC) - timedelta(hours=window_hours)
    try:
        events = recent_events(since=cutoff) or []
        return [e if isinstance(e, dict) else e.__dict__ for e in events]
    except Exception:  # noqa: BLE001
        return []


async def fetch_pending_approvals() -> list[dict[str, Any]]:
    try:
        from auto_client_acquisition.approval_center import list_pending  # type: ignore
    except ImportError:
        return []
    try:
        items = list_pending() or []
        return [a if isinstance(a, dict) else a.__dict__ for a in items]
    except Exception:  # noqa: BLE001
        return []


async def fetch_inbound_count() -> int:
    try:
        from auto_client_acquisition.support_inbox import inbound_pending_count  # type: ignore
    except ImportError:
        return 0
    try:
        return int(inbound_pending_count() or 0)
    except Exception:  # noqa: BLE001
        return 0
