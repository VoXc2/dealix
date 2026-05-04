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

__all__ = [
    "HealthDimension",
    "HealthStatus",
    "SubsystemHealth",
    "build_health_matrix",
    "summary",
]
