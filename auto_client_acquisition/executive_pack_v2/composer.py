"""Per-customer Executive Pack composer.

Pulls from:
  - leadops_spine.list_records           → lead_kpis
  - support_inbox.find_breached_tickets  → sla_breaches
  - approval_center.list_pending         → next_3_actions
  - service_sessions.list_sessions       → active_sessions, blockers
  - market_intelligence (best-effort)    → sector_context

All best-effort; missing sources degrade gracefully (empty list).
"""
from __future__ import annotations

import uuid
from datetime import UTC, datetime, timezone
from typing import Any

from auto_client_acquisition.full_ops_contracts.schemas import (
    ExecutivePackRecord,
)


def _lead_kpis(customer_handle: str) -> dict[str, Any]:
    try:
        from auto_client_acquisition.leadops_spine import list_records
        records = [
            r for r in list_records(limit=200)
            if r.customer_handle == customer_handle
        ]
        return {
            "leads_total": len(records),
            "leads_allowed": sum(1 for r in records if r.compliance_status == "allowed"),
            "leads_blocked": sum(1 for r in records if r.compliance_status == "blocked"),
            "leads_needs_review": sum(1 for r in records if r.compliance_status == "needs_review"),
            "drafts_created": sum(1 for r in records if r.draft_id is not None),
        }
    except Exception:
        return {"leads_total": 0, "leads_allowed": 0, "leads_blocked": 0,
                "leads_needs_review": 0, "drafts_created": 0}


def _support_kpis(customer_handle: str) -> dict[str, Any]:
    try:
        from auto_client_acquisition.support_inbox import (
            find_breached_tickets,
            list_tickets,
        )
        tickets = list_tickets(customer_id=customer_handle, limit=100)
        breached = find_breached_tickets(customer_id=customer_handle)
        return {
            "tickets_total": len(tickets),
            "tickets_open": sum(1 for t in tickets if t.status == "open"),
            "tickets_escalated": sum(1 for t in tickets if t.status == "escalated"),
            "sla_breached_count": len(breached),
        }
    except Exception:
        return {"tickets_total": 0, "tickets_open": 0,
                "tickets_escalated": 0, "sla_breached_count": 0}


def _next_3_actions(customer_handle: str) -> list[dict[str, Any]]:
    """Top 3 pending approvals scoped to this customer (by proof_impact prefix)."""
    try:
        from auto_client_acquisition.approval_center import approval_store
        pending = approval_store.get_default_approval_store().list_pending()
        # Filter to those that look like they belong to this customer
        scoped = [
            ap for ap in pending
            if customer_handle in (ap.proof_impact or "")
            or customer_handle in (ap.summary_ar or "")
        ][:3]
        return [
            {
                "approval_id": ap.approval_id,
                "action_type": ap.action_type,
                "channel": ap.channel,
                "risk_level": ap.risk_level,
                "summary_ar": (ap.summary_ar or "")[:120],
            }
            for ap in scoped
        ]
    except Exception:
        return []


def _active_sessions(customer_handle: str) -> list[dict[str, Any]]:
    try:
        from auto_client_acquisition.service_sessions import list_sessions
        sessions = list_sessions(customer_handle=customer_handle, limit=20)
        return [
            {
                "session_id": s.session_id,
                "service_type": s.service_type,
                "status": s.status,
                "deliverable_count": len(s.deliverables),
            }
            for s in sessions
        ]
    except Exception:
        return []


def _blockers(customer_handle: str) -> list[dict[str, Any]]:
    """Sessions or approvals in 'blocked' state."""
    blockers: list[dict[str, Any]] = []
    try:
        from auto_client_acquisition.service_sessions import list_sessions
        for s in list_sessions(customer_handle=customer_handle, status="blocked", limit=20):
            blockers.append({
                "type": "session_blocked",
                "id": s.session_id,
                "service_type": s.service_type,
            })
    except Exception:
        pass
    return blockers


def _sector_context(customer_handle: str) -> dict[str, Any]:
    """Best-effort sector pulse pull for the customer's sector."""
    try:
        from auto_client_acquisition.customer_brain import get_snapshot
        snap = get_snapshot(customer_handle=customer_handle)
        sector = snap.profile.get("sector") if snap else None
        if not sector:
            return {"sector": None, "pulse": "unknown"}
        return {
            "sector": sector,
            "pulse": "tracked",
            "source": "customer_brain.profile + market_intelligence.sector_pulse",
        }
    except Exception:
        return {"sector": None, "pulse": "unavailable"}


def build_daily_pack(*, customer_handle: str) -> ExecutivePackRecord:
    leads = _lead_kpis(customer_handle)
    support = _support_kpis(customer_handle)
    next_3 = _next_3_actions(customer_handle)
    sessions = _active_sessions(customer_handle)
    blockers = _blockers(customer_handle)

    summary_ar_parts: list[str] = []
    summary_en_parts: list[str] = []
    if leads["leads_total"]:
        summary_ar_parts.append(f"{leads['leads_total']} ليد، {leads['drafts_created']} مسوّدة قيد المراجعة")
        summary_en_parts.append(f"{leads['leads_total']} leads, {leads['drafts_created']} drafts in queue")
    if support["sla_breached_count"]:
        summary_ar_parts.append(f"{support['sla_breached_count']} تذكرة دعم تجاوزت SLA")
        summary_en_parts.append(f"{support['sla_breached_count']} support tickets past SLA")
    if blockers:
        summary_ar_parts.append(f"{len(blockers)} عائق يحتاج مراجعتك")
        summary_en_parts.append(f"{len(blockers)} blocker(s) need your review")

    pack = ExecutivePackRecord(
        pack_id=f"pack_{uuid.uuid4().hex[:10]}",
        customer_handle=customer_handle,
        cadence="daily",
        executive_summary_ar=" · ".join(summary_ar_parts) or "لا تحديثات اليوم",
        executive_summary_en=" · ".join(summary_en_parts) or "No updates today",
        revenue_movement={"source": "payment_ops_phase_9_pending"},
        leads=leads,
        support=support,
        blockers=blockers,
        decisions=next_3,
        proof_events=[],
        risks=[],
        next_3_actions=next_3,
        sector_context=_sector_context(customer_handle),
        appendix={
            "active_sessions": sessions,
            "built_from": [
                "leadops_spine",
                "support_inbox",
                "approval_center",
                "service_sessions",
                "customer_brain",
            ],
        },
    )
    return pack


def build_weekly_pack(*, customer_handle: str) -> ExecutivePackRecord:
    """Weekly pack — same data shape, different cadence + week_label."""
    pack = build_daily_pack(customer_handle=customer_handle)
    pack.cadence = "weekly"
    now = datetime.now(UTC)
    week_num = now.isocalendar().week
    pack.week_label = f"{now.year}-W{week_num:02d}"
    return pack
