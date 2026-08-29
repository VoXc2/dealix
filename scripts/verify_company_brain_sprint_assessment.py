#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/commercial/company_brain_sprint_assessment_v1.json"


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    require(CONTRACT.exists(), "missing Company Brain sprint assessment", errors)
    if errors:
        print("DEALIX_COMPANY_BRAIN_SPRINT_VERDICT=FAIL")
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    require(contract.get("schema") == "dealix.company-brain-sprint-assessment.v1", "wrong schema", errors)
    require(contract.get("package") == "COMPANY_BRAIN_GOVERNED_AI_SPRINT", "package drift", errors)
    require(contract.get("canonical_owner") == "Dealix Company Brain", "canonical Company Brain owner drift", errors)
    require(contract.get("owner_mode") == "REUSE_AND_EXTEND_EXISTING_ONLY", "parallel brain must be blocked", errors)

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
        require(required in prohibited, f"missing duplicate-owner prohibition: {required}", errors)

    entry = contract.get("commercial_entry", {})
    require(entry.get("public_fixed_price_authority") is False, "fixed-price authority must remain false", errors)
    require(entry.get("generic_chatbot_offer") is False, "generic chatbot offer must remain false", errors)
    require(entry.get("unlimited_agent_build_offer") is False, "unlimited agent build must remain false", errors)
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
        require(required in required_per_source, f"source-registry field missing: {required}", errors)
    require(registry.get("missing_authority") == "BLOCK_USE", "missing source authority must fail closed", errors)
    require(registry.get("public_data_is_consent") is False, "public data must not equal consent", errors)

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
        require(required in workflow_required, f"bounded-workflow field missing: {required}", errors)
    require(workflow.get("ai_may_self_expand_tool_authority") is False, "AI must not self-expand authority", errors)
    require(workflow.get("workflow_may_auto_create_external_commitment") is False, "workflow must not create external commitments", errors)
    require(workflow.get("workflow_may_bypass_tenant_scope") is False, "tenant boundary bypass must be blocked", errors)
    require(workflow.get("workflow_may_promote_unknown_to_fact") is False, "unknown promotion must be blocked", errors)

    phases = [phase.get("phase") for phase in contract.get("delivery_phases", [])]
    required_phases = [
        "CONTEXT_AND_AUTHORITY_AUDIT",
        "BOUNDED_USE_CASE_SELECTION",
        "COMPANY_BRAIN_SEED_OR_EXTENSION",
        "ONE_BOUNDED_WORKFLOW",
        "EVALUATION_AND_HANDOVER",
        "THIRTY_DAY_PROOF",
    ]
    require(phases == required_phases, "delivery phases drift", errors)

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
        require(required in dimensions, f"evaluation dimension missing: {required}", errors)
    require(evaluation.get("customer_value_requires_customer_validation") is True, "customer validation gate missing", errors)
    require(evaluation.get("technical_pass_is_customer_value") is False, "technical pass must not equal customer value", errors)
    require(evaluation.get("synthetic_eval_is_customer_proof") is False, "synthetic eval must not equal customer proof", errors)

    proof = contract.get("proof_output", {})
    require(proof.get("public_use_requires_permission") is True, "public proof permission missing", errors)

    stop_rules = set(contract.get("stop_rules", []))
    require("No second Company Brain or truth store." in stop_rules, "duplicate Company Brain stop rule missing", errors)
    require("No generic chatbot as the default deliverable." in stop_rules, "generic chatbot stop rule missing", errors)
    require("No customer-value claim from synthetic or technical-only evidence." in stop_rules, "proof integrity stop rule missing", errors)

    if errors:
        print("DEALIX_COMPANY_BRAIN_SPRINT_VERDICT=FAIL")
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("DEALIX_COMPANY_BRAIN_SPRINT_VERDICT=PASS")
    print("CANONICAL_COMPANY_BRAIN=REUSED")
    print("BOUNDED_USE_CASES=REQUIRED")
    print("SOURCE_PROVENANCE_AND_AUTHORITY=REQUIRED")
    print("TECHNICAL_PASS_IS_CUSTOMER_VALUE=NO")
    print("EXTERNAL_COMMITMENTS=APPROVAL_GATED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
