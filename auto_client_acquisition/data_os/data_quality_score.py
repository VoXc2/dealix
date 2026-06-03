"""Lightweight data quality metrics for account-style rows (dicts)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def account_row_completeness(row: dict[str, Any], required_keys: tuple[str, ...]) -> float:
    """Share of required keys with non-empty string values (or numeric)."""
    if not required_keys:
        return 1.0
    ok = 0
    for k in required_keys:
        v = row.get(k)
        if v is None:
            continue
        if (isinstance(v, str) and v.strip()) or (
            isinstance(v, (int, float)) and not isinstance(v, bool)
        ):
            ok += 1
    return ok / len(required_keys)


def mean_completeness(rows: list[dict[str, Any]], required_keys: tuple[str, ...]) -> float:
    if not rows:
        return 0.0
    return round(
        sum(account_row_completeness(r, required_keys) for r in rows) / len(rows),
        4,
    )


def duplicate_ratio_by_field(rows: list[dict[str, Any]], field: str = "company_name") -> float:
    """
    Approximate duplicate rate: 1 - (unique non-empty / total non-empty).

    Case-insensitive on string values.
    """
    vals: list[str] = []
    for r in rows:
        raw = r.get(field)
        if raw is None:
            continue
        s = str(raw).strip().lower()
        if s:
            vals.append(s)
    if not vals:
        return 0.0
    unique = len(set(vals))
    return round(1.0 - (unique / len(vals)), 4)


def summarize_table_quality(
    rows: list[dict[str, Any]],
    *,
    required_keys: tuple[str, ...] = ("company_name", "sector", "city"),
) -> dict[str, Any]:
    """Single dict for executive appendix — deterministic."""
    return {
        "row_count": len(rows),
        "mean_completeness": mean_completeness(rows, required_keys),
        "duplicate_ratio_company_name": duplicate_ratio_by_field(rows, "company_name"),
    }


@dataclass(frozen=True, slots=True)
class DataQualityScore:
    """0–100 Data Quality Score with its four transparent sub-scores."""

    overall: float
    completeness: float
    duplicate_inverse: float
    format_consistency: float
    source_clarity: float


def _format_consistency(rows: list[dict[str, Any]], columns: list[str]) -> float:
    """Share of rows that carry every detected column (structural uniformity)."""
    if not rows or not columns:
        return 0.0
    consistent = sum(1 for r in rows if all(c in r for c in columns))
    return round(consistent / len(rows) * 100, 1)


def _source_coverage(rows: list[dict[str, Any]]) -> float:
    """Share of rows carrying a non-empty ``source`` field."""
    if not rows:
        return 0.0
    with_source = sum(1 for r in rows if str(r.get("source", "")).strip())
    return round(with_source / len(rows) * 100, 1)


def compute_dq(
    rows: list[dict[str, Any]],
    *,
    columns: list[str],
    has_valid_passport: bool,
    required_keys: tuple[str, ...] = ("company_name", "sector", "city"),
) -> DataQualityScore:
    """Compute a 0–100 Data Quality Score from real, deterministic metrics."""
    completeness = round(mean_completeness(rows, required_keys) * 100, 1)
    duplicate_inverse = round(
        (1.0 - duplicate_ratio_by_field(rows, "company_name")) * 100, 1,
    )
    format_consistency = _format_consistency(rows, columns)
    source_clarity = 100.0 if has_valid_passport else _source_coverage(rows)
    overall = round(
        0.40 * completeness
        + 0.30 * duplicate_inverse
        + 0.15 * format_consistency
        + 0.15 * source_clarity,
        1,
    )
    return DataQualityScore(
        overall=overall,
        completeness=completeness,
        duplicate_inverse=duplicate_inverse,
        format_consistency=format_consistency,
        source_clarity=source_clarity,
    )


def compute_dq_from_preview(
    preview: Any,
    *,
    duplicates_found: int = 0,
    source_passport: Any | None = None,
) -> DataQualityScore:
    """Legacy adapter for ImportPreview-style objects (flywheel, delivery sprint)."""
    row_count = int(getattr(preview, "row_count", 0) or 0)
    rows = list(getattr(preview, "rows", ()) or ())
    columns = list(getattr(preview, "columns", ()) or getattr(preview, "detected_columns", ()) or [])
    if not rows and hasattr(preview, "missing_pct"):
        # ImportPreview dataclass path — no row bodies; approximate from metadata.
        missing_pct = getattr(preview, "missing_pct", {}) or {}
        if missing_pct:
            avg_missing = sum(float(v) for v in missing_pct.values()) / len(missing_pct)
            completeness = round(max(0.0, 100.0 - (avg_missing * 100.0)), 2)
        elif row_count > 0:
            completeness = 100.0
        else:
            completeness = 0.0
        if row_count <= 0:
            duplicate_inverse = 0.0
        else:
            duplicate_ratio = min(1.0, max(0.0, float(duplicates_found) / float(row_count)))
            duplicate_inverse = round((1.0 - duplicate_ratio) * 100.0, 2)
        format_consistency = 100.0 if row_count > 0 else 0.0
        source_clarity = 100.0 if source_passport is not None else 70.0
        overall = round(
            (0.40 * completeness)
            + (0.25 * duplicate_inverse)
            + (0.20 * format_consistency)
            + (0.15 * source_clarity),
            2,
        )
        return DataQualityScore(
            overall=overall,
            completeness=completeness,
            duplicate_inverse=duplicate_inverse,
            format_consistency=format_consistency,
            source_clarity=source_clarity,
        )
    return compute_dq(
        rows,
        columns=columns,
        has_valid_passport=source_passport is not None,
    )


__all__ = [
    "DataQualityScore",
    "account_row_completeness",
    "compute_dq",
    "compute_dq_from_preview",
    "duplicate_ratio_by_field",
    "mean_completeness",
    "summarize_table_quality",
]
