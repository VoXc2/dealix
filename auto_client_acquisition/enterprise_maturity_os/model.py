"""Enterprise Maturity Operating System scoring model for Dealix.

This module answers one question:
"Are we building features, or building organizational capability?"
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean
from typing import Mapping


CAPABILITY_KEYS: tuple[str, ...] = (
    "workflow_redesign",
    "agent_orchestration",
    "action_governance",
    "memory_management",
    "execution_supervision",
    "business_impact_measurement",
    "safe_evolution",
    "digital_workforce_management",
    "executive_intelligence_generation",
    "organizational_intelligence_scaling",
)

DOMAIN_CAPABILITY_MAP: Mapping[str, tuple[str, ...]] = {
    "foundation_maturity": (
        "action_governance",
        "execution_supervision",
        "safe_evolution",
    ),
    "agentic_runtime_maturity": (
        "agent_orchestration",
        "digital_workforce_management",
        "action_governance",
        "execution_supervision",
    ),
    "workflow_orchestration_maturity": (
        "workflow_redesign",
        "execution_supervision",
        "action_governance",
    ),
    "organizational_memory_maturity": (
        "memory_management",
        "organizational_intelligence_scaling",
        "action_governance",
    ),
    "governance_maturity": (
        "action_governance",
        "execution_supervision",
        "safe_evolution",
    ),
    "evaluation_maturity": (
        "business_impact_measurement",
        "execution_supervision",
        "safe_evolution",
    ),
    "continuous_evolution_maturity": (
        "safe_evolution",
        "business_impact_measurement",
        "organizational_intelligence_scaling",
    ),
}


@dataclass(frozen=True)
class CapabilitySnapshot:
    """Scored capability inputs for enterprise maturity (0..100 each)."""

    workflow_redesign: float
    agent_orchestration: float
    action_governance: float
    memory_management: float
    execution_supervision: float
    business_impact_measurement: float
    safe_evolution: float
    digital_workforce_management: float
    executive_intelligence_generation: float
    organizational_intelligence_scaling: float

    def to_dict(self) -> dict[str, float]:
        data = {
            "workflow_redesign": self.workflow_redesign,
            "agent_orchestration": self.agent_orchestration,
            "action_governance": self.action_governance,
            "memory_management": self.memory_management,
            "execution_supervision": self.execution_supervision,
            "business_impact_measurement": self.business_impact_measurement,
            "safe_evolution": self.safe_evolution,
            "digital_workforce_management": self.digital_workforce_management,
            "executive_intelligence_generation": self.executive_intelligence_generation,
            "organizational_intelligence_scaling": self.organizational_intelligence_scaling,
        }
        validate_capability_scores(data)
        return data


@dataclass(frozen=True)
class DomainScore:
    domain: str
    capability_score: float
    artifact_coverage: float
    blended_score: float


@dataclass(frozen=True)
class EnterpriseMaturityReport:
    overall_score: float
    transformation_ready: bool
    domain_scores: tuple[DomainScore, ...]


def validate_capability_scores(scores: Mapping[str, float]) -> None:
    """Raise ValueError when capability keys are missing or out of range."""
    keys = set(scores.keys())
    expected = set(CAPABILITY_KEYS)
    missing = sorted(expected - keys)
    extra = sorted(keys - expected)
    if missing or extra:
        raise ValueError(f"Invalid capability keys. missing={missing} extra={extra}")
    for key in CAPABILITY_KEYS:
        value = float(scores[key])
        if value < 0 or value > 100:
            raise ValueError(f"{key} must be between 0 and 100")


def compute_domain_capability_score(domain: str, scores: Mapping[str, float]) -> float:
    if domain not in DOMAIN_CAPABILITY_MAP:
        raise ValueError(f"Unknown domain: {domain}")
    validate_capability_scores(scores)
    return fmean(float(scores[key]) for key in DOMAIN_CAPABILITY_MAP[domain])


def evaluate_enterprise_maturity(
    capability_scores: Mapping[str, float],
    artifact_coverage: Mapping[str, float],
    *,
    capability_weight: float = 0.7,
) -> EnterpriseMaturityReport:
    """Blend capability score with real implementation artifact coverage.

    Args:
        capability_scores: 10 capability scores (0..100 each).
        artifact_coverage: Per-domain implementation coverage (0..100).
        capability_weight: Weight for capability signal in blended domain score.
            Artifact signal weight is (1 - capability_weight).
    """
    if capability_weight <= 0 or capability_weight >= 1:
        raise ValueError("capability_weight must be in (0, 1)")

    validate_capability_scores(capability_scores)

    scores: list[DomainScore] = []
    for domain in DOMAIN_CAPABILITY_MAP:
        coverage = float(artifact_coverage.get(domain, 0.0))
        if coverage < 0 or coverage > 100:
            raise ValueError(f"artifact_coverage[{domain}] must be between 0 and 100")
        cap_score = compute_domain_capability_score(domain, capability_scores)
        blended = capability_weight * cap_score + (1.0 - capability_weight) * coverage
        scores.append(
            DomainScore(
                domain=domain,
                capability_score=round(cap_score, 2),
                artifact_coverage=round(coverage, 2),
                blended_score=round(blended, 2),
            ),
        )

    overall = round(fmean(item.blended_score for item in scores), 2)
    transformation_ready = all(item.blended_score >= 75 for item in scores)
    return EnterpriseMaturityReport(
        overall_score=overall,
        transformation_ready=transformation_ready,
        domain_scores=tuple(scores),
    )
