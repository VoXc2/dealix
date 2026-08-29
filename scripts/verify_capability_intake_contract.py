#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "ops" / "capability_intake_contract.json"
RADAR = ROOT / "data" / "ops" / "capability_radar_20260828.json"
NORTH_STAR = "CASH_READY_AUTONOMOUS_DEALIX_COMPANY"
PRIMARY_METRIC = "VERIFIED_ECONOMIC_MOVEMENT_PER_FOUNDER_MINUTE_PER_COST_PER_RISK"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"CAPABILITY_INTAKE_VERIFY=FAIL\nREASON={message}")


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    radar = json.loads(RADAR.read_text(encoding="utf-8"))

    require(contract["schema"] == "dealix.capability-intake.v1", "wrong intake schema")
    require(contract["north_star"] == NORTH_STAR, "wrong portfolio objective")
    require(contract["primary_metric"] == PRIMARY_METRIC, "wrong primary metric")
    require(radar["north_star"] == contract["north_star"], "radar/intake north-star drift")
    require(radar["primary_metric"] == PRIMARY_METRIC, "radar/intake primary-metric drift")
    require(contract["owner"] == "dealix-pm", "capability intake must use canonical President agent")
    require(contract["owner_workload"] == "capability_research", "capability research must remain a workload")
    require(contract["decision_owner"] == "dealix-pm", "capability decision owner must be canonical President")

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
    for field in ("production_mutation", "external_customer_send", "payment_or_spend", "new_truth_owner"):
        require(pilot[field] is False, f"pilot boundary must keep {field}=false")

    loop = contract["agent_loop"]
    require("no new timer" in loop["frequency"], "capability radar must reuse existing cadence")
    require(loop["max_isolated_pilots_concurrent"] <= 2, "too many concurrent capability pilots")
    require(loop["priority"][0] == "current_verified_blocker", "verified blockers must outrank novelty")
    require("verified_economic_movement" in loop["priority"], "economic objective missing from priority")

    patterns = contract["current_high_value_patterns"]
    require(patterns["playwright_test_agents"]["decision"] == "ADOPT_FOR_ACCEPTANCE", "Playwright decision drift")
    require(patterns["promptfoo_agent_mcp_eval"]["decision"] == "PILOT_ISOLATED", "Promptfoo decision drift")
    require(patterns["otel_semantic_conventions"]["decision"] == "ADOPT_NOW_BOUNDED", "OTel posture drift")
    require(patterns["otel_semantic_conventions"]["implementation_state"] == "BOUNDED_IMPLEMENTATION_ON_MAIN", "OTel implementation evidence missing")
    require(patterns["otel_semantic_conventions"]["privacy_default"].startswith("no prompt"), "OTel privacy default must fail closed")
    require(patterns["openfeature_authority_lowering"]["decision"] == "ADOPT_NOW_BOUNDED", "OpenFeature posture drift")
    require(patterns["openfeature_authority_lowering"]["implementation_state"] == "BOUNDED_IMPLEMENTATION_ON_MAIN", "OpenFeature implementation evidence missing")
    require(patterns["docling_provenance_ingestion"]["decision"] == "PILOT_ISOLATED", "Docling decision drift")
    require(patterns["schemathesis_api_acceptance"]["decision"] == "PILOT_ISOLATED", "Schemathesis decision drift")
    require(patterns["github_custom_agents"]["decision"] == "DEFER", "GitHub custom agents must not duplicate roster")
    require(patterns["github_agentic_workflows"]["decision"] == "DEFER", "runnerless agentic workflows must remain deferred")

    radar_candidates = {row["id"]: row for row in radar["candidates"]}
    required_candidates = {
        "playwright_acceptance",
        "osv_scanner_v2",
        "uv_uvx",
        "otel_genai_semantics",
        "openfeature_kill_switch",
        "promptfoo_agent_redteam",
        "docling_document_ingestion",
        "schemathesis_api_acceptance",
        "github_custom_agents",
        "github_agentic_workflows_repo_ops",
        "new_crm",
        "new_agent_framework_fleet",
        "new_workflow_scheduler",
        "linkedin_browser_bots",
    }
    require(required_candidates.issubset(radar_candidates), "radar required candidates missing")

    require(radar_candidates["otel_genai_semantics"]["decision"] == "ADOPT_NOW_BOUNDED", "OTel radar posture drift")
    require(radar_candidates["openfeature_kill_switch"]["decision"] == "ADOPT_NOW_BOUNDED", "OpenFeature radar posture drift")
    require(radar_candidates["promptfoo_agent_redteam"]["decision"] == "PILOT_ISOLATED", "Promptfoo radar posture drift")
    require(radar_candidates["github_custom_agents"]["decision"] == "DEFER", "parallel GitHub agent roster must remain deferred")
    require(radar_candidates["github_agentic_workflows_repo_ops"]["decision"] == "DEFER", "agentic workflows must remain deferred until runner evidence")
    require(radar_candidates["new_crm"]["decision"] == "REJECT_DUPLICATE", "new CRM must remain rejected")
    require(radar_candidates["new_agent_framework_fleet"]["decision"] == "REJECT_DUPLICATE", "parallel agent fleet must remain rejected")
    require(radar_candidates["new_workflow_scheduler"]["decision"] == "REJECT_DUPLICATE", "parallel scheduler must remain rejected")
    require(radar_candidates["linkedin_browser_bots"]["decision"] == "REJECT_POLICY", "LinkedIn bots must remain rejected")

    print("DEALIX_CAPABILITY_INTAKE=PASS")
    print(f"NORTH_STAR={NORTH_STAR}")
    print(f"PRIMARY_METRIC={PRIMARY_METRIC}")
    print("OWNER=dealix-pm")
    print("CAPABILITY_RESEARCH=WORKLOAD_NOT_AGENT")
    print("NEW_TIMER=0")
    print("NEW_TRUTH_OWNER=0")
    print("MAX_ISOLATED_PILOTS=2")
    print("PLAYWRIGHT=ADOPT_FOR_ACCEPTANCE")
    print("OTEL=ADOPT_NOW_BOUNDED_IMPLEMENTED")
    print("OPENFEATURE=ADOPT_NOW_BOUNDED_IMPLEMENTED")
    print("PROMPTFOO=PILOT_ISOLATED")
    print("GITHUB_CUSTOM_AGENTS=DEFER_DUPLICATE_ROSTER")
    print("GITHUB_AGENTIC_WORKFLOWS=DEFER_RUNNER_PLANE")
    print("DUPLICATE_ARCHITECTURE=REJECT")


if __name__ == "__main__":
    main()
