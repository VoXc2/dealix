"""Phase 9 — Payment Ops state-machine tests.

Asserts:
- invoice_intent != revenue
- evidence_reference required for confirm
- delivery_kickoff requires payment_confirmed
- moyasar_live blocked unless DEALIX_MOYASAR_MODE=live
"""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_invoice_intent_creates_payment_in_intent_state() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/payment-ops/invoice-intent", json={
            "customer_handle": "pay-test-1",
            "amount_sar": 5000.0,
            "method": "bank_transfer",
        })
    assert r.status_code == 200
    body = r.json()
    pay = body["payment"]
    assert pay["status"] == "invoice_intent"
    assert pay["amount_sar"] == 5000.0
    assert pay["confirmed_at"] is None
    assert pay["confirmed_by"] is None
    assert body["warning_invoice_not_revenue"] == "invoice_intent != revenue"
    assert body["hard_gates"]["no_fake_revenue"] is True


@pytest.mark.asyncio
async def test_full_payment_to_delivery_lifecycle() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        intent = await c.post("/api/v1/payment-ops/invoice-intent", json={
            "customer_handle": "lifecycle-pay",
            "amount_sar": 12000.0,
            "method": "bank_transfer",
        })
        pid = intent.json()["payment"]["payment_id"]

        # Cannot confirm without evidence
        r = await c.post("/api/v1/payment-ops/confirm", json={
            "payment_id": pid, "confirmed_by": "founder",
        })
        assert r.status_code == 409  # state machine refuses

        # Upload evidence
        r = await c.post("/api/v1/payment-ops/manual-evidence", json={
            "payment_id": pid,
            "evidence_reference": "BANK-TXN-12345",
        })
        assert r.status_code == 200
        assert r.json()["payment"]["status"] == "payment_evidence_uploaded"

        # Now confirm
        r = await c.post("/api/v1/payment-ops/confirm", json={
            "payment_id": pid, "confirmed_by": "Sami Al-Foulan",
        })
        assert r.status_code == 200
        assert r.json()["payment"]["status"] == "payment_confirmed"
        assert r.json()["is_revenue_now"] is True
        assert r.json()["payment"]["confirmed_by"] == "Sami Al-Foulan"

        # Kickoff delivery
        r = await c.post(f"/api/v1/payment-ops/{pid}/kickoff-delivery")
        assert r.status_code == 200
        assert r.json()["payment"]["status"] == "delivery_kickoff"
        assert r.json()["delivery_kickoff_id"].startswith("dk_")


@pytest.mark.asyncio
async def test_delivery_blocked_without_payment_confirmed() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        intent = await c.post("/api/v1/payment-ops/invoice-intent", json={
            "customer_handle": "no-pay-test",
            "amount_sar": 5000.0,
            "method": "bank_transfer",
        })
        pid = intent.json()["payment"]["payment_id"]
        # Try to kickoff without confirming
        r = await c.post(f"/api/v1/payment-ops/{pid}/kickoff-delivery")
    assert r.status_code == 409
    assert "payment_confirmed" in r.json()["detail"]


@pytest.mark.asyncio
async def test_evidence_too_short_rejected() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        intent = await c.post("/api/v1/payment-ops/invoice-intent", json={
            "customer_handle": "short-ev-test",
            "amount_sar": 100.0,
            "method": "bank_transfer",
        })
        pid = intent.json()["payment"]["payment_id"]
        r = await c.post("/api/v1/payment-ops/manual-evidence", json={
            "payment_id": pid,
            "evidence_reference": "x",  # too short
        })
    assert r.status_code == 409
    assert "5_chars" in r.json()["detail"]


@pytest.mark.asyncio
async def test_moyasar_live_blocked_without_env() -> None:
    """NO_LIVE_CHARGE — moyasar_live refused unless explicit env opt-in."""
    import os
    # Ensure env is NOT set
    os.environ.pop("DEALIX_MOYASAR_MODE", None)
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/payment-ops/invoice-intent", json={
            "customer_handle": "live-test",
            "amount_sar": 5000.0,
            "method": "moyasar_live",
        })
    assert r.status_code == 403
    assert "DEALIX_MOYASAR_MODE=live" in r.json()["detail"]


@pytest.mark.asyncio
async def test_invalid_method_422() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/payment-ops/invoice-intent", json={
            "customer_handle": "x",
            "amount_sar": 100.0,
            "method": "stripe_live",  # not allowed
        })
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_state_endpoint_returns_is_revenue_flag() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        intent = await c.post("/api/v1/payment-ops/invoice-intent", json={
            "customer_handle": "state-test",
            "amount_sar": 5000.0,
            "method": "bank_transfer",
        })
        pid = intent.json()["payment"]["payment_id"]
        r = await c.get(f"/api/v1/payment-ops/{pid}/state")
    body = r.json()
    assert body["is_revenue"] is False  # invoice_intent is not revenue


@pytest.mark.asyncio
async def test_unknown_payment_404() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/payment-ops/pay_doesnotexist/state")
    assert r.status_code == 404
