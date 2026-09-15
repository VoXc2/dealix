#!/usr/bin/env python3
"""Fail-closed verifier for Dealix bounded 24x7 Company Operations contract.

This verifier is intentionally stdlib-only. It proves contract invariants; it does not
start timers, send messages, publish content, spend money, merge main, or mutate prod.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "commercial" / "continuous_company_operations_v1.json"

EXPECTED_WORKERS = {
    "dealix-pm",
    "dealix-sales",
    "dealix-content",
    "dealix-delivery",
    "dealix-engineer",
}
# Historical five names are legacy compatibility aliases only. Canonical
# logical-agent authority is the Agentic Holding current registry; runtime
# capacity belongs to ResourceGovernor + Session Factory.
LEGACY_EXECUTOR_ALIASES = EXPECTED_WORKERS
LEGACY_ALIAS_SEMANTICS = "LEGACY_EXECUTOR_ALIASES_ONLY_NOT_ARCHITECTURE_AUTHORITY"
LOGICAL_AGENT_AUTHORITY = "dealix.agentic_holding.runtime.build_current_registry"
RUNTIME_CAPACITY_AUTHORITY = "ResourceGovernor+Session Factory"
MAX_BETS_SEMANTICS = "ECONOMIC_FOCUS_HEURISTIC_ONLY_NOT_RUNTIME_CAPACITY"

EXPECTED_WORKLOADS = {
    "RUNTIME_TRUST_WATCH",
    "MARKET_EVENT_RADAR",
    "BRAND_CONTENT_OPPORTUNITY_QUEUE",
    "RELATIONSHIP_REVENUE_QUEUE",
    "DELIVERY_PROOF_LOOP",
    "PORTFOLIO_ECONOMICS_AND_DECISIONS",
    "EVIDENCE_DRIVEN_DEVELOPMENT_FACTORY",
}

EXPECTED_MODES = {
    "status",
    "heartbeat",
    "production",
    "repo-watch",
    "preflight",
    "morning-fallback",
    "midday",
    "evening",
    "nightly",
    "market-radar",
    "weekly",
    "local-ai",
}

REQUIRED_RECEIPT_FIELDS = {
    "workload_id",
    "system_id",
    "agent_owner",
    "objective",
    "input_evidence_refs",
    "source_sha",
    "state_before",
    "action",
    "authority_class",
    "started_at",
    "finished_at",
    "result",
    "state_after",
    "output_evidence_refs",
    "next_evidence",
    "next_action",
    "founder_minutes",
    "agent_minutes",
    "elapsed_seconds",
    "ai_cost",
    "tool_cost",
    "risk",
    "economic_delta",
    "idempotency_key",
    "rollback_or_safe_failure",
}

REQUIRED_L5 = {
    "external_customer_send",
    "public_publish",
    "paid_spend",
    "payment_or_refund",
    "binding_quote_or_discount",
    "legal_commitment",
    "tender_submission",
    "main_merge",
    "production_mutation",
    "dns_mutation",
    "database_mutation",
    "secret_or_credential_mutation",
    "public_customer_proof",
}

REQUIRED_ACTIVATION_DEPENDENCIES = {
    "CURRENT_MAIN_MARKET_RADAR_ACCEPTANCE",
    "CURRENT_MAIN_BRAND_GROWTH_ACCEPTANCE",
    "CURRENT_MAIN_SERVER_AGENT_MODEL_ACCEPTANCE",
    "CURRENT_MAIN_GROWTH_AUTOPILOT_WIRING_ACCEPTANCE",
    "CURRENT_VPS_RUNTIME_RECEIPT",
    "SOVEREIGN_TRUST_RECEIPT",
}

EXPECTED_FOUNDER_SECTIONS = ["MONEY", "DECISIONS", "RISKS", "APPROVALS", "NEXT_ACTION"]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> None:
    require(CONTRACT.is_file(), f"missing contract: {CONTRACT}")
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))

    require(data.get("schema") == "dealix.continuous-company-operations.v1", "schema drift")
    require(data.get("portfolio_objective") == "CASH_READY_AUTONOMOUS_DEALIX_COMPANY", "portfolio objective drift")
    require(
        data.get("optimization_objective")
        == "MAXIMIZE_VERIFIED_ECONOMIC_MOVEMENT_PER_FOUNDER_MINUTE_PER_COST_PER_RISK",
        "economic objective drift",
    )

    runtime = data.get("runtime_ownership", {})
    require(runtime.get("scheduler_owner") == "EXISTING_DEALIX_COMPANY_AUTOPILOT_ONLY", "scheduler owner drift")
    for key in (
        "new_scheduler_allowed",
        "new_timer_allowed",
        "new_permanent_agent_allowed",
        "new_company_os_allowed",
        "new_truth_store_allowed",
    ):
        require(runtime.get(key) is False, f"{key} must remain false")
    require(set(runtime.get("allowed_existing_modes", [])) == EXPECTED_MODES, "existing autopilot mode set drift")

    require(set(data.get("canonical_workers", [])) == EXPECTED_WORKERS, "canonical worker roster drift")
    require(data.get("canonical_workers_field_semantics") == LEGACY_ALIAS_SEMANTICS, "worker alias semantics drift")
    require(set(data.get("legacy_executor_aliases", [])) == LEGACY_EXECUTOR_ALIASES, "legacy executor alias set drift")
    require(data.get("logical_agent_authority") == LOGICAL_AGENT_AUTHORITY, "logical-agent authority drift")
    require(data.get("fixed_five_authority") is False, "fixed-five authority must remain false")
    require(data.get("runtime_capacity_authority") == RUNTIME_CAPACITY_AUTHORITY, "runtime capacity authority drift")

    workloads = data.get("always_on_workloads", [])
    workload_ids = {item.get("id") for item in workloads}
    require(workload_ids == EXPECTED_WORKLOADS, "always-on workload set drift")
    for item in workloads:
        require(item.get("owner") in EXPECTED_WORKERS, f"non-canonical owner for {item.get('id')}")
        require(bool(item.get("scope")), f"missing scope for {item.get('id')}")
        require(bool(item.get("output")), f"missing output for {item.get('id')}")
        require(bool(item.get("side_effects")), f"missing side-effect declaration for {item.get('id')}")

    event = data.get("active_event_mode", {})
    require(event.get("forbidden_promotions") == [
        "EXHIBITOR_AS_LEAD",
        "BADGE_SCAN_AS_RELATIONSHIP",
        "PUBLIC_EMAIL_AS_CONSENT",
        "EVENT_DIRECTORY_AS_PIPELINE",
    ], "event truth-firewall drift")
    require("REAL_TWO_WAY_INTERACTION" in event.get("conversion_path", []), "event path requires real interaction")
    require("VERIFIED_RELATIONSHIP_BY_CANONICAL_OWNER" in event.get("conversion_path", []), "relationship owner boundary missing")

    ladder = data.get("autonomy_ladder", {})
    require(ladder.get("L0_OBSERVE") == "AUTOMATIC", "L0 must remain automatic")
    require(ladder.get("L1_ANALYZE") == "AUTOMATIC", "L1 must remain automatic")
    require(ladder.get("L2_DRAFT") == "AUTOMATIC", "L2 must remain automatic")
    require("AUTOMATIC" in str(ladder.get("L3_INTERNAL_EXECUTE", "")), "L3 internal autonomy missing")
    require("AUTOMATIC" in str(ladder.get("L4_REPO_EXECUTE", "")), "L4 repo autonomy missing")
    require(ladder.get("L5_EXTERNAL_OR_IRREVERSIBLE") == "ACTION_SPECIFIC_APPROVAL_REQUIRED", "L5 approval boundary drift")
    require(set(data.get("l5_actions", [])) == REQUIRED_L5, "L5 action set drift")

    receipt = data.get("universal_work_receipt", {})
    require(set(receipt.get("required_fields", [])) == REQUIRED_RECEIPT_FIELDS, "universal receipt fields drift")
    require(receipt.get("unknown_value") == "UNKNOWN_NOT_EVIDENCE_BACKED", "unknown-value truth rule drift")
    require(receipt.get("no_secret_or_customer_payload_capture") is True, "receipt privacy boundary must remain true")

    slo = data.get("service_objectives", {})
    zero_objectives = (
        "unauthorized_external_effects",
        "truth_promotion_violations",
        "parallel_scheduler_count",
        "parallel_company_os_count",
        "parallel_permanent_agent_fleets",
        "unreceipted_internal_mutations",
        "lost_required_receipts",
    )
    for key in zero_objectives:
        require(slo.get(key) == 0, f"{key} objective must be zero")
    require(slo.get("stale_critical_source_behavior") == "DEGRADE_OR_BLOCK_NEVER_INVENT", "stale-source behavior drift")
    require(slo.get("missing_evidence_behavior") == "UNKNOWN_NOT_EVIDENCE_BACKED", "missing-evidence behavior drift")
    require(slo.get("vanity_metric_authority") == "DIAGNOSTIC_ONLY", "vanity metrics gained authority")

    recovery = data.get("recovery_policy", {})
    for key in (
        "bounded_retry_required",
        "idempotency_required",
        "safe_failure_required",
        "rollback_required_when_mutating_internal_state",
        "never_self_grant_authority",
        "never_repair_by_disabling_truth_or_security_gates",
    ):
        require(recovery.get(key) is True, f"recovery invariant false: {key}")

    improvement = data.get("self_improvement_policy", {})
    require(improvement.get("evidence_backed_observation_required") is True, "self-improvement must be evidence-backed")
    require(improvement.get("simulated_metrics_can_authorize_mutation") is False, "simulated metrics cannot authorize mutation")
    require(improvement.get("synthetic_evidence_can_authorize_commercial_truth") is False, "synthetic evidence cannot authorize truth")
    expected_path = [
        "VERIFIED_GAP",
        "CANONICAL_OWNER_LOOKUP",
        "ISSUE",
        "FRESH_MAIN_ISOLATED_WORKTREE",
        "SMALLEST_PATCH",
        "TARGETED_TESTS",
        "DRAFT_PR",
        "EXACT_HEAD_SOVEREIGN_VERIFICATION",
        "KEEP_OR_REVERT_DECISION",
        "LEARNING_EVENT",
    ]
    require(improvement.get("path") == expected_path, "development factory path drift")

    research = data.get("research_policy", {})
    require(research.get("official_and_first_party_first") is True, "official/first-party source priority missing")
    require(research.get("authorized_reporting_read_only_first") is True, "reporting must be read-only first")
    require(research.get("public_data_does_not_create_relationship_or_consent") is True, "public-data truth boundary missing")
    require(research.get("maximum_admitted_web_research_adapters") == 1, "more than one research adapter admitted")
    require(research.get("adapter_requires_measured_coverage_gap") is True, "research adapter gap gate missing")
    require(research.get("linkedin_personal_automation") is False, "personal LinkedIn automation must remain false")
    require(research.get("cold_bulk_whatsapp") is False, "cold/bulk WhatsApp must remain false")

    founder = data.get("founder_interface", {})
    require(founder.get("sections") == EXPECTED_FOUNDER_SECTIONS, "founder command projection drift")
    require(founder.get("maximum_active_growth_bets") == 3, "founder WIP limit drift")
    require(founder.get("maximum_active_growth_bets_semantics") == MAX_BETS_SEMANTICS, "growth-bet focus semantics drift")
    require(founder.get("runtime_capacity_authority") == RUNTIME_CAPACITY_AUTHORITY, "founder runtime capacity authority drift")
    require(founder.get("default_low_urgency_behavior") == "BATCH_AND_DELEGATE", "founder attention policy drift")

    activation = data.get("activation_gate", {})
    require(
        REQUIRED_ACTIVATION_DEPENDENCIES.issubset(set(activation.get("depends_on", []))),
        "current-main activation dependencies drift",
    )
    require(activation.get("main_merge_authority") is False, "contract cannot authorize main merge")
    require(activation.get("production_activation_authority") is False, "contract cannot authorize production activation")

    print("DEALIX_CONTINUOUS_COMPANY_OPERATIONS_V1=PASS")
    print(f"contract={CONTRACT.relative_to(ROOT)}")
    print(f"workers={len(EXPECTED_WORKERS)}")
    print(f"always_on_workloads={len(EXPECTED_WORKLOADS)}")
    print(f"receipt_fields={len(REQUIRED_RECEIPT_FIELDS)}")
    print("scheduler=EXISTING_DEALIX_COMPANY_AUTOPILOT_ONLY")
    print("allowed_existing_mode=market-radar")
    print("activation_dependencies=CURRENT_MAIN_AND_SOVEREIGN_RECEIPTS")
    print("external_or_irreversible_authority=ACTION_SPECIFIC_APPROVAL_REQUIRED")


if __name__ == "__main__":
    main()
