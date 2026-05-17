"""Sales OS — qualification, ICP/risk scoring, proposal skeleton (deterministic)."""

from __future__ import annotations

from auto_client_acquisition.sales_os.client_risk_score import ClientRiskSignals, client_risk_score
from auto_client_acquisition.sales_os.decision_tree import verdict_label_ar
from auto_client_acquisition.sales_os.founder_revenue_machine import (
    MACHINE_GUARDRAILS,
    PIPELINE_STATES,
    PRICING_TIERS_SAR,
    SALES_MACHINE_CONFIG,
    RiskScoreInput,
    compute_ops_risk_score,
    score_lead_fit,
    transitions,
    validate_transition,
)
from auto_client_acquisition.sales_os.icp_score import ICPDimensions, icp_score
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
    "MACHINE_GUARDRAILS",
    "PIPELINE_STATES",
    "PRICING_TIERS_SAR",
    "QualificationResult",
    "QualificationVerdict",
    "RiskScoreInput",
    "SALES_MACHINE_CONFIG",
    "build_proposal_skeleton",
    "client_risk_score",
    "compute_ops_risk_score",
    "icp_score",
    "qualify",
    "qualify_opportunity",
    "render_scope_bullets",
    "score_lead_fit",
    "transitions",
    "validate_transition",
    "verdict_label_ar",
]
