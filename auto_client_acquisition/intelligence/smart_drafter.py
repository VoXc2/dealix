"""
SmartDrafter — wraps core.llm.router.ModelRouter with:
  - Saudi-tone Arabic system prompts
  - per-Brain personalization (offer / ICP / tone / forbidden_claims)
  - assert_safe() on every output BEFORE returning
  - graceful fallback to deterministic template on:
      * no LLM provider configured
      * provider error
      * LLM produced unsafe content (forbidden claim)

Returns a `DraftResult` so callers can audit which path was used + emit
the right RWU.

Usage:
    drafter = SmartDrafter()
    r = await drafter.draft_outreach_message(
        brain={"offer_ar":"...","ideal_customer_ar":"...","tone_ar":"..."},
        prospect_hint="مدير مبيعات في وكالة ريادة B2B",
        fallback="السلام عليكم، ...",
    )
    if r.text:
        emit_proof_event(meta={"draft_text": r.text, "provider": r.provider})
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.compliance.forbidden_claims import (
    ForbiddenClaimError,
    assert_safe,
)

log = logging.getLogger(__name__)


@dataclass
class DraftResult:
    text: str
    used_llm: bool
    provider: str | None
    fallback_used: bool
    fallback_reason: str | None
    safety_passed: bool
    input_tokens: int = 0
    output_tokens: int = 0


class SmartDrafter:
    """LLM-aware drafter with safety + deterministic fallback.

    Designed so tests run without API keys: if no provider is configured,
    `_router.run()` will either raise (no clients) or be mocked. Either way,
    `draft_*()` returns a DraftResult that says fallback_used=True.
    """

    SAUDI_TONE_SYSTEM_PROMPT = (
        "أنت مساعد محترف لكتابة رسائل B2B عربية موجَّهة للسوق السعودي. "
        "نبرتك: محترمة، مباشرة، بدون مبالغة. "
        "ممنوع تماماً: \"نضمن\"، \"guaranteed\"، أي وعد بنتائج محددة. "
        "ممنوع تماماً: cold outreach للأرقام المشتراة، scraping، LinkedIn automation. "
        "كل رسالة لازم تذكر next-step واضح + خيار 'STOP' للإلغاء."
    )

    def __init__(self, router: Any | None = None):
        # Lazy: router built on first use so test environments without
        # API keys don't blow up at import time.
        self._router = router
        self._router_attempted = False

    def _get_router(self):
        if self._router is not None:
            return self._router
        if self._router_attempted:
            return None
        self._router_attempted = True
        try:
            from core.llm.router import get_router
            r = get_router()
            if not r.available_providers():
                log.info("smart_drafter: no LLM providers configured — fallback path active")
                return None
            self._router = r
            return r
        except Exception as exc:  # noqa: BLE001
            log.info("smart_drafter: ModelRouter unavailable (%s) — fallback path active", exc)
            return None

    async def _safe_run(
        self,
        task_kind: str,
        prompt: str,
        *,
        system: str | None = None,
        max_tokens: int = 600,
        temperature: float = 0.7,
        fallback: str = "",
    ) -> DraftResult:
        """Execute LLM call with safety scanning + fallback.

        task_kind is one of the values in core.config.models.Task. We import
        lazily to avoid hard dependency at module import time.
        """
        router = self._get_router()
        if router is None:
            return DraftResult(
                text=fallback,
                used_llm=False,
                provider=None,
                fallback_used=True,
                fallback_reason="no_provider_configured",
                safety_passed=True,  # fallback text is hand-crafted safe
            )

        try:
            from core.config.models import Task
            from core.llm.base import Message
            task = getattr(Task, task_kind, None) or Task.REASONING
            response = await router.run(
                task=task,
                messages=[Message(role="user", content=prompt)],
                system=system or self.SAUDI_TONE_SYSTEM_PROMPT,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            text = (response.content or "").strip()
        except Exception as exc:  # noqa: BLE001
            log.warning("smart_drafter: LLM run failed (%s) — using fallback", exc)
            return DraftResult(
                text=fallback,
                used_llm=False,
                provider=None,
                fallback_used=True,
                fallback_reason=f"llm_error:{type(exc).__name__}",
                safety_passed=True,
            )

        # Safety scan — must pass before return
        try:
            assert_safe(text)
        except ForbiddenClaimError as exc:
            log.warning(
                "smart_drafter: LLM output contained forbidden claim %r — using fallback",
                exc.claim,
            )
            return DraftResult(
                text=fallback,
                used_llm=False,
                provider=getattr(response, "provider", None),
                fallback_used=True,
                fallback_reason=f"unsafe_claim:{exc.claim}",
                safety_passed=False,
            )

        return DraftResult(
            text=text,
            used_llm=True,
            provider=getattr(response, "provider", None),
            fallback_used=False,
            fallback_reason=None,
            safety_passed=True,
            input_tokens=getattr(response, "input_tokens", 0),
            output_tokens=getattr(response, "output_tokens", 0),
        )

    # ── Public methods (one per draft type) ──────────────────────

    async def draft_outreach_message(
        self,
        brain: dict[str, Any],
        *,
        prospect_hint: str = "",
        prospect_recent_signal: str = "",
        fallback: str = "",
    ) -> DraftResult:
        """Generate one Saudi-tone Arabic LinkedIn warm-intro message."""
        company = brain.get("company_name", "—")
        offer = brain.get("offer_ar", "خدمات الشركة")
        icp = brain.get("ideal_customer_ar", "شركات سعودية B2B")
        forbidden = ", ".join(brain.get("forbidden_claims", []) or ["نضمن", "guaranteed"])
        prompt = (
            f"اكتب رسالة LinkedIn warm-intro واحدة (3-5 أسطر، عربية، محترمة).\n"
            f"شركتي: {company}\n"
            f"عرضي: {offer}\n"
            f"العميل المثالي: {icp}\n"
            f"المخاطَب: {prospect_hint or 'مؤسس / مدير في شركة سعودية B2B'}\n"
            f"إشارة حديثة (إن وُجدت): {prospect_recent_signal or '(لا شيء — لا تختلق)'}\n\n"
            f"شروط صارمة:\n"
            f"- لا تستخدم: {forbidden}\n"
            f"- لا تَعِد بنتائج محددة\n"
            f"- اطلب 15 دقيقة، ليس بيع مباشر\n"
            f"- اذكر 'STOP' للإلغاء في النهاية\n"
            f"- إذا لا توجد إشارة حقيقية، لا تختلقها — استخدم سؤالاً عاماً\n\n"
            f"أعد فقط نصّ الرسالة، بدون شرح أو ترقيم أسطر."
        )
        return await self._safe_run(
            "PROPOSAL", prompt, max_tokens=400, temperature=0.7, fallback=fallback,
        )

    async def draft_followup(
        self,
        brain: dict[str, Any],
        *,
        days_since_last: int = 5,
        fallback: str = "",
    ) -> DraftResult:
        """Polite follow-up to a non-replier."""
        prompt = (
            f"اكتب رسالة follow-up قصيرة (سطرين-ثلاثة) بنبرة محترمة سعودية. "
            f"مرّت {days_since_last} أيام بدون رد. "
            f"لا ضغط. اعرض async option (1-page summary) كبديل عن الاجتماع. "
            f"اطلب رد بسطر واحد فقط 'مهتم/غير مناسب الآن/ابعد عني'. "
            f"اذكر 'STOP' في النهاية."
        )
        return await self._safe_run(
            "FAST_VARIANTS", prompt, max_tokens=200, temperature=0.6, fallback=fallback,
        )

    async def draft_objection_response(
        self,
        brain: dict[str, Any],
        *,
        objection_text: str,
        fallback: str = "",
    ) -> DraftResult:
        """Generate response to a customer objection with brain context."""
        offer = brain.get("offer_ar", "خدمات الشركة")
        prompt = (
            f"العميل قال: \"{objection_text}\".\n"
            f"اكتب رد بنبرة سعودية محترمة + قصيرة (3-4 أسطر).\n"
            f"عرضي: {offer}.\n"
            f"القاعدة: لا تخفض السعر. اقترح Pilot 499 SAR لمدة 7 أيام كنقطة دخول صغيرة.\n"
            f"لا تَعِد بنتائج محددة. لا تستخدم 'نضمن' أو 'guaranteed'.\n"
            f"أعد نص الرد فقط."
        )
        return await self._safe_run(
            "REASONING", prompt, max_tokens=300, temperature=0.7, fallback=fallback,
        )

    async def clarify_intent(
        self,
        user_message: str,
        *,
        fallback: str = "",
    ) -> DraftResult:
        """When the keyword classifier returns low confidence, ask one
        clarifying intake question."""
        prompt = (
            f"العميل كتب: \"{user_message}\".\n\n"
            f"النية غير واضحة. اطرح سؤالاً واحداً صغيراً (سطر-سطرين) لفهم:\n"
            f"- هل يريد عملاء جدد، تنظيف قائمة، شراكات، أو تشغيل يومي؟\n"
            f"- ما حجم الشركة؟\n"
            f"- ما القناة المفضلة؟\n\n"
            f"اختر أهم سؤال واحد فقط. عربي. ودود. لا قائمة طويلة."
        )
        return await self._safe_run(
            "CLASSIFICATION", prompt, max_tokens=200, temperature=0.5, fallback=fallback,
        )


# Module-level singleton — built lazily on first use
_drafter: SmartDrafter | None = None


def get_drafter() -> SmartDrafter:
    global _drafter
    if _drafter is None:
        _drafter = SmartDrafter()
    return _drafter
