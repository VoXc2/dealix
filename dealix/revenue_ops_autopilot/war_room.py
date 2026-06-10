"""War Room list filters, outreach transitions, daily summary."""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any

from dealix.revenue_ops_autopilot.schemas import FunnelLeadRecord, WarRoomOutreachStatus
from dealix.revenue_ops_autopilot.war_room_mapping import STAGE_TO_WAR_ROOM, WAR_ROOM_TO_STAGE

OUTREACH_ORDER: tuple[WarRoomOutreachStatus, ...] = (
    "not_contacted",
    "message_drafted",
    "approved_to_send",
    "sent_manual",
    "replied",
    "proof_pack_sent",
    "meeting_booked",
    "scope_requested",
    "invoice_sent",
    "paid",
    "delivery_started",
    "proof_pack_delivered",
    "upsell_candidate",
    "referral_requested",
    "closed_lost",
)

CRITICAL_OUTREACH_EVENTS: dict[WarRoomOutreachStatus, str] = {
    "approved_to_send": "war_room_approved_to_send",
    "sent_manual": "war_room_sent_manual",
    "meeting_booked": "war_room_meeting_booked",
    "paid": "war_room_payment_logged",
    "proof_pack_delivered": "war_room_proof_delivered",
    "closed_lost": "war_room_closed_lost",
}


def _outreach_idx(status: WarRoomOutreachStatus) -> int:
    try:
        return OUTREACH_ORDER.index(status)
    except ValueError:
        return -1


def normalize_lead(lead: FunnelLeadRecord) -> FunnelLeadRecord:
    """Backfill war-room fields for JSON records written before the extension."""
    updates: dict[str, Any] = {}
    mapped = STAGE_TO_WAR_ROOM.get(lead.stage, "not_contacted")
    if lead.war_room_status not in OUTREACH_ORDER or _outreach_idx(mapped) > _outreach_idx(lead.war_room_status):
        updates["war_room_status"] = mapped
    if not lead.pain_hypothesis.strip() and lead.pain.strip():
        updates["pain_hypothesis"] = lead.pain.strip()
    if not lead.segment.strip():
        seg = lead.industry.strip() or lead.source.strip()
        if "partner" in lead.source.lower() or lead.stage == "partner_candidate":
            seg = seg or "agency_partner"
        updates["segment"] = seg
    if not lead.next_action.strip() and lead.next_action_hint_ar.strip():
        updates["next_action"] = lead.next_action_hint_ar.strip()
    if updates:
        return lead.model_copy(update=updates)
    return lead


def outreach_transition_allowed(
    current: WarRoomOutreachStatus,
    target: WarRoomOutreachStatus,
    *,
    has_payment_proof: bool = False,
) -> tuple[bool, str]:
    if target == "closed_lost":
        return True, "ok_closed_lost"
    if _outreach_idx(target) < _outreach_idx(current) and current != "closed_lost":
        return False, "backward_outreach_blocked"
    if target == "sent_manual" and current not in {"approved_to_send", "sent_manual"}:
        return False, "needs_approved_before_sent_manual"
    if target == "paid" and not has_payment_proof:
        return False, "needs_payment_proof"
    return True, "ok"


def war_room_row(lead: FunnelLeadRecord) -> dict[str, Any]:
    """Seven-column War Room view for API/UI."""
    L = normalize_lead(lead)
    target = L.company.strip() or L.name.strip() or L.email.strip() or L.id
    return {
        "lead_id": L.id,
        "target": target,
        "segment": L.segment,
        "pain_hypothesis": L.pain_hypothesis or L.pain,
        "offer": L.offer_id,
        "proof_asset": L.proof_asset,
        "next_action": L.next_action or L.next_action_hint_ar,
        "next_action_due": L.next_action_due,
        "status": L.war_room_status,
        "lead_score": L.lead_score,
        "stage": L.stage,
        "source": L.source,
        "email": L.email,
        "updated_at": L.updated_at.isoformat(),
    }


def _due_today(lead: FunnelLeadRecord, today: date) -> bool:
    if not lead.next_action_due:
        return False
    try:
        due = date.fromisoformat(lead.next_action_due[:10])
    except ValueError:
        return False
    return due <= today


def filter_leads(
    leads: list[FunnelLeadRecord],
    *,
    due_today: bool = False,
    needs_follow_up: bool = False,
    status_in: list[str] | None = None,
    top_n: int | None = None,
) -> list[FunnelLeadRecord]:
    today = datetime.now(UTC).date()
    normalized = [normalize_lead(L) for L in leads]
    out = normalized

    if status_in:
        allowed = set(status_in)
        out = [L for L in out if L.war_room_status in allowed]

    if due_today:
        out = [L for L in out if _due_today(L, today)]

    if needs_follow_up:
        follow_statuses = {
            "message_drafted",
            "approved_to_send",
            "sent_manual",
            "replied",
            "proof_pack_sent",
            "meeting_booked",
        }
        out = [
            L
            for L in out
            if L.war_room_status in follow_statuses or _due_today(L, today)
        ]

    out.sort(key=lambda x: (x.lead_score, x.updated_at), reverse=True)
    if top_n is not None:
        out = out[:top_n]
    return out


def build_daily_summary(leads: list[FunnelLeadRecord]) -> dict[str, Any]:
    today = datetime.now(UTC).date()
    normalized = [normalize_lead(L) for L in leads]
    active = [L for L in normalized if L.war_room_status != "closed_lost"]

    top_ten = filter_leads(active, top_n=10)
    follow = filter_leads(active, needs_follow_up=True, top_n=50)

    def _count(status: WarRoomOutreachStatus) -> int:
        return sum(1 for L in active if L.war_room_status == status)

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "today": {
            "approved_touches_target": 10,
            "follow_ups_target": 5,
            "top_targets_count": len(top_ten),
            "follow_ups_due": len([L for L in follow if _due_today(L, today)]),
        },
        "revenue": {
            "conversations": _count("replied") + _count("sent_manual"),
            "meetings": _count("meeting_booked"),
            "scopes": _count("scope_requested"),
            "invoices": _count("invoice_sent"),
            "paid": _count("paid"),
        },
        "queues": {
            "needs_proof": _count("replied") + _count("proof_pack_sent"),
            "ready_meeting": _count("proof_pack_sent"),
            "needs_scope": _count("meeting_booked"),
            "needs_invoice": _count("scope_requested"),
            "needs_delivery": _count("paid") + _count("delivery_started"),
            "upsell": _count("upsell_candidate"),
        },
        "risks": {
            "no_live_auto_send": True,
            "no_cold_whatsapp": True,
            "no_fake_proof": True,
            "no_revenue_claim_before_payment": True,
        },
        "top_targets": [war_room_row(L) for L in top_ten],
    }


def sync_stage_from_war_room(status: WarRoomOutreachStatus) -> str:
    return WAR_ROOM_TO_STAGE.get(status, "qualified_B")
