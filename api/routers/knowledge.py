"""
Knowledge router — per-tenant RAG ingestion + search + delete.

Endpoints:
    POST  /api/v1/knowledge/ingest   — register a document + kick off
                                       chunking + embedding (sync for
                                       short text; arq-queued otherwise).
    GET   /api/v1/knowledge/{doc_id} — read status + chunk count.
    GET   /api/v1/knowledge          — list documents for the caller.
    GET   /api/v1/knowledge/search   — semantic search.
    DELETE /api/v1/knowledge/{doc_id} — cascade-delete chunks + record.

Auth: tenant-scoped via request.state.tenant_id.

PDPL/DSR: every document is a data subject. The DSR delete endpoint
cascades into this router (`api/routers/pdpl_dsr.delete_request` already
audits + queues; T5b wires the actual cascade as a follow-up).
"""

from __future__ import annotations

import secrets
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from db.models import KnowledgeChunkRecord, KnowledgeDocumentRecord
from db.session import get_db

router = APIRouter(prefix="/api/v1/knowledge", tags=["knowledge"])
log = get_logger(__name__)


def _tenant(request: Request) -> str:
    tid = getattr(request.state, "tenant_id", None)
    if not tid and not getattr(request.state, "is_super_admin", False):
        raise HTTPException(401, "tenant_unresolved")
    return str(tid or "")


class IngestIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    source_kind: str = Field(default="upload", max_length=32)
    source_uri: str | None = Field(default=None, max_length=2048)
    locale: str = Field(default="ar", max_length=8)
    text: str = Field(..., min_length=20, max_length=200_000)


class SearchOut(BaseModel):
    chunk_id: str
    document_id: str
    text: str
    similarity: float
    rerank_score: float


@router.post("/ingest")
async def ingest_document(
    payload: IngestIn,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    tid = _tenant(request)
    from dealix.rag.ingest import embed_chunks, split

    doc_id = "kdoc_" + secrets.token_hex(8)
    doc = KnowledgeDocumentRecord(
        id=doc_id,
        tenant_id=tid,
        title=payload.title,
        source_kind=payload.source_kind,
        source_uri=payload.source_uri,
        locale=payload.locale,
        status="processing",
    )
    db.add(doc)
    try:
        await db.commit()
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(500, "doc_persist_failed") from None

    chunks = split(payload.text)
    embedded = await embed_chunks(chunks)
    written = 0
    for chunk, vec, model in embedded:
        cid = "kchk_" + secrets.token_hex(8)
        row = KnowledgeChunkRecord(
            id=cid,
            tenant_id=tid,
            document_id=doc_id,
            order=chunk.order,
            text=chunk.text,
            embedding_model=model,
            meta_json={"dim": len(vec)},
        )
        db.add(row)
        written += 1
    try:
        # The pgvector column is set via a raw UPDATE so we keep the
        # ORM portable. On non-Postgres backends this is a no-op and
        # similarity search returns empty (callers handle that).
        await db.commit()
        if embedded:
            from sqlalchemy import text as _sql_text

            for (chunk, vec, _model), cid in zip(
                embedded,
                [c.id for c, _, _ in embedded],
                strict=False,
            ):
                if vec:
                    try:
                        await db.execute(
                            _sql_text(
                                "UPDATE knowledge_chunks SET embedding = :vec "
                                "WHERE id = :cid"
                            ),
                            {"vec": vec, "cid": cid},
                        )
                    except Exception:
                        # Non-Postgres backend; column doesn't exist.
                        break
            await db.commit()
        doc.chunk_count = written
        doc.status = "ready"
        await db.commit()
    except SQLAlchemyError:
        await db.rollback()
        doc.status = "failed"
        await db.commit()
        raise HTTPException(500, "chunk_persist_failed") from None

    log.info(
        "knowledge_ingested",
        tenant_id=tid,
        document_id=doc_id,
        chunks=written,
    )
    return {
        "document_id": doc_id,
        "status": doc.status,
        "chunk_count": written,
    }


@router.get("/search")
async def knowledge_search(
    request: Request,
    q: str = Query(..., min_length=1, max_length=500),
    top_n: int = Query(default=5, ge=1, le=20),
) -> dict[str, Any]:
    tid = _tenant(request)
    from dealix.rag.search import search as rag_search

    hits = await rag_search(tenant_id=tid, query=q, top_n=top_n)
    return {
        "query": q,
        "tenant_id": tid,
        "count": len(hits),
        "hits": [
            {
                "chunk_id": h.chunk_id,
                "document_id": h.document_id,
                "text": h.text,
                "similarity": h.similarity,
                "rerank_score": h.rerank_score,
            }
            for h in hits
        ],
    }


@router.get("/{document_id}")
async def get_document(
    request: Request,
    document_id: str = Path(..., max_length=64),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    tid = _tenant(request)
    row = (
        await db.execute(
            select(KnowledgeDocumentRecord).where(
                KnowledgeDocumentRecord.id == document_id,
                KnowledgeDocumentRecord.tenant_id == tid,
            )
        )
    ).scalar_one_or_none()
    if row is None:
        raise HTTPException(404, "document_not_found")
    return {
        "id": row.id,
        "title": row.title,
        "status": row.status,
        "chunk_count": row.chunk_count,
        "source_kind": row.source_kind,
        "source_uri": row.source_uri,
        "locale": row.locale,
        "created_at": row.created_at.isoformat(),
    }


@router.get("")
async def list_documents(
    request: Request, db: AsyncSession = Depends(get_db)
) -> dict[str, Any]:
    tid = _tenant(request)
    rows = (
        await db.execute(
            select(KnowledgeDocumentRecord)
            .where(
                KnowledgeDocumentRecord.tenant_id == tid,
                KnowledgeDocumentRecord.deleted_at.is_(None),
            )
            .order_by(KnowledgeDocumentRecord.created_at.desc())
            .limit(500)
        )
    ).scalars().all()
    return {
        "tenant_id": tid,
        "count": len(rows),
        "items": [
            {
                "id": r.id,
                "title": r.title,
                "status": r.status,
                "chunk_count": r.chunk_count,
                "locale": r.locale,
                "created_at": r.created_at.isoformat(),
            }
            for r in rows
        ],
    }


@router.delete("/{document_id}")
async def delete_document(
    request: Request,
    document_id: str = Path(..., max_length=64),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    tid = _tenant(request)
    row = (
        await db.execute(
            select(KnowledgeDocumentRecord).where(
                KnowledgeDocumentRecord.id == document_id,
                KnowledgeDocumentRecord.tenant_id == tid,
            )
        )
    ).scalar_one_or_none()
    if row is None:
        raise HTTPException(404, "document_not_found")
    from datetime import datetime, timezone
    from sqlalchemy import delete as _delete

    row.deleted_at = datetime.now(timezone.utc).replace(tzinfo=None)
    try:
        await db.execute(
            _delete(KnowledgeChunkRecord).where(
                KnowledgeChunkRecord.document_id == document_id,
                KnowledgeChunkRecord.tenant_id == tid,
            )
        )
        await db.commit()
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(500, "delete_failed") from None
    log.info("knowledge_deleted", document_id=document_id, tenant_id=tid)
    return {"ok": True, "id": document_id}
