"""
Role-OS aliases — convenience endpoints that mirror the role-briefs router.

These exist so the URL matches the natural mental model:
    /api/v1/sales-os/pipeline-snapshot   instead of   ?role=sales_manager
    /api/v1/growth-os/daily-plan         instead of   ?role=growth_manager
    /api/v1/revops/funnel                instead of   ?role=revops
    /api/v1/customer-success/health      instead of   ?role=customer_success
    /api/v1/compliance/blocked-actions   instead of   ?role=compliance

Each is a thin wrapper around the existing role_brief_builder. Defensive —
returns {} with `_errors` rather than 500 if the underlying gather fails.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.revenue_company_os.role_action_policy import list_blocked_for
from auto_client_acquisition.revenue_company_os.role_brief_builder import build
from api.routers.role_briefs import _gather_data

router = APIRouter(tags=["role-os"])


async def _safe_brief(role: str, partner_id: str | None = None) -> dict[str, Any]:
    errors: dict[str, str] = {}
    data: dict[str, Any] = {}
    try:
        data = await _gather_data(role, partner_id=partner_id, customer_id=None)
    except Exception as exc:  # noqa: BLE001
        errors["gather"] = f"{type(exc).__name__}: {str(exc)[:200]}"
    try:
        out = build(role, data=data)
    except Exception as exc:  # noqa: BLE001
        errors["build"] = f"{type(exc).__name__}: {str(exc)[:200]}"
        out = {"role": role, "brief_type": "degraded", "summary": {}, "top_decisions": []}
    if errors:
        out["_errors"] = errors
    return out


@router.get("/api/v1/sales-os/pipeline-snapshot")
async def sales_os_pipeline_snapshot() -> dict[str, Any]:
    """Sales pipeline snapshot — mirror of role-briefs?role=sales_manager."""
    brief = await _safe_brief("sales_manager")
    return {
        "role": "sales_manager",
        "as_of": brief.get("date"),
        "summary": brief.get("summary") or {},
        "by_stage": brief.get("by_stage") or {},
        "top_decisions": brief.get("top_decisions") or [],
        "blocked_today_ar": brief.get("blocked_today_ar") or [],
        **({"_errors": brief["_errors"]} if "_errors" in brief else {}),
    }


@router.get("/api/v1/growth-os/daily-plan")
async def growth_os_daily_plan() -> dict[str, Any]:
    """Growth manager daily plan — mirror of role-briefs?role=growth_manager."""
    brief = await _safe_brief("growth_manager")
    # Also include the deterministic Self-Growth daily plan for richer payload
    sg_plan: dict[str, Any] = {}
    try:
        from auto_client_acquisition.revenue_company_os.self_growth_mode import (
            build_daily_plan, daily_plan_to_dict,
        )
        sg_plan = daily_plan_to_dict(build_daily_plan())
    except Exception as exc:  # noqa: BLE001
        sg_plan = {"_error": f"{type(exc).__name__}: {str(exc)[:120]}"}
    return {
        "role": "growth_manager",
        "as_of": brief.get("date"),
        "summary": brief.get("summary") or {},
        "top_decisions": brief.get("top_decisions") or [],
        "blocked_today_ar": brief.get("blocked_today_ar") or [],
        "self_growth_plan": sg_plan,
        **({"_errors": brief["_errors"]} if "_errors" in brief else {}),
    }


@router.get("/api/v1/revops/funnel")
async def revops_funnel() -> dict[str, Any]:
    """RevOps funnel snapshot — mirror of role-briefs?role=revops."""
    brief = await _safe_brief("revops")
    return {
        "role": "revops",
        "as_of": brief.get("date"),
        "summary": brief.get("summary") or {},
        "funnel_event_counts": (brief.get("summary") or {}).get("funnel_event_counts") or {},
        "top_decisions": brief.get("top_decisions") or [],
        "blocked_today_ar": brief.get("blocked_today_ar") or [],
        **({"_errors": brief["_errors"]} if "_errors" in brief else {}),
    }


@router.get("/api/v1/customer-success/health")
async def customer_success_health() -> dict[str, Any]:
    """CS health summary — mirror of role-briefs?role=customer_success.

    Distinct from /api/v1/customer-success/* (existing router) which is the
    full CS detail surface. This endpoint is the single-shot brief view.
    """
    brief = await _safe_brief("customer_success")
    return {
        "role": "customer_success",
        "as_of": brief.get("date"),
        "summary": brief.get("summary") or {},
        "top_decisions": brief.get("top_decisions") or [],
        "blocked_today_ar": brief.get("blocked_today_ar") or [],
        **({"_errors": brief["_errors"]} if "_errors" in brief else {}),
    }


@router.get("/api/v1/compliance/blocked-actions")
async def compliance_blocked_actions(role: str | None = None) -> dict[str, Any]:
    """Compliance posture — gate state + role-action policy table.

    Returns blocked actions for ALL roles (or one role if ?role= given).
    Useful for the trust center UI + audit reports.
    """
    brief = await _safe_brief("compliance")
    roles = (
        ("ceo", "sales_manager", "growth_manager", "revops", "customer_success",
         "agency_partner", "finance", "compliance", "meeting_intelligence")
        if not role else (role,)
    )
    policy = {r: list_blocked_for(r) for r in roles}
    return {
        "role": "compliance",
        "as_of": brief.get("date"),
        "live_action_gates": (brief.get("summary") or {}).get("gates")
                             or (brief.get("summary") or {}),
        "policy_per_role": policy,
        "top_decisions": brief.get("top_decisions") or [],
        "blocked_today_ar": brief.get("blocked_today_ar") or [],
        **({"_errors": brief["_errors"]} if "_errors" in brief else {}),
    }
