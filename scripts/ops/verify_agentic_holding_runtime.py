from __future__ import annotations

import json

from dealix.agentic_holding.runtime import (
    AgentDispatcher,
    ResourceGovernor,
    ResourceSnapshot,
    WorkItem,
    build_current_registry,
)


def verify() -> dict[str, object]:
    registry = build_current_registry()
    receipt = registry.receipt()
    failures = list(receipt["orphan_failures"])
    if receipt["sector_companies"] != 20:
        failures.append(f"sector_count:{receipt['sector_companies']}")
    if receipt["distinct_arms"] < 44:
        failures.append(f"arm_count:{receipt['distinct_arms']}")
    if receipt["group_roles"] < 20:
        failures.append(f"group_roles:{receipt['group_roles']}")
    if receipt["sector_agents"] < 20 * 20:
        failures.append(f"sector_agents:{receipt['sector_agents']}")

    governor = ResourceGovernor(max_workers=12, max_repo_writers=2)
    normal = ResourceSnapshot(0.25, 8192, 0.05, 0.10, 1.0, 1.0, 2, cpu_count=4)
    pressure = ResourceSnapshot(0.95, 900, 0.85, 0.95, 0.2, 0.2, 2, cpu_count=4)
    exhausted = ResourceSnapshot(0.25, 8192, 0.05, 0.10, 0.0, 0.0, 2, cpu_count=4)
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

    quota_plan = dispatcher.dispatch(
        [
            WorkItem("model-dependent", revenue_agent, 95, 10, requires_model=True),
            WorkItem("deterministic", revenue_agent, 50, 10),
        ],
        registry=registry,
        snapshot=exhausted,
    )
    if quota_plan.rejected.get("model-dependent") != "model_quota_exhausted":
        failures.append("model_quota_fail_closed_guard_failed")
    if [item.work_id for item in quota_plan.selected] != ["deterministic"]:
        failures.append("deterministic_fallback_failed")

    return {
        "verdict": "FAIL" if failures else "PASS",
        **receipt,
        "resource_snapshot_source": "synthetic_acceptance_fixture",
        "live_runtime_activation_proven": False,
        "normal_worker_slots": normal_budget.worker_slots,
        "pressure_worker_slots": pressure_budget.worker_slots,
        "normal_writer_slots": normal_budget.writer_slots,
        "dispatch_receipt": plan.receipt(),
        "quota_exhaustion_receipt": quota_plan.receipt(),
        "failures": failures,
    }


def main() -> int:
    receipt = verify()
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    print(f"DEALIX_AGENTIC_HOLDING_RUNTIME={receipt['verdict']}")
    return 0 if receipt["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
