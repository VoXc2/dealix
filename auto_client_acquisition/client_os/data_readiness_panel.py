"""Data readiness panel — signals shown on the client workspace."""

from __future__ import annotations

DATA_READINESS_PANEL_SIGNALS: tuple[str, ...] = (
    "sources_uploaded",
    "source_passport_status",
    "data_quality_score",
    "duplicates",
    "missing_fields",
    "pii_flags",
    "allowed_use",
)


def data_readiness_panel_coverage_score(signals_tracked: frozenset[str]) -> int:
    if not DATA_READINESS_PANEL_SIGNALS:
        return 0
    n = sum(1 for s in DATA_READINESS_PANEL_SIGNALS if s in signals_tracked)
    return (n * 100) // len(DATA_READINESS_PANEL_SIGNALS)
