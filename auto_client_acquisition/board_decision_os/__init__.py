"""Dealix Board Decision OS — scorecards + CEO Command Center."""

from __future__ import annotations

from auto_client_acquisition.board_decision_os.board_scorecards import (
    ClientScorecardComponents,
    OFFER_SCORECARD_WEIGHTS,
    OfferScorecardComponents,
    PRODUCTIZATION_SCORECARD_WEIGHTS,
    ProductizationScorecardComponents,
    ScorecardTier,
    classify_scorecard,
    compute_client_scorecard,
    compute_offer_scorecard,
    compute_productization_scorecard,
)
from auto_client_acquisition.board_decision_os.ceo_command_center import (
    CEOCommandCenterTopFive,
    PriorityDecision,
)
from auto_client_acquisition.board_decision_os.strategic_bets import (
    STRATEGIC_BET_KINDS,
    StrategicBet,
    StrategicBetKind,
    validate_bet_count,
)

__all__ = [
    "ClientScorecardComponents",
    "OFFER_SCORECARD_WEIGHTS",
    "OfferScorecardComponents",
    "PRODUCTIZATION_SCORECARD_WEIGHTS",
    "ProductizationScorecardComponents",
    "ScorecardTier",
    "classify_scorecard",
    "compute_client_scorecard",
    "compute_offer_scorecard",
    "compute_productization_scorecard",
    "CEOCommandCenterTopFive",
    "PriorityDecision",
    "STRATEGIC_BET_KINDS",
    "StrategicBet",
    "StrategicBetKind",
    "validate_bet_count",
]
