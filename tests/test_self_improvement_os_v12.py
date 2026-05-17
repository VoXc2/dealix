"""V12 Phase 7 — Self-Improvement OS tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_status() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/self-improvement-os/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "self_improvement_os"
    assert body["hard_gates"]["no_self_modifying_code"] is True
    assert body["hard_gates"]["no_automatic_pr"] is True
    assert body["hard_gates"]["no_fake_metrics"] is True


@pytest.mark.asyncio
async def test_weekly_learning_returns_suggest_only() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/self-improvement-os/weekly-learning")
    body = r.json()
    # Full Ops 2.0 — real learning loops replace the placeholder stubs.
    assert len(body["learning_loops"]) == 2
    for loop in body["learning_loops"]:
        assert loop["action_mode"] == "suggest_only"
