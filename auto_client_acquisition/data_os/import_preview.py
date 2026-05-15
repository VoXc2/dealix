"""CSV import preview — delegates to revenue_data_intake (single source of truth)."""

from __future__ import annotations

from typing import Any


def import_preview_csv(csv_text: str, **kwargs: Any) -> dict[str, Any]:
    """Return structured preview; never persists."""
    # Imported lazily: a module-level import creates a cycle
    # (csv_preview → data_quality_score → data_os/__init__ → import_preview).
    from auto_client_acquisition.revenue_data_intake.csv_preview import parse_account_csv

    return parse_account_csv(csv_text, **kwargs)
