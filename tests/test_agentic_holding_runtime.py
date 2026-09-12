from dataclasses import dataclass

import pytest

from dealix.agentic_holding.runtime import (
    ARM_POD_ROLES,
    GROUP_ROLES,
    SECTOR_ROLES,
    AgentDispatcher,
    AgentLayer,
    LogicalAgent,
    ResourceGovernor,
    ResourceSnapshot,
    WorkItem,
    build_registry,
)


@dataclass
class FakeArm:
    arm_id: str
    owner_agent: str
    supported_sectors: list[str]
    capabilities: list[str]


def _registry():
    return build_registry(
        ["technology_saas_si", "construction_epc"],
        [
            FakeArm("arm_global", "dealix-pm", [], ["rank"]),
            FakeArm("arm_tech", "dealix-engineer", ["technology_saas_si"], ["build"]),
        ],
    )


def test_registry_builds_group_sector_and_arm_hierarchy_without_orphans():
    registry = _registry()
    assert registry.validate() == []
    assert len(GROUP_ROLES) == 24
    assert len(SECTOR_ROLES) == 22
    assert set(ARM_POD_ROLES) == {"lead", "scout", "operator", "verifier"}
    assert len(registry.sector_ids) == 2
    assert registry.receipt()["distinct_arms"] == 2
    assert "dealix.technology_saas_si.arm_tech.operator" in registry.agents
    assert "dealix.construction_epc.arm_tech.operator" not in registry.agents
    assert "dealix.construction_epc.arm_global.verifier" in registry.agents


def test_explicit_unknown_sector_marks_arm_unmapped_and_fails_validation():
    registry = build_registry(
        ["technology_saas_si"],
        [FakeArm("arm_unknown", "dealix-pm", ["missing_sector"], [])],
    )
    assert registry.unmapped_arms == {"arm_unknown"}
    assert registry.validate() == ["unmapped_arm:arm_unknown"]


def test_registry_rejects_orphan_agent():
    registry = _registry()
    with pytest.raises(ValueError, match="orphan agent parent"):
        registry.register_agent(
            LogicalAgent(
                agent_id="dealix.missing.worker",
                parent_id="dealix.missing",
                layer=AgentLayer.SPECIALIST,
                role="worker",
            )
        )


def test_resource_governor_is_host_capacity_aware_and_throttles_pressure():
    governor = ResourceGovernor(max_workers=12, max_repo_writers=3)
    normal = governor.budget(
        ResourceSnapshot(0.30, 8192, 0.05, 0.10, 1.0, 1.0, 4)
    )
    explicit_two_cpu = governor.budget(
        ResourceSnapshot(0.30, 8192, 0.05, 0.10, 1.0, 1.0, 4, cpu_count=2)
    )
    pressure = governor.budget(
        ResourceSnapshot(0.95, 900, 0.85, 0.95, 0.5, 0.5, 4, cpu_count=8)
    )
    assert normal.worker_slots == 4
    assert normal.writer_slots == 3
    assert explicit_two_cpu.worker_slots == 2
    assert pressure.worker_slots == 1
    assert pressure.writer_slots == 1


def test_dispatch_prioritizes_economic_value_and_respects_writer_budget():
    registry = _registry()
    agent = "dealix.group.revenue"
    items = [
        WorkItem("high", agent, 95, 15, 5, repo_writer=False),
        WorkItem("writer-1", agent, 80, 20, 5, repo_writer=True),
        WorkItem("writer-2", agent, 75, 20, 5, repo_writer=True),
        WorkItem("low", agent, 20, 20, 20, repo_writer=False),
    ]
    plan = AgentDispatcher(ResourceGovernor(max_workers=3, max_repo_writers=1)).dispatch(
        items,
        registry=registry,
        snapshot=ResourceSnapshot(0.2, 8192, 0.0, 0.0, 1.0, 1.0, 1),
    )
    selected = [item.work_id for item in plan.selected]
    assert selected[0] == "high"
    assert sum(item.repo_writer for item in plan.selected) <= 1
    assert plan.rejected["writer-2"] == "worktree_capacity"


def test_dispatch_fails_closed_for_model_work_when_quota_is_exhausted():
    registry = _registry()
    agent = "dealix.group.revenue"
    plan = AgentDispatcher().dispatch(
        [
            WorkItem("model-job", agent, 95, 10, requires_model=True),
            WorkItem("deterministic-job", agent, 50, 10),
        ],
        registry=registry,
        snapshot=ResourceSnapshot(0.2, 8192, 0.0, 0.0, 0.0, 0.0, 2, cpu_count=4),
    )
    assert [item.work_id for item in plan.selected] == ["deterministic-job"]
    assert plan.rejected["model-job"] == "model_quota_exhausted"
    assert plan.budget.model_capacity_available is False


def test_dispatch_blocks_paid_spill_material_effect_and_unknown_agent():
    registry = _registry()
    valid_agent = "dealix.group.revenue"
    items = [
        WorkItem("paid", valid_agent, 90, 10, requires_paid_model=True),
        WorkItem("external", valid_agent, 90, 10, material_external_effect=True),
        WorkItem("unknown", "dealix.unknown.agent", 90, 10),
    ]
    plan = AgentDispatcher().dispatch(
        items,
        registry=registry,
        snapshot=ResourceSnapshot(0.2, 8192, 0.0, 0.0, 1.0, 1.0, 2),
    )
    assert not plan.selected
    assert plan.rejected == {
        "paid": "paid_spill_blocked",
        "external": "exact_action_authority_required",
        "unknown": "unknown_agent",
    }
