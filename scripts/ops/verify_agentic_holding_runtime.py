from __future__ import annotations

import json
from pathlib import Path

import yaml

from dealix.agentic_holding.runtime import (
    ARM_POD_ROLES,
    GROUP_ROLES,
    SECTOR_ROLES,
    AgentDispatcher,
    ResourceGovernor,
    ResourceSnapshot,
    WorkItem,
    build_current_registry,
)

ROOT = Path(__file__).resolve().parents[2]
CANONICAL_CONFIG = ROOT / "dealix/config/commercial_reset_2026_09_12.yaml"


def _canonical_roles() -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    payload = yaml.safe_load(CANONICAL_CONFIG.read_text(encoding="utf-8"))
    architecture = payload["architecture"]
    return (
        tuple(architecture["group_roles"]),
        tuple(architecture["sector_role_templates"]),
        tuple(architecture["arm_pod_roles"]),
    )


def verify() -> dict[str, object]:
    registry = build_current_registry()
    receipt = registry.receipt()
    failures = list(receipt["orphan_failures"])

    canonical_group, canonical_sector, canonical_arm = _canonical_roles()
    if tuple(GROUP_ROLES) != canonical_group:
        failures.append("canonical_group_role_drift")
    if tuple(SECTOR_ROLES) != canonical_sector:
        failures.append("canonical_sector_role_drift")
    if tuple(ARM_POD_ROLES) != canonical_arm:
        failures.append("canonical_arm_role_drift")
    if receipt["sector_companies"] != 20:
        failures.append(f"sector_count:{receipt['sector_companies']}")
    if receipt["distinct_arms"] < 44:
        failures.append(f"arm_count:{receipt['distinct_arms']}")
    if receipt["group_roles"] != len(canonical_group):
        failures.append(f"group_roles:{receipt['group_roles']}")
    if receipt["sector_agents"] != receipt["sector_companies"] * len(canonical_sector):
        failures.append(f"sector_agents:{receipt['sector_agents']}")

    governor = ResourceGovernor(max_workers=12, max_repo_writers=2)
    normal = ResourceSnapshot(0.25, 8192, 0.05, 0.10, 1.0, 1.0, 2, cpu_count=4)
    pressure = ResourceSnapshot(0.95, 900, 0.85, 0.95, 0.2, 0.2, 2, cpu_count=4)
    normal_budget = governor.budget(normal)
    pressure_budget = governor.budget(pressure)
    if normal_budget.worker_slots > 4:
        failures.append("host_capacity_cap_failed")
    if pressure_budget.worker_slots >= normal_budget.worker_slots:
        failures.append("resource_governor_did_not_throttle")

    revenue_agent = "dealix.group.revenue"
    dispatcher = AgentDispatcher(governor)
    plan = dispatcher.dispatch(
        [
            WorkItem("economic", revenue_agent, 95, 10, 5),
            WorkItem("paid-spill", revenue_agent, 90, 10, 5, requires_paid_model=True),
            WorkItem("live-send", revenue_agent, 100, 5, 5, material_external_effect=True),
        ],
        registry=registry,
        snapshot=normal,
    )
    if [item.work_id for item in plan.selected] != ["economic"]:
        failures.append("dispatcher_selection_drift")
    if plan.rejected.get("paid-spill") != "paid_spill_blocked":
        failures.append("paid_spill_guard_failed")
    if plan.rejected.get("live-send") != "exact_action_authority_required":
        failures.append("external_authority_guard_failed")

    free_plan = dispatcher.dispatch(
        [WorkItem("free-model", revenue_agent, 90, 10, requires_model=True, model_cost_authority="explicit_free")],
        registry=registry,
        snapshot=normal,
    )
    if [item.work_id for item in free_plan.selected] != ["free-model"]:
        failures.append("explicit_free_model_dispatch_failed")

    unknown_cost_plan = dispatcher.dispatch(
        [WorkItem("unknown-cost", revenue_agent, 90, 10, requires_model=True)],
        registry=registry,
        snapshot=normal,
    )
    if unknown_cost_plan.rejected.get("unknown-cost") != "model_cost_authority_unknown":
        failures.append("model_cost_authority_guard_failed")

    unknown_quota_plan = dispatcher.dispatch(
        [WorkItem("unknown-quota", revenue_agent, 90, 10, requires_model=True, model_cost_authority="explicit_free")],
        registry=registry,
        snapshot=ResourceSnapshot(0.25, 8192, 0.05, 0.10, None, None, 2, cpu_count=4),
    )
    if unknown_quota_plan.rejected.get("unknown-quota") != "provider_quota_unknown":
        failures.append("unknown_quota_fail_closed_guard_failed")

    exhausted_plan = dispatcher.dispatch(
        [
            WorkItem("model-dependent", revenue_agent, 95, 10, requires_model=True, model_cost_authority="explicit_free"),
            WorkItem("deterministic", revenue_agent, 50, 10),
        ],
        registry=registry,
        snapshot=ResourceSnapshot(0.25, 8192, 0.05, 0.10, 0.0, 1.0, 2, cpu_count=4),
    )
    if exhausted_plan.rejected.get("model-dependent") != "provider_quota_exhausted":
        failures.append("model_quota_fail_closed_guard_failed")
    if [item.work_id for item in exhausted_plan.selected] != ["deterministic"]:
        failures.append("deterministic_fallback_failed")

    paid_governor = ResourceGovernor(
        max_workers=4,
        paid_spill_allowed=True,
        paid_approval_reference="approval:verifier-paid-model-canary",
    )
    paid_plan = AgentDispatcher(paid_governor).dispatch(
        [WorkItem("paid-approved", revenue_agent, 90, 10, requires_paid_model=True)],
        registry=registry,
        snapshot=normal,
    )
    if [item.work_id for item in paid_plan.selected] != ["paid-approved"]:
        failures.append("paid_approval_reference_guard_failed")

    return {
        "verdict": "FAIL" if failures else "PASS",
        **receipt,
        "canonical_role_source": str(CANONICAL_CONFIG.relative_to(ROOT)),
        "canonical_group_roles": len(canonical_group),
        "canonical_sector_roles": len(canonical_sector),
        "canonical_arm_roles": len(canonical_arm),
        "resource_snapshot_source": "synthetic_acceptance_fixture",
        "live_runtime_activation_proven": False,
        "normal_worker_slots": normal_budget.worker_slots,
        "pressure_worker_slots": pressure_budget.worker_slots,
        "normal_writer_slots": normal_budget.writer_slots,
        "dispatch_receipt": plan.receipt(),
        "free_model_receipt": free_plan.receipt(),
        "unknown_quota_receipt": unknown_quota_plan.receipt(),
        "quota_exhaustion_receipt": exhausted_plan.receipt(),
        "paid_approval_receipt": paid_plan.receipt(),
        "failures": failures,
    }


def main() -> int:
    receipt = verify()
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    print(f"DEALIX_AGENTIC_HOLDING_RUNTIME={receipt['verdict']}")
    print("LIVE_RUNTIME_ACTIVATION=NOT_PROVEN")
    return 0 if receipt["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
