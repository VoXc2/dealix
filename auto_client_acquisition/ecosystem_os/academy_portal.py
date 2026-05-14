"""Academy portal (phase) — curriculum distribution surface checklist."""

from __future__ import annotations

ACADEMY_PORTAL_SIGNALS: tuple[str, ...] = (
    "courses",
    "assessments",
    "certificates",
    "templates",
    "practice_cases",
)


def academy_portal_coverage_score(signals_tracked: frozenset[str]) -> int:
    if not ACADEMY_PORTAL_SIGNALS:
        return 0
    n = sum(1 for s in ACADEMY_PORTAL_SIGNALS if s in signals_tracked)
    return (n * 100) // len(ACADEMY_PORTAL_SIGNALS)
