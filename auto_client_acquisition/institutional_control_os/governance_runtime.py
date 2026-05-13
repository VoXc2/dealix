"""Institutional runtime governance — 8-question evaluator record.

See ``docs/institutional_control/RUNTIME_GOVERNANCE.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from auto_client_acquisition.endgame_os.governance_product import (
    GovernanceDecision,
)


class GovernanceRuntimeQuestion(str, Enum):
    SOURCE_STATUS = "source_status"
    PII_STATUS = "pii_status"
    ALLOWED_USE = "allowed_use"
    CLAIM_RISK = "claim_risk"
    CHANNEL_RISK = "channel_risk"
    AGENT_AUTONOMY = "agent_autonomy"
    APPROVAL_REQUIREMENT = "approval_requirement"
    AUDIT_EVENT = "audit_event"


REQUIRED_RUNTIME_QUESTIONS: tuple[GovernanceRuntimeQuestion, ...] = tuple(
    GovernanceRuntimeQuestion
)


@dataclass(frozen=True)
class RuntimeEvaluationRecord:
    """One pre-action evaluation against every required question."""

    decision: GovernanceDecision
    risk_level: str
    answers: dict[GovernanceRuntimeQuestion, bool]
    matched_rules: tuple[str, ...] = ()
    redactions: tuple[str, ...] = ()
    audit_event_id: str | None = None
    next_action: str | None = None
    reason: str = ""
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        missing = set(REQUIRED_RUNTIME_QUESTIONS) - set(self.answers)
        if missing:
            raise ValueError(
                "missing_runtime_answers:"
                + ",".join(sorted(q.value for q in missing))
            )

    def is_blocking(self) -> bool:
        return self.decision in {
            GovernanceDecision.BLOCK,
            GovernanceDecision.REDACT,
            GovernanceDecision.REQUIRE_APPROVAL,
            GovernanceDecision.ESCALATE,
        }
