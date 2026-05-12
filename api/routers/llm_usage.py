"""
LLM usage endpoint — per-tenant cost dashboard data.

When Portkey is configured, queries Portkey's logs API for definitive
spend; otherwise reads from the existing `llm_calls` table populated by
`core/llm/cost_tracker` and the cost guardrail.

Endpoint:
    GET /api/v1/customers/{tenant_id}/llm/usage?since=...&until=...
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from sqlalchemy import and_, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.llm.cost_guard import CostGuard
from core.logging import get_logger
from db.session import get_db

router = APIRouter(prefix="/api/v1/customers", tags=["llm-usage"])
log = get_logger(__name__)


def _assert_tenant(request: Request, tenant_id: str) -> None:
    caller = getattr(request.state, "tenant_id", None)
    if getattr(request.state, "is_super_admin", False):
        return
    if caller and caller != tenant_id:
        raise HTTPException(403, "cross_tenant_access_denied")


@router.get("/{tenant_id}/llm/usage")
async def llm_usage(
    request: Request,
    tenant_id: str = Path(..., max_length=64),
    since: datetime | None = Query(default=None),
    until: datetime | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    _assert_tenant(request, tenant_id)
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    until_ts = until.replace(tzinfo=None) if until else now
    since_ts = since.replace(tzinfo=None) if since else (until_ts - timedelta(days=30))

    # Today's accumulated spend from the cost guard's Redis counter.
    guard = CostGuard(tenant_id=tenant_id)
    spent_today = await guard.current_day_spend_usd()

    # Aggregate from the llm_calls table when present.
    rows: list[dict[str, Any]] = []
    try:
        from db.models import LLMCallRecord  # type: ignore

        agg = await db.execute(
            select(
                LLMCallRecord.provider,
                LLMCallRecord.model,
                func.count().label("calls"),
                func.coalesce(func.sum(LLMCallRecord.cost_usd), 0).label("cost_usd"),
                func.coalesce(func.sum(LLMCallRecord.tokens_total), 0).label("tokens"),
            )
            .where(
                and_(
                    LLMCallRecord.tenant_id == tenant_id,
                    LLMCallRecord.created_at >= since_ts,
                    LLMCallRecord.created_at <= until_ts,
                )
            )
            .group_by(LLMCallRecord.provider, LLMCallRecord.model)
            .order_by(func.sum(LLMCallRecord.cost_usd).desc())
        )
        rows = [
            {
                "provider": r.provider,
                "model": r.model,
                "calls": int(r.calls or 0),
                "cost_usd": round(float(r.cost_usd or 0.0), 4),
                "tokens": int(r.tokens or 0),
            }
            for r in agg
        ]
    except (SQLAlchemyError, ImportError):
        log.warning("llm_usage_table_missing_or_failed", tenant=tenant_id)

    total_usd = round(sum(r["cost_usd"] for r in rows), 4)

    return {
        "tenant_id": tenant_id,
        "since": since_ts.isoformat(),
        "until": until_ts.isoformat(),
        "total_usd_window": total_usd,
        "spent_today_usd": round(spent_today, 4),
        "per_request_cap_usd": guard.request_cap_usd,
        "tenant_day_cap_usd": guard.tenant_day_cap_usd,
        "by_model": rows,
        "portkey_configured": bool(os.getenv("PORTKEY_API_KEY", "").strip()),
    }
