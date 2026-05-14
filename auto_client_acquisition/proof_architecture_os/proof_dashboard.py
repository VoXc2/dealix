"""Proof dashboard — headline portfolio signals."""

from __future__ import annotations

PROOF_DASHBOARD_SIGNALS: tuple[str, ...] = (
    "proof_packs_delivered",
    "average_proof_score",
    "proof_by_type",
    "proof_to_retainer_conversion",
    "case_candidate_count",
    "weak_proof_count",
    "risk_events_blocked",
    "value_events_recorded",
    "client_confirmed_value",
    "estimated_vs_verified_value",
)


def proof_dashboard_coverage_score(signals_tracked: frozenset[str]) -> int:
    if not PROOF_DASHBOARD_SIGNALS:
        return 0
    n = sum(1 for s in PROOF_DASHBOARD_SIGNALS if s in signals_tracked)
    return (n * 100) // len(PROOF_DASHBOARD_SIGNALS)
