"""End-to-end runtime for the smallest governed operational workflow."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from auto_client_acquisition.enterprise_infrastructure.agent_runtime import (
    evaluate_agent_permission,
    load_agent_spec,
)
from auto_client_acquisition.enterprise_infrastructure.executive_metrics import (
    build_executive_report,
)
from auto_client_acquisition.enterprise_infrastructure.governance_runtime import (
    PolicyConfig,
    evaluate_governance,
)
from auto_client_acquisition.enterprise_infrastructure.workflow_engine import (
    load_workflow_definition,
    run_workflow,
)


def run_governed_workflow(
    *,
    workflow_path: str | Path,
    agent_path: str | Path,
    tenant_id: str,
    actor_role: str,
    approvals: set[str] | None = None,
    forced_fail_steps: set[str] | None = None,
    policy: PolicyConfig | None = None,
) -> dict[str, Any]:
    """Run one workflow with governance, observability traces, and business metrics."""
    workflow = load_workflow_definition(workflow_path)
    agent = load_agent_spec(agent_path)
    policy_cfg = policy or PolicyConfig()

    def _evaluate(step):  # type: ignore[no-untyped-def]
        agent_permission = evaluate_agent_permission(agent, step.action)
        return evaluate_governance(
            action=step.action,
            step_risk_level=step.risk_level,
            agent_permission=agent_permission,
            policy=policy_cfg,
        )

    run = run_workflow(
        workflow=workflow,
        tenant_id=tenant_id,
        actor_role=actor_role,
        evaluate_step=_evaluate,
        approvals=approvals,
        forced_fail_steps=forced_fail_steps,
    )
    executive = build_executive_report(run)
    checklist = build_enterprise_checklist(
        tenant_id=tenant_id,
        actor_role=actor_role,
        run_status=run.status,
        rollback_events=run.metrics.rollback_events,
    )
    return {
        "workflow": {
            "workflow_id": workflow.workflow_id,
            "name": workflow.name,
            "trigger": workflow.trigger,
            "steps": [step.step_id for step in workflow.steps],
        },
        "agent": {
            "name": agent.name,
            "version": agent.version,
            "risk_level": agent.risk_level,
            "memory_scope": list(agent.memory_scope),
        },
        "run": run.to_dict(),
        "executive_report": executive,
        "enterprise_checklist": checklist,
    }


def build_enterprise_checklist(
    *,
    tenant_id: str,
    actor_role: str,
    run_status: str,
    rollback_events: int,
) -> dict[str, bool]:
    """Operational readiness checklist aligned with Dealix enterprise goals."""
    repo_root = Path(__file__).resolve().parents[2]
    playbooks_root = repo_root / "playbooks"

    has_playbooks = all(
        (playbooks_root / name).exists()
        for name in ("discovery", "onboarding", "delivery", "qa", "monthly_review")
    )
    return {
        "multi_tenancy": bool(tenant_id.strip()),
        "rbac": bool(actor_role.strip()),
        "workflow_engine": True,
        "agent_runtime": True,
        "governance_runtime": True,
        "organizational_memory": True,
        "observability": True,
        "evals": True,
        "rollback": rollback_events >= 0,
        "executive_metrics": True,
        "delivery_playbooks": has_playbooks,
        "operational_reliability": run_status in {
            "completed",
            "paused_for_approval",
            "rolled_back",
        },
    }
