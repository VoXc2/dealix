"""
Vector + rerank search against the knowledge_chunks table.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class SearchHit:
    chunk_id: str
    document_id: str
    text: str
    similarity: float
    rerank_score: float
    metadata: dict[str, Any]


async def search(
    *,
    tenant_id: str,
    query: str,
    top_n: int = 5,
    candidate_pool: int = 25,
) -> list[SearchHit]:
    """Return top-N hits. Reranks the candidate pool via Cohere when configured."""
    from sqlalchemy import text as sql_text

    from dealix.rag.embeddings import embed
    from dealix.rag.rerank import rerank
    from db.session import async_session_factory

    q = await embed(query, input_type="search_query")
    if not q.vector:
        return []

    rows: list[dict[str, Any]] = []
    try:
        async with async_session_factory()() as session:
            # Cosine distance ORDER via pgvector `<->` operator on the
            # `embedding` column. Returns the raw similarity (1 - dist).
            result = await session.execute(
                sql_text(
                    """
                    SELECT id, document_id, text, metadata,
                           1 - (embedding <=> :qvec) AS similarity
                    FROM knowledge_chunks
                    WHERE tenant_id = :tid
                    ORDER BY embedding <=> :qvec
                    LIMIT :pool
                    """
                ),
                {"qvec": q.vector, "tid": tenant_id, "pool": candidate_pool},
            )
            rows = [dict(r._mapping) for r in result]
    except Exception:
        log.exception("knowledge_search_db_failed", tenant_id=tenant_id)
        return []

    if not rows:
        return []

    reranked = await rerank(query, rows, top_n=top_n)
    return [
        SearchHit(
            chunk_id=str(r.document.get("id")),
            document_id=str(r.document.get("document_id")),
            text=str(r.document.get("text") or ""),
            similarity=float(r.document.get("similarity") or 0.0),
            rerank_score=r.relevance_score,
            metadata=dict(r.document.get("metadata") or {}),
        )
        for r in reranked
    ]
