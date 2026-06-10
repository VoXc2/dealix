"""Data intelligence — anonymized patterns and pattern confidence."""

from __future__ import annotations

DATA_PATTERN_TYPES: tuple[str, ...] = (
    "duplicate_rate",
    "missing_field_pattern",
    "source_clarity_gap",
    "pii_flag_pattern",
    "sector_taxonomy_issue",
    "city_region_quality",
    "allowed_use_gap",
)


def pattern_confidence_band(occurrences: int) -> str:
    if occurrences >= 6:
        return "high"
    if occurrences >= 3:
        return "medium"
    return "low"


def data_pattern_actionable(occurrences: int) -> bool:
    return pattern_confidence_band(occurrences) != "low"
