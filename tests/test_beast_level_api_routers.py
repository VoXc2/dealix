"""Smoke tests for V12.5 beast closure routers."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from api.main import app


@pytest.mark.asyncio
async def test_revops_finance_brief_endpoint() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/revops/finance-brief")
        assert r.status_code == 200
        body = r.json()
        assert body["schema_version"] == 1
        assert body["hard_gates"]["no_live_charge"] is True


@pytest.mark.asyncio
async def test_growth_beast_daily_loop_post() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/growth-beast/daily-loop",
            json={"company_profile": {"sector": "agency"}},
        )
        assert r.status_code == 200
        assert r.json()["experience_layer"] == "growth_beast_loop"


@pytest.mark.asyncio
async def test_proof_to_market_plan_post() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/proof-to-market/plan",
            json={"proof_events": [{"event_type": "x"}], "has_written_approval": False},
        )
        assert r.status_code == 200
        assert r.json()["schema_version"] == 1


@pytest.mark.asyncio
async def test_observability_beast_sample() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/observability-beast/sample-record")
        assert r.status_code == 200
        assert r.json()["redacted"] is True


@pytest.mark.asyncio
async def test_role_command_new_roles_exist() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        for role in ("delivery", "support", "operations"):
            r = await client.get(f"/api/v1/role-command/{role}")
            assert r.status_code == 200
            body = r.json()
            assert body["role"] == role
            assert body["guardrails"]["no_live_send"] is True
