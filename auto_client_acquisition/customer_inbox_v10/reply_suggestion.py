"""Deterministic reply suggester. NEVER auto-sends.

Templates are stage-keyed and bilingual. action_mode is always
``draft_only``, ``approval_required``, or ``blocked`` — never
``approved_execute``.
"""
from __future__ import annotations

from auto_client_acquisition.customer_inbox_v10.schemas import (
    ConsentStatus,
    Conversation,
    ReplySuggestion,
)


_TEMPLATES_AR: dict[str, str] = {
    "lead_intake": (
        "شكراً لتواصلك معنا. هل يمكنك مشاركتي تحدّيك الرئيسي حالياً "
        "حتى أرشّح لك الخطوة التالية المناسبة؟"
    ),
    "diagnostic": (
        "بناءً على ما شاركته، أقترح جلسة تشخيص قصيرة (٣٠ دقيقة) "
        "لتحديد أهم فرصتين قابلتين للتنفيذ."
    ),
    "proposal": (
        "إليك ملخص مقترح يحدد النطاق والمخرجات المتوقعة. "
        "أي تعديل قبل الاعتماد؟"
    ),
    "delivery": "تحديث التسليم: المرحلة الحالية على المسار. هل لديك ملاحظات؟",
    "renewal": "نقترب من نهاية الفترة الحالية — هل نحجز مراجعة قصيرة؟",
}

_TEMPLATES_EN: dict[str, str] = {
    "lead_intake": (
        "Thanks for reaching out. Could you share your top current "
        "challenge so I can suggest the right next step?"
    ),
    "diagnostic": (
        "Based on what you shared, I'd suggest a 30-minute diagnostic "
        "to surface the two highest-leverage opportunities."
    ),
    "proposal": (
        "Here's a short proposal scoping the deliverables. "
        "Any tweaks before approval?"
    ),
    "delivery": "Delivery update: current milestone on track. Any feedback?",
    "renewal": "We're approaching the end of the current period — book a short review?",
}


def suggest_reply(conv: Conversation) -> ReplySuggestion:
    """Suggest a draft reply for the conversation.

    Always returns ``action_mode in {"draft_only", "approval_required", "blocked"}``.
    Never auto-approves.
    """
    consent_value = (
        conv.consent_status.value
        if isinstance(conv.consent_status, ConsentStatus)
        else str(conv.consent_status)
    )

    if consent_value == ConsentStatus.BLOCKED.value:
        return ReplySuggestion(
            conversation_id=conv.id,
            suggested_text_ar="",
            suggested_text_en="",
            action_mode="blocked",
            blocked_reason="consent_status=blocked — no outbound permitted",
        )

    if consent_value == ConsentStatus.WITHDRAWN.value:
        return ReplySuggestion(
            conversation_id=conv.id,
            suggested_text_ar="",
            suggested_text_en="",
            action_mode="blocked",
            blocked_reason="consent_status=withdrawn — no outbound permitted",
        )

    stage = (conv.customer_stage or "lead_intake").lower()
    text_ar = _TEMPLATES_AR.get(stage, _TEMPLATES_AR["lead_intake"])
    text_en = _TEMPLATES_EN.get(stage, _TEMPLATES_EN["lead_intake"])

    # If consent is unknown, raise the bar to approval_required for human gate.
    if consent_value == ConsentStatus.UNKNOWN.value:
        action_mode = "approval_required"
    else:
        action_mode = "draft_only"

    return ReplySuggestion(
        conversation_id=conv.id,
        suggested_text_ar=text_ar,
        suggested_text_en=text_en,
        action_mode=action_mode,
        blocked_reason="",
    )
