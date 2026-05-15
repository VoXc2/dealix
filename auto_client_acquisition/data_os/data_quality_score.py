"""Lightweight data quality metrics for account-style rows (dicts)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from auto_client_acquisition.data_os.import_preview import CSVPreview
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


@dataclass(frozen=True, slots=True)
class DQScore:
    """Data Quality Score for the 1,500 SAR Data Pack offer (0-100)."""

    overall: float
    completeness: float
    duplicate_inverse: float
    format_consistency: float
    source_clarity: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "overall": self.overall,
            "completeness": self.completeness,
            "duplicate_inverse": self.duplicate_inverse,
            "format_consistency": self.format_consistency,
            "source_clarity": self.source_clarity,
        }


def _clamp(value: float) -> float:
    return round(max(0.0, min(100.0, value)), 1)


def compute_dq(
    *,
    preview: CSVPreview,
    duplicates_found: int = 0,
    source_passport: SourcePassport | None = None,
) -> DQScore:
    """Score an uploaded table across four deterministic dimensions.

    - completeness     — inverse of mean per-column missing %.
    - duplicate_inverse — inverse of the duplicate-row rate.
    - format_consistency — penalised per suggested cleanup action.
    - source_clarity   — driven by Source Passport presence + validity.
    """
    missing_values = list(preview.missing_pct.values())
    mean_missing = sum(missing_values) / len(missing_values) if missing_values else 0.0
    completeness = _clamp(100.0 - mean_missing)

    row_count = max(preview.row_count, 1)
    dup_rate = min(1.0, max(0, duplicates_found) / row_count)
    duplicate_inverse = _clamp(100.0 * (1.0 - dup_rate))

    pii_cleanups = sum(
        1 for c in preview.suggested_cleanup if c.startswith("pii_column")
    )
    other_cleanups = len(preview.suggested_cleanup) - pii_cleanups
    format_consistency = _clamp(100.0 - 8.0 * other_cleanups)

    if source_passport is None:
        source_clarity = 40.0
    else:
        from auto_client_acquisition.sovereignty_os.source_passport_standard import (
            source_passport_valid_for_ai,
        )

        ok, _errors = source_passport_valid_for_ai(source_passport)
        source_clarity = 100.0 if ok else 60.0

    overall = _clamp(
        0.40 * completeness
        + 0.25 * duplicate_inverse
        + 0.20 * format_consistency
        + 0.15 * source_clarity,
    )
    return DQScore(
        overall=overall,
        completeness=completeness,
        duplicate_inverse=duplicate_inverse,
        format_consistency=format_consistency,
        source_clarity=source_clarity,
    )
