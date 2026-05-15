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


@dataclass(slots=True)
class DQScore:
    overall: float
    completeness: float
    duplicate_inverse: float
    format_consistency: float
    source_clarity: float


def compute_dq(
    *,
    preview: Any,
    duplicates_found: int = 0,
    source_passport: Any | None = None,
) -> DQScore:
    """Compute deterministic 0..100 DQ score for Data OS import-preview endpoints."""
    row_count = max(1, int(getattr(preview, "row_count", 0)))
    missing_pct = getattr(preview, "missing_pct", {}) or {}

    if missing_pct:
        avg_missing = sum(float(v) for v in missing_pct.values()) / len(missing_pct)
    else:
        avg_missing = 100.0
    completeness = round(max(0.0, 100.0 - avg_missing), 2)

    duplicates_ratio = min(max(float(duplicates_found) / row_count, 0.0), 1.0)
    duplicate_inverse = round((1.0 - duplicates_ratio) * 100.0, 2)

    pii_columns = getattr(preview, "pii_columns", []) or []
    format_consistency = 85.0 if not pii_columns else 75.0

    source_clarity = 95.0 if source_passport is not None else 65.0

    overall = round(
        (
            (completeness * 0.45)
            + (duplicate_inverse * 0.25)
            + (format_consistency * 0.15)
            + (source_clarity * 0.15)
        ),
        2,
    )

    return DQScore(
        overall=overall,
        completeness=completeness,
        duplicate_inverse=duplicate_inverse,
        format_consistency=format_consistency,
        source_clarity=source_clarity,
    )


__all__ = [
    "DQScore",
    "account_row_completeness",
    "compute_dq",
    "duplicate_ratio_by_field",
    "mean_completeness",
    "summarize_table_quality",
]
