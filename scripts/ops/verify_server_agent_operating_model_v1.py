#!/usr/bin/env python3
"""Fail-closed verifier for Dealix's server agent operating model.

The VPS may keep legacy runtime process/profile names for compatibility, but
only the five canonical Dealix agents are allowed to be accountable execution
authority owners. Legacy runtimes remain bounded implementation components.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "data" / "ops" / "server_agent_operating_manifest_v1.json"
AUTHORITY_PATH = ROOT / "data" / "ops" / "canonical_five_agent_authority_v1.json"
DELEGATION_PATH = ROOT / "data" / "ops" / "agent_council_company_delegation.json"
ORCHESTRATION_GUARDRAILS_PATH = ROOT / "data" / "ops" / "agent_orchestration_guardrails_v1.json"

REQUIRED_SYSTEMS = {
    "command_os",
    "revenue_os",
    "proof_os",
    "client_os",
    "delivery_os",
    "support_os",
    "finance_os",
    "data_os",
    "governance_os",
    "academy_os",
    "partner_os",
    "venture_os",
}

CANONICAL_AGENTS = {
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
}

REQUIRED_RUNTIME_AGENTS = {
    "company_brain",
    "sprint_orchestrator",
    "governance",
    "market_intel",
    "lead_intelligence",
    "revenue_intelligence",
    "sales_intelligence",
    "customer_acquisition",
    "diagnostic_agent",
    "data_architect",
    "managed_ops",
}

REQUIRED_SPECIALIST_PROFILES = {
    "founder-president",
    "sovereign-security",
    "engineering-verifier",
    "production-sre",
    "revenue-copilot",
    "market-partner-scout",
    "sales-negotiation",
    "delivery-success",
    "proof-data",
    "governance-finance",
    "capability-research",
    "self-improvement",
}

REQUIRED_RECEIPT_FIELDS = {
    "work_id",
    "timestamp",
    "source_owner",
    "target_owner",
    "system_id",
    "workload_id",
    "objective",
    "truth_class",
    "evidence_refs",
    "facts",
    "inferences",
    "unknowns",
    "current_state",
    "next_state",
    "next_evidence_required",
    "proposed_action",
    "execution_boundary",
    "autonomy_level",
    "approval_class",
    "idempotency_key",
    "stop_condition",
    "result",
    "output_evidence_refs",
    "founder_minutes",
    "agent_minutes",
    "elapsed_ms",
    "ai_cost",
    "tool_cost",
    "economic_delta",
}


def _load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise AssertionError(f"not_object:{path}")
    return payload


def load_manifest() -> dict[str, Any]:
    return _load(MANIFEST_PATH)


def load_authority_overlay() -> dict[str, Any]:
    return _load(AUTHORITY_PATH)


def load_orchestration_guardrails() -> dict[str, Any]:
    return _load(ORCHESTRATION_GUARDRAILS_PATH)


def validate_orchestration_guardrails(payload: dict[str, Any]) -> None:
    assert payload.get("schema") == "dealix.agent-orchestration-guardrails.v1"
    assert payload.get("status") == "PATTERN_CONTRACT_ONLY_NO_NEW_RUNTIME"

    dependency = payload.get("dependency_policy") or {}
    assert dependency.get("openai_agents_sdk_installed_by_this_contract") is False
    assert dependency.get("new_agent_framework_installed_by_this_contract") is False
    assert dependency.get("adoption_requires_capability_intake") is True
    assert dependency.get("existing_openclaw_hermes_runtime_remains_owner") is True

    controller = payload.get("controller_pattern") or {}
    assert controller.get("founder_facing_accountable_agent") == "dealix-pm"
    assert controller.get("default_pattern") == "MANAGER_CALLS_BOUNDED_SPECIALISTS"
    assert controller.get("manager_retains_final_founder_response") is True
    assert controller.get("specialists_may_own_truth") is False
    assert controller.get("specialists_may_self_schedule") is False
    assert controller.get("specialists_may_self_escalate_authority") is False
    assert controller.get("handoff_is_exception_not_default") is True
    assert controller.get("handoff_requires_typed_reason_and_target") is True
    assert controller.get("handoff_authority_check_at_start") is True

    tools = payload.get("tool_guardrails") or {}
    assert tools.get("applies_to_every_custom_side_effect_tool") is True
    assert tools.get("pre_execution_policy_check_required") is True
    assert tools.get("post_execution_receipt_check_required") is True
    assert tools.get("schema_validation_required") is True
    assert tools.get("timeout_and_failure_policy_required") is True
    assert tools.get("idempotency_required_for_mutating_internal_tools") is True
    assert tools.get("fail_closed_on_guardrail_error") is True
    assert tools.get("raw_model_output_may_execute_side_effect") is False
    assert tools.get("raw_model_output_may_promote_truth") is False

    approval = payload.get("human_approval") or {}
    assert approval.get("L0_L4_bounded_internal_may_continue") is True
    assert approval.get("L5_external_or_irreversible_requires_action_specific_approval") is True
    assert approval.get("approval_may_be_inferred_from_general_delegation") is False
    assert approval.get("approval_receipt_required_before_effect") is True
    assert approval.get("expired_or_mismatched_approval_blocks_effect") is True

    handoff = payload.get("handoff_boundary") or {}
    assert handoff.get("tool_guardrails_do_not_substitute_for_handoff_authorization") is True
    assert handoff.get("authorization_must_be_checked_before_handoff_side_effects") is True
    assert handoff.get("handoff_metadata_is_not_application_truth") is True
    assert handoff.get("receiving_specialist_must_use_canonical_context") is True

    observability = payload.get("observability") or {}
    assert observability.get("reuse_existing_opentelemetry") is True
    assert set(observability.get("gen_ai_operation_names") or []) == {
        "invoke_agent",
        "invoke_workflow",
        "execute_tool",
    }
    assert observability.get("workflow_name_attribute") == "gen_ai.workflow.name"
    assert observability.get("operation_name_attribute") == "gen_ai.operation.name"
    assert observability.get("capture_prompt_content_by_default") is False
    assert observability.get("capture_customer_content_by_default") is False
    assert observability.get("capture_secrets_by_default") is False
    assert observability.get("capture_raw_credentials_by_default") is False

    truth = payload.get("truth_and_authority") or {}
    assert truth
    assert all(value is False for value in truth.values())


def validate_authority_overlay(payload: dict[str, Any], manifest: dict[str, Any]) -> None:
    assert payload.get("schema") == "dealix.canonical-five-agent-authority.v1"
    assert payload.get("status") == "AUTHORITY_OVERLAY_ONLY"
    assert set(payload.get("canonical_agents") or {}) == CANONICAL_AGENTS

    lanes = manifest.get("responsibility_lanes") or []
    lane_ids = {lane.get("id") for lane in lanes}
    lane_authority = payload.get("lane_authority") or {}
    assert set(lane_authority) == lane_ids
    assert set(lane_authority.values()).issubset(CANONICAL_AGENTS)

    runtime_agents = set(manifest.get("existing_runtime_agents") or [])
    runtime_bindings = payload.get("legacy_runtime_bindings") or {}
    assert runtime_agents == REQUIRED_RUNTIME_AGENTS
    assert set(runtime_bindings) == runtime_agents
    for runtime_name, binding in runtime_bindings.items():
        assert runtime_name in REQUIRED_RUNTIME_AGENTS
        assert binding.get("canonical_owner") in CANONICAL_AGENTS
        assert binding.get("authority_owner") is False
        assert binding.get("self_schedule") is False
        assert binding.get("l5_authority") is False

    specialists = set(manifest.get("existing_specialist_profiles") or [])
    specialist_bindings = payload.get("specialist_profile_bindings") or {}
    assert specialists == REQUIRED_SPECIALIST_PROFILES
    assert set(specialist_bindings) == specialists
    assert set(specialist_bindings.values()).issubset(CANONICAL_AGENTS)

    growth_profiles = set(manifest.get("existing_growth_overlays") or [])
    growth_bindings = payload.get("growth_workload_bindings") or {}
    assert set(growth_bindings) == growth_profiles
    assert set(growth_bindings.values()).issubset(CANONICAL_AGENTS)

    compatibility = payload.get("compatibility_policy") or {}
    assert compatibility.get("legacy_names_may_continue_running") is True
    assert compatibility.get("legacy_names_are_truth_owners") is False
    assert compatibility.get("legacy_names_are_portfolio_authority_owners") is False
    assert compatibility.get("legacy_names_may_create_new_cadence") is False
    assert compatibility.get("legacy_names_may_self_escalate_authority") is False
    assert compatibility.get("legacy_names_may_execute_l5_without_action_specific_authority") is False
    assert compatibility.get("canonical_agents_remain_accountable_when_legacy_runtime_executes") is True

    defaults = payload.get("authority_defaults") or {}
    assert defaults
    assert all(value is False for value in defaults.values())


def validate_manifest(payload: dict[str, Any]) -> None:
    assert payload.get("schema") == "dealix.server-agent-operating-model.v1"
    assert payload.get("status") == "MANIFEST_READY_RUNTIME_INSTALLATION_REQUIRED"
    assert payload.get("logical_lanes_are_not_new_runtimes") is True

    based_on = payload.get("based_on") or {}
    assert based_on.get("repository") == "Dealix-sa/dealix"
    assert based_on.get("main_sha") == "b7115e09ef051ceaaf18d4d307cf3044a203f051"
    assert based_on.get("radar_pr") == 1405
    assert based_on.get("activation_claim") == "NOT_CLAIMED"

    with DELEGATION_PATH.open(encoding="utf-8") as handle:
        delegation = json.load(handle)
    binding = delegation.get("server_operating_model") or {}
    assert binding.get("manifest") == "data/ops/server_agent_operating_manifest_v1.json"
    assert binding.get("activation_claim") == "NOT_CLAIMED"
    assert binding.get("runtime_installation_required") is True
    assert binding.get("new_permanent_agents") == 0
    assert binding.get("new_timers_or_cron") == 0

    runtime_agents = set(payload.get("existing_runtime_agents") or [])
    assert runtime_agents == REQUIRED_RUNTIME_AGENTS

    lanes = payload.get("responsibility_lanes") or []
    assert len(lanes) >= 18
    lane_ids = {lane.get("id") for lane in lanes}
    assert len(lane_ids) == len(lanes)
    for lane in lanes:
        assert lane.get("id")
        assert lane.get("runtime_agents")
        assert set(lane["runtime_agents"]).issubset(runtime_agents)
        assert lane.get("specialists")
        assert lane.get("workload")
        assert lane.get("accountable_system") in REQUIRED_SYSTEMS
        assert lane.get("autonomy")
        assert lane.get("outputs")
        assert lane.get("blocked_effects")

    coverage = payload.get("canonical_system_coverage") or []
    assert {item.get("id") for item in coverage} == REQUIRED_SYSTEMS
    assert len({item.get("accountable_owner") for item in coverage}) == len(coverage)
    assert all(item.get("existing_cadence") for item in coverage)

    handoff = payload.get("handoff_contract") or {}
    assert set(handoff.get("required_fields") or []) == REQUIRED_RECEIPT_FIELDS
    assert len(handoff.get("forbidden_transitions") or []) >= 8

    external = payload.get("external_effect_defaults") or {}
    assert external
    assert all(value is False for value in external.values())

    kill = payload.get("kill_switches") or {}
    assert kill.get("default_state") == "OFF"
    assert "only reduce authority" in str(kill.get("semantics", ""))
    assert len(kill.get("switches") or []) >= 8

    cadence = payload.get("cadence_binding") or {}
    assert cadence.get("new_permanent_agents") == 0
    assert cadence.get("new_timers_or_cron") == 0
    assert cadence.get("parallel_scheduler_created") is False

    wip = payload.get("wip_and_capacity") or {}
    assert wip.get("global_primary_wip") == 1
    assert wip.get("per_agent_primary_tasks") == 1
    assert wip.get("overlapping_writer_serialization") is True
    assert wip.get("unbounded_agent_loops") is False

    gates = set(payload.get("quality_gates") or [])
    assert "SOURCE_AND_PROVENANCE" in gates
    assert "COMMERCIAL_AUTHORITY" in gates
    assert "CONSENT_SUPPRESSION_AND_CHANNEL_POLICY" in gates
    assert "CLAIM_PROOF_AND_PERMISSION" in gates
    assert "IDEMPOTENCY_RETRY_ROLLBACK_AND_HUMAN_HANDOFF" in gates

    done = set(payload.get("definition_of_done") or [])
    assert "all_12_canonical_systems_have_one_accountable_lane" in done
    assert "no_new_agent_runtime" in done
    assert "no_new_scheduler" in done
    assert "exact_head_runtime_acceptance_is_recorded_before_activation_claim" in done

    validate_authority_overlay(load_authority_overlay(), payload)
    validate_orchestration_guardrails(load_orchestration_guardrails())


def main() -> int:
    payload = load_manifest()
    validate_manifest(payload)
    print("DEALIX_SERVER_AGENT_OPERATING_MODEL=PASS")
    print("CANONICAL_SYSTEMS=12")
    print(f"RESPONSIBILITY_LANES={len(payload['responsibility_lanes'])}")
    print("CANONICAL_EXECUTION_AGENTS=5")
    print("LEGACY_RUNTIME_AUTHORITY_OWNERS=0")
    print("MANAGER_SPECIALIST_ORCHESTRATION=PASS")
    print("TOOL_GUARDRAILS=FAIL_CLOSED")
    print("OTEL_GENAI_SEMANTICS=PASS")
    print("NEW_AGENT_RUNTIMES=0")
    print("NEW_SCHEDULERS=0")
    print("EXTERNAL_EFFECT_DEFAULTS=ALL_FALSE")
    print("RUNTIME_INSTALLATION=REQUIRED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
