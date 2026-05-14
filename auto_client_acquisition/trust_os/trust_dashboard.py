"""Trust dashboard signal keys (client-facing read models)."""

from __future__ import annotations

TRUST_DASHBOARD_SIGNALS: tuple[str, ...] = (
    "passport_valid",
    "governance_runtime_green",
    "proof_pack_current",
    "approval_queue_depth",
    "blocked_risk_count",
    "last_audit_export_at",
)


def trust_dashboard_coverage_score(tracked: frozenset[str]) -> int:
    if not TRUST_DASHBOARD_SIGNALS:
        return 0
    n = sum(1 for s in TRUST_DASHBOARD_SIGNALS if s in tracked)
    return (n * 100) // len(TRUST_DASHBOARD_SIGNALS)


__all__ = ["TRUST_DASHBOARD_SIGNALS", "trust_dashboard_coverage_score"]
