"""Institutional risk register — minimum viable entry shape."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class InstitutionalRisk(StrEnum):
    """Reference risk IDs (R1–R10) for scaling doctrine."""

    R1_AGENCY_TRAP = "R1_agency_trap"
    R2_PREMATURE_SAAS = "R2_premature_saas"
    R3_GOVERNANCE_INCIDENT = "R3_governance_incident"
    R4_WEAK_PROOF = "R4_weak_proof"
    R5_FOUNDER_BOTTLENECK = "R5_founder_bottleneck"
    R6_PARTNER_BRAND_DAMAGE = "R6_partner_brand_damage"
    R7_OVER_CUSTOMIZATION = "R7_over_customization"
    R8_LOW_MARGIN_PROJECTS = "R8_low_margin_projects"
    R9_MODEL_PROVIDER_DEPENDENCY = "R9_model_provider_dependency"
    R10_SAUDI_COMPLIANCE_TRUST_GAP = "R10_saudi_compliance_trust_gap"


@dataclass(frozen=True, slots=True)
class RiskRegisterEntry:
    risk_id: str
    owner: str
    likelihood: str
    impact: str
    control: str
    early_warning_signal: str
    response_plan: str


def risk_register_entry_valid(entry: RiskRegisterEntry) -> bool:
    return all(
        (
            entry.risk_id.strip(),
            entry.owner.strip(),
            entry.likelihood.strip(),
            entry.impact.strip(),
            entry.control.strip(),
            entry.early_warning_signal.strip(),
            entry.response_plan.strip(),
        ),
    )
