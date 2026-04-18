"""
Tests for BaseEngagementAgent — rate limiting, retry, compliance checks.
"""
from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.engagement.base import (
    AgentContext,
    ChannelType,
    DeliveryReceipt,
    DeliveryStatus,
    EngagementSettings,
    IncomingMessage,
    LeadStage,
    check_compliance,
    ComplianceResult,
)


# ─────────────────────────────────────────────────────────────
# Compliance checks
# ─────────────────────────────────────────────────────────────

def test_compliance_allows_opted_in():
    """Opt-in context outside quiet hours should be allowed."""
    settings = EngagementSettings(
        quiet_hours_start=22,
        quiet_hours_end=8,
    )
    # Force current time to be 14:00 UTC → 17:00 KSA (within business hours)
    with patch("app.engagement.base.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2025, 1, 1, 11, 0, tzinfo=timezone.utc)
        context = AgentContext(opt_in=True, timezone_offset=3)
        result = check_compliance(context, settings)

    assert result.allowed is True


def test_compliance_blocks_opted_out():
    """Opt-out context must be blocked regardless of time."""
    settings = EngagementSettings()
    context = AgentContext(opt_in=False)
    result = check_compliance(context, settings)
    assert result.allowed is False
    assert "opted in" in result.reason.lower()


def test_compliance_blocks_unsubscribed():
    """Unsubscribed lead must be blocked."""
    settings = EngagementSettings(quiet_hours_start=23, quiet_hours_end=0)
    with patch("app.engagement.base.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2025, 1, 1, 11, 0, tzinfo=timezone.utc)
        context = AgentContext(opt_in=True, stage=LeadStage.UNSUBSCRIBED)
        result = check_compliance(context, settings)

    assert result.allowed is False
    assert "unsubscribed" in result.reason.lower()


def test_compliance_blocks_quiet_hours():
    """Messages during quiet hours must be blocked."""
    settings = EngagementSettings(quiet_hours_start=22, quiet_hours_end=8)
    # 22:00 UTC → 01:00 KSA (past midnight — quiet hours)
    with patch("app.engagement.base.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2025, 1, 1, 22, 30, tzinfo=timezone.utc)
        context = AgentContext(opt_in=True, timezone_offset=3)
        result = check_compliance(context, settings)

    assert result.allowed is False
    assert "quiet" in result.reason.lower()


# ─────────────────────────────────────────────────────────────
# Rate limiter
# ─────────────────────────────────────────────────────────────

def test_rate_limiter_allows_within_limit():
    """Rate limiter allows tokens within the per-minute budget."""
    from app.engagement.base import _RateLimiter

    rl = _RateLimiter(max_per_minute=5, max_per_hour=100)
    for _ in range(5):
        assert rl.consume() is True


def test_rate_limiter_blocks_over_limit():
    """Rate limiter blocks when per-minute bucket is exhausted."""
    from app.engagement.base import _RateLimiter

    rl = _RateLimiter(max_per_minute=3, max_per_hour=100)
    for _ in range(3):
        rl.consume()
    # 4th consume should fail (no refill time has passed)
    assert rl.consume() is False


# ─────────────────────────────────────────────────────────────
# send_with_guards — retry + rate limit + compliance
# ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_send_with_guards_success(wa_agent):
    """send_with_guards calls send() and persists the message."""
    receipt_mock = DeliveryReceipt(
        channel=ChannelType.WHATSAPP,
        to="+966512345678",
        status=DeliveryStatus.SENT,
        provider_message_id="SM123",
    )
    wa_agent.send = AsyncMock(return_value=receipt_mock)

    context = AgentContext(opt_in=True)
    with patch("app.engagement.base.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2025, 1, 1, 11, 0, tzinfo=timezone.utc)
        receipt = await wa_agent.send_with_guards("+966512345678", "مرحبا", context)

    assert receipt.status == DeliveryStatus.SENT
    wa_agent.send.assert_called_once()


@pytest.mark.asyncio
async def test_send_with_guards_compliance_block(wa_agent):
    """send_with_guards returns COMPLIANCE_BLOCKED for opted-out lead."""
    context = AgentContext(opt_in=False)
    receipt = await wa_agent.send_with_guards("+966512345678", "test", context)
    assert receipt.status == DeliveryStatus.COMPLIANCE_BLOCKED


@pytest.mark.asyncio
async def test_send_with_guards_retry(wa_agent, settings):
    """send_with_guards retries on transient failures."""
    call_count = 0

    async def flaky_send(to, message, context):
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise RuntimeError("Transient network error")
        return DeliveryReceipt(
            channel=ChannelType.WHATSAPP,
            to=to,
            status=DeliveryStatus.SENT,
        )

    wa_agent.send = flaky_send
    context = AgentContext(opt_in=True)

    with patch("app.engagement.base.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2025, 1, 1, 11, 0, tzinfo=timezone.utc)
        receipt = await wa_agent.send_with_guards("+966512345678", "test", context)

    assert receipt.status == DeliveryStatus.SENT
    assert call_count == 2  # failed once, succeeded on retry


@pytest.mark.asyncio
async def test_send_with_guards_all_retries_fail(wa_agent):
    """When all retries are exhausted, returns FAILED status."""
    wa_agent.send = AsyncMock(side_effect=RuntimeError("Persistent error"))
    context = AgentContext(opt_in=True)

    with patch("app.engagement.base.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2025, 1, 1, 11, 0, tzinfo=timezone.utc)
        receipt = await wa_agent.send_with_guards("+966512345678", "test", context)

    assert receipt.status == DeliveryStatus.FAILED
    assert "retries" in receipt.error.lower()
