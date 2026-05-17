"""AI & Revenue Ops Risk Score — scorer + endpoint tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.sales_os.risk_score import (
    _RISK_WEIGHTS,
    RiskLevel,
    score_risk,
)

client = TestClient(app)

_ALL_GOOD = dict(
    has_crm=True,
    uses_ai_in_sales_or_ops=False,
    approval_before_external_messages=True,
    can_link_ai_to_financial_outcome=True,
    followup_documented=True,
    knows_source_of_every_decision=True,
    has_ai_evidence_pack=True,
)


def test_risk_weights_sum_to_100():
    assert sum(_RISK_WEIGHTS.values()) == 100


def test_all_good_answers_score_zero_low():
    r = score_risk(**_ALL_GOOD)
    assert r.score == 0
    assert r.risk_level == RiskLevel.LOW.value
    assert r.risk_signals == []
    assert r.recommended_next_step
    assert r.recommended_offer == "governed_diagnostic_starter_4999"


def test_all_gaps_score_100_high():
    r = score_risk(
        has_crm=False,
        uses_ai_in_sales_or_ops=True,
        approval_before_external_messages=False,
        can_link_ai_to_financial_outcome=False,
        followup_documented=False,
        knows_source_of_every_decision=False,
        has_ai_evidence_pack=False,
    )
    assert r.score == 100
    assert r.risk_level == RiskLevel.HIGH.value
    assert len(r.risk_signals) == 7


def test_medium_band_at_threshold():
    # no_approval_boundary (22) + uses_ai (8) = 30 → Medium boundary.
    r = score_risk(
        has_crm=True,
        uses_ai_in_sales_or_ops=True,
        approval_before_external_messages=False,
        can_link_ai_to_financial_outcome=True,
        followup_documented=True,
        knows_source_of_every_decision=True,
        has_ai_evidence_pack=True,
    )
    assert r.score == 30
    assert r.risk_level == RiskLevel.MEDIUM.value


def test_low_band_below_threshold():
    # no_crm (12) + followup_undocumented (12) = 24 → still Low.
    r = score_risk(
        has_crm=False,
        uses_ai_in_sales_or_ops=False,
        approval_before_external_messages=True,
        can_link_ai_to_financial_outcome=True,
        followup_documented=False,
        knows_source_of_every_decision=True,
        has_ai_evidence_pack=True,
    )
    assert r.score == 24
    assert r.risk_level == RiskLevel.LOW.value


def test_doctrine_trigger_forces_high():
    # All-good answers, but the context asks for scraping → forced High.
    r = score_risk(**_ALL_GOOD, context_text="we want to scrape linkedin contacts")
    assert r.risk_level == RiskLevel.HIGH.value
    assert "scraping" in r.doctrine_flags
    assert r.score == 0  # questionnaire score is unchanged; the band is escalated


def test_endpoint_rejects_missing_consent():
    resp = client.post("/api/v1/revenue-machine/risk-score", json={"consent": False})
    assert resp.status_code == 400
    assert "consent_required" in resp.json()["detail"]


def test_endpoint_returns_band_and_proof_event():
    resp = client.post(
        "/api/v1/revenue-machine/risk-score",
        json={"consent": True, **_ALL_GOOD},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["result"]["risk_level"] == RiskLevel.LOW.value
    assert body["proof_event_id"].startswith("evt_")
    assert body["governance_decision"] == "allow"


def test_endpoint_rejects_unknown_field():
    resp = client.post(
        "/api/v1/revenue-machine/risk-score",
        json={"consent": True, "rogue_field": 1},
    )
    assert resp.status_code == 422


def test_diagnostic_offer_lists_three_tiers():
    resp = client.get("/api/v1/revenue-machine/diagnostic-offer")
    assert resp.status_code == 200
    tiers = resp.json()["tiers"]
    assert [t["service_id"] for t in tiers] == [
        "governed_diagnostic_starter_4999",
        "governed_diagnostic_standard_9999",
        "governed_diagnostic_executive_15000",
    ]
    assert [t["price_sar"] for t in tiers] == [4999.0, 9999.0, 15000.0]
