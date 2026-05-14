"""CEO Command Center — canonical surfaces for weekly board-style review."""

from __future__ import annotations

CEO_COMMAND_CENTER_SURFACES: tuple[str, ...] = (
    "top_5_decisions",
    "revenue_quality",
    "proof_strength",
    "retainer_opportunities",
    "client_risks",
    "productization_queue",
    "governance_risks",
    "bad_revenue_to_reject",
    "business_unit_maturity",
    "venture_signals",
)


def ceo_command_center_coverage_score(surfaces_tracked: frozenset[str]) -> int:
    if not CEO_COMMAND_CENTER_SURFACES:
        return 0
    n = sum(1 for s in CEO_COMMAND_CENTER_SURFACES if s in surfaces_tracked)
    return (n * 100) // len(CEO_COMMAND_CENTER_SURFACES)
