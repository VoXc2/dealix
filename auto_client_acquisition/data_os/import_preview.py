"""CSV import preview — delegates to revenue_data_intake (single source of truth)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.data_os.pii_detection import column_name_suggests_pii
from auto_client_acquisition.revenue_data_intake.csv_preview import parse_account_csv


def import_preview_csv(csv_text: str, **kwargs: Any) -> dict[str, Any]:
    """Return structured preview; never persists."""
    return parse_account_csv(csv_text, **kwargs)


@dataclass(slots=True)
class ImportPreview:
    """Structured, transport-agnostic CSV preview consumed by the Data OS router."""

    columns: list[str] = field(default_factory=list)
    row_count: int = 0
    missing_pct: dict[str, float] = field(default_factory=dict)
    pii_columns: list[str] = field(default_factory=list)
    suggested_cleanup: list[str] = field(default_factory=list)
    duplicate_ratio: float = 0.0
    error: str = ""


def preview(raw: bytes | bytearray | str) -> ImportPreview:
    """Parse a CSV (bytes or text) into an :class:`ImportPreview`. Never persists."""
    text = (
        raw.decode("utf-8", errors="replace")
        if isinstance(raw, (bytes, bytearray))
        else str(raw)
    )
    parsed = parse_account_csv(text)
    if "error" in parsed:
        return ImportPreview(error=str(parsed["error"]))

    columns = list(parsed.get("detected_columns", []))
    rows: list[dict[str, Any]] = parsed.get("preview_rows", [])
    row_count = int(parsed.get("parsed_row_count", len(rows)))

    missing_pct: dict[str, float] = {}
    for col in columns:
        if not rows:
            missing_pct[col] = 0.0
            continue
        missing = sum(1 for r in rows if not str(r.get(col, "")).strip())
        missing_pct[col] = round(missing / len(rows), 4)

    pii_columns = [c for c in columns if column_name_suggests_pii(c)]

    suggested_cleanup: list[str] = []
    for col, pct in missing_pct.items():
        if pct > 0.2:
            suggested_cleanup.append(f"fill_missing:{col}")

    dq = parsed.get("data_quality", {})
    dup_ratio = float(dq.get("duplicate_ratio_company_name", 0.0))
    if dup_ratio > 0.0:
        suggested_cleanup.append("dedupe:company_name")

    return ImportPreview(
        columns=columns,
        row_count=row_count,
        missing_pct=missing_pct,
        pii_columns=pii_columns,
        suggested_cleanup=suggested_cleanup,
        duplicate_ratio=dup_ratio,
    )
