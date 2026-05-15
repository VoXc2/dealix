"""Knowledge OS router — ingest documents, ask grounded questions.

Tenant-scoped via ``customer_handle``. Blocked sources are rejected at
ingest. Answers without retrieved evidence return
``insufficient_evidence=True``. Every response carries a
``governance_decision``.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from auto_client_acquisition.governance_os.runtime_decision import GovernanceDecision
from auto_client_acquisition.knowledge_os.index import get_default_index
from auto_client_acquisition.knowledge_os.ingest import ingest_document
from auto_client_acquisition.knowledge_os.knowledge_ledger import list_knowledge_events
from auto_client_acquisition.knowledge_os.schemas import IngestRequest, RetrievalRequest
from auto_client_acquisition.knowledge_os.synthesizer import answer_query_llm

router = APIRouter(prefix="/api/v1/knowledge", tags=["Agents"])


class IngestBody(BaseModel):
    customer_id: str = Field(..., min_length=1)
    source_type: str = Field("manually_entered_note", min_length=1)
    title: str = ""
    text: str = Field(..., min_length=1)
    language: str = "ar"


class QueryBody(BaseModel):
    customer_id: str = Field(..., min_length=1)
    query: str = Field(..., min_length=3)
    language: str = "both"
    top_k: int = Field(5, ge=1, le=50)


@router.post("/documents")
async def ingest(body: IngestBody) -> dict[str, Any]:
    try:
        manifest = ingest_document(
            IngestRequest(
                customer_handle=body.customer_id,
                source_type=body.source_type,
                title=body.title,
                text=body.text,
                language=body.language,
            ),
            index=get_default_index(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {
        "document": manifest.model_dump(mode="json"),
        "governance_decision": GovernanceDecision.ALLOW.value,
    }


@router.post("/query")
async def query(body: QueryBody) -> dict[str, Any]:
    language = body.language if body.language in ("ar", "en", "both") else "both"
    answer = await answer_query_llm(
        RetrievalRequest(
            query=body.query,
            customer_handle=body.customer_id,
            language=language,
            top_k=body.top_k,
        ),
        index=get_default_index(),
    )
    payload = answer.model_dump(mode="json")
    payload["customer_id"] = body.customer_id
    payload["governance_decision"] = (
        GovernanceDecision.ALLOW.value
        if not answer.insufficient_evidence
        else GovernanceDecision.DRAFT_ONLY.value
    )
    return payload


@router.get("/{customer_id}/ledger")
async def ledger(
    customer_id: str,
    limit: int = Query(200, ge=1, le=2000),
    since_days: int = Query(90, ge=1, le=365),
) -> dict[str, Any]:
    events = list_knowledge_events(
        customer_handle=customer_id, limit=limit, since_days=since_days
    )
    return {
        "customer_id": customer_id,
        "count": len(events),
        "events": [e.to_dict() for e in events],
        "governance_decision": GovernanceDecision.ALLOW.value,
    }
