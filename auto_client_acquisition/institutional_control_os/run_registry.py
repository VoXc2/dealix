"""Control-plane workflow-run registry.

The Institutional Control OS reasons about control *metrics*; this
module gives it the missing control *state*: a tenant-scoped registry
of workflow runs that the control plane can register, pause, resume,
and roll back.

Rollback is approval-gated by construction: ``request_rollback`` does
not roll anything back — it parks the run in ``rollback_pending`` and
files an approval ticket. ``finalize_rollback`` only succeeds once that
ticket has been granted by a human. Autonomy is bounded.

In-memory / process-scoped — the dev stopgap pattern used across the
control plane. Every run carries a ``tenant_id``.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from auto_client_acquisition.approval_center.approval_store import (
    ApprovalStore,
    get_default_approval_store,
)
from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus,
)

# Run states.
RUN_REGISTERED = "registered"
RUN_RUNNING = "running"
RUN_PAUSED = "paused"
RUN_ROLLBACK_PENDING = "rollback_pending"
RUN_ROLLED_BACK = "rolled_back"
RUN_COMPLETED = "completed"
RUN_FAILED = "failed"


class RunRegistryError(ValueError):
    """Raised on an illegal run-state transition."""


@dataclass
class WorkflowRun:
    """One governed workflow run tracked by the control plane."""

    run_id: str
    tenant_id: str
    workflow_id: str
    state: str = RUN_REGISTERED
    customer_id: str = ""
    correlation_id: str = ""
    parent_run_id: str = ""
    current_step: str = ""
    rollback_ticket_id: str = ""
    attached_policy_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    registered_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "tenant_id": self.tenant_id,
            "workflow_id": self.workflow_id,
            "state": self.state,
            "customer_id": self.customer_id,
            "correlation_id": self.correlation_id,
            "parent_run_id": self.parent_run_id,
            "current_step": self.current_step,
            "rollback_ticket_id": self.rollback_ticket_id,
            "attached_policy_ids": list(self.attached_policy_ids),
            "metadata": dict(self.metadata),
            "registered_at": self.registered_at,
            "updated_at": self.updated_at,
        }


# Reentrant — internal helpers (``_require`` → ``get_run``) re-acquire it.
_LOCK = threading.RLock()
_RUNS: dict[str, WorkflowRun] = {}


def _touch(run: WorkflowRun) -> None:
    run.updated_at = datetime.now(UTC).isoformat()


def register_run(
    *,
    tenant_id: str,
    workflow_id: str,
    customer_id: str = "",
    correlation_id: str = "",
    parent_run_id: str = "",
    metadata: dict[str, Any] | None = None,
) -> WorkflowRun:
    """Register a new workflow run in the control plane."""
    if not tenant_id.strip():
        raise RunRegistryError("tenant_id_required")
    if not workflow_id.strip():
        raise RunRegistryError("workflow_id_required")
    run = WorkflowRun(
        run_id=f"run_{uuid4().hex[:12]}",
        tenant_id=tenant_id,
        workflow_id=workflow_id,
        state=RUN_RUNNING,
        customer_id=customer_id,
        correlation_id=correlation_id or f"corr_{uuid4().hex[:8]}",
        parent_run_id=parent_run_id,
        metadata=dict(metadata or {}),
    )
    with _LOCK:
        _RUNS[run.run_id] = run
    return run


def get_run(run_id: str, *, tenant_id: str | None = None) -> WorkflowRun | None:
    """Fetch a run. With ``tenant_id``, a run from another tenant is
    treated as not found (tenant isolation)."""
    with _LOCK:
        run = _RUNS.get(run_id)
    if run is None:
        return None
    if tenant_id is not None and run.tenant_id != tenant_id:
        return None
    return run


def list_runs(*, tenant_id: str | None = None) -> list[WorkflowRun]:
    """All runs, optionally scoped to a single tenant."""
    with _LOCK:
        rows = list(_RUNS.values())
    if tenant_id is not None:
        rows = [r for r in rows if r.tenant_id == tenant_id]
    rows.sort(key=lambda r: r.registered_at)
    return rows


def _require(run_id: str, *, tenant_id: str | None = None) -> WorkflowRun:
    run = get_run(run_id, tenant_id=tenant_id)
    if run is None:
        raise RunRegistryError(f"run_not_found:{run_id}")
    return run


def pause_run(
    run_id: str,
    *,
    tenant_id: str | None = None,
    reason: str = "",
) -> WorkflowRun:
    """Pause a running run (e.g. on a kill switch / safety event)."""
    with _LOCK:
        run = _require(run_id, tenant_id=tenant_id)
        if run.state in (RUN_ROLLED_BACK, RUN_COMPLETED, RUN_FAILED):
            raise RunRegistryError(f"cannot_pause_terminal_run:{run.state}")
        if run.state != RUN_ROLLBACK_PENDING:
            run.state = RUN_PAUSED
        if reason:
            run.metadata["pause_reason"] = reason
        _touch(run)
    return run


def resume_run(run_id: str, *, tenant_id: str | None = None) -> WorkflowRun:
    """Resume a paused run."""
    with _LOCK:
        run = _require(run_id, tenant_id=tenant_id)
        if run.state != RUN_PAUSED:
            raise RunRegistryError(f"cannot_resume_run_in_state:{run.state}")
        run.state = RUN_RUNNING
        run.metadata.pop("pause_reason", None)
        _touch(run)
    return run


def request_rollback(
    run_id: str,
    *,
    requested_by: str,
    reason: str,
    tenant_id: str | None = None,
    approval_store: ApprovalStore | None = None,
) -> ApprovalRequest:
    """Request a rollback. Files an approval ticket and parks the run in
    ``rollback_pending`` — nothing is rolled back without human approval."""
    store = approval_store or get_default_approval_store()
    with _LOCK:
        run = _require(run_id, tenant_id=tenant_id)
        if run.state == RUN_ROLLED_BACK:
            raise RunRegistryError("run_already_rolled_back")
        ticket = ApprovalRequest(
            tenant_id=run.tenant_id,
            object_type="workflow_run",
            object_id=run.run_id,
            action_type="rollback",
            action_mode="approval_required",
            risk_level="high",
            summary_en=f"Rollback requested by {requested_by}: {reason}",
            summary_ar="طلب تراجع يحتاج موافقة بشرية",
            run_id=run.run_id,
        )
    store.create(ticket)
    with _LOCK:
        run.state = RUN_ROLLBACK_PENDING
        run.rollback_ticket_id = ticket.approval_id
        run.metadata["rollback_reason"] = reason
        _touch(run)
    return ticket


def finalize_rollback(
    run_id: str,
    *,
    tenant_id: str | None = None,
    approval_store: ApprovalStore | None = None,
) -> WorkflowRun:
    """Finalize a rollback — only succeeds once the approval ticket is
    granted. Raises ``RunRegistryError`` otherwise."""
    store = approval_store or get_default_approval_store()
    with _LOCK:
        run = _require(run_id, tenant_id=tenant_id)
        if run.state != RUN_ROLLBACK_PENDING:
            raise RunRegistryError(f"no_rollback_pending:{run.state}")
        ticket_id = run.rollback_ticket_id
    if not ticket_id:
        raise RunRegistryError("rollback_ticket_missing")
    ticket = store.get(ticket_id)
    if ticket is None:
        raise RunRegistryError("rollback_ticket_not_found")
    if ApprovalStatus(ticket.status) != ApprovalStatus.APPROVED:
        raise RunRegistryError(
            f"rollback_not_approved:ticket_is_{ticket.status}",
        )
    with _LOCK:
        run.state = RUN_ROLLED_BACK
        _touch(run)
    return run


def clear_run_registry_for_tests() -> None:
    with _LOCK:
        _RUNS.clear()


__all__ = [
    "RUN_COMPLETED",
    "RUN_FAILED",
    "RUN_PAUSED",
    "RUN_REGISTERED",
    "RUN_ROLLBACK_PENDING",
    "RUN_ROLLED_BACK",
    "RUN_RUNNING",
    "RunRegistryError",
    "WorkflowRun",
    "clear_run_registry_for_tests",
    "finalize_rollback",
    "get_run",
    "list_runs",
    "pause_run",
    "register_run",
    "request_rollback",
    "resume_run",
]
