"""Strategic Control Metrics — thresholds and breach evaluation.

See ``docs/strategic_control/CONTROL_METRICS.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class StrategicControlThreshold(str, Enum):
    GOVERNANCE_COVERAGE_MIN = "governance_coverage_min"
    QA_AVERAGE_MIN = "qa_average_min"
    PROOF_PACK_RATE_MIN = "proof_pack_rate_min"
    CAPITAL_ASSETS_PER_PROJECT_MIN = "capital_assets_per_project_min"
    REPEATED_MANUAL_STEPS_MIN = "repeated_manual_steps_min"


# Doctrine thresholds from the Strategic Control Metrics doc.
CONTROL_METRIC_THRESHOLDS: dict[StrategicControlThreshold, float] = {
    StrategicControlThreshold.GOVERNANCE_COVERAGE_MIN: 0.70,
    StrategicControlThreshold.QA_AVERAGE_MIN: 85.0,
    StrategicControlThreshold.PROOF_PACK_RATE_MIN: 1.00,
    StrategicControlThreshold.CAPITAL_ASSETS_PER_PROJECT_MIN: 1.0,
    StrategicControlThreshold.REPEATED_MANUAL_STEPS_MIN: 3,
}


@dataclass(frozen=True)
class ControlMetricSnapshot:
    period: str
    governance_coverage: float          # 0..1
    qa_average: float                   # 0..100
    proof_pack_rate: float              # 0..1
    capital_assets_per_project: float
    repeated_manual_steps: int


@dataclass(frozen=True)
class ControlMetricResult:
    snapshot: ControlMetricSnapshot
    breaches: tuple[StrategicControlThreshold, ...]
    recommendations: tuple[str, ...]


def evaluate_control_metrics(snapshot: ControlMetricSnapshot) -> ControlMetricResult:
    breaches: list[StrategicControlThreshold] = []
    recs: list[str] = []

    if snapshot.governance_coverage < CONTROL_METRIC_THRESHOLDS[
        StrategicControlThreshold.GOVERNANCE_COVERAGE_MIN
    ]:
        breaches.append(StrategicControlThreshold.GOVERNANCE_COVERAGE_MIN)
        recs.append("do_not_scale_until_governance_coverage_recovers")
    if snapshot.qa_average < CONTROL_METRIC_THRESHOLDS[
        StrategicControlThreshold.QA_AVERAGE_MIN
    ]:
        breaches.append(StrategicControlThreshold.QA_AVERAGE_MIN)
        recs.append("fix_delivery_before_expansion")
    if snapshot.proof_pack_rate < CONTROL_METRIC_THRESHOLDS[
        StrategicControlThreshold.PROOF_PACK_RATE_MIN
    ]:
        breaches.append(StrategicControlThreshold.PROOF_PACK_RATE_MIN)
        recs.append("do_not_claim_value_publicly")
    if snapshot.capital_assets_per_project < CONTROL_METRIC_THRESHOLDS[
        StrategicControlThreshold.CAPITAL_ASSETS_PER_PROJECT_MIN
    ]:
        breaches.append(StrategicControlThreshold.CAPITAL_ASSETS_PER_PROJECT_MIN)
        recs.append("agency_risk_flag_review_engagements")
    if snapshot.repeated_manual_steps < CONTROL_METRIC_THRESHOLDS[
        StrategicControlThreshold.REPEATED_MANUAL_STEPS_MIN
    ]:
        breaches.append(StrategicControlThreshold.REPEATED_MANUAL_STEPS_MIN)
        recs.append("do_not_build_feature_yet")

    return ControlMetricResult(
        snapshot=snapshot,
        breaches=tuple(breaches),
        recommendations=tuple(recs),
    )
