"""API tests for operational fabric observability router."""

from __future__ import annotations

from starlette.testclient import TestClient

from api.main import app


def test_platform_contracts_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/platform/contracts")
    assert response.status_code == 200
    payload = response.json()
    assert payload["contracts_total"] == 41
    assert any(item["platform_path"] == "/platform/control_plane" for item in payload["contracts"])
    assert any(item["platform_path"] == "/platform/agent_mesh" for item in payload["contracts"])


def test_platform_contract_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/platform/contracts/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["systems_total"] == 10
    assert payload["contracts_total"] == 41
    assert payload["bindings_ok"] is True
