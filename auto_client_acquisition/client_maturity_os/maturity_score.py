"""Client Maturity Score — 7 dimensions, total 100."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


MATURITY_WEIGHTS: dict[str, int] = {
    "leadership_alignment": 15,
    "data_readiness": 15,
    "workflow_ownership": 15,
    "governance_coverage": 20,
    "proof_discipline": 15,
    "adoption": 10,
    "operating_cadence": 10,
}


class MaturityTier(str, Enum):
    ENTERPRISE_EXPANSION = "enterprise_expansion"        # 85+
    RETAINER_WORKSPACE = "retainer_workspace_ready"      # 70..84
    SPRINT_ENABLEMENT = "sprint_plus_enablement"         # 55..69
    DIAGNOSTIC_READINESS = "diagnostic_plus_readiness"   # 35..54
    DO_NOT_DEPLOY = "do_not_deploy"                      # <35


@dataclass(frozen=True)
class MaturityComponents:
    leadership_alignment: int
    data_readiness: int
    workflow_ownership: int
    governance_coverage: int
    proof_discipline: int
    adoption: int
    operating_cadence: int

    def __post_init__(self) -> None:
        for name in MATURITY_WEIGHTS:
            v = getattr(self, name)
            if not 0 <= v <= 100:
                raise ValueError(f"{name}_out_of_range_0_100")


def compute_maturity_score(c: MaturityComponents) -> int:
    weighted = 0.0
    for name, w in MATURITY_WEIGHTS.items():
        weighted += getattr(c, name) * (w / 100.0)
    return round(weighted)


def classify_maturity_tier(score: int) -> MaturityTier:
    if score >= 85:
        return MaturityTier.ENTERPRISE_EXPANSION
    if score >= 70:
        return MaturityTier.RETAINER_WORKSPACE
    if score >= 55:
        return MaturityTier.SPRINT_ENABLEMENT
    if score >= 35:
        return MaturityTier.DIAGNOSTIC_READINESS
    return MaturityTier.DO_NOT_DEPLOY
