"""Sprint orchestrator — 10-step end-to-end run on synthetic data."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.delivery_factory.delivery_sprint import (
    run_sprint,
    step1_kickoff,
    step2_data_quality,
    step3_account_scoring,
    step5_governance_review,
)


_DEMO_CSV = (
    "company_name,sector,city,relationship_status,last_interaction,notes\n"
    "شركة الواحة,b2b_services,Riyadh,warm,2026-04-12,clean fit\n"
    "Madar Logistics,logistics,Jeddah,warm,2026-04-22,past pilot\n"
    "NorthStar,healthcare,Riyadh,warm,2026-04-05,pii heavy\n"
    "Rawabi,real_estate,Riyadh,cold,2026-02-18,stale\n"
)

_GOOD_PASSPORT = {
    "source_id": "SRC-DEMO-1",
    "source_type": "client_upload",
    "owner": "client",
    "allowed_use": ("internal_analysis", "scoring"),
    "contains_pii": False,
    "sensitivity": "low",
    "ai_access_allowed": True,
    "external_use_allowed": False,
    "retention_policy": "project_duration",
}

client = TestClient(app)


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "fr.jsonl"))
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "val.jsonl"))
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "cap.jsonl"))
    monkeypatch.setenv("DEALIX_AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    yield


def test_step1_kickoff_no_passport_returns_invalid():
    out = step1_kickoff(customer_id="x", engagement_id="e1", source_passport=None)
    assert out["passport_provided"] is False


def test_step1_kickoff_valid_passport():
    out = step1_kickoff(customer_id="x", engagement_id="e1", source_passport=_GOOD_PASSPORT)
    assert out["passport_provided"] is True
    assert out["validation"]["is_valid"] is True


def test_step2_data_quality_handles_empty():
    out = step2_data_quality(customer_id="x", engagement_id="e1")
    assert out["row_count"] == 0


def test_step2_data_quality_on_csv():
    out = step2_data_quality(customer_id="x", engagement_id="e1", raw_csv=_DEMO_CSV)
    assert out["row_count"] == 4
    assert out["dq_overall"] > 0


def test_step3_ranks_accounts():
    accounts = [
        {"company_name": "A", "sector": "b2b_services", "city": "Riyadh", "relationship_status": "warm", "last_interaction": "2026-05", "notes": "good"},
        {"company_name": "B", "sector": "logistics", "city": "Jeddah", "relationship_status": "cold"},
        {"company_name": "C"},
    ]
    out = step3_account_scoring(customer_id="x", engagement_id="e1", accounts=accounts)
    top = out["top_10"]
    assert len(top) == 3
    assert top[0]["company_name"] == "A"
    assert top[0]["score"] > top[1]["score"]


def test_step5_governance_review_blocks_unsafe():
    drafts = [
        {"account": "A", "outline_ar": "نص آمن", "outline_en": "safe note"},
        {"account": "B", "outline_ar": "نضمن مبيعات 100%", "outline_en": "we guarantee 100% sales"},
    ]
    out = step5_governance_review(customer_id="x", engagement_id="e1", drafts=drafts)
    decisions = {r["decision"] for r in out["reviews"]}
    # At least the unsafe one is REDACT or BLOCK
    assert any(d in {"redact", "block"} for d in decisions)


def test_run_sprint_end_to_end_produces_proof_pack():
    run = run_sprint(
        engagement_id="eng_t1",
        customer_id="cust_t1",
        source_passport=_GOOD_PASSPORT,
        raw_csv=_DEMO_CSV,
        accounts=[
            {"company_name": "Co1", "sector": "b2b_services", "city": "Riyadh",
             "relationship_status": "warm", "last_interaction": "2026-05",
             "notes": "fit"},
            {"company_name": "Co2", "sector": "logistics", "city": "Jeddah",
             "relationship_status": "cold"},
        ],
        problem_summary="rank Saudi B2B accounts",
    )
    assert run.proof_pack is not None
    assert run.proof_score >= 0  # Pack assembles even with thin data
    assert len(run.steps) == 8
    assert len(run.capital_assets_registered) >= 1
    assert run.governance_decision in {"allow", "allow_with_review", "needs_review"}


def test_sprint_run_endpoint_returns_full_run():
    resp = client.post(
        "/api/v1/sprint/run",
        json={
            "engagement_id": "eng_router_1",
            "customer_id": "cust_router_1",
            "source_passport": dict(
                _GOOD_PASSPORT,
                allowed_use=list(_GOOD_PASSPORT["allowed_use"]),
            ),
            "raw_csv": _DEMO_CSV,
            "accounts": [
                {"company_name": "Co1", "sector": "b2b_services", "city": "Riyadh",
                 "relationship_status": "warm"},
            ],
            "problem_summary": "demo",
        },
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["engagement_id"] == "eng_router_1"
    assert "proof_pack" in body
    assert isinstance(body["steps"], list)
    assert len(body["steps"]) == 8


def test_sprint_sample_endpoint():
    resp = client.get("/api/v1/sprint/sample")
    assert resp.status_code == 200
    body = resp.json()
    assert body["customer_id"] == "dealix_internal_demo"
    assert body["proof_pack"] is not None
