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


def _ready_company_brain_request() -> CompanyBrainSprintRequest:
    return CompanyBrainSprintRequest(
        account_id="acct-1",
        company_name="Acme",
        relationship_ref="relationship://1",
        discovery_ref="discovery://1",
        authority_audit_ref="authority://1",
        data_boundary_ref="boundary://1",
        customer_validation_ref="customer://validation/1",
        business_objective="Reduce unowned qualified follow-ups.",
        named_problem="Qualified follow-ups are not consistently owned.",
        current_workflow="CRM task queue reviewed manually each morning.",
        current_manual_steps=["export queue", "review owners", "assign follow-up"],
        desired_outcome="Every qualified follow-up has an accountable owner and next action.",
        proof_method="Compare baseline and 30-day evidence receipts for ownership coverage.",
        risk_and_regulatory_class="STANDARD",
        integration_constraints=["read-only CRM during assessment"],
        sources=[
            BrainSource(
                source_id="crm",
                source_ref="crm://tenant/1",
                owner="sales_ops",
                freshness_or_expiry="2026-09-29T00:00:00+00:00",
                permission_ref="permission://crm/1",
                provenance="customer_connected_crm",
                source_type="CRM",
                system_owner="sales_ops",
                tenant_scope="tenant://acme",
                purpose="Prioritize qualified follow-up work.",
                authority_or_lawful_basis="permission://crm/1",
                access_class="READ_ONLY",
                freshness_sla="PT1H",
                last_verified_at="2026-08-29T09:00:00+00:00",
                provenance_ref="crm://tenant/1/schema-v1",
                retention_or_expiry="2026-09-29T00:00:00+00:00",
                allowed_claims=["workflow state observed from approved CRM fields"],
                prohibited_uses=["external send", "unapproved enrichment"],
                pii_or_sensitive_class_if_any="BUSINESS_CONTACT_DATA",
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
                trigger="scheduled internal queue review",
                input_contract="approved CRM opportunity/task fields only",
                deterministic_steps=["load approved fields", "dedupe", "rank by policy"],
                ai_reasoning_steps_if_needed=[],
                tool_allowlist=["crm_read_only"],
                authority_class="INTERNAL_PREPARATION_ONLY",
                approval_points=["any external follow-up"],
                output_contract="ranked internal follow-up queue with source refs",
                evidence_receipt="receipt://schema/followup-priority-v1",
                idempotency_key="account_id+snapshot_id+policy_version",
                retry_policy="bounded retry for transient read failures",
                rollback_or_safe_failure="fail closed to prior verified snapshot",
                human_handoff="route ambiguous account ownership to sales_ops",
                evaluation_cases=["known owner", "missing owner", "suppressed contact"],
            )
        ],
        selected_workflow_id="wf-1",
    )


def test_company_brain_sprint_ready_still_grants_no_quote_or_deploy() -> None:
    assessment = CompanyBrainSprintPlanner().assess(_ready_company_brain_request())
    assert assessment.status == "READY_FOR_CUSTOMER_SPECIFIC_SCOPE_REVIEW"
    assert assessment.next_action == "PREPARE_CUSTOMER_SPECIFIC_SCOPE_FOR_APPROVAL"
    assert assessment.gates["single_workflow_selected"] is True
    assert assessment.gates["source_registry_contract_complete"] is True
    assert assessment.gates["bounded_workflow_contract_complete"] is True
    assert assessment.gates["customer_validation_reference_present"] is True
    assert assessment.gates["customer_validation_verified"] is False
    assert assessment.customer_validation_state == "REFERENCE_PRESENT_NOT_CUSTOMER_VALUE_PROOF"
    assert assessment.source_registry_gaps == []
    assert assessment.workflow_contract_gaps == []
    assert all(value is False for value in assessment.authority.values())


def test_legacy_minimal_source_fields_do_not_satisfy_current_source_registry() -> None:
    request = _ready_company_brain_request().model_copy(
        update={
            "sources": [
                BrainSource(
                    source_id="crm",
                    source_ref="crm://tenant/1",
                    owner="sales_ops",
                    freshness_or_expiry="2026-09-29T00:00:00+00:00",
                    permission_ref="permission://crm/1",
                    provenance="customer_connected_crm",
                )
            ]
        }
    )
    assessment = CompanyBrainSprintPlanner().assess(request)
    assert assessment.status == "EVIDENCE_GAPS_BLOCK_SCOPE"
    assert "source:crm:tenant_scope" in assessment.source_registry_gaps
    assert "source:crm:freshness_sla" in assessment.source_registry_gaps
    assert "source:crm:last_verified_at" in assessment.source_registry_gaps
    assert "source:crm:allowed_claims" in assessment.source_registry_gaps
    assert assessment.gates["source_registry_contract_complete"] is False


def test_legacy_minimal_workflow_fields_do_not_satisfy_bounded_workflow_contract() -> None:
    request = _ready_company_brain_request().model_copy(
        update={
            "workflow_candidates": [
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
            ]
        }
    )
    assessment = CompanyBrainSprintPlanner().assess(request)
    assert assessment.status == "EVIDENCE_GAPS_BLOCK_SCOPE"
    assert "workflow:wf-1:tool_allowlist" in assessment.workflow_contract_gaps
    assert "workflow:wf-1:idempotency_key" in assessment.workflow_contract_gaps
    assert "workflow:wf-1:rollback_or_safe_failure" in assessment.workflow_contract_gaps
    assert assessment.gates["bounded_workflow_contract_complete"] is False


def test_source_registry_is_canonical_and_unknowns_are_not_invented() -> None:
    assessment = CompanyBrainSprintPlanner().assess(_ready_company_brain_request())
    source = assessment.source_registry[0]
    assert source["source_type"] == "CRM"
    assert source["tenant_scope"] == "tenant://acme"
    assert source["access_class"] == "READ_ONLY"
    assert source["last_verified_at"] == "2026-08-29T09:00:00+00:00"
    assert source["allowed_claims"] == ["workflow state observed from approved CRM fields"]
    assert "external send" in source["prohibited_uses"]


def test_customer_validation_reference_never_grants_customer_value_or_public_proof() -> None:
    assessment = CompanyBrainSprintPlanner().assess(_ready_company_brain_request())
    assert assessment.customer_validation_state == "REFERENCE_PRESENT_NOT_CUSTOMER_VALUE_PROOF"
    assert assessment.authority["customer_value_claim"] is False
    assert assessment.authority["public_customer_proof"] is False


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

    planner = CompanyBrainSprintPlanner()
    request = _ready_company_brain_request()
    assert planner.assess(request).assessment_id == planner.assess(request).assessment_id
