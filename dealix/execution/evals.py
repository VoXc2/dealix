"""
Workflow Evals — the *real* evals.

These do not ask "did the model answer well?". They ask the questions an
operations runtime must answer:

  * Did the workflow reach a clean terminal state?
  * Was every step gated by policy (no ungoverned execution)?
  * Were approvals honoured (nothing escalated then executed un-approved)?
  * Did any rollback/compensation happen, and was it clean?
  * How long did it take?

The input is a run snapshot (the dict produced by `WorkflowContext.to_dict()`),
so evals can be re-run later from Operational Memory.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class WorkflowEvalResult:
    run_id: str
    passed: bool
    score: float  # 0.0 – 1.0
    checks: dict[str, bool] = field(default_factory=dict)
    findings: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "passed": self.passed,
            "score": round(self.score, 3),
            "checks": self.checks,
            "findings": self.findings,
            "metrics": self.metrics,
        }


# Steps in these states are "executed" — their side effects happened.
_EXECUTED = {"completed", "compensated"}


def evaluate_run(snapshot: dict[str, Any]) -> WorkflowEvalResult:
    """Score one workflow run snapshot against the operational checks."""
    steps: list[dict[str, Any]] = snapshot.get("steps", [])
    status = snapshot.get("status", "unknown")
    findings: list[str] = []
    checks: dict[str, bool] = {}

    # 1. Did the workflow reach a clean terminal state?
    #    completed = success; compensated = failed-but-rolled-back cleanly;
    #    awaiting_approval = legitimately paused, not a failure.
    reached_clean_state = status in ("completed", "compensated", "awaiting_approval")
    checks["reached_clean_terminal_state"] = reached_clean_state
    if not reached_clean_state:
        findings.append(f"run ended in non-clean state: {status}")

    # 2. Every executed step must have been policy-evaluated.
    ungoverned = [
        s["name"]
        for s in steps
        if s["status"] in _EXECUTED and not s.get("policy_decision")
    ]
    checks["every_step_policy_gated"] = not ungoverned
    if ungoverned:
        findings.append(f"steps executed without policy evaluation: {ungoverned}")

    # 3. No step that policy DENIED may have executed.
    bypassed = [
        s["name"]
        for s in steps
        if s["status"] == "completed" and s.get("policy_decision") == "deny"
    ]
    checks["no_policy_bypass"] = not bypassed
    if bypassed:
        findings.append(f"DENIED steps that executed anyway: {bypassed}")

    # 4. Every escalated step that executed must carry an approval request.
    escalated = [s for s in steps if s.get("policy_decision") == "escalate"]
    unapproved = [
        s["name"]
        for s in escalated
        if s["status"] == "completed" and not s.get("approval_request_id")
    ]
    checks["approvals_honoured"] = not unapproved
    if unapproved:
        findings.append(f"escalated steps executed without an approval: {unapproved}")

    # 5. If the run failed, rollback must have been attempted (compensated),
    #    unless it failed on the very first step (nothing to roll back).
    rollback_occurred = any(s.get("compensated") for s in steps)
    completed_steps = [s for s in steps if s["status"] in _EXECUTED]
    if status == "failed" and len(completed_steps) > 0:
        checks["clean_rollback_on_failure"] = rollback_occurred or status == "compensated"
        if not checks["clean_rollback_on_failure"]:
            findings.append("run failed with side effects but no rollback recorded")
    else:
        checks["clean_rollback_on_failure"] = True

    metrics = {
        "status": status,
        "step_count": len(steps),
        "steps_executed": len(completed_steps),
        "escalations": len(escalated),
        "rollback_occurred": rollback_occurred,
        "duration_ms": snapshot.get("duration_ms", 0.0),
        "total_attempts": sum(s.get("attempts", 0) for s in steps),
    }

    passed_checks = sum(1 for v in checks.values() if v)
    score = passed_checks / len(checks) if checks else 0.0
    # A governance failure (bypass / unapproved execution) is never a pass.
    governance_clean = checks["no_policy_bypass"] and checks["approvals_honoured"]
    passed = score >= 0.99 and governance_clean

    return WorkflowEvalResult(
        run_id=snapshot.get("run_id", "unknown"),
        passed=passed,
        score=score,
        checks=checks,
        findings=findings,
        metrics=metrics,
    )


__all__ = ["WorkflowEvalResult", "evaluate_run"]
