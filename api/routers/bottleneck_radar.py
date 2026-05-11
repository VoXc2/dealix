"""Wave 13 Phase 9 — Bottleneck Radar HTTP surface.

- GET /api/v1/bottleneck-radar/status
- GET /api/v1/bottleneck-radar/founder           — portfolio view
- GET /api/v1/bottleneck-radar/{customer_handle}  — per-customer view

Hard rules: read-only; tenant-isolated (per Wave 12.6 middleware
on the customer-handle-scoped path).
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query

from auto_client_acquisition.bottleneck_radar import (
    compute_bottleneck,
    compute_founder_view,
)

router = APIRouter(prefix="/api/v1/bottleneck-radar", tags=["Bottleneck Radar"])


_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_fake_revenue": True,
    "read_only": True,
    "tenant_isolated": True,
}


@router.get("/status")
async def bottleneck_radar_status() -> dict[str, Any]:
    return {
        "status": "ok",
        "wave": "wave13_phase_9_bottleneck_radar",
        "hard_gates": _HARD_GATES,
    }


@router.get("/founder")
async def founder_view(
    blocking_approvals_count: int = Query(0, ge=0),
    pending_payment_confirmations: int = Query(0, ge=0),
    pending_proof_packs_to_send: int = Query(0, ge=0),
    overdue_followups: int = Query(0, ge=0),
    sla_at_risk_tickets: int = Query(0, ge=0),
) -> dict[str, Any]:
    """Founder portfolio view — counts come from caller (router compose).

    For Phase 9 v1, the router exposes the pure compute fn. A future
    enhancement will pull counts directly from approval_center,
    payment_ops, service_sessions, support_os.
    """
    fb = compute_founder_view(
        blocking_approvals_count=blocking_approvals_count,
        pending_payment_confirmations=pending_payment_confirmations,
        pending_proof_packs_to_send=pending_proof_packs_to_send,
        overdue_followups=overdue_followups,
        sla_at_risk_tickets=sla_at_risk_tickets,
    )
    return {
        "bottleneck": fb.model_dump(),
        "hard_gates": _HARD_GATES,
    }


@router.get("/{customer_handle}")
async def per_customer_view(
    customer_handle: str,
    blocking_approvals_count: int = Query(0, ge=0),
    pending_payment_confirmations: int = Query(0, ge=0),
    pending_proof_packs_to_send: int = Query(0, ge=0),
    overdue_followups: int = Query(0, ge=0),
    sla_at_risk_tickets: int = Query(0, ge=0),
) -> dict[str, Any]:
    fb = compute_bottleneck(
        customer_handle=customer_handle,
        blocking_approvals_count=blocking_approvals_count,
        pending_payment_confirmations=pending_payment_confirmations,
        pending_proof_packs_to_send=pending_proof_packs_to_send,
        overdue_followups=overdue_followups,
        sla_at_risk_tickets=sla_at_risk_tickets,
    )
    return {
        "bottleneck": fb.model_dump(),
        "hard_gates": _HARD_GATES,
    }
