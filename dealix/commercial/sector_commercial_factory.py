"""Canonical Saudi sector commercial packs for Dealix.

One commercial overlay over the existing ``economic_cell.Sector`` registry.
This module does not create another taxonomy, CRM, Company Brain, opportunity
store, or permanent agent fleet. Public-source market signals are research
only: they never count as relationship, consent, pipeline, payment or revenue.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.economic_cell import Sector

FREE = "FREE"
UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"

CANONICAL_OFFERS = frozenset(
    {
        "Saudi Opportunity Snapshot",
        "Revenue Proof Sprint",
        "Revenue Command Pilot",
        "Saudi Market Access Sprint",
        "AI Company OS Setup",
        "B2G Readiness Sprint",
        "Partner / Distributor Desk",
        "Revenue Command Room",
    }
)


class SectorMaturity(StrEnum):
    DRAFT = "DRAFT"
    RESEARCHED = "RESEARCHED"
    INTERNAL_READY = "INTERNAL_READY"
    VALIDATED = "VALIDATED"
    PUBLIC_READY = "PUBLIC_READY"
    COMMERCIAL_SIGNAL = "COMMERCIAL_SIGNAL"
    DELIVERY_PROVEN = "DELIVERY_PROVEN"


class SourceRef(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    source_id: str
    source_url: str
    source_authority: str
    source_date: str = UNKNOWN
    observed_at: str
    fresh_until: str
    refresh_policy: str


class MarketSignalRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    signal_id: str
    source_url: str
    source_authority: str
    source_date: str = UNKNOWN
    observed_at: str
    fresh_until: str
    sector: str
    subsector: str = ""
    buyer_type: str = UNKNOWN
    problem: str
    trigger: str
    deadline: str = UNKNOWN
    urgency: str = "WATCH"
    dealix_match: list[str] = Field(default_factory=list)
    diagnostic_match: list[str] = Field(default_factory=list)
    offer_match: list[str] = Field(default_factory=list)
    evidence_grade: str = "OFFICIAL_PUBLIC_SOURCE"
    truth_class: str = "OBSERVED"
    counts_as_relationship: bool = False
    counts_as_consent: bool = False
    counts_as_pipeline: bool = False
    counts_as_revenue: bool = False


class SectorCommercialPack(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    sector_id: str
    arabic_name: str
    english_name: str
    market_context: list[str]
    saudi_context: list[str]
    official_sources: list[SourceRef]
    regulators: list[str]
    current_signals: list[MarketSignalRecord]
    freshness: str
    icp_segments: list[str]
    company_size: list[str]
    business_models: list[str]
    geography: list[str]
    digital_maturity: list[str]
    buyer_roles: list[str]
    economic_buyer: str
    champion: str
    technical_buyer: str
    user_roles: list[str]
    blockers: list[str]
    top_pain_patterns: list[str]
    trigger_events: list[str]
    regulatory_triggers: list[str]
    procurement_triggers: list[str]
    growth_triggers: list[str]
    cost_triggers: list[str]
    risk_triggers: list[str]
    systems_typically_used: list[str]
    data_sources: list[str]
    integration_surfaces: list[str]
    diagnostic_modules: list[str]
    diagnostic_price: str
    ai_opportunities: list[str]
    automation_opportunities: list[str]
    workflow_opportunities: list[str]
    data_opportunities: list[str]
    security_concerns: list[str]
    privacy_concerns: list[str]
    compliance_concerns: list[str]
    procurement_paths: list[str]
    b2b_paths: list[str]
    b2g_paths: list[str]
    partner_paths: list[str]
    offer_matches: list[str]
    proposal_modules: list[str]
    delivery_modules: list[str]
    acceptance_patterns: list[str]
    proof_requirements: list[str]
    seo_themes: list[str]
    content_themes: list[str]
    arabic_queries: list[str]
    english_queries: list[str]
    maturity: SectorMaturity
    evidence_grade: str
    risk: list[str]
    last_refresh: str
    promote_criteria: list[str]
    kill_criteria: list[str]


class _Profile(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    ar: str
    en: str
    regulators: list[str]
    sources: list[str]
    icp: list[str]
    models: list[str]
    buyers: tuple[str, str, str]
    pains: list[str]
    triggers: list[str]
    systems: list[str]
    data: list[str]
    integrations: list[str]
    ai: list[str]
    automation: list[str]
    compliance: list[str]
    procurement: list[str]
    offers: list[str]
    proposal: list[str]
    delivery: list[str]
    acceptance: list[str]
    seo: list[str]


def _p(
    ar: str,
    en: str,
    regulators: list[str],
    sources: list[str],
    icp: list[str],
    models: list[str],
    buyers: tuple[str, str, str],
    pains: list[str],
    triggers: list[str],
    systems: list[str],
    data: list[str],
    integrations: list[str],
    ai: list[str],
    automation: list[str],
    compliance: list[str],
    procurement: list[str],
    offers: list[str],
    proposal: list[str],
    delivery: list[str],
    acceptance: list[str],
    seo: list[str],
) -> _Profile:
    return _Profile(
        ar=ar,
        en=en,
        regulators=regulators,
        sources=sources,
        icp=icp,
        models=models,
        buyers=buyers,
        pains=pains,
        triggers=triggers,
        systems=systems,
        data=data,
        integrations=integrations,
        ai=ai,
        automation=automation,
        compliance=compliance,
        procurement=procurement,
        offers=offers,
        proposal=proposal,
        delivery=delivery,
        acceptance=acceptance,
        seo=seo,
    )


SECTOR_PROFILES: dict[Sector, _Profile] = {
    Sector.GOVERNMENT_B2G: _p(
        "الحكومة والمشتريات الحكومية", "Government & B2G",
        ["Etimad", "SDAIA", "NCA"], ["etimad", "jadeer", "sdaia"],
        ["government entities", "government suppliers", "SMEs pursuing public procurement"],
        ["B2G", "supplier", "prime/subcontractor"],
        ("procurement_director", "project_director", "cio"),
        ["procurement_delay", "document_readiness", "approval_delay"],
        ["tender_discovered", "supplier_qualification_due", "document_expiry"],
        ["Etimad", "ERP", "document management"],
        ["tender documents", "supplier documents", "delivery evidence"],
        ["document repositories", "CRM", "ERP"],
        ["requirement extraction", "bid evidence mapping"],
        ["tender radar", "document expiry checks"],
        ["PDPL", "NCA", "procurement rules"],
        ["Etimad", "vendor onboarding", "prime contractor", "subcontractor"],
        ["B2G Readiness Sprint", "Saudi Opportunity Snapshot"],
        ["eligibility", "scope fit", "bid/no-bid", "evidence gaps"],
        ["supplier readiness", "tender evidence pack"],
        ["eligibility verified", "documents traceable", "submission remains L5"],
        ["جاهزية اعتماد", "تأهيل الموردين", "B2G Saudi"],
    ),
    Sector.CONSTRUCTION_EPC: _p(
        "الإنشاءات والمقاولات وEPC", "Construction & EPC",
        ["Etimad"], ["etimad", "gastat"],
        ["EPC contractors", "general contractors", "project owners"],
        ["project based", "contracting"],
        ("project_director", "cfo", "procurement_director"),
        ["project_delay", "document_chaos", "cost_leakage", "collection_delay"],
        ["new_project", "variation_backlog", "payment_delay"],
        ["ERP", "project controls", "document control"],
        ["RFIs", "variations", "progress certificates", "invoices"],
        ["ERP", "DMS", "project controls"],
        ["document intelligence", "variation classification"],
        ["approval routing", "progress evidence packs"],
        ["PDPL", "contractual evidence"],
        ["Etimad", "private RFP", "subcontracting"],
        ["Revenue Proof Sprint", "AI Company OS Setup"],
        ["project baseline", "variation workflow", "payment evidence"],
        ["project-controls workflow", "document automation"],
        ["cycle time measured", "acceptance evidence captured"],
        ["أتمتة المقاولات", "ذكاء المستندات EPC", "تحصيل المشاريع"],
    ),
    Sector.INDUSTRIAL_MANUFACTURING: _p(
        "الصناعة والتصنيع", "Industrial Manufacturing",
        ["MIM", "MODON"], ["mim", "modon", "gastat"],
        ["factories", "industrial SMEs", "manufacturing groups"],
        ["make-to-stock", "make-to-order", "B2B manufacturing"],
        ("operations_director", "coo", "cfo"),
        ["quality_failure", "inventory_exception", "cost_leakage"],
        ["quality_event", "downtime", "inventory_exception"],
        ["ERP", "MES", "QMS", "CMMS"],
        ["production orders", "quality events", "inventory", "maintenance"],
        ["ERP", "MES", "CMMS", "BI"],
        ["quality anomaly support", "maintenance knowledge retrieval"],
        ["exception routing", "CAPA workflow"],
        ["PDPL", "quality controls"],
        ["supplier portals", "private RFP"],
        ["AI Company OS Setup", "Revenue Proof Sprint"],
        ["operations baseline", "exception map", "quality evidence"],
        ["operations diagnostic", "exception automation"],
        ["exception handling verified", "baseline vs result measurable"],
        ["أتمتة المصانع", "ذكاء صناعي السعودية", "تحسين العمليات الصناعية"],
    ),
    Sector.LOGISTICS_SUPPLY_CHAIN: _p(
        "اللوجستيات وسلاسل الإمداد", "Logistics & Supply Chain",
        ["TGA", "Mawani"], ["tga", "mawani", "gastat"],
        ["3PLs", "freight forwarders", "warehouse operators", "port ecosystem"],
        ["3PL", "freight", "warehousing"],
        ("operations_director", "coo", "cio"),
        ["shipment_exception", "inventory_exception", "decision_latency"],
        ["SLA_breach", "shipment_exception", "warehouse_backlog"],
        ["TMS", "WMS", "ERP", "fleet systems"],
        ["shipments", "events", "inventory", "SLAs"],
        ["TMS", "WMS", "ERP", "customer portals"],
        ["exception triage", "operations copilot"],
        ["exception routing", "status synchronization"],
        ["PDPL", "transport requirements"],
        ["supplier portal", "private RFP"],
        ["AI Company OS Setup", "Revenue Proof Sprint"],
        ["control tower", "exception ownership", "SLA evidence"],
        ["exception workflow", "operations automation"],
        ["SLA event trace verified", "handoff latency measurable"],
        ["أتمتة اللوجستيات", "سلاسل الإمداد AI", "الموانئ الذكية"],
    ),
    Sector.ENERGY_UTILITIES_OIL_GAS: _p(
        "الطاقة والمرافق والنفط والغاز", "Energy, Utilities & Oil/Gas",
        ["NCA", "MIM"], ["mim", "gastat"],
        ["operators", "service companies", "utilities"],
        ["asset intensive", "field services"],
        ("operations_director", "ciso", "cto"),
        ["maintenance_backlog", "operational_exception_overload", "cyber_risk"],
        ["maintenance_delay", "field_exception", "control_gap"],
        ["ERP", "EAM", "DMS"],
        ["work orders", "maintenance", "asset records", "incidents"],
        ["EAM", "ERP", "DMS"],
        ["maintenance knowledge retrieval", "document intelligence"],
        ["work-order triage", "evidence routing"],
        ["NCA", "PDPL", "safety governance"],
        ["vendor onboarding", "RFP", "framework agreement"],
        ["AI Company OS Setup", "Revenue Proof Sprint"],
        ["security boundary", "asset/work-order baseline", "governance"],
        ["private AI workflow", "governed operations automation"],
        ["security boundary verified", "operator acceptance recorded"],
        ["AI النفط والغاز السعودية", "أتمتة الصيانة", "حوكمة AI الطاقة"],
    ),
    Sector.MINING_METALS: _p(
        "التعدين والمعادن", "Mining & Metals",
        ["MIM"], ["mim", "gastat"],
        ["miners", "mineral processors", "mining services"],
        ["asset intensive", "project based"],
        ("operations_director", "coo", "cfo"),
        ["field_data_latency", "maintenance_delay", "supplier_delay"],
        ["production_variance", "maintenance_delay", "supplier_delay"],
        ["ERP", "EAM", "fleet", "DMS"],
        ["production", "maintenance", "fleet", "supplier"],
        ["ERP", "EAM", "BI"],
        ["operations knowledge retrieval", "document extraction"],
        ["exception routing", "maintenance coordination"],
        ["PDPL", "safety controls"],
        ["supplier portal", "RFP"],
        ["AI Company OS Setup", "Revenue Proof Sprint"],
        ["operating baseline", "field-to-management flow"],
        ["operations diagnostic", "workflow automation"],
        ["field-to-management trace verified", "result evidence captured"],
        ["AI التعدين السعودية", "أتمتة التعدين", "تحسين عمليات المعادن"],
    ),
    Sector.REAL_ESTATE_PROPTECH: _p(
        "العقار والتقنية العقارية وإدارة المرافق", "Real Estate, PropTech & FM",
        ["REGA"], ["rega", "gastat"],
        ["developers", "property managers", "FM operators", "PropTechs"],
        ["development", "property management", "FM", "PropTech"],
        ("operations_director", "coo", "cio"),
        ["maintenance_backlog", "document_chaos", "tenant_service_backlog"],
        ["sandbox_pathway", "maintenance_backlog", "new_asset_portfolio"],
        ["property management", "FM/CMMS", "CRM", "ERP"],
        ["assets", "work orders", "tenant requests", "contracts"],
        ["PMS", "CMMS", "CRM", "ERP"],
        ["service triage", "document intelligence"],
        ["work-order routing", "contract workflow"],
        ["REGA requirements", "PDPL"],
        ["private RFP", "vendor onboarding"],
        ["AI Company OS Setup", "Revenue Proof Sprint"],
        ["FM baseline", "service workflow", "PropTech readiness"],
        ["FM workflow automation", "readiness implementation"],
        ["service cycle verified", "data boundary verified"],
        ["PropTech السعودية", "أتمتة إدارة المرافق", "ذكاء عقاري"],
    ),
    Sector.HEALTHCARE: _p(
        "الرعاية الصحية والصحة الرقمية", "Healthcare & Digital Health",
        ["Ministry of Health", "SDAIA", "NCA"], ["moh", "sdaia", "gastat"],
        ["providers", "healthtechs", "clinics", "non-clinical support operations"],
        ["provider", "healthtech", "B2B healthcare"],
        ("cio", "operations_director", "compliance_risk"),
        ["data_fragmentation", "documentation_burden", "support_backlog"],
        ["sandbox_pathway", "service_backlog", "administrative_burden"],
        ["HIS/EHR", "CRM", "ticketing", "DMS"],
        ["service operations", "administrative records", "support", "documents"],
        ["HIS/EHR boundary", "CRM", "DMS"],
        ["administrative summarization", "knowledge retrieval"],
        ["non-clinical routing", "evidence collection"],
        ["PDPL", "health regulation", "cybersecurity"],
        ["sector procurement", "private RFP"],
        ["AI Company OS Setup", "Revenue Proof Sprint"],
        ["data boundary", "non-clinical workflow", "sandbox readiness"],
        ["governed non-clinical automation", "readiness implementation"],
        ["data boundary verified", "human oversight verified"],
        ["الذكاء الاصطناعي الصحي السعودية", "أتمتة الرعاية الصحية", "Health AI Saudi"],
    ),
    Sector.FINANCE_FINTECH_INSURANCE: _p(
        "الخدمات المالية والتقنية المالية والتأمين", "Finance, FinTech & Insurance",
        ["SAMA", "SDAIA", "NCA", "ZATCA"], ["sama", "zatca", "sdaia", "gastat"],
        ["fintechs", "financial institutions", "insurers", "finance operations"],
        ["regulated finance", "fintech", "insurance"],
        ("cfo", "compliance_risk", "cio"),
        ["compliance_burden", "integration_failure", "control_gap"],
        ["open_banking_change", "Fatoora_notification", "control_gap"],
        ["core finance", "ERP", "CRM", "risk systems"],
        ["financial operations", "customer consent", "invoices", "controls"],
        ["Open Banking interfaces", "ERP", "Fatoora", "CRM"],
        ["regulated operations copilot", "control evidence support"],
        ["consent-aware workflows", "invoice exception handling"],
        ["SAMA", "PDPL", "NCA", "ZATCA"],
        ["regulated vendor onboarding", "RFP"],
        ["AI Company OS Setup", "Revenue Proof Sprint"],
        ["regulatory baseline", "integration/control evidence", "Fatoora readiness"],
        ["regulated workflow", "Fatoora operations", "AI governance"],
        ["control evidence verified", "consent state verified"],
        ["Open Banking Saudi", "فاتورة جاهزية", "حوكمة AI المالية"],
    ),
    Sector.RETAIL_COMMERCE_ECOMMERCE: _p(
        "التجزئة والتجارة والتجارة الإلكترونية", "Retail, Commerce & E-commerce",
        ["ZATCA", "SDAIA"], ["zatca", "gastat"],
        ["retailers", "e-commerce operators", "multi-branch merchants"],
        ["retail", "ecommerce", "marketplace"],
        ("commercial_director", "coo", "cfo"),
        ["conversion_leakage", "inventory_exception", "support_backlog"],
        ["Fatoora_notification", "conversion_drop", "inventory_exception"],
        ["POS", "commerce platform", "ERP", "CRM"],
        ["orders", "inventory", "customers", "invoices"],
        ["POS", "ERP", "CRM", "Fatoora"],
        ["support triage", "commercial analysis"],
        ["order exception routing", "invoice checks"],
        ["PDPL", "ZATCA"],
        ["direct purchase", "vendor onboarding"],
        ["Revenue Command Pilot", "AI Company OS Setup"],
        ["order-to-cash baseline", "Fatoora readiness", "conversion workflow"],
        ["revenue workflow", "Fatoora implementation"],
        ["order-to-cash trace verified", "conversion metric basis recorded"],
        ["أتمتة التجزئة السعودية", "AI ecommerce Saudi", "جاهزية فاتورة التجزئة"],
    ),
    Sector.TOURISM_HOSPITALITY: _p(
        "السياحة والضيافة", "Tourism & Hospitality",
        ["Ministry of Tourism"], ["tourism", "gastat"],
        ["hotels", "tour operators", "hospitality groups"],
        ["hospitality", "tourism services"],
        ("coo", "commercial_director", "customer_service"),
        ["service_backlog", "manual_handoffs", "conversion_leakage"],
        ["season_peak", "new_property_launch", "service_backlog"],
        ["PMS", "CRM", "booking", "ERP"],
        ["bookings", "guest requests", "service cases", "revenue"],
        ["PMS", "CRM", "booking engines"],
        ["guest service assistant", "knowledge retrieval"],
        ["request routing", "follow-up workflow"],
        ["PDPL", "tourism requirements"],
        ["private RFP", "vendor onboarding"],
        ["Revenue Command Pilot", "AI Company OS Setup"],
        ["guest journey", "service baseline", "commercial workflow"],
        ["guest operations automation", "commercial workflow"],
        ["guest request cycle verified", "customer acceptance captured"],
        ["AI السياحة السعودية", "أتمتة الفنادق", "تحسين تجربة الضيف"],
    ),
    Sector.PROFESSIONAL_SERVICES: _p(
        "الخدمات المهنية والاستشارية", "Professional Services",
        ["ZATCA", "SDAIA"], ["zatca", "jadeer", "gastat"],
        ["consultancies", "agencies", "staffing firms", "professional SMEs"],
        ["project services", "retainer", "staffing"],
        ("ceo", "sales_director", "finance_director"),
        ["revenue_leakage", "quote_delay", "collection_delay"],
        ["stale_pipeline", "quote_delay", "collection_delay"],
        ["CRM", "accounting", "project management"],
        ["leads", "proposals", "projects", "invoices"],
        ["CRM", "email", "accounting", "project tools"],
        ["proposal support", "account research"],
        ["follow-up orchestration", "proposal assembly"],
        ["PDPL", "ZATCA where applicable"],
        ["direct purchase", "RFP", "Jadeer supplier route"],
        ["Revenue Command Pilot", "Revenue Command Room"],
        ["qualified problem", "revenue workflow", "proposal scope"],
        ["revenue workflow automation", "proposal factory"],
        ["lead-to-cash trace verified", "customer acceptance captured"],
        ["أتمتة المبيعات B2B السعودية", "Revenue Operations Saudi", "تشخيص تسرّب الإيراد"],
    ),
    Sector.TECHNOLOGY_SAAS_SI: _p(
        "التقنية وSaaS وتكامل الأنظمة", "Technology, SaaS & SI",
        ["CST", "SDAIA", "NCA"], ["cst", "sdaia", "gastat"],
        ["SaaS firms", "system integrators", "IT services"],
        ["SaaS", "projects", "managed service"],
        ("ceo", "cto", "sales_director"),
        ["integration_failure", "support_backlog", "revenue_leakage"],
        ["growth_plateau", "AI_adoption", "support_backlog"],
        ["CRM", "ticketing", "product analytics", "cloud"],
        ["pipeline", "usage", "support", "delivery"],
        ["CRM", "APIs", "support", "analytics"],
        ["agentic workflow", "support copilot"],
        ["sales follow-up", "support routing"],
        ["PDPL", "NCA", "CST context"],
        ["direct", "RFP", "partner ecosystem"],
        ["Revenue Command Room", "AI Company OS Setup"],
        ["revenue baseline", "agent authority", "integration scope"],
        ["governed agents", "revenue operations"],
        ["tool permission audit verified", "economic truth gates verified"],
        ["AI agents Saudi", "SaaS automation Saudi", "حوكمة الذكاء الاصطناعي"],
    ),
    Sector.TELECOM_MEDIA_MARKETING: _p(
        "الاتصالات والإعلام والتسويق", "Telecom, Media & Marketing",
        ["CST", "SDAIA"], ["cst", "sdaia", "gastat"],
        ["telecom ecosystem", "media firms", "marketing agencies"],
        ["subscription", "media", "agency"],
        ("commercial_director", "marketing_director", "cio"),
        ["consent_complexity", "content_volume", "support_backlog"],
        ["AI_adoption", "campaign_scale", "service_backlog"],
        ["CRM", "campaign tools", "support", "analytics"],
        ["consent", "campaigns", "customers", "content"],
        ["CRM", "campaign tools", "support"],
        ["content operations", "customer-service assist"],
        ["consent-aware routing", "content workflow"],
        ["PDPL", "CST"],
        ["direct", "RFP", "agency partner"],
        ["Revenue Command Pilot", "AI Company OS Setup"],
        ["consent state", "campaign/service workflow", "measurement basis"],
        ["governed content ops", "customer workflow"],
        ["consent state verified", "opt-out path verified"],
        ["AI marketing Saudi", "أتمتة الإعلام", "اتصالات AI السعودية"],
    ),
    Sector.EDUCATION_TRAINING: _p(
        "التعليم والتدريب", "Education & Training",
        ["Ministry of Education", "HRDF", "SDAIA"], ["hrdf", "sdaia", "gastat"],
        ["training providers", "education operators", "EdTechs"],
        ["education", "training", "B2B learning"],
        ("ceo", "operations_director", "cio"),
        ["reporting_delay", "support_backlog", "manual_handoffs"],
        ["cohort_scale", "reporting_deadline", "support_backlog"],
        ["LMS", "CRM", "ERP", "content systems"],
        ["learners", "courses", "support", "outcomes"],
        ["LMS", "CRM", "ERP"],
        ["knowledge assistant", "content operations"],
        ["enrollment routing", "reporting workflow"],
        ["PDPL", "education requirements"],
        ["direct", "government procurement", "HRDF ecosystem"],
        ["AI Company OS Setup", "Revenue Proof Sprint"],
        ["learning-ops baseline", "data boundary", "reporting flow"],
        ["learning ops automation", "data/reporting"],
        ["learner data boundary verified", "outcome basis documented"],
        ["AI التعليم السعودية", "أتمتة التدريب", "EdTech Saudi"],
    ),
    Sector.AGRICULTURE_FOOD_WATER: _p(
        "الزراعة والأغذية والمياه", "Agriculture, Food & Water",
        ["MEWA"], ["gastat"],
        ["food producers", "agri businesses", "water operations"],
        ["production", "distribution", "asset intensive"],
        ("operations_director", "coo", "cfo"),
        ["field_visibility", "inventory_exception", "quality_failure"],
        ["yield_variance", "inventory_exception", "maintenance_delay"],
        ["ERP", "inventory", "field systems", "CMMS"],
        ["production", "inventory", "quality", "assets"],
        ["ERP", "inventory", "CMMS"],
        ["operations knowledge", "quality support"],
        ["exception routing", "quality evidence"],
        ["PDPL", "food/water requirements"],
        ["supplier portal", "RFP"],
        ["AI Company OS Setup", "Revenue Proof Sprint"],
        ["operations baseline", "supply/quality flow"],
        ["operations workflow", "supply-chain automation"],
        ["production event trace verified", "quality evidence captured"],
        ["AI الزراعة السعودية", "أتمتة الأغذية", "إدارة المياه AI"],
    ),
    Sector.MOBILITY_AUTOMOTIVE: _p(
        "التنقل والسيارات", "Mobility & Automotive",
        ["TGA", "SDAIA"], ["tga", "gastat"],
        ["fleet operators", "mobility companies", "automotive services"],
        ["fleet", "mobility", "after-sales"],
        ("operations_director", "coo", "customer_service"),
        ["fleet_exception", "service_backlog", "SLA_breach"],
        ["fleet_exception", "service_backlog", "dispatch_delay"],
        ["fleet", "CRM", "ERP", "service management"],
        ["vehicles", "trips", "service cases", "parts"],
        ["fleet systems", "CRM", "ERP"],
        ["service triage", "operations assistant"],
        ["dispatch routing", "service follow-up"],
        ["PDPL", "transport requirements"],
        ["vendor onboarding", "RFP"],
        ["AI Company OS Setup", "Revenue Proof Sprint"],
        ["fleet/service baseline", "dispatch workflow"],
        ["fleet/service workflow", "customer operations"],
        ["dispatch cycle verified", "SLA evidence captured"],
        ["AI النقل السعودية", "أتمتة الأساطيل", "خدمة السيارات AI"],
    ),
    Sector.EXPORT_IMPORT_RHQ: _p(
        "التصدير والاستيراد والمقرات الإقليمية", "Export, Import & RHQ",
        ["MISA", "ZATCA"], ["zatca", "gastat"],
        ["importers", "exporters", "regional headquarters", "market entrants"],
        ["trade", "distribution", "RHQ"],
        ("ceo", "commercial_director", "finance_director"),
        ["market_entry_friction", "document_chaos", "partner_search"],
        ["Saudi_market_entry", "new_distribution", "Fatoora_notification"],
        ["ERP", "CRM", "trade/logistics", "accounting"],
        ["customers", "shipments", "documents", "invoices"],
        ["ERP", "CRM", "logistics", "Fatoora"],
        ["market research synthesis", "document intelligence"],
        ["market-entry workflow", "document routing"],
        ["PDPL", "ZATCA", "trade requirements"],
        ["direct", "distributor", "partner"],
        ["Saudi Market Access Sprint", "Partner / Distributor Desk", "Saudi Opportunity Snapshot"],
        ["market-entry hypothesis", "partner criteria", "route-to-market"],
        ["market access desk", "commercial workflow"],
        ["route-to-market verified", "partner evidence separated from hypothesis"],
        ["Saudi market entry", "مقر إقليمي السعودية", "تصدير للسعودية"],
    ),
    Sector.CREATIVE_SPORTS_GAMING: _p(
        "الصناعات الإبداعية والرياضة والألعاب", "Creative, Sports & Gaming",
        ["Ministry of Sport", "SDAIA"], ["sdaia", "gastat"],
        ["sports operators", "gaming firms", "creative studios"],
        ["content", "events", "gaming", "sponsorship"],
        ("ceo", "commercial_director", "marketing_director"),
        ["content_workflow", "partner_pipeline", "manual_handoffs"],
        ["event_scale", "content_volume", "partner_pipeline"],
        ["CRM", "content tools", "ticketing", "analytics"],
        ["partners", "audiences", "content", "events"],
        ["CRM", "content systems", "analytics"],
        ["content operations", "partner research"],
        ["partner follow-up", "content workflow"],
        ["PDPL", "rights/permissions"],
        ["sponsorship", "direct", "RFP"],
        ["Revenue Command Pilot", "Partner / Distributor Desk"],
        ["partner problem", "content workflow", "rights boundary"],
        ["commercial workflow", "content operations"],
        ["rights permission verified", "partner acceptance captured"],
        ["AI الألعاب السعودية", "أتمتة الرياضة", "الصناعات الإبداعية AI"],
    ),
    Sector.ASSOCIATIONS_NONPROFITS: _p(
        "الجمعيات والقطاع غير الربحي", "Associations & Nonprofits",
        ["NCNP", "SDAIA"], ["sdaia", "gastat"],
        ["nonprofits", "associations", "foundations"],
        ["nonprofit", "membership", "program delivery"],
        ("ceo", "operations_director", "finance_director"),
        ["reporting_burden", "limited_capacity", "service_backlog"],
        ["program_scale", "reporting_deadline", "member_service_backlog"],
        ["CRM", "accounting", "case/program management"],
        ["members", "beneficiaries", "programs", "financial records"],
        ["CRM", "accounting", "reporting"],
        ["knowledge assistant", "report drafting support"],
        ["case routing", "reporting workflow"],
        ["PDPL", "nonprofit governance"],
        ["direct", "grants/partner"],
        ["AI Company OS Setup", "Revenue Proof Sprint"],
        ["program baseline", "beneficiary/member data boundary", "reporting flow"],
        ["operations automation", "reporting/data"],
        ["beneficiary data boundary verified", "program acceptance captured"],
        ["AI الجمعيات السعودية", "أتمتة القطاع غير الربحي", "حوكمة البيانات للجمعيات"],
    ),
}

if set(SECTOR_PROFILES) != set(Sector):
    missing = sorted(s.value for s in set(Sector) - set(SECTOR_PROFILES))
    extra = sorted(str(s) for s in set(SECTOR_PROFILES) - set(Sector))
    raise RuntimeError(f"SECTOR_COMMERCIAL_COVERAGE_INVALID missing={missing} extra={extra}")

for _sector, _profile in SECTOR_PROFILES.items():
    invalid = sorted(set(_profile.offers) - CANONICAL_OFFERS)
    if invalid:
        raise RuntimeError(f"NON_CANONICAL_OFFER sector={_sector.value} offers={invalid}")


_SOURCE_CATALOG: dict[str, tuple[str, str, int]] = {
    "zatca": ("ZATCA", "https://zatca.gov.sa/en/MediaCenter/News/Pages/Wave25-E-invoicing.aspx", 30),
    "jadeer": ("Monsha'at", "https://www.monshaat.gov.sa/en/node/12778", 60),
    "etimad": ("Etimad", "https://tenders.etimad.sa/", 1),
    "sama": ("SAMA", "https://www.sama.gov.sa/", 30),
    "sdaia": ("SDAIA", "https://sdaia.gov.sa/", 30),
    "cst": ("CST", "https://www.cst.gov.sa/", 30),
    "moh": ("Ministry of Health", "https://www.moh.gov.sa/", 30),
    "rega": ("REGA", "https://rega.gov.sa/en/rega-services/platforms/saudi-proptech-hub/", 30),
    "gastat": ("GASTAT", "https://www.stats.gov.sa/", 90),
    "mim": ("Ministry of Industry and Mineral Resources", "https://mim.gov.sa/", 30),
    "modon": ("MODON", "https://modon.gov.sa/", 30),
    "tga": ("Transport General Authority", "https://www.tga.gov.sa/", 30),
    "mawani": ("Saudi Ports Authority", "https://mawani.gov.sa/", 30),
    "tourism": ("Ministry of Tourism", "https://mt.gov.sa/", 30),
    "hrdf": ("HRDF", "https://www.hrdf.org.sa/", 30),
}


def _source(source_id: str, observed: datetime) -> SourceRef:
    authority, url, days = _SOURCE_CATALOG[source_id]
    return SourceRef(
        source_id=source_id,
        source_url=url,
        source_authority=authority,
        observed_at=observed.isoformat(),
        fresh_until=(observed + timedelta(days=days)).isoformat(),
        refresh_policy=f"refresh_every_{days}d",
    )


def _signal(
    signal_id: str,
    source: SourceRef,
    sector: str,
    problem: str,
    trigger: str,
    diagnostic: list[str],
    offers: list[str],
    deadline: str = UNKNOWN,
) -> MarketSignalRecord:
    return MarketSignalRecord(
        signal_id=signal_id,
        source_url=source.source_url,
        source_authority=source.source_authority,
        source_date=source.source_date,
        observed_at=source.observed_at,
        fresh_until=source.fresh_until,
        sector=sector,
        problem=problem,
        trigger=trigger,
        deadline=deadline,
        dealix_match=["free_diagnostic", "evidence_governed_delivery"],
        diagnostic_match=diagnostic,
        offer_match=offers,
    )


class SectorCommercialFactory:
    """Compile exactly one commercial pack for every canonical sector."""

    def build(self, sector: Sector) -> SectorCommercialPack:
        observed = datetime.now(UTC)
        p = SECTOR_PROFILES[sector]
        sources = [_source(source_id, observed) for source_id in p.sources]
        by_id = {source.source_id: source for source in sources}
        signals: list[MarketSignalRecord] = []
        if "zatca" in by_id:
            signals.append(
                _signal(
                    "fatoora_wave25",
                    by_id["zatca"],
                    sector.value,
                    "e_invoicing_readiness",
                    "official Fatoora integration wave; verify customer notification before treating as applicable",
                    ["Fatoora readiness", "systems/integration", "finance operations"],
                    ["AI Company OS Setup", "Revenue Proof Sprint"],
                    deadline="2027-02-01 for notified Wave 25 taxpayers; customer applicability must be verified",
                )
            )
        if "jadeer" in by_id:
            signals.append(
                _signal(
                    "jadeer_supplier_readiness",
                    by_id["jadeer"],
                    sector.value,
                    "supplier_readiness",
                    "supplier qualification/readiness pathway",
                    ["supplier readiness", "B2G readiness"],
                    ["B2G Readiness Sprint", "Saudi Opportunity Snapshot"],
                )
            )
        if "etimad" in by_id:
            signals.append(
                _signal(
                    "etimad_tender_radar",
                    by_id["etimad"],
                    sector.value,
                    "tender_readiness",
                    "relevant public tender discovered; count is a timestamped snapshot only",
                    ["B2G readiness", "tender readiness"],
                    ["B2G Readiness Sprint", "Saudi Opportunity Snapshot"],
                )
            )
        if "sama" in by_id:
            signals.append(
                _signal(
                    "sama_open_banking",
                    by_id["sama"],
                    sector.value,
                    "regulated_integration_readiness",
                    "Open Banking licensing/integration development",
                    ["AI/data/integration readiness", "risk/control"],
                    ["AI Company OS Setup", "Revenue Proof Sprint"],
                )
            )
        if "moh" in by_id:
            signals.append(
                _signal(
                    "moh_digital_health_sandbox",
                    by_id["moh"],
                    sector.value,
                    "digital_health_validation",
                    "digital-health/AI innovation or sandbox pathway",
                    ["AI readiness", "privacy/security", "delivery readiness"],
                    ["AI Company OS Setup", "Revenue Proof Sprint"],
                )
            )
        if "rega" in by_id:
            signals.append(
                _signal(
                    "rega_proptech_pathway",
                    by_id["rega"],
                    sector.value,
                    "proptech_regulatory_readiness",
                    "PropTech regulatory/innovation pathway",
                    ["digital readiness", "workflow automation", "privacy/security"],
                    ["AI Company OS Setup", "Revenue Proof Sprint"],
                )
            )

        offer_matches = list(p.offers)
        buyers = list(p.buyers)
        return SectorCommercialPack(
            sector_id=sector.value,
            arabic_name=p.ar,
            english_name=p.en,
            market_context=["sector pattern knowledge; never a customer fact"],
            saudi_context=["Saudi-first", "official-source priority", "Arabic-first with English parity"],
            official_sources=sources,
            regulators=p.regulators,
            current_signals=signals,
            freshness="source-specific; expired evidence cannot remain current",
            icp_segments=p.icp,
            company_size=["SME", "mid-market", "enterprise"],
            business_models=p.models,
            geography=["Saudi Arabia"],
            digital_maturity=["manual", "digitized", "integrated", "AI-ready"],
            buyer_roles=buyers,
            economic_buyer=buyers[0],
            champion=buyers[1],
            technical_buyer=buyers[2],
            user_roles=["process_owner", "operator"],
            blockers=["missing_evidence", "unclear_owner", "procurement_friction", *p.pains[:1]],
            top_pain_patterns=p.pains,
            trigger_events=p.triggers,
            regulatory_triggers=[t for t in p.triggers if any(k in t.lower() for k in ("fatoora", "sandbox", "banking", "control"))],
            procurement_triggers=["new_RFP_or_tender", "vendor_onboarding", "framework_renewal"],
            growth_triggers=["new_market", "new_product_or_site", "volume_growth"],
            cost_triggers=["manual_work", "exception_volume", "rework"],
            risk_triggers=["control_gap", "compliance_change", "data_or_security_concern"],
            systems_typically_used=p.systems,
            data_sources=p.data,
            integration_surfaces=p.integrations,
            diagnostic_modules=["UNIVERSAL_CORE", f"SECTOR_OVERLAY::{sector.value}", "BUYER_ROLE_OVERLAY", "COMPANY_STAGE_OVERLAY", "TRIGGER_OVERLAY"],
            diagnostic_price=FREE,
            ai_opportunities=p.ai,
            automation_opportunities=p.automation,
            workflow_opportunities=["current-state mapping", "handoff/approval optimization", "exception management"],
            data_opportunities=["data quality", "lineage", "management reporting"],
            security_concerns=["least privilege", "auditability", "customer data boundary", "prompt injection/tool misuse"],
            privacy_concerns=["PDPL", "consent", "data minimization", "purpose limitation"],
            compliance_concerns=p.compliance,
            procurement_paths=p.procurement,
            b2b_paths=["website inbound", "existing relationships", "warm introductions", "partner referrals"],
            b2g_paths=["Etimad research", "supplier readiness", "prime/subcontractor route"],
            partner_paths=["systems integrator", "sector specialist", "distributor/referral partner"],
            offer_matches=offer_matches,
            proposal_modules=p.proposal,
            delivery_modules=p.delivery,
            acceptance_patterns=["baseline recorded", "scope/exclusions agreed", *p.acceptance],
            proof_requirements=["provider/system receipt", "acceptance evidence", "customer validation before public proof"],
            seo_themes=p.seo,
            content_themes=["official signal explainer", "buyer guide", "free diagnostic CTA"],
            arabic_queries=[f"تشخيص مجاني {p.ar}", *p.seo[:2]],
            english_queries=[f"free {p.en} diagnostic Saudi Arabia", *p.seo[:2]],
            maturity=SectorMaturity.RESEARCHED,
            evidence_grade="PATTERN_PLUS_OFFICIAL_PUBLIC_SOURCE",
            risk=["research_is_not_relationship", "public_contact_is_not_consent", "pattern_is_not_customer_fact"],
            last_refresh=observed.isoformat(),
            promote_criteria=["real_interaction", "qualified_problem", "delivery_fit", "evidence_improves"],
            kill_criteria=["no_customer_problem", "no_buyer", "no_acquisition_path", "negative_economics", "unacceptable_risk"],
        )

    def build_all(self) -> list[SectorCommercialPack]:
        packs = [self.build(sector) for sector in Sector]
        if len(packs) != len(Sector) or len({pack.sector_id for pack in packs}) != len(Sector):
            raise RuntimeError("SECTOR_PACK_COVERAGE_FAILED")
        return packs

    def coverage_receipt(self) -> dict[str, Any]:
        packs = self.build_all()
        return {
            "canonical_sectors": len(Sector),
            "sectors_covered": len(packs),
            "coverage_percent": 100,
            "all_diagnostics_free": all(pack.diagnostic_price == FREE for pack in packs),
            "duplicates": len(packs) - len({pack.sector_id for pack in packs}),
            "canonical_offers_only": all(set(pack.offer_matches) <= CANONICAL_OFFERS for pack in packs),
            "research_never_pipeline": all(
                not signal.counts_as_pipeline
                and not signal.counts_as_relationship
                and not signal.counts_as_consent
                and not signal.counts_as_revenue
                for pack in packs
                for signal in pack.current_signals
            ),
        }


__all__ = [
    "SectorCommercialFactory",
    "SectorCommercialPack",
    "SectorMaturity",
    "SourceRef",
    "MarketSignalRecord",
    "SECTOR_PROFILES",
    "CANONICAL_OFFERS",
    "FREE",
    "UNKNOWN",
]
