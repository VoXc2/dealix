"""
Letta (formerly MemGPT) — long-term agent memory with hierarchical
working / archival storage.

Used by long-running agents (customer-success watcher, renewal
forecaster) to remember per-customer state across sessions.

Reference: https://docs.letta.com/api-reference
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class MemoryEntry:
    text: str
    score: float


def is_enabled() -> bool:
    return bool(os.getenv("LETTA_URL", "").strip())


def _headers() -> dict[str, str]:
    token = os.getenv("LETTA_API_TOKEN", "").strip()
    return {"Authorization": f"Bearer {token}"} if token else {}


async def ping() -> bool:
    url = os.getenv("LETTA_URL", "").strip()
    if not url:
        return False
    try:
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.get(f"{url.rstrip('/')}/v1/health", headers=_headers())
            r.raise_for_status()
        return True
    except Exception:
        log.exception("letta_ping_failed")
        return False


async def insert_memory(*, agent_id: str, text: str) -> bool:
    url = os.getenv("LETTA_URL", "").strip()
    if not url or not text:
        return False
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(
                f"{url.rstrip('/')}/v1/agents/{agent_id}/archival/text",
                headers=_headers(),
                json={"text": text},
            )
            r.raise_for_status()
        return True
    except Exception:
        log.exception("letta_insert_failed", agent_id=agent_id)
        return False


async def recall(*, agent_id: str, query: str, top_n: int = 5) -> list[MemoryEntry]:
    url = os.getenv("LETTA_URL", "").strip()
    if not url:
        return []
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(
                f"{url.rstrip('/')}/v1/agents/{agent_id}/archival/search",
                headers=_headers(),
                json={"query": query, "top_k": top_n},
            )
            r.raise_for_status()
            data = r.json()
    except Exception:
        log.exception("letta_recall_failed", agent_id=agent_id)
        return []
    return [
        MemoryEntry(text=str(e.get("text") or ""), score=float(e.get("score") or 0.0))
        for e in data.get("results", [])
    ]
