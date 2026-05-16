"""Sales OS — qualification, ICP/risk scoring, proposal skeleton (deterministic)."""

from __future__ import annotations

from auto_client_acquisition.sales_os.client_risk_score import ClientRiskSignals, client_risk_score
from auto_client_acquisition.sales_os.decision_tree import verdict_label_ar
from auto_client_acquisition.sales_os.icp_score import ICPDimensions, icp_score
from auto_client_acquisition.sales_os.market_motion import (
    BoardDecisionAction,
    MarketEvidenceLevel,
    MarketMotionMetrics,
    ResponseEvent,
    ResponsePolicy,
    build_market_motion_metrics,
    can_claim_revenue,
    can_claim_traction,
    classify_response_event,
    highest_evidence_level,
    recommend_board_action,
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
    "Decision",
    "ICPDimensions",
    "MarketEvidenceLevel",
    "MarketMotionMetrics",
    "QualificationResult",
    "QualificationVerdict",
    "ResponseEvent",
    "ResponsePolicy",
    "BoardDecisionAction",
    "build_proposal_skeleton",
    "build_market_motion_metrics",
    "can_claim_revenue",
    "can_claim_traction",
    "client_risk_score",
    "classify_response_event",
    "highest_evidence_level",
    "icp_score",
    "qualify",
    "qualify_opportunity",
    "recommend_board_action",
    "render_scope_bullets",
    "verdict_label_ar",
]
