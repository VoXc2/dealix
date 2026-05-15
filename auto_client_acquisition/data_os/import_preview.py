"""CSV import preview.

Two coexisting surfaces:
- ``import_preview_csv`` — delegates to ``revenue_data_intake`` (the
  single source of truth for the new account-CSV pipeline).
- ``ImportPreview`` / ``preview`` — the structured dataclass surface
  consumed by the Data OS router, delivery sprint, and the DQ score.
"""

from __future__ import annotations

import csv
import io
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from auto_client_acquisition.customer_data_plane.pii_redactor import (
    redact_email,
    redact_phone,
    redact_saudi_id,
)
from auto_client_acquisition.revenue_data_intake.csv_preview import parse_account_csv


def import_preview_csv(csv_text: str, **kwargs: Any) -> dict[str, Any]:
    """Return structured preview; never persists."""
    return parse_account_csv(csv_text, **kwargs)


# Heuristic column names that almost always contain PII.
_PII_COLUMN_HINTS = frozenset(
    {
        "email", "e-mail", "mail", "phone", "mobile", "msisdn", "whatsapp",
        "national_id", "iqama", "saudi_id", "id_number",
        "البريد", "الجوال", "الهاتف", "الهوية",
    }
)


@dataclass
class ImportPreview:
    columns: tuple[str, ...]
    row_count: int
    missing_pct: dict[str, float]
    pii_columns: tuple[str, ...]
    suggested_cleanup: tuple[str, ...]
    sample: tuple[dict[str, Any], ...] = field(default_factory=tuple)


def _detect_pii_columns(columns: Iterable[str], rows: list[dict[str, Any]]) -> list[str]:
    out: list[str] = []
    for col in columns:
        lc = col.strip().lower()
        if lc in _PII_COLUMN_HINTS:
            out.append(col)
            continue
        for row in rows[:50]:
            cell = str(row.get(col, "") or "")
            if cell and (
                cell != redact_email(cell)
                or cell != redact_phone(cell)
                or cell != redact_saudi_id(cell)
            ):
                out.append(col)
                break
    return out


def _missing_pct(columns: Iterable[str], rows: list[dict[str, Any]]) -> dict[str, float]:
    if not rows:
        return dict.fromkeys(columns, 0.0)
    total = len(rows)
    out: dict[str, float] = {}
    for col in columns:
        empty = sum(1 for r in rows if not str(r.get(col, "") or "").strip())
        out[col] = round(100.0 * empty / total, 2)
    return out


def _suggest_cleanup(missing: dict[str, float], pii_cols: list[str]) -> list[str]:
    out: list[str] = []
    for col, pct in missing.items():
        if pct >= 30.0:
            out.append(f"high_missing:{col}:{pct}%")
        elif pct >= 10.0:
            out.append(f"medium_missing:{col}:{pct}%")
    for col in pii_cols:
        out.append(f"pii_column:{col}:gate_for_approval")
    return out


def preview(source: Path | str | Iterable[dict[str, Any]] | bytes) -> ImportPreview:
    """Read a CSV file, raw CSV bytes, or an iterable of dicts and return a
    preview. PII columns flagged. Suggested cleanup ranked."""
    rows: list[dict[str, Any]]
    if isinstance(source, (str, Path)):
        path = Path(source)
        with path.open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
    elif isinstance(source, bytes):
        rows = list(csv.DictReader(io.StringIO(source.decode("utf-8"))))
    else:
        rows = list(source)

    columns = tuple(rows[0].keys()) if rows else ()
    pii_cols = _detect_pii_columns(columns, rows)
    missing = _missing_pct(columns, rows)
    cleanup = _suggest_cleanup(missing, pii_cols)

    return ImportPreview(
        columns=columns,
        row_count=len(rows),
        missing_pct=missing,
        pii_columns=tuple(pii_cols),
        suggested_cleanup=tuple(cleanup),
        sample=tuple(rows[:5]),
    )


__all__ = ["ImportPreview", "import_preview_csv", "preview"]
