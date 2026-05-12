"""
BetterStack (Better Uptime) — heartbeat poster + status JSON reader.

We post a heartbeat to BETTERSTACK_HEARTBEAT_URL every N seconds from
the FastAPI lifespan; BetterStack downgrades to "down" if it stops.
Public status page lives at status.dealix.me (BetterStack-hosted) and
the trust page on landing reads BETTERSTACK_STATUS_URL JSON to render
the live pill when configured (else it falls back to /api/v1/status).

Reference: https://docs.betterstack.com/uptime/heartbeats
"""

from __future__ import annotations

import asyncio
import os
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)


def heartbeat_url() -> str:
    return os.getenv("BETTERSTACK_HEARTBEAT_URL", "").strip()


def status_url() -> str:
    return os.getenv("BETTERSTACK_STATUS_URL", "").strip()


def heartbeat_interval_seconds() -> int:
    try:
        return max(30, int(os.getenv("BETTERSTACK_HEARTBEAT_INTERVAL_S", "60")))
    except ValueError:
        return 60


async def send_heartbeat(client: httpx.AsyncClient | None = None) -> bool:
    """POST a heartbeat once. Returns True on 2xx."""
    url = heartbeat_url()
    if not url:
        return False
    own = client is None
    if client is None:
        client = httpx.AsyncClient(timeout=5)
    try:
        try:
            r = await client.get(url)
            return 200 <= r.status_code < 300
        except Exception:
            log.exception("betterstack_heartbeat_failed")
            return False
    finally:
        if own:
            await client.aclose()


async def heartbeat_loop(stop_event: asyncio.Event) -> None:
    """Long-running heartbeat poster. Exit when stop_event is set.

    Designed to run as a background task spawned from FastAPI lifespan.
    Logs once when starting and once when stopping; otherwise silent
    unless heartbeats fail. Safe to start when BETTERSTACK_HEARTBEAT_URL
    is unset — it returns immediately.
    """
    url = heartbeat_url()
    if not url:
        log.info("betterstack_heartbeat_skipped", reason="unconfigured")
        return
    interval = heartbeat_interval_seconds()
    log.info("betterstack_heartbeat_started", interval_s=interval)
    async with httpx.AsyncClient(timeout=5) as client:
        while not stop_event.is_set():
            ok = await send_heartbeat(client)
            if not ok:
                log.warning("betterstack_heartbeat_dropped")
            try:
                await asyncio.wait_for(stop_event.wait(), timeout=interval)
            except asyncio.TimeoutError:
                continue
    log.info("betterstack_heartbeat_stopped")


async def fetch_status() -> dict[str, Any]:
    """Fetch the public status JSON (for the trust page).

    Returns the BetterStack response (or `{}` on failure / unconfigured).
    Caller is expected to render gracefully on `{}`.
    """
    url = status_url()
    if not url:
        return {}
    try:
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.get(url)
            r.raise_for_status()
            return r.json()
    except Exception:
        log.exception("betterstack_status_fetch_failed")
        return {}
