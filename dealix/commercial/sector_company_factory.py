"""Sector Company Factory — agents as companies per sector, intelligent, fully automated.

Each sector company is a TEMPORARY capability, not a permanent agent.
Uses sector overlays, buyer groups, problems, workflows to generate sector-specific
company execution with full communication channels.

Covers 20 sectors from economic_cell.Sector with sector-specific intelligence.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.channel_registry import Channel, ChannelRegistry, ChannelStatus, ChannelType
from dealix.commercial.consent_registry import ConsentRegistry
from dealix.commercial.economic_cell import Sector
from dealix.commercial.relationship_graph import RelationshipGraph
from dealix.commercial.universal_diagnostic_factory import (
    DiagnosticDepth,
    UniversalDiagnosticFactory,
)

UNKNOWN = "UNKNOWN"

class SectorCompany(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company_id: str
    sector: Sector
    sector_name_ar: str = UNKNOWN
    sector_name_en: str = UNKNOWN
    buyer_focus: list[str] = Field(default_factory=list)
    top_problems: list[str] = Field(default_factory=list)
    top_workflows: list[str] = Field(default_factory=list)
    automation_candidates: list[str] = Field(default_factory=list)
    procurement_pattern: str = UNKNOWN
    likely_objections: list[str] = Field(default_factory=list)
    compliance: list[str] = Field(default_factory=list)
    relevant_offers: list[str] = Field(default_factory=list)
    proof_requirements: list[str] = Field(default_factory=list)
    distribution_channels: list[str] = Field(default_factory=list)
    diagnostic_families: list[str] = Field(default_factory=list)
    channels_ready: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")

SECTOR_INTEL: dict[Sector, dict[str, Any]] = {
    Sector.GOVERNMENT_B2G: {"ar": "حكومي/B2G", "en": "Government/B2G", "buyers": ["procurement_director","project_director","ciso"], "problems": ["procurement_delay","compliance_burden","approval_delay"], "workflows": ["tender→bid","procure→pay"], "procurement": "Etimad", "compliance": ["PDPL","NCA"], "offers": ["B2G Readiness","Tender Intelligence"], "channels": ["procurement_portals","etimad_intelligence","partner_referrals"]},
    Sector.CONSTRUCTION_EPC: {"ar": "إنشاءات/EPC", "en": "Construction/EPC", "buyers": ["project_director","cfo","procurement_director"], "problems": ["project_delay","document_chaos","cost_leakage"], "workflows": ["project→cash","variation→payment"], "procurement": "Etimad+private", "compliance": ["document_control"], "offers": ["Project Controls","Document Intelligence"], "channels": ["events_conferences","partner_referrals","website_inbound"]},
    Sector.INDUSTRIAL_MANUFACTURING: {"ar": "صناعي", "en": "Industrial", "buyers": ["operations_director","coo","cfo"], "problems": ["quality_failure","inventory_exception","cost_leakage"], "workflows": ["order→cash","inventory→fulfillment"], "procurement": "supplier portals", "compliance": ["quality"], "offers": ["Operations Diagnostic","Quality"], "channels": ["supplier_portals","events_conferences"]},
    Sector.LOGISTICS_SUPPLY_CHAIN: {"ar": "لوجستي", "en": "Logistics", "buyers": ["operations_director","coo"], "problems": ["inventory_exception","project_delay","decision_latency"], "workflows": ["shipment→delivery","exception→resolution"], "procurement": "supplier portals", "compliance": [], "offers": ["Supply Chain Diagnostic","Automation"], "channels": ["supplier_portals","events_conferences"]},
    Sector.ENERGY_UTILITIES_OIL_GAS: {"ar": "طاقة/نفط", "en": "Energy/Oil&Gas", "buyers": ["cto","ciso","operations_director"], "problems": ["operational_exception_overload","cyber_risk"], "workflows": ["operations→maintenance"], "procurement": "Aramco supplier", "compliance": ["NCA","cyber"], "offers": ["Private AI","Cyber Readiness"], "channels": ["partner_referrals","events_conferences"]},
    Sector.REAL_ESTATE_PROPTECH: {"ar": "عقار/FM", "en": "Real Estate/FM", "buyers": ["operations_director","coo"], "problems": ["operational_exception_overload","document_chaos"], "workflows": ["facility→maintenance"], "procurement": "private", "compliance": [], "offers": ["FM Operations","Document"], "channels": ["events_conferences","website_inbound"]},
    Sector.HEALTHCARE: {"ar": "صحي", "en": "Healthcare", "buyers": ["cio","compliance_risk","operations_director"], "problems": ["compliance_burden","data_fragmentation","customer_support_backlog"], "workflows": ["patient→care","support→resolution"], "procurement": "Nupco", "compliance": ["PDPL","health"], "offers": ["Data Diagnostic","Support Automation"], "channels": ["partner_referrals","events_conferences"]},
    Sector.FINANCE_FINTECH_INSURANCE: {"ar": "مالي/تأمين", "en": "Finance", "buyers": ["cfo","ciso","compliance_risk"], "problems": ["compliance_burden","cyber_risk","revenue_leakage"], "workflows": ["procure→pay","lead→cash"], "procurement": "bank portals", "compliance": ["SAMA","PDPL","NCA"], "offers": ["Fatoora Ops","AI Governance"], "channels": ["partner_referrals","website_inbound"]},
    Sector.TECHNOLOGY_SAAS_SI: {"ar": "تقنية/SaaS", "en": "Technology/SaaS", "buyers": ["cto","ceo","ciso"], "problems": ["ai_governance_risk","integration_failure","revenue_leakage"], "workflows": ["lead→cash","support→resolution"], "procurement": "direct", "compliance": ["PDPL","NCA"], "offers": ["AI Governance","Revenue Command"], "channels": ["website_inbound","seo","founder_content"]},
    Sector.PROFESSIONAL_SERVICES: {"ar": "خدمات مهنية", "en": "Professional Services", "buyers": ["ceo","sales_director","finance_director"], "problems": ["revenue_leakage","quote_delay","collection_delay"], "workflows": ["lead→proposal→cash"], "procurement": "direct", "compliance": [], "offers": ["Revenue Leakage","Proposal Automation"], "channels": ["founder_content","referral","website_inbound"]},
}

# Sector-specific PATTERN intelligence for the remaining canonical sectors.
# These are internal hypotheses for diagnostics/qualification; never customer facts.
_REMAINING_SECTOR_INTEL: dict[Sector, dict[str, Any]] = {
    Sector.MINING_METALS: {"ar": "تعدين ومعادن", "en": "Mining & Metals", "buyers": ["operations_director","procurement_director","cfo"], "problems": ["maintenance_downtime","grade_data_fragmentation","procurement_delay"], "workflows": ["mine->process","maintenance->return_to_service"], "procurement": "supplier portals+private", "compliance": ["MIM","NCA","PDPL"], "offers": ["Mining Operations Diagnostic","Maintenance Intelligence"], "channels": ["supplier_portals","events_conferences","partner_referrals"]},
    Sector.RETAIL_COMMERCE_ECOMMERCE: {"ar": "تجارة تجزئة وإلكترونية", "en": "Retail & E-commerce", "buyers": ["ecommerce_director","coo","finance_director"], "problems": ["conversion_leakage","fulfillment_exception","customer_support_backlog"], "workflows": ["order->fulfillment","return->refund"], "procurement": "direct", "compliance": ["MC","ZATCA","PDPL"], "offers": ["Commerce Operations Diagnostic","Support Automation"], "channels": ["website_inbound","seo","founder_content"]},
    Sector.TOURISM_HOSPITALITY: {"ar": "سياحة وضيافة", "en": "Tourism & Hospitality", "buyers": ["general_manager","revenue_manager","operations_director"], "problems": ["booking_leakage","guest_support_backlog","operational_exception_overload"], "workflows": ["booking->stay","guest_issue->resolution"], "procurement": "private", "compliance": ["Ministry_of_Tourism","PDPL","ZATCA"], "offers": ["Guest Operations Diagnostic","Revenue Command"], "channels": ["events_conferences","partner_referrals","website_inbound"]},
    Sector.TELECOM_MEDIA_MARKETING: {"ar": "اتصالات وإعلام وتسويق", "en": "Telecom, Media & Marketing", "buyers": ["cmo","cio","operations_director"], "problems": ["campaign_attribution_gap","content_operations_bottleneck","customer_support_backlog"], "workflows": ["campaign->lead","content->publish","support->resolution"], "procurement": "direct+enterprise", "compliance": ["CST","GAMR","PDPL"], "offers": ["Growth Operations Diagnostic","AI Governance"], "channels": ["website_inbound","seo","events_conferences"]},
    Sector.EDUCATION_TRAINING: {"ar": "تعليم وتدريب", "en": "Education & Training", "buyers": ["training_director","operations_director","cio"], "problems": ["enrollment_leakage","scheduling_fragmentation","learner_support_backlog"], "workflows": ["lead->enrollment","enrollment->completion","support->resolution"], "procurement": "direct+government", "compliance": ["ETEC","Ministry_of_Education","PDPL"], "offers": ["Enrollment Operations Diagnostic","Learning Support Automation"], "channels": ["website_inbound","partner_referrals","procurement_portals"]},
    Sector.AGRICULTURE_FOOD_WATER: {"ar": "زراعة وأغذية ومياه", "en": "Agriculture, Food & Water", "buyers": ["operations_director","quality_director","procurement_director"], "problems": ["traceability_gap","inventory_exception","quality_failure"], "workflows": ["source->quality->delivery","exception->resolution"], "procurement": "supplier portals+private", "compliance": ["MEWA","SFDA","SWA"], "offers": ["Traceability Diagnostic","Operations Automation"], "channels": ["supplier_portals","events_conferences","partner_referrals"]},
    Sector.MOBILITY_AUTOMOTIVE: {"ar": "تنقل وسيارات", "en": "Mobility & Automotive", "buyers": ["fleet_director","after_sales_director","operations_director"], "problems": ["maintenance_downtime","parts_inventory_exception","service_backlog"], "workflows": ["vehicle->service","parts->fulfillment","issue->resolution"], "procurement": "supplier portals+private", "compliance": ["TGA","SASO","ZATCA"], "offers": ["Fleet Operations Diagnostic","Service Automation"], "channels": ["supplier_portals","events_conferences","website_inbound"]},
    Sector.EXPORT_IMPORT_RHQ: {"ar": "تصدير واستيراد ومقرات إقليمية", "en": "Export, Import & RHQ", "buyers": ["supply_chain_director","cfo","compliance_risk"], "problems": ["customs_document_delay","landed_cost_leakage","compliance_burden"], "workflows": ["order->customs->delivery","quote->cash"], "procurement": "direct+partner", "compliance": ["MISA","ZATCA","PDPL"], "offers": ["Trade Operations Diagnostic","Document Intelligence"], "channels": ["partner_referrals","website_inbound","events_conferences"]},
    Sector.CREATIVE_SPORTS_GAMING: {"ar": "إبداع ورياضة وألعاب", "en": "Creative, Sports & Gaming", "buyers": ["commercial_director","operations_director","marketing_director"], "problems": ["sponsorship_pipeline_leakage","fan_support_backlog","content_operations_bottleneck"], "workflows": ["campaign->revenue","event->engagement","content->publish"], "procurement": "direct+events", "compliance": ["GEA","Ministry_of_Sport","GAMR","PDPL"], "offers": ["Commercial Revenue Diagnostic","Content Operations Automation"], "channels": ["founder_content","events_conferences","website_inbound"]},
    Sector.ASSOCIATIONS_NONPROFITS: {"ar": "جمعيات وغير ربحية", "en": "Associations & Nonprofits", "buyers": ["executive_director","fundraising_director","operations_director"], "problems": ["donor_member_lifecycle_gap","reporting_burden","service_coordination_delay"], "workflows": ["donor->receipt->report","member->service","case->resolution"], "procurement": "direct+grants", "compliance": ["NCNPO","PDPL"], "offers": ["Mission Operations Diagnostic","Member and Donor Automation"], "channels": ["partner_referrals","website_inbound","events_conferences"]},
}
SECTOR_INTEL.update(_REMAINING_SECTOR_INTEL)

class SectorCompanyFactory:
    def __init__(self) -> None:
        self.factory = UniversalDiagnosticFactory()
        self.channel_registry = ChannelRegistry()
        # Seed channels for each sector
        for sector, intel in SECTOR_INTEL.items():
            for ch in intel["channels"]:
                try:
                    self.channel_registry.register(Channel(channel_id=f"{sector.value}_{ch}", channel_type=ChannelType.SEARCH if "seo" in ch else ChannelType.RELATIONSHIP, target_buyer=intel["buyers"][0] if intel["buyers"] else "ceo", sector_fit=[sector.value], current_status=ChannelStatus.READY if ch in ("website_inbound","seo") else ChannelStatus.DISCOVERED))
                except Exception:
                    pass

    def build(self, sector: Sector, company_size: str = "sme", buyer_role: str | None = None) -> SectorCompany:
        intel = SECTOR_INTEL[sector]
        buyer = buyer_role or (intel["buyers"][0] if intel["buyers"] else "ceo")
        # Diagnostic families for this sector/company
        families = self.factory.compose(sector.value, company_size, buyer, intel["problems"][0] if intel["problems"] else "revenue_leakage", DiagnosticDepth.D1_RAPID)
        # Automation candidates via frequency*manual
        automation = [f"automate {w} for {sector.value}" for w in intel["workflows"][:2]]
        # Channels ready
        channels_ready = [c.channel_id for c in self.channel_registry.channels.values() if c.sector_fit and sector.value in c.sector_fit and c.current_status == ChannelStatus.READY]
        return SectorCompany(
            company_id=f"sector_co_{sector.value}",
            sector=sector,
            sector_name_ar=intel["ar"],
            sector_name_en=intel["en"],
            buyer_focus=intel["buyers"],
            top_problems=intel["problems"],
            top_workflows=intel["workflows"],
            automation_candidates=automation,
            procurement_pattern=intel["procurement"],
            likely_objections=["no_budget","no_trust","procurement_blocked"],
            compliance=intel["compliance"],
            relevant_offers=intel["offers"],
            proof_requirements=["baseline","governance","acceptance"],
            distribution_channels=intel["channels"],
            diagnostic_families=[f.family_id for f in families[:5]],
            channels_ready=channels_ready,
        )

    def build_all(self) -> list[SectorCompany]:
        return [self.build(s) for s in Sector]

    def to_dict(self) -> dict[str, Any]:
        all_cos = self.build_all()
        return {"total": len(all_cos), "sectors": [c.sector.value for c in all_cos], "companies": [c.to_dict() for c in all_cos]}

__all__ = ["SectorCompanyFactory", "SectorCompany", "SECTOR_INTEL", "UNKNOWN"]
