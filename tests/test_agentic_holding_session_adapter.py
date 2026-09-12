from dataclasses import dataclass

import pytest

from dealix.agentic_holding.runtime import AgentDispatcher, ResourceSnapshot, WorkItem, build_registry
from dealix.agentic_holding.session_adapter import (
    SessionWorkRequest,
    legacy_executor_owner,
    render_dispatch_plan,
    render_session_job,
    session_adapter_receipt,
)


@dataclass
class FakeArm:
    arm_id: str
    owner_agent: str
    supported_sectors: list[str]
    capabilities: list[str]


class FakeSessionFactory:
    @staticmethod
    def make_job(**kwargs):
        return {
            "OWNER_AGENT": kwargs["owner_agent"],
            "BUSINESS_GOAL": kwargs["business_goal"],
            "JOB_CLASS": kwargs["job_class"],
            "AUTHORITY_LEVEL": kwargs["authority_level"],
            "CONTEXT_REFS": kwargs["context_refs"],
            "MODIFYING": kwargs["modifying"],
        }


def _registry():
    return build_registry(
        ["technology_saas_si"],
        [FakeArm("arm_code", "dealix-engineer", ["technology_saas_si"], ["build"])],
    )


def test_dynamic_group_owner_maps_to_legacy_session_factory_facade():
    registry = _registry()
    agent = registry.agents["dealix.group.revenue"]
    assert legacy_executor_owner(agent) == "dealix-sales"
    item = WorkItem("w1", agent.agent_id, 90, 10)
    job = render_session_job(
        SessionWorkRequest(item, "qualify opportunity", "economic movement", "COMMERCIAL_REASONING"),
        agent=agent,
        session_factory=FakeSessionFactory,
    )
    assert job["OWNER_AGENT"] == "dealix-sales"
    assert "logical_agent:dealix.group.revenue" in job["CONTEXT_REFS"]


def test_arm_keeps_legacy_owner_alias_but_preserves_logical_identity():
    registry = _registry()
    agent = registry.agents["dealix.technology_saas_si.arm_code.operator"]
    assert legacy_executor_owner(agent) == "dealix-engineer"
    item = WorkItem("w2", agent.agent_id, 95, 20, repo_writer=True)
    job = render_session_job(
        SessionWorkRequest(item, "implement accepted patch", "delivery value", "ENGINEERING"),
        agent=agent,
        session_factory=FakeSessionFactory,
    )
    assert job["OWNER_AGENT"] == "dealix-engineer"
    assert job["MODIFYING"] is True
    assert "arm:arm_code" in job["CONTEXT_REFS"]


def test_dispatch_plan_renders_only_governor_selected_jobs_and_never_submits():
    registry = _registry()
    agent_id = "dealix.group.revenue"
    items = [
        WorkItem("a", agent_id, 90, 10),
        WorkItem("b", agent_id, 80, 10, material_external_effect=True),
    ]
    plan = AgentDispatcher().dispatch(
        items,
        registry=registry,
        snapshot=ResourceSnapshot(0.2, 8192, 0.0, 0.0, 1.0, 1.0, 2),
    )
    requests = {
        "a": SessionWorkRequest(items[0], "prepare proposal", "cash path", "COMMERCIAL_REASONING"),
        "b": SessionWorkRequest(items[1], "send proposal", "cash path", "COMMERCIAL_REASONING"),
    }
    jobs = render_dispatch_plan(
        plan,
        registry=registry,
        requests=requests,
        session_factory=FakeSessionFactory,
    )
    assert len(jobs) == 1
    receipt = session_adapter_receipt(jobs)
    assert receipt["jobs_rendered"] == 1
    assert receipt["submitted"] is False
    assert receipt["material_external_effects_executed"] is False


def test_render_rejects_material_external_effect_even_if_called_directly():
    registry = _registry()
    agent = registry.agents["dealix.group.revenue"]
    item = WorkItem("send", agent.agent_id, 100, 5, material_external_effect=True)
    with pytest.raises(ValueError, match="material external effects"):
        render_session_job(
            SessionWorkRequest(item, "send", "external", "COMMERCIAL_REASONING"),
            agent=agent,
            session_factory=FakeSessionFactory,
        )
