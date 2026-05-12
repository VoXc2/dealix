"""Integration tests for api/routers/sso.py."""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_sso_start_503_without_keys(async_client, monkeypatch) -> None:
    monkeypatch.delenv("WORKOS_API_KEY", raising=False)
    monkeypatch.delenv("WORKOS_CLIENT_ID", raising=False)
    from dealix.identity import workos_client as wc

    wc._singleton = None
    r = await async_client.get("/api/v1/auth/sso/start?org_id=org_test")
    assert r.status_code == 503
    assert r.json()["detail"] == "sso_disabled"


@pytest.mark.asyncio
async def test_sso_admin_portal_503_without_keys(async_client, monkeypatch) -> None:
    monkeypatch.delenv("WORKOS_API_KEY", raising=False)
    monkeypatch.delenv("WORKOS_CLIENT_ID", raising=False)
    from dealix.identity import workos_client as wc

    wc._singleton = None
    r = await async_client.post(
        "/api/v1/auth/sso/admin-portal",
        json={"organization_id": "org_test"},
    )
    assert r.status_code == 503
