"""Governed workflow runtime for the execution-fabric foundation.

This module intentionally stays small and deterministic so it can be used
as the first "operational layer" primitive:

trigger -> steps -> tool calls -> retries -> risk checks -> approvals
-> execution -> metrics -> audit log
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Literal
from uuid import uuid4

import yaml

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision

RiskLevel = Literal["low", "medium", "high"]
RunStatus = Literal["completed", "blocked", "failed", "paused_for_approval"]


@dataclass(frozen=True, slots=True)
class WorkflowStepDefinition:
    """Static step definition loaded from YAML."""

    step_id: str
    action: str
    tool: str
    risk_level: RiskLevel
    max_retries: int = 0
    approval_required: bool = False


@dataclass(frozen=True, slots=True)
class WorkflowDefinition:
    """Static governed workflow definition."""

    name: str
    version: str
    trigger_type: str
    trigger_source: str
    steps: tuple[WorkflowStepDefinition, ...]


@dataclass(frozen=True, slots=True)
class StepExecutionResult:
    """Outcome of one executed step."""

    step_id: str
    status: Literal["completed", "blocked", "failed", "awaiting_approval"]
    decision: GovernanceDecision
    risk_score: float
    retries_used: int
    output: dict[str, Any] = field(default_factory=dict)
    error: str = ""


@dataclass(frozen=True, slots=True)
class AuditRecord:
    """Single auditable runtime record."""

    stage: str
    step_id: str
    decision: str
    details: dict[str, Any]


@dataclass(frozen=True, slots=True)
class RunMetrics:
    """Operational metrics for the workflow run."""

    steps_total: int
    steps_completed: int
    steps_failed: int
    retries_total: int
    approvals_required: int
    approvals_granted: int
    approvals_denied: int


@dataclass(frozen=True, slots=True)
class GovernedWorkflowRunReport:
    """Full run report used by executive/reporting layers."""

    run_id: str
    workflow_name: str
    workflow_version: str
    status: RunStatus
    executed_steps: tuple[StepExecutionResult, ...]
    metrics: RunMetrics
    audit_log: tuple[AuditRecord, ...]


RiskScorer = Callable[[dict[str, Any], WorkflowStepDefinition], float]
PolicyChecker = Callable[
    [dict[str, Any], WorkflowStepDefinition, float],
    GovernanceDecision,
]
ApprovalChecker = Callable[
    [dict[str, Any], WorkflowStepDefinition, GovernanceDecision],
    bool,
]
ToolExecutor = Callable[[dict[str, Any], WorkflowStepDefinition], dict[str, Any]]


def load_workflow_definition(path: Path) -> WorkflowDefinition:
    """Load a governed workflow definition from YAML."""
    with path.open("r", encoding="utf-8") as file_obj:
        data = yaml.safe_load(file_obj)

    if not isinstance(data, dict):
        raise ValueError("workflow definition must be a mapping")

    required_keys = {"name", "version", "trigger", "steps"}
    missing = required_keys - set(data.keys())
    if missing:
        raise ValueError(f"workflow definition missing keys: {sorted(missing)}")

    trigger = data.get("trigger")
    if not isinstance(trigger, dict):
        raise ValueError("trigger must be a mapping")
    trigger_type = str(trigger.get("type", "")).strip()
    trigger_source = str(trigger.get("source", "")).strip()
    if not trigger_type or not trigger_source:
        raise ValueError("trigger.type and trigger.source are required")

    raw_steps = data.get("steps")
    if not isinstance(raw_steps, list) or not raw_steps:
        raise ValueError("steps must be a non-empty list")

    parsed_steps: list[WorkflowStepDefinition] = []
    for raw in raw_steps:
        if not isinstance(raw, dict):
            raise ValueError("each step must be a mapping")
        parsed_steps.append(
            WorkflowStepDefinition(
                step_id=str(raw.get("step_id", "")).strip(),
                action=str(raw.get("action", "")).strip(),
                tool=str(raw.get("tool", "")).strip(),
                risk_level=str(raw.get("risk_level", "low")).strip(),  # type: ignore[arg-type]
                max_retries=max(0, int(raw.get("max_retries", 0))),
                approval_required=bool(raw.get("approval_required", False)),
            )
        )

    for step in parsed_steps:
        if not step.step_id or not step.action or not step.tool:
            raise ValueError("step_id, action, and tool are required per step")
        if step.risk_level not in {"low", "medium", "high"}:
            raise ValueError(f"invalid risk_level {step.risk_level!r} in step {step.step_id}")

    return WorkflowDefinition(
        name=str(data["name"]).strip(),
        version=str(data["version"]).strip(),
        trigger_type=trigger_type,
        trigger_source=trigger_source,
        steps=tuple(parsed_steps),
    )


def default_risk_scorer(context: dict[str, Any], step: WorkflowStepDefinition) -> float:
    """Simple deterministic risk scorer.

    Adds signal-based adjustments on top of the step's baseline risk level.
    """
    base_by_level = {"low": 0.25, "medium": 0.55, "high": 0.8}
    base = base_by_level[step.risk_level]
    trigger = context.get("trigger", {})
    if isinstance(trigger, dict) and trigger.get("contains_pii"):
        base += 0.15
    if isinstance(trigger, dict) and trigger.get("high_value_deal"):
        base += 0.1
    return min(1.0, round(base, 3))


def default_policy_checker(
    context: dict[str, Any],
    step: WorkflowStepDefinition,
    risk_score: float,
) -> GovernanceDecision:
    """Default governance policy for smallest governed workflow."""
    del context
    if risk_score >= 0.95:
        return GovernanceDecision.BLOCK
    if risk_score >= 0.7:
        return GovernanceDecision.REQUIRE_APPROVAL
    if step.action.startswith("external_"):
        return GovernanceDecision.REQUIRE_APPROVAL
    return GovernanceDecision.ALLOW


def default_approval_checker(
    context: dict[str, Any],
    step: WorkflowStepDefinition,
    decision: GovernanceDecision,
) -> bool:
    """Default approval path: explicit trigger flag required for risky actions."""
    del step
    if decision in {GovernanceDecision.REQUIRE_APPROVAL, GovernanceDecision.ESCALATE}:
        trigger = context.get("trigger", {})
        if isinstance(trigger, dict):
            return bool(trigger.get("auto_approve", False))
        return False
    return True


def execute_governed_workflow(
    *,
    definition: WorkflowDefinition,
    trigger_payload: dict[str, Any],
    tool_registry: dict[str, ToolExecutor],
    risk_scorer: RiskScorer = default_risk_scorer,
    policy_checker: PolicyChecker = default_policy_checker,
    approval_checker: ApprovalChecker = default_approval_checker,
) -> GovernedWorkflowRunReport:
    """Execute a governed workflow and return run metrics + audit trail."""
    context: dict[str, Any] = {
        "trigger": dict(trigger_payload),
        "outputs": {},
    }
    executed_steps: list[StepExecutionResult] = []
    audit_log: list[AuditRecord] = []
    retries_total = 0
    approvals_required = 0
    approvals_granted = 0
    approvals_denied = 0
    status: RunStatus = "completed"

    for step in definition.steps:
        risk_score = float(risk_scorer(context, step))
        decision = policy_checker(context, step, risk_score)
        audit_log.append(
            AuditRecord(
                stage="policy_check",
                step_id=step.step_id,
                decision=decision.value,
                details={"risk_score": risk_score},
            )
        )

        if decision == GovernanceDecision.BLOCK:
            status = "blocked"
            executed_steps.append(
                StepExecutionResult(
                    step_id=step.step_id,
                    status="blocked",
                    decision=decision,
                    risk_score=risk_score,
                    retries_used=0,
                    error="blocked_by_policy",
                )
            )
            break

        needs_approval = step.approval_required or decision in {
            GovernanceDecision.REQUIRE_APPROVAL,
            GovernanceDecision.ESCALATE,
            GovernanceDecision.DRAFT_ONLY,
        }
        if needs_approval:
            approvals_required += 1
            approved = approval_checker(context, step, decision)
            audit_log.append(
                AuditRecord(
                    stage="approval_check",
                    step_id=step.step_id,
                    decision="approved" if approved else "denied",
                    details={"required": True},
                )
            )
            if not approved:
                approvals_denied += 1
                status = "paused_for_approval"
                executed_steps.append(
                    StepExecutionResult(
                        step_id=step.step_id,
                        status="awaiting_approval",
                        decision=decision,
                        risk_score=risk_score,
                        retries_used=0,
                    )
                )
                break
            approvals_granted += 1

        executor = tool_registry.get(step.tool)
        if executor is None:
            status = "failed"
            executed_steps.append(
                StepExecutionResult(
                    step_id=step.step_id,
                    status="failed",
                    decision=decision,
                    risk_score=risk_score,
                    retries_used=0,
                    error=f"missing_tool:{step.tool}",
                )
            )
            break

        attempts = 0
        while True:
            attempts += 1
            try:
                output = executor(context, step)
                context["outputs"][step.step_id] = output
                executed_steps.append(
                    StepExecutionResult(
                        step_id=step.step_id,
                        status="completed",
                        decision=decision,
                        risk_score=risk_score,
                        retries_used=max(0, attempts - 1),
                        output=output,
                    )
                )
                audit_log.append(
                    AuditRecord(
                        stage="execution",
                        step_id=step.step_id,
                        decision="completed",
                        details={"attempt": attempts, "tool": step.tool},
                    )
                )
                break
            except Exception as exc:  # pragma: no cover - branch asserted in tests
                if attempts > step.max_retries:
                    status = "failed"
                    executed_steps.append(
                        StepExecutionResult(
                            step_id=step.step_id,
                            status="failed",
                            decision=decision,
                            risk_score=risk_score,
                            retries_used=max(0, attempts - 1),
                            error=str(exc)[:500],
                        )
                    )
                    audit_log.append(
                        AuditRecord(
                            stage="execution",
                            step_id=step.step_id,
                            decision="failed",
                            details={"attempts": attempts, "error": str(exc)[:200]},
                        )
                    )
                    break
                retries_total += 1
                audit_log.append(
                    AuditRecord(
                        stage="retry",
                        step_id=step.step_id,
                        decision="retrying",
                        details={"attempt": attempts, "error": str(exc)[:200]},
                    )
                )
        if status == "failed":
            break

    steps_completed = sum(1 for item in executed_steps if item.status == "completed")
    steps_failed = sum(1 for item in executed_steps if item.status == "failed")
    metrics = RunMetrics(
        steps_total=len(definition.steps),
        steps_completed=steps_completed,
        steps_failed=steps_failed,
        retries_total=retries_total,
        approvals_required=approvals_required,
        approvals_granted=approvals_granted,
        approvals_denied=approvals_denied,
    )

    return GovernedWorkflowRunReport(
        run_id=f"gwf_{uuid4().hex[:16]}",
        workflow_name=definition.name,
        workflow_version=definition.version,
        status=status,
        executed_steps=tuple(executed_steps),
        metrics=metrics,
        audit_log=tuple(audit_log),
    )
