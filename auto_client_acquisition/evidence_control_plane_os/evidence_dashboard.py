"""Evidence dashboard — coverage % and readiness bands."""

from __future__ import annotations


def evidence_coverage_percent(*, satisfied: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round(100.0 * satisfied / total, 2)


def evidence_coverage_band(coverage_pct: float) -> str:
    if coverage_pct < 70:
        return "fragile"
    if coverage_pct < 85:
        return "usable_internally"
    if coverage_pct < 95:
        return "client_ready"
    return "enterprise_ready"
