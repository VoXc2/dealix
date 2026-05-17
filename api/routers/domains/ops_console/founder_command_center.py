"""Ops Console — Founder Command Center.

غرفة قيادة المؤسس — صورة التشغيل اليوم.

GET /api/v1/ops/command-center
  The daily operating picture: top-3 actions, leads waiting >24h, blocked
  approvals, delivery risks, proof-event counts, pipeline + cash snapshot,
  capital assets registered this week. Read-only; admin-key gated.

All cross-module imports are lazy and wrapped — a missing module degrades a
sub-section to `{"note": "...unavailable"}`, never a 500.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Depends

from api.routers.domains.ops_console._common import governed
from api.security.api_key import require_admin_key

router = APIRouter(
    prefix="/api/v1/ops/command-center",
    tags=["Ops Console — Command Center"],
    dependencies=[Depends(require_admin_key)],
)


def _parse_dt(raw: str) -> datetime | None:
    try:
        dt = datetime.fromisoformat(raw)
    except (ValueError, TypeError):
        return None
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt


def _leads_waiting() -> dict[str, Any]:
    try:
        from auto_client_acquisition.lead_inbox import list_leads

        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        items: list[dict[str, Any]] = []
        for raw in list_leads(limit=200):
            rec = raw if isinstance(raw, dict) else getattr(raw, "__dict__", {})
            created = _parse_dt(str(rec.get("created_at", "")))
            if created is None or created >= cutoff:
                continue
            items.append(
                {
                    "id": rec.get("id") or rec.get("lead_id", ""),
                    "company": rec.get("company") or rec.get("company_name", ""),
                    "sector": rec.get("sector", ""),
                    "created_at": created.isoformat(),
                }
            )
        return {"count": len(items), "items": items[:20]}
    except Exception:  # noqa: BLE001
        return {"count": 0, "items": [], "note": "lead_inbox_unavailable"}


def _blocked_approvals() -> dict[str, Any]:
    try:
        from auto_client_acquisition.approval_center.approval_store import (
            get_default_approval_store,
        )

        store = get_default_approval_store()
        pending = store.list_pending() if hasattr(store, "list_pending") else []
        items: list[dict[str, Any]] = []
        for it in pending[:20]:
            if isinstance(it, dict):
                items.append(it)
            elif hasattr(it, "to_dict"):
                items.append(it.to_dict())
            else:
                items.append({"id": str(getattr(it, "id", ""))})
        return {"count": len(pending), "items": items}
    except Exception:  # noqa: BLE001
        return {"count": 0, "items": [], "note": "approval_center_unavailable"}


def _delivery_risks() -> dict[str, Any]:
    try:
        from auto_client_acquisition.friction_log.aggregator import aggregate

        return aggregate(customer_id="dealix_internal", window_days=7).to_dict()
    except Exception:  # noqa: BLE001
        return {"total": 0, "note": "friction_log_unavailable"}


def _proof_events() -> dict[str, Any]:
    try:
        from auto_client_acquisition.proof_ledger.file_backend import get_default_ledger

        events = get_default_ledger().list_events(limit=200)
        by_type: dict[str, int] = {}
        for e in events:
            key = str(getattr(e, "event_type", "unknown"))
            by_type[key] = by_type.get(key, 0) + 1
        return {"count": len(events), "by_type": by_type}
    except Exception:  # noqa: BLE001
        return {"count": 0, "by_type": {}, "note": "proof_ledger_unavailable"}


def _pipeline() -> dict[str, Any]:
    try:
        from auto_client_acquisition.revenue_pipeline.pipeline import get_default_pipeline
        from auto_client_acquisition.revenue_pipeline.revenue_truth import (
            snapshot_revenue_truth,
        )

        summary = get_default_pipeline().summary()
        snap = snapshot_revenue_truth(pipeline_summary=summary, proof_event_files_count=0)
        return {
            "total_leads": snap.total_leads,
            "commitments": snap.commitments,
            "paid": snap.paid,
            "total_revenue_sar": snap.total_revenue_sar,
            "revenue_live": snap.revenue_live,
            "blockers": list(snap.blockers),
            "next_action_en": snap.next_action_en,
            "next_action_ar": snap.next_action_ar,
        }
    except Exception:  # noqa: BLE001
        return {"note": "revenue_pipeline_unavailable"}


def _capital_this_week() -> dict[str, Any]:
    try:
        from auto_client_acquisition.capital_os.capital_ledger import list_assets

        cutoff = datetime.now(timezone.utc) - timedelta(days=7)
        recent: list[dict[str, Any]] = []
        for a in list_assets(limit=100):
            created = _parse_dt(str(getattr(a, "created_at", "")))
            if created is None or created < cutoff:
                continue
            recent.append(
                {
                    "asset_id": a.asset_id,
                    "asset_type": a.asset_type,
                    "owner": a.owner,
                    "created_at": a.created_at,
                }
            )
        return {"count": len(recent), "items": recent[:20]}
    except Exception:  # noqa: BLE001
        return {"count": 0, "items": [], "note": "capital_ledger_unavailable"}


def _top_3_actions(
    leads: dict[str, Any], approvals: dict[str, Any], risks: dict[str, Any]
) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    if approvals.get("count"):
        n = approvals["count"]
        actions.append(
            {
                "label_en": f"Clear {n} blocked approval(s)",
                "label_ar": f"معالجة {n} موافقة معلّقة",
                "kind": "approval",
            }
        )
    if leads.get("count"):
        n = leads["count"]
        actions.append(
            {
                "label_en": f"Respond to {n} lead(s) waiting over 24h",
                "label_ar": f"الرد على {n} عميل محتمل منتظر أكثر من 24 ساعة",
                "kind": "lead",
            }
        )
    if risks.get("total"):
        n = risks["total"]
        actions.append(
            {
                "label_en": f"Address {n} delivery friction event(s)",
                "label_ar": f"معالجة {n} حدث احتكاك في التسليم",
                "kind": "friction",
            }
        )
    if not actions:
        actions.append(
            {
                "label_en": "No urgent actions — focus on outreach and proof",
                "label_ar": "لا إجراءات عاجلة — ركّز على التواصل وبناء الأدلة",
                "kind": "idle",
            }
        )
    for i, a in enumerate(actions):
        a["priority"] = i + 1
    return actions[:3]


@router.get("")
async def command_center() -> dict[str, Any]:
    """Single consolidated founder operating view."""
    leads = _leads_waiting()
    approvals = _blocked_approvals()
    risks = _delivery_risks()
    return governed(
        {
            "top_3_actions": _top_3_actions(leads, approvals, risks),
            "leads_waiting": leads,
            "blocked_approvals": approvals,
            "delivery_risks": risks,
            "proof_events": _proof_events(),
            "pipeline": _pipeline(),
            "capital_assets_this_week": _capital_this_week(),
        }
    )
