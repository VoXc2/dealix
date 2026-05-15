"""Platform maturity engine — turn gate + verification evidence into a stage.

Stage promotion is gated on *both* aggregate gate score and verification
coverage. A platform with high gate scores but unproven workflows/governance
cannot be promoted past Enterprise AI Platform — feature count is not maturity.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any

import yaml

from auto_client_acquisition.enterprise_maturity_os.readiness_gates import (
    GATE_IDS,
    readiness_band,
    score_gate,
)
from auto_client_acquisition.enterprise_maturity_os.stages import (
    MIN_LEVEL,
    MaturityStage,
    next_stage,
    stage_for_level,
)
from auto_client_acquisition.enterprise_maturity_os.verification_systems import (
    VERIFICATION_SYSTEM_IDS,
    verification_coverage,
)

# Each stage above level 1 requires a minimum mean gate score AND minimum mean
# verification coverage. Level 1 (AI Tool) is the floor — always reachable.
_STAGE_REQUIREMENTS: dict[int, dict[str, int]] = {
    2: {"min_gate_score": 60, "min_verification": 40},
    3: {"min_gate_score": 75, "min_verification": 60},
    4: {"min_gate_score": 85, "min_verification": 80},
    5: {"min_gate_score": 95, "min_verification": 95},
}


@dataclass(frozen=True, slots=True)
class MaturityAssessment:
    overall_gate_score: int
    overall_verification_coverage: int
    current_stage: MaturityStage
    current_band: str
    next_stage: MaturityStage | None
    gate_scores: dict[str, int] = field(default_factory=dict)
    verification_coverages: dict[str, int] = field(default_factory=dict)
    blockers: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "overall_gate_score": self.overall_gate_score,
            "overall_verification_coverage": self.overall_verification_coverage,
            "current_stage": {
                "stage_id": self.current_stage.stage_id,
                "level": self.current_stage.level,
                "name_en": self.current_stage.name_en,
                "name_ar": self.current_stage.name_ar,
            },
            "current_band": self.current_band,
            "next_stage": (
                {
                    "stage_id": self.next_stage.stage_id,
                    "level": self.next_stage.level,
                    "name_en": self.next_stage.name_en,
                    "name_ar": self.next_stage.name_ar,
                }
                if self.next_stage is not None
                else None
            ),
            "gate_scores": dict(self.gate_scores),
            "verification_coverages": dict(self.verification_coverages),
            "blockers": list(self.blockers),
        }


def _mean(values: list[int]) -> int:
    return round(sum(values) / len(values)) if values else 0


def _highest_reached_level(gate_score: int, verification: int) -> int:
    level = MIN_LEVEL
    for candidate in sorted(_STAGE_REQUIREMENTS):
        req = _STAGE_REQUIREMENTS[candidate]
        if gate_score >= req["min_gate_score"] and verification >= req["min_verification"]:
            level = candidate
        else:
            break
    return level


def _blockers_for_next(
    next_level: int,
    gate_scores: dict[str, int],
    verification_coverages: dict[str, int],
) -> tuple[str, ...]:
    req = _STAGE_REQUIREMENTS.get(next_level)
    if req is None:
        return ()
    out: list[str] = []
    for gate_id, score in sorted(gate_scores.items()):
        if score < req["min_gate_score"]:
            out.append(f"gate:{gate_id} at {score} (needs {req['min_gate_score']})")
    for system_id, cov in sorted(verification_coverages.items()):
        if cov < req["min_verification"]:
            out.append(f"verification:{system_id} at {cov} (needs {req['min_verification']})")
    return tuple(out)


def assess_platform_maturity(
    *,
    gate_evidence: dict[str, dict[str, bool]] | None = None,
    verification_evidence: dict[str, dict[str, bool]] | None = None,
) -> MaturityAssessment:
    """Assess Dealix's platform maturity from gate + verification evidence."""
    gate_evidence = gate_evidence or {}
    verification_evidence = verification_evidence or {}

    gate_scores: dict[str, int] = {
        gate_id: score_gate(gate_id, gate_evidence.get(gate_id)).score for gate_id in GATE_IDS
    }
    verification_coverages: dict[str, int] = {
        system_id: verification_coverage(system_id, verification_evidence.get(system_id))
        for system_id in VERIFICATION_SYSTEM_IDS
    }

    overall_gate = _mean(list(gate_scores.values()))
    overall_verification = _mean(list(verification_coverages.values()))

    current_level = _highest_reached_level(overall_gate, overall_verification)
    current_stage = stage_for_level(current_level)
    nxt = next_stage(current_level)
    blockers = _blockers_for_next(current_level + 1, gate_scores, verification_coverages)

    return MaturityAssessment(
        overall_gate_score=overall_gate,
        overall_verification_coverage=overall_verification,
        current_stage=current_stage,
        current_band=readiness_band(overall_gate),
        next_stage=nxt,
        gate_scores=gate_scores,
        verification_coverages=verification_coverages,
        blockers=blockers,
    )


def _baseline_path() -> str:
    return os.path.join(os.path.dirname(__file__), "maturity_baseline.yaml")


@lru_cache(maxsize=1)
def _load_baseline() -> dict[str, Any]:
    with open(_baseline_path(), encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def assess_current_platform() -> MaturityAssessment:
    """Assess Dealix today against the packaged honest baseline."""
    blob = _load_baseline()
    return assess_platform_maturity(
        gate_evidence=blob.get("gate_evidence") or {},
        verification_evidence=blob.get("verification_evidence") or {},
    )


__all__ = [
    "MaturityAssessment",
    "assess_current_platform",
    "assess_platform_maturity",
]
