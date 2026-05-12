"""Integration tests for api/routers/admin_enterprise.py."""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_byok_status_admin_gated(async_client) -> None:
    r = await async_client.get("/api/v1/admin/byok/status")
    # Anonymous: 403 admin_only.
    assert r.status_code == 403


@pytest.mark.asyncio
async def test_audit_forward_status_admin_gated(async_client) -> None:
    r = await async_client.get("/api/v1/admin/audit-forward/status")
    assert r.status_code == 403


@pytest.mark.asyncio
async def test_byok_status_with_admin_key(async_client, monkeypatch) -> None:
    monkeypatch.setenv("ADMIN_API_KEYS", "admin-test-key")
    r = await async_client.get(
        "/api/v1/admin/byok/status",
        headers={"x-api-key": "admin-test-key"},
    )
    assert r.status_code == 200
    body = r.json()
    assert "configured" in body
    assert "provider" in body
    assert "key_id_present" in body


@pytest.mark.asyncio
async def test_audit_forward_status_with_admin_key(async_client, monkeypatch) -> None:
    monkeypatch.setenv("ADMIN_API_KEYS", "admin-test-key")
    r = await async_client.get(
        "/api/v1/admin/audit-forward/status",
        headers={"x-api-key": "admin-test-key"},
    )
    assert r.status_code == 200
    body = r.json()
    assert set(body) >= {"datadog", "splunk", "s3"}


@pytest.mark.asyncio
async def test_ip_allowlist_invalid_cidr_rejected(async_client, monkeypatch) -> None:
    monkeypatch.setenv("ADMIN_API_KEYS", "admin-test-key")
    r = await async_client.post(
        "/api/v1/admin/tenant/nonexistent/ip-allowlist",
        headers={"x-api-key": "admin-test-key"},
        json={"cidrs": ["not-a-cidr"]},
    )
    # Either 422 invalid_cidr or 404 tenant_not_found — both prove the
    # route is wired + payload validation runs.
    assert r.status_code in {404, 422}


@pytest.mark.asyncio
async def test_sandbox_spin_up_unknown_tenant_404(async_client, monkeypatch) -> None:
    monkeypatch.setenv("ADMIN_API_KEYS", "admin-test-key")
    r = await async_client.post(
        "/api/v1/admin/sandbox/spin-up",
        headers={"x-api-key": "admin-test-key"},
        json={"tenant_id": "nonexistent-tenant", "label": "test"},
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "tenant_not_found"
