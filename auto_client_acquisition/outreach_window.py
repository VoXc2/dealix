"""V14 Phase K5 — outreach active-conversation-window enforcement.

Closes the registry's `next_activation_step_en` for `outreach_drafts`:
"Add quiet-hours enforcement and a test that rejects sends outside
the active conversation window."

Two gates:
  1. KSA quiet-hours (Asia/Riyadh 21:00–08:00 by default) — reuses
     existing `auto_client_acquisition.orchestrator.policies.is_in_quiet_hours`
  2. 72-hour active conversation window — a draft outreach is only
     valid for follow-up within 72h of the last inbound from the
     customer. Drafts older than 72h flag as
     `requires_re_engagement_consent`.

Hard rules:
  - Default-deny on missing/malformed timestamps
  - 72h window is in WALL-clock seconds (no business-day adjustments)
  - Re-engagement after 72h requires explicit re-consent
  - Returned reasons are stable strings so the API can render them
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta, timezone
from typing import Literal
from zoneinfo import ZoneInfo

from auto_client_acquisition.orchestrator.policies import (
    Policy,
    default_policy,
    is_in_quiet_hours,
)

_KSA_TZ = ZoneInfo("Asia/Riyadh")
ACTIVE_WINDOW_HOURS = 72


@dataclass(frozen=True)
class WindowVerdict:
    """Outcome of the active-window + quiet-hours check."""

    allowed: bool
    reason_code: str  # in_active_window | quiet_hours |
                      # requires_re_engagement_consent | missing_inbound
    reason_ar: str
    reason_en: str


def _ensure_aware_utc(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def check_outreach_window(
    *,
    last_inbound_at: datetime | None,
    now: datetime | None = None,
    policy: Policy | None = None,
) -> WindowVerdict:
    """Validate a draft outreach against the 72h conversation window
    AND KSA quiet-hours. Returns `allowed=True` only when both gates
    pass.
    """
    now_utc = _ensure_aware_utc(now) or datetime.now(UTC)

    # 1. Active-window gate
    last_utc = _ensure_aware_utc(last_inbound_at)
    if last_utc is None:
        return WindowVerdict(
            allowed=False,
            reason_code="missing_inbound",
            reason_ar="لا توجد رسالة واردة سابقة — مطلوب موافقة جديدة قبل الإرسال.",
            reason_en="No prior inbound — re-consent required before sending.",
        )

    elapsed = now_utc - last_utc
    if elapsed > timedelta(hours=ACTIVE_WINDOW_HOURS):
        return WindowVerdict(
            allowed=False,
            reason_code="requires_re_engagement_consent",
            reason_ar=(
                f"انقضت نافذة المحادثة الفعّالة ({ACTIVE_WINDOW_HOURS}ساعة) — "
                f"يلزم تجديد الموافقة قبل أي إرسال."
            ),
            reason_en=(
                f"Active conversation window ({ACTIVE_WINDOW_HOURS}h) expired "
                f"— re-engagement consent required before send."
            ),
        )

    # 2. Quiet-hours gate (KSA Asia/Riyadh)
    now_ksa = now_utc.astimezone(_KSA_TZ)
    p = policy if policy is not None else default_policy("default")
    if is_in_quiet_hours(hour_riyadh=now_ksa.hour, policy=p):
        return WindowVerdict(
            allowed=False,
            reason_code="quiet_hours",
            reason_ar=(
                f"خارج ساعات النشاط (KSA): الساعة {now_ksa.hour:02d}:00 — "
                f"الإرسال يستأنف بعد الساعة {p.quiet_hours_riyadh[1]:02d}:00."
            ),
            reason_en=(
                f"KSA quiet hours: hour={now_ksa.hour:02d}:00 — "
                f"resume after {p.quiet_hours_riyadh[1]:02d}:00."
            ),
        )

    # Both gates green
    return WindowVerdict(
        allowed=True,
        reason_code="in_active_window",
        reason_ar="ضمن النافذة الفعّالة وخارج ساعات الهدوء.",
        reason_en="Inside active window and outside quiet hours.",
    )
