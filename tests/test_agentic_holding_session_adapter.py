from dataclasses import dataclass

import pytest

from dealix.agentic_holding.runtime import AgentDispatcher, ResourceSnapshot, WorkItem, build_registry
from dealix.agentic_holding.session_adapter import (
    LOGICAL_IDENTITY_FIELDS,
    SessionWorkRequest,
    legacy_executor_owner,
    render_dispatch_plan,
    render_session_job,
    resolve_live_base_sha,
    session_adapter_receipt,
    submit_dispatch_plan,
)


@dataclass
class FakeArm:
    arm_id: str
    owner_agent: str
    supported_sectors: list[str]
    capabilities: list[str]


class FakeSessionFactory:
    REPO_ROOT = None

    @staticmethod
    def resolve_default_base_sha():
        return "a" * 40

    @staticmethod
    def make_job(**kwargs):
        return {
            "JOB_ID": f"fake-{kwargs['business_goal']}",
            "OWNER_AGENT": kwargs["owner_agent"],
            "BUSINESS_GOAL": kwargs["business_goal"],
            "JOB_CLASS": kwargs["job_class"],
            "AUTHORITY_LEVEL": kwargs["authority_level"],
            "BASE_SHA": kwargs["base_sha"],
            "CONTEXT_REFS": kwargs["context_refs"],
            "MODIFYING": kwargs["modifying"],
            "STATUS": "QUEUED",
        }

    @staticmethod
    def submit_job(_root, job):
        job["STATUS"] = "WAITING_L5" if job["AUTHORITY_LEVEL"] == "L5" else "READY"
        return {"ok": True, "job": job}

    @staticmethod
    def run_job(_root, job, **_kwargs):
        job["STATUS"] = "SUCCEEDED"
        return {"ok": True, "status": "SUCCEEDED", "job": job}


def _registry():
    return build_registry(
        ["technology_saas_si"],
        [FakeArm("arm_code", "dealix-engineer", ["technology_saas_si"], ["build"])],
    )


def test_dynamic_group_owner_maps_to_legacy_session_factory_facade_and_live_base():
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
    assert job["BASE_SHA"] == "a" * 40
    assert job["LOGICAL_AGENT_ID"] == "dealix.group.revenue"
    assert job["LOGICAL_AGENT_PARENT"] == "dealix.group"
    assert job["LOGICAL_AGENT_LAYER"] == "group"
    assert job["LOGICAL_AGENT_ROLE"] == "revenue"
    assert "logical_agent:dealix.group.revenue" in job["CONTEXT_REFS"]
    assert f"agentic_base_sha:{'a' * 40}" in job["CONTEXT_REFS"]


def test_explicit_base_sha_overrides_live_resolver():
    registry = _registry()
    agent = registry.agents["dealix.group.revenue"]
    item = WorkItem("w-explicit", agent.agent_id, 90, 10)
    job = render_session_job(
        SessionWorkRequest(item, "explicit base", "reproducibility", "REVIEW", base_sha="b" * 40),
        agent=agent,
        session_factory=FakeSessionFactory,
    )
    assert job["BASE_SHA"] == "b" * 40


def test_native_live_base_resolver_is_preferred():
    assert resolve_live_base_sha(FakeSessionFactory) == "a" * 40


def test_arm_keeps_legacy_owner_alias_but_persists_top_level_logical_identity():
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
    assert job["LOGICAL_AGENT_ID"] == agent.agent_id
    assert job["LOGICAL_AGENT_PARENT"] == "dealix.technology_saas_si.arm_code"
    assert job["LOGICAL_AGENT_LAYER"] == "arm"
    assert job["LOGICAL_AGENT_ROLE"] == "operator"
    assert job["LOGICAL_AGENT_SECTOR"] == "technology_saas_si"
    assert job["LOGICAL_AGENT_ARM_ID"] == "arm_code"
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
    jobs = render_dispatch_plan(plan, registry=registry, requests=requests, session_factory=FakeSessionFactory)
    assert len(jobs) == 1
    receipt = session_adapter_receipt(jobs)
    assert receipt["jobs_rendered"] == 1
    assert receipt["logical_agent_ids"] == ["dealix.group.revenue"]
    assert receipt["logical_identity_fields"] == list(LOGICAL_IDENTITY_FIELDS)
    assert receipt["logical_identity_preserved"] is True
    assert receipt["explicit_base_sha"] is True
    assert receipt["base_shas"] == ["a" * 40]
    assert receipt["submitted"] is False
    assert receipt["material_external_effects_executed"] is False


def test_submit_dispatch_plan_uses_same_factory_queue_and_runner(tmp_path):
    registry = _registry()
    agent_id = "dealix.group.revenue"
    item = WorkItem("a", agent_id, 90, 10)
    plan = AgentDispatcher().dispatch(
        [item], registry=registry, snapshot=ResourceSnapshot(0.2, 8192, 0.0, 0.0, 1.0, 1.0, 2)
    )
    receipt = submit_dispatch_plan(
        plan,
        registry=registry,
        requests={"a": SessionWorkRequest(item, "prepare proposal", "cash path", "COMMERCIAL_REASONING")},
        session_factory=FakeSessionFactory,
        state_root=tmp_path,
        execute=True,
    )
    assert receipt["submitted"] is True
    assert receipt["submissions"][0]["status"] == "READY"
    assert receipt["executions"][0]["status"] == "SUCCEEDED"
    assert receipt["material_external_effects_executed"] is False


def test_l5_request_is_submitted_waiting_and_never_executed(tmp_path):
    registry = _registry()
    agent_id = "dealix.group.revenue"
    item = WorkItem("approval", agent_id, 90, 10)
    plan = AgentDispatcher().dispatch(
        [item], registry=registry, snapshot=ResourceSnapshot(0.2, 8192, 0.0, 0.0, 1.0, 1.0, 2)
    )
    receipt = submit_dispatch_plan(
        plan,
        registry=registry,
        requests={"approval": SessionWorkRequest(item, "material approval packet", "decision", "COMMERCIAL_REASONING", authority_level="L5")},
        session_factory=FakeSessionFactory,
        state_root=tmp_path,
        execute=True,
    )
    assert receipt["submissions"][0]["status"] == "WAITING_L5"
    assert receipt["executions"] == []


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
