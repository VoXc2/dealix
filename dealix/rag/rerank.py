"""
Cohere Rerank — top-50 → top-5 with high precision.

Inert (returns the candidate list unchanged) without COHERE_API_KEY.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)

_RERANK_URL = "https://api.cohere.ai/v1/rerank"


@dataclass
class RerankResult:
    index: int
    document: dict[str, Any]
    relevance_score: float


async def rerank(
    query: str, documents: list[dict[str, Any]], *, top_n: int = 5
) -> list[RerankResult]:
    if not documents:
        return []
    key = os.getenv("COHERE_API_KEY", "").strip()
    if not key:
        # Identity passthrough so callers don't branch.
        return [
            RerankResult(index=i, document=d, relevance_score=1.0 - (i * 0.01))
            for i, d in enumerate(documents[:top_n])
        ]
    try:
        async with httpx.AsyncClient(timeout=20) as c:
            r = await c.post(
                _RERANK_URL,
                headers={"Authorization": f"Bearer {key}"},
                json={
                    "model": "rerank-multilingual-v3.0",
                    "query": query,
                    "documents": [d.get("text", "") for d in documents],
                    "top_n": top_n,
                },
            )
            r.raise_for_status()
            data = r.json()
    except Exception:
        log.exception("cohere_rerank_failed")
        return [
            RerankResult(index=i, document=d, relevance_score=1.0 - (i * 0.01))
            for i, d in enumerate(documents[:top_n])
        ]

    return [
        RerankResult(
            index=row["index"],
            document=documents[row["index"]],
            relevance_score=float(row["relevance_score"]),
        )
        for row in data.get("results", [])
    ]
