"""
mem0 — alternative agent memory backend. Used when Letta is unavailable
or the founder prefers the mem0 hosted plan.

Reference: https://docs.mem0.ai
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class Mem0Result:
    items: list[dict[str, str]]
    provider: str


def is_enabled() -> bool:
    return bool(os.getenv("MEM0_API_KEY", "").strip())


async def search(*, user_id: str, query: str, top_n: int = 5) -> Mem0Result:
    if not is_enabled():
        return Mem0Result(items=[], provider="none")
    try:
        from mem0 import MemoryClient  # type: ignore
    except ImportError:
        log.info("mem0_sdk_not_installed")
        return Mem0Result(items=[], provider="none")
    try:
        client = MemoryClient(api_key=os.getenv("MEM0_API_KEY"))
        results = client.search(query=query, user_id=user_id, limit=top_n)
    except Exception:
        log.exception("mem0_search_failed", user_id=user_id)
        return Mem0Result(items=[], provider="mem0")
    return Mem0Result(
        items=[{"text": str(r.get("memory") or "")} for r in (results or [])],
        provider="mem0",
    )
