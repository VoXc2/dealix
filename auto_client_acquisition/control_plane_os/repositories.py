"""In-memory control plane repository with approval-first enforcement."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from auto_client_acquisition.control_plane_os.tenant_context import resolve_tenant_id


def _now() -> datetime:
    return datetime.now(UTC)


def _event_id() -> str:
    return f"evt_{uuid4().hex[:20]}"


def _ticket_id() -> str:
    return f"apt_{uuid4().hex[:20]}"


def _run_id() -> str:
    return f"run_{uuid4().hex[:20]}"


@dataclass(slots=True)
class WorkflowRun:
    run_id: str
    tenant_id: str
    workflow_id: str
    customer_id: str | None = None
    state: str = "registered"
    correlation_id: str | None = None
    parent_run_id: str | None = None
    current_step: str | None = None
    attached_policy_ids: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    registered_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)


@dataclass(slots=True)
class ControlEvent:
    id: str
    tenant_id: str
    event_type: str
    source_module: str
    actor: str
    subject_type: str | None = None
    subject_id: str | None = None
    run_id: str | None = None
    correlation_id: str | None = None
    decision: str | None = None
    occurred_at: datetime = field(default_factory=_now)
    payload: dict[str, Any] = field(default_factory=dict)
    redacted: bool = True


@dataclass(slots=True)
class ApprovalTicket:
    ticket_id: str
    tenant_id: str
    action_type: str
    description: str
    requested_by: str
    source_module: str
    subject_type: str | None = None
    subject_id: str | None = None
    run_id: str | None = None
    state: str = "pending"
    granted_by: str | None = None
    rejected_by: str | None = None
    reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_now)
    resolved_at: datetime | None = None


class InMemoryControlPlaneRepository:
    """Tenant-scoped in-memory store used by tests/dev fallback."""

    def __init__(self) -> None:
        self._runs: dict[str, dict[str, WorkflowRun]] = {}
        self._events: dict[str, list[ControlEvent]] = {}
        self._tickets: dict[str, dict[str, ApprovalTicket]] = {}

    def register_workflow_run(
        self,
        *,
        tenant_id: str | None,
        workflow_id: str,
        customer_id: str | None = None,
        run_id: str | None = None,
        correlation_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> WorkflowRun:
        tid = resolve_tenant_id(tenant_id)
        run = WorkflowRun(
            run_id=run_id or _run_id(),
            tenant_id=tid,
            workflow_id=workflow_id,
            customer_id=customer_id,
            correlation_id=correlation_id,
            metadata=metadata or {},
        )
        self._runs.setdefault(tid, {})[run.run_id] = run
        self.append_event(
            tenant_id=tid,
            event_type="workflow.registered",
            source_module="control_plane",
            actor="system",
            run_id=run.run_id,
            subject_type="workflow_run",
            subject_id=run.run_id,
            decision="registered",
            payload={"workflow_id": workflow_id},
        )
        return run

    def get_run(self, *, tenant_id: str | None, run_id: str) -> WorkflowRun:
        tid = resolve_tenant_id(tenant_id)
        try:
            return self._runs[tid][run_id]
        except KeyError as exc:
            raise KeyError(f"run not found: tenant={tid} run_id={run_id}") from exc

    def append_event(
        self,
        *,
        tenant_id: str | None,
        event_type: str,
        source_module: str,
        actor: str,
        subject_type: str | None = None,
        subject_id: str | None = None,
        run_id: str | None = None,
        correlation_id: str | None = None,
        decision: str | None = None,
        payload: dict[str, Any] | None = None,
        redacted: bool = True,
    ) -> ControlEvent:
        tid = resolve_tenant_id(tenant_id)
        event = ControlEvent(
            id=_event_id(),
            tenant_id=tid,
            event_type=event_type,
            source_module=source_module,
            actor=actor,
            subject_type=subject_type,
            subject_id=subject_id,
            run_id=run_id,
            correlation_id=correlation_id,
            decision=decision,
            payload=payload or {},
            redacted=redacted,
        )
        self._events.setdefault(tid, []).append(event)
        return event

    def trace(self, *, tenant_id: str | None, run_id: str) -> tuple[ControlEvent, ...]:
        tid = resolve_tenant_id(tenant_id)
        events = [ev for ev in self._events.get(tid, []) if ev.run_id == run_id]
        return tuple(sorted(events, key=lambda ev: ev.occurred_at))

    def request_approval(
        self,
        *,
        tenant_id: str | None,
        action_type: str,
        description: str,
        requested_by: str,
        source_module: str,
        subject_type: str | None = None,
        subject_id: str | None = None,
        run_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ApprovalTicket:
        tid = resolve_tenant_id(tenant_id)
        ticket = ApprovalTicket(
            ticket_id=_ticket_id(),
            tenant_id=tid,
            action_type=action_type,
            description=description,
            requested_by=requested_by,
            source_module=source_module,
            subject_type=subject_type,
            subject_id=subject_id,
            run_id=run_id,
            metadata=metadata or {},
        )
        self._tickets.setdefault(tid, {})[ticket.ticket_id] = ticket
        self.append_event(
            tenant_id=tid,
            event_type="approval.submitted",
            source_module=source_module,
            actor=requested_by,
            subject_type="approval_ticket",
            subject_id=ticket.ticket_id,
            run_id=run_id,
            decision="pending",
            payload={"action_type": action_type, "description": description},
        )
        return ticket

    def get_ticket(self, *, tenant_id: str | None, ticket_id: str) -> ApprovalTicket:
        tid = resolve_tenant_id(tenant_id)
        try:
            return self._tickets[tid][ticket_id]
        except KeyError as exc:
            raise KeyError(f"ticket not found: tenant={tid} ticket_id={ticket_id}") from exc

    def list_oversight_queue(self, *, tenant_id: str | None) -> tuple[ApprovalTicket, ...]:
        tid = resolve_tenant_id(tenant_id)
        pending = [ticket for ticket in self._tickets.get(tid, {}).values() if ticket.state == "pending"]
        return tuple(sorted(pending, key=lambda ticket: ticket.created_at))

    def grant_approval(
        self,
        *,
        tenant_id: str | None,
        ticket_id: str,
        granted_by: str,
        reason: str | None = None,
    ) -> ApprovalTicket:
        tid = resolve_tenant_id(tenant_id)
        ticket = self.get_ticket(tenant_id=tid, ticket_id=ticket_id)
        updated = replace(
            ticket,
            state="granted",
            granted_by=granted_by,
            reason=reason,
            resolved_at=_now(),
        )
        self._tickets[tid][ticket_id] = updated
        self.append_event(
            tenant_id=tid,
            event_type="approval.granted",
            source_module="approval_center",
            actor=granted_by,
            subject_type="approval_ticket",
            subject_id=ticket_id,
            run_id=ticket.run_id,
            decision="granted",
            payload={"reason": reason or ""},
        )
        return updated

    def reject_approval(
        self,
        *,
        tenant_id: str | None,
        ticket_id: str,
        rejected_by: str,
        reason: str,
    ) -> ApprovalTicket:
        tid = resolve_tenant_id(tenant_id)
        ticket = self.get_ticket(tenant_id=tid, ticket_id=ticket_id)
        updated = replace(
            ticket,
            state="rejected",
            rejected_by=rejected_by,
            reason=reason,
            resolved_at=_now(),
        )
        self._tickets[tid][ticket_id] = updated
        self.append_event(
            tenant_id=tid,
            event_type="approval.rejected",
            source_module="approval_center",
            actor=rejected_by,
            subject_type="approval_ticket",
            subject_id=ticket_id,
            run_id=ticket.run_id,
            decision="rejected",
            payload={"reason": reason},
        )
        return updated

    def pause_run(self, *, tenant_id: str | None, run_id: str, actor: str, reason: str) -> WorkflowRun:
        tid = resolve_tenant_id(tenant_id)
        run = self.get_run(tenant_id=tid, run_id=run_id)
        updated = replace(run, state="paused", updated_at=_now())
        self._runs[tid][run_id] = updated
        self.append_event(
            tenant_id=tid,
            event_type="workflow.paused",
            source_module="control_plane",
            actor=actor,
            run_id=run_id,
            subject_type="workflow_run",
            subject_id=run_id,
            decision="paused",
            payload={"reason": reason},
        )
        return updated

    def request_rollback(
        self,
        *,
        tenant_id: str | None,
        run_id: str,
        requested_by: str,
        reason: str,
    ) -> ApprovalTicket:
        return self.request_approval(
            tenant_id=tenant_id,
            action_type="control_plane.rollback",
            description=f"Rollback requested for run {run_id}",
            requested_by=requested_by,
            source_module="control_plane",
            run_id=run_id,
            subject_type="workflow_run",
            subject_id=run_id,
            metadata={"reason": reason},
        )

    def finalize_rollback(
        self,
        *,
        tenant_id: str | None,
        run_id: str,
        ticket_id: str,
        actor: str,
    ) -> WorkflowRun:
        tid = resolve_tenant_id(tenant_id)
        ticket = self.get_ticket(tenant_id=tid, ticket_id=ticket_id)
        if ticket.state != "granted":
            raise PermissionError("rollback requires granted approval ticket")
        if ticket.run_id != run_id:
            raise ValueError("approval ticket does not target this run")
        run = self.get_run(tenant_id=tid, run_id=run_id)
        updated = replace(run, state="rolled_back", updated_at=_now())
        self._runs[tid][run_id] = updated
        self.append_event(
            tenant_id=tid,
            event_type="workflow.rollback.finalized",
            source_module="control_plane",
            actor=actor,
            run_id=run_id,
            subject_type="workflow_run",
            subject_id=run_id,
            decision="rolled_back",
            payload={"approval_ticket_id": ticket_id},
        )
        return updated

    def request_policy_edit(
        self,
        *,
        tenant_id: str | None,
        policy_id: str,
        patch: dict[str, Any],
        requested_by: str,
    ) -> ApprovalTicket:
        return self.request_approval(
            tenant_id=tenant_id,
            action_type="control_plane.policy_edit",
            description=f"Policy edit requested for {policy_id}",
            requested_by=requested_by,
            source_module="control_plane",
            subject_type="policy",
            subject_id=policy_id,
            metadata={"patch": patch},
        )

    def finalize_policy_edit(
        self,
        *,
        tenant_id: str | None,
        ticket_id: str,
        actor: str,
    ) -> dict[str, Any]:
        ticket = self.get_ticket(tenant_id=tenant_id, ticket_id=ticket_id)
        if ticket.state != "granted":
            raise PermissionError("policy edit requires granted approval ticket")
        applied = {
            "policy_id": ticket.subject_id,
            "patch": ticket.metadata.get("patch", {}),
            "applied_by": actor,
            "ticket_id": ticket.ticket_id,
        }
        self.append_event(
            tenant_id=ticket.tenant_id,
            event_type="policy.edit.finalized",
            source_module="control_plane",
            actor=actor,
            subject_type="policy",
            subject_id=ticket.subject_id,
            decision="applied",
            payload=applied,
        )
        return applied


__all__ = [
    "ApprovalTicket",
    "ControlEvent",
    "InMemoryControlPlaneRepository",
    "WorkflowRun",
]
