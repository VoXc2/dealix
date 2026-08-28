"""V18 Experiment Registry (Workstream E / §12).

Every meaningful commercial move is a bounded experiment. Decision must be
SCALE / RETEST / STOP / INVALID. SCALE requires outcome evidence — an
experiment can never SCALE on intention or vanity metrics alone.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class ExperimentDecision(StrEnum):
    SCALE = "SCALE"
    RETEST = "RETEST"
    STOP = "STOP"
    INVALID = "INVALID"


_VALID_DECISIONS = frozenset(d.value for d in ExperimentDecision)


@dataclass(frozen=True, slots=True)
class Experiment:
    experiment_id: str
    hypothesis: str
    segment: str = ""
    account_cohort: str = ""
    buying_group_role: str = ""
    offer: str = ""
    channel: str = ""
    asset: str = ""
    cta: str = ""
    expected_evidence: str = ""
    start: str = ""
    end: str = ""
    founder_minutes: int = 0
    agent_cost: float = 0.0
    delivery_cost: int = 0
    outcome: str = ""
    confidence: str = ""
    learning: str = ""
    decision: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "hypothesis": self.hypothesis,
            "segment": self.segment,
            "account_cohort": self.account_cohort,
            "buying_group_role": self.buying_group_role,
            "offer": self.offer,
            "channel": self.channel,
            "asset": self.asset,
            "cta": self.cta,
            "expected_evidence": self.expected_evidence,
            "start": self.start,
            "end": self.end,
            "founder_minutes": self.founder_minutes,
            "agent_cost": self.agent_cost,
            "delivery_cost": self.delivery_cost,
            "outcome": self.outcome,
            "confidence": self.confidence,
            "learning": self.learning,
            "decision": self.decision,
        }


@dataclass(frozen=True, slots=True)
class ExperimentRegistry:
    experiments: tuple[Experiment, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "experiments": [e.to_dict() for e in self.experiments],
            "count": len(self.experiments),
        }


def validate_experiment(exp: Experiment) -> list[str]:
    """Deterministic gates. A decision is required to be one of the four
    canonical decisions, and SCALE requires outcome evidence."""
    errors: list[str] = []
    if not str(exp.experiment_id or "").strip():
        errors.append("MISSING_EXPERIMENT_ID")
    if not str(exp.hypothesis or "").strip():
        errors.append("MISSING_HYPOTHESIS")
    if exp.decision and exp.decision not in _VALID_DECISIONS:
        errors.append(f"INVALID_DECISION:{exp.decision}")
    if exp.decision == ExperimentDecision.SCALE.value and not str(
        exp.outcome or ""
    ).strip():
        errors.append("SCALE_WITHOUT_OUTCOME_EVIDENCE")
    if exp.decision and not exp.decision == "" and not str(exp.outcome or "").strip():
        # RETEST/STOP should also be evidence-grounded; only INVALID is a
        # declaration, but we still require the reason in outcome.
        if exp.decision != ExperimentDecision.INVALID.value:
            errors.append("DECISION_WITHOUT_OUTCOME_EVIDENCE")
    return errors


def register_experiment(
    registry: ExperimentRegistry, exp: Experiment
) -> tuple[ExperimentRegistry, list[str]]:
    """Register an experiment after deterministic validation.

    Returns (new registry, validation errors). Invalid experiments are
    rejected — never auto-qualified or auto-scaled.
    """
    errors = validate_experiment(exp)
    if errors:
        return registry, errors
    if any(e.experiment_id == exp.experiment_id for e in registry.experiments):
        return registry, ["DUPLICATE_EXPERIMENT_ID"]
    return ExperimentRegistry(experiments=registry.experiments + (exp,)), []
