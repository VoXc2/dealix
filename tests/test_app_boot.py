"""App-boot smoke test — guards against shipping routers whose backing
modules don't exist (the failure mode that left api.main unimportable).

This is the cheapest possible regression net: if any router imports a
symbol that was never built, `import api.main` fails and this test fails.
"""
from __future__ import annotations

from fastapi.testclient import TestClient


def test_app_imports_and_builds() -> None:
    from api.main import app

    assert app is not None
    # A real Dealix build mounts well over 100 routes; a near-empty app
    # means routers silently failed to register.
    route_count = len(app.routes)
    assert route_count > 100, f"only {route_count} routes mounted — routers missing"


def test_health_endpoint_responds() -> None:
    from api.main import app

    with TestClient(app) as client:
        resp = client.get("/health")
        assert resp.status_code == 200, resp.text
        body = resp.json()
        assert body.get("ok") is True or body.get("status") == "ok", body


def test_openapi_schema_generates() -> None:
    """A broken response_model or router crashes OpenAI schema generation."""
    from api.main import app

    with TestClient(app) as client:
        resp = client.get("/openapi.json")
        assert resp.status_code == 200, resp.text
        schema = resp.json()
        assert schema.get("openapi", "").startswith("3.")
        assert len(schema.get("paths", {})) > 100


def test_core_service_routers_mounted() -> None:
    """The commercial service-delivery endpoints must be reachable."""
    from api.main import app

    paths = {
        route.path for route in app.routes if hasattr(route, "path")
    }
    for required in (
        "/health",
        "/api/v1/data-os/import-preview",
        "/api/v1/value/event/{customer_id}",
    ):
        assert required in paths, f"missing route: {required}"
