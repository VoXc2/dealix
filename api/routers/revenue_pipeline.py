"""Revenue pipeline — read-only stage reference + truth labels."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.revenue_pipeline import pipeline_summary

router = APIRouter(prefix="/api/v1/revenue-pipeline", tags=["revenue-pipeline"])


@router.get("/status")
async def status() -> dict[str, Any]:
    return {"module": "revenue_pipeline", **pipeline_summary()}


@router.get("/summary")
async def summary() -> dict[str, Any]:
    return pipeline_summary()
