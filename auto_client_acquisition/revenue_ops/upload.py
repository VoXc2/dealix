"""CRM / data file intake for the Revenue Ops Diagnostic.

Reuses `data_os.import_preview_csv` (single source of truth for CSV preview).
Intake is preview-only: it never persists customer data and never sends.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.data_os import import_preview_csv


@dataclass(frozen=True)
class UploadResult:
    """Structured preview of an intaken CRM/data file. Never persisted."""

    ok: bool
    row_count: int
    columns: tuple[str, ...] = ()
    pii_columns: tuple[str, ...] = ()
    error: str | None = None
    preview: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "row_count": self.row_count,
            "columns": list(self.columns),
            "pii_columns": list(self.pii_columns),
            "error": self.error,
            "preview": dict(self.preview),
        }


def intake_csv(csv_text: str) -> UploadResult:
    """Preview a CRM/data CSV for the diagnostic.

    Args:
        csv_text: raw CSV content (decoded text).

    Returns:
        An `UploadResult`. On a parse error `ok` is `False` and `error` is set.
    """
    if not csv_text or not csv_text.strip():
        return UploadResult(ok=False, row_count=0, error="empty_csv")

    parsed = import_preview_csv(csv_text)
    if parsed.get("error"):
        return UploadResult(
            ok=False,
            row_count=0,
            error=str(parsed["error"]),
            preview=parsed,
        )

    columns = tuple(
        parsed.get("detected_columns") or parsed.get("columns") or ()
    )
    pii_columns = tuple(
        parsed.get("pii_columns") or parsed.get("pii_suspected_columns") or ()
    )
    row_count = int(
        parsed.get("row_count")
        or parsed.get("total_rows")
        or len(parsed.get("preview_rows") or [])
    )
    return UploadResult(
        ok=True,
        row_count=row_count,
        columns=columns,
        pii_columns=pii_columns,
        preview=parsed,
    )
