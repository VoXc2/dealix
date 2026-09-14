"""Sector-scale market intelligence planning — research only, no bulk outreach authority.

Historical versions of this module mixed sector research with synthetic people counts,
fixed payment values, persuasion tactics and implied auto-ingest/outbound work. Omega V3
keeps the compatibility surface but makes every output fail closed: signals are research,
relationships/consent are unknown until evidenced, diagnostics are free, and no live
send/payment/tender action is created here.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.agentic_holding.runtime import build_current_registry
from dealix.commercial.best_offers_catalog import BestOfferCatalog
from dealix.commercial.economic_cell import Sector
from dealix.commercial.hermes_sector_diagnostic import HermesSectorDiagnostic
from dealix.commercial.sector_company_factory import SectorCompanyFactory

UNKNOWN = "UNKNOWN"
RESEARCH_ONLY = "RESEARCH_ONLY"


class LargeScaleExecution(BaseModel):
    """Compatibility model for a bounded sector research plan, not an outreach batch."""

    model_config = ConfigDict(extra="forbid")

    sector: Sector
    people_targeted: int = 0
    research_scope_requested: int = 0
    channels_used: list[str] = Field(default_factory=list)
    pain_targeted: str = UNKNOWN
    complete_reply: str = UNKNOWN
    payment_sar: float | None = None
    device_ready: bool = False
    persuasion_methods: list[str] = Field(default_factory=list)
    no_ban: bool = False
    authority_state: str = RESEARCH_ONLY
    relationship_count: int = 0
    consent_count: int = 0
    live_outbound_allowed: bool = False
    tender_submission_allowed: bool = False
    generated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class LargeScaleSectorExecutor:
    """Prepare sector intelligence hypotheses; never mint people, consent, spend or sends."""

    def __init__(self) -> None:
        self.scf = SectorCompanyFactory()
        self.hermes = HermesSectorDiagnostic()
        self.offers = BestOfferCatalog()

    def execute_sector(self, sector: Sector, people: int = 100) -> LargeScaleExecution:
        co = self.scf.build(sector)
        pain = co.top_problems[0] if co.top_problems else "revenue_leakage"
        diag = self.hermes.diagnose(
            sector,
            co.buyer_focus[0] if co.buyer_focus else "ceo",
            pain,
            "ar",
        )
        # These are discovery/research surfaces only. They are not active contact channels.
        research_channels = [
            "public_web_research",
            "official_procurement_research",
            "partner_research",
            "event_research",
            "referral_hypothesis",
            "email_only_after_verified_opt_in",
        ]
        reply = (
            f"فرضية بحثية لقطاع {co.sector_name_ar}: مشكلة {pain}; "
            f"families={diag['diagnostic_families']}; offer_hypothesis={diag['offer']['offer_id']}; "
            "التالي: تحقق من المصدر ثم Real Interaction ثم Free Diagnostic/Qualified Discovery."
        )
        return LargeScaleExecution(
            sector=sector,
            people_targeted=0,
            research_scope_requested=max(0, int(people)),
            channels_used=research_channels,
            pain_targeted=pain,
            complete_reply=reply,
            payment_sar=None,
            device_ready=False,
            persuasion_methods=[
                "evidence-backed relevance",
                "customer-specific problem framing",
                "verified proof only",
                "real deadline only when independently evidenced",
            ],
            no_ban=False,
            authority_state=RESEARCH_ONLY,
            relationship_count=0,
            consent_count=0,
            live_outbound_allowed=False,
            tender_submission_allowed=False,
        )

    def execute_all_sectors(self, people_per_sector: int = 100) -> list[LargeScaleExecution]:
        return [self.execute_sector(sector, people_per_sector) for sector in Sector]

    def team_authorization_queue(self) -> list[dict[str, Any]]:
        """Internal qualification work only; no external/material side effect is queued."""
        registry = build_current_registry()
        owner = "dealix.group.research-intelligence"
        procurement_owner = "dealix.group.procurement-b2g"
        if owner not in registry.agents:
            owner = "dealix-pm"
        if procurement_owner not in registry.agents:
            procurement_owner = "dealix-pm"
        return [
            {
                "task": "Rank sector research signals by evidence, economics and time-to-cash",
                "owner": owner,
                "status": "RESEARCH_ONLY",
                "external_effect": "NONE",
            },
            {
                "task": "Qualify public procurement opportunities and partner/eligibility evidence",
                "owner": procurement_owner,
                "status": "RESEARCH_ONLY",
                "external_effect": "NONE",
                "truth_firewall": "public_tender != eligibility != bid_authority",
            },
            {
                "task": "Prepare free diagnostic hypotheses for highest-ranked verified signals",
                "owner": "dealix.group.revenue" if "dealix.group.revenue" in registry.agents else "dealix-sales",
                "status": "DRAFT_ONLY",
                "external_effect": "NONE",
                "commercial_rule": "FREE_DIAGNOSTIC_THEN_CUSTOMER_SPECIFIC_SCOPE",
            },
        ]


__all__ = ["LargeScaleSectorExecutor", "LargeScaleExecution", "UNKNOWN", "RESEARCH_ONLY"]
