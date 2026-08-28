from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "commercial" / "route_commercial_agent_workloads_v1.py"
WORKLOADS = ROOT / "data" / "commercial" / "agent_council_growth_workloads.json"

spec = importlib.util.spec_from_file_location("dealix_workload_router", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def _workloads() -> dict:
    return json.loads(WORKLOADS.read_text(encoding="utf-8"))


def _base_truth() -> dict:
    return {
        "ranking_does_not_create_relationship": True,
        "ranking_does_not_create_revenue": True,
        "readiness_does_not_equal_execution_authority": True,
        "planner_never_sends_external": True,
        "planner_never_issues_execution_authority": True,
    }


def test_internal_proposal_routes_to_existing_revenue_role() -> None:
    item = {
        "id": "deal-1",
        "stage": "DISCOVERY",
        "channel": "internal",
        "proposed_action": "prepare_proposal",
        "action_class": "INTERNAL_EXECUTABLE",
        "priority_score": 70,
    }
    command = {
        "schema": "dealix.commercial_autopilot.command.v1",
        "truth_statement": _base_truth(),
        "primary_focus": item,
        "founder_top_5": [item],
    }
    result = module.build_workload_queue(command, _workloads())
    packet = result["work_items"][0]
    assert packet["owner_role"] == "revenue"
    assert packet["packet_class"] == "EXECUTE_INTERNAL"
    assert packet["safe_internal_execute"] is True
    assert packet["external_effect_allowed_by_router"] is False
    assert result["architecture"]["new_permanent_agents"] == 0
    assert result["architecture"]["new_schedulers"] == 0


def test_external_authorized_send_is_governance_handoff_not_router_execution() -> None:
    item = {
        "id": "email-1",
        "stage": "VERIFIED_RELATIONSHIP",
        "channel": "email",
        "proposed_action": "send",
        "action_class": "EXECUTION_AUTHORIZED",
        "priority_score": 60,
        "authority_reason": "specific_execution_authority_verified:auth-1",
    }
    command = {
        "schema": "dealix.commercial_autopilot.command.v1",
        "truth_statement": _base_truth(),
        "primary_focus": item,
        "founder_top_5": [item],
        "execution_authorized_queue": [item],
    }
    result = module.build_workload_queue(command, _workloads())
    packet = result["work_items"][0]
    assert packet["owner_role"] == "governance_agent"
    assert packet["packet_class"] == "REVALIDATE_EXTERNAL_HANDOFF"
    assert packet["safe_internal_execute"] is False
    assert packet["external_effect_allowed_by_router"] is False
    assert result["authority"]["router_can_send_external"] is False
    assert result["authority"]["execution_authorized_items_are_handoff_only"] is True


def test_market_signal_routes_to_market_intelligence_without_relationship_promotion() -> None:
    item = {
        "id": "signal-1",
        "stage": "ATTENTION",
        "channel": "internal",
        "proposed_action": "research",
        "action_class": "INTERNAL_EXECUTABLE",
        "priority_score": 20,
        "signal": {"signal_type": "funding_or_expansion"},
    }
    command = {
        "schema": "dealix.commercial_autopilot.command.v1",
        "truth_statement": _base_truth(),
        "primary_focus": item,
        "founder_top_5": [item],
    }
    result = module.build_workload_queue(command, _workloads())
    assert result["work_items"][0]["owner_role"] == "market_intelligence"
    assert result["work_items"][0]["stage"] == "ATTENTION"


def test_blocked_or_specific_approval_routes_to_governance() -> None:
    blocked = {
        "id": "blocked-1",
        "stage": "VERIFIED_RELATIONSHIP",
        "channel": "whatsapp",
        "proposed_action": "cold_bulk_send",
        "action_class": "BLOCKED",
        "priority_score": 99,
    }
    approval = {
        "id": "approval-1",
        "stage": "CUSTOMER_SPECIFIC_QUOTE",
        "channel": "internal",
        "proposed_action": "final_price",
        "action_class": "SPECIFIC_APPROVAL_REQUIRED",
        "priority_score": 98,
    }
    command = {
        "schema": "dealix.commercial_autopilot.command.v1",
        "truth_statement": _base_truth(),
        "primary_focus": blocked,
        "founder_top_5": [blocked, approval],
        "approval_queue": [approval],
        "blocked_queue": [blocked],
    }
    result = module.build_workload_queue(command, _workloads())
    by_id = {x["work_item_id"]: x for x in result["work_items"]}
    assert by_id["blocked-1"]["owner_role"] == "governance_agent"
    assert by_id["blocked-1"]["packet_class"] == "BLOCK_AND_EXPLAIN"
    assert by_id["approval-1"]["owner_role"] == "governance_agent"
    assert by_id["approval-1"]["packet_class"] == "PREPARE_APPROVAL_PACKET"


def test_missing_truth_contract_fails_closed() -> None:
    command = {
        "schema": "dealix.commercial_autopilot.command.v1",
        "truth_statement": {"ranking_does_not_create_revenue": True},
        "founder_top_5": [],
    }
    try:
        module.build_workload_queue(command, _workloads())
    except ValueError as exc:
        assert "commercial_truth_contract_incomplete" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected fail-closed truth validation")
