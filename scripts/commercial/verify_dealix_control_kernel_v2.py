#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PATH = ROOT / "config" / "company" / "dealix_control_kernel_v2.json"

EXPECTED_SECTIONS = [
    "LXXI", "LXXII", "LXXIII", "LXXIV", "LXXV", "LXXVI", "LXXVII", "LXXVIII", "LXXIX", "LXXX",
    "LXXXI", "LXXXII", "LXXXIII", "LXXXIV", "LXXXV", "LXXXVI", "LXXXVII", "LXXXVIII", "LXXXIX", "XC",
    "XCI", "XCII", "XCIII", "XCIV", "XCV", "XCVI", "XCVII", "XCVIII", "XCIX", "C", "CI", "CII",
    "CIII", "CIV", "CV", "CVI", "CVII", "CVIII", "CIX", "CX", "CXI", "CXII", "CXIII", "CXIV",
    "CXV", "CXVI", "CXVII", "CXVIII", "CXIX", "CXX",
]
EXPECTED_EPISTEMIC = ["DATA", "EVIDENCE", "BELIEF", "PREDICTION", "DECISION", "ACTION", "RESULT"]


def _dict(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    return value if isinstance(value, dict) else {}


def _list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    return value if isinstance(value, list) else []


def _sum_is_one(values: dict[str, Any]) -> bool:
    if not values or any(not isinstance(v, (int, float)) for v in values.values()):
        return False
    return math.isclose(sum(float(v) for v in values.values()), 1.0, rel_tol=0.0, abs_tol=1e-9)


def verify(data: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            failures.append(code)

    require(data.get("status") == "CANONICAL_CONSTITUTIONAL_SUPERLAYER", "STATUS")
    require(data.get("kernel_version") == "2.0-control-kernel", "KERNEL_VERSION")
    require(data.get("effective_date") == "2026-09-11", "EFFECTIVE_DATE")
    require(data.get("north_star") == "CASH_READY_AUTONOMOUS_DEALIX_COMPANY", "NORTH_STAR")
    require(data.get("objective") == "AUTONOMOUS_BUSINESS_THROUGHPUT", "OBJECTIVE")
    require("WITHOUT_REPLACING_EXISTING_DEALIX_CONSTITUTION" in str(data.get("scope", "")), "SUPERLAYER_SCOPE")

    sections = _list(data, "section_registry")
    ids = [row[0] for row in sections if isinstance(row, list) and len(row) == 2]
    require(ids == EXPECTED_SECTIONS, "SECTION_REGISTRY_EXACT")
    require(len(sections) == 50, "SECTION_COUNT")

    dq = _dict(data, "decision_quality")
    require(dq.get("epistemic_states") == EXPECTED_EPISTEMIC, "EPISTEMIC_STATES")
    require(dq.get("prediction_is_not_fact") is True, "PREDICTION_NOT_FACT")
    require(dq.get("inference_is_not_customer_evidence") is True, "INFERENCE_NOT_EVIDENCE")
    required_decision_fields = {"decision_id", "decision", "decision_owner", "evidence", "assumptions", "confidence", "expected_result", "expected_value", "downside", "reversibility", "decision_deadline", "prediction", "actual_result", "calibration_error"}
    require(required_decision_fields <= set(dq.get("material_decision_fields", [])), "DECISION_FIELDS")

    econ = _dict(data, "economic_dispatcher")
    require(_sum_is_one(_dict(econ, "value_weights")), "VALUE_WEIGHTS_SUM")
    require(_sum_is_one(_dict(econ, "execution_drag_weights")), "DRAG_WEIGHTS_SUM")
    require(econ.get("close_candidate_threshold_percent") == 10, "TIE_THRESHOLD")
    require(econ.get("score_is_decision_aid_not_objective_truth") is True, "SCORE_NOT_OBJECTIVE_TRUTH")
    require("MAX(0.20, EXECUTION_DRAG)" in str(econ.get("final_priority", "")), "PRIORITY_FLOOR")

    voi = _dict(data, "value_of_information")
    require(voi.get("research_must_not_be_procrastination") is True, "VOI_NO_PROCRASTINATION")
    require("VOI" in str(voi.get("decision_rule", "")), "VOI_DECISION_RULE")

    rev = _dict(data, "reversibility")
    classes = _dict(rev, "classes")
    require(list(classes.keys()) == ["R0", "R1", "R2", "R3", "R4", "R5"], "REVERSIBILITY_CLASSES")
    require(rev.get("high_uncertainty_r4_r5_default") == "HOLD", "R45_DEFAULT_HOLD")
    require(rev.get("high_confidence_r0_r1_default") == "EXECUTE", "R01_DEFAULT_EXECUTE")

    sm = _dict(data, "state_machines")
    opportunity = sm.get("opportunity", [])
    production = sm.get("production", [])
    financial = sm.get("financial", [])
    require(opportunity and opportunity[0] == "RESEARCH_ONLY" and opportunity[-1] == "EXPANSION", "OPPORTUNITY_STATE_MACHINE")
    require(production and production[0] == "SOURCE_ACCEPTED" and production[-1] == "PRODUCTION_GREEN", "PRODUCTION_STATE_MACHINE")
    require(financial and financial[0] == "OPPORTUNITY_VALUE" and financial[-1] == "REVENUE_RECOGNITION_STATE", "FINANCIAL_STATE_MACHINE")
    require(sm.get("illegal_transition_outcome") == "INVALID_STATE_TRANSITION", "ILLEGAL_TRANSITION")
    require(sm.get("automatic_promotion_forbidden") is True, "NO_AUTO_PROMOTION")
    require(sm.get("previous_green_does_not_green_new_release") is True, "NO_STALE_GREEN")

    identity = _dict(data, "identity")
    require(identity.get("never_authorize_by_agent_name_only") is True, "NO_AGENT_NAME_AUTHORITY")
    require({"agent_id", "workload_id", "environment", "code_version", "policy_version", "tool", "authority"} <= set(identity.get("material_binding_fields", [])), "IDENTITY_BINDING")

    trust = _dict(data, "workload_trust_roadmap")
    require(trust.get("do_not_install_spire_without_trigger") is True, "NO_PREMATURE_SPIRE")

    runtime = _dict(data, "runtime_control")
    require({"IDENTIFY", "INSPECT", "TRACE", "ALLOW", "DENY", "PAUSE", "CANCEL", "RATE_LIMIT", "BUDGET", "REVOKE", "KILL"} <= set(runtime.get("hooks", [])), "RUNTIME_HOOKS")
    require(runtime.get("runtime_policy_required") is True, "RUNTIME_POLICY")
    require(runtime.get("prompt_policy_alone_is_insufficient") is True, "PROMPT_NOT_ENOUGH")

    receipt = _dict(data, "policy_decision_receipt")
    require({"ALLOW", "DENY", "REQUIRE_APPROVAL", "REQUIRE_MORE_EVIDENCE", "RATE_LIMIT", "QUARANTINE"} <= set(receipt.get("outcomes", [])), "POLICY_OUTCOMES")
    require(receipt.get("observable") is True, "POLICY_OBSERVABLE")

    planes = _dict(data, "planes")
    require(set(planes.get("required", [])) == {"INTELLIGENCE_PLANE", "CONTROL_PLANE", "EXECUTION_PLANE", "DATA_PLANE", "PROOF_PLANE"}, "PLANE_SEPARATION")
    require(planes.get("single_layer_must_not_silently_control_all_others") is True, "NO_SINGLE_LAYER_CONTROL")

    mcp = _dict(data, "mcp_control")
    flow = mcp.get("flow", [])
    require(flow and flow[0] == "AGENT" and flow[-1] == "TELEMETRY", "MCP_FLOW")
    require(set(mcp.get("protocol_session_must_not_own", [])) == {"BUSINESS_STATE", "CUSTOMER_STATE", "AUTHORITY_STATE", "ECONOMIC_STATE"}, "MCP_STATE_BOUNDARY")

    tasks = _dict(data, "long_running_tasks")
    require(set(tasks.get("states", [])) == {"QUEUED", "RUNNING", "WAITING", "BLOCKED", "CANCELLING", "CANCELLED", "FAILED", "SUCCEEDED"}, "TASK_STATES")
    require({"MODEL_RESTART", "PROCESS_RESTART", "AGENT_RESTART", "MCP_RECONNECT", "PROVIDER_FAILOVER"} <= set(tasks.get("must_survive", [])), "TASK_DURABILITY")

    a2a = _dict(data, "a2a_boundary")
    require(a2a.get("internal_five_agents_use_company_os") is True, "INTERNAL_A2A_BOUNDARY")
    require(a2a.get("external_agent_card_is_discovery_metadata_not_authority") is True, "AGENT_CARD_NOT_AUTHORITY")

    telemetry = _dict(data, "telemetry")
    require(telemetry.get("standard") == "OPENTELEMETRY_COMPATIBLE_WHERE_PRACTICAL", "OTEL_STANDARD")
    require(telemetry.get("sensitive_prompt_tool_content_default_recording") is False, "NO_SENSITIVE_TELEMETRY_DEFAULT")

    observability = _dict(data, "business_observability")
    require("TIME_QUOTE_TO_PAYMENT" in observability.get("timers", []), "BUSINESS_OBSERVABILITY")

    budget = _dict(data, "budget_governor")
    require(budget.get("exhaustion_outcome") == "BUDGET_BLOCKED", "BUDGET_BLOCKED")
    require(budget.get("agents_cannot_self_grant_unlimited_budget") is True, "NO_SELF_BUDGET")

    marginal = _dict(data, "marginal_value")
    require("STOP_OR_REPLAN" in str(marginal.get("rule", "")), "MARGINAL_STOP")

    stop_loss = _dict(data, "stop_loss")
    require(set(stop_loss.get("required", [])) == {"TIME_STOP", "COST_STOP", "RISK_STOP", "EVIDENCE_STOP", "CUSTOMER_STOP"}, "STOP_LOSS")
    require(stop_loss.get("no_immortal_initiatives") is True, "NO_IMMORTAL_INITIATIVES")

    require(_dict(data, "customer_trust").get("maximize_outreach_at_expense_of_trust") is False, "TRUST_OVER_OUTREACH")

    relationship = _dict(data, "relationship_graph")
    require(relationship.get("contact_graph_separate") is True, "CONTACT_RELATIONSHIP_SEPARATION")
    require(relationship.get("promotion_requires_evidence") is True, "RELATIONSHIP_EVIDENCE")

    memory = _dict(data, "customer_memory")
    require(memory.get("global_uncontrolled_customer_sensitive_memory_forbidden") is True, "NO_GLOBAL_CUSTOMER_MEMORY")
    require({"source", "purpose", "tenant", "sensitivity", "retention", "access_scope", "last_validation"} <= set(memory.get("record_fields", [])), "CUSTOMER_MEMORY_FIELDS")

    require("CUSTOMER_VALIDATION" in _dict(data, "proof_compounding_index").get("dimensions", []), "PROOF_INDEX")

    repeat = _dict(data, "repeatability_index")
    require(len(repeat.get("dimensions", [])) == 8 and repeat.get("productization_requires_threshold") is True, "REPEATABILITY_INDEX")

    auto_roi = _dict(data, "automation_roi")
    require(set(auto_roi.get("required_components", [])) == {"VALUE_CREATED", "HUMAN_COST_REMOVED", "BUILD_COST", "MAINTENANCE_COST", "FAILURE_COST"}, "AUTOMATION_ROI_COMPONENTS")
    require(auto_roi.get("operator_relationship") == "UNSPECIFIED_IN_FOUNDER_TEXT", "AUTOMATION_ROI_OPERATOR")
    require(auto_roi.get("aggregation_requires_explicit_policy") is True, "AUTOMATION_ROI_EXPLICIT_POLICY")
    require(auto_roi.get("kill_negative_automation") is True, "KILL_NEGATIVE_AUTOMATION")
    require(auto_roi.get("automation_volume_is_not_success") is True, "AUTOMATION_VOLUME_NOT_SUCCESS")

    scorecard = _dict(data, "agent_scorecard")
    require({"tool_calls", "message_count", "token_usage", "tasks_generated"} <= set(scorecard.get("do_not_reward", [])), "AGENT_ACTIVITY_NOT_REWARD")

    promotion = _dict(data, "autonomy_promotion")
    require(promotion.get("bounded_workflow_only") is True, "BOUNDED_AUTONOMY_PROMOTION")
    require(promotion.get("universal_l5_autonomy_forbidden") is True, "NO_UNIVERSAL_L5")

    require(_dict(data, "autonomy_degradation").get("autonomy_is_earned_continuously") is True, "AUTONOMY_DEGRADATION")

    model = _dict(data, "model_change")
    require(model.get("silent_model_replacement_forbidden") is True, "NO_SILENT_MODEL_CHANGE")
    require(model.get("lifecycle") == ["DISCOVERED", "EVALUATION", "APPROVED_INTERNAL", "APPROVED_BOUNDED_PRODUCTION", "PRODUCTION", "DEPRECATED", "RETIRED"], "MODEL_LIFECYCLE")

    require(_dict(data, "shadow_execution").get("material_effect") is False, "SHADOW_NO_EFFECT")

    canary = _dict(data, "canary_autonomy")
    require(canary.get("progression") == ["OFF", "SHADOW", "CANARY", "BOUNDED", "STANDARD"], "CANARY_PROGRESSION")
    require(canary.get("rollback_defined_before_promotion") is True, "CANARY_ROLLBACK")

    invariants = set(str(x) for x in _list(data, "invariants"))
    for invariant, code in [
        ("PERMANENT_AGENTS == 5", "AGENT_INVARIANT"),
        ("DEEP_WIP <= 3", "WIP_INVARIANT"),
        ("NO_AGENT_SELF_AUTHORITY", "SELF_AUTHORITY_INVARIANT"),
        ("NO_SECRET_IN_REPO", "SECRET_INVARIANT"),
    ]:
        require(invariant in invariants, code)

    tests = set(str(x) for x in _list(data, "control_tests"))
    require("PROMPT_INJECTION_DOES_NOT_ESCALATE_PRIVILEGE" in tests, "PROMPT_INJECTION_CONTROL_TEST")
    require("WRONG_TENANT_DENIED" in tests, "TENANT_CONTROL_TEST")
    require("STALE_EVIDENCE_REJECTED" in tests, "STALE_EVIDENCE_CONTROL_TEST")

    twin = _dict(data, "company_twin")
    require(twin.get("derived_projection_not_another_company_brain") is True, "TWIN_NOT_BRAIN")
    require("current_constraint" in twin.get("fields", []), "TWIN_CONSTRAINT")

    require("PDPL" in _list(data, "saudi_operating_graph"), "SAUDI_PDPL")
    require("ETIMAD" in _list(data, "saudi_operating_graph"), "SAUDI_ETIMAD")

    regulatory = _dict(data, "regulatory_radar")
    require(regulatory.get("sources_must_be_authoritative") is True, "REGULATORY_AUTHORITY")
    require("URGENT" in regulatory.get("classifications", []), "REGULATORY_CLASSIFICATION")

    demand = _dict(data, "demand_radar")
    require(demand.get("market_hype_separate_from_purchase_signal") is True, "HYPE_NOT_DEMAND")
    require(demand.get("metric") == "DEMAND_CONFIDENCE", "DEMAND_CONFIDENCE")

    category = _dict(data, "category_control")
    require(category.get("category") == "AI_BUSINESS_OPERATING_SYSTEM", "CATEGORY")
    require(category.get("corporate_vision_broad_commercial_conversation_narrow") is True, "CATEGORY_NARROW_COMMERCIAL")

    require(_list(data, "customer_acquisition_ladder")[:3] == ["MARKET_SIGNAL", "USEFUL_INSIGHT", "PERMISSIONED_INTERACTION"], "ACQUISITION_LADDER")
    require(_dict(data, "growth_loops").get("measure_loop_speed") is True, "LOOP_SPEED")

    commander = _dict(data, "commanders_intent")
    require(commander.get("execute_best_bounded_action_when_exact_instructions_absent") is True, "COMMANDERS_INTENT")
    require(set(commander.get("never_override", [])) == {"TRUTH", "POLICY", "AUTHORITY"}, "COMMANDER_BOUNDARY")

    founder = _dict(data, "minimum_founder_surface")
    require(founder.get("founder_actions") == ["APPROVE", "REJECT", "CHOOSE", "NEGOTIATE", "RELATIONSHIP", "STRATEGY"], "FOUNDER_SURFACE")
    require(founder.get("do_not_ask_founder_to_do_safe_machine_work") is True, "FOUNDER_LEVERAGE")

    healing = _dict(data, "self_healing")
    require({"PRODUCTION_DB_MUTATION", "SECRET_REPLACEMENT", "DNS_CHANGE", "EXTERNAL_COMMITMENT", "PAYMENT", "PRIVILEGE_EXPANSION", "APPROVAL_BYPASS"} <= set(healing.get("forbidden", [])), "SELF_HEALING_BOUNDARY")

    final = _dict(data, "final_directive")
    require(final.get("policy") == "GOVERNS", "FINAL_POLICY")
    require(final.get("identity") == "PROVES", "FINAL_IDENTITY")
    require(final.get("receipts") == "PROVE", "FINAL_RECEIPTS")
    require(final.get("founder") == "HANDLES_EXCEPTIONS", "FINAL_FOUNDER")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Dealix Meta-Operating System V2 Control Kernel")
    parser.add_argument("--path", default=str(DEFAULT_PATH))
    args = parser.parse_args()
    path = Path(args.path)
    if not path.is_file():
        print(f"DEALIX_CONTROL_KERNEL_V2_VERIFY=FAIL missing={path}")
        return 2
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"DEALIX_CONTROL_KERNEL_V2_VERIFY=FAIL parse={type(exc).__name__}")
        return 2
    if not isinstance(data, dict):
        print("DEALIX_CONTROL_KERNEL_V2_VERIFY=FAIL root_not_object")
        return 2
    failures = verify(data)
    if failures:
        print("DEALIX_CONTROL_KERNEL_V2_VERIFY=FAIL " + ",".join(failures))
        return 2
    print("DEALIX_CONTROL_KERNEL_V2_VERIFY=PASS")
    print(f"KERNEL_VERSION={data['kernel_version']}")
    print("SECTIONS=LXXI..CXX")
    print("SECTION_COUNT=50")
    print("CONTROL_POLICY=FAIL_CLOSED")
    print("UNIVERSAL_L5_AUTONOMY=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
