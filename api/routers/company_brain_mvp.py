"""HTTP surface for Company Brain MVP (in-memory; dev/founder demos)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.company_brain_mvp.memory import (
    ingest_chunk,
    query_workspace,
)

router = APIRouter(prefix="/api/v1/company-brain", tags=["company-brain"])


class IngestBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    workspace_id: str = Field(min_length=1, max_length=64)
    text: str = Field(min_length=1, max_length=50_000)
    source_id: str = Field(min_length=1, max_length=200)
    title: str | None = Field(default=None, max_length=200)


class QueryBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    workspace_id: str = Field(min_length=1, max_length=64)
    question: str = Field(min_length=1, max_length=2000)


@router.post("/ingest")
def post_ingest(body: IngestBody) -> dict[str, Any]:
    try:
        chunk = ingest_chunk(
            workspace_id=body.workspace_id,
            text=body.text,
            source_id=body.source_id,
            title=body.title,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"chunk": chunk, "no_source_no_answer": True}


@router.post("/query")
def post_query(body: QueryBody) -> dict[str, Any]:
    return query_workspace(workspace_id=body.workspace_id, question=body.question)
