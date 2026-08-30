#!/usr/bin/env python3
"""Fail-closed verifier for Dealix Brand & Growth Portfolio V2."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/commercial/brand_growth_portfolio_v2.json"
CONTINUITY_CONTRACT = ROOT / "data/commercial/continuous_company_operations_v1.json"

EXPECTED_COMPOSITE_ARMS = {
    "MARKET_INTELLIGENCE_FORESIGHT",
    "BRAND_CATEGORY_AUTHORITY",
    "CONTENT_SEARCH_DISTRIBUTION",
    "RELATIONSHIP_REVENUE",
    "COMPANY_BRAIN_DEEP_TECH",
    "SAUDI_MARKET_ACCESS_PARTNERS",
    "PROOF_EXPANSION_PRODUCTIZATION",
    "DEVELOPMENT_LEARNING_FACTORY",
}

EXPECTED_ARMS = {
    "BRAND_AUTHORITY",
    "WEBSITE_CONVERSION",
    "SEARCH_SEO_AEO",
    "FOUNDER_THOUGHT_LEADERSHIP",
    "COMPANY_SOCIAL_VIDEO",
    "EVENT_FIELD_INTELLIGENCE",
    "PARTNER_MARKET_ACCESS",
    "ACCOUNT_ABM_INTELLIGENCE",
    "INBOUND_DIAGNOSTIC_CAPTURE",
    "EMAIL_LIFECYCLE",
    "PR_MEDIA_COMMUNITY_SPEAKING",
    "PROOF_ADVOCACY_REFERRAL",
    "PAID_MEDIA_READINESS",
    "DEEP_TECHNICAL_DEMAND",
    "MARKET_INTELLIGENCE_EXPERIMENTATION",
}

EXPECTED_WORKERS = ["dealix-pm", "dealix-sales", "dealix-content", "dealix-delivery", "dealix-engineer"]

REQUIRED_FALSE_AUTHORITY = {
    "new_scheduler",
    "new_permanent_agent_fleet",
    "new_crm",
    "new_company_brain",
    "new_opportunity_graph",
    "new_approval_center",
    "new_proof_ledger",
    "new_analytics_truth_store",
    "external_send",
    "public_publish",
    "paid_spend",
    "payment_or_refund",
    "quote_discount_contract",
    "tender_submission",
    "production_dns_db_secrets",
    "main_merge",
    "public_customer_proof",
    "personal_linkedin_automation",
    "cold_or_bulk_whatsapp",
}

REQUIRED_TRUTH_INVARIANTS = {
    "research != relationship",
    "public_contact != consent",
    "draft != sent_or_published",
    "proposal_or_invoice != payment",
    "technical_or_synthetic != customer_outcome_proof",
}


def fail(message: str) -> None:
    raise SystemExit(f"DEALIX_BRAND_GROWTH_PORTFOLIO_VERDICT=FAIL\nFAIL: {message}")


def read_json(path: Path, label: str) -> dict:
    if not path.exists():
        fail(f"{label} is missing")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{label} is not valid JSON: {exc}")
    if not isinstance(payload, dict):
        fail(f"{label} must be a JSON object")
    return payload


def main() -> int:
    payload = read_json(CONTRACT, "portfolio contract")

    if payload.get("schema") != "dealix.brand-growth-portfolio.v2":
        fail("unexpected contract schema")

    if payload.get("portfolio_objective") != "CASH_READY_AUTONOMOUS_DEALIX_COMPANY":
        fail("portfolio objective drift")

    composite_arms = payload.get("composite_arms")
    if not isinstance(composite_arms, list):
        fail("composite_arms must be a list")
    composite_ids = [arm.get("id") for arm in composite_arms if isinstance(arm, dict)]
    if set(composite_ids) != EXPECTED_COMPOSITE_ARMS or len(composite_ids) != len(set(composite_ids)):
        fail("composite arm registry drift")
    for arm in composite_arms:
        if not isinstance(arm.get("owner"), list) or not arm.get("composes") or not arm.get("outcome"):
            fail(f"invalid composite arm: {arm.get('id', '<unknown>')}")

    arms = payload.get("arms")
    if not isinstance(arms, list):
        fail("arms must be a list")

    arm_ids = [arm.get("id") for arm in arms if isinstance(arm, dict)]
    if len(arm_ids) != len(set(arm_ids)):
        fail("duplicate arm id")
    if set(arm_ids) != EXPECTED_ARMS:
        fail(f"arm registry drift: {sorted(set(arm_ids) ^ EXPECTED_ARMS)}")

    for arm in arms:
        if not isinstance(arm, dict):
            fail("arm entry must be an object")
        for field in ("id", "owner", "inputs", "outputs", "primary_evidence", "success_signal"):
            if not arm.get(field):
                fail(f"{arm.get('id', '<unknown>')} missing {field}")
        if not all(isinstance(owner, str) and owner.startswith("#") for owner in arm["owner"]):
            fail(f"{arm['id']} has non-canonical owner reference")

    authority = payload.get("authority", {})
    missing = REQUIRED_FALSE_AUTHORITY - set(authority)
    if missing:
        fail(f"missing authority keys: {sorted(missing)}")
    raised = sorted(key for key in REQUIRED_FALSE_AUTHORITY if authority.get(key) is not False)
    if raised:
        fail(f"authority must remain false: {raised}")

    if set(payload.get("truth_invariants", [])) < REQUIRED_TRUTH_INVARIANTS:
        fail("truth invariant coverage drift")

    workers = payload.get("canonical_workers", [])
    if workers != EXPECTED_WORKERS:
        fail("canonical worker roster drift")

    allocation = payload.get("allocation_model", {})
    if allocation.get("max_active_growth_bets_per_week") != 3:
        fail("growth bet WIP limit drift")
    if allocation.get("vanity_metrics_are_diagnostic_only") is not True:
        fail("vanity metric boundary drift")

    radar = payload.get("radar_activation", {})
    if radar.get("max_admitted_web_research_adapters") != 1:
        fail("web research adapter limit drift")
    if radar.get("blocked_if_unmeasured") is not True:
        fail("unmeasured adapter admission must fail closed")

    productization = payload.get("productization_gate", {})
    if productization.get("minimum_paid_deployments_same_family") != 3:
        fail("productization payment evidence gate drift")
    if productization.get("minimum_customer_accepted_proof_packs") != 2:
        fail("productization proof gate drift")

    if payload.get("continuous_loop") != ["OBSERVE", "RECONCILE", "PRIORITIZE", "DELEGATE", "EXECUTE", "VERIFY", "RECEIPT", "MEASURE", "LEARN", "IMPROVE", "REPEAT"]:
        fail("continuous loop drift")

    president = payload.get("president_contract", {})
    if president.get("unknown_value") != "UNKNOWN_NOT_EVIDENCE_BACKED":
        fail("unknown handling drift")
    if not president.get("required_receipt_fields") or president.get("founder_output") != ["MONEY", "DECISIONS", "RISKS", "APPROVALS", "NEXT_ACTION"]:
        fail("president receipt/output contract drift")

    continuity = read_json(CONTINUITY_CONTRACT, "continuous company operations contract")
    if continuity.get("schema") != "dealix.continuous-company-operations.v1":
        fail("continuous operations schema drift")
    if continuity.get("portfolio_objective") != payload.get("portfolio_objective"):
        fail("continuous operations objective must match portfolio objective")
    if continuity.get("canonical_workers") != EXPECTED_WORKERS:
        fail("continuous operations canonical worker roster drift")

    runtime = continuity.get("runtime_ownership", {})
    if runtime.get("scheduler_owner") != "EXISTING_DEALIX_COMPANY_AUTOPILOT_ONLY":
        fail("continuous operations must reuse canonical Company Autopilot")
    for key in (
        "new_scheduler_allowed",
        "new_timer_allowed",
        "new_permanent_agent_allowed",
        "new_company_os_allowed",
        "new_truth_store_allowed",
    ):
        if runtime.get(key) is not False:
            fail(f"continuous operations may not raise {key}")

    ladder = continuity.get("autonomy_ladder", {})
    if ladder.get("L5_EXTERNAL_OR_IRREVERSIBLE") != "ACTION_SPECIFIC_APPROVAL_REQUIRED":
        fail("L5 action-specific approval boundary drift")

    objectives = continuity.get("service_objectives", {})
    for key in (
        "unauthorized_external_effects",
        "truth_promotion_violations",
        "parallel_scheduler_count",
        "parallel_company_os_count",
        "parallel_permanent_agent_fleets",
        "unreceipted_internal_mutations",
        "lost_required_receipts",
    ):
        if objectives.get(key) != 0:
            fail(f"continuous service objective must remain zero: {key}")

    improvement = continuity.get("self_improvement_policy", {})
    if improvement.get("evidence_backed_observation_required") is not True:
        fail("self-improvement must remain evidence-backed")
    if improvement.get("simulated_metrics_can_authorize_mutation") is not False:
        fail("simulated metrics may not authorize mutation")
    if improvement.get("synthetic_evidence_can_authorize_commercial_truth") is not False:
        fail("synthetic evidence may not authorize commercial truth")

    activation = continuity.get("activation_gate", {})
    if activation.get("main_merge_authority") is not False or activation.get("production_activation_authority") is not False:
        fail("continuous operations contract may not authorize merge or production activation")
    required_dependencies = {
        "#1405_EXACT_HEAD_ACCEPTANCE",
        "#1406_EXACT_HEAD_ACCEPTANCE",
        "CURRENT_VPS_RUNTIME_RECEIPT",
        "SOVEREIGN_TRUST_RECEIPT",
    }
    if not required_dependencies.issubset(set(activation.get("depends_on", []))):
        fail("continuous operations activation dependencies drift")

    print("DEALIX_BRAND_GROWTH_PORTFOLIO_VERDICT=PASS")
    print("MULTI_ARM_REGISTRY=PASS")
    print("EIGHT_COMPOSITE_ARMS=PASS")
    print("CASH_READY_OBJECTIVE=PASS")
    print("CANONICAL_OWNER_REUSE=PASS")
    print("TRUTH_FIREWALL=PASS")
    print("NO_PARALLEL_SCHEDULER_OR_AGENT_FLEET=PASS")
    print("EXTERNAL_AUTHORITY=BLOCKED")
    print("PAID_MEDIA=READINESS_ONLY")
    print("WEB_RESEARCH_ADAPTER_MAX=1")
    print("PRODUCTIZATION=EVIDENCE_GATED")
    print("BOUNDED_24X7_CONTINUITY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
