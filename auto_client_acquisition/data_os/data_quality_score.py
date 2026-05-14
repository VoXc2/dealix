"""Data Quality scoring — two surfaces in one module.

1. Lightweight account-row helpers (``account_row_completeness``,
   ``mean_completeness``, ``duplicate_ratio_by_field``,
   ``summarize_table_quality``) used by ``delivery_os.readiness_gates``.

2. ``compute_dq`` / ``DQScore`` — Phase-1 weighted composite (60%
   completeness, 30% inverse-duplicate, 5% format, 5% source clarity)
   used by ``api/routers/data_os.py`` and the delivery sprint factory.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# Note: ``ImportPreview`` and ``SourcePassport`` are referenced only as
# forward-ref strings in this module. We deliberately avoid even a
# ``TYPE_CHECKING`` import of them because their packages re-import
# ``data_quality_score`` at module load (e.g. via
# ``revenue_data_intake.csv_preview``). A real import here — even guarded —
# is enough to make CodeQL flag the import graph as cyclic.


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
    """Approximate duplicate rate: 1 - (unique non-empty / total non-empty).

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


# ── Phase-1 composite DQ score ────────────────────────────────────────


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


def _format_consistency(preview: "ImportPreview") -> float:
    penalty = 0.0
    for col, pct in preview.missing_pct.items():
        if 0 < pct < 100 and col.lower().endswith(("date", "_at", "amount", "price")):
            penalty += 5.0
    return round(max(0.0, 100.0 - min(30.0, penalty)), 2)


def _source_clarity(passport: "SourcePassport | None") -> float:
    if passport is None:
        return 0.0
    if not passport.source_id:
        return 25.0
    if not passport.allowed_use:
        return 50.0
    return 100.0


def compute_dq(
    *,
    preview: "ImportPreview",
    duplicates_found: int = 0,
    source_passport: "SourcePassport | None" = None,
) -> DQScore:
    """Weighted: completeness 0.60, duplicate_inverse 0.30, format 0.05,
    source_clarity 0.05."""
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
            "weights": {
                "completeness": 0.60,
                "duplicate_inverse": 0.30,
                "format": 0.05,
                "source": 0.05,
            },
        },
    )


__all__ = [
    "DQScore",
    "account_row_completeness",
    "compute_dq",
    "duplicate_ratio_by_field",
    "mean_completeness",
    "summarize_table_quality",
]
