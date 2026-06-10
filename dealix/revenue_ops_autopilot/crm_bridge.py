"""HubSpot sync bridge for Revenue Ops Autopilot leads (best-effort, no auto-send)."""

from __future__ import annotations

import asyncio
from typing import Any

from dealix.revenue_ops_autopilot.schemas import FunnelLeadRecord
from dealix.revenue_ops_autopilot.store import AutopilotJSONStore


def _funnel_to_intake_lead(record: FunnelLeadRecord) -> Any:
    from auto_client_acquisition.agents.intake import Lead, LeadSource, LeadStatus

    status_map = {
        "new_lead": LeadStatus.NEW,
        "qualified_A": LeadStatus.QUALIFIED,
        "qualified_B": LeadStatus.QUALIFIED,
        "meeting_booked": LeadStatus.DISCOVERY,
        "meeting_done": LeadStatus.DISCOVERY,
        "invoice_paid": LeadStatus.WON,
        "closed_lost": LeadStatus.LOST,
    }
    src = LeadSource.WEBSITE
    if "partner" in (record.source or "").lower():
        src = LeadSource.REFERRAL
    elif "api" in (record.source or "").lower() or "import" in (record.source or "").lower():
        src = LeadSource.API
    return Lead(
        id=record.id,
        source=src,
        company_name=record.company,
        contact_name=record.name or record.company,
        contact_email=record.email or None,
        contact_phone=record.phone or None,
        sector=record.industry or None,
        region=record.country or None,
        message=record.pain,
        status=status_map.get(record.stage, LeadStatus.NEW),
    )


async def sync_lead_to_hubspot_async(record: FunnelLeadRecord) -> dict[str, Any]:
    from integrations.hubspot import HubSpotClient

    client = HubSpotClient()
    if not client.configured:
        return {"synced": False, "reason": "hubspot_not_configured"}
    lead = _funnel_to_intake_lead(record)
    result = await client.sync_lead(lead, create_deal=bool(record.company))
    return result.to_dict()


def _run_coro_sync(coro: Any) -> Any:
    import concurrent.futures

    def _runner() -> Any:
        return asyncio.run(coro)

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return _runner()
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(_runner).result(timeout=90)


def sync_lead_to_hubspot(
    record: FunnelLeadRecord,
    store: AutopilotJSONStore | None = None,
) -> dict[str, Any]:
    """Sync funnel lead to HubSpot; persist contact/deal ids on record when successful."""
    from dealix.revenue_ops_autopilot.store import get_autopilot_store

    st = store or get_autopilot_store()
    try:
        out = _run_coro_sync(sync_lead_to_hubspot_async(record))
    except Exception as exc:
        return {"synced": False, "reason": str(exc)}

    if out.get("synced") and (out.get("contact_id") or out.get("deal_id")):
        updated = record.model_copy(
            update={
                "crm_status": "hubspot_synced",
                "hubspot_contact_id": out.get("contact_id") or record.hubspot_contact_id,
                "hubspot_deal_id": out.get("deal_id") or record.hubspot_deal_id,
            },
        )
        st.upsert_lead(updated)
        return {**out, "lead_id": record.id}
    return out


def count_meetings_this_week_from_store(store: AutopilotJSONStore | None = None) -> int:
    """Count demo_booked / meeting evidence in ledger for rolling 7 days."""
    from datetime import UTC, datetime, timedelta

    from dealix.revenue_ops_autopilot.store import get_autopilot_store

    st = store or get_autopilot_store()
    cutoff = datetime.now(UTC) - timedelta(days=7)
    meeting_types = {"demo_booked", "meeting_booked", "founder_meeting_booked", "crm_meeting_booked"}
    n = 0
    for ev in st.list_evidence(limit=500):
        if ev.event_type not in meeting_types:
            continue
        if ev.created_at >= cutoff:
            n += 1
    return n
