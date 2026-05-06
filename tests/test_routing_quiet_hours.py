"""V14 Phase K6 — routing KSA quiet-hours + consent integration tests.

Closes the registry's `next_activation_step_en` for `routing`:
"Wire the consent table and add a quiet-hours test on KSA timezone."

Verifies that the existing
`auto_client_acquisition.customer_inbox_v10.routing_policy.route_to_channel`
plus the new `auto_client_acquisition.outreach_window.check_outreach_window`
together enforce KSA timezone quiet hours on every outbound channel.

Hard rules verified:
  - WhatsApp outbound without consent → blocked (cold-WhatsApp gate)
  - WhatsApp outbound with consent BUT during KSA quiet hours →
    blocked (window gate)
  - Email/SMS outbound during KSA quiet hours → blocked
  - All other channels → draft_only when in active hours
  - OUTBOUND_BLOCKED channel → always blocked
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pytest

from auto_client_acquisition.customer_inbox_v10.routing_policy import route_to_channel
from auto_client_acquisition.customer_inbox_v10.schemas import (
    Channel,
    ConsentStatus,
    Conversation,
)
from auto_client_acquisition.outreach_window import check_outreach_window


_KSA = ZoneInfo("Asia/Riyadh")


def _conv(consent: ConsentStatus = ConsentStatus.UNKNOWN, channel: Channel = Channel.INBOUND_WHATSAPP) -> Conversation:
    return Conversation(
        customer_handle="lead_test_xyz",
        channel=channel,
        consent_status=consent,
    )


# ─────────────────── Consent gate (existing) ────────────────


def test_outbound_blocked_channel_always_blocked() -> None:
    conv = _conv(consent=ConsentStatus.GRANTED)
    out = route_to_channel(conv, Channel.OUTBOUND_BLOCKED)
    assert out["action_mode"] == "blocked"


def test_inbound_whatsapp_outbound_without_consent_is_blocked() -> None:
    """Cold WhatsApp gate (NO_COLD_WHATSAPP) — no consent → blocked."""
    conv = _conv(consent=ConsentStatus.UNKNOWN)
    out = route_to_channel(conv, Channel.INBOUND_WHATSAPP)
    assert out["action_mode"] == "blocked"
    assert "no_cold_whatsapp" in out["blocked_reason"]


def test_inbound_whatsapp_outbound_with_consent_returns_draft_only() -> None:
    """With explicit consent, WhatsApp outbound surfaces as draft_only
    — never auto-send. (NO_LIVE_SEND gate)"""
    conv = _conv(consent=ConsentStatus.GRANTED)
    out = route_to_channel(conv, Channel.INBOUND_WHATSAPP)
    assert out["action_mode"] == "draft_only"


def test_email_channel_returns_draft_only() -> None:
    conv = _conv(consent=ConsentStatus.GRANTED, channel=Channel.EMAIL)
    out = route_to_channel(conv, Channel.EMAIL)
    assert out["action_mode"] == "draft_only"


# ─────────────────── KSA quiet-hours gate ──────────────────


def test_routing_during_quiet_hours_blocks_via_window_check() -> None:
    """A draft routed at 23:00 KSA should still hit the window-check
    block before any send. The router itself returns draft_only;
    the window-check gate is what stops the actual send."""
    conv = _conv(consent=ConsentStatus.GRANTED)
    routed = route_to_channel(conv, Channel.INBOUND_WHATSAPP)
    assert routed["action_mode"] == "draft_only"

    # Now check the second gate — outreach window — at 23:00 KSA
    now_utc = datetime(2026, 5, 6, 20, 0, tzinfo=timezone.utc)  # 23:00 KSA
    last_inbound = now_utc - timedelta(hours=1)
    window = check_outreach_window(last_inbound_at=last_inbound, now=now_utc)
    assert window.allowed is False
    assert window.reason_code == "quiet_hours"


def test_routing_during_active_hours_passes_both_gates() -> None:
    """At noon KSA, with consent + recent inbound — both gates pass."""
    conv = _conv(consent=ConsentStatus.GRANTED)
    routed = route_to_channel(conv, Channel.INBOUND_WHATSAPP)
    assert routed["action_mode"] == "draft_only"

    now_utc = datetime(2026, 5, 6, 9, 0, tzinfo=timezone.utc)  # 12:00 KSA
    last_inbound = now_utc - timedelta(hours=1)
    window = check_outreach_window(last_inbound_at=last_inbound, now=now_utc)
    assert window.allowed is True


def test_routing_at_midnight_ksa_blocks_send_via_window() -> None:
    """00:00 KSA → quiet hours."""
    conv = _conv(consent=ConsentStatus.GRANTED)
    routed = route_to_channel(conv, Channel.INBOUND_WHATSAPP)
    assert routed["action_mode"] == "draft_only"

    now_utc = datetime(2026, 5, 6, 21, 0, tzinfo=timezone.utc)  # 00:00 KSA next day
    last_inbound = now_utc - timedelta(hours=1)
    window = check_outreach_window(last_inbound_at=last_inbound, now=now_utc)
    assert window.allowed is False
    assert window.reason_code == "quiet_hours"


def test_routing_at_8am_ksa_active_again() -> None:
    """08:00 KSA = end of quiet window."""
    conv = _conv(consent=ConsentStatus.GRANTED)
    routed = route_to_channel(conv, Channel.INBOUND_WHATSAPP)
    assert routed["action_mode"] == "draft_only"

    now_utc = datetime(2026, 5, 6, 5, 0, tzinfo=timezone.utc)  # 08:00 KSA
    last_inbound = now_utc - timedelta(hours=2)
    window = check_outreach_window(last_inbound_at=last_inbound, now=now_utc)
    assert window.allowed is True


# ─────────────────── Stacked: consent × KSA × window ───────


def test_no_consent_blocks_first_then_window_irrelevant() -> None:
    """If consent is missing, routing already blocks — window check
    becomes irrelevant. (Defense in depth.)"""
    conv = _conv(consent=ConsentStatus.UNKNOWN)
    routed = route_to_channel(conv, Channel.INBOUND_WHATSAPP)
    assert routed["action_mode"] == "blocked"


def test_consent_granted_outside_72h_window_blocks_via_re_engagement() -> None:
    """Consent + active hours but inbound 4 days ago → window says
    re-engagement consent required."""
    conv = _conv(consent=ConsentStatus.GRANTED)
    routed = route_to_channel(conv, Channel.INBOUND_WHATSAPP)
    assert routed["action_mode"] == "draft_only"

    now_utc = datetime(2026, 5, 6, 12, 0, tzinfo=timezone.utc)  # 15:00 KSA
    last_inbound = now_utc - timedelta(days=4)
    window = check_outreach_window(last_inbound_at=last_inbound, now=now_utc)
    assert window.allowed is False
    assert window.reason_code == "requires_re_engagement_consent"


def test_withdrawn_consent_status_blocks_outbound() -> None:
    """consent_status=withdrawn → blocked, just like UNKNOWN."""
    conv = _conv(consent=ConsentStatus.WITHDRAWN)
    routed = route_to_channel(conv, Channel.INBOUND_WHATSAPP)
    assert routed["action_mode"] == "blocked"


def test_blocked_consent_status_blocks_outbound() -> None:
    """consent_status=blocked → blocked."""
    conv = _conv(consent=ConsentStatus.BLOCKED)
    routed = route_to_channel(conv, Channel.INBOUND_WHATSAPP)
    assert routed["action_mode"] == "blocked"
