#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/commercial/autonomous_portfolio_contract_v1.json"
ROUTER = ROOT / "dealix/commercial/portfolio_router.py"
SPRINT = ROOT / "dealix/commercial/company_brain_sprint.py"


def main() -> int:
    payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
    if payload.get("schema") != "dealix.autonomous-portfolio.v1":
        raise SystemExit("DEALIX_AUTONOMOUS_PORTFOLIO=FAIL:schema")
    architecture = payload.get("architecture", {})
    for key in ("company_brain", "opportunity_graph", "approval_center", "proof_ledger", "scheduler"):
        if architecture.get(key) != "reuse_existing":
            raise SystemExit(f"DEALIX_AUTONOMOUS_PORTFOLIO=FAIL:duplicate:{key}")
    if architecture.get("new_permanent_agents") != 0:
        raise SystemExit("DEALIX_AUTONOMOUS_PORTFOLIO=FAIL:agent_growth")

    truth = payload.get("truth_invariants", {})
    for key in (
        "research_is_relationship",
        "route_is_offer",
        "route_is_quote",
        "route_is_send_authority",
        "route_is_execution_authority",
        "source_context_is_customer_validation",
        "synthetic_is_customer_proof",
    ):
        if truth.get(key) is not False:
            raise SystemExit(f"DEALIX_AUTONOMOUS_PORTFOLIO=FAIL:truth:{key}")
    if truth.get("payment_requires_canonical_proof") is not True:
        raise SystemExit("DEALIX_AUTONOMOUS_PORTFOLIO=FAIL:payment_truth")

    router = ROUTER.read_text(encoding="utf-8")
    sprint = SPRINT.read_text(encoding="utf-8")
    for marker in (
        "COMPANY_BRAIN_GOVERNED_AI_SPRINT",
        "SAUDI_MARKET_ACCESS_SPRINT",
        "PARTNER_IMPLEMENTATION_PROOF_LAYER",
        '"external_send": False',
        '"quote": False',
    ):
        if marker not in router:
            raise SystemExit(f"DEALIX_AUTONOMOUS_PORTFOLIO=FAIL:router:{marker}")
    for marker in (
        "one bounded sprint",
        '"deployment": False',
        '"customer_value_claim": False',
        "customer_validation_ref",
        "permission_ref",
    ):
        if marker not in sprint:
            raise SystemExit(f"DEALIX_AUTONOMOUS_PORTFOLIO=FAIL:sprint:{marker}")

    print("DEALIX_AUTONOMOUS_PORTFOLIO=PASS")
    print("NEW_PERMANENT_AGENTS=0")
    print("NEW_SCHEDULERS=0")
    print("ROUTING_CREATES_AUTHORITY=NO")
    print("COMPANY_BRAIN_SPRINT_REUSES_CANONICAL_BRAIN=YES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
