"""CSV import preview — delegates to revenue_data_intake (single source of truth)."""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.revenue_data_intake.csv_preview import parse_account_csv


def import_preview_csv(csv_text: str, **kwargs: Any) -> dict[str, Any]:
    """Return structured preview; never persists."""
    return parse_account_csv(csv_text, **kwargs)
