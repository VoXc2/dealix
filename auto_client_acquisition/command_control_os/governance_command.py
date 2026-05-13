"""Governance Command — pre-action checklist and structured record.

See ``docs/command_control/GOVERNANCE_COMMAND.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from auto_client_acquisition.endgame_os.governance_product import (
    GovernanceDecision,
)


class GovernanceCommandQuestion(str, Enum):
    SOURCE_KNOWN = "source_known"
    PII_PRESENT = "pii_present"
    USE_ALLOWED = "use_allowed"
    CLAIM_RISK = "claim_risk"
    CHANNEL_SAFE = "channel_safe"
    AGENT_AUTONOMY_OK = "agent_autonomy_ok"
    APPROVAL_REQUIRED = "approval_required"
    AUDIT_RECORDED = "audit_recorded"


REQUIRED_GOVERNANCE_QUESTIONS: tuple[GovernanceCommandQuestion, ...] = tuple(
    GovernanceCommandQuestion
)


@dataclass(frozen=True)
class GovernanceCommandRecord:
    """One pre-action evaluation answered for every required question."""

    decision: GovernanceDecision
    risk_level: str
    reason: str
    answers: dict[GovernanceCommandQuestion, bool]
    audit_event_id: str | None = None
    next_action: str | None = None

    def __post_init__(self) -> None:
        missing = set(REQUIRED_GOVERNANCE_QUESTIONS) - set(self.answers)
        if missing:
            raise ValueError(
                "missing_governance_answers:"
                + ",".join(sorted(q.value for q in missing))
            )

    def is_blocking(self) -> bool:
        return self.decision in {
            GovernanceDecision.BLOCK,
            GovernanceDecision.REDACT,
            GovernanceDecision.REQUIRE_APPROVAL,
            GovernanceDecision.ESCALATE,
        }
