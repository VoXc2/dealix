"""CSV import preview — delegates to revenue_data_intake (single source of truth)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.data_os.pii_detection import column_name_suggests_pii
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
    rows: tuple[dict[str, Any], ...]


def preview(raw_csv: bytes, **kwargs: Any) -> ImportPreview:
    text = raw_csv.decode("utf-8")
    parsed = parse_account_csv(text, **kwargs)
    if parsed.get("error"):
        return ImportPreview(
            columns=(),
            row_count=0,
            missing_pct={},
            pii_columns=(),
            suggested_cleanup=(str(parsed["error"]),),
            rows=(),
        )
    rows = tuple(parsed.get("preview_rows", []))
    columns = tuple(parsed.get("detected_columns", []))
    row_count = int(parsed.get("parsed_row_count", 0))
    missing_pct: dict[str, float] = {}
    if row_count > 0:
        for col in columns:
            missing = 0
            for row in rows:
                value = row.get(col)
                if value is None or (isinstance(value, str) and not value.strip()):
                    missing += 1
            missing_pct[col] = round(missing / row_count, 4)
    pii_columns = tuple(col for col in columns if column_name_suggests_pii(col))
    cleanup: list[str] = []
    for required in ("company_name", "sector", "city"):
        if required not in columns:
            cleanup.append(f"missing_required_column:{required}")
    if not cleanup and row_count == 0:
        cleanup.append("no_rows_found")
    return ImportPreview(
        columns=columns,
        row_count=row_count,
        missing_pct=missing_pct,
        pii_columns=pii_columns,
        suggested_cleanup=tuple(cleanup),
        rows=rows,
    )


__all__ = ["ImportPreview", "import_preview_csv", "preview"]
