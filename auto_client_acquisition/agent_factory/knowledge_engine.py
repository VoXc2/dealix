"""Knowledge OS semantic retrieval engine — in-memory, permission-aware.
محرّك الاسترجاع الدلالي لـ Knowledge OS — في الذاكرة، واعٍ بالصلاحيات.

This is the working retrieval backend behind an agent's memory binding. It
indexes document chunks, embeds them with a pluggable embedder, and ranks
them by cosine similarity — filtered by the source allow-list and the
customer scope so an agent can only retrieve within its bound customer.

The default embedder is deterministic and offline (a token-hashing lexical
proxy): texts sharing tokens land near each other in vector space, with no
network and no API key, so the bundle stays test-safe.

# LATER WAVE: an OpenAI-backed ``Embedder`` wrapping
# ``core.memory.embedding_service.EmbeddingService`` gives true neural
# embeddings — it is async and needs an OpenAI key, so it ships separately.
# The ``Embedder`` protocol below is the seam it plugs into.
"""
from __future__ import annotations

import hashlib
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.knowledge_v10.schemas import RetrievalResult, SourceType
from auto_client_acquisition.knowledge_v10.source_policy import is_source_allowed
from core.memory.embedding_service import cosine_similarity

_EMBED_DIMS = 256


class Embedder(Protocol):
    """A text → fixed-length float vector function."""

    def embed(self, text: str) -> list[float]: ...


class HashingEmbedder:
    """Deterministic offline embedder — token hashing into a fixed vector.

    A lexical-semantic proxy: every token is hashed to one bucket; cosine
    similarity then reflects shared-token weight. No network, no API key.
    """

    def __init__(self, dims: int = _EMBED_DIMS) -> None:
        self._dims = dims

    def embed(self, text: str) -> list[float]:
        vec = [0.0] * self._dims
        for token in text.lower().split():
            if len(token) < 2:
                continue
            digest = hashlib.blake2b(token.encode(), digest_size=8).digest()
            vec[int.from_bytes(digest, "big") % self._dims] += 1.0
        return vec


class DocumentChunk(BaseModel):
    """One retrievable chunk. ``text`` MUST be PII-free / redacted before indexing."""

    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    chunk_id: str = Field(..., min_length=1)
    document_id: str = Field(..., min_length=1)
    customer_handle: str = ""
    source_type: SourceType
    text: str = ""


class SemanticChunkIndex:
    """In-memory, permission-aware semantic index of document chunks."""

    def __init__(self, embedder: Embedder | None = None) -> None:
        self._embedder: Embedder = embedder or HashingEmbedder()
        self._chunks: list[DocumentChunk] = []
        self._vectors: dict[str, list[float]] = {}

    def add_chunk(self, chunk: DocumentChunk) -> None:
        """Index one chunk. Blocked source types are refused, never stored."""
        if not is_source_allowed(chunk.source_type):
            msg = "blocked_source_type"
            raise ValueError(msg)
        self._chunks.append(chunk)
        self._vectors[chunk.chunk_id] = self._embedder.embed(chunk.text)

    def add_chunks(self, chunks: list[DocumentChunk]) -> None:
        for chunk in chunks:
            self.add_chunk(chunk)

    def chunk_count(self) -> int:
        return len(self._chunks)

    def search(
        self,
        query: str,
        *,
        customer_handle: str = "",
        allowed_sources: list[SourceType] | None = None,
        top_k: int = 5,
    ) -> list[RetrievalResult]:
        """Return the ``top_k`` chunks ranked by cosine similarity to ``query``.

        Hard filters applied BEFORE ranking: customer scope, the caller's
        ``allowed_sources``, and the global source allow-list.
        """
        allowed = {
            (s.value if isinstance(s, SourceType) else str(s))
            for s in (allowed_sources or [])
            if is_source_allowed(s)
        }
        query_vec = self._embedder.embed(query)
        scored: list[tuple[float, DocumentChunk]] = []
        for chunk in self._chunks:
            if customer_handle and chunk.customer_handle != customer_handle:
                continue
            if not is_source_allowed(chunk.source_type):
                continue
            if allowed and str(chunk.source_type) not in allowed:
                continue
            sim = cosine_similarity(query_vec, self._vectors[chunk.chunk_id])
            if sim > 0.0:
                scored.append((sim, chunk))
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [
            RetrievalResult(
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                snippet_redacted=chunk.text,
                score=min(1.0, round(sim, 4)),
                source_type=chunk.source_type,
            )
            for sim, chunk in scored[:top_k]
        ]


__all__ = [
    "DocumentChunk",
    "Embedder",
    "HashingEmbedder",
    "SemanticChunkIndex",
]
