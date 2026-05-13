"""Board Decision OS — strategic intelligence & board-facing read models."""

from auto_client_acquisition.board_decision_os.agent_decision_gate import evaluate_agent_gate
from auto_client_acquisition.board_decision_os.board_memo_generator import (
    board_memo_template_markdown,
    build_board_memo,
)
from auto_client_acquisition.board_decision_os.board_scorecards import (
    score_client,
    score_offer,
    score_productization,
)
from auto_client_acquisition.board_decision_os.capital_allocation_board import (
    classify_initiative,
    default_capital_allocation,
)
from auto_client_acquisition.board_decision_os.ceo_command_center import build_top_decisions
from auto_client_acquisition.board_decision_os.decision_engine import (
    band_from_total_generic,
    client_decision_verb,
    offer_decision_verb,
    productization_decision_verb,
)
from auto_client_acquisition.board_decision_os.risk_decisions import list_risk_register
from auto_client_acquisition.board_decision_os.strategic_bets import (
    StrategicBetsError,
    validate_monthly_bets,
)

__all__ = [
    "StrategicBetsError",
    "band_from_total_generic",
    "board_memo_template_markdown",
    "build_board_memo",
    "build_top_decisions",
    "classify_initiative",
    "client_decision_verb",
    "default_capital_allocation",
    "evaluate_agent_gate",
    "list_risk_register",
    "offer_decision_verb",
    "productization_decision_verb",
    "score_client",
    "score_offer",
    "score_productization",
    "validate_monthly_bets",
]
