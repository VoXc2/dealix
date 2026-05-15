"""Google Sheets integration — read tabular client data.

تكامل Google Sheets — قراءة بيانات العميل الجدولية.

Docs: https://developers.google.com/sheets/api/reference/rest
Read-oriented: pulls a value range for import into Data OS / Company Brain.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from core.config.settings import get_settings
from core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class SheetsResult:
    success: bool
    rows: list[list[str]] = field(default_factory=list)
    error: str | None = None

    @property
    def row_count(self) -> int:
        return len(self.rows)


class GoogleSheetsClient:
    """Thin async read client for the Google Sheets values API."""

    BASE_URL = "https://sheets.googleapis.com/v4/spreadsheets"

    def __init__(self) -> None:
        self.settings = get_settings()

    @property
    def configured(self) -> bool:
        return self.settings.google_workspace_token is not None

    def _headers(self) -> dict[str, str]:
        token = self.settings.google_workspace_token.get_secret_value()  # type: ignore[union-attr]
        return {"Authorization": f"Bearer {token}"}

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPStatusError)),
        reraise=True,
    )
    async def read_range(self, spreadsheet_id: str, a1_range: str = "A1:Z200") -> SheetsResult:
        """Read a value range as a list of string rows. No-op when unconfigured."""
        if not self.configured:
            return SheetsResult(success=False, error="google_sheets_not_configured")
        if not spreadsheet_id.strip():
            return SheetsResult(success=False, error="spreadsheet_id_required")
        url = f"{self.BASE_URL}/{spreadsheet_id}/values/{a1_range}"
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.get(url, headers=self._headers())
                resp.raise_for_status()
                data: dict[str, Any] = resp.json()
            rows = [
                [str(cell) for cell in row]
                for row in data.get("values", [])
            ]
            logger.info("sheets_range_read", rows=len(rows))
            return SheetsResult(success=True, rows=rows)
        except Exception as e:  # noqa: BLE001
            logger.exception("sheets_read_failed", error=str(e))
            return SheetsResult(success=False, error=str(e))


__all__ = ["GoogleSheetsClient", "SheetsResult"]
