"""Lightweight data quality metrics for account-style rows (dicts)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover - typing only
    from auto_client_acquisition.data_os.import_preview import ImportPreview
    from auto_client_acquisition.sovereignty_os.source_passport_standard import (
        SourcePassport,
    )


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
class DataQualityScore:
    """Composite Data Quality Score (0-100) for the 1,500 SAR Data Pack."""

    overall: float
    completeness: float
    duplicate_inverse: float
    format_consistency: float
    source_clarity: float


def compute_dq(
    *,
    preview: ImportPreview,
    duplicates_found: int = 0,
    source_passport: SourcePassport | None = None,
) -> DataQualityScore:
    """Composite DQ score from an :class:`ImportPreview` and optional passport.

    All sub-scores are on a 0-100 scale. ``overall`` is a weighted blend that
    favours completeness, then de-duplication, source clarity, and format.
    """
    missing = preview.missing_pct
    if missing:
        completeness = 100.0 * (1.0 - sum(missing.values()) / len(missing))
    else:
        completeness = 100.0 if preview.row_count else 0.0

    dup_ratio = float(getattr(preview, "duplicate_ratio", 0.0))
    if duplicates_found and preview.row_count:
        dup_ratio = max(dup_ratio, duplicates_found / preview.row_count)
    duplicate_inverse = 100.0 * (1.0 - min(1.0, max(0.0, dup_ratio)))

    format_consistency = 100.0 if preview.columns else 0.0

    if source_passport is None:
        source_clarity = 25.0
    else:
        from auto_client_acquisition.sovereignty_os.source_passport_standard import (
            source_passport_valid_for_ai,
        )

        ok, _errors = source_passport_valid_for_ai(source_passport)
        source_clarity = 100.0 if ok else 50.0

    overall = (
        0.40 * completeness
        + 0.25 * duplicate_inverse
        + 0.15 * format_consistency
        + 0.20 * source_clarity
    )
    return DataQualityScore(
        overall=round(overall, 1),
        completeness=round(completeness, 1),
        duplicate_inverse=round(duplicate_inverse, 1),
        format_consistency=round(format_consistency, 1),
        source_clarity=round(source_clarity, 1),
    )
