"""Tests for responsible_ai_os — D-RAIOS contracts."""

from __future__ import annotations

from auto_client_acquisition.responsible_ai_os.ai_inventory import AIInventoryRow, ai_inventory_row_complete
from auto_client_acquisition.responsible_ai_os.compliance_to_product import product_artifact_for_need
from auto_client_acquisition.responsible_ai_os.literacy_modules import (
    LITERACY_MODULE_IDS,
    literacy_modules_complete,
)
from auto_client_acquisition.responsible_ai_os.responsible_ai_score import (
    ResponsibleAIDimensions,
    responsible_ai_deployment_band,
    responsible_ai_score,
)
from auto_client_acquisition.responsible_ai_os.trust_pack import TRUST_PACK_SECTIONS, trust_pack_sections_complete
from auto_client_acquisition.responsible_ai_os.use_case_risk_classifier import (
    RiskLevel,
    UseCaseCard,
    classify_operational_risk,
    forbidden_use_case_reasons,
    high_risk_requires_governance_review,
    use_case_card_consistent,
)


def test_forbidden_use_case_reasons() -> None:
    r = forbidden_use_case_reasons(
        requests_scraping_system=True,
        requests_cold_whatsapp_automation=True,
        requests_linkedin_automation=False,
        requests_guaranteed_sales_claims=False,
        sourceless_decisioning=False,
    )
    assert "forbidden_scraping_system" in r
    assert "forbidden_cold_whatsapp_automation" in r


def test_classify_operational_risk_low_internal() -> None:
    assert (
        classify_operational_risk(
            external_outreach=False,
            financial_or_compliance_decision=False,
            sensitive_personal_data=False,
            automated_workflow_high_impact=False,
            customer_facing_draft=False,
            pii_in_analysis=False,
            internal_summarization_non_sensitive=True,
        )
        == RiskLevel.LOW
    )


def test_classify_operational_risk_high_external() -> None:
    assert (
        classify_operational_risk(
            external_outreach=True,
            financial_or_compliance_decision=False,
            sensitive_personal_data=False,
            automated_workflow_high_impact=False,
            customer_facing_draft=False,
            pii_in_analysis=False,
            internal_summarization_non_sensitive=False,
        )
        == RiskLevel.HIGH
    )


def test_high_risk_requires_governance_review() -> None:
    assert high_risk_requires_governance_review(RiskLevel.HIGH) is True
    assert high_risk_requires_governance_review(RiskLevel.MEDIUM) is False


def test_use_case_card_consistency() -> None:
    bad = UseCaseCard(
        use_case_id="UC-1",
        name="x",
        department="Sales",
        data_sources=(),
        contains_pii=False,
        risk_level=RiskLevel.LOW,
        human_oversight="required",
        external_action_allowed=True,
        governance_decision="DRAFT_ONLY",
        proof_metric="m",
    )
    ok, errors = use_case_card_consistent(bad)
    assert not ok
    assert "data_sources_required" in errors
    assert "external_action_not_low_risk" in errors


def test_responsible_ai_score_and_band() -> None:
    dims = ResponsibleAIDimensions(
        source_clarity=90,
        data_sensitivity_handling=80,
        human_oversight=85,
        governance_decision_coverage=80,
        auditability=75,
        proof_of_value=82,
        incident_readiness=70,
    )
    s = responsible_ai_score(dims)
    assert 70 <= s <= 100
    assert responsible_ai_deployment_band(90) == "responsible_ai_ready"
    assert responsible_ai_deployment_band(75) == "ready_with_controls"
    assert responsible_ai_deployment_band(60) == "governance_review_required"
    assert responsible_ai_deployment_band(40) == "do_not_deploy"


def test_trust_pack_contract() -> None:
    ok, missing = trust_pack_sections_complete({})
    assert not ok
    assert set(missing) == set(TRUST_PACK_SECTIONS)


def test_literacy_modules_contract() -> None:
    ok, missing = literacy_modules_complete(frozenset({"ai_for_executives"}))
    assert not ok
    assert "ai_for_sales_operators" in missing
    assert len(LITERACY_MODULE_IDS) == 6


def test_compliance_to_product_map() -> None:
    assert product_artifact_for_need("source_clarity") == "source_passport_panel"
    assert product_artifact_for_need("unknown") is None


def test_ai_inventory_complete() -> None:
    row = AIInventoryRow(
        use_case_id="UC-1",
        department="Sales",
        owner="",
        data_source_ids=("SRC-1",),
        agent_or_model="AGT-1",
        risk_level="medium",
        approval_path="approval_center",
        audit_status="ok",
        proof_metric="accounts_scored",
        status="active",
    )
    ok, missing = ai_inventory_row_complete(row)
    assert not ok
    assert "owner" in missing
