"""Tests for GET /api/v1/customer-portal/{handle}/subscription.

Verifies the new endpoint added in Phase G:
  - Returns 200 with inactive status when no schedules exist
  - Returns latest schedule fields when present
  - Doctrine: no internal terminology leaked, no live charge triggered
"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_subscription_no_schedules_returns_inactive() -> None:
    from api.main import app

    with patch(
        "auto_client_acquisition.payment_ops.renewal_scheduler.list_by_customer",
        return_value=[],
    ):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as c:
            r = await c.get("/api/v1/customer-portal/acme/subscription")
    assert r.status_code == 200
    body = r.json()
    assert body["customer_handle"] == "acme"
    assert body["status"] == "inactive"
    assert body["mrr_sar"] == 0
    assert body["next_renewal_at"] is None
    assert body["source"] == "renewal_scheduler"


@pytest.mark.asyncio
async def test_subscription_returns_latest_schedule() -> None:
    from api.main import app
    from auto_client_acquisition.payment_ops.renewal_scheduler import RenewalSchedule

    fake = RenewalSchedule(
        schedule_id="rnw_test",
        customer_id="acme",
        plan="managed_revenue_ops_growth",
        amount_sar=4999,
        cadence_days=30,
        next_attempt_at="2026-07-01T00:00:00+00:00",
        cycle_count=3,
        status="scheduled",
    )
    with patch(
        "auto_client_acquisition.payment_ops.renewal_scheduler.list_by_customer",
        return_value=[fake],
    ):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as c:
            r = await c.get("/api/v1/customer-portal/acme/subscription")
    assert r.status_code == 200
    body = r.json()
    assert body["plan"] == "managed_revenue_ops_growth"
    assert body["mrr_sar"] == 4999
    assert body["next_renewal_at"] == "2026-07-01T00:00:00+00:00"
    assert body["cycles_completed"] == 3


@pytest.mark.asyncio
async def test_subscription_no_internal_terminology_leak() -> None:
    """Article 6 #2 — public endpoint must not leak internal names."""
    from api.main import app

    with patch(
        "auto_client_acquisition.payment_ops.renewal_scheduler.list_by_customer",
        return_value=[],
    ):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as c:
            r = await c.get("/api/v1/customer-portal/acme/subscription")
    text = r.text.lower()
    # source field intentionally names renewal_scheduler as the data origin;
    # but no version labels, agent names, or wave labels should appear.
    for forbidden in ("wave", "v10", "v11", "v12", "v13", "agent_os", "claude"):
        assert forbidden not in text, f"leaked internal term: {forbidden}"
