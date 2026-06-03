"""Runtime governance decision vocabulary — defensive operating layer."""

from __future__ import annotations

from enum import StrEnum


class RuntimeGovernanceDecision(StrEnum):
    ALLOW = "allow"
    ALLOW_WITH_REVIEW = "allow_with_review"
    DRAFT_ONLY = "draft_only"
    REQUIRE_APPROVAL = "require_approval"
    REDACT = "redact"
    BLOCK = "block"
    ESCALATE = "escalate"


def runtime_governance_decision_valid(decision: str) -> bool:
    return decision in {e.value for e in RuntimeGovernanceDecision}
