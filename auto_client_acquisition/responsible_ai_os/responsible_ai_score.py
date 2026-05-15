"""Responsible AI Score — seven weighted dimensions (0–100 each)."""

from __future__ import annotations

from dataclasses import dataclass

_WEIGHTS: tuple[int, ...] = (15, 15, 15, 15, 15, 15, 10)


@dataclass(frozen=True, slots=True)
class ResponsibleAIDimensions:
    source_clarity: int
    data_sensitivity_handling: int
    human_oversight: int
    governance_decision_coverage: int
    auditability: int
    proof_of_value: int
    incident_readiness: int


def _clamp_pct(value: int) -> int:
    if value < 0:
        return 0
    if value > 100:
        return 100
    return value


def responsible_ai_score(dimensions: ResponsibleAIDimensions) -> int:
    d = dimensions
    values = (
        _clamp_pct(d.source_clarity),
        _clamp_pct(d.data_sensitivity_handling),
        _clamp_pct(d.human_oversight),
        _clamp_pct(d.governance_decision_coverage),
        _clamp_pct(d.auditability),
        _clamp_pct(d.proof_of_value),
        _clamp_pct(d.incident_readiness),
    )
    total = sum(v * w for v, w in zip(values, _WEIGHTS, strict=True))
    return min(100, total // 100)


def responsible_ai_deployment_band(score: int) -> str:
    if score >= 85:
        return "responsible_ai_ready"
    if score >= 70:
        return "ready_with_controls"
    if score >= 55:
        return "governance_review_required"
    return "do_not_deploy"
