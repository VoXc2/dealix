"""Mission-critical readiness scoring for reliability drills and controls."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DrillResult:
    name: str
    passed: bool
    severity: str = "high"


@dataclass(frozen=True, slots=True)
class MissionCriticalScore:
    score: float
    status: str
    blockers: tuple[str, ...]


def compute_mission_critical_score(drills: tuple[DrillResult, ...], slo_breaches_open: int) -> MissionCriticalScore:
    blockers: list[str] = []
    if not drills:
        blockers.append("no_drills_recorded")
    for drill in drills:
        if not drill.passed:
            blockers.append(f"drill_failed:{drill.name}")
    if slo_breaches_open > 0:
        blockers.append("open_slo_breaches")
    total = len(drills) if drills else 1
    passed = sum(1 for drill in drills if drill.passed)
    base = (passed / total) * 100.0
    penalty = min(40.0, float(slo_breaches_open) * 5.0)
    score = round(max(0.0, base - penalty), 2)
    if score >= 90.0 and not blockers:
        status = "mission_critical_ready"
    elif score >= 70.0:
        status = "enterprise_ready"
    else:
        status = "not_ready"
    return MissionCriticalScore(score=score, status=status, blockers=tuple(blockers))


__all__ = ["DrillResult", "MissionCriticalScore", "compute_mission_critical_score"]
