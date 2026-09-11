"""Probability Engine — evidence-aware, range-based.

Models P(PROBLEM_IS_REAL) etc., updates via Bayes via evidence.
Never fake precision; weak evidence uses ordinal bands.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN"

class ProbBand(StrEnum):
    VERY_LOW = "very_low"  # 0.05-0.15
    LOW = "low"  # 0.15-0.35
    MEDIUM = "medium"  # 0.35-0.65
    HIGH = "high"  # 0.65-0.85
    VERY_HIGH = "very_high"  # 0.85-0.95

    def to_range(self) -> tuple[float, float]:
        return {
            "very_low": (0.05, 0.15),
            "low": (0.15, 0.35),
            "medium": (0.35, 0.65),
            "high": (0.65, 0.85),
            "very_high": (0.85, 0.95),
        }[self.value]

    def midpoint(self) -> float:
        lo, hi = self.to_range()
        return round((lo + hi) / 2, 3)

class ProbabilityVector(BaseModel):
    model_config = ConfigDict(extra="forbid")

    p_problem_real: ProbBand = ProbBand.MEDIUM
    p_reach_buyer: ProbBand = ProbBand.MEDIUM
    p_buyer_authority: ProbBand = ProbBand.MEDIUM
    p_urgency: ProbBand = ProbBand.MEDIUM
    p_diagnostic_accepted: ProbBand = ProbBand.MEDIUM
    p_discovery_progress: ProbBand = ProbBand.MEDIUM
    p_quote_accepted: ProbBand = ProbBand.LOW
    p_payment: ProbBand = ProbBand.LOW
    p_delivery_success: ProbBand = ProbBand.MEDIUM
    p_expansion: ProbBand = ProbBand.LOW

    def expected_chain(self) -> float:
        # chain product of midpoints
        vals = [self.p_problem_real.midpoint(), self.p_reach_buyer.midpoint(), self.p_buyer_authority.midpoint(), self.p_urgency.midpoint(), self.p_quote_accepted.midpoint(), self.p_payment.midpoint()]
        prod = 1.0
        for v in vals:
            prod *= v
        return round(prod, 4)

    def update(self, evidence: str, delta: str = "positive") -> "ProbabilityVector":
        # Simple Bayesian update: positive evidence nudges bands up one, negative down one
        order = [ProbBand.VERY_LOW, ProbBand.LOW, ProbBand.MEDIUM, ProbBand.HIGH, ProbBand.VERY_HIGH]
        def bump(band: ProbBand, d: int) -> ProbBand:
            idx = order.index(band)
            return order[max(0, min(len(order)-1, idx + d))]
        d = 1 if delta == "positive" else -1
        # Update relevant band based on evidence keyword
        data = self.model_dump()
        if "problem" in evidence:
            data["p_problem_real"] = bump(self.p_problem_real, d)
        if "buyer" in evidence or "reach" in evidence:
            data["p_reach_buyer"] = bump(self.p_reach_buyer, d)
        if "authority" in evidence:
            data["p_buyer_authority"] = bump(self.p_buyer_authority, d)
        if "urgency" in evidence or "payment" in evidence:
            data["p_urgency"] = bump(self.p_urgency, d)
        if "quote" in evidence:
            data["p_quote_accepted"] = bump(self.p_quote_accepted, d)
        return ProbabilityVector(**data)

class BetState(StrEnum):
    IDEA = "idea"
    WATCH = "watch"
    CHEAP_TEST = "cheap_test"
    VALIDATING = "validating"
    PROMISING = "promising"
    QUALIFIED = "qualified"
    ACTIVE_DEEP = "active_deep"
    WINNING = "winning"
    SCALING = "scaling"
    PAUSED = "paused"
    KILLED = "killed"

class EconomicBet(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bet_id: str
    economic_cell_id: str
    sector: str = UNKNOWN
    buyer: str = UNKNOWN
    problem: str = UNKNOWN
    offer: str = UNKNOWN
    channel: str = UNKNOWN
    relationship: str = UNKNOWN
    hypothesis: str = UNKNOWN
    prior: ProbBand = ProbBand.MEDIUM
    current: ProbBand = ProbBand.MEDIUM
    expected_value_sar: float = 0.0
    expected_gross_profit_sar: float = 0.0
    time_to_cash_days: int = 30
    cost_to_test_sar: float = 0.0
    founder_minutes: int = 60
    engineering_minutes: int = 0
    delivery_cost_sar: float = 0.0
    information_value: str = UNKNOWN
    confidence: ProbBand = ProbBand.MEDIUM
    experiment: str = UNKNOWN
    success_condition: str = UNKNOWN
    kill_condition: str = UNKNOWN
    next_review: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    state: BetState = BetState.IDEA
    probability_vector: ProbabilityVector = Field(default_factory=ProbabilityVector)

    def expected_chain_value(self) -> float:
        return round(self.expected_gross_profit_sar * self.probability_vector.expected_chain(), 2)

__all__ = ["ProbabilityVector", "ProbBand", "EconomicBet", "BetState", "UNKNOWN"]
