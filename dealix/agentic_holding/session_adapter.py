from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
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


def resolve_live_base_sha(
    session_factory: Any,
    *,
    repo_root: Path | str | None = None,
) -> str:
    """Resolve an exact live base; never inherit the legacy frozen default."""
    native = getattr(session_factory, "resolve_default_base_sha", None)
    if callable(native):
        value = str(native()).strip()
        if value:
            return value

    repo = Path(repo_root or getattr(session_factory, "REPO_ROOT", Path.cwd()))
    git = shutil.which("git")
    if not git:
        raise RuntimeError("git is required to resolve Agentic Holding live base")

    explicit = os.environ.get("DEALIX_AGENTIC_BASE_SHA", "").strip()
    default_ref = os.environ.get("DEALIX_AGENTIC_BASE_REF", "origin/main").strip() or "origin/main"
    candidates = (explicit,) if explicit else (default_ref, "HEAD")
    for candidate in candidates:
        result = subprocess.run(
            [git, "-C", str(repo), "rev-parse", "--verify", f"{candidate}^{{commit}}"],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        resolved = result.stdout.strip()
        if result.returncode == 0 and resolved:
            return resolved
    raise RuntimeError(f"unable to resolve Agentic Holding live base from {candidates}")


def _attach_logical_identity(job: dict[str, Any], agent: LogicalAgent) -> dict[str, Any]:
    """Persist hierarchy while OWNER_AGENT remains a compatibility facade."""
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

    base_sha = request.base_sha or resolve_live_base_sha(session_factory)
    context_refs.append(f"agentic_base_sha:{base_sha}")
    job = session_factory.make_job(
        owner_agent=legacy_executor_owner(agent),
        business_goal=request.business_goal,
        job_class=request.job_class,
        authority_level=request.authority_level,
        economic_reason=request.economic_reason,
        priority=float(item.expected_economic_value),
        urgency=request.urgency,
        base_sha=base_sha,
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


def submit_dispatch_plan(
    plan: DispatchPlan,
    *,
    registry: Any,
    requests: Mapping[str, SessionWorkRequest],
    session_factory: Any,
    state_root: Path,
    execute: bool = False,
    repo_root: Path | None = None,
    worktree_root: Path | None = None,
) -> dict[str, Any]:
    """Use the canonical Session Factory; never create a second durable queue."""
    jobs = render_dispatch_plan(
        plan,
        registry=registry,
        requests=requests,
        session_factory=session_factory,
    )
    submissions: list[dict[str, Any]] = []
    executions: list[dict[str, Any]] = []
    for job in jobs:
        submitted = session_factory.submit_job(state_root, job)
        submitted_job = submitted.get("job") or job
        submissions.append(
            {
                "JOB_ID": job.get("JOB_ID"),
                "ok": bool(submitted.get("ok")),
                "status": submitted_job.get("STATUS"),
            }
        )
        if execute and submitted.get("ok") and submitted_job.get("STATUS") == "READY":
            outcome = session_factory.run_job(
                state_root,
                submitted_job,
                repo_root=repo_root or getattr(session_factory, "REPO_ROOT", None),
                worktree_root=worktree_root,
            )
            executions.append(
                {
                    "JOB_ID": submitted_job.get("JOB_ID"),
                    "ok": bool(outcome.get("ok")),
                    "status": outcome.get("status"),
                }
            )
    return {
        **session_adapter_receipt(jobs),
        "submitted": True,
        "execute_requested": execute,
        "governor_worker_slots": plan.budget.worker_slots,
        "governor_writer_slots": plan.budget.writer_slots,
        "submissions": submissions,
        "executions": executions,
    }


def session_adapter_receipt(jobs: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    logical_identity_preserved = all(
        bool(job.get("LOGICAL_AGENT_ID"))
        and bool(job.get("LOGICAL_AGENT_PARENT"))
        and bool(job.get("LOGICAL_AGENT_LAYER"))
        and bool(job.get("LOGICAL_AGENT_ROLE"))
        and any(str(ref).startswith("logical_agent:") for ref in (job.get("CONTEXT_REFS") or []))
        for job in jobs
    )
    base_shas = sorted({str(job.get("BASE_SHA")) for job in jobs if job.get("BASE_SHA")})
    return {
        "jobs_rendered": len(jobs),
        "legacy_executor_owners": sorted({str(job.get("OWNER_AGENT")) for job in jobs}),
        "logical_agent_ids": sorted({str(job.get("LOGICAL_AGENT_ID")) for job in jobs if job.get("LOGICAL_AGENT_ID")}),
        "logical_identity_fields": list(LOGICAL_IDENTITY_FIELDS),
        "logical_identity_preserved": logical_identity_preserved,
        "explicit_base_sha": bool(jobs) and len(base_shas) == 1,
        "base_shas": base_shas,
        "submitted": False,
        "material_external_effects_executed": False,
    }
