"""Wave 7.5 §24.2 Fix 4 — safe_send_gateway middleware.

Single canonical guard for any external send path. Raises
`SendBlocked` exception when consent / opt-out / channel rules
fail. Wraps existing blocking logic from whatsapp_safe_send +
email_send compliance check; does NOT replace them.

Usage:

    from auto_client_acquisition.safe_send_gateway import (
        enforce_consent_or_block, SendBlocked
    )

    try:
        enforce_consent_or_block(
            channel="whatsapp",
            destination="+966512345678",
            approval_status="approved",
            is_opted_out=False,
            consent_record_id="con_123",
        )
        # Safe to call provider.send_text(...)
    except SendBlocked as exc:
        # Audit + return uniform error
        ...

Design intent: keep the gate logic discoverable in one place so
new send paths (e.g. SMS, Telegram if ever added) inherit the
same blocking pattern automatically.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

_VALID_CHANNELS = {"whatsapp", "email", "sms"}
_VALID_APPROVAL_STATUSES = {"draft", "pending", "approved", "rejected", "expired"}


class SendBlocked(Exception):  # noqa: N818 - public API name
    """Raised when any send-gate refuses an external send.

    Carries structured `reasons` so audit logs + customer-portal
    can render the block reason without parsing exception text.
    """

    def __init__(
        self,
        *,
        reason_code: str,
        reasons_ar: str,
        reasons_en: str,
        channel: str,
        destination: str = "",
        gate: str = "",
    ) -> None:
        self.reason_code = reason_code
        self.reasons_ar = reasons_ar
        self.reasons_en = reasons_en
        self.channel = channel
        self.destination = destination
        self.gate = gate
        super().__init__(f"SendBlocked[{gate}|{reason_code}]: {reasons_en}")


@dataclass(frozen=True)
class SendDecision:
    """Outcome of `enforce_consent_or_block` when it does NOT raise.

    Always `is_safe_to_send=True` here; if anything refused, the
    function raises `SendBlocked` instead of returning this dataclass.
    """

    is_safe_to_send: bool = True
    channel: str = ""
    destination: str = ""
    consent_record_id: str = ""
    approval_action_id: str = ""
    audit_breadcrumb: dict[str, Any] = field(default_factory=dict)


def enforce_consent_or_block(
    *,
    channel: str,
    destination: str,
    approval_status: str,
    is_opted_out: bool = False,
    consent_record_id: str = "",
    approval_action_id: str = "",
    quiet_hours_active: bool = False,
) -> SendDecision:
    """Single canonical guard. Raises SendBlocked or returns SendDecision.

    Caller MUST resolve all inputs (consent record, opt-out state,
    quiet-hours window) before calling. This function does not
    fetch state — it just enforces the decision boundary.
    """
    # 1. Channel validation
    if channel not in _VALID_CHANNELS:
        raise SendBlocked(
            reason_code="invalid_channel",
            reasons_ar=f"القناة '{channel}' غير مدعومة.",
            reasons_en=f"Channel '{channel}' not supported.",
            channel=channel,
            destination=destination,
            gate="channel_validation",
        )

    # 2. Approval gate
    if approval_status not in _VALID_APPROVAL_STATUSES:
        raise SendBlocked(
            reason_code="invalid_approval_status",
            reasons_ar=f"حالة الموافقة '{approval_status}' غير معروفة.",
            reasons_en=f"Approval status '{approval_status}' not recognized.",
            channel=channel,
            destination=destination,
            gate="approval_status_validation",
        )
    if approval_status != "approved":
        raise SendBlocked(
            reason_code="not_approved",
            reasons_ar="الإجراء غير مُعتمد — لازم موافقة المؤسس قبل الإرسال.",
            reasons_en="Action not approved — founder approval required before send.",
            channel=channel,
            destination=destination,
            gate="approval_gate",
        )

    # 3. Destination present
    if not destination or not destination.strip():
        raise SendBlocked(
            reason_code="missing_destination",
            reasons_ar="وجهة الإرسال غير موجودة.",
            reasons_en="Destination missing — cannot send.",
            channel=channel,
            destination="",
            gate="destination_present",
        )

    # 4. Opt-out gate (PDPL — permanent)
    if is_opted_out:
        raise SendBlocked(
            reason_code="opted_out",
            reasons_ar="المستلم سجّل opt-out — الإرسال محظور دائماً (PDPL).",
            reasons_en="Recipient opted out — send permanently blocked (PDPL).",
            channel=channel,
            destination=destination,
            gate="opt_out_gate",
        )

    # 5. Consent record gate (PDPL — must exist for marketing/non-transactional channels)
    if channel == "whatsapp" and not consent_record_id:
        raise SendBlocked(
            reason_code="no_consent_record",
            reasons_ar="لا يوجد سجلّ موافقة (consent record) للمستلم — الإرسال على واتساب يحتاج موافقة موثّقة.",
            reasons_en="No consent record on file — WhatsApp send requires documented consent.",
            channel=channel,
            destination=destination,
            gate="consent_record_gate",
        )

    # 6. Quiet-hours gate (KSA Asia/Riyadh)
    if quiet_hours_active:
        raise SendBlocked(
            reason_code="quiet_hours",
            reasons_ar="خارج ساعات النشاط السعوديّة (21:00-08:00) — الإرسال مؤجّل.",
            reasons_en="Outside KSA active hours (21:00-08:00) — send queued.",
            channel=channel,
            destination=destination,
            gate="quiet_hours_gate",
        )

    return SendDecision(
        is_safe_to_send=True,
        channel=channel,
        destination=destination,
        consent_record_id=consent_record_id,
        approval_action_id=approval_action_id,
        audit_breadcrumb={
            "all_gates_passed": True,
            "gates_checked": [
                "channel_validation",
                "approval_status_validation",
                "approval_gate",
                "destination_present",
                "opt_out_gate",
                "consent_record_gate" if channel == "whatsapp" else "consent_record_gate_skipped",
                "quiet_hours_gate",
            ],
        },
    )


def summarize_gates() -> dict[str, str]:
    """Documentation helper — describes every gate enforced by this module.

    Used by `landing/customer-portal.html` Trust panel + `docs/SERVICE_TRUTH_REPORT.md`.
    """
    return {
        "channel_validation": "Only whatsapp / email / sms accepted",
        "approval_status_validation": "Status must be a known enum value",
        "approval_gate": "Send refused if approval_status != 'approved'",
        "destination_present": "Send refused if destination empty",
        "opt_out_gate": "Send permanently blocked if recipient opted out (PDPL)",
        "consent_record_gate": "WhatsApp requires documented consent_record_id (PDPL)",
        "quiet_hours_gate": "Send queued if KSA quiet hours (21:00-08:00) active",
    }
