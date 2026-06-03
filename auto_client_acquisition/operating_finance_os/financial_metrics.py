"""Financial control metric keys — monthly operating finance review."""

from __future__ import annotations

FINANCIAL_CONTROL_METRICS: tuple[str, ...] = (
    "revenue_by_offer",
    "gross_margin_by_offer",
    "delivery_hours_by_offer",
    "ai_cost_by_workflow",
    "qa_review_hours",
    "scope_creep_incidents",
    "proof_score_by_offer",
    "retainer_conversion",
    "capital_assets_per_project",
    "bad_revenue_rejected",
)


def financial_metrics_tracking_score(metrics_tracked: frozenset[str]) -> int:
    if not FINANCIAL_CONTROL_METRICS:
        return 0
    n = sum(1 for m in FINANCIAL_CONTROL_METRICS if m in metrics_tracked)
    return (n * 100) // len(FINANCIAL_CONTROL_METRICS)
