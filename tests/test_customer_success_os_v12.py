"""V12 Phase 7 — Customer Success OS tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_status() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/customer-success-os/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "customer_success_os"


@pytest.mark.asyncio
async def test_health_score_high_signals_excellent() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/customer-success-os/health-score",
            json={
                "intake_complete": True,
                "diagnostic_delivered": True,
                "proof_events_count": 3,
                "open_support_tickets": 0,
                "last_customer_response_days": 1,
                "delivery_sla_status": "on_track",
                "payment_status": "paid",
                "renewal_signal": True,
            },
        )
    body = r.json()
    assert body["score"] >= 81
    assert body["band"] == "excellent"


@pytest.mark.asyncio
async def test_health_score_no_signals_band_high_risk() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/customer-success-os/health-score",
            json={
                "intake_complete": False,
                "diagnostic_delivered": False,
                "open_support_tickets": 3,
                "last_customer_response_days": 30,
                "payment_status": "overdue",
            },
        )
    body = r.json()
    assert body["band"] in {"high_risk", "needs_attention"}


@pytest.mark.asyncio
async def test_weekly_checkin_draft_only() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/customer-success-os/weekly-checkin-draft",
            json={"customer_handle": "Slot-A", "week": 2},
        )
    body = r.json()
    assert body["action_mode"] == "draft_only"
    assert body["send_method"] == "manual_only"
