"""Process inbound HubSpot / Calendly webhooks into autopilot ledger."""

from __future__ import annotations

import os
from datetime import UTC, datetime
from typing import Any

from dealix.revenue_ops_autopilot.schemas import FunnelLeadRecord, LeadStage
from dealix.revenue_ops_autopilot.store import get_autopilot_store
from dealix.revenue_ops_autopilot.war_room import normalize_lead, sync_stage_from_war_room


def _append_ev(ev_type: str, summary: str, entity_id: str) -> None:
    from dealix.revenue_ops_autopilot.schemas import EvidenceEvent
    from dealix.revenue_ops_autopilot.store import get_autopilot_store, uid

    get_autopilot_store().append_evidence(
        EvidenceEvent(
            id=uid("ev"),
            event_type=ev_type,
            entity_type="funnel_lead",
            entity_id=entity_id,
            source="webhook_handlers",
            summary=summary,
        ),
    )


def _find_lead_by_email(email: str) -> FunnelLeadRecord | None:
    if not email or "@" not in email:
        return None
    em = email.strip().lower()
    for lead in get_autopilot_store().list_leads(limit=2000):
        if (lead.email or "").strip().lower() == em:
            return lead
    return None


def handle_calendly_webhook(payload: dict[str, Any]) -> dict[str, Any]:
    """Map invitee.created → demo_booked evidence + stage meeting_booked."""
    event = str(payload.get("event") or payload.get("type") or "")
    if event not in {"invitee.created", "invitee_created"}:
        return {"ok": True, "handled": False, "event": event}

    invitee = payload.get("payload") or {}
    if isinstance(invitee, dict) and "invitee" in invitee:
        invitee = invitee.get("invitee") or invitee
    email = ""
    name = ""
    if isinstance(invitee, dict):
        email = str(invitee.get("email") or "").strip()
        name = str(invitee.get("name") or "").strip()

    store = get_autopilot_store()
    lead = _find_lead_by_email(email)
    if not lead and email:
        from dealix.revenue_ops_autopilot.orchestrator import get_default_orchestrator

        lead = get_default_orchestrator().capture_lead(
            {
                "name": name or email.split("@")[0],
                "email": email,
                "company": name or "Calendly booking",
                "source": "calendly_webhook",
                "hold_stage": False,
            },
        )

    if not lead:
        return {"ok": True, "handled": False, "reason": "no_lead_match"}

    nl = normalize_lead(lead).model_copy(
        update={
            "stage": "meeting_booked",
            "war_room_status": "meeting_booked",
            "updated_at": datetime.now(UTC),
        },
    )
    store.upsert_lead(nl)
    _append_ev("demo_booked", f"Calendly · {email or name}", nl.id)

    try:
        from dealix.revenue_ops_autopilot.crm_bridge import sync_lead_to_hubspot

        sync_lead_to_hubspot(nl, store=store)
    except Exception:
        pass

    return {"ok": True, "handled": True, "lead_id": nl.id, "event": event}


_HUBSPOT_STAGE_TO_FUNNEL: dict[str, LeadStage] = {
    "appointmentscheduled": "meeting_booked",
    "qualifiedtobuy": "qualified_A",
    "presentationscheduled": "meeting_done",
    "decisionmakerboughtin": "scope_sent",
    "contractsent": "invoice_sent",
    "closedwon": "invoice_paid",
    "closedlost": "closed_lost",
}


def handle_hubspot_webhook(payload: dict[str, Any]) -> dict[str, Any]:
    """Best-effort HubSpot subscription events → ledger stage sync."""
    events = payload if isinstance(payload, list) else [payload]
    handled = 0
    store = get_autopilot_store()

    for ev in events:
        if not isinstance(ev, dict):
            continue
        sub_type = str(ev.get("subscriptionType") or ev.get("eventType") or "")
        if "deal.propertyChange" not in sub_type and "deal.creation" not in sub_type:
            continue
        props = ev.get("properties") or {}
        deal_stage = str(props.get("dealstage") or props.get("hs_deal_stage") or "").lower()
        deal_id = str(ev.get("objectId") or props.get("hs_object_id") or "")
        target_stage = _HUBSPOT_STAGE_TO_FUNNEL.get(deal_stage)
        if not target_stage:
            continue

        lead: FunnelLeadRecord | None = None
        for L in store.list_leads(limit=2000):
            if L.hubspot_deal_id and str(L.hubspot_deal_id) == deal_id:
                lead = L
                break
        if not lead:
            continue

        nl = lead.model_copy(update={"stage": target_stage, "updated_at": datetime.now(UTC)})
        store.upsert_lead(nl)
        _append_ev("crm_stage_synced", f"HubSpot {deal_stage}→{target_stage}", nl.id)
        handled += 1

    return {"ok": True, "handled": handled}


def calendly_url() -> str:
    return os.environ.get(
        "CALENDLY_URL",
        "https://calendly.com/sami-assiri11/dealix-demo",
    )
