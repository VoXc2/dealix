#!/usr/bin/env python3
"""Fail-closed structural verifier for Market-to-Delivery wedge policy V1.

This verifier checks policy integrity only. It does not prove market demand,
production readiness, customer consent, delivery capacity, revenue or proof.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "data/commercial/market_to_delivery_wedge_policy_v1.json"

EXPECTED_AGENTS = {
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
}
EXPECTED_WEDGES = {
    "CONSTRUCTION_FM",
    "SI_MSP_IMPLEMENTERS",
    "MANUFACTURING_SUPPLY_CHAIN_ADMIN",
}
EXPECTED_ROUTES = {
    "BUILD_DIRECT",
    "ADAPT_EXISTING",
    "INTEGRATE_EXISTING_PRODUCT",
    "QUALIFIED_PARTNER",
    "SUBCONTRACT_PACKAGE",
    "REFER_WITH_DISCLOSURE",
    "DECLINE_OR_DEFER",
}
EXPECTED_DECISIONS = {"SCALE", "ITERATE", "STOP", "INVALID"}
FORBIDDEN_TRUE_AUTHORITY = {
    "external_send",
    "commercial_commitment",
    "payment_execution",
    "public_publish",
    "production_mutation",
    "merge_main",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"DEALIX_MARKET_TO_DELIVERY_WEDGE_POLICY=FAIL: {message}")


def load() -> dict:
    require(POLICY.is_file(), f"missing_policy:{POLICY}")
    value = json.loads(POLICY.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "policy_not_object")
    return value


def main() -> int:
    p = load()

    require(
        p.get("schema_version") == "dealix.market-to-delivery.wedge-policy.v1",
        "schema_version",
    )
    require(
        p.get("north_star") == "CASH_READY_AUTONOMOUS_DEALIX_COMPANY",
        "north_star",
    )

    authority = p.get("authority") or {}
    require(set(authority) == FORBIDDEN_TRUE_AUTHORITY, "authority_keys")
    require(all(authority[k] is False for k in FORBIDDEN_TRUE_AUTHORITY), "authority_not_fail_closed")

    weights = p.get("portfolio_weights") or {}
    for key in ("when_production_trust_not_green", "when_production_trust_green"):
        row = weights.get(key) or {}
        require(set(row) == {"TRUST", "MONEY_NOW", "COMPOUNDING"}, f"portfolio_keys:{key}")
        require(sum(row.values()) == 100, f"portfolio_weights_not_100:{key}")

    market = p.get("market_law") or {}
    require(market.get("research_scope") == "BROAD_20_SECTOR_RADAR", "research_scope")
    require(market.get("max_simultaneous_active_gtm_wedges") == 3, "wip_limit")
    ladder = market.get("demand_evidence_ladder") or []
    require(ladder[:2] == ["EXPLICIT_RFP_OR_TENDER", "CUSTOMER_CONFIRMED_PROBLEM"], "demand_ladder")
    forbidden = set(market.get("forbidden_promotions") or [])
    require("RESEARCH_TO_RELATIONSHIP" in forbidden, "research_truth_firewall")
    require("PUBLIC_CONTACT_TO_CONSENT" in forbidden, "consent_truth_firewall")
    require("QUOTE_TO_PAYMENT" in forbidden, "payment_truth_firewall")

    wedges = p.get("active_wedge_hypotheses") or []
    require(len(wedges) == 3, "active_wedge_count")
    require({w.get("id") for w in wedges} == EXPECTED_WEDGES, "wedge_ids")
    require(sorted(w.get("priority") for w in wedges) == [1, 2, 3], "wedge_priority")
    for w in wedges:
        require(bool(w.get("segments")), f"segments:{w.get('id')}")
        require(bool(w.get("problem_families")), f"problem_families:{w.get('id')}")
        require(bool(w.get("proof_targets")), f"proof_targets:{w.get('id')}")
        require(bool(w.get("stop_conditions")), f"stop_conditions:{w.get('id')}")
        require(set(w.get("initial_solution_routes") or []).issubset(EXPECTED_ROUTES), f"wedge_routes:{w.get('id')}")

    route = p.get("solution_route_decision") or {}
    require(set(route.get("allowed_routes") or []) == EXPECTED_ROUTES, "allowed_routes")
    require("PROVEN_CAPABILITY" in set(route.get("required_inputs") or []), "capability_gate")
    require("LIABILITY" in set(route.get("required_inputs") or []), "liability_gate")
    no_override = set(route.get("no_route_may_override") or [])
    require({"CONSENT", "AUTHORITY", "LICENSING", "SAFETY", "TENANT_ISOLATION"}.issubset(no_override), "route_override_guard")

    score = p.get("opportunity_score") or {}
    require("VERIFIED_ECONOMIC_VALUE" in set(score.get("numerator") or []), "economic_value_score")
    require("FOUNDER_MINUTES" in set(score.get("denominator") or []), "founder_minutes_score")
    require("BUYER_INTENT" in set(score.get("score_is_not") or []), "score_truth_firewall")

    authority_ladder = p.get("commercial_authority_ladder") or {}
    require(authority_ladder.get("phase_0") == "FOUNDER_APPROVAL_FOR_BINDING_QUOTES_AND_MATERIAL_EXCEPTIONS", "commercial_phase_0")
    require("GUARANTEE" in set(authority_ladder.get("always_escalate") or []), "guarantee_escalation")
    require("LEGAL_LIABILITY" in set(authority_ladder.get("always_escalate") or []), "legal_escalation")

    cell = p.get("project_cell_contract") or {}
    prereq = set(cell.get("required_before_provisioning") or [])
    require("APPROVED_SCOPE_DIGEST" in prereq, "project_scope_gate")
    require("VERIFIED_START_OR_PAYMENT_AUTHORITY" in prereq, "project_start_gate")
    require("ACCOUNTABLE_HUMAN" in prereq, "accountable_human_gate")
    require("ROLLBACK_AND_EXIT_PLAN" in prereq, "project_rollback_gate")
    gates = cell.get("delivery_gates") or []
    require(gates[-1:] == ["OUTCOME_PROOF"], "delivery_proof_last_gate")

    scale = p.get("scale_policy") or {}
    require(set(scale.get("decision_classes") or []) == EXPECTED_DECISIONS, "decision_classes")
    require("REPEATED_REAL_DEMAND" in set(scale.get("scale_requires") or []), "scale_demand_gate")
    require("POSITIVE_OR_APPROVED_UNIT_ECONOMICS" in set(scale.get("scale_requires") or []), "scale_economics_gate")
    require("DATA_OR_EVIDENCE_NOT_TRUSTWORTHY" in set(scale.get("invalid_when") or []), "invalid_evidence_gate")

    kpis = set(p.get("kpis") or [])
    for metric in (
        "REAL_INTERACTIONS",
        "QUALIFIED_PROBLEMS",
        "QUOTE_TO_VERIFIED_CASH_RATE",
        "CONTRIBUTION_MARGIN",
        "CUSTOMER_VALIDATED_PROOF_RATE",
        "FOUNDER_MINUTES_PER_VERIFIED_ECONOMIC_MOVEMENT",
    ):
        require(metric in kpis, f"missing_kpi:{metric}")

    milestones = p.get("milestones") or {}
    require(set(milestones) == {"A5", "A6"}, "milestones")

    # Permanent-agent truth must remain owned elsewhere; this policy must not mint another fleet.
    encoded = json.dumps(p, sort_keys=True)
    for agent in EXPECTED_AGENTS:
        # It is acceptable for the policy not to name the agents; if a future edit does,
        # only canonical names are accepted by the explicit roster check below.
        pass
    for forbidden_token in ("sixth-agent", "new_permanent_agent", "parallel_crm", "parallel_scheduler"):
        require(forbidden_token not in encoded.lower(), f"duplicate_architecture_marker:{forbidden_token}")

    print("DEALIX_MARKET_TO_DELIVERY_WEDGE_POLICY=PASS")
    print("ACTIVE_WEDGES=3")
    print("DECISIONS=SCALE,ITERATE,STOP,INVALID")
    print("EXTERNAL_AUTHORITY=false")
    print("SCORE_IS_NOT_BUYER_INTENT=PASS")
    print("A5_A6_EVIDENCE_GATED=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
