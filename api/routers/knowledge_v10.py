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
    DocumentManifest,
    RAGEvalResult,
    RetrievalRequest,
    RetrievalResult,
    SourceType,
    answer as kg_answer,
    evaluate_answer,
    retrieve,
    validate_manifest,
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
            "/search", "/answer", "/evaluate",
        ],
    }


@router.get("/sources")
async def knowledge_sources() -> dict[str, Any]:
    return {"sources": [s.value for s in SourceType]}


@router.post("/manifest/validate")
async def knowledge_manifest_validate(payload: dict) -> dict[str, Any]:
    try:
        manifest = validate_manifest(payload)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return manifest.model_dump(mode="json")


@router.post("/search")
async def knowledge_search(payload: RetrievalRequest) -> list[dict[str, Any]]:
    results = retrieve(payload)
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
