"""Board Scorecards — Offer / Client / Productization."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


OFFER_SCORECARD_WEIGHTS: dict[str, int] = {
    "win_rate": 15,
    "gross_margin": 15,
    "proof_strength": 20,
    "retainer_conversion": 20,
    "repeatability": 15,
    "governance_safety": 10,
    "productization_signal": 5,
}


CLIENT_SCORECARD_WEIGHTS: dict[str, int] = {
    "clear_pain": 15,
    "executive_sponsor": 15,
    "data_readiness": 15,
    "governance_alignment": 15,
    "adoption_score": 15,
    "proof_score": 15,
    "expansion_potential": 10,
}


PRODUCTIZATION_SCORECARD_WEIGHTS: dict[str, int] = {
    "repeated_pain": 20,
    "delivery_hours_saved": 20,
    "revenue_linkage": 20,
    "risk_reduction": 15,
    "client_pull": 15,
    "build_simplicity": 10,
}


class ScorecardTier(str, Enum):
    SCALE_BUILD_NOW = "scale_or_build_now"          # 85+
    IMPROVE_MVP = "improve_or_mvp"                  # 70..84
    PILOT_TEMPLATE = "pilot_or_template_only"       # 55..69
    HOLD_KILL = "hold_or_kill"                      # <55


def classify_scorecard(score: int) -> ScorecardTier:
    if score >= 85:
        return ScorecardTier.SCALE_BUILD_NOW
    if score >= 70:
        return ScorecardTier.IMPROVE_MVP
    if score >= 55:
        return ScorecardTier.PILOT_TEMPLATE
    return ScorecardTier.HOLD_KILL


def _weighted(values: dict[str, int], weights: dict[str, int]) -> int:
    total = 0.0
    for k, w in weights.items():
        v = values.get(k, 0)
        if not 0 <= v <= 100:
            raise ValueError(f"{k}_out_of_range_0_100")
        total += v * (w / 100.0)
    return round(total)


@dataclass(frozen=True)
class OfferScorecardComponents:
    win_rate: int
    gross_margin: int
    proof_strength: int
    retainer_conversion: int
    repeatability: int
    governance_safety: int
    productization_signal: int

    def values(self) -> dict[str, int]:
        return {k: getattr(self, k) for k in OFFER_SCORECARD_WEIGHTS}


@dataclass(frozen=True)
class ClientScorecardComponents:
    clear_pain: int
    executive_sponsor: int
    data_readiness: int
    governance_alignment: int
    adoption_score: int
    proof_score: int
    expansion_potential: int

    def values(self) -> dict[str, int]:
        return {k: getattr(self, k) for k in CLIENT_SCORECARD_WEIGHTS}


@dataclass(frozen=True)
class ProductizationScorecardComponents:
    repeated_pain: int
    delivery_hours_saved: int
    revenue_linkage: int
    risk_reduction: int
    client_pull: int
    build_simplicity: int

    def values(self) -> dict[str, int]:
        return {k: getattr(self, k) for k in PRODUCTIZATION_SCORECARD_WEIGHTS}


def compute_offer_scorecard(c: OfferScorecardComponents) -> int:
    return _weighted(c.values(), OFFER_SCORECARD_WEIGHTS)


def compute_client_scorecard(c: ClientScorecardComponents) -> int:
    return _weighted(c.values(), CLIENT_SCORECARD_WEIGHTS)


def compute_productization_scorecard(c: ProductizationScorecardComponents) -> int:
    return _weighted(c.values(), PRODUCTIZATION_SCORECARD_WEIGHTS)
