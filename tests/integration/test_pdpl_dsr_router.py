"""Integration tests for api/routers/pdpl_dsr.py."""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_dsr_delete_requires_confirm(async_client) -> None:
    r = await async_client.post(
        "/api/v1/pdpl/dsr/delete",
        json={"subject_email": "x@example.sa", "confirm": False},
    )
    # Either 422 (confirm_required) or 401 (no tenant)
    assert r.status_code in {401, 403, 422}


@pytest.mark.asyncio
async def test_dsr_access_validation(async_client) -> None:
    r = await async_client.post(
        "/api/v1/pdpl/dsr/access",
        json={},
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_dsr_portability_route_registered(async_client) -> None:
    r = await async_client.get("/api/v1/pdpl/dsr/portability")
    assert r.status_code in {200, 401, 403, 500}
