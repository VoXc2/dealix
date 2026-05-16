"""Invoice alias endpoint for governed revenue ops."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.revenue_ops import InvoiceDraftRequest, RevenueOpsState, get_record
from auto_client_acquisition.revenue_ops.store import apply_transition
from auto_client_acquisition.revops import InvoiceState, create_invoice_draft, transition_invoice

router = APIRouter(prefix="/api/v1/invoices", tags=["invoices"])

_HARD_GATES = {
    "invoice_draft_is_not_revenue": True,
    "manual_dispatch_required": True,
    "approval_first": True,
}

_INVOICES: dict[str, InvoiceState] = {}


@router.get("/status")
async def invoices_status() -> dict[str, Any]:
    return {
        "service": "invoices_alias",
        "status": "operational",
        "stored_invoices": len(_INVOICES),
        "hard_gates": _HARD_GATES,
    }


@router.post("")
async def create_invoice(req: InvoiceDraftRequest) -> dict[str, Any]:
    record = get_record(req.diagnostic_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"unknown diagnostic_id: {req.diagnostic_id}")

    try:
        invoice = create_invoice_draft(
            customer_handle=req.customer_handle,
            amount_sar=req.amount_sar,
            description=req.description,
            mode="test" if req.mode == "test" else "manual_only",
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if req.mark_as_sent:
        try:
            invoice = transition_invoice(invoice, "sent")
            apply_transition(record, RevenueOpsState.INVOICE_SENT)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
    _INVOICES[invoice.invoice_id] = invoice
    return {
        "invoice": invoice.model_dump(mode="json"),
        "diagnostic_state": record.state.value,
        "hard_gates": _HARD_GATES,
    }


def _reset_invoices_alias() -> None:
    """Test-only helper."""
    _INVOICES.clear()
