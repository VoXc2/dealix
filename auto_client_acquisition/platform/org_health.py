"""Organizational health scoring."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OrgHealthSnapshot:
    health_score: float
    status: str
    notes: tuple[str, ...]


def compute_org_health(*, failure_rate: float, sla_hit_ratio: float, governance_coverage_ratio: float) -> OrgHealthSnapshot:
    score = max(
        0.0,
        min(1.0, (0.4 * (1 - failure_rate)) + (0.3 * sla_hit_ratio) + (0.3 * governance_coverage_ratio)),
    )
    if score >= 0.85:
        status = 'strong'
    elif score >= 0.65:
        status = 'stable'
    elif score >= 0.45:
        status = 'at_risk'
    else:
        status = 'critical'
    notes = (
        f'failure_rate={round(failure_rate,4)}',
        f'sla_hit_ratio={round(sla_hit_ratio,4)}',
        f'governance_coverage_ratio={round(governance_coverage_ratio,4)}',
    )
    return OrgHealthSnapshot(health_score=round(score, 4), status=status, notes=notes)


__all__ = ['OrgHealthSnapshot', 'compute_org_health']
