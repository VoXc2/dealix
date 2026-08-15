"""Revenue OS workflow control surfaces must remain admin-only."""

from __future__ import annotations

import pytest
from fastapi import HTTPException
from fastapi.routing import APIRoute

from api.routers import revenue_os
from api.routers.revenue_os import router
from api.security.api_key import require_admin_key

_CONTROL_PATHS = {
    "/api/v1/revenue-os/workflows/run",
    "/api/v1/revenue-os/tasks",
    "/api/v1/revenue-os/tasks/{task_id}/approve",
    "/api/v1/revenue-os/tasks/{task_id}/reject",
    "/api/v1/revenue-os/workflows/runs/{run_id}",
    "/api/v1/revenue-os/workflows/runs/{run_id}/retry",
}


def test_workflow_control_surfaces_require_admin_key() -> None:
    protected: set[str] = set()
    for route in router.routes:
        if not isinstance(route, APIRoute) or route.path not in _CONTROL_PATHS:
            continue
        dependency_calls = {dependency.call for dependency in route.dependant.dependencies}
        assert require_admin_key in dependency_calls, route.path
        protected.add(route.path)

    assert protected == _CONTROL_PATHS


def test_production_control_surface_requires_explicit_tenant(monkeypatch) -> None:
    monkeypatch.setattr(revenue_os, "_APP_ENV", "production")
    with pytest.raises(HTTPException) as raised:
        revenue_os._control_tenant(None)
    assert raised.value.status_code == 400
    assert "tenant_id is required" in str(raised.value.detail)
