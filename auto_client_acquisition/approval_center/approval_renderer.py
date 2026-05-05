"""Render an ApprovalRequest as a bilingual approval card.

The card is a plain dict — UI-agnostic. Frontends (founder console,
Slack/WhatsApp bots, email digests) bind to the same structure.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus,
)


_RISK_BADGE_AR = {
    "low": "مخاطرة منخفضة",
    "medium": "مخاطرة متوسطة",
    "high": "مخاطرة عالية",
    "blocked": "محظور",
}

_RISK_BADGE_EN = {
    "low": "Low risk",
    "medium": "Medium risk",
    "high": "High risk",
    "blocked": "Blocked",
}


def render_approval_card(req: ApprovalRequest) -> dict[str, Any]:
    """Return a bilingual approval card for the given request."""
    risk_key = (req.risk_level or "low").lower()
    status = ApprovalStatus(req.status)

    title_ar = f"اعتماد مطلوب: {req.action_type} ({req.object_type})"
    title_en = f"Approval needed: {req.action_type} ({req.object_type})"

    recommended_ar = "اعتمد إذا الرسالة دقيقة والتوقيت مناسب."
    recommended_en = "Approve if the message is accurate and the timing is right."
    if status == ApprovalStatus.BLOCKED:
        recommended_ar = "محظور بسياسة. لا يمكن اعتماده."
        recommended_en = "Blocked by policy. Cannot be approved."

    why_now_ar = req.proof_impact or "إجراء يحتاج موافقة بشرية قبل التنفيذ."
    why_now_en = req.proof_impact or "Action requires human approval before execution."

    # Buttons — disabled when terminal status reached.
    can_act = status == ApprovalStatus.PENDING
    buttons = [
        {"id": "approve", "label_ar": "اعتماد", "label_en": "Approve", "enabled": can_act},
        {"id": "reject", "label_ar": "رفض", "label_en": "Reject", "enabled": can_act},
        {"id": "edit", "label_ar": "تعديل", "label_en": "Edit", "enabled": can_act},
    ]

    return {
        "approval_id": req.approval_id,
        "object_type": req.object_type,
        "object_id": req.object_id,
        "action_type": req.action_type,
        "action_mode": req.action_mode,
        "channel": req.channel,
        "status": status.value,
        "title_ar": title_ar,
        "title_en": title_en,
        "summary_ar": req.summary_ar,
        "summary_en": req.summary_en,
        "risk_level": risk_key,
        "risk_badge_ar": _RISK_BADGE_AR.get(risk_key, risk_key),
        "risk_badge_en": _RISK_BADGE_EN.get(risk_key, risk_key),
        "proof_impact": req.proof_impact,
        "recommended_action_ar": recommended_ar,
        "recommended_action_en": recommended_en,
        "why_now_ar": why_now_ar,
        "why_now_en": why_now_en,
        "buttons": buttons,
    }
