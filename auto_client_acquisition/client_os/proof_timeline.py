"""Proof timeline — portfolio of proof and value events on the client surface."""

from __future__ import annotations

PROOF_TIMELINE_SIGNALS: tuple[str, ...] = (
    "proof_events",
    "value_events",
    "blocked_risks",
    "before_after",
    "client_confirmed_value",
    "estimated_vs_verified_value",
)


def proof_timeline_coverage_score(signals_tracked: frozenset[str]) -> int:
    if not PROOF_TIMELINE_SIGNALS:
        return 0
    n = sum(1 for s in PROOF_TIMELINE_SIGNALS if s in signals_tracked)
    return (n * 100) // len(PROOF_TIMELINE_SIGNALS)
