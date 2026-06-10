"""Approval Command Center HTTP surface.

Routes every "approval_required" action through one queryable queue
with a uniform shape: pending list, create, approve, reject, edit
(audit-trailed), history. Backed by the in-memory ``ApprovalStore``.

Hard rules (mirrored at module level):
  - No live external send happens here. UI lives elsewhere.
  - "blocked" requests can never be approved (returns 400).
  - Schema is ``extra='forbid'`` so unknown fields surface as 422.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query
from pydantic import ValidationError

from auto_client_acquisition.approval_center import (
    ApprovalRequest,
    get_default_approval_store,
    render_approval_card,
)
from core.logging import get_logger

router = APIRouter(prefix="/api/v1/approvals", tags=["approval-center"])
log = get_logger(__name__)


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "module": "approval_center",
        "backend": "in_memory",
        "swappable_to_redis": True,
        "guardrails": {
            "no_live_send": True,
            "blocked_cannot_be_approved": True,
            "edit_history_append_only": True,
            "no_pii_in_logs": True,
        },
        "endpoints": [
            "/pending",
            "/create",
            "/{approval_id}/approve",
            "/{approval_id}/reject",
            "/{approval_id}/edit",
            "/history",
        ],
    }


@router.get("/pending")
async def pending() -> dict[str, Any]:
    rows = get_default_approval_store().list_pending()
    log.info("approval_center_pending", count=len(rows))
    return {
        "count": len(rows),
        "approvals": [r.model_dump(mode="json") for r in rows],
        "cards": [render_approval_card(r) for r in rows],
    }


@router.post("/create")
async def create(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Create a new approval request. Body must match ``ApprovalRequest``
    minus auto-generated fields. Unknown fields → 422 (extra='forbid')."""
    try:
        req = ApprovalRequest.model_validate(payload)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc
    stored = get_default_approval_store().create(req)
    log.info("approval_center_create", approval_id=stored.approval_id, action_type=stored.action_type)
    return {
        "approval": stored.model_dump(mode="json"),
        "card": render_approval_card(stored),
    }


@router.post("/{approval_id}/approve")
async def approve_endpoint(
    approval_id: str,
    payload: dict[str, Any] = Body(default_factory=dict),
) -> dict[str, Any]:
    who = str(payload.get("who", "")).strip()
    if not who:
        raise HTTPException(status_code=422, detail="'who' is required")
    try:
        stored = get_default_approval_store().approve(approval_id, who)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    log.info("approval_center_approve", approval_id=approval_id, who=who)
    return {
        "approval": stored.model_dump(mode="json"),
        "card": render_approval_card(stored),
    }


@router.post("/{approval_id}/reject")
async def reject_endpoint(
    approval_id: str,
    payload: dict[str, Any] = Body(default_factory=dict),
) -> dict[str, Any]:
    who = str(payload.get("who", "")).strip()
    reason = str(payload.get("reason", "")).strip()
    if not who:
        raise HTTPException(status_code=422, detail="'who' is required")
    if not reason:
        raise HTTPException(status_code=422, detail="'reason' is required")
    try:
        stored = get_default_approval_store().reject(approval_id, who, reason)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    log.info("approval_center_reject", approval_id=approval_id, who=who)
    return {
        "approval": stored.model_dump(mode="json"),
        "card": render_approval_card(stored),
    }


@router.post("/{approval_id}/edit")
async def edit_endpoint(
    approval_id: str,
    payload: dict[str, Any] = Body(default_factory=dict),
) -> dict[str, Any]:
    who = str(payload.get("who", "")).strip()
    patch = payload.get("patch") or {}
    if not who:
        raise HTTPException(status_code=422, detail="'who' is required")
    if not isinstance(patch, dict):
        raise HTTPException(status_code=422, detail="'patch' must be an object")
    try:
        stored = get_default_approval_store().edit(approval_id, who, patch)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "approval": stored.model_dump(mode="json"),
        "card": render_approval_card(stored),
    }


@router.get("/history")
async def history(limit: int = Query(default=50, ge=1, le=500)) -> dict[str, Any]:
    rows = get_default_approval_store().list_history(limit=limit)
    return {
        "count": len(rows),
        "approvals": [r.model_dump(mode="json") for r in rows],
    }


@router.post("/expire-sweep")
async def expire_sweep() -> dict[str, Any]:
    """Sweep pending approvals whose expires_at has passed.

    Designed for a background job; safe to call ad-hoc. Returns count.
    """
    expired = get_default_approval_store().expire_overdue()
    return {
        "expired_count": expired,
        "guardrails": {
            "no_live_send": True,
            "expiry_is_terminal": True,
        },
    }


@router.post("/bulk-approve")
async def bulk_approve(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    """Bulk-approve pending approvals.

    Body: {
      'who': 'founder',
      'proof_impact_prefix': 'leadops:lops_xxxx'  (OR)
      'approval_ids': ['apv_a', 'apv_b']
    }
    """
    who = str(payload.get("who", "")).strip()
    if not who:
        raise HTTPException(status_code=422, detail="'who' is required")
    proof_impact_prefix = payload.get("proof_impact_prefix")
    approval_ids = payload.get("approval_ids")
    if not proof_impact_prefix and not approval_ids:
        raise HTTPException(
            status_code=422,
            detail="either 'proof_impact_prefix' or 'approval_ids' required",
        )
    result = get_default_approval_store().bulk_approve(
        who=who,
        proof_impact_prefix=proof_impact_prefix,
        approval_ids=approval_ids,
    )
    return result
