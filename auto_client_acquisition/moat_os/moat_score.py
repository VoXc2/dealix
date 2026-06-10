"""Weighted Dealix Moat Score and tier labels."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

MoatTier = Literal["strong", "emerging", "weak", "commodity_risk"]


@dataclass(frozen=True, slots=True)
class MoatScoreDimensions:
    """Each field is 0–100; weights sum to 100 across dimensions."""

    governance_depth: int
    proof_strength: int
    product_reuse: int
    saudi_arabic_differentiation: int
    capital_assets_created: int
    partner_academy_distribution: int
    market_language_adoption: int

    def __post_init__(self) -> None:
        for name, val in (
            ("governance_depth", self.governance_depth),
            ("proof_strength", self.proof_strength),
            ("product_reuse", self.product_reuse),
            ("saudi_arabic_differentiation", self.saudi_arabic_differentiation),
            ("capital_assets_created", self.capital_assets_created),
            ("partner_academy_distribution", self.partner_academy_distribution),
            ("market_language_adoption", self.market_language_adoption),
        ):
            if not 0 <= val <= 100:
                msg = f"{name} must be 0..100, got {val}"
                raise ValueError(msg)


def weighted_moat_score(d: MoatScoreDimensions) -> int:
    """Return 0–100 composite moat score."""
    parts = (
        d.governance_depth * 20
        + d.proof_strength * 20
        + d.product_reuse * 15
        + d.saudi_arabic_differentiation * 15
        + d.capital_assets_created * 10
        + d.partner_academy_distribution * 10
        + d.market_language_adoption * 10
    )
    return parts // 100


def moat_tier(score: int) -> MoatTier:
    if score >= 85:
        return "strong"
    if score >= 70:
        return "emerging"
    if score >= 50:
        return "weak"
    return "commodity_risk"


def moat_compound_index(d: MoatScoreDimensions) -> int:
    """Geometric-style compounding 0–100 (all dimensions must pull weight)."""
    vals = (
        d.governance_depth,
        d.proof_strength,
        d.product_reuse,
        d.saudi_arabic_differentiation,
        d.capital_assets_created,
        d.partner_academy_distribution,
        d.market_language_adoption,
    )
    product = 1.0
    for v in vals:
        product *= v / 100.0
    return round(100 * (product ** (1.0 / len(vals))))
