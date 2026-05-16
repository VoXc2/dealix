"""Revenue Pipeline — the "Governed Value Decisions Created" north-star metric.

The single success metric for Dealix (strategy §2): the count of revenue or
operational decisions made with ALL FOUR of —

    clear source · clear approval · documented evidence · measurable value

A decision missing any one of the four elements is NOT counted. This module
is the pure, testable definition of that metric.

Strategy reference: docs/02_strategy/GOVERNED_REVENUE_AI_OPERATIONS.md §2.
Pure-local. NO DB. NO external call. NO LLM.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.revenue_pipeline.lead import Lead
from auto_client_acquisition.revenue_pipeline.stage_policy import counts_as_commitment

# The four elements every governed value decision must carry.
REQUIRED_ELEMENTS: tuple[str, ...] = ("source", "approval", "evidence", "value")


class GovernedValueDecision(BaseModel):
    """One revenue/operational decision, evaluated against the north-star rule."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1, max_length=64)
    source: str = ""        # where the decision came from
    approval: str = ""      # who approved it
    evidence_ref: str = ""  # pointer to documented evidence
    decision: str = ""      # what was decided
    value_sar: int | None = None  # measurable value (must be > 0 to count)
    asset_ref: str = ""     # optional reusable-asset pointer
    ts: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def missing_elements(self) -> tuple[str, ...]:
        """Which of the four required elements are absent."""
        missing: list[str] = []
        if not self.source.strip():
            missing.append("source")
        if not self.approval.strip():
            missing.append("approval")
        if not self.evidence_ref.strip():
            missing.append("evidence")
        if self.value_sar is None or self.value_sar <= 0:
            missing.append("value")
        return tuple(missing)


def qualifies_as_governed_value_decision(decision: GovernedValueDecision) -> bool:
    """True only when source, approval, evidence, and a measurable value are present."""
    return not decision.missing_elements()


def count_governed_value_decisions(
    decisions: Iterable[GovernedValueDecision],
) -> int:
    """Count only the decisions that satisfy all four required elements."""
    return sum(1 for d in decisions if qualifies_as_governed_value_decision(d))


def governed_value_decision_from_lead(lead: Lead) -> GovernedValueDecision | None:
    """Build a candidate decision from a pipeline lead.

    A lead represents a governed value decision once the founder has
    advanced it to a commitment stage. Whether it *qualifies* still
    depends on the four-element rule (e.g. a commitment with no
    measurable amount does not count).

    Returns ``None`` for leads that have not reached a commitment stage.
    """
    if not counts_as_commitment(lead.stage):
        return None
    evidence_ref = lead.payment_evidence or lead.commitment_evidence
    value_sar = lead.actual_amount_sar or lead.expected_amount_sar
    return GovernedValueDecision(
        id=f"gvd_{lead.id}",
        source=f"revenue_pipeline:{lead.slot_id}",
        approval="founder_advanced",
        evidence_ref=evidence_ref,
        decision=f"advanced lead to '{lead.stage}'",
        value_sar=value_sar,
        ts=lead.created_at,
    )
