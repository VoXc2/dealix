"""Phase 6 — Revenue Profitability tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.revenue_profitability import (
    compute_gross_margin,
    estimate_service_cost,
    finance_radar_summary,
    is_revenue,
    revenue_summary,
)


def test_is_revenue_strict_rule() -> None:
    """Only payment_confirmed and delivery_kickoff count as revenue."""
    assert is_revenue("payment_confirmed") is True
    assert is_revenue("delivery_kickoff") is True
    assert is_revenue("invoice_intent") is False
    assert is_revenue("invoice_sent_manual") is False
    assert is_revenue("payment_pending") is False
    assert is_revenue("payment_evidence_uploaded") is False
    assert is_revenue("refunded") is False
    assert is_revenue("voided") is False


def test_revenue_summary_zero_when_no_payments() -> None:
    summary = revenue_summary(customer_handle="rp-empty-test")
    assert summary["confirmed_revenue_sar"] == 0.0
    assert summary["confirmed_count"] == 0


def test_estimate_service_cost_returns_breakdown() -> None:
    cost = estimate_service_cost(service_type="leadops_sprint")
    assert "ai_cost_sar" in cost
    assert "founder_cost_sar" in cost
    assert "support_cost_sar" in cost
    assert "delivery_cost_sar" in cost
    assert "total_cost_sar" in cost
    assert cost["is_estimate"] is True


def test_compute_gross_margin_marks_estimate() -> None:
    margin = compute_gross_margin(
        service_type="leadops_sprint",
        revenue_sar=1500.0,
    )
    assert margin["is_estimate"] is True
    assert "gross_margin_sar" in margin
    assert "gross_margin_pct" in margin
    assert "is_profitable" in margin


def test_gross_margin_unprofitable_at_low_price() -> None:
    """leadops_sprint at 499 SAR may not be profitable given founder time."""
    margin = compute_gross_margin(
        service_type="leadops_sprint",
        revenue_sar=499.0,
    )
    # Should detect this is below cost
    assert margin["gross_margin_sar"] < 0 or margin["gross_margin_pct"] < 50


def test_gross_margin_profitable_at_partner_price() -> None:
    """Partner tier (12,000/mo) should be profitable."""
    margin = compute_gross_margin(
        service_type="growth_proof_sprint",
        revenue_sar=12000.0,
    )
    assert margin["is_profitable"] is True
    assert margin["gross_margin_sar"] > 0


def test_finance_radar_summary_returns_dict() -> None:
    summary = finance_radar_summary()
    assert "at_risk_top_3" in summary
    assert "unprofitable_top_3" in summary
    assert summary["is_estimate"] is True


@pytest.mark.asyncio
async def test_status_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/revenue-profitability/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "revenue_profitability"
    assert body["hard_gates"]["no_fake_revenue"] is True
    assert body["hard_gates"]["only_payment_confirmed_counts_as_revenue"] is True


@pytest.mark.asyncio
async def test_estimate_service_margin_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/revenue-profitability/estimate-service-margin", json={
            "service_type": "leadops_sprint",
            "revenue_sar": 1500.0,
        })
    assert r.status_code == 200
    body = r.json()
    assert body["is_estimate"] is True
    assert "gross_margin_sar" in body


@pytest.mark.asyncio
async def test_estimate_endpoint_requires_fields() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/revenue-profitability/estimate-service-margin", json={})
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_radar_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/revenue-profitability/radar")
    assert r.status_code == 200
    body = r.json()
    assert "at_risk_top_3" in body
    assert "unprofitable_top_3" in body


@pytest.mark.asyncio
async def test_revenue_summary_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/revenue-profitability/revenue-summary?customer_handle=rp-summary-test")
    body = r.json()
    assert "confirmed_revenue_sar" in body
    assert body["is_estimate"] is False  # revenue ground truth is not estimate


@pytest.mark.asyncio
async def test_invoice_intent_does_not_count_as_revenue() -> None:
    """Create an invoice_intent but no confirmation; revenue must be 0."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        # Create invoice intent only
        await c.post("/api/v1/payment-ops/invoice-intent", json={
            "customer_handle": "rp-no-revenue-test",
            "amount_sar": 5000.0,
            "method": "bank_transfer",
        })
        r = await c.get("/api/v1/revenue-profitability/revenue-summary?customer_handle=rp-no-revenue-test")
    body = r.json()
    # invoice_intent != revenue
    assert body["confirmed_revenue_sar"] == 0.0
    assert body["confirmed_count"] == 0


@pytest.mark.asyncio
async def test_payment_confirmed_counts_as_revenue() -> None:
    """Full payment lifecycle → revenue appears."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        intent = await c.post("/api/v1/payment-ops/invoice-intent", json={
            "customer_handle": "rp-revenue-test",
            "amount_sar": 5000.0,
            "method": "bank_transfer",
        })
        pid = intent.json()["payment"]["payment_id"]
        await c.post("/api/v1/payment-ops/manual-evidence", json={
            "payment_id": pid, "evidence_reference": "BANK-TXN-PROFIT-001",
        })
        await c.post("/api/v1/payment-ops/confirm", json={
            "payment_id": pid, "confirmed_by": "founder",
        })
        r = await c.get("/api/v1/revenue-profitability/revenue-summary?customer_handle=rp-revenue-test")
    body = r.json()
    assert body["confirmed_revenue_sar"] == 5000.0
    assert body["confirmed_count"] == 1
