"""Enterprise control plane import smoke tests."""

from __future__ import annotations


def test_api_imports_without_errors() -> None:
    from api.main import app

    assert app is not None


def test_systems_26_35_routers_registered() -> None:
    from api.main import app

    registered_paths = {route.path for route in app.routes}
    required_paths = {
        "/api/v1/control-plane/health",
        "/api/v1/agent-mesh/health",
        "/api/v1/assurance-contracts/health",
        "/api/v1/sandbox/health",
        "/api/v1/org-graph/health",
        "/api/v1/runtime-safety/health",
        "/api/v1/simulation/health",
        "/api/v1/human-ai/health",
        "/api/v1/value-engine/health",
        "/api/v1/self-evolving/health",
    }
    assert required_paths.issubset(registered_paths)
