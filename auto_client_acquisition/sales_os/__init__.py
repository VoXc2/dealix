"""Sales OS — qualification, ICP/risk scoring, proposal skeleton (deterministic)."""

from __future__ import annotations

from auto_client_acquisition.sales_os.client_risk_score import ClientRiskSignals, client_risk_score
from auto_client_acquisition.sales_os.decision_tree import verdict_label_ar
from auto_client_acquisition.sales_os.funnel import (
    STAGE_PROPERTIES,
    FunnelStage,
    StageSpec,
    validate_transition,
)
from auto_client_acquisition.sales_os.icp_score import ICPDimensions, icp_score
from auto_client_acquisition.sales_os.partner_engine import (
    CommissionContext,
    PartnerType,
    classify_partner,
    commission_eligible,
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
    "STAGE_PROPERTIES",
    "ClientRiskSignals",
    "CommissionContext",
    "Decision",
    "FunnelStage",
    "ICPDimensions",
    "PartnerType",
    "QualificationResult",
    "QualificationVerdict",
    "StageSpec",
    "build_proposal_skeleton",
    "classify_partner",
    "client_risk_score",
    "commission_eligible",
    "icp_score",
    "qualify",
    "qualify_opportunity",
    "render_scope_bullets",
    "validate_transition",
    "verdict_label_ar",
]
