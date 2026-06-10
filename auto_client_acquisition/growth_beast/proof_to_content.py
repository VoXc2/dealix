"""Proof → content idea (approval-required)."""
from __future__ import annotations


def proof_to_content_idea(*, proof_event: dict) -> dict:
    """Turn a real proof event into a content draft. NEVER fabricates."""
    if not proof_event or not proof_event.get("action_taken"):
        return {
            "blocked": True,
            "reason_ar": "لا proof event صالح — لا تنشر",
            "reason_en": "No valid proof event — do not publish.",
            "action_mode": "blocked",
        }
    if not proof_event.get("customer_approved"):
        return {
            "blocked": True,
            "reason_ar": "العميل لم يوافق — لا نشر",
            "reason_en": "Customer hasn't approved — no publish.",
            "action_mode": "approval_required",
        }
    action = proof_event["action_taken"]
    return {
        "blocked": False,
        "draft_ar": f"خلال أسبوع: {action} — التفاصيل بإذن العميل.",
        "draft_en": f"In one week: {action} — details only with customer permission.",
        "action_mode": "approval_required",
        "audience": "internal_only",
        "publish_requires": "signed_customer_permission",
    }
