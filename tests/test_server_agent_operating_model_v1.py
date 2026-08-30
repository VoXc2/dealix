from __future__ import annotations

from scripts.ops.verify_server_agent_operating_model_v1 import (
    CANONICAL_AGENTS,
    load_authority_overlay,
    load_manifest,
    load_orchestration_guardrails,
    validate_manifest,
    validate_orchestration_guardrails,
)


def test_server_agent_operating_model_is_fail_closed():
    validate_manifest(load_manifest())


def test_all_external_effects_default_false():
    payload = load_manifest()
    assert all(value is False for value in payload["external_effect_defaults"].values())
    overlay = load_authority_overlay()
    assert all(value is False for value in overlay["authority_defaults"].values())


def test_each_canonical_system_has_one_accountable_lane():
    payload = load_manifest()
    coverage = payload["canonical_system_coverage"]
    assert len(coverage) == 12
    assert len({item["id"] for item in coverage}) == 12
    assert len({item["accountable_owner"] for item in coverage}) == 12


def test_exactly_five_canonical_agents_own_every_responsibility_lane():
    payload = load_manifest()
    overlay = load_authority_overlay()
    assert set(overlay["canonical_agents"]) == CANONICAL_AGENTS
    lane_ids = {lane["id"] for lane in payload["responsibility_lanes"]}
    assert set(overlay["lane_authority"]) == lane_ids
    assert set(overlay["lane_authority"].values()).issubset(CANONICAL_AGENTS)


def test_legacy_runtime_processes_are_implementation_only():
    overlay = load_authority_overlay()
    for binding in overlay["legacy_runtime_bindings"].values():
        assert binding["canonical_owner"] in CANONICAL_AGENTS
        assert binding["authority_owner"] is False
        assert binding["self_schedule"] is False
        assert binding["l5_authority"] is False


def test_specialist_profiles_are_bounded_under_canonical_agents():
    overlay = load_authority_overlay()
    assert set(overlay["specialist_profile_bindings"].values()).issubset(CANONICAL_AGENTS)
    policy = overlay["compatibility_policy"]
    assert policy["legacy_names_are_truth_owners"] is False
    assert policy["legacy_names_are_portfolio_authority_owners"] is False
    assert policy["legacy_names_may_create_new_cadence"] is False
    assert policy["legacy_names_may_self_escalate_authority"] is False


def test_no_parallel_agent_or_scheduler_is_declared():
    payload = load_manifest()
    cadence = payload["cadence_binding"]
    assert cadence["new_permanent_agents"] == 0
    assert cadence["new_timers_or_cron"] == 0
    assert cadence["parallel_scheduler_created"] is False


def test_orchestration_patterns_are_manager_owned_and_fail_closed():
    guardrails = load_orchestration_guardrails()
    validate_orchestration_guardrails(guardrails)
    controller = guardrails["controller_pattern"]
    assert controller["founder_facing_accountable_agent"] == "dealix-pm"
    assert controller["manager_retains_final_founder_response"] is True
    assert controller["specialists_may_own_truth"] is False
    assert controller["handoff_authority_check_at_start"] is True


def test_side_effect_tools_and_telemetry_do_not_create_authority():
    guardrails = load_orchestration_guardrails()
    tool_policy = guardrails["tool_guardrails"]
    assert tool_policy["pre_execution_policy_check_required"] is True
    assert tool_policy["post_execution_receipt_check_required"] is True
    assert tool_policy["fail_closed_on_guardrail_error"] is True
    assert tool_policy["raw_model_output_may_execute_side_effect"] is False
    assert tool_policy["raw_model_output_may_promote_truth"] is False

    telemetry = guardrails["observability"]
    assert set(telemetry["gen_ai_operation_names"]) == {
        "invoke_agent",
        "invoke_workflow",
        "execute_tool",
    }
    assert telemetry["capture_prompt_content_by_default"] is False
    assert telemetry["capture_customer_content_by_default"] is False
