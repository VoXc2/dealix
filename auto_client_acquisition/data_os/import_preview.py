"""CSV import preview helpers for Data OS router + package utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.data_os.pii_detection import (
    column_name_suggests_pii,
    pii_flags_for_row,
)
from auto_client_acquisition.revenue_data_intake.csv_preview import parse_account_csv


@dataclass(frozen=True, slots=True)
class ImportPreview:
    columns: list[str]
    row_count: int
    missing_pct: dict[str, float] = field(default_factory=dict)
    pii_columns: list[str] = field(default_factory=list)
    suggested_cleanup: list[str] = field(default_factory=list)
    preview_rows: list[dict[str, Any]] = field(default_factory=list)


def import_preview_csv(csv_text: str, **kwargs: Any) -> dict[str, Any]:
    """Return structured preview dict; never persists."""
    return parse_account_csv(csv_text, **kwargs)


def _missing_pct(rows: list[dict[str, Any]], columns: list[str]) -> dict[str, float]:
    if not rows:
        return {c: 100.0 for c in columns}
    out: dict[str, float] = {}
    total = len(rows)
    for c in columns:
        missing = 0
        for r in rows:
            val = r.get(c)
            if val is None or (isinstance(val, str) and not val.strip()):
                missing += 1
        out[c] = round((missing / total) * 100.0, 2)
    return out


def preview(raw_csv: bytes) -> ImportPreview:
    """Router-facing adapter returning typed preview fields."""
    try:
        csv_text = raw_csv.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("csv must be utf-8 encoded") from exc

    parsed = import_preview_csv(csv_text)
    columns = [str(c) for c in parsed.get("detected_columns", [])]
    rows = [r for r in parsed.get("preview_rows", []) if isinstance(r, dict)]
    row_count = int(parsed.get("parsed_row_count", len(rows)) or 0)
    missing_pct = _missing_pct(rows, columns)

    pii_cols: set[str] = {c for c in columns if column_name_suggests_pii(c)}
    for row in rows:
        for flag in pii_flags_for_row(row):
            pii_cols.add(flag.field)

    cleanup: list[str] = []
    for col, pct in missing_pct.items():
        if pct >= 20.0:
            cleanup.append(f"fill_missing:{col}")
    if pii_cols:
        cleanup.append("review_pii_columns_before_ai_use")
    if row_count == 0:
        cleanup.append("empty_dataset")

    return ImportPreview(
        columns=columns,
        row_count=row_count,
        missing_pct=missing_pct,
        pii_columns=sorted(pii_cols),
        suggested_cleanup=cleanup,
        preview_rows=rows,
    )


__all__ = ["ImportPreview", "import_preview_csv", "preview"]
