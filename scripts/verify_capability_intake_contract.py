#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "ops" / "capability_intake_contract.json"
RADAR = ROOT / "data" / "ops" / "capability_radar_20260828.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"CAPABILITY_INTAKE_VERIFY=FAIL\nREASON={message}")


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    radar = json.loads(RADAR.read_text(encoding="utf-8"))

    require(contract["schema"] == "dealix.capability-intake.v1", "wrong intake schema")
    require(contract["north_star"] == "FIRST_VERIFIED_PAID_PILOT", "wrong north star")
    require(radar["north_star"] == contract["north_star"], "radar/intake north-star drift")

    hard_reject = set(contract["hard_reject"])
    for required in {
        "creates_parallel_company_brain",
        "creates_parallel_opportunity_graph",
        "creates_parallel_approval_center",
        "creates_parallel_proof_ledger",
        "creates_parallel_crm_truth",
        "creates_parallel_scheduler",
        "creates_parallel_permanent_agent_fleet",
        "enables_cold_bulk_whatsapp",
        "enables_unauthorized_linkedin_automation",
        "can_self_issue_payment_or_external_execution_authority",
    }:
        require(required in hard_reject, f"missing hard reject: {required}")

    dimensions = contract["score"]["dimensions"]
    require(sum(dimensions.values()) == 100, "positive scoring dimensions must sum to 100")
    require(contract["score"]["penalties"]["duplicates_existing_owner"] <= -100, "duplicate owner must hard fail")
    require(contract["score"]["penalties"]["requires_unbounded_external_authority"] <= -100, "unbounded authority must hard fail")

    pilot = contract["pilot_contract"]
    require(pilot["production_mutation"] is False, "isolated pilot cannot mutate production")
    require(pilot["external_customer_send"] is False, "isolated pilot cannot send externally")
    require(pilot["payment_or_spend"] is False, "isolated pilot cannot spend/charge")
    require(pilot["new_truth_owner"] is False, "isolated pilot cannot create truth owner")

    loop = contract["agent_loop"]
    require("no new timer" in loop["frequency"], "capability radar must reuse existing cadence")
    require(loop["max_isolated_pilots_concurrent"] <= 2, "too many concurrent capability pilots")
    require(loop["priority"][0] == "current_verified_blocker", "verified blockers must outrank novelty")
    require("first_paid_pilot_conversion" in loop["priority"], "revenue conversion missing from priority")

    patterns = contract["current_high_value_patterns"]
    require(patterns["playwright_test_agents"]["decision"] == "ADOPT_FOR_ACCEPTANCE", "Playwright decision drift")
    require(patterns["promptfoo_agent_mcp_eval"]["decision"] == "PILOT_ISOLATED", "Promptfoo decision drift")
    require(patterns["otel_semantic_conventions"]["decision"] == "PILOT_ISOLATED", "OTel decision drift")
    require(patterns["otel_semantic_conventions"]["privacy_default"].startswith("no prompt"), "OTel privacy default must fail closed")

    radar_candidates = {c["id"]: c for c in radar["candidates"]}
    for candidate in [
        "playwright_acceptance",
        "osv_scanner_v2",
        "uv_uvx",
        "otel_genai_semantics",
        "new_crm",
        "new_agent_framework_fleet",
        "new_workflow_scheduler",
        "linkedin_browser_bots",
    ]:
        require(candidate in radar_candidates, f"missing radar candidate: {candidate}")

    require(radar_candidates["new_crm"]["decision"] == "REJECT_DUPLICATE", "new CRM must remain rejected")
    require(radar_candidates["new_agent_framework_fleet"]["decision"] == "REJECT_DUPLICATE", "parallel agent fleet must remain rejected")
    require(radar_candidates["new_workflow_scheduler"]["decision"] == "REJECT_DUPLICATE", "parallel scheduler must remain rejected")
    require(radar_candidates["linkedin_browser_bots"]["decision"] == "REJECT_POLICY", "LinkedIn bots must remain rejected")

    print("DEALIX_CAPABILITY_INTAKE=PASS")
    print("NORTH_STAR=FIRST_VERIFIED_PAID_PILOT")
    print("NEW_TIMER=0")
    print("NEW_TRUTH_OWNER=0")
    print("MAX_ISOLATED_PILOTS=2")
    print("PLAYWRIGHT_TEST_AGENTS=ADOPT_FOR_ACCEPTANCE")
    print("PROMPTFOO_AGENT_MCP_EVAL=PILOT_ISOLATED")
    print("OTEL_SEMCONV=PILOT_ISOLATED")
    print("DUPLICATE_ARCHITECTURE=REJECT")


if __name__ == "__main__":
    main()
