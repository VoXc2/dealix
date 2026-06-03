"""Adoption dashboard — headline signals for account growth decisions."""

from __future__ import annotations

ADOPTION_DASHBOARD_SIGNALS: tuple[str, ...] = (
    "client_adoption_score",
    "workspace_activity",
    "approval_completion",
    "proof_visibility",
    "friction_events",
    "retainer_readiness",
    "expansion_pull",
    "training_needs",
)


def adoption_dashboard_coverage_score(signals_tracked: frozenset[str]) -> int:
    if not ADOPTION_DASHBOARD_SIGNALS:
        return 0
    n = sum(1 for s in ADOPTION_DASHBOARD_SIGNALS if s in signals_tracked)
    return (n * 100) // len(ADOPTION_DASHBOARD_SIGNALS)
