#!/usr/bin/env python3
"""Fail-closed verifier for Dealix Meta-Operating System V2.

This verifier validates the machine-readable control kernel only. It does not
claim that optional future infrastructure (for example SPIFFE/SPIRE) is active.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config" / "company" / "dealix_meta_operating_system_v2.json"

CANONICAL_AGENTS = {
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
}

EXPECTED_OPPORTUNITY = [
    "RESEARCH_ONLY", "KNOWN", "INTERACTION", "QUALIFIED_PROBLEM",
    "DIAGNOSTIC", "DISCOVERY", "QUOTE_READY", "QUOTED",
    "PAYMENT_PENDING", "PAID", "DELIVERY", "PROOF", "EXPANSION",
]
EXPECTED_PRODUCTION = [
    "SOURCE_ACCEPTED", "BUILD_ACCEPTED", "RELEASE_CANDIDATE", "DEPLOYED",
    "HEALTHY", "RELEASE_PARITY_PROVEN", "BUSINESS_FLOW_PROVEN",
    "PRODUCTION_GREEN",
]
EXPECTED_FINANCIAL = [
    "OPPORTUNITY_VALUE", "QUOTE", "ACCEPTED_COMMERCIAL_TERMS", "INVOICE",
    "PAYMENT_REQUESTED", "PAYMENT_PENDING", "PAYMENT_VERIFIED",
    "CASH_AVAILABLE", "REVENUE_RECOGNITION_STATE",
]
REQUIRED_INVARIANTS = {
    "PERMANENT_AGENTS == 5",
    "DEEP_WIP <= 3",
    "PUBLIC_CONTACT != CONSENT",
    "QUOTE != PAYMENT",
    "PRODUCTION_GREEN_REQUIRES_CURRENT_EVIDENCE",
    "NO_CROSS_TENANT_ACCESS",
    "NO_AGENT_SELF_AUTHORITY",
    "NO_PUBLIC_LOCAL_LLM_ADMIN",
    "NO_SECRET_IN_REPO",
    "NO_DUPLICATE_CANONICAL_SCHEDULER",
}
REQUIRED_PLANES = {
    "INTELLIGENCE_PLANE",
    "CONTROL_PLANE",
    "EXECUTION_PLANE",
    "DATA_PLANE",
    "PROOF_PLANE",
}
REQUIRED_SECTIONS = [
    "LXXI", "LXXII", "LXXIII", "LXXIV", "LXXV", "LXXVI", "LXXVII",
    "LXXVIII", "LXXIX", "LXXX", "LXXXI", "LXXXII", "LXXXIII",
    "LXXXIV", "LXXXV", "LXXXVI", "LXXXVII", "LXXXVIII", "LXXXIX",
    "XC", "XCI", "XCII", "XCIII", "XCIV", "XCV", "XCVI", "XCVII",
    "XCVIII", "XCIX", "C", "CI", "CII", "CIII", "CIV", "CV", "CVI",
    "CVII", "CVIII", "CIX", "CX", "CXI", "CXII", "CXIII", "CXIV",
    "CXV", "CXVI", "CXVII", "CXVIII", "CXIX", "CXX",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_keys(mapping: dict[str, Any], keys: set[str], label: str) -> None:
    missing = sorted(keys - set(mapping))
    require(not missing, f"{label} missing keys: {','.join(missing)}")


def require_unit_weights(mapping: dict[str, Any], expected_keys: set[str], label: str) -> None:
    require_keys(mapping, expected_keys, label)
    values = [mapping[key] for key in expected_keys]
    require(all(isinstance(value, (int, float)) for value in values), f"{label} non-numeric weight")
    require(all(0.0 <= float(value) <= 1.0 for value in values), f"{label} weight outside 0..1")
    require(math.isclose(sum(float(value) for value in values), 1.0, rel_tol=0.0, abs_tol=1e-9), f"{label} weights must sum to 1")


def load() -> dict[str, Any]:
    require(CONFIG.is_file(), "V2 kernel missing")
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    require(isinstance(data, dict), "V2 kernel must be an object")
    return data


def verify(data: dict[str, Any]) -> None:
    require(data.get("schema_version") == 2, "unsupported V2 schema")
    require(data.get("north_star") == "CASH_READY_AUTONOMOUS_DEALIX_COMPANY", "north star drift")
    require(data.get("precedence") == "OVERRIDES_CONFLICTING_LOWER_LEVEL_OPERATING_LOGIC", "precedence drift")
    require(data.get("replaces_existing_constitution") is False, "V2 must strengthen, not replace, the constitution")
    require(data.get("objective") == "AUTONOMOUS_BUSINESS_THROUGHPUT", "objective drift")
    require(set(data.get("permanent_agents", [])) == CANONICAL_AGENTS, "permanent agent set drift")
    require(len(data.get("permanent_agents", [])) == 5, "exactly five permanent agents required")
    require(data.get("deep_wip_max") == 3, "deep WIP max drift")

    decision = data["decision_quality"]
    require(decision.get("prediction_is_fact") is False, "prediction cannot be fact")
    require(decision.get("inference_is_customer_evidence") is False, "inference cannot be customer evidence")
    require(set(decision.get("distinctions", [])) == {"DATA", "EVIDENCE", "BELIEF", "PREDICTION", "DECISION", "ACTION", "RESULT"}, "decision distinctions drift")

    dispatcher = data["economic_dispatcher"]
    require(dispatcher.get("normalization") == {"min": 0.0, "max": 1.0}, "dispatcher normalization drift")
    require_unit_weights(
        dispatcher["value_weights"],
        {"cash_impact", "customer_value", "proof_value", "constraint_relief", "founder_time_saved", "strategic_reuse"},
        "value weights",
    )
    require_unit_weights(
        dispatcher["execution_drag_weights"],
        {"time_cost", "cash_cost", "failure_risk", "irreversibility", "complexity_cost", "maintenance_cost"},
        "execution drag weights",
    )
    require(float(dispatcher.get("drag_floor", 0.0)) == 0.20, "drag floor drift")
    require(dispatcher.get("score_is_decision_aid_not_truth") is True, "priority score must not become truth")

    voi = data["value_of_information"]
    require(voi.get("enabled") is True, "VOI must be enabled")
    require(voi.get("research_first_when_voi_exceeds_immediate_execution_advantage") is True, "VOI decision rule drift")
    require(voi.get("anti_procrastination") is True, "VOI anti-procrastination guard missing")

    rev = data["reversibility"]
    require(rev.get("classes") == ["R0", "R1", "R2", "R3", "R4", "R5"], "reversibility classes drift")
    require(rev.get("high_uncertainty_r4_r5") == "DEFAULT_HOLD", "high-risk default hold missing")

    machines = data["state_machines"]
    require(machines.get("opportunity") == EXPECTED_OPPORTUNITY, "opportunity state machine drift")
    require(machines.get("production") == EXPECTED_PRODUCTION, "production state machine drift")
    require(machines.get("financial") == EXPECTED_FINANCIAL, "financial state machine drift")
    require(machines.get("illegal_transition_action") == "BLOCK", "illegal transitions must block")

    identity = data["identity"]
    require(identity.get("separate_agent_and_workload_identity") is True, "agent/workload identity separation required")
    require(identity.get("spiffe_spire", {}).get("auto_install") is False, "SPIFFE/SPIRE must not auto-install")
    require(identity.get("spiffe_spire", {}).get("status") == "TRIGGERED_OPTION_ONLY", "SPIFFE/SPIRE must remain triggered option")

    runtime = data["runtime_control"]
    require(runtime.get("runtime_policy_required") is True, "runtime policy required")
    require(runtime.get("prompt_policy_only_is_sufficient") is False, "prompt-only policy is insufficient")
    require({"ALLOW", "DENY", "PAUSE", "CANCEL", "RATE_LIMIT", "BUDGET", "REVOKE", "KILL"}.issubset(set(runtime.get("hooks", []))), "runtime control hooks incomplete")

    require(set(data.get("planes", [])) == REQUIRED_PLANES, "control plane separation drift")
    mcp = data["mcp"]
    architecture = set(mcp.get("architecture", []))
    require({"AUTHENTICATE_WORKLOAD", "RESOLVE_TENANT", "AUTHORIZE", "APPLY_POLICY", "APPLY_COST_RATE_BUDGET", "RECEIPT"}.issubset(architecture), "MCP control path incomplete")
    require(mcp.get("protocol_session_is_authority_state") is False, "MCP session cannot be authority state")

    durable = data["durable_tasks"]
    require({"QUEUED", "RUNNING", "WAITING", "BLOCKED", "CANCELLED", "FAILED", "SUCCEEDED"}.issubset(set(durable.get("states", []))), "durable task states incomplete")

    a2a = data["a2a"]
    require(a2a.get("internal_five_agents_transport") == "COMPANY_OS", "internal agents must use Company OS")
    require(a2a.get("agent_card_is_authority") is False, "Agent Card cannot grant authority")

    telemetry = data["telemetry"]
    require(telemetry.get("standard") == "OPENTELEMETRY_COMPATIBLE_WHERE_PRACTICAL", "telemetry standard drift")
    require(telemetry.get("sensitive_payload_default") is False, "sensitive telemetry must be off by default")

    budgets = data["budgets"]
    require(budgets.get("exhaustion_state") == "BUDGET_BLOCKED", "budget exhaustion must fail closed")
    require(budgets.get("agent_self_grant_unlimited_budget") is False, "agents cannot self-grant budgets")

    relationship = data["relationship_graph"]
    require(relationship.get("contact_is_relationship") is False, "contact cannot imply relationship")
    require(relationship.get("promotion_requires_evidence") is True, "relationship promotion requires evidence")

    autonomy = data["autonomy"]
    require(autonomy.get("universal_l5_autonomy") is False, "universal L5 forbidden")
    require("MISSING_EVIDENCE" in autonomy.get("degrade_on", []), "autonomy must degrade on missing evidence")

    invariants = set(data.get("invariants", []))
    require(REQUIRED_INVARIANTS.issubset(invariants), "critical invariant registry incomplete")
    require("AGENT_CANNOT_BYPASS_APPROVAL" in data.get("control_tests", []), "approval bypass control test missing")
    require("PROMPT_INJECTION_CANNOT_ESCALATE_PRIVILEGE" in data.get("control_tests", []), "prompt injection privilege test missing")

    twin = data["company_twin"]
    require(twin.get("is_company_brain") is False, "Company Twin cannot become second Company Brain")

    intent = data["commanders_intent"]
    require(set(intent.get("never_override", [])) == {"TRUTH", "POLICY", "AUTHORITY"}, "Commander's Intent override boundary drift")

    self_healing = set(data["self_healing"].get("forbidden", []))
    require({"PRODUCTION_DB_MUTATION", "SECRET_REPLACEMENT", "DNS_CHANGE", "PAYMENT", "PRIVILEGE_EXPANSION", "APPROVAL_BYPASS"}.issubset(self_healing), "self-healing boundary incomplete")

    l5 = data["l5"]
    require(l5.get("universal_authority") is False, "universal L5 authority forbidden")
    require(l5.get("exact_action_bound") is True, "L5 must be exact-action-bound")
    require(l5.get("material_effects_default") is False, "material effects must default off")

    require(data.get("section_coverage") == REQUIRED_SECTIONS, "V2 section coverage drift")


def main() -> int:
    try:
        data = load()
        verify(data)
        digest = hashlib.sha256(CONFIG.read_bytes()).hexdigest()
        print("DEALIX_META_OPERATING_SYSTEM_V2=PASS")
        print(f"META_CONTROL_SHA256={digest}")
        print("PERMANENT_AGENTS=5")
        print("DEEP_WIP_MAX=3")
        print("RUNTIME_POLICY_REQUIRED=true")
        print("UNIVERSAL_L5=false")
        print("SPIFFE_SPIRE_AUTO_INSTALL=false")
        return 0
    except Exception as exc:  # noqa: BLE001 - bounded fail-closed verifier
        print(f"DEALIX_META_OPERATING_SYSTEM_V2=FAIL reason={exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
