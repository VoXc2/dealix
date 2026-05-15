"""ROI OS schemas — ROI lines, snapshots, executive briefs.

Doctrine: a ROI line marked ``verified`` MUST carry a non-empty
``evidence_ref`` (``no_fake_proof`` / ``no_unverified_outcomes``).
Estimated figures are always labelled ``estimated`` and never presented
as verified.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

__all__ = ["ROILine", "ROISnapshot", "ExecutiveBrief", "roi_snapshot_valid"]

CONFIDENCE_TIERS: tuple[str, ...] = ("verified", "estimated")


@dataclass(frozen=True, slots=True)
class ROILine:
    """One line of the ROI ledger view."""

    label: str
    value_sar: float
    confidence: str  # "verified" | "estimated"
    evidence_ref: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ROISnapshot:
    """A point-in-time ROI computation for one customer."""

    snapshot_id: str = field(default_factory=lambda: f"roi_{uuid4().hex[:16]}")
    customer_id: str = ""
    window_days: int = 30
    agent_runs: int = 0
    grounded_answers: int = 0
    eval_pass_rate: float = 0.0
    knowledge_grounding_rate: float = 0.0
    verified_value_sar: float = 0.0
    estimated_value_sar: float = 0.0
    llm_cost_sar: float = 0.0
    net_roi_sar: float = 0.0
    lines: tuple[ROILine, ...] = ()
    occurred_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "customer_id": self.customer_id,
            "window_days": self.window_days,
            "agent_runs": self.agent_runs,
            "grounded_answers": self.grounded_answers,
            "eval_pass_rate": self.eval_pass_rate,
            "knowledge_grounding_rate": self.knowledge_grounding_rate,
            "verified_value_sar": self.verified_value_sar,
            "estimated_value_sar": self.estimated_value_sar,
            "llm_cost_sar": self.llm_cost_sar,
            "net_roi_sar": self.net_roi_sar,
            "lines": [line.to_dict() for line in self.lines],
            "occurred_at": self.occurred_at,
        }


@dataclass(frozen=True, slots=True)
class ExecutiveBrief:
    """A board-readable narrative built from a ROISnapshot."""

    customer_id: str
    window_days: int
    headline: str
    markdown: str
    snapshot: ROISnapshot

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "window_days": self.window_days,
            "headline": self.headline,
            "markdown": self.markdown,
            "snapshot": self.snapshot.to_dict(),
        }


def roi_snapshot_valid(snapshot: ROISnapshot) -> bool:
    """Valid iff every ``verified`` line carries evidence and the tier is known."""
    for line in snapshot.lines:
        if line.confidence not in CONFIDENCE_TIERS:
            return False
        if line.confidence == "verified" and not line.evidence_ref.strip():
            return False
    return bool(snapshot.customer_id.strip())
