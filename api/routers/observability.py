"""
Observability router — costs, unsafe-action ledger, quality KPIs.

  POST /api/v1/observability/costs/runs       record one run cost
  GET  /api/v1/observability/costs/summary    cost aggregates (last N days)
  POST /api/v1/observability/unsafe/record    record one blocked action
  GET  /api/v1/observability/unsafe/summary   refusal aggregates
  GET  /api/v1/observability/quality          quality KPIs snapshot
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Body, Query
from sqlalchemy import select

from auto_client_acquisition.agent_observability.cost_tracker import (
    record_run as record_cost, summarize as summarize_costs,
)
from auto_client_acquisition.agent_observability.quality_metrics import compute as compute_quality
from auto_client_acquisition.agent_observability.unsafe_action_monitor import (
    record_block, summarize as summarize_unsafe,
)
from db.models import (
    ObjectionEventRecord, ProofEventRecord, SupportTicketRecord, UnsafeActionRecord,
)
from db.session import get_session

router = APIRouter(prefix="/api/v1/observability", tags=["observability"])


@router.post("/costs/runs")
async def post_cost(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    async with get_session() as s:
        row = await record_cost(
            s,
            agent_name=str(body.get("agent_name") or "unknown"),
            agent_run_id=body.get("agent_run_id"),
            service_id=body.get("service_id"),
            role=body.get("role"),
            customer_id=body.get("customer_id"),
            partner_id=body.get("partner_id"),
            provider=body.get("provider"),
            model=body.get("model"),
            input_tokens=int(body.get("input_tokens") or 0),
            output_tokens=int(body.get("output_tokens") or 0),
            latency_ms=int(body.get("latency_ms") or 0),
            tool_calls_count=int(body.get("tool_calls_count") or 0),
            error_type=body.get("error_type"),
            meta=body.get("meta") or {},
        )
    return {
        "id": row.id,
        "cost_estimate_usd": row.cost_estimate_usd,
        "cost_estimate_sar": row.cost_estimate_sar,
    }


@router.get("/costs/summary")
async def cost_summary(
    days: int = Query(default=7, ge=1, le=90),
    role: str | None = Query(default=None),
    service_id: str | None = Query(default=None),
) -> dict[str, Any]:
    async with get_session() as s:
        return await summarize_costs(s, days=days, role=role, service_id=service_id)


@router.post("/unsafe/record")
async def post_unsafe(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    async with get_session() as s:
        row = await record_block(
            s,
            pattern=str(body.get("pattern") or "unknown"),
            blocked_reason=str(body.get("blocked_reason") or "policy"),
            actor=str(body.get("actor") or "system"),
            source_module=body.get("source_module"),
            customer_id=body.get("customer_id"),
            partner_id=body.get("partner_id"),
            meta=body.get("meta") or {},
        )
    return {"id": row.id, "severity": row.severity, "pattern": row.pattern}


@router.get("/unsafe/summary")
async def unsafe_summary(days: int = Query(default=7, ge=1, le=90)) -> dict[str, Any]:
    async with get_session() as s:
        return await summarize_unsafe(s, days=days)


@router.get("/quality")
async def quality_snapshot(days: int = Query(default=7, ge=1, le=90)) -> dict[str, Any]:
    since = datetime.now(timezone.utc) - timedelta(days=days)
    async with get_session() as s:
        proof = list((await s.execute(
            select(ProofEventRecord).where(ProofEventRecord.occurred_at >= since)
        )).scalars().all())
        objections = list((await s.execute(
            select(ObjectionEventRecord).where(ObjectionEventRecord.occurred_at >= since)
        )).scalars().all())
        tickets = list((await s.execute(
            select(SupportTicketRecord).where(SupportTicketRecord.created_at >= since)
        )).scalars().all())
        unsafe = list((await s.execute(
            select(UnsafeActionRecord).where(UnsafeActionRecord.occurred_at >= since)
        )).scalars().all())
    return {
        "since": since.isoformat(),
        "kpis": compute_quality(
            proof_events=proof,
            objection_events=objections,
            tickets=tickets,
            unsafe_actions=unsafe,
        ),
    }
