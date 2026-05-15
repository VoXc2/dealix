"""Knowledge v10 router — RAG contract endpoints.

Pure local composition. No LLM, no external HTTP, no scraping.
Real Qdrant adapter ships in §S6.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.knowledge_v10 import (
    Answer,
    AnswerRequest,
    RAGEvalResult,
    RetrievalRequest,
    RetrievalResult,
    SourceType,
    evaluate_answer,
    ingest_text,
    retrieve,
    validate_manifest,
)
from auto_client_acquisition.knowledge_v10 import (
    answer as kg_answer,
)

router = APIRouter(
    prefix="/api/v1/knowledge-v10",
    tags=["knowledge-v10"],
)


_GUARDRAILS = {
    "no_external_http": True,
    "no_pii_ingestion": True,
    "no_default_scraping": True,
    "no_llm_calls": True,
}


class _EvaluateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answer: Answer
    retrieved_chunks: list[RetrievalResult] = Field(default_factory=list)
    golden_answer: str = ""


@router.get("/status")
async def knowledge_status() -> dict[str, Any]:
    return {
        "module": "knowledge_v10",
        "status": "operational",
        "guardrails": _GUARDRAILS,
        "endpoints": [
            "/status", "/sources", "/manifest/validate",
            "/ingest", "/search", "/answer", "/evaluate",
        ],
    }


@router.get("/sources")
async def knowledge_sources() -> dict[str, Any]:
    return {"sources": [s.value for s in SourceType]}


@router.post("/manifest/validate")
async def knowledge_manifest_validate(payload: dict) -> dict[str, Any]:
    try:
        manifest = validate_manifest(payload)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return manifest.model_dump(mode="json")


class _IngestRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document_id: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)
    customer_handle: str = ""
    source_type: SourceType = SourceType.INTERNAL_DOC
    language: str = "ar"


@router.post("/ingest")
async def knowledge_ingest(payload: _IngestRequest) -> dict[str, Any]:
    try:
        return await ingest_text(
            document_id=payload.document_id,
            text=payload.text,
            customer_handle=payload.customer_handle,
            source_type=payload.source_type,
            language=payload.language,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/search")
async def knowledge_search(payload: RetrievalRequest) -> list[dict[str, Any]]:
    results = await retrieve(payload)
    return [r.model_dump(mode="json") for r in results]


@router.post("/answer")
async def knowledge_answer(payload: AnswerRequest) -> dict[str, Any]:
    out = kg_answer(payload)
    return out.model_dump(mode="json")


@router.post("/evaluate")
async def knowledge_evaluate(payload: _EvaluateRequest) -> dict[str, Any]:
    result: RAGEvalResult = evaluate_answer(
        payload.answer, payload.retrieved_chunks, payload.golden_answer,
    )
    return result.model_dump(mode="json")
