"""Institutional Audit Trail — typed event + 100% coverage targets.

See ``docs/institutional_control/AUDIT_TRAIL_STANDARD.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class ActorType(str, Enum):
    AGENT = "agent"
    HUMAN = "human"
    SYSTEM = "system"


@dataclass(frozen=True)
class InstitutionalAuditEvent:
    audit_event_id: str
    actor_type: ActorType
    actor_id: str
    human_owner: str
    action: str
    policy_decision: str
    approval_required: bool
    dataset_id: str | None = None
    source_id: str | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.audit_event_id:
            raise ValueError("audit_event_id_required")
        if not self.actor_id:
            raise ValueError("actor_id_required")
        if not self.human_owner:
            raise ValueError("human_owner_required")
        if not self.action:
            raise ValueError("action_required")

    def to_dict(self) -> dict[str, object]:
        return {
            "audit_event_id": self.audit_event_id,
            "actor_type": self.actor_type.value,
            "actor_id": self.actor_id,
            "human_owner": self.human_owner,
            "action": self.action,
            "policy_decision": self.policy_decision,
            "approval_required": self.approval_required,
            "dataset_id": self.dataset_id,
            "source_id": self.source_id,
            "timestamp": self.timestamp.isoformat(),
            "metadata": dict(self.metadata),
        }


# Doctrine: institutional grade requires 100% coverage. Anything less is a P1 incident.
AUDIT_COVERAGE_TARGETS: dict[str, float] = {
    "ai_runs_logged": 1.0,
    "governance_decisions_logged": 1.0,
    "client_outputs_linked_to_audit": 1.0,
    "external_actions_with_approval": 1.0,
}


@dataclass(frozen=True)
class AuditCoverageReport:
    period: str
    ai_runs_logged: float
    governance_decisions_logged: float
    client_outputs_linked_to_audit: float
    external_actions_with_approval: float
    breaches: tuple[str, ...]


def evaluate_audit_coverage(
    *,
    period: str,
    ai_runs_logged: float,
    governance_decisions_logged: float,
    client_outputs_linked_to_audit: float,
    external_actions_with_approval: float,
) -> AuditCoverageReport:
    """Return a report flagging any sub-100% metric as a breach."""

    actuals = {
        "ai_runs_logged": ai_runs_logged,
        "governance_decisions_logged": governance_decisions_logged,
        "client_outputs_linked_to_audit": client_outputs_linked_to_audit,
        "external_actions_with_approval": external_actions_with_approval,
    }
    breaches = tuple(
        name
        for name, value in actuals.items()
        if value < AUDIT_COVERAGE_TARGETS[name]
    )
    return AuditCoverageReport(
        period=period,
        ai_runs_logged=ai_runs_logged,
        governance_decisions_logged=governance_decisions_logged,
        client_outputs_linked_to_audit=client_outputs_linked_to_audit,
        external_actions_with_approval=external_actions_with_approval,
        breaches=breaches,
    )
