#!/usr/bin/env python3
"""Fail-closed verifier for Dealix's server agent operating model."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "data" / "ops" / "server_agent_operating_manifest_v1.json"
DELEGATION_PATH = ROOT / "data" / "ops" / "agent_council_company_delegation.json"

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


def load_manifest() -> dict[str, Any]:
    with MANIFEST_PATH.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise AssertionError("manifest_not_object")
    return payload


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


def main() -> int:
    payload = load_manifest()
    validate_manifest(payload)
    print("DEALIX_SERVER_AGENT_OPERATING_MODEL=PASS")
    print("CANONICAL_SYSTEMS=12")
    print(f"RESPONSIBILITY_LANES={len(payload['responsibility_lanes'])}")
    print("NEW_AGENT_RUNTIMES=0")
    print("NEW_SCHEDULERS=0")
    print("EXTERNAL_EFFECT_DEFAULTS=ALL_FALSE")
    print("RUNTIME_INSTALLATION=REQUIRED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
