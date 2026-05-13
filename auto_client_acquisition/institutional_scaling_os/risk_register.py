"""Institutional Risk Register — 12 canonical doctrine risks."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DoctrineRisk(str, Enum):
    R1_AGENCY_TRAP = "agency_trap"
    R2_PREMATURE_SAAS = "premature_saas"
    R3_GOVERNANCE_INCIDENT = "governance_incident"
    R4_WEAK_PROOF = "weak_proof"
    R5_FOUNDER_BOTTLENECK = "founder_bottleneck"
    R6_PARTNER_BRAND_DAMAGE = "partner_brand_damage"
    R7_OVER_CUSTOMIZATION = "over_customization"
    R8_LOW_MARGIN_PROJECTS = "low_margin_projects"
    R9_MODEL_PROVIDER_DEPENDENCY = "model_provider_dependency"
    R10_SAUDI_COMPLIANCE_GAP = "saudi_compliance_gap"
    R11_AGENT_OVER_PERMISSION = "agent_over_permission"
    R12_PROOF_CLAIMS_WITHOUT_EVIDENCE = "proof_claims_without_evidence"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class RiskEntry:
    risk: DoctrineRisk
    owner: str
    likelihood: RiskLevel
    impact: RiskLevel
    early_warning_signal: str
    control: str
    response_plan: str


DOCTRINE_RISKS: tuple[DoctrineRisk, ...] = tuple(DoctrineRisk)
