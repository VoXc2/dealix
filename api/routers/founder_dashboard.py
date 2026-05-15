"""Founder dashboard router — the daily/weekly view for the solo founder.

GET /api/v1/founder/dashboard
  Consolidates: leads waiting > 24h, friction events last 7 days, retainer
  renewals due in next 7 days, pending approvals, recent proof events,
  capital assets registered this week. Admin-key gated.

This is the operator-facing "command center" — NOT the public portal.
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Depends

from api.security.api_key import require_admin_key

router = APIRouter(prefix="/api/v1/founder", tags=["founder"])


def _leads_waiting() -> dict[str, Any]:
    try:
        from auto_client_acquisition import lead_inbox
        records = lead_inbox.list_records(limit=200) if hasattr(lead_inbox, "list_records") else []
        if not records:
            return {"count": 0, "items": []}
        cutoff = datetime.now(UTC) - timedelta(hours=24)
        items: list[dict[str, Any]] = []
        for r in records:
            try:
                created = datetime.fromisoformat(getattr(r, "created_at", "") or "")
                if created.tzinfo is None:
                    created = created.replace(tzinfo=UTC)
            except Exception:  # noqa: S112 - skip record with unparsable timestamp
                continue
            if created < cutoff:
                items.append({
                    "id": getattr(r, "id", ""),
                    "name": getattr(r, "name", ""),
                    "company": getattr(r, "company", ""),
                    "sector": getattr(r, "sector", ""),
                    "created_at": created.isoformat(),
                })
        return {"count": len(items), "items": items[:20]}
    except Exception:
        return {"count": 0, "items": [], "note": "lead_inbox_unavailable"}


def _friction_last_7d(customer_id: str | None = None) -> dict[str, Any]:
    try:
        from auto_client_acquisition.friction_log.aggregator import aggregate
        agg = aggregate(customer_id=customer_id or "dealix_internal", window_days=7)
        return agg.to_dict()
    except Exception:
        return {"total": 0, "note": "friction_log_unavailable"}


def _renewals_due() -> dict[str, Any]:
    try:
        from auto_client_acquisition.payment_ops.renewal_scheduler import list_due
        due = list_due()
        return {
            "count": len(due),
            "items": [
                {"customer_id": s.customer_id, "plan": s.plan, "amount_sar": s.amount_sar,
                 "next_attempt_at": s.next_attempt_at, "cycle": s.cycle_count}
                for s in due[:10]
            ],
        }
    except Exception:
        return {"count": 0, "items": [], "note": "renewal_scheduler_unavailable"}


def _pending_approvals() -> dict[str, Any]:
    try:
        from auto_client_acquisition.approval_center.approval_store import (
            get_default_approval_store,
        )
        store = get_default_approval_store()
        items = store.list_pending() if hasattr(store, "list_pending") else []
        return {"count": len(items), "items": items[:20]}
    except Exception:
        return {"count": 0, "items": [], "note": "approval_center_unavailable"}


def _recent_proof_events() -> dict[str, Any]:
    try:
        from auto_client_acquisition.proof_ledger.file_backend import get_default_ledger
        ledger = get_default_ledger()
        events = ledger.list_events(limit=20)
        return {
            "count": len(events),
            "items": [
                {"id": e.id, "event_type": str(e.event_type),
                 "customer_handle": e.customer_handle,
                 "created_at": e.created_at.isoformat()}
                for e in events
            ],
        }
    except Exception:
        return {"count": 0, "items": [], "note": "proof_ledger_unavailable"}


def _capital_this_week() -> dict[str, Any]:
    try:
        from auto_client_acquisition.capital_os.capital_ledger import list_assets
        assets = list_assets(limit=100)
        cutoff = datetime.now(UTC) - timedelta(days=7)
        recent: list[dict[str, Any]] = []
        for a in assets:
            try:
                created = datetime.fromisoformat(a.created_at)
                if created.tzinfo is None:
                    created = created.replace(tzinfo=UTC)
            except Exception:  # noqa: S112 - skip asset with unparsable timestamp
                continue
            if created >= cutoff:
                recent.append({
                    "asset_id": a.asset_id,
                    "asset_type": a.asset_type,
                    "owner": a.owner,
                    "engagement_id": a.engagement_id,
                    "created_at": a.created_at,
                })
        return {"count": len(recent), "items": recent[:20]}
    except Exception:
        return {"count": 0, "items": [], "note": "capital_ledger_unavailable"}


@router.get("/dashboard", dependencies=[Depends(require_admin_key)])
async def founder_dashboard() -> dict[str, Any]:
    """Single consolidated founder view. Admin-key gated."""
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "leads_waiting_24h_plus": _leads_waiting(),
        "friction_last_7d": _friction_last_7d(),
        "renewals_due_next_7d": _renewals_due(),
        "pending_approvals": _pending_approvals(),
        "recent_proof_events": _recent_proof_events(),
        "capital_assets_this_week": _capital_this_week(),
        "governance_decision": "allow",
        "is_estimate": True,
    }


@router.get("/dashboard/{customer_id}", dependencies=[Depends(require_admin_key)])
async def founder_customer_view(customer_id: str) -> dict[str, Any]:
    """Per-customer drill-down."""
    return {
        "customer_id": customer_id,
        "generated_at": datetime.now(UTC).isoformat(),
        "friction_last_30d": _friction_last_7d(customer_id),
        "governance_decision": "allow",
    }
