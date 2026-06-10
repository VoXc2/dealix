"""Tests for admin tenant management endpoints (W7.3)."""
from __future__ import annotations

import pytest

ADMIN_HEADER = "X-Admin-API-Key"


@pytest.mark.asyncio
async def test_list_tenants_requires_admin_key(async_client):
    res = await async_client.get("/api/v1/admin/tenants")
    # require_admin_key blocks without header (401 or 403)
    assert res.status_code in (401, 403)


@pytest.mark.asyncio
async def test_create_tenant_requires_admin_key(async_client):
    res = await async_client.post(
        "/api/v1/admin/tenants",
        json={"handle": "acme_saas", "name": "ACME"},
    )
    assert res.status_code in (401, 403)


@pytest.mark.asyncio
async def test_create_tenant_validates_handle(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_handle_validation")
    res = await async_client.post(
        "/api/v1/admin/tenants",
        json={"handle": "BAD-SLUG", "name": "X"},
        headers={ADMIN_HEADER: "test_admin_handle_validation"},
    )
    assert res.status_code == 400
    assert "handle" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_create_tenant_validates_plan(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_plan_validation")
    res = await async_client.post(
        "/api/v1/admin/tenants",
        json={"handle": "valid_slug", "name": "X", "plan": "bogus"},
        headers={ADMIN_HEADER: "test_admin_plan_validation"},
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_create_tenant_validates_locale(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_locale_validation")
    res = await async_client.post(
        "/api/v1/admin/tenants",
        json={"handle": "valid_slug", "name": "X", "locale": "ru"},
        headers={ADMIN_HEADER: "test_admin_locale_validation"},
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_create_tenant_validates_max_leads_bound(async_client, monkeypatch):
    """Pydantic enforces ge=1, le=1_000_000."""
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_bounds")
    # below lower bound
    res = await async_client.post(
        "/api/v1/admin/tenants",
        json={"handle": "valid_slug", "name": "X", "max_leads_per_month": 0},
        headers={ADMIN_HEADER: "test_admin_bounds"},
    )
    assert res.status_code == 422

    # above upper bound
    res = await async_client.post(
        "/api/v1/admin/tenants",
        json={"handle": "valid_slug", "name": "X", "max_leads_per_month": 99_999_999},
        headers={ADMIN_HEADER: "test_admin_bounds"},
    )
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_list_tenants_validates_status_filter(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_list_filter")
    res = await async_client.get(
        "/api/v1/admin/tenants?status=bogus",
        headers={ADMIN_HEADER: "test_admin_list_filter"},
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_list_tenants_pagination_params(async_client, monkeypatch):
    """limit must be 1-200, offset >= 0."""
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_pagination")
    # limit too large
    res = await async_client.get(
        "/api/v1/admin/tenants?limit=500",
        headers={ADMIN_HEADER: "test_admin_pagination"},
    )
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_get_tenant_validates_handle_format(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_get_handle")
    # Path-level regex rejects this
    res = await async_client.get(
        "/api/v1/admin/tenants/BAD-HANDLE",
        headers={ADMIN_HEADER: "test_admin_get_handle"},
    )
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_patch_tenant_validates_status(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_patch_status")
    res = await async_client.patch(
        "/api/v1/admin/tenants/valid_slug",
        json={"status": "bogus"},
        headers={ADMIN_HEADER: "test_admin_patch_status"},
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_patch_tenant_rejects_unknown_fields(async_client, monkeypatch):
    """Pydantic ConfigDict(extra='forbid') blocks unknown fields."""
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_patch_extra")
    res = await async_client.patch(
        "/api/v1/admin/tenants/valid_slug",
        json={"id": "tn_attacker_supplied"},  # id should be immutable
        headers={ADMIN_HEADER: "test_admin_patch_extra"},
    )
    assert res.status_code == 422
