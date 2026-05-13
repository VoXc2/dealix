"""Runtime Governance Product — typed record + tier-by-readiness helper.

See ``docs/global_grade/RUNTIME_GOVERNANCE_PRODUCT.md``. This module
mirrors the endgame-layer governance vocabulary, packaged for enterprise
contracting and reporting.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from auto_client_acquisition.endgame_os.governance_product import (
    GovernanceDecision,
    GovernanceProductForm,
    SAFE_DEFAULT_DECISION,
)


class RuntimeProductTier(str, Enum):
    EMBEDDED = GovernanceProductForm.EMBEDDED.value
    STANDALONE_REVIEW = GovernanceProductForm.STANDALONE_REVIEW.value
    MANAGED = GovernanceProductForm.MANAGED.value


@dataclass(frozen=True)
class RuntimeEvaluation:
    """A typed evaluation record matching the enterprise reporting shape."""

    decision: GovernanceDecision
    risk_level: str
    matched_rules: tuple[str, ...] = ()
    redactions: tuple[str, ...] = ()
    audit_event_id: str | None = None
    next_action: str | None = None
    agent_id: str | None = None
    workflow_id: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    @classmethod
    def fail_closed(cls, *, reason: str) -> "RuntimeEvaluation":
        """Construct the fail-closed evaluation used on unexpected errors."""

        return cls(
            decision=SAFE_DEFAULT_DECISION,
            risk_level="unknown",
            matched_rules=("runtime_error_fail_closed",),
            next_action="operator_review",
            metadata={"reason": reason},
        )


def runtime_tier_for_readiness(readiness_level: int) -> RuntimeProductTier:
    """Map an enterprise readiness level to the runtime product tier.

    Levels 1–2 ship Embedded only. Level 3 unlocks Standalone Review.
    Levels 4–5 unlock Managed.
    """

    if readiness_level >= 4:
        return RuntimeProductTier.MANAGED
    if readiness_level == 3:
        return RuntimeProductTier.STANDALONE_REVIEW
    return RuntimeProductTier.EMBEDDED
