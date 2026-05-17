"""Ops Console — Billing & Invoices.

الفواتير والمدفوعات.

GET /api/v1/ops/billing
  Invoices with payment status, the revenue ladder, and unit economics.
  Read-only; admin-key gated.

Doctrine: invoice-intent totals and unit economics are estimates
(`is_estimate: True`); only confirmed paid revenue is ground truth
(`is_estimate: False`).
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from api.routers.domains.ops_console._common import governed
from api.security.api_key import require_admin_key

router = APIRouter(
    prefix="/api/v1/ops/billing",
    tags=["Ops Console — Billing"],
    dependencies=[Depends(require_admin_key)],
)


async def _invoices() -> list[dict[str, Any]]:
    from sqlalchemy import select

    from db.models import ZATCAInvoiceRecord
    from db.session import async_session_factory

    async with async_session_factory()() as session:
        stmt = (
            select(ZATCAInvoiceRecord)
            .order_by(ZATCAInvoiceRecord.created_at.desc())
            .limit(50)
        )
        rows = (await session.execute(stmt)).scalars().all()
        return [
            {
                "invoice_number": r.invoice_number,
                "buyer_name": r.buyer_name,
                "subtotal_sar": float(r.subtotal_sar or 0),
                "vat_amount_sar": float(r.vat_amount_sar or 0),
                "total_sar": float(r.total_sar or 0),
                "zatca_status": r.zatca_status,
                "issue_date": str(r.issue_date),
                "created_at": str(r.created_at),
            }
            for r in rows
        ]


def _pipeline_summary() -> dict[str, Any]:
    from auto_client_acquisition.revenue_pipeline.pipeline import get_default_pipeline

    return dict(get_default_pipeline().summary())


def _revenue_ladder() -> list[dict[str, Any]]:
    from auto_client_acquisition.service_catalog.registry import list_offerings

    return [
        {
            "id": o.id,
            "name_ar": o.name_ar,
            "name_en": o.name_en,
            "price_sar": o.price_sar,
            "price_unit": o.price_unit,
        }
        for o in list_offerings()
    ]


@router.get("")
async def billing() -> dict[str, Any]:
    """Invoices, payment status, revenue ladder, unit economics."""
    try:
        invoices = await _invoices()
        invoices_note: str | None = None
    except Exception:  # noqa: BLE001
        invoices, invoices_note = [], "database_unavailable"

    invoice_intent_total = sum(float(i.get("total_sar") or 0) for i in invoices)

    try:
        summary = _pipeline_summary()
    except Exception:  # noqa: BLE001
        summary = {}
    paid = int(summary.get("paid", 0) or 0)
    confirmed_revenue = float(summary.get("total_revenue_sar", 0) or 0)

    try:
        ladder = _revenue_ladder()
    except Exception:  # noqa: BLE001
        ladder = []

    unit_economics = {
        "paid_customers": paid,
        "avg_confirmed_deal_sar": round(confirmed_revenue / paid, 2) if paid else 0.0,
        "is_estimate": True,
    }

    return governed(
        {
            "invoices": {
                "count": len(invoices),
                "items": invoices,
                "note": invoices_note,
            },
            # Drafted invoices are intent, not collected cash → estimate.
            "invoice_intent_total_sar": {
                "value": invoice_intent_total,
                "is_estimate": True,
            },
            # Confirmed paid revenue is ground truth.
            "confirmed_revenue_sar": {
                "value": confirmed_revenue,
                "is_estimate": False,
            },
            "revenue_ladder": ladder,
            "unit_economics": unit_economics,
        }
    )
