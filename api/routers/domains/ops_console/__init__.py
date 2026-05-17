"""Ops Console domain — the unified operator console.

غرفة التشغيل — الواجهة الموحّدة للمشغّل.

Eight read/composition surfaces under the `/api/v1/ops/*` namespace. Every
router is admin-key gated and emits the doctrine envelope
(`governance_decision` + `is_estimate`). No new persistence — these routers
compose data from existing modules and ledgers.
"""
from __future__ import annotations

from fastapi import APIRouter

from api.routers.domains.ops_console import (
    billing_console,
    board_decision_os,
    evidence_ledger,
    founder_command_center,
    market_proof_console,
    proof_pack_generator,
    revenue_ops_console,
    service_catalog_console,
)

_ROUTERS = [
    founder_command_center.router,
    service_catalog_console.router,
    market_proof_console.router,
    revenue_ops_console.router,
    evidence_ledger.router,
    billing_console.router,
    board_decision_os.router,
    proof_pack_generator.router,
]


def get_routers() -> list[APIRouter]:
    """Return all Ops Console domain routers."""
    return _ROUTERS
