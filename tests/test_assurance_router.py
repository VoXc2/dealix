"""Assurance System — HTTP router integration tests.

Mounts only the assurance router on a minimal FastAPI app so the test is
fast and isolated from the full application bootstrap.
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.assurance import router

_app = FastAPI()
_app.include_router(router)
_client = TestClient(_app)


def test_status_endpoint() -> None:
    resp = _client.get("/api/v1/assurance/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["config_loaded"] is True
    assert len(body["layers"]) == 7
    assert body["hard_gates"]["read_only"] is True


def test_get_report_empty_inputs() -> None:
    body = _client.get("/api/v1/assurance/report").json()
    assert body["verdict"] == "no_scale"
    assert len(body["gates"]) == 6
    assert len(body["acceptance_tests"]) == 25


def test_post_report_with_inputs() -> None:
    payload = {
        "funnel_counts": {"attention": 100, "lead": 30},
        "machine_maturity": {"sales_autopilot": 4},
    }
    body = _client.post("/api/v1/assurance/report", json=payload).json()
    assert body["health"]["total"] == 16.0  # (4/5)*20
    rungs = {r["key"]: r["count"] for r in body["funnel"]["rungs"]}
    assert rungs["attention"] == 100
    assert rungs["paid"] is None  # unknown, not fabricated


def test_post_report_full_scale_verdict() -> None:
    from auto_client_acquisition.assurance_os.gates import GATE_SPECS

    payload = {
        "gate_answers": {cid: True for _, _, _, cs in GATE_SPECS for cid, _, _ in cs},
        "machine_maturity": {
            "sales_autopilot": 5, "marketing_factory": 5, "support_autopilot": 5,
            "delivery_factory": 5, "partner_machine": 5, "affiliate_machine": 5,
            "approval_center": 5, "evidence_ledger": 5, "no_build_engine": 5,
            "reporting": 5,
        },
        "evidence_completeness_pct": 95,
        "lead_scoring_coverage_pct": 100,
        "support_high_risk_escalation_pct": 100,
        "affiliate_payout_before_payment_count": 0,
        "approval_compliance_pct": 100,
    }
    body = _client.post("/api/v1/assurance/report", json=payload).json()
    assert body["verdict"] == "scale"


def test_layer_endpoints() -> None:
    assert len(_client.get("/api/v1/assurance/gates").json()["gates"]) == 6
    assert len(_client.get("/api/v1/assurance/scorecards").json()["scorecards"]) == 9
    health = _client.get("/api/v1/assurance/health-score").json()
    assert len(health["no_scale_conditions"]) == 7
    assert len(_client.get("/api/v1/assurance/funnel").json()["rungs"]) == 10
    assert len(_client.get("/api/v1/assurance/weekly-review").json()
               ["answered_questions"]) == 12
    assert "revenue" in _client.get("/api/v1/assurance/board-pack").json()["sections"]
