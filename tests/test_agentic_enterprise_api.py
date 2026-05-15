"""Agentic Enterprise OS — API smoke + registry wiring."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app

_ENVELOPE_KEYS = {"governance_decision", "matched_rules", "risk_level"}

_FULL_CAPABILITIES = {
    "redesign_workflows": 70,
    "execute_workflows": 65,
    "govern_workflows": 80,
    "evaluate_workflows": 60,
    "scale_workflows": 55,
    "supervise_agents": 75,
    "manage_digital_workforce": 50,
    "generate_executive_intelligence": 68,
    "measure_operational_impact": 62,
    "improve_continuously": 58,
}


def test_systems_endpoint_lists_twelve_systems() -> None:
    client = TestClient(app)
    r = client.get("/api/v1/enterprise/systems")
    assert r.status_code == 200
    body = r.json()
    assert set(body) >= _ENVELOPE_KEYS
    assert body["summary"]["systems_total"] == 12
    assert len(body["systems"]) == 12


def test_maturity_endpoint_without_scores_returns_null_emi() -> None:
    client = TestClient(app)
    r = client.get("/api/v1/enterprise/maturity")
    assert r.status_code == 200
    body = r.json()
    assert set(body) >= _ENVELOPE_KEYS
    assert body["maturity"]["emi"] is None
    assert len(body["maturity"]["capabilities_missing"]) == 10


def test_maturity_endpoint_with_full_scores_computes_emi() -> None:
    client = TestClient(app)
    r = client.get("/api/v1/enterprise/maturity", params=_FULL_CAPABILITIES)
    assert r.status_code == 200
    maturity = r.json()["maturity"]
    assert isinstance(maturity["emi"], (int, float))
    assert 0.0 <= maturity["emi"] <= 100.0
    assert maturity["stage"]["key"]
    assert maturity["stage"]["ar"] and maturity["stage"]["en"]


def test_evaluation_endpoint_reports_gaps() -> None:
    client = TestClient(app)
    r = client.get("/api/v1/enterprise/evaluation")
    assert r.status_code == 200
    evaluation = r.json()["evaluation"]
    assert evaluation["overall_score"] is None
    assert len(evaluation["gaps"]) == 6


def test_evolution_endpoint_smoke() -> None:
    client = TestClient(app)
    r = client.get("/api/v1/enterprise/evolution")
    assert r.status_code == 200
    body = r.json()
    assert set(body) >= _ENVELOPE_KEYS
    assert "recommendations" in body["evolution"]


def test_agents_endpoint_smoke() -> None:
    client = TestClient(app)
    r = client.get("/api/v1/enterprise/agents")
    assert r.status_code == 200
    body = r.json()
    assert set(body) >= _ENVELOPE_KEYS
    assert isinstance(body["agents_total"], int)


def test_scorecard_endpoint_with_full_scores() -> None:
    client = TestClient(app)
    r = client.get("/api/v1/enterprise/scorecard", params=_FULL_CAPABILITIES)
    assert r.status_code == 200
    scorecard = r.json()["scorecard"]
    assert scorecard["maturity"]["emi"] is not None
    assert scorecard["coverage"]["systems_total"] == 12
    assert scorecard["offer"]["recommended_offer"]


def test_scorecard_endpoint_without_scores_has_null_offer() -> None:
    client = TestClient(app)
    r = client.get("/api/v1/enterprise/scorecard")
    assert r.status_code == 200
    scorecard = r.json()["scorecard"]
    assert scorecard["maturity"]["emi"] is None
    assert scorecard["offer"] is None
