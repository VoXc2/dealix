"""Board dashboard — twelve headline metrics for governance / investors."""

from __future__ import annotations

BOARD_DASHBOARD_METRICS: tuple[str, ...] = (
    "revenue",
    "mrr",
    "gross_margin",
    "proof_packs_delivered",
    "proof_to_retainer_conversion",
    "governance_incidents",
    "ai_run_audit_coverage",
    "capital_assets_created",
    "productization_candidates",
    "client_health",
    "business_unit_maturity",
    "market_power_signals",
)


def board_dashboard_coverage_score(metrics_reported: frozenset[str]) -> int:
    """Share of board metrics explicitly tracked (0–100)."""
    if not BOARD_DASHBOARD_METRICS:
        return 0
    n = sum(1 for m in BOARD_DASHBOARD_METRICS if m in metrics_reported)
    return (n * 100) // len(BOARD_DASHBOARD_METRICS)
