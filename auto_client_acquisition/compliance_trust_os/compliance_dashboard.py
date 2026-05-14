"""Compliance dashboard — coverage metrics taxonomy."""

from __future__ import annotations

COMPLIANCE_DASHBOARD_METRICS: tuple[str, ...] = (
    "source_passport_coverage",
    "ai_run_ledger_coverage",
    "governance_decision_coverage",
    "approval_completion_rate",
    "pii_flags",
    "blocked_risks",
    "unsupported_claims_removed",
    "incidents",
    "open_risk_items",
    "trust_pack_updates",
)


def compliance_dashboard_coverage_score(metrics_tracked: frozenset[str]) -> int:
    if not COMPLIANCE_DASHBOARD_METRICS:
        return 0
    n = sum(1 for m in COMPLIANCE_DASHBOARD_METRICS if m in metrics_tracked)
    return (n * 100) // len(COMPLIANCE_DASHBOARD_METRICS)
