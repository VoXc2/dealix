"""API tests for institutional operating core router."""

from __future__ import annotations

from starlette.testclient import TestClient

from api.main import app


def test_institutional_operating_core_status() -> None:
    client = TestClient(app)
    resp = client.get("/api/v1/institutional-operating-core/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["service"] == "institutional_operating_core"
    assert len(data["systems_56_to_65"]) == 10


def test_dependency_verdict_requires_readiness_and_dependency() -> None:
    client = TestClient(app)
    body = {
        "decision_dependency_pct": 90,
        "execution_dependency_pct": 90,
        "governance_dependency_pct": 90,
        "memory_dependency_pct": 90,
        "resilience_dependency_pct": 90,
        "economic_dependency_pct": 90,
        "systems_ready": {
            "56_control_plane": True,
            "57_agent_society_engine": True,
            "58_assurance_and_safety_contracts": True,
            "59_institutional_memory_fabric": True,
            "60_organizational_reasoning_engine": True,
            "61_resilience_and_chaos_engine": True,
            "62_meta_governance_engine": True,
            "63_institutional_value_engine": True,
            "64_institutional_learning_engine": True,
            "65_institutional_operating_core": True,
        },
    }
    resp = client.post("/api/v1/institutional-operating-core/dependency/verdict", json=body)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "institutional_operational_infrastructure"
    assert data["infrastructure_status"] is True
