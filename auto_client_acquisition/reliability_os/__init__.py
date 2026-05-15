"""Reliability OS v5 — health matrix aggregator over local subsystems.

Probes the in-process state of every subsystem we care about and
returns one structured matrix for the founder dashboard / Daily
digest. Pure local checks — never network, never DB writes.
"""
from auto_client_acquisition.reliability_os.health_matrix import (
    HealthDimension,
    HealthStatus,
    SubsystemHealth,
    build_health_matrix,
    summary,
)
from auto_client_acquisition.reliability_os.mission_critical_program import (
    DrillResult,
    MissionCriticalScore,
    compute_mission_critical_score,
)

__all__ = [
    "HealthDimension",
    "HealthStatus",
    "DrillResult",
    "MissionCriticalScore",
    "SubsystemHealth",
    "build_health_matrix",
    "compute_mission_critical_score",
    "summary",
]
