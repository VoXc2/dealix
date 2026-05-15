"""CSV import preview helpers.

Two compatibility surfaces are kept:
- ``import_preview_csv(csv_text: str) -> dict`` for helper callers.
- ``preview(raw: bytes) -> ImportPreview`` for Data OS router callers.
"""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.revenue_data_intake.csv_preview import parse_account_csv


def import_preview_csv(csv_text: str, **kwargs: Any) -> dict[str, Any]:
    """Return structured preview; never persists."""
    return parse_account_csv(csv_text, **kwargs)


@dataclass(frozen=True, slots=True)
class ImportPreview:
    columns: tuple[str, ...]
    row_count: int
    missing_pct: dict[str, float]
    pii_columns: tuple[str, ...]
    suggested_cleanup: tuple[str, ...]


def preview(raw: bytes, *, max_rows: int = 500) -> ImportPreview:
    """Parse raw CSV bytes into an object-like preview used by routers."""
    text = raw.decode("utf-8", errors="ignore")
    stream = io.StringIO(text)
    reader = csv.DictReader(stream)
    if not reader.fieldnames:
        return ImportPreview(
            columns=(),
            row_count=0,
            missing_pct={},
            pii_columns=(),
            suggested_cleanup=("no_header_row",),
        )

    columns = tuple(str(c).strip() for c in reader.fieldnames if c)
    rows: list[dict[str, str]] = []
    for i, row in enumerate(reader):
        if i >= max_rows:
            break
        normalized = {
            str(k).strip(): (str(v).strip() if v is not None else "")
            for k, v in row.items()
            if k
        }
        rows.append(normalized)

    missing_pct: dict[str, float] = {}
    if rows:
        n = float(len(rows))
        for c in columns:
            missing = 0
            for r in rows:
                if not str(r.get(c, "")).strip():
                    missing += 1
            missing_pct[c] = round((missing / n) * 100.0, 2)
    else:
        missing_pct = {c: 100.0 for c in columns}

    pii_columns: list[str] = []
    for c in columns:
        lc = c.lower()
        if any(k in lc for k in ("email", "phone", "mobile", "name")):
            pii_columns.append(c)

    suggested_cleanup: list[str] = []
    if "company_name" not in {c.lower() for c in columns} and "company" in {
        c.lower() for c in columns
    }:
        suggested_cleanup.append("rename_company_to_company_name")
    if "source" not in {c.lower() for c in columns}:
        suggested_cleanup.append("add_source_column")

    return ImportPreview(
        columns=columns,
        row_count=len(rows),
        missing_pct=missing_pct,
        pii_columns=tuple(pii_columns),
        suggested_cleanup=tuple(suggested_cleanup),
    )
