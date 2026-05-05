"""V12 Phase 7 — Sales OS wrapper tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_status() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/sales-os/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "sales_os"
    assert body["hard_gates"]["no_guaranteed_claims"] is True


@pytest.mark.asyncio
async def test_qualify_high_score_recommends_pilot() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/sales-os/qualify",
            json={
                "has_warm_intro": True,
                "pain_described": True,
                "budget_signal": True,
                "authority_signal": True,
            },
        )
    body = r.json()
    assert body["score"] >= 75
    assert body["next_step"] == "offer_pilot"


@pytest.mark.asyncio
async def test_qualify_low_score_recommends_nurture() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/sales-os/qualify",
            json={
                "has_warm_intro": False,
                "pain_described": False,
                "budget_signal": False,
                "authority_signal": False,
            },
        )
    body = r.json()
    assert body["score"] < 40
    assert body["next_step"] == "nurture_only"


@pytest.mark.asyncio
async def test_objection_guarantee_request_blocked() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/sales-os/objection-response",
            json={"objection_text": "can you guarantee 10x revenue?"},
        )
    body = r.json()
    assert body["action_mode"] == "blocked"


@pytest.mark.asyncio
async def test_meeting_prep_returns_bilingual_agenda() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/sales-os/meeting-prep",
            json={"customer_handle": "Slot-A", "duration_min": 30},
        )
    body = r.json()
    assert len(body["agenda_ar"]) >= 4
    assert len(body["agenda_en"]) >= 4
    assert "must_avoid_ar" in body
