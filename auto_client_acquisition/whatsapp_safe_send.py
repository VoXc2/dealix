"""V14 Phase K1 — safe WhatsApp send orchestration.

Wraps `integrations.whatsapp.WhatsAppClient` with the safety checks
required to flip `lead_intake_whatsapp` from `partial` to `live` in
the registry.

Stack of gates (in order — first refusal wins):

  1. Approval gate:   the supplied approval status must be `approved`
                      and action_type must be a WhatsApp variant
  2. Destination:     MSISDN must be present
  3. Opt-out gate:    caller-supplied `is_opted_out` flag — if True,
                      send is permanently refused (PDPL — opt-out
                      always overrides any other state)
  4. Quiet-hours gate: KSA Asia/Riyadh local hour must NOT be in
                      the configured quiet window (default 21:00–08:00).
                      Returns `queued_until` for the next active window.
  5. Live-send flag:  WhatsAppClient itself enforces
                      `whatsapp_allow_live_send` (in settings)
  6. Then:            delegate to WhatsAppClient.send_text

Every refusal returns a structured `SafeSendResult` so callers can
log/audit the exact reason without exposing internals to the user.

Hard rules (non-negotiable):
- Default-deny: any unknown failure path returns blocked, not allowed.
- Opt-out is permanent and overrides any approval (PDPL Article 5).
- Quiet hours apply EVEN if approved — manager approves a SCHEDULE,
  not "send right now bypassing PDPL". The send is queued for the
  next active window.
- This module never persists outbound messages on its own — that's
  the audit_trail's job.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from auto_client_acquisition.orchestrator.policies import (
    Policy,
    default_policy,
    is_in_quiet_hours,
)

_KSA_TZ = ZoneInfo("Asia/Riyadh")

_VALID_WHATSAPP_ACTIONS = frozenset({
    "whatsapp_outbound",
    "whatsapp_template",
    "whatsapp_text",
})


@dataclass(frozen=True)
class SafeSendResult:
    """Outcome of a safe-send orchestration call. `delivered=True` ONLY
    when the message was actually accepted by Meta. Any earlier
    refusal returns `delivered=False` with a `reason_code`."""

    delivered: bool
    reason_code: str  # approved_and_sent | live_send_disabled |
                      # not_approved | opted_out | quiet_hours |
                      # missing_msisdn | client_error
    reason_ar: str
    reason_en: str
    message_id: str | None = None
    queued_until: datetime | None = None  # set when reason_code=quiet_hours


def _refuse(code: str, ar: str, en: str, **extra: Any) -> SafeSendResult:
    return SafeSendResult(
        delivered=False,
        reason_code=code,
        reason_ar=ar,
        reason_en=en,
        **extra,
    )


def check_quiet_hours(
    *,
    now: datetime | None = None,
    policy: Policy | None = None,
) -> bool:
    """Returns True if `now` is in KSA quiet hours (21:00–08:00
    Asia/Riyadh by default — the policy.quiet_hours_riyadh tuple)."""
    if now is None:
        now = datetime.now(_KSA_TZ)
    if now.tzinfo is None:
        now = now.replace(tzinfo=ZoneInfo("UTC")).astimezone(_KSA_TZ)
    else:
        now = now.astimezone(_KSA_TZ)
    p = policy if policy is not None else default_policy("default")
    return is_in_quiet_hours(hour_riyadh=now.hour, policy=p)


def next_active_window(
    *,
    now: datetime | None = None,
    policy: Policy | None = None,
) -> datetime:
    """Compute the next moment that is OUTSIDE quiet hours."""
    cur = (now or datetime.now(_KSA_TZ)).astimezone(_KSA_TZ)
    p = policy if policy is not None else default_policy("default")
    end_hour = p.quiet_hours_riyadh[1]
    candidate = cur.replace(hour=end_hour, minute=0, second=0, microsecond=0)
    if candidate <= cur:
        candidate = candidate + timedelta(days=1)
    return candidate


async def safe_send_text(
    *,
    msisdn: str,
    body: str,
    approval_status: str,
    approval_action_type: str,
    is_opted_out: bool = False,
    policy: Policy | None = None,
    now: datetime | None = None,
    client: Any = None,
) -> SafeSendResult:
    """Run all 4 gates then send a free-form text via WhatsApp Cloud API.

    Caller MUST have already created+approved the approval via
    /api/v1/approvals/* and queried any opt-out store before calling.
    This module is the gate orchestrator; persistence is elsewhere.
    """
    # 1. Approval gate
    if approval_status != "approved":
        return _refuse(
            "not_approved",
            ar="الإجراء غير مُعتمد — يجب موافقة المؤسس قبل الإرسال.",
            en="Action is not approved — founder approval required before send.",
        )
    if approval_action_type not in _VALID_WHATSAPP_ACTIONS:
        return _refuse(
            "not_approved",
            ar="نوع الإجراء لا يطابق قناة WhatsApp.",
            en="Approval action_type does not match WhatsApp channel.",
        )

    # 2. Destination present
    if not msisdn or not msisdn.strip():
        return _refuse(
            "missing_msisdn",
            ar="رقم الجوّال غير موجود — لا يمكن الإرسال.",
            en="Missing destination MSISDN — cannot send.",
        )

    # 3. Opt-out gate (PDPL — permanent override)
    if is_opted_out:
        return _refuse(
            "opted_out",
            ar="الرقم سجّل opt-out — الإرسال محظور دائماً (PDPL).",
            en="MSISDN has opted out — send permanently blocked (PDPL).",
        )

    # 4. Quiet-hours gate (KSA Asia/Riyadh)
    if check_quiet_hours(now=now, policy=policy):
        next_active = next_active_window(now=now, policy=policy)
        return _refuse(
            "quiet_hours",
            ar=f"خارج ساعات النشاط — الإرسال مؤجَّل حتى {next_active.strftime('%Y-%m-%d %H:%M')} KSA.",
            en=f"Outside KSA active hours — send queued until {next_active.isoformat()}.",
            queued_until=next_active,
        )

    # 5. Delegate to client. Client itself enforces whatsapp_allow_live_send.
    if client is None:
        from integrations.whatsapp import WhatsAppClient
        client = WhatsAppClient()
    try:
        result = await client.send_text(msisdn, body)
    except Exception as exc:
        return _refuse(
            "client_error",
            ar=f"خطأ في عميل WhatsApp: {type(exc).__name__}",
            en=f"WhatsApp client error: {type(exc).__name__}",
        )

    if getattr(result, "success", False):
        return SafeSendResult(
            delivered=True,
            reason_code="approved_and_sent",
            reason_ar="تمّ الإرسال بنجاح بعد كلّ البوّابات.",
            reason_en="Sent successfully after all gates.",
            message_id=getattr(result, "message_id", None),
        )

    err = getattr(result, "error", "unknown") or "unknown"
    if err == "whatsapp_allow_live_send_false":
        return _refuse(
            "live_send_disabled",
            ar="الإرسال الحيّ غير مفعَّل — اضبط whatsapp_allow_live_send=true بعد موافقة Meta.",
            en="Live send disabled — set whatsapp_allow_live_send=true after Meta approval.",
        )
    return _refuse(
        "client_error",
        ar=f"رفضت Meta الإرسال: {err}",
        en=f"Meta refused the send: {err}",
    )
