"""V12 Phase 7 — Delivery OS tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_status() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/delivery-os/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "delivery_os"


@pytest.mark.asyncio
async def test_create_session_returns_checklist() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/delivery-os/create-session",
            json={"customer_handle": "Slot-A", "service_id": "growth_starter"},
        )
    body = r.json()
    assert body["status"] == "new"
    assert len(body["checklist"]) == 8
    assert body["checklist"][0]["day"] == 0
    assert body["checklist"][-1]["day"] == 7


@pytest.mark.asyncio
async def test_get_session_after_create() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r1 = await client.post(
            "/api/v1/delivery-os/create-session",
            json={"customer_handle": "Slot-B", "service_id": "growth_starter"},
        )
        sid = r1.json()["id"]
        r2 = await client.get(f"/api/v1/delivery-os/session/{sid}")
    assert r2.status_code == 200
    assert r2.json()["customer_handle"] == "Slot-B"


@pytest.mark.asyncio
async def test_get_session_missing_returns_degraded_not_500() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/delivery-os/session/ds_doesnotexist")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "not_found"
    assert body["degraded"] is True


@pytest.mark.asyncio
async def test_next_step_advances_status() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r1 = await client.post(
            "/api/v1/delivery-os/create-session",
            json={"customer_handle": "Slot-C", "service_id": "growth_starter"},
        )
        sid = r1.json()["id"]
        r2 = await client.post(
            "/api/v1/delivery-os/next-step",
            json={"session_id": sid, "target_status": "in_progress"},
        )
    assert r2.status_code == 200
    assert r2.json()["status"] == "in_progress"
