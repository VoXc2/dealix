"""V18 Portfolio Graph + priority scoring (Workstream C, §7-8).

Aggregates opportunities across lanes and ranks by risk-adjusted expected
verified movement per scarce resource consumed. The score is ordinal aid;
assumptions are recorded; no fake mathematical precision.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class PortfolioLane(StrEnum):
    FIRST_FIVE_DIRECT = "FIRST_FIVE_DIRECT"
    WARM_NETWORK = "WARM_NETWORK"
    EVENT_RELATIONSHIP = "EVENT_RELATIONSHIP"
    PARTNER_CHANNEL = "PARTNER_CHANNEL"
    B2G_PARTNER_GO = "B2G_PARTNER_GO"
    INBOUND = "INBOUND"
    CONTENT = "CONTENT"
    SEARCH_AEO = "SEARCH_AEO"
    PROOF_DISTRIBUTION = "PROOF_DISTRIBUTION"
    PRODUCTIZATION = "PRODUCTIZATION"


_VALID_LANES = frozenset(l.value for l in PortfolioLane)


@dataclass(frozen=True, slots=True)
class PortfolioItem:
    """One portfolio item across any lane. Evidence fields only."""

    item_id: str
    lane: str
    current_stage: str = "RESEARCH_ONLY"
    relationship_state: str = "unknown"
    buyability_score: float = 0.0
    evidence_strength: int = 0  # 0..5
    expected_next_evidence: str = ""
    time_to_evidence_days: int = 30
    founder_minutes: int = 60
    agent_cost: float = 0.0  # ordinal agent effort units
    delivery_load: int = 0  # 0..5
    risk: int = 3  # 1..5
    reversibility: int = 5  # 1..5 (5 = fully reversible)
    strategic_reuse: int = 0  # 0..5
    proof_potential: int = 0  # 0..5
    recurring_potential: int = 0  # 0..5
    probability_of_movement: float = 0.3  # 0..1, ordinal aid, not a stat
    account_id: str = ""
    company: str = ""
    assumptions: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "lane": self.lane,
            "account_id": self.account_id,
            "company": self.company,
            "current_stage": self.current_stage,
            "relationship_state": self.relationship_state,
            "buyability_score": round(self.buyability_score, 2),
            "evidence_strength": self.evidence_strength,
            "expected_next_evidence": self.expected_next_evidence,
            "time_to_evidence_days": self.time_to_evidence_days,
            "founder_minutes": self.founder_minutes,
            "agent_cost": self.agent_cost,
            "delivery_load": self.delivery_load,
            "risk": self.risk,
            "reversibility": self.reversibility,
            "strategic_reuse": self.strategic_reuse,
            "proof_potential": self.proof_potential,
            "recurring_potential": self.recurring_potential,
            "probability_of_movement": self.probability_of_movement,
            "assumptions": list(self.assumptions),
        }


def value_score(item: PortfolioItem) -> float:
    """VALUE_SCORE = expected evidence value × movement probability × reuse
    factors ÷ scarce resources consumed.

    Deliberately coarse ordinal arithmetic with recorded assumptions, not a
    financial model. Returns 0..100.
    """
    expected_evidence_value = (
        (item.evidence_strength + 1)
        * (item.proof_potential + 1)
        * (item.strategic_reuse + 1)
        * (item.recurring_potential + 1)
    ) / 625.0  # normalize to ~0..1
    probability = max(0.01, min(1.0, item.probability_of_movement))

    scarce = (
        max(1, item.founder_minutes)
        + max(1, item.agent_cost * 20)
        + item.delivery_load * 40
        + item.risk * 20
        + max(0, 6 - item.reversibility) * 10
    )
    score = (
        expected_evidence_value
        * probability
        * 1000.0
        / scarce
    )
    return round(max(0.0, min(100.0, score)), 2)


@dataclass(frozen=True, slots=True)
class PortfolioRanking:
    """Deterministic ranking of portfolio items with assumptions."""

    items: tuple[PortfolioItem, ...]
    ranked_ids: tuple[str, ...]
    scores: dict[str, float]
    assumptions: tuple[str, ...] = ()

    def top(self, n: int = 5) -> list[PortfolioItem]:
        return list(self.items[: max(1, n)])

    def to_dict(self) -> dict[str, Any]:
        return {
            "ranked_ids": list(self.ranked_ids),
            "scores": {k: round(v, 2) for k, v in self.scores.items()},
            "assumptions": list(self.assumptions),
        }


def rank_portfolio(items: list[PortfolioItem]) -> PortfolioRanking:
    """Rank by value_score descending; stable tie-break by item_id."""
    if not items:
        return PortfolioRanking(
            items=(), ranked_ids=(), scores={}, assumptions=("empty portfolio",)
        )
    scored = [(value_score(i), i.item_id, i) for i in items]
    scored.sort(key=lambda t: (-t[0], t[1]))
    ranked = tuple(i for _, _, i in scored)
    scores = {i.item_id: value_score(i) for i in items}
    return PortfolioRanking(
        items=ranked,
        ranked_ids=tuple(i.item_id for i in ranked),
        scores=scores,
        assumptions=(
            "score is ordinal aid; never qualification evidence",
            "probability_of_movement is an ordinal estimate, not a statistic",
        ),
    )
