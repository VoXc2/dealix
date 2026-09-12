from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from dealix.agentic_holding.runtime import DispatchPlan, LogicalAgent, WorkItem


LEGACY_EXECUTOR_OWNERS = (
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
)

LOGICAL_IDENTITY_FIELDS = (
    "LOGICAL_AGENT_ID",
    "LOGICAL_AGENT_PARENT",
    "LOGICAL_AGENT_LAYER",
    "LOGICAL_AGENT_ROLE",
    "LOGICAL_AGENT_SECTOR",
    "LOGICAL_AGENT_ARM_ID",
)

_GROUP_ROLE_TO_LEGACY_OWNER = {
    "president": "dealix-pm",
    "strategy-capital": "dealix-pm",
    "coo": "dealix-pm",
    "cfo-economic-truth": "dealix-pm",
    "risk": "dealix-pm",
    "governance-compliance": "dealix-pm",
    "qa-verification": "dealix-pm",
    "proof": "dealix-pm",
    "self-improvement": "dealix-pm",
    "revenue": "dealix-sales",
    "growth": "dealix-sales",
    "procurement-b2g": "dealix-sales",
    "partnerships": "dealix-sales",
    "delivery": "dealix-delivery",
    "customer-success": "dealix-delivery",
    "cto": "dealix-engineer",
    "ai-automation": "dealix-engineer",
    "product": "dealix-engineer",
    "data-analytics": "dealix-engineer",
    "engineering": "dealix-engineer",
    "security": "dealix-engineer",
    "research-intelligence": "dealix-pm",
    "talent-workforce": "dealix-pm",
    "brand-content": "dealix-content",
}

_SECTOR_ROLE_HINTS = (
    (("sales", "business-development", "procurement", "b2g", "partnerships", "diagnostic"), "dealix-sales"),
    (("delivery", "customer-success", "proof"), "dealix-delivery"),
    (("solution-architect", "product", "data", "qa"), "dealix-engineer"),
    (("content", "distribution"), "dealix-content"),
)

_ARM_ROLE_TO_LEGACY_OWNER = {
    "lead": "dealix-pm",
    "scout": "dealix-sales",
    "operator": "dealix-engineer",
    "verifier": "dealix-delivery",
}


@dataclass(frozen=True, slots=True)
class SessionWorkRequest:
    work_item: WorkItem
    business_goal: str
    economic_reason: str
    job_class: str
    authority_level: str = "L3"
    urgency: str = "normal"
    base_sha: str | None = None
    files_in_scope: tuple[str, ...] = ()
    context_refs: tuple[str, ...] = ()
    tests: tuple[str, ...] = ()
    acceptance: Mapping[str, Any] | None = None
    executor: Mapping[str, Any] | None = None
    next_action: str = ""


def legacy_executor_owner(agent: LogicalAgent) -> str:
    if agent.legacy_owner_alias in LEGACY_EXECUTOR_OWNERS:
        return str(agent.legacy_owner_alias)
    if agent.layer.value == "group":
        return _GROUP_ROLE_TO_LEGACY_OWNER.get(agent.role, "dealix-pm")
    if agent.layer.value == "sector":
        for hints, owner in _SECTOR_ROLE_HINTS:
            if any(hint in agent.role for hint in hints):
                return owner
        return "dealix-pm"
    if agent.layer.value == "arm":
        return _ARM_ROLE_TO_LEGACY_OWNER.get(agent.role, "dealix-pm")
    return "dealix-pm"


def _attach_logical_identity(job: dict[str, Any], agent: LogicalAgent) -> dict[str, Any]:
    """Persist hierarchical identity while OWNER_AGENT remains an executor facade.

    The current Session Factory validator tolerates additional top-level fields,
    so these values survive durable job persistence without weakening the
    compatibility owner gate. They become first-class contract candidates for
    the next bounded Session Factory schema migration.
    """
    job.update(
        {
            "LOGICAL_AGENT_ID": agent.agent_id,
            "LOGICAL_AGENT_PARENT": agent.parent_id,
            "LOGICAL_AGENT_LAYER": agent.layer.value,
            "LOGICAL_AGENT_ROLE": agent.role,
            "LOGICAL_AGENT_SECTOR": agent.sector,
            "LOGICAL_AGENT_ARM_ID": agent.arm_id,
        }
    )
    return job


def render_session_job(
    request: SessionWorkRequest,
    *,
    agent: LogicalAgent,
    session_factory: Any,
) -> dict[str, Any]:
    item = request.work_item
    if item.material_external_effect:
        raise ValueError("material external effects must not be rendered as autonomous jobs")
    if item.agent_id != agent.agent_id:
        raise ValueError("work item agent does not match logical agent")

    context_refs = list(request.context_refs)
    context_refs.extend(
        [
            f"logical_agent:{agent.agent_id}",
            f"agent_parent:{agent.parent_id}",
            f"agent_layer:{agent.layer.value}",
            f"agent_role:{agent.role}",
        ]
    )
    if agent.sector:
        context_refs.append(f"sector:{agent.sector}")
    if agent.arm_id:
        context_refs.append(f"arm:{agent.arm_id}")

    job = session_factory.make_job(
        owner_agent=legacy_executor_owner(agent),
        business_goal=request.business_goal,
        job_class=request.job_class,
        authority_level=request.authority_level,
        economic_reason=request.economic_reason,
        priority=float(item.expected_economic_value),
        urgency=request.urgency,
        base_sha=request.base_sha,
        modifying=item.repo_writer,
        executor=dict(request.executor or {}),
        acceptance=dict(request.acceptance or {}),
        tests=list(request.tests),
        files_in_scope=list(request.files_in_scope),
        context_refs=context_refs,
        next_action=request.next_action,
    )
    return _attach_logical_identity(job, agent)


def render_dispatch_plan(
    plan: DispatchPlan,
    *,
    registry: Any,
    requests: Mapping[str, SessionWorkRequest],
    session_factory: Any,
) -> list[dict[str, Any]]:
    jobs: list[dict[str, Any]] = []
    for item in plan.selected:
        request = requests.get(item.work_id)
        if request is None:
            raise ValueError(f"missing session request for selected work: {item.work_id}")
        agent = registry.agents.get(item.agent_id)
        if agent is None:
            raise ValueError(f"logical agent disappeared after dispatch: {item.agent_id}")
        jobs.append(render_session_job(request, agent=agent, session_factory=session_factory))
    return jobs


def session_adapter_receipt(jobs: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    logical_identity_preserved = all(
        bool(job.get("LOGICAL_AGENT_ID"))
        and bool(job.get("LOGICAL_AGENT_PARENT"))
        and bool(job.get("LOGICAL_AGENT_LAYER"))
        and bool(job.get("LOGICAL_AGENT_ROLE"))
        and any(str(ref).startswith("logical_agent:") for ref in (job.get("CONTEXT_REFS") or []))
        for job in jobs
    )
    return {
        "jobs_rendered": len(jobs),
        "legacy_executor_owners": sorted({str(job.get("OWNER_AGENT")) for job in jobs}),
        "logical_agent_ids": sorted({str(job.get("LOGICAL_AGENT_ID")) for job in jobs if job.get("LOGICAL_AGENT_ID")}),
        "logical_identity_fields": list(LOGICAL_IDENTITY_FIELDS),
        "logical_identity_preserved": logical_identity_preserved,
        "submitted": False,
        "material_external_effects_executed": False,
    }
