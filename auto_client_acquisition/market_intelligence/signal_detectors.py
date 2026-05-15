"""
Signal detectors — pure functions over raw observations.

Production: each detector has a real source adapter (LinkedIn jobs API,
Wayback Machine for diffs, Google Ads transparency, Saudi tender feed,
funding announcement RSS, etc.). The detector itself just sees normalized
input + emits a typed SignalDetection.

This module exposes 5 core detectors. More can be added as the catalog
of adapters grows.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta, timezone
from typing import Any

# ── Signal taxonomy — 23 signal types Dealix tracks (Wave 12.5 §33.2.1) ──
# Original 16 (Wave 8) + 7 new founder-vision signals (Engine 1 v2).
SIGNAL_TYPES: tuple[str, ...] = (
    "hiring_sales_rep",
    "hiring_marketing",
    "hiring_engineering",
    "new_branch_opened",
    "new_service_launched",
    "booking_page_added",
    "whatsapp_business_added",
    "ads_volume_increased",
    "website_redesigned",
    "exhibition_participation",
    "negative_review_spike",
    "sector_pulse_rising",
    "tender_published",
    "leadership_change",
    "funding_round",
    "vision2030_alignment",
    # Wave 12.5 §33.2.1 — 7 new founder-vision signals
    "weak_website",                    # Lighthouse score ≤50 OR slow load
    "whatsapp_no_followup_system",     # WhatsApp Business present but no CRM
    "review_surge",                    # Sudden Google review volume spike
    "agency_no_proof",                 # Agency claims clients but shows no case studies
    "high_ticket_b2b_no_sales_process", # >50K SAR offer but no formal sales motion
    "unused_leads_dormant",             # Leads in CRM not contacted in 60+ days
    "zatca_phase_2_eligible",           # SAR turnover in Wave 24 bracket (>375K)
)


# ── Per-signal output schema (Wave 12.5 §33.2.1) ─────────────────────
# Maps each signal_type to the 6 founder-vision output fields:
# business_pain · best_offer · risk · safe_channel · recommended_action · proof_target
# Used by opportunity_feed.py to enrich SignalDetection with actionable context.
SIGNAL_OUTPUT_SCHEMA: dict[str, dict[str, str]] = {
    "hiring_sales_rep": {
        "business_pain": "expanding sales team — pipeline pressure rising",
        "best_offer": "Revenue Proof Sprint",
        "risk": "no consent for outbound; reach via warm intro only",
        "safe_channel": "manual_linkedin_or_warm_intro",
        "recommended_action": "prepare_diagnostic_for_sales_leader",
        "proof_target": "demo_booked",
    },
    "hiring_marketing": {
        "business_pain": "growth motion forming — needs attribution + funnels",
        "best_offer": "Growth Ops Monthly",
        "risk": "no consent for outbound; reach via warm intro only",
        "safe_channel": "manual_linkedin_or_warm_intro",
        "recommended_action": "prepare_diagnostic_for_growth_leader",
        "proof_target": "demo_booked",
    },
    "hiring_engineering": {
        "business_pain": "scaling team — technical debt likely",
        "best_offer": "Data-to-Revenue Pack",
        "risk": "may be technical buyer (longer cycle)",
        "safe_channel": "manual_linkedin_or_warm_intro",
        "recommended_action": "low_priority_nurture",
        "proof_target": "diagnostic_delivered",
    },
    "new_branch_opened": {
        "business_pain": "geographic expansion — need lead routing",
        "best_offer": "Revenue Proof Sprint",
        "risk": "validate physical presence first",
        "safe_channel": "manual_warm_intro_via_partner",
        "recommended_action": "prepare_market_audit",
        "proof_target": "demo_booked",
    },
    "new_service_launched": {
        "business_pain": "needs go-to-market velocity for new offering",
        "best_offer": "Revenue Proof Sprint",
        "risk": "messaging may not be finalized",
        "safe_channel": "manual_linkedin_or_warm_intro",
        "recommended_action": "prepare_offer_audit",
        "proof_target": "demo_booked",
    },
    "booking_page_added": {
        "business_pain": "ready for inbound — may need conversion optimization",
        "best_offer": "Mini Diagnostic",
        "risk": "low — indicates buying motion",
        "safe_channel": "warm_inbound",
        "recommended_action": "send_diagnostic_offer",
        "proof_target": "diagnostic_delivered",
    },
    "whatsapp_business_added": {
        "business_pain": "manual WhatsApp ops — no follow-up system",
        "best_offer": "Growth Ops Monthly",
        "risk": "verify consent posture before any outreach",
        "safe_channel": "manual_inbound_only",
        "recommended_action": "wait_for_inbound_then_diagnostic",
        "proof_target": "inbound_reply_received",
    },
    "ads_volume_increased": {
        "business_pain": "active acquisition — needs attribution",
        "best_offer": "Growth Ops Monthly",
        "risk": "validate ad spend > 5K SAR/mo first",
        "safe_channel": "manual_linkedin_or_warm_intro",
        "recommended_action": "prepare_attribution_audit",
        "proof_target": "demo_booked",
    },
    "website_redesigned": {
        "business_pain": "rebrand or repositioning — likely budget cycle",
        "best_offer": "Mini Diagnostic",
        "risk": "may be in build mode; defer",
        "safe_channel": "manual_warm_intro",
        "recommended_action": "low_priority_nurture",
        "proof_target": "diagnostic_delivered",
    },
    "exhibition_participation": {
        "business_pain": "in-market timing — need follow-up automation",
        "best_offer": "Data-to-Revenue Pack",
        "risk": "high — many vendors compete post-event",
        "safe_channel": "manual_warm_intro_via_event_organizer",
        "recommended_action": "prepare_event_followup_offer",
        "proof_target": "demo_booked",
    },
    "negative_review_spike": {
        "business_pain": "customer experience crisis — needs Support OS",
        "best_offer": "Support OS",
        "risk": "high — they may be defensive",
        "safe_channel": "manual_warm_intro",
        "recommended_action": "prepare_support_audit",
        "proof_target": "diagnostic_delivered",
    },
    "sector_pulse_rising": {
        "business_pain": "sector tailwind — competitors moving fast",
        "best_offer": "Revenue Proof Sprint",
        "risk": "low — broad timing",
        "safe_channel": "manual_linkedin_or_warm_intro",
        "recommended_action": "prepare_sector_audit",
        "proof_target": "demo_booked",
    },
    "tender_published": {
        "business_pain": "active procurement — need bid support",
        "best_offer": "Custom (out of standard catalog)",
        "risk": "tender process is formal — may not fit Dealix scope",
        "safe_channel": "official_tender_response_only",
        "recommended_action": "evaluate_fit_then_decline_or_refer",
        "proof_target": "evaluation_completed",
    },
    "leadership_change": {
        "business_pain": "new leadership = new strategy = budget review",
        "best_offer": "Mini Diagnostic",
        "risk": "high — new leader may have own vendors",
        "safe_channel": "manual_warm_intro_via_mutual_contact",
        "recommended_action": "prepare_intro_diagnostic",
        "proof_target": "intro_meeting_booked",
    },
    "funding_round": {
        "business_pain": "growth pressure post-funding",
        "best_offer": "Executive Command Center",
        "risk": "competing for attention — many vendors will reach out",
        "safe_channel": "manual_warm_intro_via_investor",
        "recommended_action": "prepare_growth_audit",
        "proof_target": "demo_booked",
    },
    "vision2030_alignment": {
        "business_pain": "needs Saudi-aligned positioning",
        "best_offer": "Mini Diagnostic",
        "risk": "low — broad signal",
        "safe_channel": "manual_linkedin_or_warm_intro",
        "recommended_action": "prepare_vision2030_audit",
        "proof_target": "diagnostic_delivered",
    },
    # Wave 12.5 §33.2.1 — 7 new founder-vision signals
    "weak_website": {
        "business_pain": "website dragging conversion — high bounce rate likely",
        "best_offer": "Mini Diagnostic",
        "risk": "low — non-controversial entry",
        "safe_channel": "manual_warm_intro",
        "recommended_action": "prepare_website_audit",
        "proof_target": "diagnostic_delivered",
    },
    "whatsapp_no_followup_system": {
        "business_pain": "WhatsApp messages drop — no CRM follow-up",
        "best_offer": "Data-to-Revenue Pack",
        "risk": "verify they want a CRM (not all do)",
        "safe_channel": "manual_warm_intro",
        "recommended_action": "prepare_followup_audit",
        "proof_target": "demo_booked",
    },
    "review_surge": {
        "business_pain": "high engagement — customer voice scaling",
        "best_offer": "Support OS",
        "risk": "validate review sentiment first",
        "safe_channel": "manual_warm_intro",
        "recommended_action": "prepare_support_audit",
        "proof_target": "diagnostic_delivered",
    },
    "agency_no_proof": {
        "business_pain": "agency renewal pressure — needs case studies",
        "best_offer": "Agency Partner OS",
        "risk": "low — agencies actively seek proof tools",
        "safe_channel": "manual_warm_intro",
        "recommended_action": "prepare_agency_proof_audit",
        "proof_target": "agency_partnership_call_booked",
    },
    "high_ticket_b2b_no_sales_process": {
        "business_pain": "high-value deals lost to messy sales process",
        "best_offer": "Revenue Proof Sprint",
        "risk": "validate deal-size signal first (don't assume)",
        "safe_channel": "manual_warm_intro",
        "recommended_action": "prepare_sales_process_audit",
        "proof_target": "demo_booked",
    },
    "unused_leads_dormant": {
        "business_pain": "money-on-the-table — leads in CRM going stale",
        "best_offer": "Data-to-Revenue Pack",
        "risk": "leads may be old/unconsented — verify before re-engagement",
        "safe_channel": "manual_inbound_only_no_recontact",
        "recommended_action": "prepare_dormant_lead_audit",
        "proof_target": "data_to_revenue_engagement",
    },
    "zatca_phase_2_eligible": {
        "business_pain": "ZATCA Phase 2 deadline pressure (June 2026 Wave 24)",
        "best_offer": "Compliance + Growth Ops Monthly",
        "risk": "may already have ZATCA solution — verify gap",
        "safe_channel": "manual_warm_intro_via_compliance_angle",
        "recommended_action": "prepare_zatca_readiness_audit",
        "proof_target": "compliance_diagnostic_delivered",
    },
}


def get_signal_output(signal_type: str) -> dict[str, str]:
    """Return the 6-field founder-vision output for a signal type.

    Returns an empty dict for unknown signal types (Article 8 — no
    fabrication of fields the registry doesn't explicitly define).
    """
    return SIGNAL_OUTPUT_SCHEMA.get(signal_type, {})


@dataclass
class SignalDetection:
    """A detected signal — feeds Why-Now? engine + Daily Growth Run."""

    company_id: str
    signal_type: str
    detected_at: datetime
    source: str
    confidence: float          # 0..1
    evidence_url: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)


# ── Hiring Signal Detector ───────────────────────────────────────
def detect_hiring_signal(
    *,
    company_id: str,
    job_postings: list[dict[str, Any]],
    now: datetime | None = None,
) -> list[SignalDetection]:
    """
    Detect sales / marketing / engineering hiring signals.

    Each posting is dict with: title, posted_at (datetime), url.
    """
    n = now or datetime.now(UTC).replace(tzinfo=None)
    out: list[SignalDetection] = []
    for jp in job_postings:
        title = (jp.get("title") or "").lower()
        posted = jp.get("posted_at")
        if not posted:
            continue
        if posted.tzinfo:
            posted = posted.replace(tzinfo=None)
        if (n - posted) > timedelta(days=45):
            continue  # too old to act on

        if any(k in title for k in ("sdr", "sales", "account executive", "ae", "مبيعات")):
            out.append(SignalDetection(
                company_id=company_id,
                signal_type="hiring_sales_rep",
                detected_at=posted,
                source="linkedin_jobs",
                confidence=0.9,
                evidence_url=jp.get("url"),
                payload={"title": jp.get("title")},
            ))
        elif any(k in title for k in ("marketing", "growth", "تسويق")):
            out.append(SignalDetection(
                company_id=company_id,
                signal_type="hiring_marketing",
                detected_at=posted,
                source="linkedin_jobs",
                confidence=0.8,
                evidence_url=jp.get("url"),
                payload={"title": jp.get("title")},
            ))
        elif any(k in title for k in ("engineer", "developer", "backend", "frontend", "مبرمج")):
            out.append(SignalDetection(
                company_id=company_id,
                signal_type="hiring_engineering",
                detected_at=posted,
                source="linkedin_jobs",
                confidence=0.7,
                evidence_url=jp.get("url"),
                payload={"title": jp.get("title")},
            ))
    return out


# ── Website Change Detector ──────────────────────────────────────
def detect_website_change(
    *,
    company_id: str,
    diff: dict[str, Any],
    now: datetime | None = None,
) -> list[SignalDetection]:
    """
    Detect signals from a website diff:
      - new booking page added
      - new pricing page
      - WhatsApp Business widget added
      - new service / product launched
    """
    n = now or datetime.now(UTC).replace(tzinfo=None)
    out: list[SignalDetection] = []
    added_paths = set(diff.get("added_paths", []))
    added_widgets = set(diff.get("added_widgets", []))

    booking_keywords = ("/booking", "/book", "/calendly", "/appointment", "/حجز")
    if any(any(k in p for k in booking_keywords) for p in added_paths):
        out.append(SignalDetection(
            company_id=company_id,
            signal_type="booking_page_added",
            detected_at=n,
            source="website_diff",
            confidence=0.85,
            evidence_url=diff.get("homepage_url"),
            payload={"new_paths": list(added_paths)},
        ))

    if "whatsapp_business" in added_widgets or "whatsapp_chat" in added_widgets:
        out.append(SignalDetection(
            company_id=company_id,
            signal_type="whatsapp_business_added",
            detected_at=n,
            source="website_diff",
            confidence=0.95,
            evidence_url=diff.get("homepage_url"),
            payload={"widgets": list(added_widgets)},
        ))

    service_paths = ("/services/", "/products/", "/خدماتنا/", "/منتجاتنا/")
    new_services = [p for p in added_paths if any(s in p for s in service_paths)]
    if new_services:
        out.append(SignalDetection(
            company_id=company_id,
            signal_type="new_service_launched",
            detected_at=n,
            source="website_diff",
            confidence=0.7,
            evidence_url=diff.get("homepage_url"),
            payload={"new_pages": new_services},
        ))

    if diff.get("major_redesign"):
        out.append(SignalDetection(
            company_id=company_id,
            signal_type="website_redesigned",
            detected_at=n,
            source="website_diff",
            confidence=0.8,
            evidence_url=diff.get("homepage_url"),
        ))

    return out


# ── Ads Volume Detector ──────────────────────────────────────────
def detect_ads_signal(
    *,
    company_id: str,
    weekly_ad_spend_history: list[float],
    now: datetime | None = None,
) -> list[SignalDetection]:
    """
    Detect a meaningful jump in advertising spend.

    weekly_ad_spend_history: most recent week LAST. Need >= 4 weeks of history.
    """
    if len(weekly_ad_spend_history) < 4:
        return []
    n = now or datetime.now(UTC).replace(tzinfo=None)
    recent = weekly_ad_spend_history[-2:]
    baseline = weekly_ad_spend_history[:-2]
    if not baseline or sum(baseline) == 0:
        return []
    baseline_avg = sum(baseline) / len(baseline)
    recent_avg = sum(recent) / len(recent)
    if recent_avg < baseline_avg * 1.4:  # need 40%+ jump
        return []
    pct = round((recent_avg / baseline_avg - 1) * 100, 1)
    return [SignalDetection(
        company_id=company_id,
        signal_type="ads_volume_increased",
        detected_at=n,
        source="ads_transparency_feed",
        confidence=min(0.95, 0.5 + (pct / 200)),
        payload={"increase_pct": pct, "baseline_avg": baseline_avg, "recent_avg": recent_avg},
    )]


# ── Funding Signal Detector ──────────────────────────────────────
def detect_funding_signal(
    *,
    company_id: str,
    announcements: list[dict[str, Any]],
    now: datetime | None = None,
) -> list[SignalDetection]:
    """
    Detect a recent funding announcement.

    announcements: list of {round_type, amount_sar, announced_at, url}
    """
    n = now or datetime.now(UTC).replace(tzinfo=None)
    out: list[SignalDetection] = []
    for a in announcements:
        announced = a.get("announced_at")
        if not announced:
            continue
        if announced.tzinfo:
            announced = announced.replace(tzinfo=None)
        if (n - announced) > timedelta(days=90):
            continue
        out.append(SignalDetection(
            company_id=company_id,
            signal_type="funding_round",
            detected_at=announced,
            source="funding_announcement",
            confidence=0.95,
            evidence_url=a.get("url"),
            payload={
                "round_type": a.get("round_type"),
                "amount_sar": a.get("amount_sar"),
            },
        ))
    return out


# ── Tender Signal Detector ───────────────────────────────────────
def detect_tender_signal(
    *,
    company_id: str,
    tenders: list[dict[str, Any]],
    icp_keywords: tuple[str, ...] = (),
    now: datetime | None = None,
) -> list[SignalDetection]:
    """
    Detect a published government / large-corp tender that matches the ICP.

    tenders: list of {title, body, published_at, deadline, url, value_sar}
    """
    n = now or datetime.now(UTC).replace(tzinfo=None)
    out: list[SignalDetection] = []
    for t in tenders:
        published = t.get("published_at")
        deadline = t.get("deadline")
        if not published:
            continue
        if published.tzinfo:
            published = published.replace(tzinfo=None)
        if deadline and deadline.tzinfo:
            deadline = deadline.replace(tzinfo=None)
        if deadline and deadline < n:
            continue  # already closed
        text = (t.get("title", "") + " " + t.get("body", "")).lower()
        if icp_keywords and not any(kw.lower() in text for kw in icp_keywords):
            continue
        out.append(SignalDetection(
            company_id=company_id,
            signal_type="tender_published",
            detected_at=published,
            source="tender_feed",
            confidence=0.9,
            evidence_url=t.get("url"),
            payload={
                "title": t.get("title"),
                "deadline": deadline.isoformat() if deadline else None,
                "value_sar": t.get("value_sar"),
            },
        ))
    return out
