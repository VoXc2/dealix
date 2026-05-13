"""Governance runtime — decision vocabulary and product packaging.

This module does not perform governance evaluation (that lives in
``auto_client_acquisition.governance_os``). It encodes the **product**
shape of the runtime so the rest of the firm can reason about it
consistently — see ``docs/endgame/RUNTIME_GOVERNANCE_PRODUCT.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class GovernanceDecision(str, Enum):
    """The decision vocabulary the runtime is allowed to emit."""

    ALLOW = "ALLOW"
    ALLOW_WITH_REVIEW = "ALLOW_WITH_REVIEW"
    DRAFT_ONLY = "DRAFT_ONLY"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"
    REDACT = "REDACT"
    BLOCK = "BLOCK"
    ESCALATE = "ESCALATE"


# The fail-closed default. Any unexpected error inside the runtime must
# fall back to DRAFT_ONLY rather than ALLOW.
SAFE_DEFAULT_DECISION: GovernanceDecision = GovernanceDecision.DRAFT_ONLY


class GovernanceProductForm(str, Enum):
    """The three product packages of the runtime."""

    EMBEDDED = "embedded"        # bundled into every engagement
    STANDALONE_REVIEW = "standalone_review"  # the AI Governance Review offer
    MANAGED = "managed"          # Monthly Governance retainer


@dataclass(frozen=True)
class GovernanceRuntimeDecision:
    """A structured decision record matching the doctrine example."""

    decision: GovernanceDecision
    risk_level: str
    matched_rules: tuple[str, ...] = ()
    redactions: tuple[str, ...] = ()
    audit_event_id: str | None = None
    next_action: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "decision": self.decision.value,
            "risk_level": self.risk_level,
            "matched_rules": list(self.matched_rules),
            "redactions": list(self.redactions),
            "audit_event_id": self.audit_event_id,
            "next_action": self.next_action,
            "metadata": dict(self.metadata),
        }


def coerce_decision(value: str | GovernanceDecision) -> GovernanceDecision:
    """Coerce a raw value into the decision enum, falling back safely.

    Any unknown value collapses to ``SAFE_DEFAULT_DECISION``. This is the
    enforcement of the doctrine rule that cost or rate-limit failures
    must never default to ``ALLOW``.
    """

    if isinstance(value, GovernanceDecision):
        return value
    try:
        return GovernanceDecision(value)
    except ValueError:
        return SAFE_DEFAULT_DECISION
