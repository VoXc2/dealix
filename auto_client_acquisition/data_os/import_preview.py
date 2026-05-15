"""CSV import preview helpers for Data OS router + package-level helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.data_os.pii_detection import column_name_suggests_pii
from auto_client_acquisition.revenue_data_intake.csv_preview import parse_account_csv


def import_preview_csv(csv_text: str, **kwargs: Any) -> dict[str, Any]:
    """Return structured preview; never persists."""
    return parse_account_csv(csv_text, **kwargs)


@dataclass(slots=True)
class ImportPreview:
    columns: list[str]
    row_count: int
    missing_pct: dict[str, float]
    pii_columns: list[str]
    suggested_cleanup: list[str]
    preview_rows: list[dict[str, Any]]


def _missing_pct(rows: list[dict[str, Any]], columns: list[str]) -> dict[str, float]:
    if not rows:
        return dict.fromkeys(columns, 100.0)
    totals = len(rows)
    out: dict[str, float] = {}
    for column in columns:
        missing = 0
        for row in rows:
            value = row.get(column)
            if value is None or (isinstance(value, str) and not value.strip()):
                missing += 1
        out[column] = round((missing / totals) * 100.0, 2)
    return out


def preview(csv_payload: bytes | str, **kwargs: Any) -> ImportPreview:
    """Return normalized preview object expected by `/api/v1/data-os/*` routers."""
    if isinstance(csv_payload, bytes):
        csv_text = csv_payload.decode("utf-8", errors="replace")
    else:
        csv_text = csv_payload

    parsed = parse_account_csv(csv_text, **kwargs)
    columns = list(parsed.get("detected_columns", []))
    rows = list(parsed.get("preview_rows", []))
    missing_pct = _missing_pct(rows, columns)
    pii_columns = [column for column in columns if column_name_suggests_pii(column)]
    suggested_cleanup = [
        f"fill_missing_{column}" for column, pct in missing_pct.items() if pct > 0
    ]

    return ImportPreview(
        columns=columns,
        row_count=int(parsed.get("parsed_row_count", 0)),
        missing_pct=missing_pct,
        pii_columns=pii_columns,
        suggested_cleanup=suggested_cleanup,
        preview_rows=rows,
    )


__all__ = ["ImportPreview", "import_preview_csv", "preview"]
