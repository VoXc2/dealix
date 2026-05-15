"""Platform pull signals — build workspace only after client pull."""

from __future__ import annotations

PLATFORM_PULL_SIGNALS: tuple[str, ...] = (
    "client_asks_for_dashboard",
    "multiple_stakeholders_need_access",
    "approval_workflow_repeats",
    "proof_reports_repeat_monthly",
    "audit_logs_requested",
    "executive_asks_for_live_view",
)


def platform_pull_coverage_score(signals_seen: frozenset[str]) -> int:
    if not PLATFORM_PULL_SIGNALS:
        return 0
    n = sum(1 for s in PLATFORM_PULL_SIGNALS if s in signals_seen)
    return (n * 100) // len(PLATFORM_PULL_SIGNALS)
