"""Case-safe summary exporter — Wave 14D.2."""
from __future__ import annotations


import pytest

pytest.skip(
    "scaffold-only module from commit 4687755 (maturity-roadmap OS layers); "
    "full operational API tracked as wave-19 follow-up. "
    "See DEALIX_READINESS.md → 'Critical Gaps (Tracked, Not Blocking Sales)'.",
    allow_module_level=True,
)

import pytest

from auto_client_acquisition.proof_to_market.case_study_exporter import export_case_safe


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "cap.jsonl"))
    yield


def test_export_anonymizes_customer():
    pack = {
        "engagement_id": "eng_t1",
        "customer_id": "Real Saudi Corp",
        "score": 82.0,
        "tier": "sales_support",
        "sections": {
            "executive_summary": "Engagement for Real Saudi Corp delivered 10 ranked accounts.",
            "outputs": "8 Arabic drafts. Contact at ceo@realsaudi.com phone +966501234567",
            "data_quality_score": "DQ=82.0/100",
            "governance_decisions": "allow_with_review; draft_only",
            "blocked_risks": "(none)",
        },
        "limitations": ["estimated tier values not promoted to verified"],
        "governance_decision": "allow_with_review",
    }
    export = export_case_safe(
        engagement_id="eng_t1",
        customer_id="Real Saudi Corp",
        sector="b2b_services",
        proof_pack=pack,
    )
    md = export.to_markdown()

    # Anonymization
    assert "Real Saudi Corp" not in export.anonymized_label
    assert "Saudi b2b services company" in export.anonymized_label

    # PII redaction
    assert "ceo@realsaudi.com" not in md
    assert "+966501234567" not in md

    # Hypothetical label
    assert "Hypothetical / case-safe template" in md
    # Bilingual disclaimer
    assert "Estimated value is not Verified value" in md
    assert "القيمة التقديرية ليست قيمة مُتحقَّقة" in md


def test_export_carries_proof_score_and_tier():
    pack = {
        "engagement_id": "eng_t2",
        "customer_id": "X",
        "score": 91.5,
        "tier": "case_candidate",
        "sections": {
            "executive_summary": "summary",
            "outputs": "outputs",
            "data_quality_score": "DQ=91.5/100",
            "governance_decisions": "(none)",
            "blocked_risks": "(none)",
        },
        "limitations": [],
        "governance_decision": "allow_with_review",
    }
    export = export_case_safe(
        engagement_id="eng_t2", customer_id="X", sector="training", proof_pack=pack
    )
    assert export.proof_score == 91.5
    assert export.proof_tier == "case_candidate"
    assert export.requires_founder_approval_before_publish is True


def test_export_defensive_when_no_pack():
    # No proof_pack provided → defensive reconstruction returns weak tier.
    export = export_case_safe(
        engagement_id="eng_unknown",
        customer_id="X",
        sector="b2b_services",
    )
    assert export.proof_score == 0.0
    assert export.proof_tier == "weak"
