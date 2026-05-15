"""Knowledge OS schemas.

The Pydantic v2 RAG contract already lives in ``knowledge_v10.schemas`` —
this module re-exports it verbatim (no duplicate enums) and adds the
engine-side dataclasses the Knowledge OS needs: ingest requests, indexed
chunks, and the auditable knowledge ledger event.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from auto_client_acquisition.knowledge_v10.schemas import (
    Answer,
    AnswerRequest,
    DocumentManifest,
    RAGEvalResult,
    RetrievalRequest,
    RetrievalResult,
    SourceType,
)

__all__ = [
    "Answer",
    "AnswerRequest",
    "DocumentManifest",
    "IngestRequest",
    "KnowledgeChunk",
    "KnowledgeEvent",
    "RAGEvalResult",
    "RetrievalRequest",
    "RetrievalResult",
    "SourceType",
    "knowledge_event_valid",
    "new_chunk_id",
    "new_document_id",
]


def new_document_id() -> str:
    return f"kdoc_{uuid4().hex[:16]}"


def new_chunk_id() -> str:
    return f"kchk_{uuid4().hex[:16]}"


@dataclass(frozen=True, slots=True)
class IngestRequest:
    """A document submitted for ingestion into the Knowledge OS."""

    customer_handle: str
    source_type: str
    title: str
    text: str
    language: str = "ar"


@dataclass(frozen=True, slots=True)
class KnowledgeChunk:
    """A redacted, indexable slice of an ingested document."""

    chunk_id: str
    document_id: str
    customer_handle: str
    source_type: str
    position: int
    snippet_redacted: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class KnowledgeEvent:
    """Append-only audit record for ingest + query activity."""

    knowledge_event_id: str = field(default_factory=lambda: f"kevt_{uuid4().hex[:16]}")
    customer_handle: str = ""
    kind: str = "document_ingested"  # document_ingested|query_answered|retrieval_empty
    document_id: str = ""
    query: str = ""
    source_types: tuple[str, ...] = ()
    chunk_count: int = 0
    citation_count: int = 0
    insufficient_evidence: bool = False
    occurred_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["source_types"] = list(self.source_types)
        return d


_VALID_KINDS = frozenset({"document_ingested", "query_answered", "retrieval_empty"})


def knowledge_event_valid(event: KnowledgeEvent) -> bool:
    """A knowledge event is valid iff it identifies a tenant + a known kind."""
    return bool(
        event.knowledge_event_id.strip()
        and event.customer_handle.strip()
        and event.kind in _VALID_KINDS
    )
