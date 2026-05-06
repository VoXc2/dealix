"""V14 Phase K1 — WhatsApp safe-send orchestration tests.

Closes the registry gap: `lead_intake_whatsapp` status `partial` → `live`.

Three abuse-boundary tests required by the registry's
`next_activation_step_en`:

  1. Approval-gated:    unapproved send → refused with `not_approved`
  2. Opt-out abuse:     opted-out MSISDN → refused with `opted_out`,
                        even when approval is valid (PDPL — opt-out
                        is permanent and overrides any approval)
  3. Quiet-hours:       KSA 21:00–08:00 → refused with `quiet_hours`,
                        plus `queued_until` for the next active window

Plus a happy-path test that proves a fully-approved, opt-in,
in-active-hours send actually reaches the client (mocked).

These pure-orchestration unit tests don't require Meta credentials
or the live `whatsapp_allow_live_send` flag — they exercise the
module's gate logic in isolation, with a fake client.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

import pytest

from auto_client_acquisition.whatsapp_safe_send import (
    SafeSendResult,
    check_quiet_hours,
    next_active_window,
    safe_send_text,
)


_KSA = ZoneInfo("Asia/Riyadh")


# ─────────────────────── Fake client ──────────────────────────


@dataclass
class _FakeResult:
    success: bool
    message_id: str | None = None
    error: str | None = None


class _FakeClient:
    """Records calls; returns a configurable result. Mirrors
    `integrations.whatsapp.WhatsAppClient.send_text` shape only."""

    def __init__(self, result: _FakeResult | None = None) -> None:
        self._result = result or _FakeResult(success=True, message_id="wa.fake.msg.001")
        self.calls: list[tuple[str, str]] = []

    async def send_text(self, to: str, body: str) -> _FakeResult:
        self.calls.append((to, body))
        return self._result


# ─────────────────────── Approval gate ────────────────────────


@pytest.mark.asyncio
async def test_unapproved_send_is_refused() -> None:
    """An approval that is `pending` (not yet approved) must NOT
    result in a send. Default-deny."""
    client = _FakeClient()
    out = await safe_send_text(
        msisdn="+966501234567",
        body="مرحبا — اختبار",
        approval_status="pending",
        approval_action_type="whatsapp_outbound",
        is_opted_out=False,
        now=datetime(2026, 5, 6, 12, 0, tzinfo=_KSA),  # mid-day, in active hours
        client=client,
    )
    assert out.delivered is False
    assert out.reason_code == "not_approved"
    assert client.calls == [], "Client must not be called when approval is pending"


@pytest.mark.asyncio
async def test_rejected_approval_is_refused() -> None:
    """An approval rejected by the founder MUST never lead to a send."""
    client = _FakeClient()
    out = await safe_send_text(
        msisdn="+966501234567",
        body="test",
        approval_status="rejected",
        approval_action_type="whatsapp_outbound",
        now=datetime(2026, 5, 6, 12, 0, tzinfo=_KSA),
        client=client,
    )
    assert out.delivered is False
    assert out.reason_code == "not_approved"


@pytest.mark.asyncio
async def test_wrong_action_type_is_refused() -> None:
    """An approved action_type that isn't a WhatsApp variant must
    NOT cause a WhatsApp send."""
    client = _FakeClient()
    out = await safe_send_text(
        msisdn="+966501234567",
        body="test",
        approval_status="approved",
        approval_action_type="email_outbound",  # WRONG channel
        now=datetime(2026, 5, 6, 12, 0, tzinfo=_KSA),
        client=client,
    )
    assert out.delivered is False
    assert out.reason_code == "not_approved"


# ─────────────────────── Opt-out gate ─────────────────────────


@pytest.mark.asyncio
async def test_opted_out_msisdn_is_refused_even_when_approved() -> None:
    """The crown jewel test: PDPL says opt-out overrides every
    other state. Even with a valid approval and within active hours,
    an opted-out destination MUST be refused."""
    client = _FakeClient()
    out = await safe_send_text(
        msisdn="+966501234567",
        body="مرحبا",
        approval_status="approved",
        approval_action_type="whatsapp_outbound",
        is_opted_out=True,  # ← critical
        now=datetime(2026, 5, 6, 12, 0, tzinfo=_KSA),
        client=client,
    )
    assert out.delivered is False
    assert out.reason_code == "opted_out"
    assert client.calls == [], "Client must not be invoked for opted-out MSISDN"


# ─────────────────────── Quiet-hours gate ─────────────────────


@pytest.mark.asyncio
async def test_send_during_quiet_hours_is_refused() -> None:
    """KSA 22:00 is in the default quiet window (21:00–08:00).
    Even with approval + no opt-out, send is refused and queued."""
    client = _FakeClient()
    night = datetime(2026, 5, 6, 22, 30, tzinfo=_KSA)  # 10:30pm Riyadh
    out = await safe_send_text(
        msisdn="+966501234567",
        body="late night",
        approval_status="approved",
        approval_action_type="whatsapp_outbound",
        is_opted_out=False,
        now=night,
        client=client,
    )
    assert out.delivered is False
    assert out.reason_code == "quiet_hours"
    assert out.queued_until is not None
    # next active window must be the morning (08:00)
    assert out.queued_until.hour == 8
    assert client.calls == []


@pytest.mark.asyncio
async def test_send_at_3am_is_refused() -> None:
    """3am is also inside the default quiet window."""
    client = _FakeClient()
    night = datetime(2026, 5, 6, 3, 0, tzinfo=_KSA)
    out = await safe_send_text(
        msisdn="+966501234567",
        body="3am test",
        approval_status="approved",
        approval_action_type="whatsapp_outbound",
        now=night,
        client=client,
    )
    assert out.delivered is False
    assert out.reason_code == "quiet_hours"


def test_check_quiet_hours_unit_at_midnight_is_quiet() -> None:
    """Pure unit test for the quiet-hour helper at boundary cases."""
    midnight = datetime(2026, 5, 6, 0, 0, tzinfo=_KSA)
    assert check_quiet_hours(now=midnight) is True


def test_check_quiet_hours_unit_at_noon_is_active() -> None:
    noon = datetime(2026, 5, 6, 12, 0, tzinfo=_KSA)
    assert check_quiet_hours(now=noon) is False


def test_check_quiet_hours_unit_at_8am_is_active() -> None:
    """08:00 is the END of the quiet window — `is_in_quiet_hours`
    returns True only when hour < 8 (default policy 21..8)."""
    eight_am = datetime(2026, 5, 6, 8, 0, tzinfo=_KSA)
    assert check_quiet_hours(now=eight_am) is False


def test_check_quiet_hours_unit_at_9pm_is_quiet() -> None:
    """21:00 is the start of the quiet window."""
    nine_pm = datetime(2026, 5, 6, 21, 0, tzinfo=_KSA)
    assert check_quiet_hours(now=nine_pm) is True


def test_next_active_window_after_evening_quiet() -> None:
    """At 23:00 today, next active window is 08:00 tomorrow."""
    eleven_pm = datetime(2026, 5, 6, 23, 0, tzinfo=_KSA)
    nxt = next_active_window(now=eleven_pm)
    assert nxt.date() > eleven_pm.date()
    assert nxt.hour == 8


# ─────────────────────── Missing-MSISDN gate ──────────────────


@pytest.mark.asyncio
async def test_empty_msisdn_is_refused() -> None:
    out = await safe_send_text(
        msisdn="",
        body="msg",
        approval_status="approved",
        approval_action_type="whatsapp_outbound",
        now=datetime(2026, 5, 6, 12, 0, tzinfo=_KSA),
    )
    assert out.delivered is False
    assert out.reason_code == "missing_msisdn"


# ─────────────────────── Happy path ───────────────────────────


@pytest.mark.asyncio
async def test_happy_path_send_succeeds() -> None:
    """All gates green → delegate to client → `delivered=True`."""
    client = _FakeClient(_FakeResult(success=True, message_id="wa.real.id.42"))
    out = await safe_send_text(
        msisdn="+966501234567",
        body="مرحبا، صباح الخير",
        approval_status="approved",
        approval_action_type="whatsapp_outbound",
        is_opted_out=False,
        now=datetime(2026, 5, 6, 12, 0, tzinfo=_KSA),
        client=client,
    )
    assert out.delivered is True
    assert out.reason_code == "approved_and_sent"
    assert out.message_id == "wa.real.id.42"
    assert len(client.calls) == 1
    assert client.calls[0][0] == "+966501234567"


@pytest.mark.asyncio
async def test_live_send_disabled_returns_specific_reason() -> None:
    """If the underlying client refuses with `whatsapp_allow_live_send_false`,
    we surface a distinct `live_send_disabled` reason code so the
    founder knows to flip the env var (vs. e.g. a network error)."""
    client = _FakeClient(_FakeResult(success=False, error="whatsapp_allow_live_send_false"))
    out = await safe_send_text(
        msisdn="+966501234567",
        body="test",
        approval_status="approved",
        approval_action_type="whatsapp_outbound",
        now=datetime(2026, 5, 6, 12, 0, tzinfo=_KSA),
        client=client,
    )
    assert out.delivered is False
    assert out.reason_code == "live_send_disabled"


@pytest.mark.asyncio
async def test_client_exception_is_caught_and_surfaced() -> None:
    """An unexpected client exception MUST NOT propagate — caller
    sees a structured `client_error` response instead."""

    class _ExplodingClient:
        async def send_text(self, to: str, body: str) -> Any:
            raise RuntimeError("network down")

    out = await safe_send_text(
        msisdn="+966501234567",
        body="test",
        approval_status="approved",
        approval_action_type="whatsapp_outbound",
        now=datetime(2026, 5, 6, 12, 0, tzinfo=_KSA),
        client=_ExplodingClient(),
    )
    assert out.delivered is False
    assert out.reason_code == "client_error"


# ─────────────────────── SafeSendResult shape ─────────────────


def test_safe_send_result_is_immutable() -> None:
    """SafeSendResult must be frozen so callers can't mutate it
    after the gate decision is made."""
    r = SafeSendResult(
        delivered=False,
        reason_code="not_approved",
        reason_ar="...",
        reason_en="...",
    )
    with pytest.raises((AttributeError, Exception)):
        r.delivered = True  # type: ignore[misc]
