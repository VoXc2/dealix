"""Bad revenue filter — operating finance discipline."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BadRevenueSignals:
    open_scope: bool
    weak_margin: bool
    high_risk: bool
    governance_refused: bool
    wants_scraping: bool
    wants_guaranteed_sales: bool
    no_proof_path: bool
    no_retainer_path: bool
    no_productization_signal: bool


@dataclass(frozen=True, slots=True)
class GoodRevenueSignals:
    pain_clear: bool
    buyer_clear: bool
    data_source_clear: bool
    governance_acceptable: bool
    proof_path_clear: bool
    retainer_potential: bool
    repeatable_delivery: bool
    product_signal: bool


def is_bad_revenue(signals: BadRevenueSignals) -> tuple[bool, tuple[str, ...]]:
    reasons: list[str] = []
    if signals.open_scope:
        reasons.append("open_scope")
    if signals.weak_margin:
        reasons.append("weak_margin")
    if signals.high_risk:
        reasons.append("high_risk")
    if signals.governance_refused:
        reasons.append("governance_refused")
    if signals.wants_scraping:
        reasons.append("wants_scraping")
    if signals.wants_guaranteed_sales:
        reasons.append("wants_guaranteed_sales")
    if signals.no_proof_path:
        reasons.append("no_proof_path")
    if signals.no_retainer_path:
        reasons.append("no_retainer_path")
    if signals.no_productization_signal:
        reasons.append("no_productization_signal")
    return bool(reasons), tuple(reasons)


def good_revenue_green(signals: GoodRevenueSignals) -> tuple[bool, tuple[str, ...]]:
    """All gates true → operating 'good revenue' green light (orthogonal to `is_bad_revenue`)."""
    missing: list[str] = []
    if not signals.pain_clear:
        missing.append("pain_unclear")
    if not signals.buyer_clear:
        missing.append("buyer_unclear")
    if not signals.data_source_clear:
        missing.append("data_source_unclear")
    if not signals.governance_acceptable:
        missing.append("governance_not_acceptable")
    if not signals.proof_path_clear:
        missing.append("proof_path_unclear")
    if not signals.retainer_potential:
        missing.append("no_retainer_potential")
    if not signals.repeatable_delivery:
        missing.append("delivery_not_repeatable")
    if not signals.product_signal:
        missing.append("no_product_signal")
    return not missing, tuple(missing)
