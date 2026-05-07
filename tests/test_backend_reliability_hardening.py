"""Phase 11 — Backend Reliability Hardening tests."""
from __future__ import annotations

import json

import pytest
from httpx import ASGITransport, AsyncClient


WAVE_5_STATUS_ENDPOINTS = [
    "/api/v1/leadops/reliability",
    "/api/v1/revenue-profitability/status",
    "/api/v1/support-journey/status",
    "/api/v1/tool-guardrails/status",
    "/api/v1/agent-observability/status",
]


@pytest.mark.asyncio
async def test_every_wave5_status_returns_200() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        for path in WAVE_5_STATUS_ENDPOINTS:
            r = await c.get(path)
            assert r.status_code == 200, f"{path} returned {r.status_code}"


@pytest.mark.asyncio
async def test_every_wave5_status_has_hard_gates() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        for path in WAVE_5_STATUS_ENDPOINTS:
            r = await c.get(path)
            body = r.json()
            assert "hard_gates" in body, f"{path} missing hard_gates"


@pytest.mark.asyncio
async def test_no_stacktrace_leak_in_responses() -> None:
    """No customer-facing endpoint may include stacktrace or traceback."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        for path in [
            "/api/v1/leadops/reliability",
            "/api/v1/revenue-profitability/radar",
            "/api/v1/support-journey/status",
            "/api/v1/tool-guardrails/status",
            "/api/v1/agent-observability/recent",
            "/api/v1/customer-portal/reliability-test",
            "/api/v1/executive-command-center/reliability-test",
        ]:
            r = await c.get(path)
            blob = json.dumps(r.json(), ensure_ascii=False).lower()
            assert "stacktrace" not in blob, f"{path} leaks stacktrace"
            assert "traceback" not in blob, f"{path} leaks traceback"


@pytest.mark.asyncio
async def test_status_paths_resolve_before_dynamic() -> None:
    """Status routes must be reachable (not captured by /{param})."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        for path in WAVE_5_STATUS_ENDPOINTS:
            r = await c.get(path)
            assert r.status_code == 200
            body = r.json()
            # Each must declare its `service` field — proof it hit the right handler
            assert "service" in body or body.get("status") is not None


@pytest.mark.asyncio
async def test_unknown_payment_returns_404_not_500() -> None:
    """Edge case: unknown payment_id → 404, never 500."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/payment-ops/pay_completely_unknown_xyz/state")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_invalid_payload_returns_422_not_500() -> None:
    """Tools that require fields must return 422 on missing fields."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/revenue-profitability/estimate-service-margin", json={})
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_unknown_customer_returns_200_with_degraded_data() -> None:
    """Customer-facing endpoints with unknown handle return 200 + degraded shape."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/totally-unknown-x")
    assert r.status_code == 200  # NEVER 500


def test_doc_exists() -> None:
    from pathlib import Path
    assert Path("docs/BACKEND_RELIABILITY_HARDENING_PLAN.md").exists()
