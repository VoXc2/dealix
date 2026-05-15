"""CSV import preview — delegates to revenue_data_intake (single source of truth)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.revenue_data_intake.csv_preview import parse_account_csv


@dataclass(slots=True)
class ImportPreview:
    columns: list[str]
    row_count: int
    missing_pct: dict[str, float]
    pii_columns: list[str]
    suggested_cleanup: list[str]


def import_preview_csv(csv_text: str, **kwargs: Any) -> dict[str, Any]:
    """Return structured preview; never persists."""
    return parse_account_csv(csv_text, **kwargs)


def preview(raw_csv: bytes | str, **kwargs: Any) -> ImportPreview:
    """Compatibility wrapper used by Data OS router and delivery sprint."""
    csv_text = raw_csv.decode("utf-8") if isinstance(raw_csv, (bytes, bytearray)) else str(raw_csv)
    parsed = parse_account_csv(csv_text, **kwargs)
    if parsed.get("error"):
        raise ValueError(str(parsed["error"]))
    columns = list(parsed.get("detected_columns", []))
    rows = list(parsed.get("preview_rows", []))
    row_count = int(parsed.get("parsed_row_count", 0))

    missing_pct: dict[str, float] = {}
    if row_count > 0:
        for col in columns:
            missing = 0
            for row in rows:
                value = row.get(col)
                if value is None or (isinstance(value, str) and not value.strip()):
                    missing += 1
            # Fallback to preview rows ratio; deterministic and cheap.
            base = len(rows) if rows else row_count
            missing_pct[col] = round((missing / base) * 100.0, 2)
    pii_markers = ("email", "phone", "mobile", "contact")
    pii_columns = [col for col in columns if any(marker in col.lower() for marker in pii_markers)]
    suggested_cleanup: list[str] = []
    for col, pct in missing_pct.items():
        if pct > 30.0:
            suggested_cleanup.append(f"fill_missing_values:{col}")
    if pii_columns:
        suggested_cleanup.append("review_pii_columns_before_external_use")
    return ImportPreview(
        columns=columns,
        row_count=row_count,
        missing_pct=missing_pct,
        pii_columns=pii_columns,
        suggested_cleanup=suggested_cleanup,
    )


__all__ = ["ImportPreview", "import_preview_csv", "preview"]
