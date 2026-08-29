from __future__ import annotations

from dealix.commercial.company_brain_sprint import (
    BrainSource,
    CompanyBrainSprintPlanner,
    CompanyBrainSprintRequest,
    WorkflowCandidate,
)
from dealix.commercial.portfolio_router import (
    DemandSignal,
    EntryPackage,
    PortfolioPackageRouter,
)


def test_technical_demand_routes_to_company_brain_without_authority() -> None:
    decision = PortfolioPackageRouter().route(
        DemandSignal(
            signal_id="sig-1",
            company_name="Acme",
            observed_at="2026-08-29T09:00:00+00:00",
            source_ref="form://request/1",
            explicit_inbound_ref="inbound://1",
            consent_state="CONSENTED",
            problem_statement="We need a governed company brain and workflow automation.",
            requested_capabilities=["company_brain", "automation"],
        )
    )
    assert decision.recommended_package == EntryPackage.COMPANY_BRAIN
    assert decision.relationship_state == "VERIFIED_RELATIONSHIP"
    assert decision.next_action == "RUN_COMPANY_BRAIN_SPRINT_ASSESSMENT"
    assert all(value is False for value in decision.authority.values())


def test_research_without_evidence_never_becomes_lead_or_offer() -> None:
    decision = PortfolioPackageRouter().route(
        DemandSignal(
            signal_id="sig-2",
            company_name="Research Target",
            observed_at="2026-08-29T09:00:00+00:00",
            problem_tags=["revenue"],
        )
    )
    assert decision.recommended_package == EntryPackage.RESEARCH_NURTURE_SUPPRESS
    assert decision.relationship_state == "UNKNOWN_NOT_EVIDENCE_BACKED"
    assert decision.authority["offer"] is False
    assert decision.authority["external_send"] is False


def test_suppression_overrides_package_interest() -> None:
    decision = PortfolioPackageRouter().route(
        DemandSignal(
            signal_id="sig-3",
            company_name="Suppressed Co",
            observed_at="2026-08-29T09:00:00+00:00",
            source_ref="crm://1",
            real_interaction_ref="meeting://1",
            consent_state="OPTED_OUT",
            partner_intent=True,
        )
    )
    assert decision.recommended_package == EntryPackage.RESEARCH_NURTURE_SUPPRESS
    assert decision.owner == "governance"


def test_company_brain_sprint_blocks_scope_until_evidence_complete() -> None:
    assessment = CompanyBrainSprintPlanner().assess(
        CompanyBrainSprintRequest(account_id="acct-1", company_name="Acme")
    )
    assert assessment.status == "EVIDENCE_GAPS_BLOCK_SCOPE"
    assert assessment.selected_workflow == "UNKNOWN_NOT_EVIDENCE_BACKED"
    assert assessment.authority["deployment"] is False
    assert assessment.missing_evidence


def test_company_brain_sprint_ready_still_grants_no_quote_or_deploy() -> None:
    request = CompanyBrainSprintRequest(
        account_id="acct-1",
        company_name="Acme",
        relationship_ref="relationship://1",
        discovery_ref="discovery://1",
        authority_audit_ref="authority://1",
        data_boundary_ref="boundary://1",
        customer_validation_ref="customer://validation/1",
        sources=[
            BrainSource(
                source_id="crm",
                source_ref="crm://tenant/1",
                owner="sales_ops",
                freshness_or_expiry="2026-09-29T00:00:00+00:00",
                permission_ref="permission://crm/1",
                provenance="customer_connected_crm",
            )
        ],
        workflow_candidates=[
            WorkflowCandidate(
                workflow_id="wf-1",
                name="Revenue follow-up prioritization",
                outcome_hypothesis="Reduce unowned qualified follow-ups.",
                baseline_ref="baseline://1",
                evidence_refs=["evidence://1"],
                accountable_owner="sales_ops",
                approval_path_ref="approval://1",
                acceptance_criteria_ref="acceptance://1",
            )
        ],
        selected_workflow_id="wf-1",
    )
    assessment = CompanyBrainSprintPlanner().assess(request)
    assert assessment.status == "READY_FOR_CUSTOMER_SPECIFIC_SCOPE_REVIEW"
    assert assessment.next_action == "PREPARE_CUSTOMER_SPECIFIC_SCOPE_FOR_APPROVAL"
    assert assessment.gates["single_workflow_selected"] is True
    assert all(value is False for value in assessment.authority.values())


def test_routing_and_assessment_are_deterministic() -> None:
    signal = DemandSignal(
        signal_id="sig-4",
        company_name="Acme",
        observed_at="2026-08-29T09:00:00+00:00",
        explicit_inbound_ref="inbound://4",
        problem_tags=["sales"],
    )
    router = PortfolioPackageRouter()
    assert router.route(signal).decision_id == router.route(signal).decision_id
