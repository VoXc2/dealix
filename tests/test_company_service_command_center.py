"""Company service command center — customer-safe JSON."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app


def test_company_command_center_200_and_no_internal_jargon_keys() -> None:
    c = TestClient(create_app())
    r = c.get("/api/v1/company-service/command-center")
    assert r.status_code == 200
    body = r.json()
    assert body.get("experience_layer") == "company_portal"
    assert "north_star_hint_ar" in body
    assert "hard_gates" in body
    # Should not expose raw module names as top-level keys
    assert "agents" not in body
    assert "command_center_snapshot" not in body


def test_company_service_status() -> None:
    c = TestClient(create_app())
    r = c.get("/api/v1/company-service/status")
    assert r.status_code == 200
    assert r.json()["module"] == "company_service"
