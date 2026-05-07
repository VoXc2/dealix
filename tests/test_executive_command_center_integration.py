"""Phase 5 — Executive Command Center tests."""
from __future__ import annotations

import json

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.executive_command_center import (
    build_command_center,
    build_daily,
    build_weekly,
)


def test_build_command_center_returns_view() -> None:
    view = build_command_center(customer_handle="ecc-test-1")
    assert view.customer_handle == "ecc-test-1"
    assert view.cadence == "snapshot"


def test_build_daily_sets_cadence() -> None:
    v = build_daily(customer_handle="ecc-daily")
    assert v.cadence == "daily"


def test_build_weekly_sets_cadence() -> None:
    v = build_weekly(customer_handle="ecc-weekly")
    assert v.cadence == "weekly"


def test_safety_summary_present() -> None:
    v = build_command_center(customer_handle="ecc-safety")
    assert "no_fake_revenue" in v.safety_summary
    assert "no_fake_proof" in v.safety_summary


def test_today_3_decisions_max_3() -> None:
    v = build_command_center(customer_handle="ecc-decisions")
    assert len(v.today_3_decisions) <= 3


def test_no_fake_revenue_when_no_payment() -> None:
    v = build_command_center(customer_handle="ecc-no-payment")
    assert v.revenue_radar.get("confirmed_payments_count", 0) == 0
    assert v.revenue_radar.get("confirmed_revenue_sar", 0) == 0


def test_no_fake_proof_when_no_proof() -> None:
    v = build_command_center(customer_handle="ecc-no-proof")
    assert v.proof_ledger.get("proof_events_count", 0) == 0


@pytest.mark.asyncio
async def test_status_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/executive-command-center/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "executive_command_center"
    assert body["section_count"] == 15
    assert body["hard_gates"]["no_fake_revenue"] is True


@pytest.mark.asyncio
async def test_customer_endpoint_returns_15_sections() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/executive-command-center/ecc-15")
    assert r.status_code == 200
    view = r.json()["view"]
    expected = [
        "executive_summary", "full_ops_score", "today_3_decisions",
        "revenue_radar", "sales_pipeline", "growth_radar",
        "partnership_radar", "support_inbox", "delivery_operations",
        "finance_state", "proof_ledger", "risks_compliance",
        "approval_center", "whatsapp_decision_preview",
    ]
    for sec in expected:
        assert sec in view, f"missing section: {sec}"


@pytest.mark.asyncio
async def test_customer_facing_no_internal_terms() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/executive-command-center/ecc-leak-test")
    blob = json.dumps(r.json(), ensure_ascii=False).lower()
    forbidden = ["v11", "v12", "v13", "v14", "router", "verifier",
                 "growth_beast", "stacktrace", "pytest"]
    for f in forbidden:
        assert f not in blob, f"ECC leaks internal term: {f}"


@pytest.mark.asyncio
async def test_daily_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/executive-command-center/ecc-daily/daily")
    assert r.status_code == 200
    assert r.json()["view"]["cadence"] == "daily"


@pytest.mark.asyncio
async def test_weekly_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/executive-command-center/ecc-weekly/weekly")
    assert r.status_code == 200
    assert r.json()["view"]["cadence"] == "weekly"


@pytest.mark.asyncio
async def test_no_500_on_unknown_customer() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/executive-command-center/totally-unknown-zzz")
    assert r.status_code == 200
