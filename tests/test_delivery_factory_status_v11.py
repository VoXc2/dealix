"""V11 Phase 3 — delivery-factory /status never 5xx."""
from __future__ import annotations

import os

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_status_returns_200_with_real_registry() -> None:
    from api.main import app

    os.environ.pop("DEALIX_REGISTRY_DIR", None)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/delivery-factory/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "delivery_factory"
    assert body["status"] == "operational"
    assert body["degraded"] is False
    assert body["services_total"] >= 1
    # Hard gates must be present and locked
    for gate in ("no_live_send", "no_scraping", "no_cold_outreach"):
        assert body["hard_gates"][gate] is True


@pytest.mark.asyncio
async def test_status_returns_200_degraded_when_registry_missing() -> None:
    """Bogus override → degraded 200, not 500."""
    from api.main import app

    os.environ["DEALIX_REGISTRY_DIR"] = "/no/such/v11/path/anywhere"
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as client:
            r = await client.get("/api/v1/delivery-factory/status")
        assert r.status_code == 200, "status must NEVER return 5xx"
        body = r.json()
        assert body["degraded"] is True
        assert body["blocker"] == "registry_missing"
        assert body["services_total"] == 0
        assert body["next_action_ar"]
        assert body["next_action_en"]
    finally:
        os.environ.pop("DEALIX_REGISTRY_DIR", None)


@pytest.mark.asyncio
async def test_services_endpoint_degrades_gracefully() -> None:
    from api.main import app

    os.environ["DEALIX_REGISTRY_DIR"] = "/no/such/v11/path/anywhere"
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as client:
            r = await client.get("/api/v1/delivery-factory/services")
        assert r.status_code == 200
        body = r.json()
        assert body["services"] == []
        assert body["degraded"] is True
    finally:
        os.environ.pop("DEALIX_REGISTRY_DIR", None)
