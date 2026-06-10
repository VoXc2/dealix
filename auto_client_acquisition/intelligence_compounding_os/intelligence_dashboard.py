"""Intelligence dashboard — canonical signal tiles for compounding review."""

from __future__ import annotations

INTELLIGENCE_DASHBOARD_SIGNALS: tuple[str, ...] = (
    "top_market_pains",
    "top_client_expansion_signals",
    "data_readiness_patterns",
    "workflow_friction_patterns",
    "governance_risks_repeated",
    "productization_candidates",
    "benchmark_candidates",
    "offer_performance",
    "arabic_qa_issues",
    "retainer_signals",
    "business_unit_signals",
)


def intelligence_dashboard_coverage_score(signals_tracked: frozenset[str]) -> int:
    if not INTELLIGENCE_DASHBOARD_SIGNALS:
        return 0
    n = sum(1 for s in INTELLIGENCE_DASHBOARD_SIGNALS if s in signals_tracked)
    return (n * 100) // len(INTELLIGENCE_DASHBOARD_SIGNALS)
