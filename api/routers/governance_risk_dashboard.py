"""Founder-facing read-only risk + policy snapshot."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.governance_os.policy_registry import (
    forbidden_actions,
    load_policy_registry,
)
from auto_client_acquisition.risk_resilience_os.risk_ledger import (
    RiskValidationError,
    get_default_risk_register,
)
from auto_client_acquisition.risk_resilience_os.risk_register import (
    RISK_TAXONOMY_CATEGORIES,
)
from auto_client_acquisition.service_sessions import list_sessions

router = APIRouter(prefix="/api/v1/governance", tags=["governance"])


def build_risk_dashboard_payload() -> dict[str, Any]:
    """Shared payload for HTTP and founder scorecard (read-only)."""
    sessions = list_sessions(limit=100)
    blocked = sum(1 for s in sessions if s.status == "blocked")
    waiting = sum(1 for s in sessions if s.status == "waiting_for_approval")
    reg = load_policy_registry()
    return {
        "schema_version": 1,
        "policy_registry_version": reg.get("version", 0),
        "forbidden_actions": forbidden_actions(),
        "risk_categories": reg.get("risk_categories", []),
        "service_sessions": {
            "sampled": len(sessions),
            "blocked_count": blocked,
            "waiting_for_approval_count": waiting,
        },
        "related_readonly_endpoints": {
            "business_metrics_board": "/api/v1/metrics",
        },
        "read_only": True,
    }


@router.get("/risk-dashboard")
def get_risk_dashboard() -> dict[str, Any]:
    """Aggregate lightweight signals — read-only, no mutations."""
    return build_risk_dashboard_payload()


# ── Risk Register CRUD ────────────────────────────────────────────


@router.get("/risk-register/categories")
def risk_register_categories() -> dict[str, Any]:
    """The twelve canonical risk taxonomy categories."""
    return {
        "categories": list(RISK_TAXONOMY_CATEGORIES),
        "governance_decision": "allow",
    }


@router.post("/risk-register")
def create_risk(payload: dict = Body(...)) -> dict[str, Any]:
    """Create one Risk Register entry. ``category`` must be a taxonomy value."""
    category = payload.get("category")
    title = payload.get("title")
    if not category or not title:
        raise HTTPException(status_code=422, detail="category + title required")
    try:
        row = get_default_risk_register().add(
            category=str(category),
            title=str(title),
            tenant_id=payload.get("tenant_id"),
            description=str(payload.get("description", "")),
            owner=str(payload.get("owner", "")),
            severity=str(payload.get("severity", "medium")),
            likelihood=str(payload.get("likelihood", "medium")),
            control=str(payload.get("control", "")),
            early_warning_signal=str(payload.get("early_warning_signal", "")),
            response_plan=str(payload.get("response_plan", "")),
            test_or_checklist=str(payload.get("test_or_checklist", "")),
            status=str(payload.get("status", "open")),
            linked_deal_id=payload.get("linked_deal_id"),
            linked_customer_id=payload.get("linked_customer_id"),
            meta_json=payload.get("meta_json"),
        )
    except RiskValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"risk": row, "governance_decision": "allow"}


@router.get("/risk-register")
def list_risks(
    tenant_id: str | None = None,
    category: str | None = None,
    status: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """List active Risk Register entries, newest first."""
    rows = get_default_risk_register().list(
        tenant_id=tenant_id,
        category=category,
        status=status,
        limit=max(1, min(int(limit), 1000)),
    )
    return {"count": len(rows), "risks": rows, "governance_decision": "allow"}


@router.get("/risk-register/{risk_id}")
def get_risk(risk_id: str) -> dict[str, Any]:
    """Fetch one Risk Register entry by id."""
    row = get_default_risk_register().get(risk_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"risk {risk_id!r} not found")
    return {"risk": row, "governance_decision": "allow"}


@router.patch("/risk-register/{risk_id}/status")
def update_risk_status(risk_id: str, payload: dict = Body(...)) -> dict[str, Any]:
    """Update a risk's status."""
    status = payload.get("status")
    if not status:
        raise HTTPException(status_code=422, detail="status required")
    row = get_default_risk_register().update_status(risk_id, str(status))
    if row is None:
        raise HTTPException(status_code=404, detail=f"risk {risk_id!r} not found")
    return {"risk": row, "governance_decision": "allow"}


@router.delete("/risk-register/{risk_id}")
def delete_risk(risk_id: str) -> dict[str, Any]:
    """Soft-delete a Risk Register entry."""
    found = get_default_risk_register().soft_delete(risk_id)
    if not found:
        raise HTTPException(status_code=404, detail=f"risk {risk_id!r} not found")
    return {"deleted": True, "risk_id": risk_id, "governance_decision": "allow"}
