"""
Governance Engine API — endpoint behaviour.

The router is mounted on a standalone FastAPI app for this test. The full
`api.main` app currently has an unrelated pre-existing import break in the
`value_os` package; the router under test is fully exercised here regardless.
"""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.governance_engine import router
from dealix.classifications import ApprovalClass, ReversibilityClass, SensitivityClass
from dealix.contracts.decision import DecisionOutput, Evidence, NextAction


@pytest.fixture()
def client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def _decision_payload() -> dict:
    decision = DecisionOutput(
        entity_id="lead_api_1",
        objective="qualify_lead",
        agent_name="api_test",
        recommendation={"verdict": "qualified"},
        confidence=0.9,
        rationale="api test rationale",
        approval_class=ApprovalClass.A3,
        reversibility_class=ReversibilityClass.R3,
        sensitivity_class=SensitivityClass.S3,
        evidence=[Evidence(source="hubspot.contact", excerpt="excerpt")],
        next_actions=[
            NextAction(
                action_type="pricing_offer_commit",
                description="commit a price",
                approval_class=ApprovalClass.A3,
                reversibility_class=ReversibilityClass.R3,
                sensitivity_class=SensitivityClass.S3,
            )
        ],
    )
    return decision.model_dump(mode="json")


def test_status_endpoint(client: TestClient) -> None:
    resp = client.get("/api/v1/governance-engine/status")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["engine_count"] == 12
    assert body["read_only"] is True
    assert body["governance_engine"]["engine"]["engine_id"] == "governance"


def test_engines_endpoint_lists_twelve(client: TestClient) -> None:
    resp = client.get("/api/v1/governance-engine/engines")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["engine_count"] == 12
    assert len(body["engines"]) == 12
    governance = next(e for e in body["engines"] if e["engine_id"] == "governance")
    assert governance["status"] == "production"


def test_engines_status_endpoint(client: TestClient) -> None:
    resp = client.get("/api/v1/governance-engine/engines/status")
    assert resp.status_code == 200, resp.text
    assert len(resp.json()["reports"]) == 12


def test_evaluate_endpoint_escalates_and_explains(client: TestClient) -> None:
    resp = client.post(
        "/api/v1/governance-engine/evaluate", json=_decision_payload()
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert len(body["evaluations"]) == 1
    ev = body["evaluations"][0]
    assert ev["verdict"] == "escalate"
    assert ev["explanation"]["human_readable_ar"]


def test_explain_endpoint_replays_decision(client: TestClient) -> None:
    payload = _decision_payload()
    evaluate = client.post("/api/v1/governance-engine/evaluate", json=payload)
    decision_id = evaluate.json()["decision_id"]
    resp = client.get(f"/api/v1/governance-engine/explain/{decision_id}")
    assert resp.status_code == 200, resp.text
    explanations = resp.json()
    assert explanations
    assert explanations[0]["decision_id"] == decision_id


def test_risk_snapshot_endpoint(client: TestClient) -> None:
    resp = client.get("/api/v1/governance-engine/risk-snapshot")
    assert resp.status_code == 200, resp.text
    assert resp.json()["never_auto_execute_actions"]


def test_audit_recent_endpoint(client: TestClient) -> None:
    client.post("/api/v1/governance-engine/evaluate", json=_decision_payload())
    resp = client.get("/api/v1/governance-engine/audit/recent", params={"limit": 50})
    assert resp.status_code == 200, resp.text
    assert isinstance(resp.json(), list)
