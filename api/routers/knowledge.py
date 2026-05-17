"""Knowledge Base — articles, search, source-grounded answers, gap loop.

Publishing a draft is approval-gated: ``POST /articles/{id}/publish``
creates an ApprovalRequest and returns ``approval_required`` — the
article stays ``draft`` until a founder approves, then a second publish
call completes the transition. Every article create / publish writes an
evidence event.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from auto_client_acquisition.approval_center import (
    ApprovalRequest,
    ApprovalStatus,
    create_approval,
    get_default_approval_store,
)
from auto_client_acquisition.evidence_control_plane_os.event_store import (
    record_evidence_event,
)
from auto_client_acquisition.knowledge.article_store import (
    KnowledgeArticle,
    get_default_article_store,
)
from auto_client_acquisition.knowledge.gaps import get_default_gap_store
from auto_client_acquisition.knowledge.search import search_articles
from auto_client_acquisition.knowledge.suggest import suggest_answer

router = APIRouter(prefix="/api/v1/knowledge", tags=["knowledge"])

_PUBLISH_ACTION = "knowledge_publish"


# ─── Schemas ─────────────────────────────────────────────────────


class ArticleCreate(BaseModel):
    slug: str = ""
    title_ar: str = ""
    title_en: str = ""
    body_ar: str = ""
    body_en: str = ""
    tags: list[str] = Field(default_factory=list)
    category: str = "general"
    source: str = ""
    tenant_id: str | None = None


class ArticleUpdate(BaseModel):
    slug: str | None = None
    title_ar: str | None = None
    title_en: str | None = None
    body_ar: str | None = None
    body_en: str | None = None
    tags: list[str] | None = None
    category: str | None = None
    source: str | None = None


class QueryBody(BaseModel):
    query: str
    limit: int = 5


# ─── Helpers ─────────────────────────────────────────────────────


def _find_publish_approval(article_id: str) -> ApprovalRequest | None:
    """Most recent publish ApprovalRequest for an article, if any."""
    store = get_default_approval_store()
    candidates = [
        r
        for r in store.list_history(limit=500)
        if r.object_id == article_id and r.action_type == _PUBLISH_ACTION
    ]
    candidates.sort(key=lambda r: r.created_at, reverse=True)
    return candidates[0] if candidates else None


# ─── Endpoints ───────────────────────────────────────────────────


@router.get("/status")
async def status() -> dict:
    store = get_default_article_store()
    return {
        "module": "knowledge",
        "backend": "memory_jsonl",
        "articles": len(store.list(include_deleted=False)),
        "approved": len(store.list(status="approved")),
        "open_gaps": len(get_default_gap_store().list(status="open")),
        "guardrails": {
            "publish_requires_approval": True,
            "suggest_answer_approved_only": True,
        },
    }


@router.post("/articles")
async def create_article(body: ArticleCreate) -> dict:
    art = get_default_article_store().create(
        KnowledgeArticle(**body.model_dump())
    )
    record_evidence_event(
        event_type="knowledge_article_created",
        entity_type="knowledge_article",
        entity_id=art.article_id,
        action="create",
        summary_en=f"KB article created (draft): {art.slug or art.article_id}",
        tenant_id=art.tenant_id,
    )
    return art.model_dump(mode="json")


@router.get("/articles")
async def list_articles(
    status: str | None = None,
    category: str | None = None,
    tenant_id: str | None = None,
) -> dict:
    rows = get_default_article_store().list(
        status=status, category=category, tenant_id=tenant_id
    )
    return {"count": len(rows), "articles": [r.model_dump(mode="json") for r in rows]}


@router.get("/articles/{article_id}")
async def get_article(article_id: str) -> dict:
    art = get_default_article_store().get(article_id)
    if art is None:
        raise HTTPException(status_code=404, detail="knowledge_article_not_found")
    return art.model_dump(mode="json")


@router.patch("/articles/{article_id}")
async def update_article(article_id: str, body: ArticleUpdate) -> dict:
    patch = {k: v for k, v in body.model_dump().items() if v is not None}
    try:
        art = get_default_article_store().update(article_id, patch)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return art.model_dump(mode="json")


@router.delete("/articles/{article_id}")
async def delete_article(article_id: str) -> dict:
    try:
        art = get_default_article_store().soft_delete(article_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"deleted": True, "article_id": art.article_id}


@router.post("/articles/{article_id}/publish")
async def publish_article(article_id: str) -> dict:
    """Approval-gated publish. First call queues an approval; once a
    founder has approved it, a second call completes the transition."""
    store = get_default_article_store()
    art = store.get(article_id)
    if art is None:
        raise HTTPException(status_code=404, detail="knowledge_article_not_found")
    if art.status == "approved":
        return {"published": True, "already_published": True, "article_id": article_id}

    existing = _find_publish_approval(article_id)
    if existing is not None and ApprovalStatus(existing.status) == ApprovalStatus.APPROVED:
        art = store.set_status(article_id, "approved")
        record_evidence_event(
            event_type="knowledge_article_published",
            entity_type="knowledge_article",
            entity_id=article_id,
            action="publish",
            summary_en=f"KB article published after approval: {art.slug or article_id}",
            approval_id=existing.approval_id,
            tenant_id=art.tenant_id,
        )
        return {"published": True, "article_id": article_id,
                "approval_id": existing.approval_id}

    if existing is not None and ApprovalStatus(existing.status) == ApprovalStatus.PENDING:
        return {"published": False, "approval_status": "approval_required",
                "approval_id": existing.approval_id, "article_id": article_id}

    approval = create_approval(
        ApprovalRequest(
            object_type="knowledge_article",
            object_id=article_id,
            action_type=_PUBLISH_ACTION,
            action_mode="approval_required",
            risk_level="medium",
            summary_en=f"Publish KB article: {art.slug or article_id}",
            summary_ar="نشر مقال قاعدة المعرفة",
            proof_impact=f"knowledge:{article_id}",
        )
    )
    record_evidence_event(
        event_type="knowledge_publish_requested",
        entity_type="knowledge_article",
        entity_id=article_id,
        action="request_publish_approval",
        summary_en=f"Publish approval requested for KB article {article_id}",
        approval_id=approval.approval_id,
        tenant_id=art.tenant_id,
    )
    return {"published": False, "approval_status": "approval_required",
            "approval_id": approval.approval_id, "article_id": article_id}


@router.post("/search")
async def search(body: QueryBody) -> dict:
    ranked = search_articles(body.query, status="approved", limit=body.limit)
    return {
        "count": len(ranked),
        "results": [
            {"article": a.model_dump(mode="json"), "score": round(s, 3)}
            for a, s in ranked
        ],
    }


@router.post("/suggest-answer")
async def suggest(body: QueryBody) -> dict[str, Any]:
    return suggest_answer(body.query)


@router.get("/gaps")
async def list_gaps(status: str | None = Query(default="open")) -> dict:
    rows = get_default_gap_store().list(status=status)
    return {"count": len(rows), "gaps": [g.model_dump(mode="json") for g in rows]}


@router.post("/gaps/{gap_id}/resolve")
async def resolve_gap(gap_id: str, article_id: str | None = None) -> dict:
    try:
        gap = get_default_gap_store().resolve(gap_id, article_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return gap.model_dump(mode="json")
