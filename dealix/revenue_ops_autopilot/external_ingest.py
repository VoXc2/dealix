"""Bridge Postgres LeadRecord (Meta/Google webhooks) into governed autopilot ledger."""

from __future__ import annotations

import logging
from typing import Any

from dealix.revenue_ops_autopilot.orchestrator import get_default_orchestrator
from dealix.revenue_ops_autopilot.schemas import FunnelLeadRecord
from dealix.revenue_ops_autopilot.store import AutopilotJSONStore, get_autopilot_store

log = logging.getLogger(__name__)

def autopilot_id_for_pg_lead(pg_lead_id: str) -> str:
    safe = "".join(c if c.isalnum() or c in "_-" else "_" for c in pg_lead_id.strip())
    return f"lea_ext_{safe[:48]}"


def postgres_row_to_capture_payload(
    *,
    pg_lead_id: str,
    source: str,
    contact_name: str = "",
    contact_email: str | None = None,
    contact_phone: str | None = None,
    company_name: str = "",
    region: str | None = None,
    sector: str | None = None,
    message: str | None = None,
    utm_campaign: str | None = None,
    utm_medium: str | None = None,
    utm_source: str | None = None,
) -> dict[str, Any]:
    src = source.strip() or "external_inbound"
    pain = (message or "").strip()
    if utm_campaign or utm_medium or utm_source:
        tags = [
            f"utm_source={utm_source}" if utm_source else "",
            f"utm_medium={utm_medium}" if utm_medium else "",
            f"utm_campaign={utm_campaign}" if utm_campaign else "",
        ]
        pain = f"{pain} [{' '.join(t for t in tags if t)}]".strip()

    return {
        "id": autopilot_id_for_pg_lead(pg_lead_id),
        "name": contact_name or "",
        "email": contact_email or "",
        "phone": contact_phone or "",
        "company": company_name or "",
        "country": region or "Saudi Arabia",
        "industry": sector or "",
        "source": src,
        "pain": pain,
        "message": pain,
        "hold_stage": False,
        "consent_marketing": True,
    }


def ingest_postgres_lead_fields(
    *,
    pg_lead_id: str,
    source: str,
    contact_name: str = "",
    contact_email: str | None = None,
    contact_phone: str | None = None,
    company_name: str = "",
    region: str | None = None,
    sector: str | None = None,
    message: str | None = None,
    utm_campaign: str | None = None,
    utm_medium: str | None = None,
    utm_source: str | None = None,
    store: AutopilotJSONStore | None = None,
) -> FunnelLeadRecord:
    """Idempotent capture into autopilot JSON ledger + lead_captured evidence."""

    st = store or get_autopilot_store()
    payload = postgres_row_to_capture_payload(
        pg_lead_id=pg_lead_id,
        source=source,
        contact_name=contact_name,
        contact_email=contact_email,
        contact_phone=contact_phone,
        company_name=company_name,
        region=region,
        sector=sector,
        message=message,
        utm_campaign=utm_campaign,
        utm_medium=utm_medium,
        utm_source=utm_source,
    )
    aid = str(payload["id"])
    existing = st.get_lead(aid)
    if existing:
        return existing

    orch = get_default_orchestrator(store=st)
    lead = orch.capture_lead(payload)
    from dealix.revenue_ops_autopilot.schemas import EvidenceEvent
    from dealix.revenue_ops_autopilot.store import uid

    st.append_evidence(
        EvidenceEvent(
            id=uid("ev"),
            event_type="external_lead_bridged",
            entity_type="funnel_lead",
            entity_id=lead.id,
            source="external_ingest",
            summary=f"pg_id={pg_lead_id} source={source}",
        ),
    )
    return lead


def ingest_lead_record_model(lead: Any, store: AutopilotJSONStore | None = None) -> FunnelLeadRecord:
    """Accept SQLAlchemy LeadRecord or dict-like row."""

    meta = getattr(lead, "meta_json", None) or getattr(lead, "metadata", None) or {}
    if not isinstance(meta, dict):
        meta = {}
    utm_raw = meta.get("utm")
    utm: dict[str, Any] = utm_raw if isinstance(utm_raw, dict) else {}

    return ingest_postgres_lead_fields(
        pg_lead_id=str(getattr(lead, "id", "")),
        source=str(getattr(lead, "source", "external_inbound")),
        contact_name=str(getattr(lead, "contact_name", "") or ""),
        contact_email=getattr(lead, "contact_email", None),
        contact_phone=getattr(lead, "contact_phone", None),
        company_name=str(getattr(lead, "company_name", "") or ""),
        region=getattr(lead, "region", None),
        sector=getattr(lead, "sector", None),
        message=getattr(lead, "message", None),
        utm_campaign=utm.get("utm_campaign"),
        utm_medium=utm.get("utm_medium"),
        utm_source=utm.get("utm_source"),
        store=store,
    )
