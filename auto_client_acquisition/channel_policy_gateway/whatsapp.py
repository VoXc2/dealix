"""WhatsApp channel policy."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.channel_policy_gateway.schemas import (
    ActionKind,
    PolicyDecision,
)


def whatsapp_policy(
    *,
    action_kind: ActionKind,
    consent_record_exists: bool = False,
    approved_template_or_24h_window: bool = False,
    live_gate_true: bool = False,
    human_approved: bool = False,
    is_cold: bool = False,
    is_blast: bool = False,
    is_purchased_list: bool = False,
) -> PolicyDecision:
    """Evaluate a WhatsApp action under the 4-condition customer-outbound rule."""

    if is_cold or is_blast or is_purchased_list:
        reasons = []
        if is_cold:
            reasons.append("cold_whatsapp")
        if is_blast:
            reasons.append("broadcast_blast")
        if is_purchased_list:
            reasons.append("purchased_list")
        return PolicyDecision(
            channel="whatsapp",
            action_kind=action_kind,
            allowed=False,
            action_mode="blocked",
            reason_ar="ممنوع: WhatsApp بارد أو إرسال جماعي أو قائمة مشتراة.",
            reason_en="Blocked: cold WhatsApp, broadcast, or purchased list.",
            safe_alternative_ar="استخدم رسالة شخصيّة لجهة على علاقة قائمة معك.",
            safe_alternative_en="Use a personal message to an existing relationship.",
            missing_conditions=reasons,
        )

    if action_kind == "internal_brief":
        return PolicyDecision(
            channel="whatsapp",
            action_kind=action_kind,
            allowed=True,
            action_mode="internal_only",
            reason_ar="مسموح: ملخّص داخلي للمؤسس/CSM فقط — لا إرسال للعميل.",
            reason_en="Allowed: internal brief for founder/CSM only — no customer send.",
            required_conditions=["internal_admin_only"],
        )

    # Customer outbound — 4 conditions required
    required = [
        "consent_record_exists",
        "approved_template_or_24h_window",
        "live_gate_true",
        "human_approved",
    ]
    missing: list[str] = []
    if not consent_record_exists:
        missing.append("consent_record_exists")
    if not approved_template_or_24h_window:
        missing.append("approved_template_or_24h_window")
    if not live_gate_true:
        missing.append("live_gate_true")
    if not human_approved:
        missing.append("human_approved")

    if missing:
        return PolicyDecision(
            channel="whatsapp",
            action_kind=action_kind,
            allowed=False,
            action_mode="blocked",
            reason_ar=f"ممنوع: تنقص شروط ({len(missing)}).",
            reason_en=f"Blocked: {len(missing)} required condition(s) missing.",
            safe_alternative_ar="جهّز رسالة كمسوّدة + اطلب موافقة المؤسس.",
            safe_alternative_en="Draft the message + request founder approval.",
            required_conditions=required,
            missing_conditions=missing,
        )

    # All 4 conditions met → still approval_required (never live-send-without-human)
    return PolicyDecision(
        channel="whatsapp",
        action_kind=action_kind,
        allowed=True,
        action_mode="approved_manual",
        reason_ar="مسموح إرسال يدوي بعد الموافقة.",
        reason_en="Approved manual send permitted.",
        required_conditions=required,
        missing_conditions=[],
    )
