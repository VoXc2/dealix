"""Document ingestion — source-gate, chunk, redact, index, audit.

Order matters and is non-negotiable:
  1. Source policy gate — blocked (scraped / personal-data) sources are
     rejected before any text is touched.
  2. Chunk deterministically.
  3. Redact PII from every chunk *before* it reaches the index or ledger.
  4. Index the redacted chunks.
  5. Append a KnowledgeEvent to the audit ledger.
"""
from __future__ import annotations

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text
from auto_client_acquisition.knowledge_os.chunker import chunk_text
from auto_client_acquisition.knowledge_os.index import KnowledgeIndex
from auto_client_acquisition.knowledge_os.knowledge_ledger import emit_knowledge_event
from auto_client_acquisition.knowledge_os.schemas import (
    DocumentManifest,
    IngestRequest,
    KnowledgeChunk,
    KnowledgeEvent,
    new_chunk_id,
    new_document_id,
)
from auto_client_acquisition.knowledge_v10.source_policy import is_source_allowed

__all__ = ["ingest_document"]


def ingest_document(req: IngestRequest, *, index: KnowledgeIndex) -> DocumentManifest:
    """Ingest one document. Raises ``ValueError`` for a blocked source."""
    if not req.customer_handle.strip():
        raise ValueError("customer_handle is required")
    if not is_source_allowed(req.source_type):
        raise ValueError(f"source_type not permitted: {req.source_type}")

    document_id = new_document_id()
    raw_chunks = chunk_text(req.text)
    for position, raw in enumerate(raw_chunks):
        chunk = KnowledgeChunk(
            chunk_id=new_chunk_id(),
            document_id=document_id,
            customer_handle=req.customer_handle,
            source_type=req.source_type,
            position=position,
            snippet_redacted=redact_text(raw),
        )
        index.add(chunk)

    manifest = DocumentManifest(
        id=document_id,
        customer_handle=req.customer_handle,
        source_type=req.source_type,
        title=req.title,
        language=req.language if req.language in ("ar", "en", "mixed") else "mixed",
        chunk_count=len(raw_chunks),
    )
    emit_knowledge_event(
        KnowledgeEvent(
            customer_handle=req.customer_handle,
            kind="document_ingested",
            document_id=document_id,
            source_types=(req.source_type,),
            chunk_count=len(raw_chunks),
        )
    )
    return manifest
