"""
Company Brain — read-only aggregator over existing Dealix models.

Composes:
    CustomerRecord + CompanyRecord + LeadRecord + DealRecord + TaskRecord +
    ConsentRecord/SuppressionRecord + ProofEvent (deploy branch) +
    ServiceSession (deploy branch)

NO new tables. Pure read. Async DB session is optional — if absent we fall
back to a clearly-labeled demo payload, which is useful for tests, smoke
runs, and onboarding screenshots without polluting the database.

Public API:
    await build_company_brain(customer_id, session=None) -> dict
    build_demo_company_brain(customer_id="cust_demo") -> dict   # sync, no DB
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class BrainSource(str, Enum):
    DB = "db"
    DEMO = "demo"
    PARTIAL = "partial"


@dataclass
class _BrainTemplate:
    """Skeleton response — every key is always present."""

    company_name: str = ""
    website: str | None = None
    sector: str | None = None
    city: str | None = None
    offer: str | None = None
    icp: dict[str, Any] | None = None
    language_preference: str = "ar"
    tone_preference: str = "professional_khaliji"
    approved_channels: list[str] = None  # type: ignore[assignment]
    blocked_channels: list[str] = None  # type: ignore[assignment]
    consent_records: list[dict[str, Any]] = None  # type: ignore[assignment]
    current_service: dict[str, Any] | None = None
    open_decisions: list[dict[str, Any]] = None  # type: ignore[assignment]
    proof_summary: dict[str, Any] | None = None
    past_objections: list[dict[str, Any]] = None  # type: ignore[assignment]
    next_best_actions: list[dict[str, Any]] = None  # type: ignore[assignment]


# Channels that are NEVER auto-allowed regardless of toggles. This is part of
# the brain so downstream components can rely on it without reaching into env.
_ALWAYS_BLOCKED_CHANNELS: tuple[str, ...] = (
    "cold_whatsapp",
    "purchased_lists_whatsapp",
    "scraped_lists_whatsapp",
    "cold_call_unverified",
    "linkedin_automation",
)

# Default approved channel mix for a Saudi B2B company. Matches the company
# intake's `channel_plan.auto_send_allowed` defaults but exposes them here so
# the brain answers the question "what is this company allowed to do today?".
_DEFAULT_APPROVED_CHANNELS: tuple[str, ...] = (
    "form_inbound",
    "wa_me_inbound",
    "email_draft_with_approval",
    "linkedin_manual_warm_intro",
    "customer_initiated_whatsapp",
)


def _empty_lists(t: _BrainTemplate) -> _BrainTemplate:
    """Initialize all list fields (avoid mutable defaults)."""
    if t.approved_channels is None:
        t.approved_channels = list(_DEFAULT_APPROVED_CHANNELS)
    if t.blocked_channels is None:
        t.blocked_channels = list(_ALWAYS_BLOCKED_CHANNELS)
    if t.consent_records is None:
        t.consent_records = []
    if t.open_decisions is None:
        t.open_decisions = []
    if t.past_objections is None:
        t.past_objections = []
    if t.next_best_actions is None:
        t.next_best_actions = []
    return t


def _to_dict(t: _BrainTemplate, customer_id: str, source: BrainSource) -> dict[str, Any]:
    return {
        "customer_id": customer_id,
        "source": source.value,
        "company_name": t.company_name,
        "website": t.website,
        "sector": t.sector,
        "city": t.city,
        "offer": t.offer,
        "icp": t.icp or {},
        "language_preference": t.language_preference,
        "tone_preference": t.tone_preference,
        "approved_channels": list(t.approved_channels or _DEFAULT_APPROVED_CHANNELS),
        "blocked_channels": list(t.blocked_channels or _ALWAYS_BLOCKED_CHANNELS),
        "consent_records": list(t.consent_records or []),
        "current_service": t.current_service,
        "open_decisions": list(t.open_decisions or []),
        "proof_summary": t.proof_summary or {
            "pipeline_created_sar": 0.0,
            "qualified_leads": 0,
            "meetings_booked": 0,
            "rwus_emitted": 0,
        },
        "past_objections": list(t.past_objections or []),
        "next_best_actions": list(t.next_best_actions or []),
    }


def build_demo_company_brain(customer_id: str = "cust_demo") -> dict[str, Any]:
    """Sync, no-DB demo brain. Always labelled `source=demo`."""
    t = _empty_lists(_BrainTemplate(
        company_name="Demo Saudi B2B SaaS",
        website="https://example.sa",
        sector="saas",
        city="Riyadh",
        offer="AI sales rep that replies to leads in Arabic within 45s",
        icp={
            "best_segments": ["clinics_riyadh", "real_estate_jeddah", "logistics_eastern"],
            "buying_triggers": ["high lead volume", "WhatsApp inbound", "CRM in use"],
            "decision_makers": ["CEO", "Head of Sales", "Head of Growth"],
        },
        language_preference="ar",
        tone_preference="professional_khaliji",
        current_service={"bundle_id": "growth_starter", "status": "diagnostic_sent"},
        proof_summary={
            "pipeline_created_sar": 0.0,
            "qualified_leads": 0,
            "meetings_booked": 0,
            "rwus_emitted": 0,
            "label": "demo — replace with live data after first run",
        },
        next_best_actions=[
            {"id": "nba_1", "type": "send_diagnostic_to_prospect",
             "title_ar": "أرسل Mini Diagnostic للعميل المحتمل خلال 24 ساعة"},
            {"id": "nba_2", "type": "request_payment_manual",
             "title_ar": "اعرض Pilot 499 عبر تحويل بنكي يدوي — لا تستخدم live charge"},
        ],
    ))
    return _to_dict(t, customer_id, BrainSource.DEMO)


async def build_company_brain(  # noqa: C901 — long but flat
    customer_id: str,
    session: Any = None,
) -> dict[str, Any]:
    """Build a Company Brain payload for a customer.

    If `session` is None or the customer is not found, return the demo brain
    with `source=demo` so callers can render screens without crashing.
    """
    if not customer_id or not isinstance(customer_id, str):
        raise ValueError("customer_id required")

    if session is None:
        return build_demo_company_brain(customer_id)

    # Lazy imports — avoid hard dependency at module import time.
    try:
        from sqlalchemy import select
    except Exception:
        return build_demo_company_brain(customer_id)

    try:
        from db.models import (
            CustomerRecord,
            DealRecord,
            LeadRecord,
        )
    except Exception:
        return build_demo_company_brain(customer_id)

    t = _BrainTemplate()
    _empty_lists(t)
    found_anything = False

    # 1. CustomerRecord — the spine
    try:
        cust = (await session.execute(
            select(CustomerRecord).where(CustomerRecord.id == customer_id)
        )).scalar_one_or_none()
    except Exception:
        cust = None

    if cust:
        found_anything = True
        t.company_name = getattr(cust, "company_name", "") or ""
        t.website = getattr(cust, "website", None)
        t.sector = getattr(cust, "sector", None)
        t.city = getattr(cust, "city", None)

    # 2. CompanyRecord (separate table) — try a name-based join when present
    try:
        from db.models import CompanyRecord  # type: ignore
    except Exception:
        CompanyRecord = None  # type: ignore[assignment]

    company = None
    if CompanyRecord is not None and t.company_name:
        try:
            company = (await session.execute(
                select(CompanyRecord).where(CompanyRecord.name == t.company_name)
            )).scalar_one_or_none()
        except Exception:
            company = None
    if company is not None:
        found_anything = True
        t.website = getattr(company, "website", t.website) or t.website
        t.sector = getattr(company, "industry", t.sector) or t.sector
        t.city = getattr(company, "city", t.city) or t.city
        t.offer = getattr(company, "products", t.offer) or t.offer
        t.icp = getattr(company, "icp_profile", None) or t.icp
        # Tone / channels — fall back to defaults when not set
        t.tone_preference = getattr(company, "tone_of_voice", None) or t.tone_preference
        chan_plan = getattr(company, "channel_plan", None) or {}
        if isinstance(chan_plan, dict):
            allowed = chan_plan.get("auto_send_allowed") or []
            human = chan_plan.get("human_required") or []
            if allowed:
                t.approved_channels = list(allowed) + list(_DEFAULT_APPROVED_CHANNELS)
            if human:
                t.blocked_channels = list(_ALWAYS_BLOCKED_CHANNELS) + list(human)

    # 3. Leads / open decisions
    try:
        leads = (await session.execute(
            select(LeadRecord).limit(20)
        )).scalars().all()
        if leads:
            found_anything = True
            t.open_decisions = [
                {"id": getattr(l, "id", ""), "type": "qualify_lead",
                 "title": getattr(l, "company_name", "") or ""}
                for l in leads[:5]
            ]
    except Exception:
        pass

    # 4. Deals → proof summary baseline
    try:
        deals = (await session.execute(
            select(DealRecord).limit(50)
        )).scalars().all()
    except Exception:
        deals = []

    pipeline_sar = 0.0
    won = 0
    for d in deals or []:
        amt = getattr(d, "amount", None) or getattr(d, "value_sar", None) or 0
        try:
            amt = float(amt or 0)
        except Exception:
            amt = 0.0
        pipeline_sar += amt
        if (getattr(d, "stage", None) or "") in {"won", "paid", "closed_won"}:
            won += 1

    if deals:
        found_anything = True
        t.proof_summary = {
            "pipeline_created_sar": pipeline_sar,
            "qualified_leads": len(deals),
            "deals_won": won,
            "rwus_emitted": 0,  # deploy branch's proof_ledger fills this
        }

    # 5. Always-blocked floor — must include cold_whatsapp regardless of company config
    if "cold_whatsapp" not in (t.blocked_channels or []):
        t.blocked_channels = list(_ALWAYS_BLOCKED_CHANNELS) + list(t.blocked_channels or [])

    # 6. Next best actions — minimal, deterministic, safety-first
    t.next_best_actions = list(t.next_best_actions or [])
    if not t.next_best_actions:
        t.next_best_actions = [
            {
                "id": "nba_safe_1",
                "type": "linkedin_manual_warm_intro",
                "title_ar": "أرسل 10 رسائل LinkedIn warm يدوياً (لا automation).",
            },
            {
                "id": "nba_safe_2",
                "type": "request_inbound_consent_first",
                "title_ar": "اطلب موافقة inbound قبل أي رسالة WhatsApp.",
            },
        ]

    source = BrainSource.DB if found_anything else BrainSource.PARTIAL
    return _to_dict(t, customer_id, source)
