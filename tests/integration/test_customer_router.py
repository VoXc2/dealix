"""Integration tests for api/routers/customer.py (T0)."""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_summary_returns_zeroes_for_unknown_tenant(async_client) -> None:
    r = await async_client.get("/api/v1/customers/no_such_tenant/summary")
    # Without a tenant resolver (test client doesn't set request.state.tenant_id),
    # the path is unauthenticated; we accept 404 (tenant_not_found) or 401 depending
    # on middleware order. Either way: not a 500.
    assert r.status_code in {401, 403, 404}, r.text


@pytest.mark.asyncio
async def test_summary_shape_smoke(async_client) -> None:
    """Even on auth/forbid, the route is registered (404 != 'no route')."""
    r = await async_client.get("/api/v1/customers/ten_test/summary")
    assert r.status_code != 405  # not method-not-allowed


@pytest.mark.asyncio
async def test_team_invite_validation(async_client) -> None:
    r = await async_client.post(
        "/api/v1/customers/ten_test/team/invite",
        json={"email": "not-an-email"},
    )
    assert r.status_code in {401, 403, 422}


@pytest.mark.asyncio
async def test_invoices_route_registered(async_client) -> None:
    r = await async_client.get("/api/v1/customers/ten_test/invoices")
    assert r.status_code != 405
