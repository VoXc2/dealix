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
class DQScore:
    overall: float
    completeness: float
    duplicate_inverse: float
    format_consistency: float
    source_clarity: float


def _clamp_score(v: float) -> float:
    return round(max(0.0, min(100.0, float(v))), 2)


def compute_dq(
    *,
    preview: Any,
    duplicates_found: int = 0,
    source_passport: Any = None,
) -> DQScore:
    """Compute weighted DQ score from preview + governance context."""
    missing_pct = getattr(preview, "missing_pct", {}) or {}
    row_count = max(int(getattr(preview, "row_count", 0) or 0), 0)
    suggested_cleanup = getattr(preview, "suggested_cleanup", []) or []

    if missing_pct:
        avg_missing = sum(float(v) for v in missing_pct.values()) / len(missing_pct)
        completeness = _clamp_score(100.0 - avg_missing)
    else:
        completeness = 0.0

    if row_count <= 0:
        duplicate_inverse = 0.0
    else:
        duplicate_inverse = _clamp_score(
            100.0 - (max(int(duplicates_found), 0) / row_count) * 100.0
        )

    format_penalty = 0.0
    for item in suggested_cleanup:
        if str(item).startswith("fill_missing:"):
            format_penalty += 6.0
        elif item == "review_pii_columns_before_ai_use":
            format_penalty += 4.0
        elif item == "empty_dataset":
            format_penalty += 100.0
    format_consistency = _clamp_score(100.0 - format_penalty)

    if source_passport is None:
        source_clarity = 35.0
    else:
        source_id = str(getattr(source_passport, "source_id", "")).strip()
        ai_ok = bool(getattr(source_passport, "ai_access_allowed", False))
        source_clarity = 100.0 if (source_id and ai_ok) else 60.0

    overall = _clamp_score(
        completeness * 0.35
        + duplicate_inverse * 0.2
        + format_consistency * 0.2
        + source_clarity * 0.25
    )
    return DQScore(
        overall=overall,
        completeness=completeness,
        duplicate_inverse=duplicate_inverse,
        format_consistency=format_consistency,
        source_clarity=_clamp_score(source_clarity),
    )


__all__ = [
    "DQScore",
    "account_row_completeness",
    "compute_dq",
    "duplicate_ratio_by_field",
    "mean_completeness",
    "summarize_table_quality",
]
