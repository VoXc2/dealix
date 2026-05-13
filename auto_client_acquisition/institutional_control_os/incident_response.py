"""Incident Response — types, severity, response flow.

See ``docs/institutional_control/INCIDENT_RESPONSE.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class IncidentType(str, Enum):
    PII_EXPOSURE = "pii_exposure"
    SOURCE_MISUSE = "source_misuse"
    UNAPPROVED_EXTERNAL_ACTION = "unapproved_external_action"
    UNSUPPORTED_CLAIM = "unsupported_claim"
    HALLUCINATED_ANSWER = "hallucinated_answer"
    WRONG_CLIENT_DATA = "wrong_client_data"
    PARTNER_VIOLATION = "partner_violation"


class IncidentSeverity(str, Enum):
    SEV_1 = "sev_1"
    SEV_2 = "sev_2"
    SEV_3 = "sev_3"
    SEV_4 = "sev_4"


INCIDENT_RESPONSE_STEPS: tuple[str, ...] = (
    "detect",
    "contain",
    "notify_internal_owner",
    "assess_severity",
    "correct_output",
    "log_incident",
    "update_rule",
    "add_test",
    "update_playbook",
)


@dataclass(frozen=True)
class IncidentRecord:
    incident_id: str
    type: IncidentType
    severity: IncidentSeverity
    detected_at: datetime
    contained_at: datetime | None
    owner: str
    description: str
    affected_clients: tuple[str, ...] = ()
    rule_updated: bool = False
    test_added: bool = False
    playbook_updated: bool = False
    postmortem_url: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.incident_id:
            raise ValueError("incident_id_required")
        if not self.owner:
            raise ValueError("owner_required")
        if not self.description:
            raise ValueError("description_required")


def incident_must_create_change(record: IncidentRecord) -> bool:
    """Doctrine: every Sev-1/Sev-2 incident must produce a rule, test, or
    playbook update before it can be closed.
    """

    if record.severity in {IncidentSeverity.SEV_1, IncidentSeverity.SEV_2}:
        return not (record.rule_updated or record.test_added or record.playbook_updated)
    return False
