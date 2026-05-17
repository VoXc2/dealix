"""Base adapter — shared constructors for AdapterResult."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.assurance_os.models import AdapterResult, Status


class BaseAdapter:
    """All adapters inherit this. ``source`` names the underlying module."""

    source: str = "unwired"

    def ok(self, value: Any, detail: str = "") -> AdapterResult:
        return AdapterResult(Status.OK, value, self.source, detail)

    def unknown(self, detail: str = "source not wired / no data") -> AdapterResult:
        return AdapterResult(Status.UNKNOWN, None, self.source, detail)

    def error(self, detail: str) -> AdapterResult:
        return AdapterResult(Status.ERROR, None, self.source, detail)
