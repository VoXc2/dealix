"""Retrieval — cosine search over the knowledge store.

One ``retrieve()`` interface; the backend (JSONL or pgvector) is chosen by
DEALIX_KNOWLEDGE_BACKEND via ``store.get_store()``. Blocked source types are
dropped from BOTH the request and every result, so a backend can never
surface a denied source. Snippets are PII-redacted before they leave.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from auto_client_acquisition.customer_data_plane.pii_redactor import (
    redact_email,
    redact_phone,
    redact_saudi_id,
)
from auto_client_acquisition.knowledge_v10.schemas import (
    RetrievalRequest,
    RetrievalResult,
)
from auto_client_acquisition.knowledge_v10.source_policy import is_source_allowed
from auto_client_acquisition.knowledge_v10.store import KnowledgeStore, get_store
from core.memory.embedding_service import cosine_similarity

QueryEmbedFn = Callable[[str], Awaitable[list[float]]]


async def _default_embed(text: str) -> list[float]:
    from core.memory.embedding_service import EmbeddingService

    return await EmbeddingService().embed(text)


def _redact(text: str) -> str:
    return redact_saudi_id(redact_phone(redact_email(text)))


async def retrieve(
    req: RetrievalRequest,
    *,
    store: KnowledgeStore | None = None,
    embed_fn: QueryEmbedFn | None = None,
) -> list[RetrievalResult]:
    """Return tenant-scoped, source-filtered, cosine-ranked chunks.

    Returns ``[]`` when no allowed sources are requested or nothing is indexed.
    """
    allowed = {
        (s.value if hasattr(s, "value") else str(s))
        for s in req.allowed_sources
        if is_source_allowed(s)
    }
    if not allowed:
        return []

    target = store or get_store()
    chunks = await target.iter_chunks(customer_handle=req.customer_handle or None)
    if not chunks:
        return []

    embed = embed_fn or _default_embed
    query_vec = await embed(req.query)
    if not query_vec:
        return []

    scored: list[tuple[float, object]] = []
    for c in chunks:
        if c.source_type not in allowed or not is_source_allowed(c.source_type):
            continue
        if not c.embedding:
            continue
        scored.append((cosine_similarity(query_vec, c.embedding), c))

    scored.sort(key=lambda x: x[0], reverse=True)

    results: list[RetrievalResult] = []
    for score, c in scored[: req.top_k]:
        results.append(
            RetrievalResult(
                chunk_id=c.chunk_id,
                document_id=c.document_id,
                snippet_redacted=_redact(c.text[:500]),
                score=max(0.0, min(1.0, score)),
                source_type=c.source_type,
            )
        )
    return results
