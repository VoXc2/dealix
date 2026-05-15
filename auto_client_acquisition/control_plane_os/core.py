"""System 26 — the Organizational Control Plane.

Central control over every workflow run: register, monitor, pause, resume,
rollback, trace, re-route, and live-edit attached policies — in real time.

The control plane is a governance + observability layer *over* workflows. It
never executes external actions itself. Rollbacks and policy edits are
state-changing, so they route through the approval gate (approval-first); the
compensating action only runs once the ticket is granted.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.control_plane_os.approval_gate import (
    ApprovalGateError,
    ApprovalTicket,
    ControlApprovalGate,
    get_approval_gate,
)
from auto_client_acquisition.control_plane_os.ledger import (
    ControlEventType,
    ControlLedger,
    emit,
    get_control_ledger,
)
from auto_client_acquisition.control_plane_os.schemas import (
    PolicyEdit,
    RunState,
    RunStatus,
    RunTrace,
    WorkflowRun,
)

_MODULE = "control_plane_os"


class ControlPlaneError(RuntimeError):
    """Raised on an invalid control-plane operation — never swallowed."""


class ControlPlane:
    """Supervises workflow runs. Wraps the orchestrator's TaskQueue when wired."""

    def __init__(
        self,
        *,
        task_queue: Any | None = None,
        ledger: ControlLedger | None = None,
        gate: ControlApprovalGate | None = None,
    ) -> None:
        self._runs: dict[str, WorkflowRun] = {}
        self._task_queue = task_queue  # orchestrator.queue.TaskQueue, optional
        self._ledger = ledger or get_control_ledger()
        self._gate = gate or get_approval_gate()

    # ── registration ─────────────────────────────────────────────
    def register_run(
        self,
        *,
        workflow_id: str,
        customer_id: str,
        correlation_id: str | None = None,
        actor: str = "system",
        attached_policy_ids: list[str] | None = None,
    ) -> WorkflowRun:
        run = WorkflowRun(
            workflow_id=workflow_id,
            customer_id=customer_id,
            correlation_id=correlation_id,
            state=RunState.RUNNING,
            attached_policy_ids=attached_policy_ids or [],
        )
        self._runs[run.run_id] = run
        self._emit(ControlEventType.RUN_REGISTERED, run, actor)
        return run

    # ── observability ────────────────────────────────────────────
    def monitor(self, run_id: str) -> RunStatus:
        """Read-only live snapshot — joins ledger events + task queue."""
        run = self._require(run_id)
        events = self._ledger.list_events(run_id=run_id, limit=500)
        task_summary = self._task_summary(run.workflow_id)
        awaiting = [
            t.ticket_id for t in self._gate.list_pending() if t.run_id == run_id
        ]
        return RunStatus(
            run=run,
            task_summary=task_summary,
            events_count=len(events),
            awaiting_approval=awaiting,
        )

    def trace(self, run_id: str) -> RunTrace:
        """Full ordered event timeline for a run (read-only)."""
        self._require(run_id)
        events = self._ledger.list_events(run_id=run_id, limit=1000)
        events.sort(key=lambda e: e.occurred_at)
        timeline = [
            {
                "occurred_at": e.occurred_at.isoformat(),
                "event_type": str(e.event_type),
                "actor": e.actor,
                "decision": e.decision,
                "source_module": e.source_module,
            }
            for e in events
        ]
        return RunTrace(run_id=run_id, events=events, timeline=timeline)

    def list_runs(self, *, state: str | None = None) -> list[WorkflowRun]:
        runs = list(self._runs.values())
        if state:
            runs = [r for r in runs if str(r.state) == state]
        return runs

    # ── live control ─────────────────────────────────────────────
    def pause(self, run_id: str, *, actor: str = "system") -> WorkflowRun:
        run = self._require(run_id)
        if run.state not in (RunState.RUNNING, RunState.REGISTERED):
            raise ControlPlaneError(f"run {run_id} not pausable from {run.state}")
        cancelled = self._cancel_pending_tasks(run.workflow_id)
        self._transition(run, RunState.PAUSED, actor, ControlEventType.RUN_PAUSED,
                          {"cancelled_tasks": cancelled})
        return run

    def resume(self, run_id: str, *, actor: str = "system") -> WorkflowRun:
        run = self._require(run_id)
        if run.state != RunState.PAUSED:
            raise ControlPlaneError(f"run {run_id} not paused (state {run.state})")
        self._transition(run, RunState.RUNNING, actor, ControlEventType.RUN_RESUMED, {})
        return run

    def rollback(
        self, run_id: str, *, actor: str = "system", reason: str = ""
    ) -> ApprovalTicket:
        """Request a rollback. Returns an approval ticket — does NOT roll back yet.

        Compensating actions run only via `finalize_rollback` after a grant.
        """
        run = self._require(run_id)
        ticket = self._gate.submit(
            action_type="run_rollback",
            description=f"Rollback run {run_id}: {reason}".strip(),
            requested_by=actor,
            source_module=_MODULE,
            subject_type="workflow_run",
            subject_id=run_id,
            run_id=run_id,
        )
        run.state = RunState.ROLLING_BACK
        run.updated_at = datetime.now(UTC)
        return ticket

    def finalize_rollback(
        self, run_id: str, ticket_id: str, *, actor: str = "system"
    ) -> WorkflowRun:
        """Complete a rollback once its approval ticket is granted."""
        run = self._require(run_id)
        if not self._gate.is_granted(ticket_id):
            raise ApprovalGateError(
                f"rollback ticket {ticket_id} is not granted — cannot finalize"
            )
        self._transition(run, RunState.ROLLED_BACK, actor,
                          ControlEventType.RUN_ROLLED_BACK, {"ticket_id": ticket_id})
        return run

    def reroute(
        self, run_id: str, *, new_workflow_id: str, actor: str = "system"
    ) -> WorkflowRun:
        """Re-route a run onto a new workflow. Returns the new child run."""
        run = self._require(run_id)
        child = WorkflowRun(
            workflow_id=new_workflow_id,
            customer_id=run.customer_id,
            correlation_id=run.correlation_id,
            parent_run_id=run_id,
            state=RunState.RUNNING,
            attached_policy_ids=list(run.attached_policy_ids),
        )
        self._runs[child.run_id] = child
        run.state = RunState.REROUTED
        run.updated_at = datetime.now(UTC)
        emit(
            event_type=ControlEventType.RUN_REROUTED,
            source_module=_MODULE,
            actor=actor,
            subject_type="workflow_run",
            subject_id=run_id,
            run_id=run_id,
            payload={"new_run_id": child.run_id, "new_workflow_id": new_workflow_id},
        )
        self._emit(ControlEventType.RUN_REGISTERED, child, actor)
        return child

    def edit_policy(
        self, edit: PolicyEdit, *, actor: str = "system"
    ) -> ApprovalTicket:
        """Request a live policy edit. Returns an approval ticket.

        The policy is never mutated here — applied only via `finalize_policy_edit`
        after a grant, which keeps `no_unaudited_changes` intact.
        """
        run = self._require(edit.run_id)
        emit(
            event_type=ControlEventType.POLICY_EDIT_REQUESTED,
            source_module=_MODULE,
            actor=actor,
            subject_type="policy",
            subject_id=edit.policy_id,
            run_id=run.run_id,
            decision="escalate",
            payload={"before": list(run.attached_policy_ids), "change": edit.change},
        )
        return self._gate.submit(
            action_type="policy_edit",
            description=f"Edit policy {edit.policy_id} on run {edit.run_id}",
            requested_by=actor,
            source_module=_MODULE,
            subject_type="policy",
            subject_id=edit.policy_id,
            run_id=edit.run_id,
            metadata={"change": edit.change},
        )

    def finalize_policy_edit(
        self, edit: PolicyEdit, ticket_id: str, *, actor: str = "system"
    ) -> WorkflowRun:
        """Apply a policy edit once its approval ticket is granted."""
        run = self._require(edit.run_id)
        if not self._gate.is_granted(ticket_id):
            raise ApprovalGateError(
                f"policy-edit ticket {ticket_id} is not granted — cannot apply"
            )
        before = list(run.attached_policy_ids)
        if edit.policy_id not in run.attached_policy_ids:
            run.attached_policy_ids.append(edit.policy_id)
        run.updated_at = datetime.now(UTC)
        emit(
            event_type=ControlEventType.POLICY_EDITED,
            source_module=_MODULE,
            actor=actor,
            subject_type="policy",
            subject_id=edit.policy_id,
            run_id=run.run_id,
            decision="allow",
            payload={"before": before, "after": list(run.attached_policy_ids),
                     "change": edit.change, "ticket_id": ticket_id},
        )
        return run

    def get_run(self, run_id: str) -> WorkflowRun | None:
        return self._runs.get(run_id)

    # ── internals ────────────────────────────────────────────────
    def _require(self, run_id: str) -> WorkflowRun:
        run = self._runs.get(run_id)
        if run is None:
            raise ControlPlaneError(f"workflow run not found: {run_id}")
        return run

    def _transition(
        self,
        run: WorkflowRun,
        new_state: RunState,
        actor: str,
        event_type: ControlEventType,
        payload: dict[str, Any],
    ) -> None:
        run.state = new_state
        run.updated_at = datetime.now(UTC)
        emit(
            event_type=event_type,
            source_module=_MODULE,
            actor=actor,
            subject_type="workflow_run",
            subject_id=run.run_id,
            run_id=run.run_id,
            payload={**payload, "state": str(new_state)},
        )

    def _emit(self, event_type: ControlEventType, run: WorkflowRun, actor: str) -> None:
        emit(
            event_type=event_type,
            source_module=_MODULE,
            actor=actor,
            subject_type="workflow_run",
            subject_id=run.run_id,
            run_id=run.run_id,
            correlation_id=run.correlation_id,
            payload={"workflow_id": run.workflow_id, "state": str(run.state)},
        )

    def _task_summary(self, workflow_id: str) -> dict[str, int]:
        if self._task_queue is None:
            return {}
        try:
            tasks = self._task_queue.for_workflow(workflow_id)
        except Exception:  # noqa: BLE001 — queue is best-effort for monitoring
            return {}
        summary: dict[str, int] = {}
        for task in tasks:
            summary[task.status] = summary.get(task.status, 0) + 1
        return summary

    def _cancel_pending_tasks(self, workflow_id: str) -> int:
        if self._task_queue is None:
            return 0
        cancelled = 0
        try:
            tasks = self._task_queue.for_workflow(workflow_id)
        except Exception:  # noqa: BLE001
            return 0
        for task in tasks:
            if task.status in ("pending", "awaiting_approval", "approved"):
                try:
                    self._task_queue.cancel(task.task_id)
                    cancelled += 1
                except Exception:  # noqa: BLE001
                    continue
        return cancelled


_CONTROL_PLANE: ControlPlane | None = None


def get_control_plane() -> ControlPlane:
    """Return the process-scoped control plane singleton."""
    global _CONTROL_PLANE
    if _CONTROL_PLANE is None:
        _CONTROL_PLANE = ControlPlane()
    return _CONTROL_PLANE


def reset_control_plane() -> None:
    """Test helper: drop the cached control plane."""
    global _CONTROL_PLANE
    _CONTROL_PLANE = None


__all__ = [
    "ControlPlane",
    "ControlPlaneError",
    "get_control_plane",
    "reset_control_plane",
]
