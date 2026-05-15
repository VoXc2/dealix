"""Data and learning flywheel metrics for governed revenue workflows."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FlywheelInputs:
    source_reliability: float
    dedupe_precision: float
    signal_freshness: float
    actionability_precision: float
    outcome_conversion: float
    learning_adoption: float


@dataclass(frozen=True, slots=True)
class FlywheelScore:
    overall: float
    band: str


def compute_flywheel_score(inputs: FlywheelInputs) -> FlywheelScore:
    values = (
        inputs.source_reliability,
        inputs.dedupe_precision,
        inputs.signal_freshness,
        inputs.actionability_precision,
        inputs.outcome_conversion,
        inputs.learning_adoption,
    )
    clipped = tuple(max(0.0, min(100.0, float(v))) for v in values)
    overall = round(sum(clipped) / len(clipped), 2)
    if overall >= 85.0:
        band = "compounding"
    elif overall >= 70.0:
        band = "stable"
    elif overall >= 50.0:
        band = "developing"
    else:
        band = "fragile"
    return FlywheelScore(overall=overall, band=band)


def gating_failures(inputs: FlywheelInputs) -> tuple[str, ...]:
    failures: list[str] = []
    if inputs.source_reliability < 70.0:
        failures.append("source_reliability_below_gate")
    if inputs.dedupe_precision < 80.0:
        failures.append("dedupe_precision_below_gate")
    if inputs.actionability_precision < 65.0:
        failures.append("actionability_precision_below_gate")
    if inputs.outcome_conversion < 40.0:
        failures.append("outcome_conversion_below_gate")
    return tuple(failures)


__all__ = ["FlywheelInputs", "FlywheelScore", "compute_flywheel_score", "gating_failures"]
