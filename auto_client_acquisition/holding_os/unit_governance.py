"""Holding unit governance and portfolio-style decisions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class UnitPortfolioDecision(StrEnum):
    SCALE = "scale"
    BUILD = "build"
    PILOT = "pilot"
    HOLD = "hold"
    KILL = "kill"
    SPINOUT = "spinout"


@dataclass(frozen=True, slots=True)
class UnitMonthlySnapshot:
    revenue_growing: bool = False
    margin_ok: bool = False
    retainers_growing: bool = False
    proof_delivery_on_track: bool = False
    qa_score: float = 0.0
    governance_risk_acceptable: bool = False
    module_usage_growing: bool = False
    playbook_maturity_ok: bool = False
    client_health_ok: bool = False
    venture_signal_strong: bool = False


def evaluate_unit_decision(snapshot: UnitMonthlySnapshot) -> UnitPortfolioDecision:
    """Conservative rules for monthly unit review (template, not legal advice)."""
    if not snapshot.governance_risk_acceptable:
        return UnitPortfolioDecision.HOLD
    if not snapshot.client_health_ok:
        return UnitPortfolioDecision.PILOT
    if snapshot.qa_score < 55 and not snapshot.revenue_growing:
        return UnitPortfolioDecision.KILL
    if snapshot.venture_signal_strong and snapshot.module_usage_growing and snapshot.qa_score >= 85:
        return UnitPortfolioDecision.SPINOUT
    if (
        snapshot.revenue_growing
        and snapshot.margin_ok
        and snapshot.qa_score >= 80
        and snapshot.retainers_growing
    ):
        return UnitPortfolioDecision.SCALE
    if snapshot.playbook_maturity_ok and snapshot.proof_delivery_on_track:
        return UnitPortfolioDecision.BUILD
    return UnitPortfolioDecision.PILOT
