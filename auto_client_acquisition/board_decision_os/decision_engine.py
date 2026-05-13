"""Map scorecard bands to canonical decision verbs (advisory)."""

from __future__ import annotations

from auto_client_acquisition.board_decision_os.schemas import DecisionBand, ScorecardResult


def offer_decision_verb(result: ScorecardResult) -> str:
    if result.band == "top":
        return "SCALE"
    if result.band == "strong":
        return "IMPROVE_AND_SELL"
    if result.band == "mid":
        return "PILOT_ONLY"
    return "HOLD_OR_KILL"


def client_decision_verb(result: ScorecardResult) -> str:
    if result.band == "top":
        return "STRATEGIC_ACCOUNT"
    if result.band == "strong":
        return "OFFER_RETAINER"
    if result.band == "mid":
        return "ENABLEMENT_PROGRAM"
    return "AVOID_OR_DIAGNOSTIC"


def productization_decision_verb(result: ScorecardResult) -> str:
    if result.band == "top":
        return "BUILD_NOW"
    if result.band == "strong":
        return "BUILD_MVP"
    if result.band == "mid":
        return "TEMPLATE_OR_MANUAL"
    return "HOLD"


def band_from_total_generic(total: float) -> DecisionBand:
    """Expose band thresholds for tests without full scorecard input."""
    if total >= 85:
        return "top"
    if total >= 70:
        return "strong"
    if total >= 55:
        return "mid"
    return "low"
