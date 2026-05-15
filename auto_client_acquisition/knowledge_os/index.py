"""Knowledge index — the searchable store of redacted chunks.

``InMemoryKnowledgeIndex`` is the default: deterministic keyword/TF scoring,
no external service, no network. A pgvector-backed adapter satisfying the
same ``KnowledgeIndex`` protocol is the upgrade path.

Hard guarantee: a chunk whose ``source_type`` is on the blocked list is
never stored — ingestion is the gate, but the index refuses too, so a bad
caller cannot smuggle a scraped source past retrieval.
"""
from __future__ import annotations

import re
import threading
from typing import Protocol

from auto_client_acquisition.knowledge_os.schemas import KnowledgeChunk, RetrievalResult
from auto_client_acquisition.knowledge_v10.source_policy import is_source_allowed

__all__ = ["KnowledgeIndex", "InMemoryKnowledgeIndex"]

_TOKEN_RE = re.compile(r"[^\W\d_]+", re.UNICODE)


def _tokens(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


class KnowledgeIndex(Protocol):
    """Contract every index implementation must satisfy."""

    def add(self, chunk: KnowledgeChunk) -> None: ...

    def search(
        self,
        query: str,
        *,
        customer_handle: str,
        top_k: int,
        allowed_sources: frozenset[str],
    ) -> list[RetrievalResult]: ...

    def clear(self) -> None: ...


class InMemoryKnowledgeIndex:
    """Deterministic keyword-overlap index. Thread-safe, tenant-scoped."""

    def __init__(self) -> None:
        self._chunks: list[KnowledgeChunk] = []
        self._lock = threading.Lock()

    def add(self, chunk: KnowledgeChunk) -> None:
        if not is_source_allowed(chunk.source_type):
            raise ValueError(f"blocked source_type cannot be indexed: {chunk.source_type}")
        with self._lock:
            self._chunks.append(chunk)

    def search(
        self,
        query: str,
        *,
        customer_handle: str,
        top_k: int,
        allowed_sources: frozenset[str],
    ) -> list[RetrievalResult]:
        q_tokens = set(_tokens(query))
        if not q_tokens:
            return []
        scored: list[tuple[float, KnowledgeChunk]] = []
        with self._lock:
            chunks = list(self._chunks)
        for chunk in chunks:
            if chunk.customer_handle != customer_handle:
                continue
            if chunk.source_type not in allowed_sources:
                continue
            if not is_source_allowed(chunk.source_type):
                continue
            c_tokens = _tokens(chunk.snippet_redacted)
            if not c_tokens:
                continue
            overlap = sum(1 for t in c_tokens if t in q_tokens)
            if overlap == 0:
                continue
            # Score: query coverage, normalised to 0..1, deterministic.
            score = overlap / (len(q_tokens) + len(set(c_tokens)) - overlap)
            scored.append((round(min(score, 1.0), 6), chunk))
        scored.sort(key=lambda pair: (-pair[0], pair[1].chunk_id))
        return [
            RetrievalResult(
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                snippet_redacted=chunk.snippet_redacted,
                score=score,
                source_type=chunk.source_type,
            )
            for score, chunk in scored[:top_k]
        ]

    def clear(self) -> None:
        with self._lock:
            self._chunks.clear()


# ── Process-wide default index (spine; DB-backed adapter is the upgrade) ──
_DEFAULT_INDEX: InMemoryKnowledgeIndex | None = None


def get_default_index() -> InMemoryKnowledgeIndex:
    global _DEFAULT_INDEX
    if _DEFAULT_INDEX is None:
        _DEFAULT_INDEX = InMemoryKnowledgeIndex()
    return _DEFAULT_INDEX


def clear_default_index_for_test() -> None:
    get_default_index().clear()
