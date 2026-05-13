"""Audit Trail — append-only structured records.

See ``docs/command_control/AUDIT_TRAIL.md``. Persistence is intentionally
out of scope here; the in-memory trail is the typed surface that storage
adapters wrap.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable


@dataclass(frozen=True)
class AuditEvent:
    audit_event_id: str
    actor: str
    human_owner: str
    action: str
    dataset_id: str | None
    policy_decision: str
    approval_required: bool
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.audit_event_id:
            raise ValueError("audit_event_id_required")
        if not self.actor:
            raise ValueError("actor_required")
        if not self.human_owner:
            raise ValueError("human_owner_required")
        if not self.action:
            raise ValueError("action_required")

    def to_dict(self) -> dict[str, object]:
        return {
            "audit_event_id": self.audit_event_id,
            "actor": self.actor,
            "human_owner": self.human_owner,
            "action": self.action,
            "dataset_id": self.dataset_id,
            "policy_decision": self.policy_decision,
            "approval_required": self.approval_required,
            "timestamp": self.timestamp.isoformat(),
            "metadata": dict(self.metadata),
        }


class AuditTrail:
    """Append-only audit trail. Edits and deletes are forbidden by design."""

    def __init__(self) -> None:
        self._events: list[AuditEvent] = []
        self._seen_ids: set[str] = set()

    def append(self, event: AuditEvent) -> AuditEvent:
        if event.audit_event_id in self._seen_ids:
            raise ValueError(f"duplicate_audit_event_id:{event.audit_event_id}")
        self._seen_ids.add(event.audit_event_id)
        self._events.append(event)
        return event

    def all(self) -> tuple[AuditEvent, ...]:
        return tuple(self._events)

    def by_actor(self, actor: str) -> tuple[AuditEvent, ...]:
        return tuple(e for e in self._events if e.actor == actor)

    def by_dataset(self, dataset_id: str) -> tuple[AuditEvent, ...]:
        return tuple(e for e in self._events if e.dataset_id == dataset_id)

    def export(self, events: Iterable[AuditEvent] | None = None) -> list[dict[str, object]]:
        return [e.to_dict() for e in (events if events is not None else self._events)]
