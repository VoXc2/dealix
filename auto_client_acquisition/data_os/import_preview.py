"""CSV import preview.

Two surfaces:

- ``import_preview_csv`` — dict preview that delegates to
  ``revenue_data_intake`` (single source of truth for parsing).
- ``preview`` — a typed ``CSVPreview`` used by the Data OS router
  (``/api/v1/data-os/import-preview``): columns, row count, per-column
  missing %, heuristic PII columns, and suggested cleanup actions.

Nothing here persists the uploaded data.
"""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.data_os.pii_detection import column_name_suggests_pii
from auto_client_acquisition.revenue_data_intake.csv_preview import parse_account_csv

_MAX_ROWS = 500


def import_preview_csv(csv_text: str, **kwargs: Any) -> dict[str, Any]:
    """Return structured preview; never persists."""
    return parse_account_csv(csv_text, **kwargs)


@dataclass(frozen=True, slots=True)
class CSVPreview:
    """Typed preview of an uploaded CSV (no rows retained)."""

    columns: tuple[str, ...]
    row_count: int
    missing_pct: dict[str, float]
    pii_columns: tuple[str, ...]
    suggested_cleanup: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "columns": list(self.columns),
            "row_count": self.row_count,
            "missing_pct": dict(self.missing_pct),
            "pii_columns": list(self.pii_columns),
            "suggested_cleanup": list(self.suggested_cleanup),
        }


def preview(raw: bytes | str) -> CSVPreview:
    """Parse a CSV upload into a typed, non-persisted preview."""
    text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else raw
    reader = csv.DictReader(io.StringIO(text))
    columns = tuple(f.strip() for f in (reader.fieldnames or []) if f and f.strip())

    rows: list[dict[str, str]] = []
    for i, row in enumerate(reader):
        if i >= _MAX_ROWS:
            break
        rows.append(
            {
                str(k).strip(): (v.strip() if isinstance(v, str) else "")
                for k, v in row.items()
                if k
            },
        )

    row_count = len(rows)
    missing_pct: dict[str, float] = {}
    for col in columns:
        if row_count == 0:
            missing_pct[col] = 0.0
            continue
        missing = sum(1 for r in rows if not r.get(col, "").strip())
        missing_pct[col] = round(100.0 * missing / row_count, 2)

    pii_columns = tuple(c for c in columns if column_name_suggests_pii(c))

    cleanup: list[str] = []
    if not columns:
        cleanup.append("no_header_row_detected")
    for col, pct in missing_pct.items():
        if pct >= 50.0:
            cleanup.append(f"high_missing_rate:{col}:{pct}%")
    if len(columns) != len({c.lower() for c in columns}):
        cleanup.append("duplicate_column_headers")
    for col in pii_columns:
        cleanup.append(f"pii_column_needs_source_passport:{col}")

    return CSVPreview(
        columns=columns,
        row_count=row_count,
        missing_pct=missing_pct,
        pii_columns=pii_columns,
        suggested_cleanup=tuple(cleanup),
    )


__all__ = ["CSVPreview", "import_preview_csv", "preview"]
