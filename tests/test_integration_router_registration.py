"""Phase 16 — Router registration tests.

Asserts:
- All 7 new routers register in OpenAPI
- Existing customer portal route still appears
- /status routes resolve before /{param} dynamic routes
"""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_openapi_includes_all_new_routers() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/openapi.json")
    spec = r.json()
    paths = list(spec.get("paths", {}).keys())

    required_prefixes = [
        "/api/v1/unified-operating-graph/",
        "/api/v1/full-ops-radar/",
        "/api/v1/executive-command-center/",
        "/api/v1/whatsapp-decision/",
        "/api/v1/channel-policy/",
        "/api/v1/radar-events/",
        "/api/v1/agent-observability/",
    ]
    for prefix in required_prefixes:
        matches = [p for p in paths if p.startswith(prefix)]
        assert matches, f"no route registered with prefix {prefix}"


@pytest.mark.asyncio
async def test_existing_customer_portal_still_registered() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/openapi.json")
    paths = list(r.json().get("paths", {}).keys())
    assert any("/api/v1/customer-portal/" in p for p in paths)


@pytest.mark.asyncio
async def test_status_routes_static_before_dynamic() -> None:
    """Each /status route must be hit by exact match, not captured by
    /{param} dynamic match. Verify that GET /api/v1/.../status returns
    the expected status payload (not a 404 or wrong JSON shape)."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        for path in [
            "/api/v1/unified-operating-graph/status",
            "/api/v1/full-ops-radar/status",
            "/api/v1/executive-command-center/status",
            "/api/v1/whatsapp-decision/status",
            "/api/v1/channel-policy/status",
            "/api/v1/radar-events/status",
            "/api/v1/agent-observability/status",
        ]:
            r = await c.get(path)
            assert r.status_code == 200, f"status route broken: {path}"
            body = r.json()
            assert "service" in body, f"status payload wrong for {path}"
            assert "hard_gates" in body, f"hard_gates missing for {path}"


@pytest.mark.asyncio
async def test_no_breaking_change_on_legacy_routes() -> None:
    """Existing pre-Wave-4 routes still register (verify via OpenAPI)."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/openapi.json")
    paths = list(r.json().get("paths", {}).keys())
    legacy_required = [
        "/api/v1/customer-portal/{customer_handle}",
        "/api/v1/leadops/status",
        "/api/v1/service-sessions/start",
        "/api/v1/approvals/status",
        "/api/v1/proof-ledger/status",
        "/api/v1/case-study/library",
    ]
    for legacy_path in legacy_required:
        assert legacy_path in paths, f"legacy route disappeared from OpenAPI: {legacy_path}"


@pytest.mark.asyncio
async def test_new_routers_have_hard_gates() -> None:
    """Constitutional: every new endpoint must include _HARD_GATES dict."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        for path in [
            "/api/v1/unified-operating-graph/status",
            "/api/v1/full-ops-radar/status",
            "/api/v1/executive-command-center/status",
            "/api/v1/whatsapp-decision/status",
            "/api/v1/channel-policy/status",
            "/api/v1/radar-events/status",
            "/api/v1/agent-observability/status",
        ]:
            r = await c.get(path)
            assert "hard_gates" in r.json(), f"hard_gates missing on {path}"
