"""In-memory repositories for enterprise control-plane orchestration."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from uuid import uuid4

from auto_client_acquisition.control_plane_os.ledger import JsonlControlLedger
from auto_client_acquisition.control_plane_os.schemas import ApprovalTicket, ControlEvent, WorkflowRun


class InMemoryControlPlaneRepository:
    def __init__(self, *, ledger: JsonlControlLedger | None = None) -> None:
        self._ledger = ledger or JsonlControlLedger()
        self._runs: dict[tuple[str, str], WorkflowRun] = {}
        self._tickets: dict[tuple[str, str], ApprovalTicket] = {}

    def register_run(
        self,
        *,
        tenant_id: str,
        workflow_id: str,
        actor: str,
        customer_id: str = "",
        run_id: str | None = None,
    ) -> WorkflowRun:
        rid = run_id or f"run_{uuid4().hex[:10]}"
        run = WorkflowRun(
            run_id=rid,
            tenant_id=tenant_id,
            workflow_id=workflow_id,
            customer_id=customer_id,
            state="running",
            actor=actor,
        )
        self._runs[(tenant_id, rid)] = run
        self._emit(
            tenant_id=tenant_id,
            event_type="workflow.registered",
            actor=actor,
            run_id=rid,
            subject_type="workflow_run",
            subject_id=rid,
            payload={"workflow_id": workflow_id, "customer_id": customer_id},
        )
        return run

    def get_run(self, *, tenant_id: str, run_id: str) -> WorkflowRun:
        try:
            return self._runs[(tenant_id, run_id)]
        except KeyError as exc:
            raise ValueError("run_not_found") from exc

    def pause_run(self, *, tenant_id: str, run_id: str, actor: str, reason: str = "") -> WorkflowRun:
        run = self.get_run(tenant_id=tenant_id, run_id=run_id)
        updated = replace(run, state="paused", updated_at=datetime.now(UTC).isoformat())
        self._runs[(tenant_id, run_id)] = updated
        self._emit(
            tenant_id=tenant_id,
            event_type="workflow.paused",
            actor=actor,
            run_id=run_id,
            subject_type="workflow_run",
            subject_id=run_id,
            payload={"reason": reason},
        )
        return updated

    def resume_run(self, *, tenant_id: str, run_id: str, actor: str) -> WorkflowRun:
        run = self.get_run(tenant_id=tenant_id, run_id=run_id)
        updated = replace(run, state="running", updated_at=datetime.now(UTC).isoformat())
        self._runs[(tenant_id, run_id)] = updated
        self._emit(
            tenant_id=tenant_id,
            event_type="workflow.resumed",
            actor=actor,
            run_id=run_id,
            subject_type="workflow_run",
            subject_id=run_id,
        )
        return updated

    def request_rollback(self, *, tenant_id: str, run_id: str, actor: str, reason: str) -> ApprovalTicket:
        self.get_run(tenant_id=tenant_id, run_id=run_id)
        ticket = self._new_ticket(
            tenant_id=tenant_id,
            action_type="rollback",
            requested_by=actor,
            run_id=run_id,
            description=reason,
            source_module="control_plane_os.rollback",
        )
        self._emit(
            tenant_id=tenant_id,
            event_type="rollback.requested",
            actor=actor,
            run_id=run_id,
            subject_type="approval_ticket",
            subject_id=ticket.ticket_id,
            decision="approval_required",
            payload={"reason": reason},
        )
        return ticket

    def finalize_rollback(self, *, tenant_id: str, run_id: str, actor: str, ticket_id: str) -> WorkflowRun:
        ticket = self._require_ticket_state(tenant_id=tenant_id, ticket_id=ticket_id, state="granted")
        if ticket.action_type != "rollback" or ticket.run_id != run_id:
            raise ValueError("ticket_not_for_run_rollback")
        run = self.pause_run(tenant_id=tenant_id, run_id=run_id, actor=actor, reason="rollback_finalized")
        rolled_back = replace(run, state="rolled_back", updated_at=datetime.now(UTC).isoformat())
        self._runs[(tenant_id, run_id)] = rolled_back
        self._emit(
            tenant_id=tenant_id,
            event_type="rollback.finalized",
            actor=actor,
            run_id=run_id,
            subject_type="workflow_run",
            subject_id=run_id,
            decision="approved_execute",
            payload={"ticket_id": ticket_id},
        )
        return rolled_back

    def request_policy_edit(
        self,
        *,
        tenant_id: str,
        actor: str,
        policy_id: str,
        patch: dict[str, str],
    ) -> ApprovalTicket:
        ticket = self._new_ticket(
            tenant_id=tenant_id,
            action_type="policy_edit",
            requested_by=actor,
            description=f"edit policy {policy_id}",
            source_module="control_plane_os.policy",
            subject_type="policy",
            subject_id=policy_id,
            metadata={"patch": patch},
        )
        self._emit(
            tenant_id=tenant_id,
            event_type="policy.edit_requested",
            actor=actor,
            subject_type="approval_ticket",
            subject_id=ticket.ticket_id,
            decision="approval_required",
            payload={"policy_id": policy_id, "patch": patch},
        )
        return ticket

    def finalize_policy_edit(self, *, tenant_id: str, actor: str, ticket_id: str) -> dict[str, str]:
        ticket = self._require_ticket_state(tenant_id=tenant_id, ticket_id=ticket_id, state="granted")
        if ticket.action_type != "policy_edit":
            raise ValueError("ticket_not_policy_edit")
        patch = dict(ticket.metadata.get("patch") or {})
        self._emit(
            tenant_id=tenant_id,
            event_type="policy.edit_finalized",
            actor=actor,
            subject_type="policy",
            subject_id=ticket.subject_id,
            decision="approved_execute",
            payload={"ticket_id": ticket.ticket_id, "patch": patch},
        )
        return patch

    def grant_approval(self, *, tenant_id: str, ticket_id: str, actor: str) -> ApprovalTicket:
        ticket = self._require_ticket_state(tenant_id=tenant_id, ticket_id=ticket_id, state="pending")
        updated = replace(
            ticket,
            state="granted",
            granted_by=actor,
            resolved_at=datetime.now(UTC).isoformat(),
        )
        self._tickets[(tenant_id, ticket_id)] = updated
        self._emit(
            tenant_id=tenant_id,
            event_type="approval.granted",
            actor=actor,
            run_id=ticket.run_id,
            subject_type="approval_ticket",
            subject_id=ticket.ticket_id,
        )
        return updated

    def reject_approval(self, *, tenant_id: str, ticket_id: str, actor: str, reason: str) -> ApprovalTicket:
        ticket = self._require_ticket_state(tenant_id=tenant_id, ticket_id=ticket_id, state="pending")
        updated = replace(
            ticket,
            state="rejected",
            rejected_by=actor,
            reason=reason,
            resolved_at=datetime.now(UTC).isoformat(),
        )
        self._tickets[(tenant_id, ticket_id)] = updated
        self._emit(
            tenant_id=tenant_id,
            event_type="approval.rejected",
            actor=actor,
            run_id=ticket.run_id,
            subject_type="approval_ticket",
            subject_id=ticket.ticket_id,
            payload={"reason": reason},
        )
        return updated

    def list_approval_queue(self, *, tenant_id: str, state: str = "pending") -> list[ApprovalTicket]:
        rows = [t for (tid, _), t in self._tickets.items() if tid == tenant_id]
        if state:
            rows = [t for t in rows if t.state == state]
        rows.sort(key=lambda t: t.created_at)
        return rows

    def trace_run(self, *, tenant_id: str, run_id: str) -> list[ControlEvent]:
        return self._ledger.list_events(tenant_id=tenant_id, run_id=run_id, limit=5000)

    def _new_ticket(
        self,
        *,
        tenant_id: str,
        action_type: str,
        requested_by: str,
        description: str,
        source_module: str,
        run_id: str = "",
        subject_type: str = "",
        subject_id: str = "",
        metadata: dict[str, str] | None = None,
    ) -> ApprovalTicket:
        ticket = ApprovalTicket(
            ticket_id=f"tkt_{uuid4().hex[:10]}",
            tenant_id=tenant_id,
            action_type=action_type,
            description=description,
            requested_by=requested_by,
            source_module=source_module,
            run_id=run_id,
            subject_type=subject_type,
            subject_id=subject_id,
            metadata=dict(metadata or {}),
        )
        self._tickets[(tenant_id, ticket.ticket_id)] = ticket
        return ticket

    def _require_ticket_state(self, *, tenant_id: str, ticket_id: str, state: str) -> ApprovalTicket:
        try:
            ticket = self._tickets[(tenant_id, ticket_id)]
        except KeyError as exc:
            raise ValueError("ticket_not_found") from exc
        if ticket.state != state:
            raise ValueError(f"ticket_state_must_be_{state}")
        return ticket

    def _emit(
        self,
        *,
        tenant_id: str,
        event_type: str,
        actor: str,
        source_module: str = "control_plane_os",
        subject_type: str = "",
        subject_id: str = "",
        run_id: str = "",
        correlation_id: str = "",
        decision: str = "",
        payload: dict[str, object] | None = None,
    ) -> ControlEvent:
        event = ControlEvent(
            id=f"evt_{uuid4().hex[:10]}",
            tenant_id=tenant_id,
            event_type=event_type,
            source_module=source_module,
            actor=actor,
            subject_type=subject_type,
            subject_id=subject_id,
            run_id=run_id,
            correlation_id=correlation_id,
            decision=decision,
            payload=dict(payload or {}),
        )
        self._ledger.append(event)
        return event
