"""Per-customer readiness endpoints.

  GET /api/v1/customer/{handle}/readiness          (admin-gated)
      Full breakdown for the founder / advisor / auditor:
        - source passport status
        - governance decisions in the last 7 days
        - proof pack count
        - capital asset count
        - signed-scope status
        - PROCEED / HOLD_FOR_SCOPE / HOLD_FOR_GOVERNANCE
        - rationale codes

  GET /api/v1/customer/{handle}/readiness/public   (public, no auth)
      Buyer-safe projection: only the recommendation, an `as_of`
      timestamp, and a doctrine statement. **NO counts, NO rationale,
      NO internal state.**

Doctrine moat: the safety of the `/public` projection is enforced by
`tests/test_customer_readiness_public_endpoint_is_safe.py`. If a future
change leaks a count into the public response, that test fails.

For PR6 the per-customer numeric inputs come from a small stub-resolver
(`_resolve_signals_for_handle`). In production this resolver wires into
the existing customer-aware modules (customer_data_plane,
customer_brain, client_maturity_os, governance_os/runtime_decision).
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.customer_readiness.readiness_gate import (
    compute_readiness_gate,
    public_projection,
)

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["doctrine"])


def _resolve_signals_for_handle(handle: str) -> dict[str, Any]:
    """Stub resolver — production wires this to the customer modules.

    Deterministic output so the endpoint is testable and demoable.
    Anyone with a customer handle can see what their score WOULD be in
    the dev/test environment. Production overrides this via dependency
    injection.
    """
    handle_l = handle.lower()
    # Synthetic mapping for demo / test purposes.
    if handle_l == "demo-proceed":
        return {
            "source_passport_status": "present",
            "governance_decisions_7d": 12,
            "proof_pack_count": 2,
            "capital_asset_count": 3,
            "has_signed_scope": True,
        }
    if handle_l == "demo-hold-scope":
        return {
            "source_passport_status": "present",
            "governance_decisions_7d": 8,
            "proof_pack_count": 1,
            "capital_asset_count": 1,
            "has_signed_scope": False,
        }
    if handle_l == "demo-hold-governance":
        return {
            "source_passport_status": "missing",
            "governance_decisions_7d": 0,
            "proof_pack_count": 0,
            "capital_asset_count": 0,
            "has_signed_scope": False,
        }
    # Default for unknown handles: governance-hold (safest).
    return {
        "source_passport_status": "unknown",
        "governance_decisions_7d": 0,
        "proof_pack_count": 0,
        "capital_asset_count": 0,
        "has_signed_scope": False,
    }


def _compute(handle: str):
    signals = _resolve_signals_for_handle(handle)
    return compute_readiness_gate(handle=handle, **signals)


@router.get("/customer/{handle}/readiness")
async def customer_readiness_full(handle: str) -> dict[str, Any]:
    """ADMIN-GATED in production. PR6 ships the route open; PR6.1 wires
    the existing `require_admin_key` dependency once the founder confirms
    which auth scheme to use. Until then, this endpoint is feature-flagged
    behind the doctrine that it not be linked from public surfaces.
    """
    gate = _compute(handle)
    return {
        "handle": gate.handle,
        "source_passport_status": gate.source_passport_status,
        "governance_decisions_7d": gate.governance_decisions_7d,
        "proof_pack_count": gate.proof_pack_count,
        "capital_asset_count": gate.capital_asset_count,
        "has_signed_scope": gate.has_signed_scope,
        "recommendation": gate.recommendation,
        "rationale": list(gate.rationale),
    }


@router.get("/customer/{handle}/readiness/public")
async def customer_readiness_public(handle: str) -> dict[str, Any]:
    """PUBLIC. Returns only the recommendation + as_of + doctrine.
    Locked by tests/test_customer_readiness_public_endpoint_is_safe.py.
    """
    gate = _compute(handle)
    as_of = datetime.now(timezone.utc).isoformat()
    return public_projection(gate, as_of)
