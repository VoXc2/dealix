"""Phone calls channel policy."""
from __future__ import annotations

from auto_client_acquisition.channel_policy_gateway.schemas import (
    ActionKind,
    PolicyDecision,
)


def calls_policy(
    *,
    action_kind: ActionKind,
    customer_permission: bool = False,
    live_gate_true: bool = False,
    human_approved: bool = False,
) -> PolicyDecision:
    if action_kind == "draft":
        return PolicyDecision(
            channel="calls",
            action_kind=action_kind,
            allowed=True,
            action_mode="draft_only",
            reason_ar="مسموح كتابة سيناريو المكالمة.",
            reason_en="Call script drafting allowed.",
        )
    if action_kind == "send_live":
        if customer_permission and live_gate_true and human_approved:
            return PolicyDecision(
                channel="calls",
                action_kind=action_kind,
                allowed=True,
                action_mode="approved_manual",
                reason_ar="مسموح اتصال يدوي بعد موافقة العميل والمؤسس.",
                reason_en="Approved manual dial after customer + founder approval.",
            )
        missing = []
        if not customer_permission: missing.append("customer_permission")
        if not live_gate_true: missing.append("live_gate_true")
        if not human_approved: missing.append("human_approved")
        return PolicyDecision(
            channel="calls",
            action_kind=action_kind,
            allowed=False,
            action_mode="blocked",
            reason_ar="ممنوع اتصال حيّ بدون إذن العميل + gate + موافقة.",
            reason_en="Live dial blocked without customer permission + gate + approval.",
            required_conditions=["customer_permission", "live_gate_true", "human_approved"],
            missing_conditions=missing,
        )
    return PolicyDecision(
        channel="calls",
        action_kind=action_kind,
        allowed=True,
        action_mode="draft_only",
        reason_ar="إجراء غير ضارّ — مسوّدة.",
        reason_en="Non-harmful action — draft only.",
    )
