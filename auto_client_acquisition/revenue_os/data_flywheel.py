"""Data and learning flywheel metrics for governed revenue workflows."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.data_os.data_quality_score import DataQualityScore, compute_dq


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


def flywheel_inputs_from_import_quality(
    dq: DataQualityScore,
    *,
    signal_freshness: float = 78.0,
    outcome_conversion: float = 62.0,
    learning_adoption: float = 72.0,
) -> FlywheelInputs:
    """Map Data OS quality scoring into flywheel dimensions (production hook for governed imports)."""
    return FlywheelInputs(
        source_reliability=float(dq.source_clarity),
        dedupe_precision=float(dq.duplicate_inverse),
        signal_freshness=float(signal_freshness),
        actionability_precision=float(dq.completeness),
        outcome_conversion=float(outcome_conversion),
        learning_adoption=float(learning_adoption),
    )


def flywheel_inputs_from_preview(
    *,
    preview: Any,
    duplicates_found: int = 0,
    source_passport: Any | None = None,
    signal_freshness: float = 78.0,
    outcome_conversion: float = 62.0,
    learning_adoption: float = 72.0,
) -> FlywheelInputs:
    """Convenience: compute DQ from import preview then derive flywheel inputs."""
    dq = compute_dq(preview=preview, duplicates_found=duplicates_found, source_passport=source_passport)
    return flywheel_inputs_from_import_quality(
        dq,
        signal_freshness=signal_freshness,
        outcome_conversion=outcome_conversion,
        learning_adoption=learning_adoption,
    )


__all__ = [
    "FlywheelInputs",
    "FlywheelScore",
    "compute_flywheel_score",
    "flywheel_inputs_from_import_quality",
    "flywheel_inputs_from_preview",
    "gating_failures",
]
