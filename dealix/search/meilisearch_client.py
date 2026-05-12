"""
Meilisearch — typo-tolerant full-text search across leads / deals /
docs / audit. Tenant-scoped indexes (`leads_{tenant_id}`).

Inert when MEILI_URL is unset; the search router falls back to a
simple ILIKE query against Postgres.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class SearchHit:
    id: str
    type: str
    text: str
    score: float
    metadata: dict[str, Any]


def is_configured() -> bool:
    return bool(os.getenv("MEILI_URL", "").strip())


def _base() -> str:
    return os.getenv("MEILI_URL", "http://localhost:7700").rstrip("/")


def _headers() -> dict[str, str]:
    key = os.getenv("MEILI_API_KEY", "").strip()
    return {"Authorization": f"Bearer {key}"} if key else {}


def _index_name(tenant_id: str, kind: str) -> str:
    safe = "".join(c for c in tenant_id if c.isalnum() or c in "_-")
    return f"{kind}_{safe}"


async def index_document(*, tenant_id: str, kind: str, document: dict[str, Any]) -> bool:
    if not is_configured():
        return False
    index = _index_name(tenant_id, kind)
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(
                f"{_base()}/indexes/{index}/documents",
                headers={**_headers(), "Content-Type": "application/json"},
                json=[document],
            )
            r.raise_for_status()
    except Exception:
        log.exception("meilisearch_index_failed", tenant_id=tenant_id, kind=kind)
        return False
    return True


async def search(
    *, tenant_id: str, kind: str, query: str, limit: int = 20
) -> list[SearchHit]:
    if not is_configured():
        return []
    index = _index_name(tenant_id, kind)
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(
                f"{_base()}/indexes/{index}/search",
                headers={**_headers(), "Content-Type": "application/json"},
                json={"q": query, "limit": min(max(limit, 1), 100)},
            )
            r.raise_for_status()
            data = r.json()
    except Exception:
        log.exception("meilisearch_query_failed", tenant_id=tenant_id, kind=kind)
        return []
    out: list[SearchHit] = []
    for h in data.get("hits", []):
        out.append(
            SearchHit(
                id=str(h.get("id", "")),
                type=kind,
                text=str(h.get("_formatted", {}).get("text") or h.get("text") or h.get("company_name") or ""),
                score=float(h.get("_score") or 0.0),
                metadata=h,
            )
        )
    return out
