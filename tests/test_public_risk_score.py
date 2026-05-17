"""Public Diagnostic Funnel — risk-score endpoint contract + doctrine guards.

Covers the anti-fabrication rule (empty input never yields a score), the
fit buckets, the doctrine block path, governance-status presence, the
consent-gated sample Proof Pack, and the unauthenticated public-prefix path.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture(autouse=True)
def _isolated_lead_inbox(tmp_path, monkeypatch) -> None:
    """Point the lead inbox at a throwaway file so tests never pollute var/."""
    monkeypatch.setenv("DEALIX_LEAD_INBOX_PATH", str(tmp_path / "leads.jsonl"))


def _client() -> TestClient:
    return TestClient(app)


_STRONG_FORM = {
    "name": "Sami",
    "company": "Acme Co",
    "email": "sami@acme.com",
    "role": "founder",
    "sector": "logistics",
    "crm": "yes",
    "biggest_pain": "pipeline",
    "consent_before_external_action": "yes",
    "can_link_workflow_to_value": "yes",
    "budget_range": "5000_25000",
    "urgency": "high",
    "consent": True,
}


def test_risk_score_empty_input_no_fabrication() -> None:
    """Empty input must be rejected — and must NOT produce a synthesized score."""
    r = _client().post("/api/v1/public/risk-score", json={})
    assert r.status_code == 422
    body = r.json()
    assert "fit_score" not in body
    assert "bucket" not in body


def test_risk_score_missing_email_rejected() -> None:
    r = _client().post(
        "/api/v1/public/risk-score",
        json={"name": "A", "company": "B"},
    )
    assert r.status_code == 422


def test_risk_score_high_bucket() -> None:
    r = _client().post("/api/v1/public/risk-score", json=_STRONG_FORM)
    assert r.status_code == 200
    body = r.json()
    assert body["bucket"] == "high"
    assert body["fit_score"] >= 70
    assert body["governance_decision"] == "allow"
    assert body["next_step"] == "book_diagnostic_review"


def test_risk_score_low_bucket() -> None:
    r = _client().post(
        "/api/v1/public/risk-score",
        json={"name": "A", "company": "B", "email": "a@b.com"},
    )
    assert r.status_code == 200
    assert r.json()["bucket"] == "low"


def test_risk_score_medium_bucket() -> None:
    form = {
        "name": "A",
        "company": "B",
        "email": "a@b.com",
        "crm": "yes",
        "biggest_pain": "crm",
        "consent_before_external_action": "yes",
    }
    body = _client().post("/api/v1/public/risk-score", json=form).json()
    assert body["bucket"] == "medium"
    assert 45 <= body["fit_score"] < 70


def test_risk_score_doctrine_violation_blocks() -> None:
    """Free text asking for guaranteed sales must force a blocked verdict."""
    form = {**_STRONG_FORM, "notes": "we want guaranteed sales results fast"}
    body = _client().post("/api/v1/public/risk-score", json=form).json()
    assert body["bucket"] == "blocked"
    assert body["governance_decision"] == "blocked"
    assert body["doctrine_violations"]


def test_risk_score_carries_governance_status() -> None:
    body = _client().post("/api/v1/public/risk-score", json=_STRONG_FORM).json()
    assert "governance_decision" in body


def test_risk_score_proof_pack_consent_gated() -> None:
    """Without consent the sample Proof Pack is not offered."""
    form = {k: v for k, v in _STRONG_FORM.items() if k != "consent"}
    body = _client().post("/api/v1/public/risk-score", json=form).json()
    assert body["sample_proof_pack"]["available"] is False
    assert body["sample_proof_pack"]["reason"] == "consent_required"


def test_risk_score_proof_pack_available_with_consent() -> None:
    body = _client().post("/api/v1/public/risk-score", json=_STRONG_FORM).json()
    assert body["sample_proof_pack"]["available"] is True


def test_risk_score_public_path_no_api_key() -> None:
    """The /api/v1/public/ prefix is exempt from API-key auth — no 401."""
    r = _client().post("/api/v1/public/risk-score", json=_STRONG_FORM)
    assert r.status_code != 401


def test_risk_score_honeypot_silently_accepts() -> None:
    r = _client().post(
        "/api/v1/public/risk-score",
        json={**_STRONG_FORM, "website": "http://spam.example"},
    )
    assert r.status_code == 200
    assert "fit_score" not in r.json()
