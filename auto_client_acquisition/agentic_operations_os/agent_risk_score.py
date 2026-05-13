"""Agent Risk Score — 7 dimensions, total 100; 4 bands."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


AGENT_RISK_WEIGHTS: dict[str, int] = {
    "data_sensitivity": 20,
    "tool_risk": 20,
    "autonomy_level": 20,
    "external_action_exposure": 15,
    "human_oversight_inverse": 10,
    "audit_coverage_inverse": 10,
    "business_criticality": 5,
}


class AgentRiskBand(str, Enum):
    LOW = "low"                    # 0..30
    MEDIUM = "medium"              # 31..60
    HIGH = "high"                  # 61..80
    RESTRICTED = "restricted"      # 81..100


@dataclass(frozen=True)
class AgentRiskComponents:
    """Each component is 0..100; higher = more risk.

    For human_oversight and audit_coverage, the *inverse* is used (less oversight = more risk).
    """

    data_sensitivity: int
    tool_risk: int
    autonomy_level: int
    external_action_exposure: int
    human_oversight_inverse: int
    audit_coverage_inverse: int
    business_criticality: int

    def __post_init__(self) -> None:
        for name in AGENT_RISK_WEIGHTS:
            v = getattr(self, name)
            if not 0 <= v <= 100:
                raise ValueError(f"{name}_out_of_range_0_100")


def compute_agent_risk_score(c: AgentRiskComponents) -> int:
    weighted = 0.0
    for name, w in AGENT_RISK_WEIGHTS.items():
        weighted += getattr(c, name) * (w / 100.0)
    return round(weighted)


def classify_agent_risk(score: int) -> AgentRiskBand:
    if score <= 30:
        return AgentRiskBand.LOW
    if score <= 60:
        return AgentRiskBand.MEDIUM
    if score <= 80:
        return AgentRiskBand.HIGH
    return AgentRiskBand.RESTRICTED
