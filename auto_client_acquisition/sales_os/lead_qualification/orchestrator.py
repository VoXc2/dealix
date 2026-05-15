"""Executable orchestrator for the lead_qualification governed workflow.

Drives the ``workflow_os_v10`` state machine through the 13-step pipeline
declared in ``data/workflows/lead_qualification.yaml``. It does not
reimplement governance, scoring, approval, or observability — it wires
the existing canonical modules together and threads ``governance_decision``,
tracing, audit, rollback, and an eval report through every step.

Public API:
  - ``run_lead_qualification(lead, deps=None)`` — runs steps 1-9; with
    ``auto_approve`` it continues to step 13, otherwise it returns paused.
  - ``resume_lead_qualification(run_id, deps=None, approver=...)`` —
    approves the pending request and runs steps 10-13.
"""

from __future__ import annotations

import copy
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from auto_client_acquisition.agent_observability.trace import record_trace
from auto_client_acquisition.approval_center.approval_store import (
    ApprovalStore,
    get_default_approval_store,
)
from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.sales_os.lead_qualification.sales_agent import (
    DraftLLM,
    ensure_sales_agent_identity,
)
from auto_client_acquisition.sales_os.lead_qualification.schemas import (
    LeadInput,
    StepResult,
    WorkflowOutput,
    worst_governance,
)
from auto_client_acquisition.sales_os.lead_qualification.steps import (
    WORKFLOW_NAME,
    step_approval,
    step_crm_update,
    step_draft_response,
    step_eval_report,
    step_executive_dashboard,
    step_knowledge_retrieval,
    step_lead_intake,
    step_lead_scoring,
    step_metrics_emission,
    step_qualification,
    step_rbac_check,
    step_risk_check,
    step_tenant_detection,
    timed,
)
from auto_client_acquisition.workflow_os_v10.schemas import WorkflowDefinition, WorkflowRun
from auto_client_acquisition.workflow_os_v10.state_machine import (
    advance_workflow,
    block_workflow,
    get_run,
    start_workflow,
)

_SPEC_PATH = Path(__file__).resolve().parents[3] / "data" / "workflows" / "lead_qualification.yaml"

# step_id, function, observability action_mode, audit actor
_STEPS: list[tuple[str, Callable[..., StepResult], str, str]] = [
    ("lq_lead_intake", step_lead_intake, "draft_only", "system"),
    ("lq_tenant_detection", step_tenant_detection, "draft_only", "system"),
    ("lq_rbac_check", step_rbac_check, "draft_only", "system"),
    ("lq_knowledge_retrieval", step_knowledge_retrieval, "draft_only", "sales_agent"),
    ("lq_qualification", step_qualification, "draft_only", "sales_agent"),
    ("lq_lead_scoring", step_lead_scoring, "draft_only", "sales_agent"),
    ("lq_draft_response", step_draft_response, "draft_only", "sales_agent"),
    ("lq_risk_check", step_risk_check, "draft_only", "system"),
    ("lq_approval", step_approval, "approval_required", "founder"),
    ("lq_crm_update", step_crm_update, "approved_execute", "system"),
    ("lq_metrics_emission", step_metrics_emission, "approved_execute", "system"),
    ("lq_eval_report", step_eval_report, "approved_execute", "system"),
    ("lq_executive_dashboard", step_executive_dashboard, "approved_execute", "founder"),
]
_APPROVAL_INDEX = 8

_BLOCK = str(GovernanceDecision.BLOCK)

# Default RBAC: mirrors the system roles seeded by db/models.py RoleRecord.
_DEFAULT_ROLE_PERMISSIONS: dict[str, list[str]] = {
    "owner": ["admin:*"],
    "admin": ["leads:read", "leads:write", "deals:read", "deals:write", "agents:run"],
    "sales_rep": ["leads:read", "leads:write", "deals:read", "agents:run"],
    "agent_operator": ["leads:read", "agents:run"],
    "viewer": ["leads:read", "deals:read"],
}


def load_workflow_spec() -> dict[str, Any]:
    """Load the declarative workflow spec from data/workflows/."""
    with _SPEC_PATH.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def build_definition() -> WorkflowDefinition:
    """Build the v10 WorkflowDefinition from the YAML declaration."""
    spec = load_workflow_spec()
    return WorkflowDefinition(
        workflow_id=WORKFLOW_NAME,
        name=spec["name"],
        description_ar=spec.get("description_ar", ""),
        description_en=spec.get("description_en", ""),
        steps=[s["step_id"] for s in spec["steps"]],
    )


def _default_tenant_resolver(slug: str) -> dict[str, Any] | None:
    if not slug or not slug.strip():
        return None
    return {"tenant_id": f"tnt_{slug}", "slug": slug, "status": "active"}


def _default_rbac_resolver(slug: str, role: str) -> list[str]:
    return list(_DEFAULT_ROLE_PERMISSIONS.get(role, []))


def _default_knowledge_retriever(lead: LeadInput) -> list[dict[str, Any]]:
    return [
        {
            "id": f"sector_brief:{lead.sector}",
            "excerpt": (
                f"Sector brief for {lead.sector}: governed B2B engagement, "
                "consent-based outreach, evidence-backed proof."
            ),
        }
    ]


@dataclass(slots=True)
class WorkflowDeps:
    """Injectable dependencies — production wires real ones, tests pass stubs."""

    tenant_resolver: Callable[[str], dict[str, Any] | None] = _default_tenant_resolver
    rbac_resolver: Callable[[str, str], list[str]] = _default_rbac_resolver
    knowledge_retriever: Callable[[LeadInput], list[dict[str, Any]]] = _default_knowledge_retriever
    llm: DraftLLM | None = None
    approval_store: ApprovalStore = field(default_factory=get_default_approval_store)
    auto_approve: bool = False
    approver: str = "founder"


def _snapshot(run: WorkflowRun) -> dict[str, Any]:
    return copy.deepcopy(dict(run.checkpoint))


def _restore(run: WorkflowRun, snapshot: dict[str, Any]) -> None:
    run.checkpoint.clear()
    run.checkpoint.update(copy.deepcopy(snapshot))


def _append_step(run: WorkflowRun, result: StepResult) -> None:
    run.checkpoint.setdefault("step_results", []).append(result.to_dict())


def _audit(run: WorkflowRun, result: StepResult, actor: str) -> None:
    run.checkpoint.setdefault("audit", []).append({
        "step_id": result.step_id,
        "at": datetime.now(UTC).isoformat(),
        "actor": actor,
        "governance_decision": result.governance_decision,
        "blocked": result.blocked,
        "idempotency_key": f"{run.run_id}:{result.step_id}",
    })


def _audit_event(run: WorkflowRun, event: str, detail: dict[str, Any]) -> None:
    run.checkpoint.setdefault("audit", []).append({
        "step_id": event,
        "at": datetime.now(UTC).isoformat(),
        "actor": detail.get("who", "system"),
        "governance_decision": detail.get("governance_decision", ""),
        "blocked": False,
        "detail": detail,
    })


def _trace(run: WorkflowRun, lead: LeadInput, action_mode: str, result: StepResult,
           *, degraded: bool = False, approved: bool = False) -> None:
    record_trace(
        agent_name="sales_agent",
        action_mode="blocked" if result.blocked else action_mode,  # type: ignore[arg-type]
        customer_handle=lead.company_name,
        workflow=WORKFLOW_NAME,
        input_kind=result.step_id,
        output_kind=result.artifact_kind,
        latency_ms=result.latency_ms,
        guardrail_result=result.governance_decision,
        approval_status="approved" if approved else "pending",
        degraded=degraded,
        error_type=result.reason if result.blocked else None,
        payload={
            "step": result.step_id,
            "artifact_kind": result.artifact_kind,
            "decision": result.governance_decision,
        },
    )


def _finalize(run: WorkflowRun, *, blocked_reason: str = "") -> WorkflowOutput:
    step_results = run.checkpoint.get("step_results", [])
    overall = worst_governance([r["governance_decision"] for r in step_results])
    return WorkflowOutput(
        run_id=run.run_id,
        workflow_id=run.workflow_id,
        state=run.state,
        governance_decision=overall,
        steps=step_results,
        audit=run.checkpoint.get("audit", []),
        eval_report=run.checkpoint.get("eval", {}),
        dashboard_card=run.checkpoint.get("dashboard_card", {}),
        approval_id=run.checkpoint.get("approval_id", ""),
        blocked_reason=blocked_reason,
    )


def _execute(run: WorkflowRun, lead: LeadInput, deps: WorkflowDeps,
             start_index: int) -> WorkflowOutput:
    for idx in range(start_index, len(_STEPS)):
        step_id, fn, action_mode, actor = _STEPS[idx]
        snapshot = _snapshot(run)
        try:
            result = timed(fn, run, lead, deps)
        except Exception as exc:  # no_silent_failures: surfaced, never swallowed
            result = StepResult(
                step_id, "error", _BLOCK, ok=False, blocked=True,
                reason=f"step_exception:{type(exc).__name__}:{exc}",
            )

        # Every step output must carry a governance decision.
        if not result.governance_decision:
            _restore(run, snapshot)
            raise RuntimeError(f"step {step_id} produced no governance_decision")

        if result.blocked:
            _restore(run, snapshot)  # rollback partial writes from the failed step
            _append_step(run, result)
            _audit(run, result, actor)
            _trace(run, lead, action_mode, result, degraded=True)
            block_workflow(run, result.reason)
            return _finalize(run, blocked_reason=result.reason)

        _append_step(run, result)
        _audit(run, result, actor)
        approved = idx > _APPROVAL_INDEX
        _trace(run, lead, action_mode, result, approved=approved)

        if idx == _APPROVAL_INDEX and not deps.auto_approve:
            run.state = "paused_for_approval"
            run.updated_at = datetime.now(UTC)
            return _finalize(run)

        if idx == _APPROVAL_INDEX and deps.auto_approve:
            approval_id = run.checkpoint["approval_id"]
            deps.approval_store.approve(approval_id, deps.approver)
            _audit_event(run, "approval_granted",
                         {"who": deps.approver, "approval_id": approval_id})

        advance_workflow(run, step_id, idempotency_key=f"{run.run_id}:{step_id}",
                         result=result.artifact)

    return _finalize(run)


def run_lead_qualification(lead: LeadInput,
                           deps: WorkflowDeps | None = None) -> WorkflowOutput:
    """Run the lead_qualification workflow from intake.

    Without ``auto_approve`` the run stops at ``paused_for_approval`` after
    creating the approval request; call ``resume_lead_qualification`` to
    finish it once the founder has approved.
    """
    deps = deps or WorkflowDeps()
    ensure_sales_agent_identity()  # no agent without identity
    definition = build_definition()
    run = start_workflow(definition, customer_handle=lead.company_name)
    run.checkpoint["lead"] = lead_to_dict(lead)
    run.checkpoint["step_results"] = []
    run.checkpoint["audit"] = []
    return _execute(run, lead, deps, start_index=0)


def resume_lead_qualification(run_id: str, deps: WorkflowDeps | None = None,
                              *, approver: str = "founder") -> WorkflowOutput:
    """Approve the pending request and finish a paused run (steps 10-13)."""
    deps = deps or WorkflowDeps()
    run = get_run(run_id)
    if run.state != "paused_for_approval":
        return _finalize(run)
    lead = LeadInput.from_dict(run.checkpoint["lead"])
    approval_id = run.checkpoint["approval_id"]
    deps.approval_store.approve(approval_id, approver)
    _audit_event(run, "approval_granted", {"who": approver, "approval_id": approval_id})
    advance_workflow(run, "lq_approval",
                     idempotency_key=f"{run.run_id}:lq_approval",
                     result=run.checkpoint.get("approval", {}))
    return _execute(run, lead, deps, start_index=_APPROVAL_INDEX + 1)


def lead_to_dict(lead: LeadInput) -> dict[str, Any]:
    return {f: getattr(lead, f) for f in LeadInput.__dataclass_fields__}


__all__ = [
    "WorkflowDeps",
    "build_definition",
    "lead_to_dict",
    "load_workflow_spec",
    "resume_lead_qualification",
    "run_lead_qualification",
]
