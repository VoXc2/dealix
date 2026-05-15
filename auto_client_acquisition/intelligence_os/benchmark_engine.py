"""Benchmark labels and safe sector templates — deterministic, no external API."""

from __future__ import annotations

from typing import Final

# Canonical benchmark dimensions (populate from aggregated, anonymized ledgers over time)
BENCHMARK_DIMENSIONS: Final[tuple[str, ...]] = (
    "data_readiness_by_sector",
    "workflow_bottlenecks",
    "governance_risk_patterns",
    "proof_pack_metrics",
    "retainer_conversion_by_service",
    "delivery_effort_by_service",
)

# Illustrative safe defaults for B2B services (replace with measured aggregates)
B2B_SERVICES_DEFAULT_READINESS_RANGE: Final[tuple[int, int]] = (50, 70)
B2B_SERVICES_COMMON_GAPS: Final[tuple[str, ...]] = (
    "missing_source_field",
    "duplicate_leads",
    "no_pipeline_stage",
)


def b2b_services_starting_offer_hint() -> str:
    """Product copy / strategy hint only — not a client-specific claim."""
    return "Lead Intelligence Sprint"
