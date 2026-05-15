"""CSV preview + CRM board MVP (read-only, no CRM sync)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.revenue_data_intake.crm_board_mvp import crm_board_mvp_snapshot
from auto_client_acquisition.revenue_data_intake.csv_preview import parse_account_csv

router = APIRouter(prefix="/api/v1/revenue-data", tags=["revenue-data"])


class CsvPreviewBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    csv_text: str = Field(default="", max_length=600_000)
    max_rows: int = Field(default=500, ge=1, le=2000)
    preview_limit: int = Field(default=20, ge=1, le=100)


@router.post("/csv-preview")
def post_csv_preview(body: CsvPreviewBody) -> dict[str, Any]:
    """Parse CSV text into account rows + data_quality summary."""
    if not body.csv_text.strip():
        raise HTTPException(status_code=422, detail="csv_text required")
    return parse_account_csv(
        body.csv_text,
        max_rows=body.max_rows,
        preview_limit=body.preview_limit,
    )


@router.get("/crm-board")
def get_crm_board() -> dict[str, Any]:
    return crm_board_mvp_snapshot()


@router.post("/crm-board")
def post_crm_board(body: dict[str, Any]) -> dict[str, Any]:
    opps = body.get("opportunities")
    if opps is not None and not isinstance(opps, list):
        raise HTTPException(status_code=422, detail="opportunities must be a list")
    return crm_board_mvp_snapshot(opportunities=opps if isinstance(opps, list) else None)
