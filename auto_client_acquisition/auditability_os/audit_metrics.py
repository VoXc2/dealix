"""Audit metrics keys — coverage of logging and policy checks."""

from __future__ import annotations

AUDIT_METRIC_KEYS: tuple[str, ...] = (
    "policy_checks_logged",
    "governance_decisions_logged",
    "approval_events_logged",
    "ai_runs_logged",
    "outputs_linked_to_proof",
    "pii_incidents_zero",
)


def audit_metrics_coverage_score(tracked: frozenset[str]) -> int:
    if not AUDIT_METRIC_KEYS:
        return 0
    n = sum(1 for k in AUDIT_METRIC_KEYS if k in tracked)
    return (n * 100) // len(AUDIT_METRIC_KEYS)


__all__ = ["AUDIT_METRIC_KEYS", "audit_metrics_coverage_score"]
