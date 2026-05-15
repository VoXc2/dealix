"""Agentic Enterprise OS contracts for Systems 16–25."""

from auto_client_acquisition.agentic_enterprise_os.system_registry import (
    SYSTEMS_16_25,
    AgenticDominanceSystem,
    all_required_paths,
    dominance_coverage_percent,
    missing_capabilities,
    most_critical_gaps,
    readiness_by_system,
    system_completion_ratio,
    systems_by_id,
)

__all__ = [
    "SYSTEMS_16_25",
    "AgenticDominanceSystem",
    "all_required_paths",
    "dominance_coverage_percent",
    "missing_capabilities",
    "most_critical_gaps",
    "readiness_by_system",
    "system_completion_ratio",
    "systems_by_id",
]
