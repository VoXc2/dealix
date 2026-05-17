"""Maturity scorecard engine for the Execution Assurance System.

Replaces the binary "does the module import?" proxy with an honest 0-5
maturity model that is attested in the registry and cross-checked against
each machine's Definition-of-Done completion. Pure functions, never raise.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from auto_client_acquisition.execution_assurance_os.definition_of_done import (
    evaluate_dod,
)
from auto_client_acquisition.execution_assurance_os.registry import (
    MachineRegistry,
    MachineSpec,
)

MATURITY_LEVELS: dict[int, str] = {
    0: "Absent",
    1: "Manual",
    2: "Partial",
    3: "Automated",
    4: "Governed",
    5: "Self-improving",
}

# How far the declared maturity may drift from the band implied by
# Definition-of-Done completion before it is flagged inconsistent.
_CONSISTENCY_TOLERANCE = 2

ReadinessLabel = Literal[
    "Full Ops Ready",
    "Customer Ready with Manual Ops",
    "Diagnostic Only",
    "Internal Only",
]


def readiness_label(percentage: float) -> ReadinessLabel:
    """Map a 0-100 portfolio percentage to a readiness label."""
    if percentage >= 90:
        return "Full Ops Ready"
    if percentage >= 75:
        return "Customer Ready with Manual Ops"
    if percentage >= 60:
        return "Diagnostic Only"
    return "Internal Only"


@dataclass(frozen=True, slots=True)
class MachineScore:
    """Honest maturity score for one machine."""

    machine_id: str
    name: str
    declared_score: int
    declared_level: str
    target_score: int
    dod_pct: float
    implied_band: int
    consistency: Literal["consistent", "inconsistent"]
    gap_to_target: int
    owner: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "machine_id": self.machine_id,
            "name": self.name,
            "declared_score": self.declared_score,
            "declared_level": self.declared_level,
            "target_score": self.target_score,
            "dod_pct": self.dod_pct,
            "implied_band": self.implied_band,
            "consistency": self.consistency,
            "gap_to_target": self.gap_to_target,
            "owner": self.owner,
        }


@dataclass(frozen=True, slots=True)
class PortfolioScore:
    """Aggregate maturity across every machine."""

    machines: tuple[MachineScore, ...]
    mean_maturity: float
    target_mean: float
    percentage: float
    readiness_label: ReadinessLabel
    machines_at_target: int
    machines_total: int
    inconsistent_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "mean_maturity": self.mean_maturity,
            "target_mean": self.target_mean,
            "percentage": self.percentage,
            "readiness_label": self.readiness_label,
            "machines_at_target": self.machines_at_target,
            "machines_total": self.machines_total,
            "inconsistent_count": self.inconsistent_count,
            "machines": [m.to_dict() for m in self.machines],
            "safety_summary": "maturity_attested_in_registry_no_fake_green",
        }


def score_machine(spec: MachineSpec) -> MachineScore:
    """Score one machine, cross-checking declared maturity vs DoD."""
    dod = evaluate_dod(spec)
    implied_band = round(dod.pct / 100 * 5)
    drift = abs(spec.maturity_score - implied_band)
    consistency: Literal["consistent", "inconsistent"] = (
        "consistent" if drift <= _CONSISTENCY_TOLERANCE else "inconsistent"
    )
    return MachineScore(
        machine_id=spec.id,
        name=spec.name,
        declared_score=spec.maturity_score,
        declared_level=MATURITY_LEVELS.get(spec.maturity_score, "Unknown"),
        target_score=spec.scorecard_target,
        dod_pct=dod.pct,
        implied_band=implied_band,
        consistency=consistency,
        gap_to_target=max(0, spec.scorecard_target - spec.maturity_score),
        owner=spec.owner,
    )


def aggregate_score(reg: MachineRegistry) -> PortfolioScore:
    """Aggregate maturity across the whole registry."""
    scores = tuple(score_machine(m) for m in reg.machines)
    total = len(scores)
    if total == 0:
        return PortfolioScore(
            machines=(),
            mean_maturity=0.0,
            target_mean=0.0,
            percentage=0.0,
            readiness_label="Internal Only",
            machines_at_target=0,
            machines_total=0,
            inconsistent_count=0,
        )
    mean = round(sum(s.declared_score for s in scores) / total, 2)
    target_mean = round(sum(s.target_score for s in scores) / total, 2)
    percentage = round(mean / 5 * 100, 1)
    return PortfolioScore(
        machines=scores,
        mean_maturity=mean,
        target_mean=target_mean,
        percentage=percentage,
        readiness_label=readiness_label(percentage),
        machines_at_target=sum(
            1 for s in scores if s.declared_score >= s.target_score
        ),
        machines_total=total,
        inconsistent_count=sum(
            1 for s in scores if s.consistency == "inconsistent"
        ),
    )


__all__ = [
    "MATURITY_LEVELS",
    "MachineScore",
    "PortfolioScore",
    "ReadinessLabel",
    "aggregate_score",
    "readiness_label",
    "score_machine",
]
