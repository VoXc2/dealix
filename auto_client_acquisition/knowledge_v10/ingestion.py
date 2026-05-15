"""Document ingestion — text → chunks → embeddings → store.

Deterministic, paragraph-aware chunking. Embeddings are produced by the
injected ``embed_fn`` (defaults to EmbeddingService.embed_batch). Blocked
source types are rejected up-front by source policy.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from auto_client_acquisition.knowledge_v10.schemas import SourceType
from auto_client_acquisition.knowledge_v10.source_policy import is_source_allowed
from auto_client_acquisition.knowledge_v10.store import (
    KnowledgeChunk,
    KnowledgeStore,
    get_store,
)

_MAX_CHUNK_CHARS = 1000
_MIN_CHUNK_CHARS = 80

BatchEmbedFn = Callable[[list[str]], Awaitable[list[list[float]]]]


def chunk_text(text: str, *, max_chars: int = _MAX_CHUNK_CHARS) -> list[str]:
    """Split text into paragraph-aware, size-capped chunks."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    buf = ""
    for para in paragraphs:
        if buf and len(buf) + len(para) + 2 > max_chars:
            chunks.append(buf)
            buf = ""
        if len(para) > max_chars:
            if buf:
                chunks.append(buf)
                buf = ""
            for i in range(0, len(para), max_chars):
                chunks.append(para[i : i + max_chars])
        else:
            buf = f"{buf}\n\n{para}".strip() if buf else para
    if buf:
        chunks.append(buf)
    kept = [c for c in chunks if len(c) >= _MIN_CHUNK_CHARS]
    if kept:
        return kept
    return [text.strip()] if text.strip() else []


async def _default_embed(texts: list[str]) -> list[list[float]]:
    from core.memory.embedding_service import EmbeddingService

    return await EmbeddingService().embed_batch(texts)


async def ingest_text(
    *,
    document_id: str,
    text: str,
    customer_handle: str = "",
    source_type: SourceType | str = SourceType.INTERNAL_DOC,
    language: str = "ar",
    store: KnowledgeStore | None = None,
    embed_fn: BatchEmbedFn | None = None,
) -> dict[str, Any]:
    """Chunk + embed + persist a document. Returns an ingestion summary."""
    st_value = source_type.value if isinstance(source_type, SourceType) else str(source_type)
    if not is_source_allowed(st_value):
        raise ValueError(f"source_type {st_value!r} is blocked by source policy")

    pieces = chunk_text(text)
    if not pieces:
        return {"document_id": document_id, "chunks": 0, "status": "empty"}

    embed = embed_fn or _default_embed
    vectors = await embed(pieces)

    target = store or get_store()
    chunks = [
        KnowledgeChunk(
            document_id=document_id,
            customer_handle=customer_handle,
            source_type=st_value,
            text=piece,
            embedding=list(vec),
            language=language,
        )
        for piece, vec in zip(pieces, vectors, strict=True)
    ]
    written = await target.add_chunks(chunks)
    return {"document_id": document_id, "chunks": written, "status": "ok"}


__all__ = ["chunk_text", "ingest_text"]
