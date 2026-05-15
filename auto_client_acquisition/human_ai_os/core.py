"""System 33 — the Human-AI Operating Model.

Delegation, escalation, explainability and a human oversight surface. The
future is human + AI co-intelligence, not AI replacing humans — so humans must
be able to delegate, escalate, understand decisions, and intervene.

Delegations are always bounded (mandatory expiry — `no_unbounded_agents`).
Escalations create an approval-gate ticket; the oversight queue is the API
surface humans use to grant or reject pending control-plane actions.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from auto_client_acquisition.control_plane_os.approval_gate import (
    ControlApprovalGate,
    get_approval_gate,
)
from auto_client_acquisition.control_plane_os.ledger import (
    ControlEventType,
    ControlLedger,
    emit,
    get_control_ledger,
)
from auto_client_acquisition.human_ai_os.schemas import (
    Delegation,
    Escalation,
    Explanation,
    OversightItem,
)

_MODULE = "human_ai_os"


class HumanAIError(ValueError):
    """Raised on an invalid human-AI operation — never swallowed."""


class HumanAIModel:
    """Delegation, escalation and oversight for human + AI co-operation."""

    def __init__(
        self,
        *,
        gate: ControlApprovalGate | None = None,
        ledger: ControlLedger | None = None,
    ) -> None:
        self._delegations: dict[str, Delegation] = {}
        self._escalations: dict[str, Escalation] = {}
        self._gate = gate or get_approval_gate()
        self._ledger = ledger or get_control_ledger()

    def delegate(
        self,
        *,
        from_human: str,
        to_agent: str,
        scope: list[str],
        ttl_hours: float,
    ) -> Delegation:
        """Delegate bounded authority to an agent. TTL must be positive."""
        if ttl_hours <= 0:
            raise HumanAIError(
                "delegation requires a positive ttl_hours — "
                "unbounded delegation is forbidden"
            )
        delegation = Delegation(
            from_human=from_human,
            to_agent=to_agent,
            scope=scope,
            expires_at=datetime.now(UTC) + timedelta(hours=ttl_hours),
        )
        self._delegations[delegation.delegation_id] = delegation
        emit(
            event_type=ControlEventType.DELEGATION_CREATED,
            source_module=_MODULE,
            actor=from_human,
            subject_type="agent",
            subject_id=to_agent,
            payload={"scope": scope, "expires_at": delegation.expires_at.isoformat()},
        )
        return delegation

    def revoke_delegation(
        self, delegation_id: str, *, actor: str = "system"
    ) -> Delegation:
        delegation = self._delegations.get(delegation_id)
        if delegation is None:
            raise HumanAIError(f"delegation not found: {delegation_id}")
        delegation.revoked = True
        emit(
            event_type=ControlEventType.DELEGATION_REVOKED,
            source_module=_MODULE,
            actor=actor,
            subject_type="agent",
            subject_id=delegation.to_agent,
            payload={"delegation_id": delegation_id},
        )
        return delegation

    def is_delegation_active(self, delegation_id: str) -> bool:
        delegation = self._delegations.get(delegation_id)
        if delegation is None or delegation.revoked:
            return False
        return delegation.expires_at > datetime.now(UTC)

    def escalate(
        self, *, run_id: str, reason: str, escalated_to: str = "founder"
    ) -> Escalation:
        """Escalate a run to a human — creates an approval-gate ticket."""
        ticket = self._gate.submit(
            action_type="escalation",
            description=f"Escalation on run {run_id}: {reason}",
            requested_by=_MODULE,
            source_module=_MODULE,
            subject_type="workflow_run",
            subject_id=run_id,
            run_id=run_id,
        )
        escalation = Escalation(
            run_id=run_id,
            reason=reason,
            escalated_to=escalated_to,
            ticket_id=ticket.ticket_id,
        )
        self._escalations[escalation.escalation_id] = escalation
        emit(
            event_type=ControlEventType.ESCALATION_RAISED,
            source_module=_MODULE,
            subject_type="workflow_run",
            subject_id=run_id,
            run_id=run_id,
            decision="escalate",
            payload={"reason": reason, "ticket_id": ticket.ticket_id},
        )
        return escalation

    def explain(self, subject_id: str) -> Explanation:
        """Explain a subject by reconstructing its control-event trail."""
        events = [
            e
            for e in self._ledger.list_events(limit=1000)
            if e.subject_id == subject_id
        ]
        factors = [
            {
                "event_type": str(e.event_type),
                "decision": e.decision,
                "actor": e.actor,
                "at": e.occurred_at.isoformat(),
            }
            for e in sorted(events, key=lambda e: e.occurred_at)
        ]
        last_decision = events[-1].decision if events else "n/a"
        confidence = 0.9 if events else 0.0
        return Explanation(
            subject_id=subject_id,
            decision=last_decision,
            factors=factors,
            evidence_refs=[e.id for e in events],
            confidence=confidence,
        )

    def oversight_queue(self, *, source_module: str | None = None) -> list[OversightItem]:
        """The pending-approval queue humans review."""
        return [
            OversightItem(
                ticket_id=t.ticket_id,
                action_type=t.action_type,
                description=t.description,
                requested_by=t.requested_by,
                source_module=t.source_module,
                run_id=t.run_id,
                created_at=t.created_at,
            )
            for t in self._gate.list_pending(source_module=source_module)
        ]

    def grant(self, ticket_id: str, approver: str) -> dict[str, str]:
        ticket = self._gate.grant(ticket_id, approver)
        return {"ticket_id": ticket.ticket_id, "state": str(ticket.state)}

    def reject(self, ticket_id: str, approver: str, reason: str = "") -> dict[str, str]:
        ticket = self._gate.reject(ticket_id, approver, reason)
        return {"ticket_id": ticket.ticket_id, "state": str(ticket.state)}


_MODEL: HumanAIModel | None = None


def get_human_ai_model() -> HumanAIModel:
    """Return the process-scoped human-AI model singleton."""
    global _MODEL
    if _MODEL is None:
        _MODEL = HumanAIModel()
    return _MODEL


def reset_human_ai_model() -> None:
    """Test helper: drop the cached model."""
    global _MODEL
    _MODEL = None


__all__ = [
    "HumanAIError",
    "HumanAIModel",
    "get_human_ai_model",
    "reset_human_ai_model",
]
