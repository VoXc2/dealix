"""AI Opportunity Report — founder-led enterprise sales engine.

End-to-end: target company -> AI Opportunity Report -> enterprise proposal,
all governance-gated. Deterministic, no LLM.
"""
from __future__ import annotations

import re

from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.diagnostic_engine import generate_opportunity_report
from auto_client_acquisition.service_catalog import get_enterprise_offering

client = TestClient(app)

_GUARANTEE = re.compile(r"نضمن|\bguarantee[ds]?\b", re.IGNORECASE)


def test_report_has_five_opportunities() -> None:
    report = generate_opportunity_report(company="شركة الواحة", sector="real_estate")
    assert len(report.opportunities) == 5
    assert report.approval_status == "approval_required"
    assert report.is_estimate is True
    for opp in report.opportunities:
        assert opp.title_ar.strip() and opp.title_en.strip()
        assert opp.mapped_program_id


def test_report_markdown_is_bilingual_and_clean() -> None:
    report = generate_opportunity_report(company="ACME", sector="b2b_services")
    md = report.markdown_ar_en
    assert "AI Opportunity Report" in md
    assert "القراءة السريعة" in md
    assert "Executive summary" in md
    # Article 8 — no guaranteed-outcome language anywhere in the report.
    assert _GUARANTEE.search(md) is None, "report must not promise guaranteed outcomes"


def test_recommended_program_is_a_real_enterprise_offering() -> None:
    for sector in ("real_estate", "b2b_services", "training_consulting",
                    "healthcare_clinic", "unknown_sector"):
        report = generate_opportunity_report(company="Co", sector=sector)
        offering = get_enterprise_offering(report.recommended_program_id)
        assert offering is not None, f"{sector} -> bad program {report.recommended_program_id}"
        tier_ids = {t.id for t in offering.tiers}
        assert report.recommended_tier_id in tier_ids


def test_opportunity_report_endpoint() -> None:
    resp = client.post(
        "/api/v1/diagnostic/opportunity-report",
        json={"company": "Madar Logistics", "sector": "real_estate"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert len(body["opportunities"]) == 5
    assert body["recommended_program_id"]
    assert body["approval_status"] == "approval_required"


def test_opportunity_report_pdf_endpoint_returns_a_document() -> None:
    resp = client.post(
        "/api/v1/diagnostic/opportunity-report/pdf",
        json={"company": "Madar Logistics", "sector": "b2b_services"},
    )
    assert resp.status_code == 200, resp.text
    # PDF when an engine is installed, else markdown fallback — both are 200.
    assert resp.headers["content-type"].split(";")[0] in (
        "application/pdf",
        "text/markdown",
    )


def test_founder_enterprise_path_end_to_end() -> None:
    """Company -> AI Opportunity Report -> tiered enterprise proposal."""
    report_resp = client.post(
        "/api/v1/diagnostic/opportunity-report",
        json={"company": "Tameer Co", "sector": "real_estate"},
    )
    assert report_resp.status_code == 200
    report = report_resp.json()

    proposal_resp = client.post(
        "/api/v1/service-setup/enterprise-proposal/tameer",
        json={
            "customer_name": "Tameer Co",
            "customer_handle": "tameer",
            "sector": "real_estate",
            "city": "Jeddah",
            "engagement_id": "ENG-E2E",
            "offering_id": report["recommended_program_id"],
            "recommended_tier_id": report["recommended_tier_id"],
        },
    )
    assert proposal_resp.status_code == 200, proposal_resp.text
    proposal = proposal_resp.json()
    assert proposal["governance_decision"] == "allow_with_review"
    assert len(proposal["tiers"]) == 3
    assert proposal["is_estimate"] is True
