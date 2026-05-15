"""Email channel policy."""
from __future__ import annotations

from auto_client_acquisition.channel_policy_gateway.schemas import (
    ActionKind,
    PolicyDecision,
)


def email_policy(
    *,
    action_kind: ActionKind,
    live_gate_true: bool = False,
    human_approved: bool = False,
) -> PolicyDecision:
    if action_kind == "draft":
        return PolicyDecision(
            channel="email",
            action_kind=action_kind,
            allowed=True,
            action_mode="draft_only",
            reason_ar="مسموح صياغة مسوّدة.",
            reason_en="Drafting allowed.",
        )
    if action_kind in ("send_live",):
        if live_gate_true and human_approved:
            return PolicyDecision(
                channel="email",
                action_kind=action_kind,
                allowed=True,
                action_mode="approved_manual",
                reason_ar="مسموح إرسال يدوي بعد الموافقة.",
                reason_en="Approved manual send permitted.",
            )
        missing = []
        if not live_gate_true:
            missing.append("live_gate_true")
        if not human_approved:
            missing.append("human_approved")
        return PolicyDecision(
            channel="email",
            action_kind=action_kind,
            allowed=False,
            action_mode="blocked",
            reason_ar="ممنوع إرسال حيّ بدون gate + موافقة.",
            reason_en="Live send blocked without gate + approval.",
            required_conditions=["live_gate_true", "human_approved"],
            missing_conditions=missing,
        )
    return PolicyDecision(
        channel="email",
        action_kind=action_kind,
        allowed=True,
        action_mode="draft_only",
        reason_ar="إجراء غير ضارّ — مسوّدة.",
        reason_en="Non-harmful action — draft only.",
    )
