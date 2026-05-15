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
    """Data-quality score for an imported table — all values on a 0-100 scale."""

    overall: float
    completeness: float
    duplicate_inverse: float
    format_consistency: float
    source_clarity: float


def _source_clarity(source_passport: Any) -> float:
    """100 when a valid Source Passport is supplied, 50 when invalid, 0 when absent."""
    if source_passport is None:
        return 0.0
    try:
        from auto_client_acquisition.data_os.source_passport import validate

        return 100.0 if validate(source_passport).is_valid else 50.0
    except Exception:
        return 50.0


def compute_dq(
    *,
    preview: Any,
    duplicates_found: int = 0,
    source_passport: Any = None,
) -> DQScore:
    """Compute a Data-Quality score from an ``ImportPreview``.

    ``preview`` must expose ``row_count``, ``missing_pct`` and ``columns``
    (see ``data_os.import_preview.ImportPreview``).
    """
    row_count = int(getattr(preview, "row_count", 0) or 0)
    missing: dict[str, float] = dict(getattr(preview, "missing_pct", {}) or {})
    columns = tuple(getattr(preview, "columns", ()) or ())

    if missing:
        completeness = round(100.0 - sum(missing.values()) / len(missing), 1)
    else:
        completeness = 100.0 if row_count else 0.0

    if row_count > 0:
        dup_ratio = min(1.0, max(0, duplicates_found) / row_count)
        duplicate_inverse = round(100.0 * (1.0 - dup_ratio), 1)
    else:
        duplicate_inverse = 0.0

    if columns:
        fully_missing = sum(1 for c in columns if missing.get(c, 0.0) >= 100.0)
        format_consistency = round(100.0 * (1.0 - fully_missing / len(columns)), 1)
    else:
        format_consistency = 0.0

    source_clarity = _source_clarity(source_passport)

    overall = round(
        0.40 * completeness
        + 0.25 * duplicate_inverse
        + 0.20 * format_consistency
        + 0.15 * source_clarity,
        1,
    )
    return DQScore(
        overall=overall,
        completeness=completeness,
        duplicate_inverse=duplicate_inverse,
        format_consistency=format_consistency,
        source_clarity=source_clarity,
    )
