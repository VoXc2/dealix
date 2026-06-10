"""Import targeting CSV rows into autopilot war-room leads."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from dealix.commercial_ops.targeting_csv import TARGET_FIELDS, load_targets
from dealix.revenue_ops_autopilot.orchestrator import RevenueAutopilotOrchestrator
from dealix.revenue_ops_autopilot.war_room import normalize_lead, sync_stage_from_war_room


def import_target_rows(
    rows: list[dict[str, str]],
    orch: RevenueAutopilotOrchestrator,
    *,
    skip_existing_company: bool = True,
) -> dict[str, Any]:
    created: list[str] = []
    skipped: list[str] = []
    store = orch.store
    existing_companies = {
        (L.company or "").strip().lower()
        for L in store.list_leads(limit=2000)
        if (L.company or "").strip()
    }

    for row in rows:
        company = (row.get("company") or "").strip()
        if not company:
            continue
        if skip_existing_company and company.lower() in existing_companies:
            skipped.append(company)
            continue

        status = (row.get("status") or "not_contacted").strip()
        if status not in {
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
        }:
            status = "not_contacted"

        lead = orch.capture_lead(
            {
                "name": (row.get("contact") or company).strip(),
                "email": f"target+{len(created)}@import.local",
                "company": company,
                "pain": (row.get("pain_hypothesis") or "").strip(),
                "source": f"targeting_import:{row.get('motion', 'A')}",
                "segment": (row.get("segment") or "agency_wedge").strip(),
                "offer_id": (row.get("offer_id") or "ten_lead_audit").strip(),
                "hold_stage": True,
            },
        )
        nl = normalize_lead(lead).model_copy(
            update={
                "war_room_status": status,  # type: ignore[assignment]
                "segment": (row.get("segment") or lead.segment).strip(),
                "pain_hypothesis": (row.get("pain_hypothesis") or lead.pain).strip(),
                "offer_id": (row.get("offer_id") or lead.offer_id).strip(),
                "proof_asset": (row.get("notes") or "")[:120],
                "next_action": (row.get("next_action") or lead.next_action_hint_ar).strip(),
                "next_action_due": (row.get("next_action_date") or None),
                "stage": sync_stage_from_war_room(status),  # type: ignore[arg-type]
                "updated_at": datetime.now(UTC),
            },
        )
        store.upsert_lead(nl)
        created.append(nl.id)
        existing_companies.add(company.lower())

    return {
        "imported": len(created),
        "skipped_duplicates": len(skipped),
        "lead_ids": created,
        "fields_expected": list(TARGET_FIELDS),
    }


def import_default_csv(orch: RevenueAutopilotOrchestrator) -> dict[str, Any]:
    return import_target_rows(load_targets(), orch)
