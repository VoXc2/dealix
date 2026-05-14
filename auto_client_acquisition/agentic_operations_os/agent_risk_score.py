"""Agent risk score — weighted 0–100."""

from __future__ import annotations

from dataclasses import dataclass

_WEIGHTS: tuple[int, ...] = (20, 20, 20, 15, 10, 10, 5)


@dataclass(frozen=True, slots=True)
class AgentRiskDimensions:
    data_sensitivity: int
    tool_risk: int
    autonomy_level: int
    external_action_exposure: int
    human_oversight: int
    audit_coverage: int
    business_criticality: int


def _clamp_pct(value: int) -> int:
    if value < 0:
        return 0
    if value > 100:
        return 100
    return value


def agent_risk_score(dimensions: AgentRiskDimensions) -> int:
    d = dimensions
    values = (
        _clamp_pct(d.data_sensitivity),
        _clamp_pct(d.tool_risk),
        _clamp_pct(d.autonomy_level),
        _clamp_pct(d.external_action_exposure),
        _clamp_pct(d.human_oversight),
        _clamp_pct(d.audit_coverage),
        _clamp_pct(d.business_criticality),
    )
    total = sum(v * w for v, w in zip(values, _WEIGHTS, strict=True))
    return min(100, total // 100)


def agent_risk_band(score: int) -> str:
    if score <= 30:
        return "low"
    if score <= 60:
        return "medium"
    if score <= 80:
        return "high"
    return "restricted_not_allowed"
