"""Unit tests for require_effective_tenant dependency."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from api.security.auth_deps import require_effective_tenant


@pytest.mark.asyncio
async def test_regular_user_returns_tenant():
    req = MagicMock()
    req.headers.get.return_value = None
    user = MagicMock()
    user.system_role = "tenant_admin"
    user.tenant_id = "ten_regular"
    tid = await require_effective_tenant(req, user)
    assert tid == "ten_regular"


@pytest.mark.asyncio
async def test_regular_user_missing_tenant_forbidden():
    req = MagicMock()
    user = MagicMock()
    user.system_role = "tenant_admin"
    user.tenant_id = None
    with pytest.raises(HTTPException) as ei:
        await require_effective_tenant(req, user)
    assert ei.value.status_code == 403


@pytest.mark.asyncio
async def test_super_admin_requires_header():
    req = MagicMock()
    req.headers.get.return_value = ""
    user = MagicMock()
    user.system_role = "super_admin"
    user.tenant_id = None
    with pytest.raises(HTTPException) as ei:
        await require_effective_tenant(req, user)
    assert ei.value.status_code == 400


@pytest.mark.asyncio
async def test_super_admin_with_header():
    req = MagicMock()
    req.headers.get.return_value = " ten_impersonate "
    user = MagicMock()
    user.system_role = "super_admin"
    tid = await require_effective_tenant(req, user)
    assert tid == "ten_impersonate"
