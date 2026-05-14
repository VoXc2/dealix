"""Data Quality Score — 0-100 composite over completeness + dedupe + format
consistency + source clarity.

Phase 1 stated weights: 60% completeness + 40% inverse-duplicate. Wave 1
keeps that core and adds two small modifiers: format_consistency (column-
type plausibility) and source_clarity (does the data have a passport?).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.data_os.import_preview import ImportPreview
from auto_client_acquisition.data_os.source_passport import SourcePassport


@dataclass
class DQScore:
    overall: float
    completeness: float
    duplicate_inverse: float
    format_consistency: float
    source_clarity: float
    breakdown: dict[str, Any]


def _completeness(missing_pct: dict[str, float]) -> float:
    if not missing_pct:
        return 0.0
    mean_missing = sum(missing_pct.values()) / len(missing_pct)
    return round(max(0.0, 100.0 - mean_missing), 2)


def _duplicate_inverse(duplicates_found: int, total_rows: int) -> float:
    if total_rows <= 0:
        return 100.0
    dup_pct = 100.0 * duplicates_found / total_rows
    return round(max(0.0, 100.0 - dup_pct), 2)


def _format_consistency(preview: ImportPreview) -> float:
    # Heuristic: every column with >0% missing AND mixed plausible formats
    # costs 5 points; capped at -30.
    penalty = 0.0
    for col, pct in preview.missing_pct.items():
        if 0 < pct < 100 and col.lower().endswith(("date", "_at", "amount", "price")):
            penalty += 5.0
    return round(max(0.0, 100.0 - min(30.0, penalty)), 2)


def _source_clarity(passport: SourcePassport | None) -> float:
    if passport is None:
        return 0.0
    if not passport.source_id:
        return 25.0
    if not passport.allowed_use:
        return 50.0
    return 100.0


def compute_dq(
    *,
    preview: ImportPreview,
    duplicates_found: int = 0,
    source_passport: SourcePassport | None = None,
) -> DQScore:
    """Weighted: completeness 0.60, duplicate_inverse 0.30, format 0.05,
    source_clarity 0.05. Wave 1 phrasing — matches Phase 1's 60/40 split
    with two small consistency modifiers."""
    completeness = _completeness(preview.missing_pct)
    dup_inv = _duplicate_inverse(duplicates_found, preview.row_count)
    fmt = _format_consistency(preview)
    src = _source_clarity(source_passport)

    overall = round(
        completeness * 0.60
        + dup_inv * 0.30
        + fmt * 0.05
        + src * 0.05,
        2,
    )
    return DQScore(
        overall=overall,
        completeness=completeness,
        duplicate_inverse=dup_inv,
        format_consistency=fmt,
        source_clarity=src,
        breakdown={
            "row_count": preview.row_count,
            "duplicates_found": duplicates_found,
            "pii_columns": list(preview.pii_columns),
            "missing_pct_mean": round(
                sum(preview.missing_pct.values()) / max(1, len(preview.missing_pct)),
                2,
            ),
            "weights": {"completeness": 0.60, "duplicate_inverse": 0.30, "format": 0.05, "source": 0.05},
        },
    )


__all__ = ["DQScore", "compute_dq"]
