"""Control-plane approval gate — the single approval surface for Systems 26-35.

A lightweight, ledger-backed gate that mirrors the Trust Plane
``ApprovalCenter`` semantics (submit / grant / reject / list_pending) without
forcing every module to construct heavyweight ``DecisionOutput`` contracts.

Every state-changing or external action in the control plane that needs human
sign-off goes through here. Each transition is written to the control-event
ledger, which is what makes ``no_unaudited_changes`` hold. Bridging this gate
to the canonical Trust Plane ``ApprovalCenter`` is a documented follow-up.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.control_plane_os.ledger import ControlEventType, emit


class ApprovalState(StrEnum):
    PENDING = "pending"
    GRANTED = "granted"
    REJECTED = "rejected"


class ApprovalTicket(BaseModel):
    """One approval request tracked by the gate."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    ticket_id: str = Field(default_factory=lambda: f"apr_{uuid4().hex[:12]}")
    action_type: str
    description: str
    requested_by: str
    source_module: str
    subject_type: str = ""
    subject_id: str = ""
    run_id: str | None = None
    state: ApprovalState = ApprovalState.PENDING
    granted_by: str | None = None
    rejected_by: str | None = None
    reason: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    resolved_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ApprovalGateError(RuntimeError):
    """Raised on an invalid approval-gate transition — never swallowed."""


class ControlApprovalGate:
    """In-memory approval queue. Every transition is recorded to the ledger."""

    def __init__(self) -> None:
        self._tickets: dict[str, ApprovalTicket] = {}

    def submit(
        self,
        *,
        action_type: str,
        description: str,
        requested_by: str,
        source_module: str,
        subject_type: str = "",
        subject_id: str = "",
        run_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ApprovalTicket:
        ticket = ApprovalTicket(
            action_type=action_type,
            description=description,
            requested_by=requested_by,
            source_module=source_module,
            subject_type=subject_type,
            subject_id=subject_id,
            run_id=run_id,
            metadata=metadata or {},
        )
        self._tickets[ticket.ticket_id] = ticket
        emit(
            event_type=ControlEventType.APPROVAL_REQUESTED,
            source_module=source_module,
            actor=requested_by,
            subject_type="approval_ticket",
            subject_id=ticket.ticket_id,
            run_id=run_id,
            decision="escalate",
            payload={"action_type": action_type, "description": description},
        )
        return ticket

    def grant(self, ticket_id: str, approver: str) -> ApprovalTicket:
        ticket = self._require(ticket_id)
        if ticket.state != ApprovalState.PENDING:
            raise ApprovalGateError(
                f"ticket {ticket_id} already resolved: {ticket.state}"
            )
        ticket.state = ApprovalState.GRANTED
        ticket.granted_by = approver
        ticket.resolved_at = datetime.now(UTC)
        emit(
            event_type=ControlEventType.APPROVAL_GRANTED,
            source_module=ticket.source_module,
            actor=approver,
            subject_type="approval_ticket",
            subject_id=ticket_id,
            run_id=ticket.run_id,
            decision="allow",
            payload={"action_type": ticket.action_type},
        )
        return ticket

    def reject(self, ticket_id: str, approver: str, reason: str = "") -> ApprovalTicket:
        ticket = self._require(ticket_id)
        if ticket.state != ApprovalState.PENDING:
            raise ApprovalGateError(
                f"ticket {ticket_id} already resolved: {ticket.state}"
            )
        ticket.state = ApprovalState.REJECTED
        ticket.rejected_by = approver
        ticket.reason = reason
        ticket.resolved_at = datetime.now(UTC)
        emit(
            event_type=ControlEventType.APPROVAL_REJECTED,
            source_module=ticket.source_module,
            actor=approver,
            subject_type="approval_ticket",
            subject_id=ticket_id,
            run_id=ticket.run_id,
            decision="deny",
            payload={"action_type": ticket.action_type, "reason": reason},
        )
        return ticket

    def get(self, ticket_id: str) -> ApprovalTicket | None:
        return self._tickets.get(ticket_id)

    def is_granted(self, ticket_id: str) -> bool:
        ticket = self._tickets.get(ticket_id)
        return ticket is not None and ticket.state == ApprovalState.GRANTED

    def list_pending(self, source_module: str | None = None) -> list[ApprovalTicket]:
        return [
            t
            for t in self._tickets.values()
            if t.state == ApprovalState.PENDING
            and (source_module is None or t.source_module == source_module)
        ]

    def _require(self, ticket_id: str) -> ApprovalTicket:
        ticket = self._tickets.get(ticket_id)
        if ticket is None:
            raise ApprovalGateError(f"approval ticket not found: {ticket_id}")
        return ticket


_GATE: ControlApprovalGate | None = None


def get_approval_gate() -> ControlApprovalGate:
    """Return the process-scoped approval gate singleton."""
    global _GATE
    if _GATE is None:
        _GATE = ControlApprovalGate()
    return _GATE


def reset_approval_gate() -> None:
    """Test helper: drop the cached gate."""
    global _GATE
    _GATE = None


__all__ = [
    "ApprovalGateError",
    "ApprovalState",
    "ApprovalTicket",
    "ControlApprovalGate",
    "get_approval_gate",
    "reset_approval_gate",
]
