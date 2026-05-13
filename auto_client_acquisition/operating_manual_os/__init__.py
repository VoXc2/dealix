"""Dealix Operating Manual OS — capstone surface that unifies prior layers.

Companion docs live under ``docs/operating_manual/``. This package
encodes the doctrine's first-class instruments:

* The Dealix Decision Rule — six questions with a scoring band.
* The Non-Negotiables — a frozen list of prohibited practices.
* The Proof-to-Retainer Gate — the rule that decides Continue / Expand
  / Pause and whether a retainer may be offered.
* The Board Memo — the monthly twelve-question leadership memo.
* The AI Run Log — canonical schema for every governed AI invocation.
* The Partner Covenant — the typed contract a partner must sign.

All modules are dependency-free and side-effect-free.
"""

from __future__ import annotations

from auto_client_acquisition.operating_manual_os.ai_run_log import (
    AIRunLedger,
    AIRunLogEntry,
)
from auto_client_acquisition.operating_manual_os.board_memo import (
    BOARD_MEMO_SECTIONS,
    BoardMemo,
    BoardMemoSection,
    render_board_memo,
)
from auto_client_acquisition.operating_manual_os.decision_rule import (
    DEALIX_DECISION_QUESTIONS,
    DealixDecisionAnswers,
    DealixDecisionEvaluation,
    DealixDecisionQuestion,
    DealixDecisionVerdict,
    evaluate_dealix_decision,
)
from auto_client_acquisition.operating_manual_os.non_negotiables import (
    DEALIX_NON_NEGOTIABLES,
    NonNegotiable,
    NonNegotiableCheck,
    check_action_against_non_negotiables,
)
from auto_client_acquisition.operating_manual_os.partner_covenant import (
    PARTNER_COVENANT_CLAUSES,
    CovenantClause,
    CovenantStatus,
    PartnerCovenant,
    PartnerCovenantEvaluation,
    evaluate_partner_covenant,
)
from auto_client_acquisition.operating_manual_os.proof_to_retainer import (
    RETAINER_GATE_THRESHOLDS,
    RetainerGateInputs,
    RetainerGateResult,
    RetainerMotion,
    evaluate_retainer_gate,
)

__all__ = [
    "AIRunLedger",
    "AIRunLogEntry",
    "BOARD_MEMO_SECTIONS",
    "BoardMemo",
    "BoardMemoSection",
    "render_board_memo",
    "DEALIX_DECISION_QUESTIONS",
    "DealixDecisionAnswers",
    "DealixDecisionEvaluation",
    "DealixDecisionQuestion",
    "DealixDecisionVerdict",
    "evaluate_dealix_decision",
    "DEALIX_NON_NEGOTIABLES",
    "NonNegotiable",
    "NonNegotiableCheck",
    "check_action_against_non_negotiables",
    "PARTNER_COVENANT_CLAUSES",
    "CovenantClause",
    "CovenantStatus",
    "PartnerCovenant",
    "PartnerCovenantEvaluation",
    "evaluate_partner_covenant",
    "RETAINER_GATE_THRESHOLDS",
    "RetainerGateInputs",
    "RetainerGateResult",
    "RetainerMotion",
    "evaluate_retainer_gate",
]
