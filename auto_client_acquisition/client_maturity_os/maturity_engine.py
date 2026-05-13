"""Client Maturity Engine — 8 levels + Maturity-to-Offer matrix."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class MaturityLevel(IntEnum):
    AI_CHAOS = 0
    AI_AWARENESS = 1
    STRUCTURED_USE_CASE = 2
    AI_ASSISTED_WORKFLOW = 3
    GOVERNED_AI_WORKFLOW = 4
    OPERATING_AI_CAPABILITY = 5
    MULTI_WORKFLOW_AI_OS = 6
    ENTERPRISE_AI_CONTROL_PLANE = 7


MATURITY_OFFER_MATRIX: dict[MaturityLevel, tuple[str, str]] = {
    MaturityLevel.AI_CHAOS: ("Governance Diagnostic", "agents"),
    MaturityLevel.AI_AWARENESS: ("Capability Diagnostic", "platform"),
    MaturityLevel.STRUCTURED_USE_CASE: ("Productized Sprint", "enterprise_os"),
    MaturityLevel.AI_ASSISTED_WORKFLOW: ("Governance Runtime Setup + Proof", "external_automation"),
    MaturityLevel.GOVERNED_AI_WORKFLOW: ("Monthly Retainer", "autonomous_agents"),
    MaturityLevel.OPERATING_AI_CAPABILITY: ("Client Workspace", "complex_enterprise_features"),
    MaturityLevel.MULTI_WORKFLOW_AI_OS: ("Enterprise AI Ops Program", "white_label"),
    MaturityLevel.ENTERPRISE_AI_CONTROL_PLANE: ("AI Control Plane", "no_audit_deployment"),
}


@dataclass(frozen=True)
class MaturityEngineInputs:
    leadership_alignment: int       # 0..100
    data_readiness: int             # 0..100
    workflow_clarity: int           # 0..100
    governance_maturity: int        # 0..100
    proof_score: int                # 0..100
    adoption_score: int             # 0..100
    monthly_cadence_active: bool
    audit_need: bool


@dataclass(frozen=True)
class MaturityEngineResult:
    level: MaturityLevel
    recommended_offer: str
    blocked: str
    reason: str


def classify_maturity_level(i: MaturityEngineInputs) -> MaturityEngineResult:
    avg_core = (
        i.leadership_alignment
        + i.data_readiness
        + i.workflow_clarity
        + i.governance_maturity
    ) / 4

    if avg_core < 25:
        level = MaturityLevel.AI_CHAOS
        reason = "no_governance_no_data_clarity"
    elif avg_core < 45:
        level = MaturityLevel.AI_AWARENESS
        reason = "no_clear_use_case"
    elif avg_core < 60 and i.workflow_clarity >= 50:
        level = MaturityLevel.STRUCTURED_USE_CASE
        reason = "owner_and_source_present_no_ai_yet"
    elif i.governance_maturity < 70 and i.proof_score >= 60:
        level = MaturityLevel.AI_ASSISTED_WORKFLOW
        reason = "ai_assists_but_governance_incomplete"
    elif i.governance_maturity >= 70 and not i.monthly_cadence_active:
        level = MaturityLevel.GOVERNED_AI_WORKFLOW
        reason = "governance_complete_no_cadence_yet"
    elif i.monthly_cadence_active and i.proof_score >= 75 and i.adoption_score >= 60:
        level = MaturityLevel.OPERATING_AI_CAPABILITY
        reason = "monthly_cadence_with_visible_value"
    elif i.proof_score >= 80 and i.adoption_score >= 75:
        level = MaturityLevel.MULTI_WORKFLOW_AI_OS
        reason = "multiple_governed_workflows"
    elif i.audit_need and i.governance_maturity >= 85:
        level = MaturityLevel.ENTERPRISE_AI_CONTROL_PLANE
        reason = "audit_demand_with_full_governance"
    else:
        level = MaturityLevel.AI_ASSISTED_WORKFLOW
        reason = "default_mid_maturity"

    offer, blocked = MATURITY_OFFER_MATRIX[level]
    return MaturityEngineResult(
        level=level,
        recommended_offer=offer,
        blocked=blocked,
        reason=reason,
    )
