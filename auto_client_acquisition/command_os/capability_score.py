"""Operating capability score — per-project delivery quality vs real capability (0–100)."""

from __future__ import annotations

from enum import StrEnum
from typing import NamedTuple


class OperatingCapabilityInputs(NamedTuple):
    """Subscores 0–100 from QA, ledgers, and review."""

    workflow_clarity: float
    data_readiness: float
    ai_usefulness: float
    governance_coverage: float
    qa_score: float
    proof_strength: float
    repeatability: float


class OperatingCapabilityBand(StrEnum):
    STRONG = "strong_capability"
    USABLE = "usable_capability"
    PARTIAL = "partial_capability"
    NOT_CAPABILITY = "not_a_capability_yet"


def compute_operating_capability_score(inputs: OperatingCapabilityInputs) -> float:
    w = (
        0.15 * inputs.workflow_clarity
        + 0.15 * inputs.data_readiness
        + 0.15 * inputs.ai_usefulness
        + 0.20 * inputs.governance_coverage
        + 0.10 * inputs.qa_score
        + 0.15 * inputs.proof_strength
        + 0.10 * inputs.repeatability
    )
    return max(0.0, min(100.0, float(w)))


def operating_capability_band(score: float) -> OperatingCapabilityBand:
    if score >= 85:
        return OperatingCapabilityBand.STRONG
    if score >= 70:
        return OperatingCapabilityBand.USABLE
    if score >= 50:
        return OperatingCapabilityBand.PARTIAL
    return OperatingCapabilityBand.NOT_CAPABILITY
