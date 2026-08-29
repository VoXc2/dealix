#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "data/ops/capability_radar_20260828.json"
NORTH_STAR = "CASH_READY_AUTONOMOUS_DEALIX_COMPANY"
PRIMARY_METRIC = "VERIFIED_ECONOMIC_MOVEMENT_PER_FOUNDER_MINUTE_PER_COST_PER_RISK"

ALLOWED_DECISIONS = {"ADOPT_NOW", "ADOPT_NOW_BOUNDED", "ADOPT_FOR_ACCEPTANCE", "PILOT_ISOLATED", "DEFER", "REJECT_DUPLICATE", "REJECT_POLICY"}
REQUIRED_REJECTIONS = {
    "new_crm": "REJECT_DUPLICATE",
    "new_vector_db_as_company_brain": "REJECT_DUPLICATE",
    "new_agent_framework_fleet": "REJECT_DUPLICATE",
    "new_workflow_scheduler": "REJECT_DUPLICATE",
    "generic_autonomous_sdr_bots": "REJECT_POLICY",
    "linkedin_browser_bots": "REJECT_POLICY",
}
REQUIRED_BOUNDED = {"hubspot_remote_mcp", "n8n_mcp_workflow_authoring", "openai_realtime_sip_remote_mcp", "openai_agents_sdk_isolated_harness", "otel_genai_semantics", "openfeature_kill_switch", "promptfoo_agent_redteam", "docling_document_ingestion", "schemathesis_api_acceptance"}


def main() -> int:
    payload = json.loads(PATH.read_text(encoding="utf-8"))
    failures: list[str] = []

    if payload.get("schema") != "dealix.capability_radar.v1":
        failures.append("schema mismatch")
    if payload.get("north_star") != NORTH_STAR:
        failures.append("north star drift")
    if payload.get("primary_metric") != PRIMARY_METRIC:
        failures.append("primary metric drift")
    if payload.get("owner_agent") != "dealix-pm":
        failures.append("capability radar must be owned by canonical dealix-pm")
    if payload.get("owner_workload") != "capability_research":
        failures.append("capability research must be a workload, not a permanent agent")
    if set(payload.get("decision_values", [])) != ALLOWED_DECISIONS:
        failures.append("decision vocabulary drift")

    candidates = payload.get("candidates", [])
    if not isinstance(candidates, list):
        failures.append("candidates must be a list")
        candidates = []
    by_id = {row.get("id"): row for row in candidates if isinstance(row, dict) and isinstance(row.get("id"), str)}

    for candidate_id, expected in REQUIRED_REJECTIONS.items():
        row = by_id.get(candidate_id)
        if not row:
            failures.append(f"missing required rejection: {candidate_id}")
        elif row.get("decision") != expected:
            failures.append(f"{candidate_id} must remain {expected}")

    for candidate_id in REQUIRED_BOUNDED:
        row = by_id.get(candidate_id)
        if not row:
            failures.append(f"missing bounded candidate: {candidate_id}")
            continue
        if row.get("decision") not in {"ADOPT_NOW_BOUNDED", "PILOT_ISOLATED"}:
            failures.append(f"{candidate_id} lost bounded adoption posture")

    playwright = by_id.get("playwright_acceptance", {})
    if playwright.get("decision") != "ADOPT_FOR_ACCEPTANCE":
        failures.append("Playwright must remain acceptance-only")
    if "academy.html" not in str(playwright.get("admission_evidence", "")):
        failures.append("Playwright admission must remain tied to proven public-surface drift")

    linkedin = by_id.get("linkedin_browser_bots", {})
    if "linkedin.com/legal/user-agreement" not in str(linkedin.get("source", "")):
        failures.append("LinkedIn rejection must remain source-bound")

    hubspot = by_id.get("hubspot_remote_mcp", {})
    if hubspot.get("decision") != "ADOPT_NOW_BOUNDED":
        failures.append("HubSpot MCP must remain bounded")

    realtime = by_id.get("openai_realtime_sip_remote_mcp", {})
    if not any("impersonate" in str(value).lower() for value in realtime.get("blocked", [])):
        failures.append("Voice pilot must block founder impersonation")

    otel = by_id.get("otel_genai_semantics", {})
    if otel.get("decision") != "ADOPT_NOW_BOUNDED":
        failures.append("OpenTelemetry must remain bounded adoption")
    if otel.get("implementation_state") != "BOUNDED_IMPLEMENTATION_ON_MAIN":
        failures.append("OpenTelemetry implementation evidence missing")
    otel_blocked = " ".join(str(value).lower() for value in otel.get("blocked", []))
    if "prompts" not in otel_blocked or "approval" not in otel_blocked:
        failures.append("OTel must keep content private and never become approval authority")

    openfeature = by_id.get("openfeature_kill_switch", {})
    if openfeature.get("decision") != "ADOPT_NOW_BOUNDED":
        failures.append("OpenFeature integrated kill-switch must remain bounded adoption")
    if openfeature.get("implementation_state") != "BOUNDED_IMPLEMENTATION_ON_MAIN":
        failures.append("OpenFeature implementation evidence missing")
    openfeature_blocked = " ".join(str(value).lower() for value in openfeature.get("blocked", []))
    if "grant authority" not in openfeature_blocked or "payment" not in openfeature_blocked:
        failures.append("OpenFeature must never mint authority/commercial side effects")

    promptfoo = by_id.get("promptfoo_agent_redteam", {})
    promptfoo_blocked = " ".join(str(value).lower() for value in promptfoo.get("blocked", []))
    if "write-capable credentials" not in promptfoo_blocked:
        failures.append("Promptfoo must block untrusted config with write-capable credentials")
    if "local user permissions" not in str(promptfoo.get("security_model", "")).lower():
        failures.append("Promptfoo security model must record local-code execution risk")

    docling = by_id.get("docling_document_ingestion", {})
    if not any("parallel company brain" in str(value).lower() for value in docling.get("blocked", [])):
        failures.append("Docling must not become a parallel Company Brain")

    schemathesis = by_id.get("schemathesis_api_acceptance", {})
    if not any("production" in str(value).lower() for value in schemathesis.get("blocked", [])):
        failures.append("Schemathesis must remain off destructive production fuzzing")

    custom_agents = by_id.get("github_custom_agents", {})
    if custom_agents.get("decision") != "DEFER":
        failures.append("GitHub custom-agent roster must remain deferred as duplicate")
    if not any("duplicate canonical agent roster" in str(value).lower() for value in custom_agents.get("blocked", [])):
        failures.append("GitHub custom-agent duplicate-roster guard missing")

    agentic = by_id.get("github_agentic_workflows_repo_ops", {})
    if agentic.get("decision") != "DEFER":
        failures.append("GitHub Agentic Workflows must remain deferred until runner evidence")
    if "runner" not in str(agentic.get("entry_gate", "")).lower():
        failures.append("GitHub Agentic Workflows entry gate must require reliable runner evidence")
    agentic_blocked = " ".join(str(value).lower() for value in agentic.get("blocked", []))
    if "second scheduler" not in agentic_blocked or "second verification" not in agentic_blocked:
        failures.append("GitHub Agentic Workflows must not duplicate scheduler/verification ownership")

    langfuse = by_id.get("langfuse_legacy_adapter", {})
    if langfuse.get("decision") != "DEFER":
        failures.append("Langfuse legacy adapter must remain contained/deferred")
    if not any("second truth store" in str(value).lower() for value in langfuse.get("blocked", [])):
        failures.append("Langfuse must not expand as a second truth store")

    non_roi = set(payload.get("non_roi_metrics", []))
    for metric in {"number_of_agents", "number_of_workflows", "token_volume", "vanity_engagement"}:
        if metric not in non_roi:
            failures.append(f"non-ROI metric missing: {metric}")

    canonical = payload.get("canonical_owners", {})
    if canonical.get("crm_truth") != "Dealix Company OS; HubSpot mirror only":
        failures.append("CRM truth ownership drift")
    if "revenue_growth_autopilot_contract.json" not in str(canonical.get("commercial_autopilot", "")):
        failures.append("Commercial Autopilot must use current stable contract path")
    if "Governance OS" not in str(canonical.get("channel_go_live", "")):
        failures.append("Channel go-live must remain governance/authority owned")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print("DEALIX_CAPABILITY_RADAR=FAIL")
        return 1

    print("DEALIX_CAPABILITY_RADAR=PASS")
    print(f"NORTH_STAR={NORTH_STAR}")
    print(f"PRIMARY_METRIC={PRIMARY_METRIC}")
    print("OWNER=dealix-pm")
    print("CAPABILITY_RESEARCH=WORKLOAD_NOT_AGENT")
    print("DUPLICATE_FRAMEWORK_EXPANSION=BLOCKED")
    print("OTEL=ADOPT_NOW_BOUNDED_IMPLEMENTED")
    print("OPENFEATURE=ADOPT_NOW_BOUNDED_IMPLEMENTED")
    print("PLAYWRIGHT=ADOPT_FOR_ACCEPTANCE")
    print("GITHUB_CUSTOM_AGENTS=DEFER_DUPLICATE_ROSTER")
    print("GITHUB_AGENTIC_WORKFLOWS=DEFER_RUNNER_PLANE")
    print("PROMPTFOO=PILOT_ISOLATED")
    print("DOCLING=PILOT_ISOLATED")
    print("SCHEMATHESIS=PILOT_ISOLATED")
    print("LANGFUSE_LEGACY=DEFER_CONTAIN_MIGRATE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
