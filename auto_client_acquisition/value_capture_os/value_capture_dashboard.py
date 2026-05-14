"""Value capture portfolio dashboard — headline signals for monetization health."""

from __future__ import annotations

VALUE_CAPTURE_DASHBOARD_SIGNALS: tuple[str, ...] = (
    "revenue_by_offer",
    "gross_margin_by_offer",
    "revenue_quality_score",
    "client_quality_score",
    "proof_to_retainer_conversion",
    "expansion_revenue",
    "platform_pull_signals",
    "partner_revenue",
    "academy_revenue",
    "venture_readiness",
    "bad_revenue_rejected",
)


def value_capture_dashboard_coverage_score(signals_tracked: frozenset[str]) -> int:
    """Share of value-capture dashboard signals explicitly tracked (0–100)."""
    if not VALUE_CAPTURE_DASHBOARD_SIGNALS:
        return 0
    n = sum(1 for s in VALUE_CAPTURE_DASHBOARD_SIGNALS if s in signals_tracked)
    return (n * 100) // len(VALUE_CAPTURE_DASHBOARD_SIGNALS)
