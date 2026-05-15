"""Tenant-aware control-plane repository with approval-gated transitions."""

from __future__ import annotations

from datetime import UTC, datetime

from auto_client_acquisition.control_plane_os.approval_gate import (
    ApprovalGateError,
    ApprovalTicket,
    InMemoryApprovalGate,
)
from auto_client_acquisition.control_plane_os.ledger import ControlEventLedger
from auto_client_acquisition.control_plane_os.schemas import (
    ControlEvent,
    PolicyEditRequest,
    RollbackRequest,
    WorkflowRun,
)
from auto_client_acquisition.control_plane_os.tenant_context import ensure_tenant_id


class ControlPlaneRepository:
    """MVP control-plane core with auditable state transitions."""

    def __init__(
        self,
        *,
        ledger: ControlEventLedger | None = None,
        approvals: InMemoryApprovalGate | None = None,
    ) -> None:
        self._ledger = ledger or ControlEventLedger()
        self._approvals = approvals or InMemoryApprovalGate()
        self._runs: dict[str, WorkflowRun] = {}

    def register_run(
        self,
        *,
        tenant_id: str,
        workflow_id: str,
        customer_id: str = "",
        actor: str = "system",
    ) -> WorkflowRun:
        tenant = ensure_tenant_id(tenant_id)
        run = WorkflowRun(
            tenant_id=tenant,
            workflow_id=workflow_id,
            customer_id=customer_id,
            state="running",
        )
        self._runs[run.run_id] = run
        self._emit_event(
            tenant_id=tenant,
            run_id=run.run_id,
            actor=actor,
            event_type="run_registered",
            decision="allow",
            payload={"workflow_id": workflow_id, "customer_id": customer_id},
        )
        return run

    def get_run(self, *, tenant_id: str, run_id: str) -> WorkflowRun:
        tenant = ensure_tenant_id(tenant_id)
        run = self._runs.get(run_id)
        if run is None or run.tenant_id != tenant:
            raise ValueError("run not found")
        return run

    def pause_run(self, *, tenant_id: str, run_id: str, actor: str = "system") -> WorkflowRun:
        run = self.get_run(tenant_id=tenant_id, run_id=run_id)
        updated = run.model_copy(
            update={"state": "paused", "updated_at": datetime.now(UTC)},
        )
        self._runs[run_id] = updated
        self._emit_event(
            tenant_id=run.tenant_id,
            run_id=run_id,
            actor=actor,
            event_type="run_paused",
            decision="allow_with_review",
        )
        return updated

    def resume_run(self, *, tenant_id: str, run_id: str, actor: str = "system") -> WorkflowRun:
        run = self.get_run(tenant_id=tenant_id, run_id=run_id)
        updated = run.model_copy(
            update={"state": "running", "updated_at": datetime.now(UTC)},
        )
        self._runs[run_id] = updated
        self._emit_event(
            tenant_id=run.tenant_id,
            run_id=run_id,
            actor=actor,
            event_type="run_resumed",
            decision="allow",
        )
        return updated

    def request_rollback(self, req: RollbackRequest) -> ApprovalTicket:
        run = self.get_run(tenant_id=req.tenant_id, run_id=req.run_id)
        ticket = self._approvals.request(
            tenant_id=run.tenant_id,
            action_type="rollback",
            run_id=run.run_id,
            requested_by=req.actor,
            reason=req.reason,
        )
        updated = run.model_copy(
            update={"state": "awaiting_approval", "updated_at": datetime.now(UTC)},
        )
        self._runs[run.run_id] = updated
        self._emit_event(
            tenant_id=run.tenant_id,
            run_id=run.run_id,
            actor=req.actor,
            event_type="rollback_requested",
            decision="escalate",
            payload={"ticket_id": ticket.ticket_id, "reason": req.reason},
        )
        return ticket

    def finalize_rollback(
        self,
        *,
        tenant_id: str,
        run_id: str,
        ticket_id: str,
        actor: str = "system",
    ) -> WorkflowRun:
        run = self.get_run(tenant_id=tenant_id, run_id=run_id)
        self._approvals.require_granted(tenant_id=run.tenant_id, ticket_id=ticket_id)
        updated = run.model_copy(
            update={"state": "rolled_back", "updated_at": datetime.now(UTC)},
        )
        self._runs[run_id] = updated
        self._emit_event(
            tenant_id=run.tenant_id,
            run_id=run_id,
            actor=actor,
            event_type="rollback_finalized",
            decision="approved_execute",
            payload={"ticket_id": ticket_id},
        )
        return updated

    def request_policy_edit(self, req: PolicyEditRequest) -> ApprovalTicket:
        run = self.get_run(tenant_id=req.tenant_id, run_id=req.run_id)
        ticket = self._approvals.request(
            tenant_id=run.tenant_id,
            action_type="policy_edit",
            run_id=run.run_id,
            requested_by=req.actor,
            reason=f"policy_id={req.policy_id}",
        )
        updated = run.model_copy(
            update={"state": "awaiting_approval", "updated_at": datetime.now(UTC)},
        )
        self._runs[run.run_id] = updated
        self._emit_event(
            tenant_id=run.tenant_id,
            run_id=run.run_id,
            actor=req.actor,
            event_type="policy_edit_requested",
            decision="escalate",
            payload={"ticket_id": ticket.ticket_id, "policy_id": req.policy_id, "change": req.change},
        )
        return ticket

    def finalize_policy_edit(
        self,
        *,
        tenant_id: str,
        run_id: str,
        ticket_id: str,
        actor: str = "system",
    ) -> WorkflowRun:
        run = self.get_run(tenant_id=tenant_id, run_id=run_id)
        self._approvals.require_granted(tenant_id=run.tenant_id, ticket_id=ticket_id)
        updated = run.model_copy(
            update={"state": "running", "updated_at": datetime.now(UTC)},
        )
        self._runs[run_id] = updated
        self._emit_event(
            tenant_id=run.tenant_id,
            run_id=run_id,
            actor=actor,
            event_type="policy_edit_finalized",
            decision="approved_execute",
            payload={"ticket_id": ticket_id},
        )
        return updated

    def grant_approval(self, *, tenant_id: str, ticket_id: str, actor: str) -> ApprovalTicket:
        ticket = self._approvals.grant(tenant_id=tenant_id, ticket_id=ticket_id, granted_by=actor)
        self._emit_event(
            tenant_id=ticket.tenant_id,
            run_id=ticket.run_id,
            actor=actor,
            event_type="approval_granted",
            decision="approved_execute",
            payload={"ticket_id": ticket.ticket_id, "action_type": ticket.action_type},
        )
        return ticket

    def pending_approvals(self, *, tenant_id: str) -> list[ApprovalTicket]:
        return self._approvals.list_pending(tenant_id=tenant_id)

    def trace_run(self, *, tenant_id: str, run_id: str) -> list[ControlEvent]:
        self.get_run(tenant_id=tenant_id, run_id=run_id)
        return self._ledger.list_by_run(tenant_id=tenant_id, run_id=run_id)

    def clear_for_test(self) -> None:
        self._runs.clear()
        self._ledger.clear_for_test()
        self._approvals.clear_for_test()

    def _emit_event(
        self,
        *,
        tenant_id: str,
        run_id: str,
        actor: str,
        event_type: str,
        decision: str = "",
        payload: dict[str, object] | None = None,
    ) -> ControlEvent:
        event = ControlEvent(
            tenant_id=tenant_id,
            event_type=event_type,
            source_module="control_plane_os",
            actor=actor,
            run_id=run_id,
            subject_type="workflow_run",
            subject_id=run_id,
            decision=decision,
            payload=payload or {},
        )
        return self._ledger.append(event)


__all__ = ["ApprovalGateError", "ControlPlaneRepository"]
