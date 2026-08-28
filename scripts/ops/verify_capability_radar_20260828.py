#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "data/ops/capability_radar_20260828.json"

ALLOWED_DECISIONS = {
    "ADOPT_NOW",
    "ADOPT_NOW_BOUNDED",
    "ADOPT_FOR_ACCEPTANCE",
    "PILOT_ISOLATED",
    "DEFER",
    "REJECT_DUPLICATE",
    "REJECT_POLICY",
}

REQUIRED_REJECTIONS = {
    "new_crm": "REJECT_DUPLICATE",
    "new_vector_db_as_company_brain": "REJECT_DUPLICATE",
    "new_agent_framework_fleet": "REJECT_DUPLICATE",
    "new_workflow_scheduler": "REJECT_DUPLICATE",
    "generic_autonomous_sdr_bots": "REJECT_POLICY",
    "linkedin_browser_bots": "REJECT_POLICY",
}

REQUIRED_BOUNDED = {
    "hubspot_remote_mcp",
    "n8n_mcp_workflow_authoring",
    "openai_realtime_sip_remote_mcp",
    "openai_agents_sdk_isolated_harness",
    "otel_genai_semantics",
}


def main() -> int:
    payload = json.loads(PATH.read_text(encoding="utf-8"))
    failures: list[str] = []

    if payload.get("schema") != "dealix.capability_radar.v1":
        failures.append("schema mismatch")
    if payload.get("north_star") != "FIRST_VERIFIED_PAID_PILOT":
        failures.append("north star drift")
    if payload.get("owner_agent") != "capability-research":
        failures.append("capability-research must own radar")

    decisions = set(payload.get("decision_values", []))
    if decisions != ALLOWED_DECISIONS:
        failures.append("decision vocabulary drift")

    candidates = payload.get("candidates", [])
    if not isinstance(candidates, list):
        failures.append("candidates must be a list")
        candidates = []

    by_id = {
        row.get("id"): row
        for row in candidates
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }

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

    linkedin = by_id.get("linkedin_browser_bots", {})
    if "linkedin.com/legal/user-agreement" not in str(linkedin.get("source", "")):
        failures.append("LinkedIn rejection must remain source-bound")

    hubspot = by_id.get("hubspot_remote_mcp", {})
    if hubspot.get("decision") != "ADOPT_NOW_BOUNDED":
        failures.append("HubSpot MCP must remain bounded")
    if not any("#1294" in str(value) for value in [hubspot.get("entry_gate", ""), *hubspot.get("blocked", [])]):
        failures.append("HubSpot MCP must remain behind #1294 truth gates")

    realtime = by_id.get("openai_realtime_sip_remote_mcp", {})
    if not any("impersonate" in str(value).lower() for value in realtime.get("blocked", [])):
        failures.append("Voice pilot must block founder impersonation")

    non_roi = set(payload.get("non_roi_metrics", []))
    for metric in {"number_of_agents", "number_of_workflows", "token_volume", "vanity_engagement"}:
        if metric not in non_roi:
            failures.append(f"non-ROI metric missing: {metric}")

    canonical = payload.get("canonical_owners", {})
    if canonical.get("crm_truth") != "Dealix Company OS; HubSpot mirror only":
        failures.append("CRM truth ownership drift")
    if canonical.get("commercial_autopilot") != "PR #1307":
        failures.append("Commercial Autopilot owner drift")
    if canonical.get("channel_go_live") != "Issue #1299":
        failures.append("Channel go-live owner drift")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print("DEALIX_CAPABILITY_RADAR=FAIL")
        return 1

    print("DEALIX_CAPABILITY_RADAR=PASS")
    print("NORTH_STAR=FIRST_VERIFIED_PAID_PILOT")
    print("DUPLICATE_FRAMEWORK_EXPANSION=BLOCKED")
    print("BOUND_ADOPTION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
