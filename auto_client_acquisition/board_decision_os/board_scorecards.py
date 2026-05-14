"""Board scorecards — weighted 0–100 signals for offers, clients, productization."""

from __future__ import annotations

from dataclasses import dataclass

# Win rate, gross margin, proof strength, retainer conversion, repeatability,
# governance safety, productization signal
_OFFER_WEIGHTS: tuple[int, ...] = (15, 15, 20, 20, 15, 10, 5)

# Clear pain, executive sponsor, data readiness, governance alignment,
# adoption, proof, expansion potential
_CLIENT_WEIGHTS: tuple[int, ...] = (15, 15, 15, 15, 15, 15, 10)

# Repeated pain, delivery hours saved, revenue linkage, risk reduction,
# client pull, build simplicity
_PRODUCTIZATION_WEIGHTS: tuple[int, ...] = (20, 20, 20, 15, 15, 10)


def _clamp_pct(value: int) -> int:
    if value < 0:
        return 0
    if value > 100:
        return 100
    return value


def _weighted_score(values: tuple[int, ...], weights: tuple[int, ...]) -> int:
    total = sum(_clamp_pct(v) * w for v, w in zip(values, weights, strict=True))
    return min(100, total // 100)


@dataclass(frozen=True, slots=True)
class OfferScorecardDimensions:
    win_rate: int
    gross_margin: int
    proof_strength: int
    retainer_conversion: int
    repeatability: int
    governance_safety: int
    productization_signal: int


@dataclass(frozen=True, slots=True)
class ClientScorecardDimensions:
    clear_pain: int
    executive_sponsor: int
    data_readiness: int
    governance_alignment: int
    adoption_score: int
    proof_score: int
    expansion_potential: int


@dataclass(frozen=True, slots=True)
class ProductizationScorecardDimensions:
    repeated_pain: int
    delivery_hours_saved: int
    revenue_linkage: int
    risk_reduction: int
    client_pull: int
    build_simplicity: int


def offer_scorecard_score(dimensions: OfferScorecardDimensions) -> int:
    d = dimensions
    return _weighted_score(
        (
            d.win_rate,
            d.gross_margin,
            d.proof_strength,
            d.retainer_conversion,
            d.repeatability,
            d.governance_safety,
            d.productization_signal,
        ),
        _OFFER_WEIGHTS,
    )


def client_scorecard_score(dimensions: ClientScorecardDimensions) -> int:
    d = dimensions
    return _weighted_score(
        (
            d.clear_pain,
            d.executive_sponsor,
            d.data_readiness,
            d.governance_alignment,
            d.adoption_score,
            d.proof_score,
            d.expansion_potential,
        ),
        _CLIENT_WEIGHTS,
    )


def productization_scorecard_score(dimensions: ProductizationScorecardDimensions) -> int:
    d = dimensions
    return _weighted_score(
        (
            d.repeated_pain,
            d.delivery_hours_saved,
            d.revenue_linkage,
            d.risk_reduction,
            d.client_pull,
            d.build_simplicity,
        ),
        _PRODUCTIZATION_WEIGHTS,
    )


def offer_scorecard_band(score: int) -> str:
    if score >= 85:
        return "scale"
    if score >= 70:
        return "improve_and_sell"
    if score >= 55:
        return "pilot_only"
    return "hold_kill"


def client_scorecard_band(score: int) -> str:
    if score >= 85:
        return "strategic_account"
    if score >= 70:
        return "retainer_ready"
    if score >= 55:
        return "enablement_needed"
    return "avoid_or_diagnostic"


def productization_scorecard_band(score: int) -> str:
    if score >= 85:
        return "build_now"
    if score >= 70:
        return "mvp"
    if score >= 55:
        return "template_manual"
    return "hold"
