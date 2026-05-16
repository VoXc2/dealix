"""Agentic Economic Operating Layer primitives (Systems 46-55)."""

from __future__ import annotations

from auto_client_acquisition.agentic_economic_os.dependency_engine import (
    DependencyScorecard,
    DependencySignals,
    InfrastructureThresholds,
    compute_dependency_scorecard,
    infrastructure_status,
)
from auto_client_acquisition.agentic_economic_os.platform_readiness import (
    collect_platform_paths,
    platform_readiness_snapshot,
)
from auto_client_acquisition.agentic_economic_os.systems_registry import (
    FINAL_CIVILIZATIONAL_SYSTEMS,
    CivilizationalSystem,
    all_required_platform_paths,
    coverage_ratio,
    missing_required_paths,
)

__all__ = [
    "FINAL_CIVILIZATIONAL_SYSTEMS",
    "DependencyScorecard",
    "DependencySignals",
    "InfrastructureThresholds",
    "CivilizationalSystem",
    "all_required_platform_paths",
    "collect_platform_paths",
    "compute_dependency_scorecard",
    "coverage_ratio",
    "infrastructure_status",
    "missing_required_paths",
    "platform_readiness_snapshot",
]
