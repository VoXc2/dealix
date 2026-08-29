#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/commercial/revenue_growth_economics_overlay.json"


def fail(msg: str) -> None:
    raise SystemExit(f"DEALIX_REVENUE_GROWTH_ECONOMICS=FAIL:{msg}")


def main() -> int:
    payload = json.loads(PATH.read_text(encoding="utf-8"))
    if payload.get("north_star") != "FIRST_VERIFIED_PAID_PILOT":
        fail("north_star")

    truth = payload.get("truth_boundary", {})
    for key in (
        "ranking_only",
        "cannot_promote_relationship",
        "cannot_promote_stage",
        "cannot_create_consent",
        "cannot_create_payment",
        "cannot_create_revenue",
        "cannot_create_customer_proof",
    ):
        if truth.get(key) is not True:
            fail(f"truth_boundary:{key}")
    if truth.get("missing_evidence_value") != "UNKNOWN_NOT_EVIDENCE_BACKED":
        fail("unknown_truth_value")

    aliases = payload.get("alias_rules", {})
    if aliases.get("aliases_are_workload_labels_not_agents") is not True:
        fail("alias_semantics")
    if aliases.get("new_permanent_agents") != 0 or aliases.get("new_schedulers") != 0:
        fail("agent_or_scheduler_growth")
    if aliases.get("alias_cannot_expand_authority") is not True:
        fail("alias_authority")

    ledger = payload.get("negotiation_concession_ledger", {})
    required = {"give", "get", "economic_cost", "strategic_value", "authority", "expiry", "evidence"}
    if set(ledger.get("required_fields", [])) != required:
        fail("concession_ledger_fields")
    rules = set(ledger.get("rules", []))
    if "NO_MATERIAL_GIVE_WITHOUT_RECIPROCAL_GET_UNLESS_SPECIFICALLY_APPROVED" not in rules:
        fail("give_get_rule")
    if "NO_AUTONOMOUS_FINAL_PRICE_OR_DISCOUNT" not in rules:
        fail("price_authority")

    output = set(ledger.get("required_output", []))
    expected_output = {"BEST_MOVE", "FALLBACK_MOVE", "DO_NOT_DO", "GIVE_GET", "EVIDENCE_GAP", "HANDOFF_TRIGGER", "NEXT_EVIDENCE"}
    if output != expected_output:
        fail("negotiation_output")

    exp = payload.get("experiment_contract", {})
    if exp.get("vanity_only_scaling_blocked") is not True:
        fail("vanity_scaling")
    if set(exp.get("decisions", [])) != {"SCALE", "RETEST", "HOLD", "STOP", "INVALID"}:
        fail("experiment_decisions")

    movement = payload.get("canonical_movement_order", [])
    if not movement or movement[0] != "REAL_INTERACTION" or "PAYMENT_PROOF" not in movement:
        fail("movement_order")

    print("DEALIX_REVENUE_GROWTH_ECONOMICS=PASS")
    print("RANKING_MUTATES_TRUTH=NO")
    print("NEW_PERMANENT_AGENTS=0")
    print("NEW_SCHEDULERS=0")
    print("NEGOTIATION_GIVE_GET=REQUIRED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
