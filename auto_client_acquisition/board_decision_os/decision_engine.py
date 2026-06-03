"""Board-level strategic decisions — maps scorecard bands to `CompoundingDecision`."""

from __future__ import annotations

from auto_client_acquisition.intelligence_compounding_os import (
    CompoundingDecision,
    suggest_compounding_decision,
)

__all__ = (
    "CompoundingDecision",
    "client_scorecard_strategic_decision",
    "offer_scorecard_strategic_decision",
    "productization_scorecard_strategic_decision",
    "suggest_compounding_decision",
)


def offer_scorecard_strategic_decision(
    score: int,
    *,
    governance_safe: bool,
) -> CompoundingDecision:
    """Offer scorecard total (0–100) → primary board hint."""
    if not governance_safe:
        return CompoundingDecision.HOLD
    if score >= 85:
        return CompoundingDecision.SCALE
    if score >= 70:
        return CompoundingDecision.RAISE_PRICE
    if score >= 55:
        return CompoundingDecision.PILOT
    if score < 40:
        return CompoundingDecision.KILL
    return CompoundingDecision.HOLD


def client_scorecard_strategic_decision(score: int) -> CompoundingDecision:
    if score >= 85:
        return CompoundingDecision.CREATE_BUSINESS_UNIT
    if score >= 70:
        return CompoundingDecision.OFFER_RETAINER
    if score >= 55:
        return CompoundingDecision.PILOT
    return CompoundingDecision.HOLD


def productization_scorecard_strategic_decision(score: int) -> CompoundingDecision:
    if score >= 70:
        return CompoundingDecision.BUILD
    if score >= 55:
        return CompoundingDecision.PILOT
    return CompoundingDecision.HOLD
