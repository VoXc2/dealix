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
    """Compute a 0–100 Data Quality Score from real, deterministic metrics.

    The score is a transparent weighted blend — no opaque heuristics:
      * completeness       — mean share of required fields present.
      * duplicate_inverse  — 1 minus the company-name duplicate ratio.
      * format_consistency — share of structurally uniform rows.
      * source_clarity     — source-field coverage; a valid Source Passport
        documents provenance and floors this at 100.
    """
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
