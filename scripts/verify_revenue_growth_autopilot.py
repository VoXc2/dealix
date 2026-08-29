#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/commercial/revenue_growth_autopilot_contract.json"
DOC = ROOT / "docs/commercial/REVENUE_GROWTH_AUTOPILOT_2026.md"


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []

    require(CONTRACT.exists(), "missing revenue growth contract", errors)
    require(DOC.exists(), "missing revenue growth operating doc", errors)
    if errors:
        print("DEALIX_REVENUE_GROWTH_AUTOPILOT_VERDICT=FAIL")
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    require(contract.get("schema") == "dealix.revenue-growth-autopilot.v1", "wrong schema", errors)
    require(contract.get("north_star") == "FIRST_VERIFIED_PAID_PILOT", "wrong north star", errors)
    require(contract.get("positioning") == "Saudi-first AI Business Operating System", "positioning drift", errors)

    truth = contract.get("truth_invariants", {})
    require(truth.get("research_is_relationship") is False, "research must not equal relationship", errors)
    require(truth.get("crm_record_is_commercial_truth") is False, "CRM must not own commercial truth", errors)
    require(truth.get("proposal_is_revenue") is False, "proposal must not equal revenue", errors)
    require(truth.get("invoice_is_payment") is False, "invoice must not equal payment", errors)
    require(truth.get("verified_revenue_requires_payment_evidence") is True, "payment evidence gate missing", errors)
    require(truth.get("public_customer_proof_requires_permission") is True, "customer proof permission gate missing", errors)

    architecture = contract.get("architecture", {})
    require(architecture.get("company_brain") == "reuse_existing", "parallel Company Brain not allowed", errors)
    require(architecture.get("opportunity_graph") == "reuse_existing", "parallel Opportunity Graph not allowed", errors)
    require(architecture.get("approval_center") == "reuse_existing", "parallel Approval Center not allowed", errors)
    require(architecture.get("proof_ledger") == "reuse_existing", "parallel Proof Ledger not allowed", errors)
    require(architecture.get("crm") == "mirror_only", "CRM must remain mirror-only", errors)
    require(architecture.get("scheduler") == "existing_canonical_owner_only", "duplicate scheduler not allowed", errors)

    states = contract.get("commercial_state_machine", [])
    for required in (
        "RESEARCH_ONLY",
        "VERIFIED_RELATIONSHIP",
        "QUALIFIED_PROBLEM",
        "DIAGNOSTIC",
        "DISCOVERY",
        "BUYING_GROUP_MAPPED",
        "NEGOTIATION",
        "PAID_PILOT",
        "DELIVERY",
        "PROOF",
    ):
        require(required in states, f"missing commercial state: {required}", errors)

    automation = contract.get("automation_classes", {})
    blocked = set(automation.get("BLOCKED", []))
    for required in (
        "cold_bulk_whatsapp",
        "unauthorized_linkedin_automation",
        "fabricated_customer_proof",
        "fabricated_compliance_claim",
        "suppression_or_optout_bypass",
    ):
        require(required in blocked, f"missing blocked action: {required}", errors)

    manual_native = set(automation.get("MANUAL_NATIVE", []))
    require("founder_linkedin_message" in manual_native, "LinkedIn personal messaging must remain manual-native", errors)

    specific = set(automation.get("SPECIFIC_APPROVAL_REQUIRED", []))
    for required in (
        "named_price_or_quote",
        "contract_or_legal_commitment",
        "payment_charge_refund_or_spend",
        "production_dns_secret_or_material_database_mutation",
        "approved_external_send_or_publish",
        "consented_follow_up_send",
    ):
        require(required in specific, f"missing specific approval gate: {required}", errors)

    negotiation = contract.get("negotiation", {})
    require(negotiation.get("concession_rule") == "NEVER_GIVE_ALWAYS_TRADE", "negotiation concession law missing", errors)
    require("walk_away_triggers" in negotiation, "walk-away policy missing", errors)
    require("tradable_variables_before_price" in negotiation, "trade-before-price policy missing", errors)

    tooling = contract.get("tooling", {})
    rejected = set(tooling.get("reject_duplicate_by_default", []))
    for required in ("new_CRM", "new_scheduler_or_workflow_engine", "new_agent_orchestration_framework"):
        require(required in rejected, f"duplicate architecture rejection missing: {required}", errors)

    require("No evidence -> reuse/refine/stop" in doc, "content evidence stop rule missing", errors)
    require("NEVER GIVE; ALWAYS TRADE" in doc, "negotiation trading rule missing from operating doc", errors)
    require("Research != relationship" in doc or "Research != Relationship" in doc or "research != relationship" in doc, "research/relationship truth rule missing from doc", errors)

    if errors:
        print("DEALIX_REVENUE_GROWTH_AUTOPILOT_VERDICT=FAIL")
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("DEALIX_REVENUE_GROWTH_AUTOPILOT_VERDICT=PASS")
    print(f"SCHEMA={contract['schema']}")
    print(f"NORTH_STAR={contract['north_star']}")
    print("DUPLICATE_ARCHITECTURE=BLOCKED")
    print("COLD_BULK_WHATSAPP=BLOCKED")
    print("LINKEDIN_PERSONAL_AUTOMATION=MANUAL_NATIVE")
    print("VERIFIED_REVENUE_REQUIRES_PAYMENT_EVIDENCE=YES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
