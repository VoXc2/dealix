"""Tests for Lead Intelligence Sprint runner."""

from __future__ import annotations

from auto_client_acquisition.commercial_engagements.lead_intelligence_sprint import (
    run_lead_intelligence_sprint,
    score_lead_row,
)
from auto_client_acquisition.commercial_engagements.schemas import LeadIntelligenceSprintInput
from auto_client_acquisition.governance_os.draft_gate import audit_draft_text


def test_score_lead_row_weights() -> None:
    base = {"company_name": "A", "sector": "tech", "city": "Riyadh"}
    s0 = score_lead_row(base, sector_weight=0.1, city_weight=0.1)
    s1 = score_lead_row({**base, "phone": "+966501234567", "email": "a@x.sa"}, sector_weight=0.1, city_weight=0.1)
    assert s1 >= s0


def test_lead_intelligence_sprint_keys_and_sorting() -> None:
    rows = [
        {"company": "Alpha", "sector": "x", "city": "c"},
        {"company_name": "Beta", "sector": "y", "city": "d", "phone": "0500000000"},
    ]
    rep = run_lead_intelligence_sprint(LeadIntelligenceSprintInput(accounts=rows, top_n=10))
    d = rep.model_dump()
    assert "data_quality" in d and d["data_quality"]["row_count"] == 2
    ranked = d["accounts_ranked"]
    scores = [r["score"] for r in ranked]
    assert scores == sorted(scores, reverse=True)
    assert isinstance(d["action_plan"], list) and len(d["action_plan"]) >= 3
    assert d.get("dedupe_hints")
    assert d.get("proof_pack_suggestions")
    assert "lead_intake" in d["proof_pack_suggestions"]
    for audit in d["draft_audits"]:
        blob = (audit.get("sample_draft") or "").lower()
        for bad in ("scraping", "cold whatsapp", "linkedin automation", "purchased list"):
            assert bad not in blob
        assert audit.get("issues") == []


def test_audit_flags_forbidden_draft() -> None:
    issues = audit_draft_text("We will use scraping for leads")
    assert any("forbidden_term" in i for i in issues)
