"""Google Drive integration — ingest client documents into Company Brain.

تكامل Google Drive — جلب مستندات العميل لتغذية عقل الشركة.

Docs: https://developers.google.com/drive/api/v3/reference
Read-oriented: lists files and fetches plain-text content for ingestion.
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
class DriveFile:
    file_id: str
    name: str
    mime_type: str


@dataclass
class DriveResult:
    success: bool
    files: list[DriveFile] = field(default_factory=list)
    text: str = ""
    error: str | None = None


class GoogleDriveClient:
    """Thin async read client for Google Drive (files.list + files.export)."""

    BASE_URL = "https://www.googleapis.com/drive/v3"

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
    async def list_files(self, query: str = "") -> DriveResult:
        """List Drive files (optionally filtered). No-op when unconfigured."""
        if not self.configured:
            return DriveResult(success=False, error="google_drive_not_configured")
        params: dict[str, Any] = {"pageSize": 50, "fields": "files(id,name,mimeType)"}
        if query:
            params["q"] = query
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.get(
                    f"{self.BASE_URL}/files", params=params, headers=self._headers()
                )
                resp.raise_for_status()
                data = resp.json()
            files = [
                DriveFile(
                    file_id=f.get("id", ""),
                    name=f.get("name", ""),
                    mime_type=f.get("mimeType", ""),
                )
                for f in data.get("files", [])
            ]
            logger.info("drive_files_listed", count=len(files))
            return DriveResult(success=True, files=files)
        except Exception as e:  # noqa: BLE001
            logger.exception("drive_list_failed", error=str(e))
            return DriveResult(success=False, error=str(e))

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPStatusError)),
        reraise=True,
    )
    async def fetch_file_text(self, file_id: str) -> DriveResult:
        """Export a Drive document as plain text for Company Brain ingestion."""
        if not self.configured:
            return DriveResult(success=False, error="google_drive_not_configured")
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.get(
                    f"{self.BASE_URL}/files/{file_id}/export",
                    params={"mimeType": "text/plain"},
                    headers=self._headers(),
                )
                resp.raise_for_status()
                text = resp.text
            return DriveResult(success=True, text=text)
        except Exception as e:  # noqa: BLE001
            logger.exception("drive_fetch_failed", error=str(e))
            return DriveResult(success=False, error=str(e))


__all__ = ["DriveFile", "DriveResult", "GoogleDriveClient"]
