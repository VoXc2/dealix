"""Dealix Execution Assurance — scorecards, KPI health, audits (YAML + runtime checks)."""

from dealix.execution_assurance.health import compute_full_ops_health
from dealix.execution_assurance.registry import assurance_version, load_registry

__all__ = ["assurance_version", "compute_full_ops_health", "load_registry"]
