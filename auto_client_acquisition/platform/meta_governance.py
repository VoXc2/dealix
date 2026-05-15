"""Meta-governance drift detection."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GovernanceDriftReport:
    drift_score: float
    violations: tuple[str, ...]
    recommended_actions: tuple[str, ...]


def assess_meta_governance(
    *, policy_violation_rate: float, unaudited_action_rate: float, approval_sla_miss_rate: float
) -> GovernanceDriftReport:
    score = (
        0.5 * min(max(policy_violation_rate, 0.0), 1.0)
        + 0.3 * min(max(unaudited_action_rate, 0.0), 1.0)
        + 0.2 * min(max(approval_sla_miss_rate, 0.0), 1.0)
    )
    violations: list[str] = []
    if policy_violation_rate > 0.05:
        violations.append('policy_violation_rate_high')
    if unaudited_action_rate > 0.01:
        violations.append('unaudited_actions_detected')
    if approval_sla_miss_rate > 0.1:
        violations.append('approval_sla_miss_high')
    actions = tuple('mitigate:' + item for item in violations)
    return GovernanceDriftReport(drift_score=round(min(score, 1.0), 4), violations=tuple(violations), recommended_actions=actions)


__all__ = ['GovernanceDriftReport', 'assess_meta_governance']
