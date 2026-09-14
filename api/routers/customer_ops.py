"""Customer Operations Kernel router — read/draft-only, no live send."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.customer_ops.event_contract import CustomerOpsEvent
from auto_client_acquisition.customer_ops.market_intel import (
    official_sector_brief,
    watch_signals,
)
from auto_client_acquisition.customer_ops.pipeline import run_customer_ops_event
from auto_client_acquisition.customer_ops.retrieval import current_only_retrieve
from auto_client_acquisition.customer_ops.sector_packs import (
    SECTOR_PACK_VERSION,
    get_sector_pack,
    list_sector_packs,
)

router = APIRouter(prefix="/api/v1/customer-ops", tags=["Customers"])

_HARD_GATES = {
    "no_live_send": True,
    "no_cold_outbound": True,
    "no_scraping": True,
    "whatsapp_inbound_only": True,
    "draft_first_web_email": True,
    "relationship_consent_separate": True,
}


class _RunRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event: CustomerOpsEvent
    message_text: str = Field(default="", max_length=4000)


class _RetrieveRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=3, max_length=500)
    allowed_sources: list[str] = Field(default_factory=list)
    top_k: int = Field(default=5, ge=1, le=20)


@router.get("/status")
async def customer_ops_status() -> dict[str, Any]:
    return {
        "service": "customer_ops_kernel",
        "version": SECTOR_PACK_VERSION,
        "status": "operational",
        "sectors": [p["sector"] for p in list_sector_packs()],
        "channels": ["web", "email", "whatsapp(inbound-only)"],
        "hard_gates": _HARD_GATES,
    }


@router.get("/sector-packs")
async def sector_packs() -> dict[str, Any]:
    return {"version": SECTOR_PACK_VERSION, "packs": list_sector_packs()}


@router.get("/sector-packs/{sector}")
async def sector_pack(sector: str) -> dict[str, Any]:
    return get_sector_pack(sector)


@router.post("/retrieve")
async def retrieve(req: _RetrieveRequest) -> dict[str, Any]:
    snapshot, decision, evidence = current_only_retrieve(
        query=req.query, allowed_sources=req.allowed_sources, top_k=req.top_k
    )
    return {
        "snapshot": snapshot.to_ref(),
        "decision": decision,
        "evidence": evidence,
        "hold_or_ask": decision != "answer",
    }


@router.post("/event")
async def run_event(req: _RunRequest) -> dict[str, Any]:
    outcome = run_customer_ops_event(req.event, message_text=req.message_text)
    return {**outcome.to_dict(), "hard_gates": _HARD_GATES}


@router.get("/sector-brief/{sector}")
async def sector_brief(sector: str) -> dict[str, Any]:
    return official_sector_brief(sector)


@router.get("/watch-signals")
async def watch(sector: str | None = None, urgency: str | None = None) -> dict[str, Any]:
    return watch_signals(sector=sector, urgency=urgency)
