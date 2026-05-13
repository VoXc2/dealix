"""Data Readiness Standard — typed score + 4-tier classification."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DataReadinessTier(str, Enum):
    READY = "ready_for_ai_workflow"            # 85+
    CLEANUP = "usable_with_cleanup"            # 70..84
    DIAGNOSTIC = "diagnostic_only"             # 50..69
    SPRINT_FIRST = "readiness_sprint_first"    # <50


@dataclass(frozen=True)
class DataReadinessComponents:
    source_clarity: int
    completeness: int
    duplicates_inverse: int  # 100 means no duplicates
    missing_fields_inverse: int
    format_quality: int
    pii_classified: int
    allowed_use_clarity: int

    def __post_init__(self) -> None:
        for name in (
            "source_clarity",
            "completeness",
            "duplicates_inverse",
            "missing_fields_inverse",
            "format_quality",
            "pii_classified",
            "allowed_use_clarity",
        ):
            v = getattr(self, name)
            if not 0 <= v <= 100:
                raise ValueError(f"{name}_out_of_range_0_100")


def compute_data_readiness_score(c: DataReadinessComponents) -> int:
    fields = (
        c.source_clarity,
        c.completeness,
        c.duplicates_inverse,
        c.missing_fields_inverse,
        c.format_quality,
        c.pii_classified,
        c.allowed_use_clarity,
    )
    return round(sum(fields) / len(fields))


def classify_data_readiness(score: int) -> DataReadinessTier:
    if score >= 85:
        return DataReadinessTier.READY
    if score >= 70:
        return DataReadinessTier.CLEANUP
    if score >= 50:
        return DataReadinessTier.DIAGNOSTIC
    return DataReadinessTier.SPRINT_FIRST
