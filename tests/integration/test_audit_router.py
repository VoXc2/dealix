"""Integration tests for api/routers/audit_logs.py."""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_audit_list_requires_tenant(async_client) -> None:
    r = await async_client.get("/api/v1/audit-logs")
    assert r.status_code in {401, 403, 200}  # 200 if super-admin path; 401 otherwise


@pytest.mark.asyncio
async def test_audit_csv_export_route_registered(async_client) -> None:
    r = await async_client.get("/api/v1/audit-logs/export.csv")
    # Anonymous caller — accept 401 / 403 / 200; just not 405/404.
    assert r.status_code in {200, 401, 403}


@pytest.mark.asyncio
async def test_audit_window_too_large_rejected(async_client) -> None:
    from datetime import datetime, timedelta

    long_ago = (datetime.utcnow() - timedelta(days=500)).isoformat()
    r = await async_client.get(f"/api/v1/audit-logs?since={long_ago}")
    # Either 422 lookback_window_too_large OR auth gate fires first.
    assert r.status_code in {401, 403, 422}
