"""Audit event shape for enterprise traceability."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuditEvent:
    audit_event_id: str
    actor_type: str
    actor_id: str
    human_owner: str
    action: str
    dataset_id: str
    source_id: str
    policy_decision: str
    approval_required: bool
    timestamp: str


def audit_event_complete(event: AuditEvent) -> bool:
    """Minimum fields for an institutional audit record."""
    return all(
        (
            event.audit_event_id.strip(),
            event.actor_type.strip(),
            event.actor_id.strip(),
            event.human_owner.strip(),
            event.action.strip(),
            event.dataset_id.strip(),
            event.source_id.strip(),
            event.policy_decision.strip(),
            event.timestamp.strip(),
        ),
    )
