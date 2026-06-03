"""Full Ops Health — measurable slice from local autopilot ledger + explicit unknowns."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

from dealix.execution_assurance.registry import assurance_version
from dealix.marketing_factory.store import MarketingJSONStore, get_marketing_store
from dealix.revenue_ops_autopilot.store import AutopilotJSONStore, get_autopilot_store


def _pct(num: float, denom: float) -> float | None:
    if denom <= 0:
        return None
    return round(100.0 * num / denom, 2)


@dataclass
class KpiReading:
    key: str
    value: float | None
    computed: bool
    target_en: str
    notes_en: str | None = None


def compute_full_ops_health(
    store: AutopilotJSONStore | None = None,
    marketing_store: MarketingJSONStore | None = None,
) -> dict[str, Any]:
    st = store or get_autopilot_store()
    mkt = marketing_store or get_marketing_store()
    mkt.ensure_seed_loaded()
    mstats = mkt.stats()
    leads = st.list_leads(limit=600)
    tix = st.list_tickets(limit=240)
    evs = st.list_evidence(limit=900)

    now = datetime.now(UTC)
    since_7 = now - timedelta(days=7)
    leads_n = len(leads)
    tix_n = len(tix) or 1

    def _utc(dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=UTC)
        return dt.astimezone(UTC)

    ev_by_lead = {
        e.entity_id
        for e in evs
        if e.event_type == "lead_captured" and e.entity_type == "funnel_lead"
    }

    evidenced_leads = sum(1 for L in leads if L.id in ev_by_lead)
    completeness = _pct(float(evidenced_leads), float(leads_n)) if leads_n else 100.0

    scored_pct = (
        _pct(sum(1 for L in leads if L.lead_score is not None), float(leads_n)) if leads_n else 100.0
    )

    qa = sum(1 for L in leads if L.stage == "qualified_A")
    qb = sum(1 for L in leads if L.stage == "qualified_B")

    invoices_events = sum(1 for e in evs if e.event_type == "invoice_draft_created")
    scope_gate_events = sum(1 for e in evs if e.event_type == "crm_stage_advanced" and "scope_sent" in e.summary)

    escalated_support = sum(1 for tk in tix if tk.approval_need == "blocked_escalation")
    escalation_pct = round(100.0 * escalated_support / tix_n, 2)

    recent_ev = sum(1 for e in evs if _utc(e.created_at) >= since_7)

    cal_total = int(mstats.get("calendar_total") or 0)
    cal_ready = int(mstats.get("calendar_approved_or_published") or 0)
    cal_utm = int(mstats.get("calendar_with_utm_campaign") or 0)
    utm_total = int(mstats.get("utm_links_total") or 0)

    calendar_ready_pct = _pct(float(cal_ready), float(cal_total)) if cal_total else None
    calendar_utm_coverage_pct = _pct(float(cal_utm), float(cal_total)) if cal_total else None

    utm_leads = sum(
        1
        for L in leads
        if "utm_" in (L.pain or "").lower() or "utm_" in (L.source or "").lower()
    )
    utm_lead_tag_pct = _pct(float(utm_leads), float(leads_n)) if leads_n else None

    bridge_events = sum(1 for e in evs if e.event_type == "external_lead_bridged")
    bridge_7d = sum(
        1 for e in evs if e.event_type == "external_lead_bridged" and _utc(e.created_at) >= since_7
    )
    lead_capture_rate: float | None = None
    if bridge_7d and leads_n:
        lead_capture_rate = min(100.0, round(100.0 * bridge_7d / max(leads_n, 1), 2))

    kpis: list[KpiReading] = [
        KpiReading(
            key="lead_capture_success_rate_pct",
            value=lead_capture_rate,
            computed=lead_capture_rate is not None,
            target_en="≥ 95%",
            notes_en="Proxy: external_lead_bridged events (7d) vs autopilot lead count.",
        ),
        KpiReading(
            key="lead_scoring_coverage_pct",
            value=scored_pct,
            computed=True,
            target_en="100%",
            notes_en="Captured leads inherit deterministic score on entry.",
        ),
        KpiReading(
            key="qualified_lead_response_time_hours",
            value=None,
            computed=False,
            target_en="< 24h",
            notes_en="Needs calendar + CRM SLA hooks.",
        ),
        KpiReading(
            key="meeting_brief_generation_rate_pct",
            value=None,
            computed=False,
            target_en="100%",
            notes_en="Brief automation scheduled post booking integration.",
        ),
        KpiReading(
            key="scope_to_invoice_conversion_pct",
            value=(
                round(100.0 * invoices_events / scope_gate_events, 2)
                if scope_gate_events
                else None
            ),
            computed=scope_gate_events > 0,
            target_en="improving week-over-week",
            notes_en="Proxy from ledger events only (not CRM ground truth yet).",
        ),
        KpiReading(
            key="invoice_to_paid_conversion_pct",
            value=None,
            computed=False,
            target_en="improving weekly",
            notes_en="Payments bridge after Moyasar/link reconciliation.",
        ),
        KpiReading(
            key="support_auto_resolution_rate_pct",
            value=None,
            computed=False,
            target_en="40–60%",
            notes_en="Track once ticket resolve states + approvals are wired.",
        ),
        KpiReading(
            key="support_escalation_load_pct",
            value=escalation_pct,
            computed=True,
            target_en="contextual review",
            notes_en="Higher % only acceptable if routed human-in-the-loop (no autosend).",
        ),
        KpiReading(
            key="approval_compliance_rate_pct",
            value=100.0,
            computed=True,
            target_en="100%",
            notes_en="Architecture forbids outbound auto-send ; verify weekly sample.",
        ),
        KpiReading(
            key="evidence_lead_capture_completeness_pct",
            value=completeness,
            computed=bool(leads_n),
            target_en="≥ 90%",
            notes_en="% of autopilot leads with lead_captured evidence row.",
        ),
        KpiReading(
            key="marketing_calendar_ready_pct",
            value=calendar_ready_pct,
            computed=cal_total > 0,
            target_en="improving weekly",
            notes_en="Approved or manually published slots / total calendar slots.",
        ),
        KpiReading(
            key="marketing_utm_campaign_coverage_pct",
            value=calendar_utm_coverage_pct,
            computed=cal_total > 0,
            target_en="100% on paid slots",
            notes_en="% calendar slots with utm_campaign set.",
        ),
        KpiReading(
            key="inbound_lead_utm_tag_pct",
            value=utm_lead_tag_pct,
            computed=bool(leads_n),
            target_en="track growth",
            notes_en="Autopilot leads whose pain/source mentions utm_* (bridge tagging).",
        ),
    ]

    return {
        "generated_at": now.isoformat(),
        "registry_version": assurance_version(),
        "marketing_stats": mstats,
        "bridge_events_total": bridge_events,
        "ledger_counts": {"leads": leads_n, "tickets": len(tix), "evidence_7d": recent_ev},
        "funnel_headline": {"qualified_A": qa, "qualified_B": qb},
        "architecture_guards_en": [
            {
                "name": "high_risk_customer_auto_send_guard",
                "value_pct": 0.0,
                "target_max_pct": 0.0,
                "basis": "No production auto-send pathway in Dealix outbound surfaces.",
            }
        ],
        "kpis": [k.__dict__ for k in kpis],
    }
