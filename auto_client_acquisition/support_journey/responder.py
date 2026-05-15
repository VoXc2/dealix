"""Stage-specific draft responder.

Wraps support_os.responder.draft_response and adds stage-specific
context. Always returns draft_only or approval_required (NEVER live send).
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.integration_upgrade import hide_internal_terms

_STAGE_PREAMBLE_AR: dict[str, str] = {
    "pre_sales": "شكراً لاهتمامك بـ Dealix.",
    "onboarding": "أهلاً بك في Dealix — نساعدك تبدأ بسرعة.",
    "delivery": "نشتغل على طلبك الآن.",
    "billing": "هذا الموضوع يخص الفواتير ويحتاج مراجعة المؤسس قبل الردّ.",
    "proof": "خصوص دلائل الأداء (Proof Pack).",
    "renewal": "خصوص تجديد الباقة.",
    "privacy": "هذا الموضوع يخص PDPL ويصعّد للمؤسس فوراً.",
}

_STAGE_PREAMBLE_EN: dict[str, str] = {
    "pre_sales": "Thanks for your interest in Dealix.",
    "onboarding": "Welcome to Dealix — we'll help you start fast.",
    "delivery": "Working on your request now.",
    "billing": "This is a billing matter and requires founder review before reply.",
    "proof": "Regarding proof-pack metrics.",
    "renewal": "Regarding package renewal.",
    "privacy": "This is a PDPL matter and is escalated to the founder immediately.",
}


def draft_stage_reply(
    *,
    message_text: str,
    journey_stage: str,
    customer_handle: str | None = None,
) -> dict[str, Any]:
    """Wraps support_os.responder.draft_response + adds stage preamble.

    Returns a draft. action_mode is ALWAYS draft_only or approval_required.
    """
    from auto_client_acquisition.support_os.classifier import classify_message
    from auto_client_acquisition.support_os.responder import draft_response

    classification = classify_message(message_text)
    base = draft_response(message=message_text, classification=classification)

    preamble_ar = _STAGE_PREAMBLE_AR.get(journey_stage, "")
    preamble_en = _STAGE_PREAMBLE_EN.get(journey_stage, "")

    # Stage-specific action_mode override
    if journey_stage in ("billing", "privacy"):
        action_mode = "approval_required"
    else:
        action_mode = base.action_mode  # draft_only or approval_required

    return {
        "journey_stage": journey_stage,
        "category": classification.category,
        "action_mode": action_mode,
        "text_ar": hide_internal_terms(f"{preamble_ar}\n\n{base.text_ar}"),
        "text_en": hide_internal_terms(f"{preamble_en}\n\n{base.text_en}"),
        "insufficient_evidence": base.insufficient_evidence,
        "would_send_live": False,
        "safety_summary": "no_live_send_draft_only_no_guaranteed_claims",
    }
