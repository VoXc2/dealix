"""Institutional Operating Core verdict engine (System 65)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InstitutionalDependencySnapshot:
    decision_dependency_pct: float
    execution_dependency_pct: float
    governance_dependency_pct: float
    memory_dependency_pct: float
    resilience_dependency_pct: float
    economic_dependency_pct: float


def institutional_dependency_score(snapshot: InstitutionalDependencySnapshot) -> float:
    """Average cross-domain dependency score in percentage."""
    values = (
        snapshot.decision_dependency_pct,
        snapshot.execution_dependency_pct,
        snapshot.governance_dependency_pct,
        snapshot.memory_dependency_pct,
        snapshot.resilience_dependency_pct,
        snapshot.economic_dependency_pct,
    )
    return round(sum(values) / len(values), 2)


def infrastructure_status(
    snapshot: InstitutionalDependencySnapshot,
    *,
    threshold: float = 80.0,
) -> bool:
    """Infrastructure status is reached when dependency crosses threshold."""
    return institutional_dependency_score(snapshot) >= threshold


def operating_core_verdict(
    *,
    snapshot: InstitutionalDependencySnapshot,
    systems_ready: dict[str, bool],
) -> dict[str, object]:
    """Single enterprise verdict for institutional operating readiness."""
    missing = tuple(sorted(name for name, ok in systems_ready.items() if not ok))
    score = institutional_dependency_score(snapshot)
    infra_ok = infrastructure_status(snapshot)
    return {
        "dependency_score": score,
        "infrastructure_status": infra_ok and len(missing) == 0,
        "status": (
            "institutional_operational_infrastructure"
            if infra_ok and len(missing) == 0
            else "in_transition"
        ),
        "system_blockers": missing,
    }
