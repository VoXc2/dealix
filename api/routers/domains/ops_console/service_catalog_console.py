"""Ops Console — Service Catalog.

كتالوج الخدمات — سلّم العروض المنتَجة.

GET /api/v1/ops/catalog
  The productized offer ladder: every offering with price, scope, KPI
  commitment language, action modes, hard gates, and journey stage.
  Read-only; admin-key gated. Reads the canonical service_catalog registry.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from api.routers.domains.ops_console._common import governed
from api.security.api_key import require_admin_key

router = APIRouter(
    prefix="/api/v1/ops/catalog",
    tags=["Ops Console — Service Catalog"],
    dependencies=[Depends(require_admin_key)],
)


def _offerings() -> list[dict[str, Any]]:
    from auto_client_acquisition.service_catalog.registry import list_offerings

    rows: list[dict[str, Any]] = []
    for rung, o in enumerate(list_offerings(), start=1):
        rows.append(
            {
                "rung": rung,
                "id": o.id,
                "name_ar": o.name_ar,
                "name_en": o.name_en,
                "price_sar": o.price_sar,
                "price_unit": o.price_unit,
                "duration_days": o.duration_days,
                "deliverables": list(o.deliverables),
                "kpi_commitment_ar": o.kpi_commitment_ar,
                "kpi_commitment_en": o.kpi_commitment_en,
                "refund_policy_ar": o.refund_policy_ar,
                "refund_policy_en": o.refund_policy_en,
                "action_modes": list(o.action_modes_used),
                "hard_gates": list(o.hard_gates),
                "journey_stage": o.customer_journey_stage,
                "is_estimate": o.is_estimate,
            }
        )
    return rows


@router.get("")
async def catalog() -> dict[str, Any]:
    """The full productized offer ladder."""
    try:
        ladder = _offerings()
    except Exception:  # noqa: BLE001
        return governed(
            {"ladder": [], "entry_offers": [], "note": "service_catalog_unavailable"}
        )

    entry_offers = [
        o for o in ladder if o["price_sar"] == 0 or o["journey_stage"] == "discovery"
    ]
    hard_gates = sorted({g for o in ladder for g in o["hard_gates"]})
    return governed(
        {
            "ladder": ladder,
            "entry_offers": entry_offers,
            "hard_gates": hard_gates,
            "offer_count": len(ladder),
        }
    )
