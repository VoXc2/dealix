"""V12 Phase 7 — Growth OS wrapper tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_status() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/growth-os/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "growth_os"
    assert body["hard_gates"]["no_scraping"] is True
    assert body["hard_gates"]["no_cold_outreach"] is True


@pytest.mark.asyncio
async def test_daily_plan_returns_safe_channels_only() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/growth-os/daily-plan",
            json={"sector": "b2b_services", "region": "riyadh"},
        )
    assert r.status_code == 200
    body = r.json()
    assert "warm_intro" in body["safe_channels"]
    assert "cold_whatsapp" in body["blocked_channels"]
    assert body["action_mode"] == "suggest_only"


@pytest.mark.asyncio
async def test_outreach_draft_warm_intro_returns_draft_only() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/growth-os/outreach-draft",
            json={"sector": "b2b_services", "audience": "warm_intro"},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["action_mode"] == "draft_only"
    assert body["send_method"] == "manual_only"
    assert "draft_ar" in body
    assert "draft_en" in body


@pytest.mark.asyncio
async def test_outreach_draft_unsafe_audience_blocked() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/growth-os/outreach-draft",
            json={"sector": "b2b_services", "audience": "cold_email"},
        )
    body = r.json()
    assert body["action_mode"] == "blocked"
