"""
In-app search — Meilisearch primary, Postgres ILIKE fallback.

Endpoints:
    GET /api/v1/search?q=...&kind=leads|deals|docs|audit&limit=20
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request
from sqlalchemy import or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from core.logging import get_logger
from dealix.search.meilisearch_client import (
    is_configured as meili_configured,
)
from dealix.search.meilisearch_client import search as meili_search
from db.models import DealRecord, KnowledgeDocumentRecord, LeadRecord
from db.session import get_db

router = APIRouter(prefix="/api/v1/search", tags=["search"])
log = get_logger(__name__)


def _tenant(request: Request) -> str:
    tid = getattr(request.state, "tenant_id", None)
    if not tid and not getattr(request.state, "is_super_admin", False):
        raise HTTPException(401, "tenant_unresolved")
    return str(tid or "")


@router.get("")
async def in_app_search(
    request: Request,
    q: str = Query(..., min_length=1, max_length=200),
    kind: str = Query(default="leads", pattern="^(leads|deals|docs|audit)$"),
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    tid = _tenant(request)
    if meili_configured():
        hits = await meili_search(tenant_id=tid, kind=kind, query=q, limit=limit)
        return {
            "engine": "meilisearch",
            "kind": kind,
            "query": q,
            "count": len(hits),
            "hits": [
                {
                    "id": h.id,
                    "type": h.type,
                    "text": h.text,
                    "score": h.score,
                }
                for h in hits
            ],
        }
    # Fallback: ILIKE against the relevant table.
    rows: list[dict[str, Any]] = []
    pattern = f"%{q.lower()}%"
    try:
        if kind == "leads":
            res = await db.execute(
                select(LeadRecord)
                .where(
                    LeadRecord.tenant_id == tid,
                    or_(
                        LeadRecord.company_name.ilike(pattern),
                        LeadRecord.contact_email.ilike(pattern),
                        LeadRecord.contact_name.ilike(pattern),
                    ),
                )
                .limit(limit)
            )
            for r in res.scalars():
                rows.append(
                    {
                        "id": r.id,
                        "type": "leads",
                        "text": f"{r.company_name} · {r.contact_email or ''}",
                        "score": 0.5,
                    }
                )
        elif kind == "deals":
            res = await db.execute(
                select(DealRecord)
                .where(
                    DealRecord.tenant_id == tid,
                    DealRecord.status.ilike(pattern),
                )
                .limit(limit)
            )
            for r in res.scalars():
                rows.append(
                    {"id": r.id, "type": "deals", "text": f"{r.id} · {r.status}", "score": 0.5}
                )
        elif kind == "docs":
            res = await db.execute(
                select(KnowledgeDocumentRecord)
                .where(
                    KnowledgeDocumentRecord.tenant_id == tid,
                    KnowledgeDocumentRecord.title.ilike(pattern),
                )
                .limit(limit)
            )
            for r in res.scalars():
                rows.append(
                    {"id": r.id, "type": "docs", "text": r.title, "score": 0.5}
                )
    except SQLAlchemyError:
        log.exception("search_fallback_failed", tenant_id=tid)
    return {
        "engine": "postgres_ilike_fallback",
        "kind": kind,
        "query": q,
        "count": len(rows),
        "hits": rows,
    }
