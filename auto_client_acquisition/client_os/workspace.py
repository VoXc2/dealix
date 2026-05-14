"""Client workspace usage signals for product traction."""

from __future__ import annotations

CLIENT_OS_USAGE_SIGNALS: tuple[str, ...] = (
    "workspace_active_clients",
    "monthly_active_stakeholders",
    "drafts_reviewed",
    "approvals_completed",
    "proof_views",
    "next_actions_accepted",
    "retainer_conversions",
    "expansion_clicks",
    "governance_decisions_viewed",
)


def client_os_usage_coverage_score(signals_tracked: frozenset[str]) -> int:
    if not CLIENT_OS_USAGE_SIGNALS:
        return 0
    n = sum(1 for s in CLIENT_OS_USAGE_SIGNALS if s in signals_tracked)
    return (n * 100) // len(CLIENT_OS_USAGE_SIGNALS)
