"""Lightweight data quality metrics for account-style rows (dicts)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class DataQualityScore:
    overall: float
    completeness: float
    duplicate_inverse: float
    format_consistency: float
    source_clarity: float


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


def compute_dq(
    *,
    preview: Any,
    duplicates_found: int = 0,
    source_passport: Any | None = None,
) -> DataQualityScore:
    """Compute a normalized Data Quality score (0..100) for preview payloads."""
    row_count = max(int(getattr(preview, "row_count", 0)), 0)
    missing_pct = dict(getattr(preview, "missing_pct", {}) or {})
    if missing_pct:
        avg_missing = sum(float(v) for v in missing_pct.values()) / len(missing_pct)
    else:
        avg_missing = 1.0 if row_count == 0 else 0.0
    completeness = round(max(0.0, min(100.0, (1.0 - avg_missing) * 100.0)), 2)

    if row_count <= 0:
        duplicate_inverse = 100.0
    else:
        duplicate_ratio = min(max(float(duplicates_found) / float(row_count), 0.0), 1.0)
        duplicate_inverse = round((1.0 - duplicate_ratio) * 100.0, 2)

    # Deterministic lightweight consistency estimate from missingness variance.
    if missing_pct:
        variance = sum((float(v) - avg_missing) ** 2 for v in missing_pct.values()) / len(missing_pct)
        format_consistency = round(max(0.0, min(100.0, (1.0 - variance) * 100.0)), 2)
    else:
        format_consistency = 80.0 if row_count > 0 else 0.0

    source_clarity = 100.0 if source_passport else 45.0
    overall = round(
        (0.45 * completeness)
        + (0.25 * duplicate_inverse)
        + (0.20 * format_consistency)
        + (0.10 * source_clarity),
        2,
    )
    return DataQualityScore(
        overall=overall,
        completeness=completeness,
        duplicate_inverse=duplicate_inverse,
        format_consistency=format_consistency,
        source_clarity=source_clarity,
    )
