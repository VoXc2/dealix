"""War Room outreach status ↔ funnel LeadStage mapping (deterministic)."""

from __future__ import annotations

from dealix.revenue_ops_autopilot.schemas import LeadStage, WarRoomOutreachStatus

# Doc: docs/ops/WAR_ROOM_STATUS_MAPPING_AR.md
STAGE_TO_WAR_ROOM: dict[LeadStage, WarRoomOutreachStatus] = {
    "new_lead": "not_contacted",
    "qualified_A": "message_drafted",
    "qualified_B": "message_drafted",
    "nurture": "not_contacted",
    "partner_candidate": "message_drafted",
    "meeting_booked": "meeting_booked",
    "meeting_done": "meeting_booked",
    "scope_requested": "scope_requested",
    "scope_sent": "scope_requested",
    "invoice_sent": "invoice_sent",
    "invoice_paid": "paid",
    "delivery_started": "delivery_started",
    "proof_pack_sent": "proof_pack_delivered",
    "sprint_candidate": "upsell_candidate",
    "retainer_candidate": "upsell_candidate",
    "closed_lost": "closed_lost",
}

WAR_ROOM_TO_STAGE: dict[WarRoomOutreachStatus, LeadStage] = {
    "not_contacted": "new_lead",
    "message_drafted": "qualified_B",
    "approved_to_send": "qualified_A",
    "sent_manual": "qualified_A",
    "replied": "qualified_A",
    "proof_pack_sent": "qualified_A",
    "meeting_booked": "meeting_booked",
    "scope_requested": "scope_requested",
    "invoice_sent": "invoice_sent",
    "paid": "invoice_paid",
    "delivery_started": "delivery_started",
    "proof_pack_delivered": "proof_pack_sent",
    "upsell_candidate": "sprint_candidate",
    "referral_requested": "retainer_candidate",
    "closed_lost": "closed_lost",
}
