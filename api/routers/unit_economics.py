"""Unit economics APIs — CAC payback and LTV (initiatives 121–122)."""

from __future__ import annotations

from fastapi import APIRouter, Query

from auto_client_acquisition.operating_finance_os.ltv_from_events import estimate_ltv_sar

router = APIRouter(prefix="/api/v1/unit-economics", tags=["finance"])


@router.get("/ltv/{customer_id}")
def get_ltv(customer_id: str, period_days: int = Query(default=365, ge=1, le=3650)) -> dict:
    return {"customer_id": customer_id, **estimate_ltv_sar(customer_id=customer_id, period_days=period_days)}


@router.get("/cac-payback")
def get_cac_payback(
    cac_sar: float = Query(ge=0),
    monthly_gross_margin_sar: float = Query(ge=0),
) -> dict:
    months = (cac_sar / monthly_gross_margin_sar) if monthly_gross_margin_sar > 0 else None
    return {
        "cac_sar": cac_sar,
        "monthly_gross_margin_sar": monthly_gross_margin_sar,
        "payback_months": months,
    }
