"""Governance risk index — aggregate risk 0–100 from normalized factor scores."""

from __future__ import annotations

from enum import StrEnum
from typing import NamedTuple


class GovernanceRiskInputs(NamedTuple):
    """Each field 0–100 where higher means more risk (pre-normalized by caller)."""

    pii_sensitivity: float
    external_action_potential: float
    source_uncertainty: float
    claim_risk: float
    channel_risk: float
    agent_autonomy: float
    client_industry_sensitivity: float


class GovernanceRiskBand(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


def compute_governance_risk_index(inputs: GovernanceRiskInputs) -> float:
    vals = tuple(inputs)
    return max(0.0, min(100.0, float(sum(vals) / len(vals))))


def governance_risk_band(score: float) -> GovernanceRiskBand:
    if score < 25:
        return GovernanceRiskBand.LOW
    if score < 50:
        return GovernanceRiskBand.MEDIUM
    if score < 75:
        return GovernanceRiskBand.HIGH
    return GovernanceRiskBand.CRITICAL
