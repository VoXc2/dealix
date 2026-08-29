#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from dealix.commercial.company_brain_sprint import (
    BrainSource,
    CompanyBrainSprintPlanner,
    CompanyBrainSprintRequest,
    WorkflowCandidate,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/commercial/company_brain_sprint_assessment_v1.json"


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def _ready_request() -> CompanyBrainSprintRequest:
    return CompanyBrainSprintRequest(
        account_id="verify-account",
        company_name="Verifier Co",
        relationship_ref="relationship://verify/1",
        discovery_ref="discovery://verify/1",
        authority_audit_ref="authority://verify/1",
        data_boundary_ref="boundary://verify/1",
        customer_validation_ref="customer://validation/verify/1",
        business_objective="Reduce unowned qualified follow-ups.",
        named_problem="Qualified follow-ups lack consistent ownership.",
        current_workflow="CRM queue is manually reviewed.",
        current_manual_steps=["review queue", "assign owner"],
        desired_outcome="Every qualified follow-up has one owner and next action.",
        proof_method="Compare source-bound baseline and 30-day receipts.",
        risk_and_regulatory_class="STANDARD",
        integration_constraints=["read-only CRM during assessment"],
        sources=[
            BrainSource(
                source_id="crm",
                source_ref="crm://tenant/verify",
                owner="sales_ops",
                freshness_or_expiry="2026-09-29T00:00:00+00:00",
                permission_ref="permission://crm/verify",
                provenance="customer_connected_crm",
                source_type="CRM",
                system_owner="sales_ops",
                tenant_scope="tenant://verify",
                purpose="Internal follow-up prioritization.",
                authority_or_lawful_basis="permission://crm/verify",
                access_class="READ_ONLY",
                freshness_sla="PT1H",
                last_verified_at="2026-08-29T09:00:00+00:00",
                provenance_ref="crm://tenant/verify/schema-v1",
                retention_or_expiry="2026-09-29T00:00:00+00:00",
                allowed_claims=["approved CRM workflow state"],
                prohibited_uses=["external send", "unapproved enrichment"],
                pii_or_sensitive_class_if_any="BUSINESS_CONTACT_DATA",
            )
        ],
        workflow_candidates=[
            WorkflowCandidate(
                workflow_id="wf-verify",
                name="Follow-up prioritization",
                outcome_hypothesis="Reduce unowned qualified follow-ups.",
                baseline_ref="baseline://verify/1",
                evidence_refs=["evidence://verify/1"],
                accountable_owner="sales_ops",
                approval_path_ref="approval://verify/1",
                acceptance_criteria_ref="acceptance://verify/1",
                trigger="scheduled internal queue review",
                input_contract="approved CRM fields only",
                deterministic_steps=["load", "dedupe", "rank"],
                ai_reasoning_steps_if_needed=[],
                tool_allowlist=["crm_read_only"],
                authority_class="INTERNAL_PREPARATION_ONLY",
                approval_points=["any external follow-up"],
                output_contract="source-bound internal priority queue",
                evidence_receipt="receipt://followup-priority-v1",
                idempotency_key="account+snapshot+policy",
                retry_policy="bounded transient retry",
                rollback_or_safe_failure="fail closed to prior verified snapshot",
                human_handoff="ambiguous ownership -> sales_ops",
                evaluation_cases=["known owner", "missing owner", "suppressed contact"],
            )
        ],
        selected_workflow_id="wf-verify",
    )


def _verify_runtime(errors: list[str]) -> None:
    planner = CompanyBrainSprintPlanner()

    empty = planner.assess(
        CompanyBrainSprintRequest(account_id="empty", company_name="Empty Co")
    )
    require(
        empty.status == "EVIDENCE_GAPS_BLOCK_SCOPE",
        "runtime: empty assessment must fail closed",
        errors,
    )
    require(
        not any(empty.authority.values()),
        "runtime: incomplete assessment granted authority",
        errors,
    )

    ready_request = _ready_request()
    ready = planner.assess(ready_request)
    require(
        ready.status == "READY_FOR_CUSTOMER_SPECIFIC_SCOPE_REVIEW",
        "runtime: complete evidence packet did not become scope-review ready",
        errors,
    )
    require(
        ready.gates.get("source_registry_contract_complete") is True,
        "runtime: complete source registry not recognized",
        errors,
    )
    require(
        ready.gates.get("bounded_workflow_contract_complete") is True,
        "runtime: complete bounded workflow not recognized",
        errors,
    )
    require(
        ready.gates.get("customer_validation_verified") is False,
        "runtime: customer validation reference must not become verified value",
        errors,
    )
    require(
        ready.customer_validation_state
        == "REFERENCE_PRESENT_NOT_CUSTOMER_VALUE_PROOF",
        "runtime: customer validation reference semantics drift",
        errors,
    )
    require(
        not any(ready.authority.values()),
        "runtime: scope-ready assessment granted execution/commercial authority",
        errors,
    )

    legacy_source = ready_request.model_copy(
        update={
            "sources": [
                BrainSource(
                    source_id="crm",
                    source_ref="crm://tenant/verify",
                    owner="sales_ops",
                    freshness_or_expiry="2026-09-29T00:00:00+00:00",
                    permission_ref="permission://crm/verify",
                    provenance="customer_connected_crm",
                )
            ]
        }
    )
    blocked_source = planner.assess(legacy_source)
    require(
        blocked_source.status == "EVIDENCE_GAPS_BLOCK_SCOPE",
        "runtime: legacy minimal source metadata must not satisfy current registry",
        errors,
    )
    require(
        "source:crm:tenant_scope" in blocked_source.source_registry_gaps,
        "runtime: tenant-scope gap not detected",
        errors,
    )
    require(
        "source:crm:last_verified_at" in blocked_source.source_registry_gaps,
        "runtime: source verification-time gap not detected",
        errors,
    )
    require(
        "source:crm:allowed_claims" in blocked_source.source_registry_gaps,
        "runtime: source claim-policy gap not detected",
        errors,
    )

    legacy_workflow = ready_request.model_copy(
        update={
            "workflow_candidates": [
                WorkflowCandidate(
                    workflow_id="wf-verify",
                    name="Follow-up prioritization",
                    outcome_hypothesis="Reduce unowned qualified follow-ups.",
                    baseline_ref="baseline://verify/1",
                    evidence_refs=["evidence://verify/1"],
                    accountable_owner="sales_ops",
                    approval_path_ref="approval://verify/1",
                    acceptance_criteria_ref="acceptance://verify/1",
                )
            ]
        }
    )
    blocked_workflow = planner.assess(legacy_workflow)
    require(
        blocked_workflow.status == "EVIDENCE_GAPS_BLOCK_SCOPE",
        "runtime: legacy minimal workflow must not satisfy bounded-workflow contract",
        errors,
    )
    require(
        "workflow:wf-verify:tool_allowlist" in blocked_workflow.workflow_contract_gaps,
        "runtime: missing tool allowlist not detected",
        errors,
    )
    require(
        "workflow:wf-verify:idempotency_key" in blocked_workflow.workflow_contract_gaps,
        "runtime: missing idempotency contract not detected",
        errors,
    )
    require(
        "workflow:wf-verify:rollback_or_safe_failure"
        in blocked_workflow.workflow_contract_gaps,
        "runtime: missing rollback/safe-failure contract not detected",
        errors,
    )

    repeated = planner.assess(ready_request)
    require(
        repeated.assessment_id == ready.assessment_id,
        "runtime: assessment identity must remain deterministic",
        errors,
    )


def main() -> int:
    errors: list[str] = []
    require(CONTRACT.exists(), "missing Company Brain sprint assessment", errors)
    if errors:
        print("DEALIX_COMPANY_BRAIN_SPRINT_VERDICT=FAIL")
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    require(
        contract.get("schema") == "dealix.company-brain-sprint-assessment.v1",
        "wrong schema",
        errors,
    )
    require(
        contract.get("package") == "COMPANY_BRAIN_GOVERNED_AI_SPRINT",
        "package drift",
        errors,
    )
    require(
        contract.get("canonical_owner") == "Dealix Company Brain",
        "canonical Company Brain owner drift",
        errors,
    )
    require(
        contract.get("owner_mode") == "REUSE_AND_EXTEND_EXISTING_ONLY",
        "parallel brain must be blocked",
        errors,
    )

    prohibited = set(contract.get("prohibited_new_owners", []))
    for required in (
        "parallel_company_brain",
        "parallel_vector_truth_store",
        "parallel_crm_truth",
        "parallel_approval_center",
        "parallel_proof_ledger",
        "parallel_scheduler",
        "new_permanent_agent_fleet",
    ):
        require(
            required in prohibited,
            f"missing duplicate-owner prohibition: {required}",
            errors,
        )

    entry = contract.get("commercial_entry", {})
    require(
        entry.get("public_fixed_price_authority") is False,
        "fixed-price authority must remain false",
        errors,
    )
    require(
        entry.get("generic_chatbot_offer") is False,
        "generic chatbot offer must remain false",
        errors,
    )
    require(
        entry.get("unlimited_agent_build_offer") is False,
        "unlimited agent build must remain false",
        errors,
    )
    paid = set(entry.get("paid_scope_requires", []))
    for required in (
        "qualified_problem",
        "named_bounded_use_case",
        "source_and_owner_map",
        "authority_map",
        "baseline_or_evidence_gap",
        "success_and_proof_method",
        "customer_specific_scope",
        "quote_authority_ref",
    ):
        require(required in paid, f"paid-scope gate missing: {required}", errors)

    registry = contract.get("company_brain_source_registry", {})
    required_per_source = set(registry.get("required_per_source", []))
    for required in (
        "source_id",
        "source_type",
        "system_owner",
        "tenant_scope",
        "purpose",
        "authority_or_lawful_basis",
        "access_class",
        "freshness_sla",
        "last_verified_at",
        "provenance_ref",
        "retention_or_expiry",
        "allowed_claims",
        "prohibited_uses",
    ):
        require(
            required in required_per_source,
            f"source-registry field missing: {required}",
            errors,
        )
    require(
        registry.get("missing_authority") == "BLOCK_USE",
        "missing source authority must fail closed",
        errors,
    )
    require(
        registry.get("public_data_is_consent") is False,
        "public data must not equal consent",
        errors,
    )

    workflow = contract.get("bounded_workflow_contract", {})
    workflow_required = set(workflow.get("required", []))
    for required in (
        "single_named_outcome",
        "input_contract",
        "deterministic_steps",
        "tool_allowlist",
        "authority_class",
        "approval_points",
        "output_contract",
        "evidence_receipt",
        "idempotency_key",
        "retry_policy",
        "rollback_or_safe_failure",
        "human_handoff",
        "evaluation_cases",
    ):
        require(
            required in workflow_required,
            f"bounded-workflow field missing: {required}",
            errors,
        )
    require(
        workflow.get("ai_may_self_expand_tool_authority") is False,
        "AI must not self-expand authority",
        errors,
    )
    require(
        workflow.get("workflow_may_auto_create_external_commitment") is False,
        "workflow must not create external commitments",
        errors,
    )
    require(
        workflow.get("workflow_may_bypass_tenant_scope") is False,
        "tenant boundary bypass must be blocked",
        errors,
    )
    require(
        workflow.get("workflow_may_promote_unknown_to_fact") is False,
        "unknown promotion must be blocked",
        errors,
    )

    phases = [phase.get("phase") for phase in contract.get("delivery_phases", [])]
    require(
        phases
        == [
            "CONTEXT_AND_AUTHORITY_AUDIT",
            "BOUNDED_USE_CASE_SELECTION",
            "COMPANY_BRAIN_SEED_OR_EXTENSION",
            "ONE_BOUNDED_WORKFLOW",
            "EVALUATION_AND_HANDOVER",
            "THIRTY_DAY_PROOF",
        ],
        "delivery phases drift",
        errors,
    )

    evaluation = contract.get("evaluation_contract", {})
    dimensions = set(evaluation.get("required_dimensions", []))
    for required in (
        "task_success",
        "groundedness_or_source_support",
        "authority_compliance",
        "tenant_isolation",
        "unknown_handling",
        "unsafe_action_refusal",
        "latency",
        "cost",
        "operator_minutes",
        "evidence_completeness",
    ):
        require(
            required in dimensions,
            f"evaluation dimension missing: {required}",
            errors,
        )
    require(
        evaluation.get("customer_value_requires_customer_validation") is True,
        "customer validation gate missing",
        errors,
    )
    require(
        evaluation.get("technical_pass_is_customer_value") is False,
        "technical pass must not equal customer value",
        errors,
    )
    require(
        evaluation.get("synthetic_eval_is_customer_proof") is False,
        "synthetic eval must not equal customer proof",
        errors,
    )

    proof = contract.get("proof_output", {})
    require(
        proof.get("public_use_requires_permission") is True,
        "public proof permission missing",
        errors,
    )

    stop_rules = set(contract.get("stop_rules", []))
    require(
        "No second Company Brain or truth store." in stop_rules,
        "duplicate Company Brain stop rule missing",
        errors,
    )
    require(
        "No generic chatbot as the default deliverable." in stop_rules,
        "generic chatbot stop rule missing",
        errors,
    )
    require(
        "No customer-value claim from synthetic or technical-only evidence."
        in stop_rules,
        "proof integrity stop rule missing",
        errors,
    )

    _verify_runtime(errors)

    if errors:
        print("DEALIX_COMPANY_BRAIN_SPRINT_VERDICT=FAIL")
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("DEALIX_COMPANY_BRAIN_SPRINT_VERDICT=PASS")
    print("CANONICAL_COMPANY_BRAIN=REUSED")
    print("CONTRACT_RUNTIME_ALIGNMENT=PASS")
    print("SOURCE_TENANT_FRESHNESS_CLAIMS_POLICY=REQUIRED")
    print("BOUNDED_WORKFLOW_TOOL_AUTHORITY_IDEMPOTENCY_ROLLBACK=REQUIRED")
    print("CUSTOMER_VALIDATION_REFERENCE_IS_CUSTOMER_VALUE_PROOF=NO")
    print("TECHNICAL_PASS_IS_CUSTOMER_VALUE=NO")
    print("EXTERNAL_COMMITMENTS=APPROVAL_GATED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
