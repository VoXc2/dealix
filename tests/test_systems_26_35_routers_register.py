"""Router registration smoke for enterprise governance/control surfaces.

Name kept for compatibility with existing hardening runbooks.
"""

from __future__ import annotations

from api.main import app


def test_control_and_governance_routers_are_registered() -> None:
    paths = {route.path for route in app.routes}
    required = {
        "/api/v1/agents/register",
        "/api/v1/data-os/import-preview",
        "/api/v1/audit/event",
        "/api/v1/value/event/{customer_id}",
        "/api/v1/workflow-os-v10/start",
        "/api/v1/revenue-os/catalog",
    }
    missing = sorted(required - paths)
    assert not missing, f"missing routes: {missing}"
