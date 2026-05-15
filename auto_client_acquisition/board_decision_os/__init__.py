"""Strategic Intelligence & Board Decision — signals → decisions → proof (gates)."""

from __future__ import annotations

from auto_client_acquisition.board_decision_os.agent_decision_gate import (
    AGENT_DECISION_GATE_FIELDS,
    AgentDecisionGate,
    agent_decision_gate_passes,
)
from auto_client_acquisition.board_decision_os.board_memo_generator import (
    BOARD_MEMO_SECTIONS,
    board_memo_sections_complete,
)
from auto_client_acquisition.board_decision_os.board_scorecards import (
    ClientScorecardDimensions,
    OfferScorecardDimensions,
    ProductizationScorecardDimensions,
    client_scorecard_band,
    client_scorecard_score,
    offer_scorecard_band,
    offer_scorecard_score,
    productization_scorecard_band,
    productization_scorecard_score,
)
from auto_client_acquisition.board_decision_os.board_signal_inputs import (
    BOARD_DECISION_INPUT_SIGNALS,
    board_input_signal_valid,
)
from auto_client_acquisition.board_decision_os.capital_allocation_board import (
    CAPITAL_BOARD_BUCKETS,
    capital_board_bucket,
)
from auto_client_acquisition.board_decision_os.ceo_command_center import (
    CEO_COMMAND_CENTER_SURFACES,
    ceo_command_center_coverage_score,
)
from auto_client_acquisition.board_decision_os.decision_engine import (
    CompoundingDecision,
    client_scorecard_strategic_decision,
    offer_scorecard_strategic_decision,
    productization_scorecard_strategic_decision,
    suggest_compounding_decision,
)
from auto_client_acquisition.board_decision_os.risk_decisions import (
    RISK_REGISTER_CODES,
    risk_register_code_valid,
    risk_to_mitigation_decision,
)
from auto_client_acquisition.board_decision_os.strategic_bets import (
    STRATEGIC_BET_TYPES,
    strategic_bet_type_valid,
)

__all__ = (
    "AGENT_DECISION_GATE_FIELDS",
    "BOARD_DECISION_INPUT_SIGNALS",
    "BOARD_MEMO_SECTIONS",
    "CAPITAL_BOARD_BUCKETS",
    "CEO_COMMAND_CENTER_SURFACES",
    "RISK_REGISTER_CODES",
    "STRATEGIC_BET_TYPES",
    "AgentDecisionGate",
    "ClientScorecardDimensions",
    "CompoundingDecision",
    "OfferScorecardDimensions",
    "ProductizationScorecardDimensions",
    "agent_decision_gate_passes",
    "board_input_signal_valid",
    "board_memo_sections_complete",
    "capital_board_bucket",
    "ceo_command_center_coverage_score",
    "client_scorecard_band",
    "client_scorecard_score",
    "client_scorecard_strategic_decision",
    "offer_scorecard_band",
    "offer_scorecard_score",
    "offer_scorecard_strategic_decision",
    "productization_scorecard_band",
    "productization_scorecard_score",
    "productization_scorecard_strategic_decision",
    "risk_register_code_valid",
    "risk_to_mitigation_decision",
    "strategic_bet_type_valid",
    "suggest_compounding_decision",
)
