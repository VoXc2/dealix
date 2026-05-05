"""Finance OS v5 — read-only pricing catalog + invoice-draft DTO."""
from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.finance_os import (
    draft_invoice,
    finance_guardrails,
    get_pricing_tier,
    pricing_catalog,
)

router = APIRouter(prefix="/api/v1/finance", tags=["finance-os"])


@router.get("/status")
async def status() -> dict:
    return {"module": "finance_os", **finance_guardrails()}


@router.get("/pricing")
async def get_catalog() -> dict:
    catalog = pricing_catalog()
    return {"count": len(catalog), "tiers": catalog}


@router.get("/pricing/{tier_id}")
async def get_tier(tier_id: str) -> dict:
    try:
        return get_pricing_tier(tier_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/invoice/draft")
async def invoice_draft(payload: dict = Body(...)) -> dict:
    """Build an InvoiceDraft DTO. Does NOT call Moyasar — the founder
    materializes the invoice via ``scripts/dealix_invoice.py``.
    """
    tier_id = payload.get("tier_id")
    customer_email = payload.get("customer_email")
    if not tier_id or not customer_email:
        raise HTTPException(
            status_code=400, detail="tier_id and customer_email required",
        )
    try:
        draft = draft_invoice(
            tier_id=str(tier_id),
            customer_email=str(customer_email),
            customer_handle=str(payload.get("customer_handle", "")),
            callback_url=payload.get("callback_url"),
            metadata=payload.get("metadata") or None,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    out = draft.model_dump(mode="json")
    out["cli_args"] = draft.to_cli_args()
    return out
