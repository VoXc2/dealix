"""Enterprise rollout dashboard — sponsor through expansion."""

from __future__ import annotations

ROLLOUT_DASHBOARD_SIGNALS: tuple[str, ...] = (
    "sponsor_status",
    "data_readiness",
    "governance_readiness",
    "workflow_owner",
    "proof_score",
    "adoption_score",
    "risk_flags",
    "retainer_readiness",
    "expansion_path",
    "platform_pull_signals",
)


def rollout_dashboard_coverage_score(signals_tracked: frozenset[str]) -> int:
    if not ROLLOUT_DASHBOARD_SIGNALS:
        return 0
    n = sum(1 for s in ROLLOUT_DASHBOARD_SIGNALS if s in signals_tracked)
    return (n * 100) // len(ROLLOUT_DASHBOARD_SIGNALS)
