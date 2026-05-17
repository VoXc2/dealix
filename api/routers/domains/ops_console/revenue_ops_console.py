"""Ops Console — Revenue Ops Console.

غرفة تشغيل الإيرادات.

GET /api/v1/ops/revenue
  Pipeline by stage, opportunities, conversion rates, and the next-best-action
  catalog. Read-only; admin-key gated. Conversion rates are estimates.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from api.routers.domains.ops_console._common import governed
from api.security.api_key import require_admin_key

router = APIRouter(
    prefix="/api/v1/ops/revenue",
    tags=["Ops Console — Revenue Ops"],
    dependencies=[Depends(require_admin_key)],
)


def _pipeline_summary() -> dict[str, Any]:
    from auto_client_acquisition.revenue_pipeline.pipeline import get_default_pipeline

    return dict(get_default_pipeline().summary())


async def _opportunities() -> list[dict[str, Any]]:
    from sqlalchemy import select

    from db.models import LeadRecord
    from db.session import async_session_factory

    async with async_session_factory()() as session:
        stmt = (
            select(LeadRecord)
            .where(LeadRecord.deleted_at.is_(None))
            .order_by(LeadRecord.created_at.desc())
            .limit(30)
        )
        rows = (await session.execute(stmt)).scalars().all()
        return [
            {
                "id": r.id,
                "company_name": r.company_name,
                "sector": r.sector,
                "status": r.status,
                "fit_score": r.fit_score,
                "urgency_score": r.urgency_score,
                "budget": r.budget,
                "created_at": str(r.created_at),
            }
            for r in rows
        ]


def _action_catalog() -> list[dict[str, Any]]:
    from auto_client_acquisition.revenue_os import list_action_catalog

    return list(list_action_catalog())


@router.get("")
async def revenue_ops() -> dict[str, Any]:
    """Pipeline-by-stage, opportunities, conversion, next-best-actions."""
    try:
        summary = _pipeline_summary()
    except Exception:  # noqa: BLE001
        summary = {}

    total = int(summary.get("total_leads", 0) or 0)
    commitments = int(summary.get("commitments", 0) or 0)
    paid = int(summary.get("paid", 0) or 0)

    conversion = {
        "lead_to_commitment_pct": round(100 * commitments / total, 1) if total else 0.0,
        "commitment_to_paid_pct": (
            round(100 * paid / commitments, 1) if commitments else 0.0
        ),
        "is_estimate": True,
    }

    try:
        opportunities = await _opportunities()
        opp_note: str | None = None
    except Exception:  # noqa: BLE001
        opportunities, opp_note = [], "database_unavailable"

    try:
        actions = _action_catalog()
    except Exception:  # noqa: BLE001
        actions = []

    return governed(
        {
            "pipeline_by_stage": {
                "leads": total,
                "commitments": commitments,
                "paid": paid,
                "total_revenue_sar": summary.get("total_revenue_sar", 0),
            },
            "opportunities": {
                "count": len(opportunities),
                "items": opportunities,
                "note": opp_note,
            },
            "conversion_rates": conversion,
            "next_best_actions": actions,
        }
    )
