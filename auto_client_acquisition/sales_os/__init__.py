"""Sales OS — qualification, ICP/risk scoring, proposal skeleton (deterministic)."""

from __future__ import annotations

from auto_client_acquisition.sales_os.client_risk_score import ClientRiskSignals, client_risk_score
from auto_client_acquisition.sales_os.decision_tree import verdict_label_ar
from auto_client_acquisition.sales_os.icp_score import ICPDimensions, icp_score
from auto_client_acquisition.sales_os.market_motion import (
    BoardDecision,
    EvidenceLevel,
    MarketEvent,
    MarketMotionEvent,
    MarketMotionScoreboard,
    OutreachDraft,
    append_event,
    board_decision,
    build_first5_drafts_from_csv,
    build_scoreboard,
    evidence_level_for_event,
    read_events,
    render_first5_markdown,
    validate_new_event,
)
from auto_client_acquisition.sales_os.proposal_generator import build_proposal_skeleton
from auto_client_acquisition.sales_os.proposal_sections import PROPOSAL_SECTION_KEYS
from auto_client_acquisition.sales_os.qualification import (
    Decision,
    QualificationResult,
    QualificationVerdict,
    qualify,
    qualify_opportunity,
)
from auto_client_acquisition.sales_os.scope_renderer import render_scope_bullets

__all__ = [
    "PROPOSAL_SECTION_KEYS",
    "ClientRiskSignals",
    "BoardDecision",
    "Decision",
    "EvidenceLevel",
    "ICPDimensions",
    "MarketEvent",
    "MarketMotionEvent",
    "MarketMotionScoreboard",
    "OutreachDraft",
    "QualificationResult",
    "QualificationVerdict",
    "append_event",
    "board_decision",
    "build_proposal_skeleton",
    "build_first5_drafts_from_csv",
    "build_scoreboard",
    "client_risk_score",
    "evidence_level_for_event",
    "icp_score",
    "qualify",
    "qualify_opportunity",
    "read_events",
    "render_first5_markdown",
    "render_scope_bullets",
    "validate_new_event",
    "verdict_label_ar",
]
