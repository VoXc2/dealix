"""Approval gate for rollback/policy state transitions."""

from __future__ import annotations

from datetime import UTC, datetime
from pydantic import BaseModel, ConfigDict, Field
from threading import Lock
from uuid import uuid4


class ApprovalGateError(ValueError):
    """Raised when approval preconditions are not met."""


class ApprovalTicket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ticket_id: str = Field(default_factory=lambda: f"tkt_{uuid4().hex[:12]}")
    tenant_id: str = Field(..., min_length=1)
    action_type: str = Field(..., min_length=1)
    run_id: str = Field(..., min_length=1)
    requested_by: str = Field(..., min_length=1)
    state: str = "pending"
    reason: str = ""
    granted_by: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    resolved_at: datetime | None = None


class InMemoryApprovalGate:
    """MVP approval gate backend."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._tickets: dict[str, ApprovalTicket] = {}

    def request(
        self,
        *,
        tenant_id: str,
        action_type: str,
        run_id: str,
        requested_by: str,
        reason: str = "",
    ) -> ApprovalTicket:
        ticket = ApprovalTicket(
            tenant_id=tenant_id,
            action_type=action_type,
            run_id=run_id,
            requested_by=requested_by,
            reason=reason,
        )
        with self._lock:
            self._tickets[ticket.ticket_id] = ticket
        return ticket

    def grant(self, *, tenant_id: str, ticket_id: str, granted_by: str) -> ApprovalTicket:
        with self._lock:
            ticket = self._tickets.get(ticket_id)
            if ticket is None or ticket.tenant_id != tenant_id:
                raise ApprovalGateError("approval ticket not found")
            if ticket.state != "pending":
                raise ApprovalGateError("approval ticket already resolved")
            resolved = ticket.model_copy(
                update={
                    "state": "approved",
                    "granted_by": granted_by,
                    "resolved_at": datetime.now(UTC),
                },
            )
            self._tickets[ticket_id] = resolved
            return resolved

    def require_granted(self, *, tenant_id: str, ticket_id: str) -> None:
        with self._lock:
            ticket = self._tickets.get(ticket_id)
            if ticket is None or ticket.tenant_id != tenant_id:
                raise ApprovalGateError("approval ticket not found")
            if ticket.state != "approved":
                raise ApprovalGateError("approval required before finalize")

    def list_pending(self, *, tenant_id: str) -> list[ApprovalTicket]:
        with self._lock:
            return [
                row
                for row in self._tickets.values()
                if row.tenant_id == tenant_id and row.state == "pending"
            ]

    def get(self, *, tenant_id: str, ticket_id: str) -> ApprovalTicket | None:
        with self._lock:
            row = self._tickets.get(ticket_id)
        if row is None or row.tenant_id != tenant_id:
            return None
        return row

    def clear_for_test(self) -> None:
        with self._lock:
            self._tickets.clear()


__all__ = ["ApprovalGateError", "ApprovalTicket", "InMemoryApprovalGate"]
