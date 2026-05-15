"""Deterministic workflow engine with retries, approvals, and rollback."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any, Callable

import yaml

from auto_client_acquisition.enterprise_infrastructure.schemas import (
    GovernanceOutcome,
    StepTrace,
    WorkflowDefinition,
    WorkflowRunMetrics,
    WorkflowRunResult,
    WorkflowStep,
    new_run_id,
)

StepEvaluator = Callable[[WorkflowStep], GovernanceOutcome]


class WorkflowDefinitionError(ValueError):
    """Raised when workflow definition YAML is invalid."""


def load_workflow_definition(path: str | Path) -> WorkflowDefinition:
    p = Path(path)
    if not p.exists():
        raise WorkflowDefinitionError(f"workflow definition not found: {p}")

    raw = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise WorkflowDefinitionError(f"workflow definition malformed: {p}")

    required = {"name", "trigger", "steps"}
    missing = required - set(raw.keys())
    if missing:
        raise WorkflowDefinitionError(f"workflow definition missing fields: {sorted(missing)}")

    steps_raw = raw.get("steps")
    if not isinstance(steps_raw, list) or not steps_raw:
        raise WorkflowDefinitionError("workflow definition requires non-empty 'steps' list")

    steps: list[WorkflowStep] = []
    for idx, item in enumerate(steps_raw):
        if not isinstance(item, dict):
            raise WorkflowDefinitionError(f"step[{idx}] is not an object")
        for key in ("id", "name", "action", "risk_level"):
            if key not in item:
                raise WorkflowDefinitionError(f"step[{idx}] missing key: {key}")
        steps.append(
            WorkflowStep(
                step_id=str(item["id"]),
                name=str(item["name"]),
                action=str(item["action"]),
                risk_level=str(item["risk_level"]),  # type: ignore[arg-type]
                max_retries=max(1, int(item.get("max_retries", 1))),
                requires_approval=bool(item.get("requires_approval", False)),
                estimated_value_sar=max(0, int(item.get("estimated_value_sar", 0))),
                rollback_on_failure=bool(item.get("rollback_on_failure", True)),
            )
        )

    return WorkflowDefinition(
        workflow_id=str(raw.get("workflow_id", f"wf::{raw['name']}")),
        name=str(raw["name"]),
        trigger=str(raw["trigger"]),
        steps=tuple(steps),
    )


def run_workflow(
    *,
    workflow: WorkflowDefinition,
    tenant_id: str,
    actor_role: str,
    evaluate_step: StepEvaluator,
    approvals: set[str] | None = None,
    forced_fail_steps: set[str] | None = None,
) -> WorkflowRunResult:
    granted_approvals = approvals or set()
    forced_fail = forced_fail_steps or set()
    run_id = new_run_id()
    started = perf_counter()

    traces: list[StepTrace] = []
    audit_log: list[dict[str, Any]] = []
    retries_total = 0
    approvals_requested = 0
    approvals_granted = 0
    completed_steps = 0
    rollback_events = 0
    value_generated_sar = 0
    executed_step_ids: list[str] = []
    blocked_step_id: str | None = None

    def _audit(step: WorkflowStep, event: str, notes: tuple[str, ...]) -> None:
        audit_log.append(
            {
                "run_id": run_id,
                "tenant_id": tenant_id,
                "step_id": step.step_id,
                "action": step.action,
                "event": event,
                "notes": list(notes),
                "timestamp": datetime.now(UTC).isoformat(),
            }
        )

    status = "completed"
    for step in workflow.steps:
        outcome = evaluate_step(step)
        approval_needed = outcome.decision == "require_approval" or step.requires_approval
        if approval_needed:
            approvals_requested += 1
            if step.step_id in granted_approvals:
                approvals_granted += 1
            else:
                blocked_step_id = step.step_id
                traces.append(
                    StepTrace(
                        step_id=step.step_id,
                        action=step.action,
                        decision="require_approval",
                        status="awaiting_approval",
                        attempt=0,
                        risk_score=outcome.risk_score,
                        notes=tuple(outcome.reasons),
                    )
                )
                _audit(step, "approval_pending", tuple(outcome.reasons))
                status = "paused_for_approval"
                break

        if outcome.decision == "block":
            blocked_step_id = step.step_id
            traces.append(
                StepTrace(
                    step_id=step.step_id,
                    action=step.action,
                    decision="block",
                    status="blocked",
                    attempt=0,
                    risk_score=outcome.risk_score,
                    notes=tuple(outcome.reasons),
                )
            )
            _audit(step, "blocked", tuple(outcome.reasons))
            status = "failed"
            break

        success = False
        for attempt in range(1, step.max_retries + 1):
            if attempt > 1:
                retries_total += 1
            failed_now = step.step_id in forced_fail
            traces.append(
                StepTrace(
                    step_id=step.step_id,
                    action=step.action,
                    decision="allow",
                    status="failed" if failed_now else "completed",
                    attempt=attempt,
                    risk_score=outcome.risk_score,
                    notes=tuple(outcome.reasons),
                )
            )
            _audit(step, "failed" if failed_now else "completed", tuple(outcome.reasons))
            if failed_now:
                continue

            success = True
            completed_steps += 1
            executed_step_ids.append(step.step_id)
            value_generated_sar += step.estimated_value_sar
            break

        if success:
            continue

        blocked_step_id = step.step_id
        if step.rollback_on_failure and executed_step_ids:
            rollback_events = len(executed_step_ids)
            for executed_step_id in reversed(executed_step_ids):
                traces.append(
                    StepTrace(
                        step_id=executed_step_id,
                        action="rollback",
                        decision="allow",
                        status="rolled_back",
                        attempt=1,
                        risk_score=0,
                        notes=("rollback_triggered_by_failure", step.step_id),
                    )
                )
                audit_log.append(
                    {
                        "run_id": run_id,
                        "tenant_id": tenant_id,
                        "step_id": executed_step_id,
                        "action": "rollback",
                        "event": "rolled_back",
                        "notes": ["rollback_triggered_by_failure", step.step_id],
                        "timestamp": datetime.now(UTC).isoformat(),
                    }
                )
            value_generated_sar = 0
            status = "rolled_back"
        else:
            status = "failed"
        break

    duration_ms = int((perf_counter() - started) * 1000)
    metrics = WorkflowRunMetrics(
        total_steps=len(workflow.steps),
        completed_steps=completed_steps,
        retries_total=retries_total,
        approvals_requested=approvals_requested,
        approvals_granted=approvals_granted,
        value_generated_sar=value_generated_sar,
        rollback_events=rollback_events,
        duration_ms=duration_ms,
    )
    return WorkflowRunResult(
        run_id=run_id,
        workflow_id=workflow.workflow_id,
        status=status,  # type: ignore[arg-type]
        tenant_id=tenant_id,
        actor_role=actor_role,
        blocked_step_id=blocked_step_id,
        traces=tuple(traces),
        audit_log=tuple(audit_log),
        metrics=metrics,
    )
