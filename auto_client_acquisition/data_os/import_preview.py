"""CSV import preview — delegates parsing to revenue_data_intake (single
source of truth) and shapes a structured ``CSVPreview`` for the Data OS API.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.data_os.pii_detection import column_name_suggests_pii
from auto_client_acquisition.revenue_data_intake.csv_preview import parse_account_csv


@dataclass(frozen=True, slots=True)
class CSVPreview:
    columns: tuple[str, ...] = ()
    row_count: int = 0
    missing_pct: dict[str, float] = field(default_factory=dict)
    pii_columns: tuple[str, ...] = ()
    suggested_cleanup: tuple[str, ...] = ()
    duplicate_ratio: float = 0.0
    error: str = ""


def import_preview_csv(csv_text: str, **kwargs: Any) -> dict[str, Any]:
    """Return raw structured preview dict; never persists."""
    return parse_account_csv(csv_text, **kwargs)


def _missing_pct(rows: list[dict[str, Any]], columns: list[str]) -> dict[str, float]:
    out: dict[str, float] = {}
    total = len(rows) or 1
    for col in columns:
        empty = sum(
            1
            for r in rows
            if not str(r.get(col, "") or "").strip()
        )
        out[col] = round(100.0 * empty / total, 1)
    return out


def preview(raw: bytes | str) -> CSVPreview:
    """Parse a CSV payload (bytes or str) into a structured ``CSVPreview``."""
    text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else raw
    parsed = parse_account_csv(text)

    if "error" in parsed:
        return CSVPreview(error=str(parsed["error"]))

    columns: list[str] = list(parsed.get("detected_columns", []))
    rows: list[dict[str, Any]] = list(parsed.get("preview_rows", []))
    row_count = int(parsed.get("parsed_row_count", len(rows)))
    quality = parsed.get("data_quality", {})

    missing = _missing_pct(rows, columns)
    pii_cols = tuple(c for c in columns if column_name_suggests_pii(c))
    dup_ratio = float(quality.get("duplicate_ratio_company_name", 0.0))

    cleanup: list[str] = []
    for col, pct in missing.items():
        if pct >= 20.0:
            cleanup.append(f"fill_missing:{col} ({pct}% empty)")
    if dup_ratio > 0.0:
        cleanup.append(f"deduplicate_rows ({round(dup_ratio * 100, 1)}% duplicates)")
    if pii_cols:
        cleanup.append(f"review_pii_columns:{','.join(pii_cols)}")
    if "company_name" not in columns and "company" not in columns:
        cleanup.append("add_company_name_column")

    return CSVPreview(
        columns=tuple(columns),
        row_count=row_count,
        missing_pct=missing,
        pii_columns=pii_cols,
        suggested_cleanup=tuple(cleanup),
        duplicate_ratio=dup_ratio,
    )


__all__ = ["CSVPreview", "import_preview_csv", "preview"]
