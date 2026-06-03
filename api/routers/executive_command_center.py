"""Executive Command Center HTTP surface (Phase 5).

  GET /api/v1/executive-command-center/status
  GET /api/v1/executive-command-center/{customer_handle}
  GET /api/v1/executive-command-center/{customer_handle}/daily
  GET /api/v1/executive-command-center/{customer_handle}/weekly

Read-only. Best-effort. Customer-safe labels.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.executive_command_center import (
    build_command_center,
    build_daily,
    build_weekly,
)
from auto_client_acquisition.executive_command_center.customer_safe_renderer import (
    render_customer_safe,
)

router = APIRouter(
    prefix="/api/v1/executive-command-center",
    tags=["executive-command-center"],
)

_HARD_GATES: dict[str, bool] = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_fake_revenue": True,
    "no_fake_proof": True,
    "no_fake_forecast": True,
    "read_only": True,
    "customer_safe_labels": True,
}


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "service": "executive_command_center",
        "version": "1.0.0",
        "sections": [
            "executive_summary", "full_ops_score", "today_3_decisions",
            "revenue_radar", "sales_pipeline", "growth_radar",
            "partnership_radar", "support_inbox", "delivery_operations",
            "finance_state", "proof_ledger", "risks_compliance",
            "approval_center", "whatsapp_decision_preview",
            "degraded_sections",
        ],
        "section_count": 15,
        "hard_gates": _HARD_GATES,
    }


@router.get("/{customer_handle}")
async def snapshot(customer_handle: str) -> dict[str, Any]:
    view = build_command_center(customer_handle=customer_handle)
    return {
        "view": render_customer_safe(view),
        "hard_gates": _HARD_GATES,
    }


@router.get("/{customer_handle}/daily")
async def daily(customer_handle: str) -> dict[str, Any]:
    view = build_daily(customer_handle=customer_handle)
    return {
        "view": render_customer_safe(view),
        "hard_gates": _HARD_GATES,
    }


@router.get("/{customer_handle}/weekly")
async def weekly(customer_handle: str) -> dict[str, Any]:
    view = build_weekly(customer_handle=customer_handle)
    return {
        "view": render_customer_safe(view),
        "hard_gates": _HARD_GATES,
    }
