"""Institutional control metrics with 100%-required thresholds.

See ``docs/institutional_control/CONTROL_METRICS.md``.
"""

from __future__ import annotations

from dataclasses import dataclass


INSTITUTIONAL_THRESHOLDS: dict[str, float] = {
    "ai_run_logging_min": 1.00,
    "external_action_approval_min": 1.00,
    "qa_average_min": 85.0,
    "proof_pack_rate_min": 1.00,
    "capital_assets_per_project_min": 1.0,
}


@dataclass(frozen=True)
class InstitutionalControlSnapshot:
    period: str
    ai_run_logging: float
    external_action_approval: float
    qa_average: float
    proof_pack_rate: float
    capital_assets_per_project: float


@dataclass(frozen=True)
class InstitutionalControlResult:
    snapshot: InstitutionalControlSnapshot
    breaches: tuple[str, ...]
    recommendations: tuple[str, ...]


_RECOMMENDATIONS: dict[str, str] = {
    "ai_run_logging_min": "not_enterprise_ready_close_coverage",
    "external_action_approval_min": "halt_external_automation",
    "qa_average_min": "do_not_scale_fix_delivery",
    "proof_pack_rate_min": "no_case_studies",
    "capital_assets_per_project_min": "agency_risk_flag",
}


def evaluate_institutional_controls(
    snapshot: InstitutionalControlSnapshot,
) -> InstitutionalControlResult:
    breaches: list[str] = []
    if snapshot.ai_run_logging < INSTITUTIONAL_THRESHOLDS["ai_run_logging_min"]:
        breaches.append("ai_run_logging_min")
    if snapshot.external_action_approval < INSTITUTIONAL_THRESHOLDS["external_action_approval_min"]:
        breaches.append("external_action_approval_min")
    if snapshot.qa_average < INSTITUTIONAL_THRESHOLDS["qa_average_min"]:
        breaches.append("qa_average_min")
    if snapshot.proof_pack_rate < INSTITUTIONAL_THRESHOLDS["proof_pack_rate_min"]:
        breaches.append("proof_pack_rate_min")
    if snapshot.capital_assets_per_project < INSTITUTIONAL_THRESHOLDS["capital_assets_per_project_min"]:
        breaches.append("capital_assets_per_project_min")

    return InstitutionalControlResult(
        snapshot=snapshot,
        breaches=tuple(breaches),
        recommendations=tuple(_RECOMMENDATIONS[b] for b in breaches),
    )
