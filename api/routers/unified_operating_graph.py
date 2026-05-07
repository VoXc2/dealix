"""Unified Operating Graph HTTP surface (Phase 3).

  GET /api/v1/unified-operating-graph/status
  GET /api/v1/unified-operating-graph/{customer_handle}

Read-only. Read-safe. Empty/missing → degraded, never 500.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.unified_operating_graph import (
    build_graph_for_customer,
    list_known_node_types,
    summarize_graph_for_customer,
)

router = APIRouter(
    prefix="/api/v1/unified-operating-graph",
    tags=["unified-operating-graph"],
)

_HARD_GATES: dict[str, bool] = {
    "no_live_send": True,
    "no_scraping": True,
    "no_fake_proof": True,
    "read_only": True,
    "approval_required_for_external_actions": True,
}


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "service": "unified_operating_graph",
        "version": "1.0.0",
        "node_types": list_known_node_types(),
        "edge_types": [
            "lead_belongs_to_company",
            "deal_created_from_lead",
            "payment_unblocks_service",
            "service_creates_proof",
            "support_ticket_blocks_delivery",
            "approval_blocks_action",
            "proof_enables_case_study",
        ],
        "hard_gates": _HARD_GATES,
    }


@router.get("/{customer_handle}")
async def graph(customer_handle: str) -> dict[str, Any]:
    """Build the unified graph for one customer (best-effort)."""
    g = build_graph_for_customer(customer_handle=customer_handle)
    summary = summarize_graph_for_customer(g)
    return {
        "graph": g.model_dump(mode="json"),
        "summary": summary,
        "hard_gates": _HARD_GATES,
    }
