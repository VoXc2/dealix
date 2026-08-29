#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from dealix.commercial.portfolio_router import (
    INTERACTION_EVIDENCE_PRESENT,
    UNKNOWN,
    DemandSignal,
    EntryPackage,
    PortfolioPackageRouter,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/commercial/package_routing_contract_v1.json"


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    require(CONTRACT.exists(), "missing package routing contract", errors)
    if errors:
        print("DEALIX_PACKAGE_ROUTER_VERDICT=FAIL")
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    require(contract.get("schema") == "dealix.package-routing.v1", "wrong schema", errors)
    require(
        contract.get("positioning") == "Saudi-first AI Business Operating System",
        "positioning drift",
        errors,
    )
    require(
        contract.get("portfolio_objective") == "CASH_READY_AUTONOMOUS_DEALIX_COMPANY",
        "portfolio objective drift",
        errors,
    )

    owners = contract.get("canonical_owners", {})
    require(owners.get("company_brain") == "existing_canonical_owner", "parallel Company Brain not allowed", errors)
    require(owners.get("opportunity_graph") == "existing_canonical_owner", "parallel Opportunity Graph not allowed", errors)
    require(owners.get("approval_center") == "existing_canonical_owner", "parallel Approval Center not allowed", errors)
    require(owners.get("proof_ledger") == "existing_canonical_owner", "parallel Proof Ledger not allowed", errors)
    require(owners.get("scheduler") == "existing_canonical_owner_only", "duplicate scheduler not allowed", errors)
    require(owners.get("crm") == "mirror_only", "CRM must remain mirror-only", errors)

    required_inputs = set(contract.get("required_input_fields", []))
    require(
        "real_interaction_state" in required_inputs,
        "contract must require canonical real_interaction_state",
        errors,
    )

    truth = contract.get("truth_firewall", {})
    require(truth.get("research_is_relationship") is False, "research must not equal relationship", errors)
    require(truth.get("lead_row_is_consent") is False, "lead row must not equal consent", errors)
    require(truth.get("draft_is_sent") is False, "draft must not equal sent", errors)
    require(truth.get("proposal_is_revenue") is False, "proposal must not equal revenue", errors)
    require(truth.get("invoice_is_payment") is False, "invoice must not equal payment", errors)
    require(truth.get("delivery_is_customer_accepted_value") is False, "delivery must not equal accepted value", errors)
    require(truth.get("synthetic_is_customer_proof") is False, "synthetic must not equal customer proof", errors)
    require(truth.get("verified_payment_requires_external_payment_evidence") is True, "payment evidence gate missing", errors)
    require(truth.get("public_customer_proof_requires_permission") is True, "public proof permission gate missing", errors)

    packages = contract.get("packages", {})
    expected_packages = {
        "REVENUE_COMMAND_PILOT",
        "COMPANY_BRAIN_GOVERNED_AI_SPRINT",
        "SAUDI_MARKET_ACCESS_SPRINT",
        "PARTNER_IMPLEMENTATION_PROOF_LAYER",
    }
    require(set(packages) == expected_packages, "package portfolio drift", errors)
    for package_name in expected_packages:
        package = packages.get(package_name, {})
        require(bool(package.get("purpose")), f"missing purpose for {package_name}", errors)
        require(bool(package.get("entry_signals")), f"missing entry signals for {package_name}", errors)
        require(bool(package.get("required_before_paid_scope")), f"missing paid-scope gates for {package_name}", errors)
        require(bool(package.get("outputs")), f"missing outputs for {package_name}", errors)

    market_access = packages.get("SAUDI_MARKET_ACCESS_SPRINT", {})
    prohibited = set(market_access.get("prohibited_claims", []))
    for required in (
        "guaranteed_government_access",
        "guaranteed_tender_or_contract",
        "unverified_official_relationship",
    ):
        require(required in prohibited, f"missing prohibited market-access claim: {required}", errors)

    brain = packages.get("COMPANY_BRAIN_GOVERNED_AI_SPRINT", {})
    anti_scope = set(brain.get("anti_scope", []))
    for required in ("generic_chatbot", "unlimited_agent_build", "parallel_company_brain"):
        require(required in anti_scope, f"missing Company Brain anti-scope: {required}", errors)

    routing_rules = contract.get("routing_rules", [])
    routes = {rule.get("route") for rule in routing_rules}
    require(routes == expected_packages, "each package must have one routing rule", errors)
    priorities = [rule.get("priority") for rule in routing_rules]
    require(len(priorities) == len(set(priorities)), "routing priorities must be unique", errors)
    require(all(isinstance(priority, int) for priority in priorities), "routing priorities must be integers", errors)

    output_contract = set(contract.get("router_output_contract", []))
    for required in (
        "recommended_package",
        "routing_reason",
        "confidence",
        "input_evidence_refs",
        "missing_evidence",
        "next_evidence_required",
        "next_action",
        "owner",
        "sla",
        "expiry",
        "authority_class",
        "risk_class",
    ):
        require(required in output_contract, f"missing router output field: {required}", errors)

    constraints = contract.get("decision_constraints", {})
    require(constraints.get("router_may_create_relationship_truth") is False, "router must not create relationship truth", errors)
    require(constraints.get("router_may_create_consent") is False, "router must not create consent", errors)
    require(constraints.get("router_may_create_payment_truth") is False, "router must not create payment truth", errors)
    require(constraints.get("router_may_create_customer_proof") is False, "router must not create customer proof", errors)
    require(constraints.get("router_may_commit_price_or_contract") is False, "router must not commit commercial terms", errors)
    require(constraints.get("router_may_auto_send_external_message") is False, "router must not auto-send", errors)
    require(constraints.get("router_may_rank_and_prepare_internal_work") is True, "router must support internal preparation", errors)

    fallback = contract.get("fallback_rules", {})
    require(fallback.get("no_evidence") == "RESEARCH_ONLY", "no-evidence fallback must remain research-only", errors)
    require(fallback.get("no_permission_for_direct_marketing") == "SUPPRESS_EXTERNAL_OUTREACH", "direct-marketing permission fallback missing", errors)
    require(fallback.get("opted_out") == "SUPPRESSED", "opt-out suppression missing", errors)

    wip = contract.get("president_wip", {})
    require(wip.get("max_company_p0s") == 3, "President P0 WIP must stay at 3", errors)
    require(wip.get("max_active_build_prs_per_owner") == 2, "build PR WIP drift", errors)
    require(wip.get("max_experiments_per_funnel_stage") == 1, "experiment WIP drift", errors)

    router = PortfolioPackageRouter()

    research = router.route(
        DemandSignal(
            signal_id="verify-research-only",
            company_name="Research Account",
            observed_at="2026-08-29T10:00:00+00:00",
            source_ref="crm://public-research/1",
            real_interaction_state="UNKNOWN",
            relationship_state="VERIFIED_RELATIONSHIP",
            problem_tags=["revenue"],
            problem_statement="Revenue follow-up gap",
            urgency="HIGH",
            economic_relevance="HIGH",
        )
    )
    require(research.status == "RESEARCH_ONLY", "public/CRM research must stay research-only", errors)
    require(research.relationship_state == UNKNOWN, "source row must not create verified relationship", errors)
    require(research.recommended_package == EntryPackage.RESEARCH_NURTURE_SUPPRESS, "research row must not package-route", errors)

    raw_ref = router.route(
        DemandSignal(
            signal_id="verify-raw-ref-only",
            company_name="Raw Ref Account",
            observed_at="2026-08-29T10:00:00+00:00",
            source_ref="source://1",
            real_interaction_state="UNKNOWN",
            real_interaction_ref="interaction://1",
            problem_tags=["revenue"],
            problem_statement="Revenue follow-up gap",
            urgency="HIGH",
            economic_relevance="HIGH",
        )
    )
    require(raw_ref.status == "RESEARCH_ONLY", "raw interaction ref without canonical state must remain research-only", errors)
    require(raw_ref.relationship_state == UNKNOWN, "raw interaction ref must not create interaction/relationship truth", errors)
    require("RAW_INTERACTION_REFERENCE_NOT_CANONICAL_STATE" in raw_ref.reason_codes, "raw ref rejection reason missing", errors)

    interaction = router.route(
        DemandSignal(
            signal_id="verify-interaction-state",
            company_name="Interaction Account",
            observed_at="2026-08-29T10:00:00+00:00",
            source_ref="source://1",
            real_interaction_state="REAL_INTERACTION",
            real_interaction_ref="interaction://1",
            relationship_state=UNKNOWN,
            problem_tags=["revenue"],
            problem_statement="Revenue follow-up gap",
            urgency="HIGH",
            economic_relevance="HIGH",
        )
    )
    require(interaction.relationship_state == INTERACTION_EVIDENCE_PRESENT, "canonical interaction state+ref must remain below relationship truth", errors)
    require(interaction.authority.get("relationship") is False, "router must not grant relationship authority", errors)
    require(interaction.authority.get("external_send") is False, "router must not grant send authority", errors)

    mismatched = router.route(
        DemandSignal(
            signal_id="verify-mismatched-state",
            company_name="Mismatched Account",
            observed_at="2026-08-29T10:00:00+00:00",
            source_ref="source://1",
            real_interaction_state="EXPLICIT_INBOUND",
            real_interaction_ref="interaction://wrong-kind",
            explicit_inbound_ref="",
            problem_tags=["revenue"],
            problem_statement="Revenue follow-up gap",
            urgency="HIGH",
            economic_relevance="HIGH",
        )
    )
    require(mismatched.status == "RESEARCH_ONLY", "mismatched interaction state/reference must fail closed", errors)

    verified = router.route(
        DemandSignal(
            signal_id="verify-relationship",
            company_name="Verified Account",
            observed_at="2026-08-29T10:00:00+00:00",
            source_ref="source://1",
            real_interaction_state="REAL_INTERACTION",
            real_interaction_ref="interaction://1",
            relationship_state="VERIFIED_RELATIONSHIP",
            problem_tags=["revenue"],
            problem_statement="Revenue follow-up gap",
            urgency="HIGH",
            economic_relevance="HIGH",
        )
    )
    require(verified.relationship_state == "VERIFIED_RELATIONSHIP", "canonical verified relationship plus canonical interaction evidence must be preserved", errors)
    require(all(value is False for value in verified.authority.values()), "package router must grant no downstream authority", errors)

    if errors:
        print("DEALIX_PACKAGE_ROUTER_VERDICT=FAIL")
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("DEALIX_PACKAGE_ROUTER_VERDICT=PASS")
    print(f"SCHEMA={contract['schema']}")
    print("PACKAGES=4")
    print("REAL_INTERACTION_STATE_CONTRACT=ENFORCED")
    print("RAW_INTERACTION_REF_TRUTH_PROMOTION=BLOCKED")
    print("ROUTER_RELATIONSHIP_PROMOTION=BLOCKED")
    print("EXTERNAL_AUTO_SEND=BLOCKED")
    print("PRICE_OR_CONTRACT_COMMIT=BLOCKED")
    print("NO_EVIDENCE_FALLBACK=RESEARCH_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
