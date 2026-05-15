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
    """Deterministic quality score used by Data OS endpoints."""

    overall: float
    completeness: float
    duplicate_inverse: float
    format_consistency: float
    source_clarity: float


def _clip_pct(v: float) -> float:
    return round(max(0.0, min(100.0, float(v))), 2)


def compute_dq(
    *,
    preview: Any,
    duplicates_found: int = 0,
    source_passport: Any | None = None,
) -> DataQualityScore:
    """Compute a stable 0..100 DQ score from preview output.

    Compatibility surface used by multiple routers/orchestrators.
    Accepts either an object-like preview (with ``row_count``/``missing_pct``)
    or a dict-based preview.
    """
    # Completeness
    if hasattr(preview, "missing_pct"):
        missing = getattr(preview, "missing_pct") or {}
        if isinstance(missing, dict) and missing:
            completeness = _clip_pct(100.0 - (sum(float(v) for v in missing.values()) / len(missing)))
        else:
            completeness = 100.0
        suggested_cleanup_len = len(getattr(preview, "suggested_cleanup", ()) or ())
    elif isinstance(preview, dict):
        dq = preview.get("data_quality", {}) if isinstance(preview.get("data_quality"), dict) else {}
        if "mean_completeness" in dq:
            completeness = _clip_pct(float(dq.get("mean_completeness", 0.0)) * 100.0)
        else:
            completeness = 0.0
        suggested_cleanup_len = 0
    else:
        completeness = 0.0
        suggested_cleanup_len = 0

    duplicate_inverse = _clip_pct(100.0 - (max(0, int(duplicates_found)) * 5.0))
    format_consistency = _clip_pct(100.0 - min(80.0, suggested_cleanup_len * 8.0))

    has_source_passport = bool(source_passport)
    source_clarity = 100.0 if has_source_passport else 60.0

    overall = _clip_pct(
        (0.5 * completeness)
        + (0.2 * duplicate_inverse)
        + (0.2 * format_consistency)
        + (0.1 * source_clarity)
    )
    return DataQualityScore(
        overall=overall,
        completeness=completeness,
        duplicate_inverse=duplicate_inverse,
        format_consistency=format_consistency,
        source_clarity=source_clarity,
    )
