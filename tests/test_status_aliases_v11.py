"""V11 Phase 2 — canonical status alias tests.

Asserts that all 7 documented status endpoints respond 200 with the
v11 canonical fields, and that ``role-command/status`` is NOT routed
through the ``/{role}`` catchall.
"""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


_ALIASES = (
    "/api/v1/role-command/status",
    "/api/v1/role-command/_status",
    "/api/v1/approvals/status",
    "/api/v1/founder/status",
    "/api/v1/delivery-factory/status",
    "/api/v1/v10/status",
    "/api/v1/v11/status",
)


@pytest.mark.asyncio
async def test_every_alias_returns_200() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        for path in _ALIASES:
            r = await client.get(path)
            assert r.status_code == 200, (
                f"{path} returned {r.status_code} (must be 200): {r.text[:200]}"
            )


@pytest.mark.asyncio
async def test_role_command_status_is_not_treated_as_role() -> None:
    """``/api/v1/role-command/status`` must hit the status route, NOT the
    ``/{role}`` catchall. We verify by checking the response shape:
    role-brief responses include ``summary_ar``; status responses don't.
    """
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/role-command/status")
    assert r.status_code == 200
    body = r.json()
    assert body.get("module") == "role_command_os"
    assert "roles" in body
    # role-brief has summary_ar; status doesn't
    assert "summary_ar" not in body


@pytest.mark.asyncio
async def test_role_command_underscore_alias_returns_status_payload() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/role-command/_status")
    assert r.status_code == 200
    body = r.json()
    assert body.get("module") == "role_command_os"
    assert body["service"] == "role_command_os"


@pytest.mark.asyncio
async def test_v10_umbrella_status_includes_all_modules() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/v10/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "v10_umbrella"
    assert body["modules_total"] == 10
    # Hard gates locked
    for gate in ("no_live_send", "no_live_charge", "no_scraping",
                 "no_cold_outreach"):
        assert body["hard_gates"][gate] is True


@pytest.mark.asyncio
async def test_v11_status_reports_v11_signals() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/v11/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "v11_customer_closure"
    # 9 hard gates including v11-specific
    for gate in ("no_live_send", "no_live_charge", "no_scraping",
                 "no_linkedin_automation", "no_fake_proof"):
        assert body["hard_gates"][gate] is True


@pytest.mark.asyncio
async def test_no_status_alias_returns_5xx() -> None:
    """Strong perimeter: every alias must be 2xx, never 5xx."""
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        for path in _ALIASES:
            r = await client.get(path)
            assert 200 <= r.status_code < 300, f"{path} returned {r.status_code}"
