"""Weekly scorecard — canonical axis keys (execution truth)."""

from __future__ import annotations

WEEKLY_SCORECARD_KEYS: tuple[str, ...] = (
    "revenue_pipeline",
    "active_delivery",
    "proof_score",
    "governance_incidents",
    "client_adoption",
    "productization_signals",
)


def weekly_scorecard_keys_complete(present: frozenset[str]) -> tuple[bool, tuple[str, ...]]:
    missing = [k for k in WEEKLY_SCORECARD_KEYS if k not in present]
    return not missing, tuple(missing)
