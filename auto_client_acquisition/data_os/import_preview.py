"""CSV import preview — delegates to revenue_data_intake (single source of truth)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.data_os.pii_detection import column_name_suggests_pii
from auto_client_acquisition.revenue_data_intake.csv_preview import parse_account_csv


def import_preview_csv(csv_text: str, **kwargs: Any) -> dict[str, Any]:
    """Return structured preview; never persists."""
    return parse_account_csv(csv_text, **kwargs)


@dataclass(frozen=True, slots=True)
class ImportPreview:
    """Structured preview of an imported CSV — no persistence, no external sends."""

    columns: tuple[str, ...]
    row_count: int
    missing_pct: dict[str, float] = field(default_factory=dict)
    pii_columns: tuple[str, ...] = ()
    suggested_cleanup: tuple[str, ...] = ()


def preview(raw_csv: bytes | str) -> ImportPreview:
    """Parse a CSV blob into an ``ImportPreview`` (columns, row count, PII hints).

    Accepts ``bytes`` or ``str``. Never raises on malformed input — returns an
    empty preview whose ``suggested_cleanup`` carries the parse error.
    """
    text = raw_csv.decode("utf-8", errors="replace") if isinstance(raw_csv, bytes) else raw_csv
    parsed = parse_account_csv(text)
    if "error" in parsed:
        return ImportPreview(columns=(), row_count=0, suggested_cleanup=(str(parsed["error"]),))

    columns = tuple(parsed.get("detected_columns", []))
    rows: list[dict[str, Any]] = parsed.get("preview_rows", [])
    row_count = int(parsed.get("parsed_row_count", 0))

    denom = len(rows) or 1
    missing_pct = {
        c: round(100.0 * sum(1 for r in rows if not str(r.get(c, "")).strip()) / denom, 1)
        for c in columns
    }
    pii_columns = tuple(c for c in columns if column_name_suggests_pii(c))

    cleanup: list[str] = []
    quality = parsed.get("data_quality", {})
    if quality.get("duplicate_ratio_company_name", 0.0) > 0.0:
        cleanup.append("deduplicate_company_name")
    if any(pct > 0.0 for pct in missing_pct.values()):
        cleanup.append("fill_missing_required_fields")
    if pii_columns:
        cleanup.append("review_pii_columns_before_ai_use")

    return ImportPreview(
        columns=columns,
        row_count=row_count,
        missing_pct=missing_pct,
        pii_columns=pii_columns,
        suggested_cleanup=tuple(cleanup),
    )


__all__ = ["ImportPreview", "import_preview_csv", "preview"]
