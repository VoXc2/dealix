"""Auditability OS — append-only audit events for policy / approval trails."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuditEvent:
    """Minimal enterprise-audit row (persisted by callers; schema-stable)."""

    event_id: str
    actor: str
    source: str
    policy_checked: str
    matched_rule: str
    decision: str
    approval_status: str
    output_id: str
    timestamp_iso: str


def audit_event_valid(e: AuditEvent) -> bool:
    return all(
        (
            e.event_id.strip(),
            e.actor.strip(),
            e.source.strip(),
            e.policy_checked.strip(),
            e.decision.strip(),
            e.timestamp_iso.strip(),
        ),
    )


__all__ = ["AuditEvent", "audit_event_valid"]
