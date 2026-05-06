"""V14 Phase K5 — outreach_drafts active-window + KSA quiet-hours tests.

Closes the registry's `next_activation_step_en` for `outreach_drafts`:
"Add quiet-hours enforcement and a test that rejects sends outside
the active conversation window."

Two stacked gates:
  1. 72h active conversation window
  2. KSA Asia/Riyadh quiet-hours (21:00–08:00 default)

Both must pass for a draft to be sent. Default-deny on either failure.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pytest

from auto_client_acquisition.outreach_window import (
    ACTIVE_WINDOW_HOURS,
    WindowVerdict,
    check_outreach_window,
)


_KSA = ZoneInfo("Asia/Riyadh")


# ─────────────────── Active-window gate ────────────────────


def test_no_prior_inbound_blocks_send() -> None:
    """Default-deny: with no inbound message ever, the draft cannot
    be sent. Re-engagement consent required."""
    v = check_outreach_window(
        last_inbound_at=None,
        now=datetime(2026, 5, 6, 12, 0, tzinfo=timezone.utc),
    )
    assert v.allowed is False
    assert v.reason_code == "missing_inbound"


def test_recent_inbound_within_window_is_allowed() -> None:
    """Inbound 1h ago, mid-day KSA → both gates green."""
    now_utc = datetime(2026, 5, 6, 9, 0, tzinfo=timezone.utc)  # 12:00 KSA (UTC+3)
    last = now_utc - timedelta(hours=1)
    v = check_outreach_window(last_inbound_at=last, now=now_utc)
    assert v.allowed is True
    assert v.reason_code == "in_active_window"


def test_inbound_at_window_boundary_72h_minus_1m_is_allowed() -> None:
    """71h59m ago is still inside the 72h window."""
    now_utc = datetime(2026, 5, 6, 9, 0, tzinfo=timezone.utc)
    last = now_utc - timedelta(hours=ACTIVE_WINDOW_HOURS, minutes=-1)
    v = check_outreach_window(last_inbound_at=last, now=now_utc)
    assert v.allowed is True


def test_inbound_just_past_72h_blocks_send() -> None:
    """72h+1min ago → window expired → re-engagement consent needed."""
    now_utc = datetime(2026, 5, 6, 9, 0, tzinfo=timezone.utc)
    last = now_utc - timedelta(hours=ACTIVE_WINDOW_HOURS, minutes=1)
    v = check_outreach_window(last_inbound_at=last, now=now_utc)
    assert v.allowed is False
    assert v.reason_code == "requires_re_engagement_consent"


def test_inbound_5_days_ago_blocks_send() -> None:
    """Way past 72h — definitely needs re-consent."""
    now_utc = datetime(2026, 5, 6, 9, 0, tzinfo=timezone.utc)
    last = now_utc - timedelta(days=5)
    v = check_outreach_window(last_inbound_at=last, now=now_utc)
    assert v.allowed is False
    assert v.reason_code == "requires_re_engagement_consent"


# ─────────────────── Quiet-hours gate ──────────────────────


def test_during_ksa_quiet_hours_blocks_even_with_recent_inbound() -> None:
    """Inbound 1h ago BUT it's 23:00 KSA → quiet-hours wins."""
    # 23:00 KSA = 20:00 UTC
    now_utc = datetime(2026, 5, 6, 20, 0, tzinfo=timezone.utc)
    last = now_utc - timedelta(hours=1)
    v = check_outreach_window(last_inbound_at=last, now=now_utc)
    assert v.allowed is False
    assert v.reason_code == "quiet_hours"


def test_at_3am_ksa_blocks_send() -> None:
    """03:00 KSA = 00:00 UTC → quiet hours."""
    now_utc = datetime(2026, 5, 6, 0, 0, tzinfo=timezone.utc)
    last = now_utc - timedelta(hours=2)
    v = check_outreach_window(last_inbound_at=last, now=now_utc)
    assert v.allowed is False
    assert v.reason_code == "quiet_hours"


def test_at_8am_ksa_is_active_again() -> None:
    """08:00 KSA = 05:00 UTC → first hour of active window. Inbound recent."""
    now_utc = datetime(2026, 5, 6, 5, 0, tzinfo=timezone.utc)
    last = now_utc - timedelta(hours=1)
    v = check_outreach_window(last_inbound_at=last, now=now_utc)
    assert v.allowed is True


def test_at_9pm_ksa_blocks_send() -> None:
    """21:00 KSA = 18:00 UTC → start of quiet hours."""
    now_utc = datetime(2026, 5, 6, 18, 0, tzinfo=timezone.utc)
    last = now_utc - timedelta(minutes=30)
    v = check_outreach_window(last_inbound_at=last, now=now_utc)
    assert v.allowed is False
    assert v.reason_code == "quiet_hours"


# ─────────────────── Stacked gates ────────────────────────


def test_outside_window_AND_quiet_hours_returns_window_failure_first() -> None:
    """When BOTH gates fail, the active-window check fires first
    (since re-engagement consent is the deeper PDPL issue)."""
    # 4 days ago AND it's 23:00 KSA → both fail
    now_utc = datetime(2026, 5, 6, 20, 0, tzinfo=timezone.utc)  # 23:00 KSA
    last = now_utc - timedelta(days=4)
    v = check_outreach_window(last_inbound_at=last, now=now_utc)
    assert v.allowed is False
    assert v.reason_code == "requires_re_engagement_consent"


# ─────────────────── Naive datetime handling ───────────────


def test_naive_inbound_datetime_treated_as_utc() -> None:
    """A naive datetime (no tzinfo) is assumed UTC and processed
    correctly — no crash."""
    now_utc = datetime(2026, 5, 6, 9, 0, tzinfo=timezone.utc)
    naive_last = (now_utc - timedelta(hours=1)).replace(tzinfo=None)
    v = check_outreach_window(last_inbound_at=naive_last, now=now_utc)
    assert v.allowed is True


# ─────────────────── Verdict shape ────────────────────────


def test_verdict_is_immutable() -> None:
    """WindowVerdict is frozen — caller can't tamper with the gate decision."""
    v = WindowVerdict(
        allowed=False,
        reason_code="quiet_hours",
        reason_ar="...",
        reason_en="...",
    )
    with pytest.raises((AttributeError, Exception)):
        v.allowed = True  # type: ignore[misc]


def test_verdict_carries_bilingual_reasons() -> None:
    """Both Arabic + English reason strings are present on every refusal."""
    now_utc = datetime(2026, 5, 6, 20, 0, tzinfo=timezone.utc)
    last = now_utc - timedelta(minutes=30)
    v = check_outreach_window(last_inbound_at=last, now=now_utc)
    assert v.reason_ar
    assert v.reason_en
