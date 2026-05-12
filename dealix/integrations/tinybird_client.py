"""
Tinybird embedded analytics — sub-second customer-facing dashboards.

Tinybird is a managed real-time analytics platform. We push events to
their HFI endpoint and query pre-defined Pipes to render charts. When
TINYBIRD_TOKEN is unset, the customer dashboard falls back to the
existing aggregates in `auto_client_acquisition/customer_success/benchmarks.py`.

Reference: https://www.tinybird.co/docs/api-reference
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)

_BASE = os.getenv("TINYBIRD_BASE_URL", "https://api.tinybird.co").rstrip("/")


@dataclass
class TinybirdResult:
    ok: bool
    rows: list[dict[str, Any]]
    error: str | None = None


def is_configured() -> bool:
    return bool(os.getenv("TINYBIRD_TOKEN", "").strip())


def _token() -> str:
    return os.getenv("TINYBIRD_TOKEN", "").strip()


async def push_event(datasource: str, payload: dict[str, Any]) -> bool:
    """Append a JSON row to a Tinybird datasource via HFI."""
    if not is_configured():
        return False
    try:
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.post(
                f"{_BASE}/v0/events",
                params={"name": datasource},
                headers={"Authorization": f"Bearer {_token()}"},
                json=payload,
            )
            r.raise_for_status()
    except Exception:
        log.exception("tinybird_event_failed", datasource=datasource)
        return False
    return True


async def query_pipe(pipe_name: str, params: dict[str, Any]) -> TinybirdResult:
    """Run a Pipe and return its rows."""
    if not is_configured():
        return TinybirdResult(ok=False, rows=[], error="tinybird_disabled")
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(
                f"{_BASE}/v0/pipes/{pipe_name}.json",
                params=params,
                headers={"Authorization": f"Bearer {_token()}"},
            )
            r.raise_for_status()
            data = r.json()
    except Exception as exc:
        log.exception("tinybird_query_failed", pipe=pipe_name)
        return TinybirdResult(ok=False, rows=[], error=str(exc))
    return TinybirdResult(ok=True, rows=data.get("data", []))
