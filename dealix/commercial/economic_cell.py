"""Economic Cell Model — addressable combination for Dealix portfolio.

An economic cell is NOT a project. It is an addressable combination of:
sector × buyer × problem × workflow/capability × offer × monetization rail
× distribution rail × procurement rail

The registry represents 500+ addressable cells without spawning 500 projects.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ─── Canonical Dimensions ──────────────────────────────────────────────


class Sector(StrEnum):
    GOVERNMENT_B2G = "government_b2g"
    CONSTRUCTION_EPC = "construction_epc"
    INDUSTRIAL_MANUFACTURING = "industrial_manufacturing"
    LOGISTICS_SUPPLY_CHAIN = "logistics_supply_chain"
    ENERGY_UTILITIES_OIL_GAS = "energy_utilities_oil_gas"
    MINING_METALS = "mining_metals"
    REAL_ESTATE_PROPTECH = "real_estate_proptech"
    HEALTHCARE = "healthcare"
    FINANCE_FINTECH_INSURANCE = "finance_fintech_insurance"
    RETAIL_COMMERCE_ECOMMERCE = "retail_commerce_ecommerce"
    TOURISM_HOSPITALITY = "tourism_hospitality"
    PROFESSIONAL_SERVICES = "professional_services"
    TECHNOLOGY_SAAS_SI = "technology_saas_si"
    TELECOM_MEDIA_MARKETING = "telecom_media_marketing"
    EDUCATION_TRAINING = "education_training"
    AGRICULTURE_FOOD_WATER = "agriculture_food_water"
    MOBILITY_AUTOMOTIVE = "mobility_automotive"
    EXPORT_IMPORT_RHQ = "export_import_rhq"
    CREATIVE_SPORTS_GAMING = "creative_sports_gaming"
    ASSOCIATIONS_NONPROFITS = "associations_nonprofits"


class Geography(StrEnum):
    KSA = "ksa"
    GCC = "gcc"
    MENA = "mena"
    GLOBAL = "global"


class BuyerGroup(StrEnum):
    FOUNDER_OWNER = "founder_owner"
    CEO = "ceo"
    COO = "coo"
    CFO = "cfo"
    CIO = "cio"
    CTO = "cto"
    CDO = "cdo"
    CISO = "ciso"
    HEAD_DIGITAL_TRANSFORMATION = "head_digital_transformation"
    COMMERCIAL_DIRECTOR = "commercial_director"
    SALES_DIRECTOR = "sales_director"
    MARKETING_DIRECTOR = "marketing_director"
    PROCUREMENT_DIRECTOR = "procurement_director"
    FINANCE_DIRECTOR = "finance_director"
    OPERATIONS_DIRECTOR = "operations_director"
    HR_DIRECTOR = "hr_director"
    PROJECT_DIRECTOR = "project_director"
    PMO = "pmo"
    COMPLIANCE_RISK = "compliance_risk"
    CUSTOMER_SERVICE = "customer_service"
    END_USER = "end_user"


class OrganizationType(StrEnum):
    GOVERNMENT = "government"
    LARGE_ENTERPRISE = "large_enterprise"
    MID_MARKET = "mid_market"
    SME = "sme"
    STARTUP = "startup"
    NONPROFIT = "nonprofit"


class OrganizationSize(StrEnum):
    MICRO = "micro"  # 1-10
    SMALL = "small"  # 11-50
    MEDIUM = "medium"  # 51-250
    LARGE = "large"  # 251-1000
    ENTERPRISE = "enterprise"  # 1000+


class ProblemClass(StrEnum):
    REVENUE_LEAKAGE = "revenue_leakage"
    CONVERSION_LEAKAGE = "conversion_leakage"
    QUOTE_DELAY = "quote_delay"
    SALES_FOLLOWUP_FAILURE = "sales_followup_failure"
    COLLECTION_DELAY = "collection_delay"
    COST_LEAKAGE = "cost_leakage"
    WORKFORCE_BOTTLENECK = "workforce_bottleneck"
    REPETITIVE_MANUAL_WORK = "repetitive_manual_work"
    MANUAL_HANDOFFS = "manual_handoffs"
    APPROVAL_DELAY = "approval_delay"
    PROCUREMENT_DELAY = "procurement_delay"
    PROJECT_DELAY = "project_delay"
    DOCUMENT_CHAOS = "document_chaos"
    DATA_FRAGMENTATION = "data_fragmentation"
    REPORTING_DELAY = "reporting_delay"
    DECISION_LATENCY = "decision_latency"
    CUSTOMER_SUPPORT_BACKLOG = "customer_support_backlog"
    CHURN = "churn"
    KNOWLEDGE_LOSS = "knowledge_loss"
    FORECASTING_WEAKNESS = "forecasting_weakness"
    INVENTORY_EXCEPTION = "inventory_exception"
    QUALITY_FAILURE = "quality_failure"
    COMPLIANCE_BURDEN = "compliance_burden"
    CYBER_RISK = "cyber_risk"
    AI_GOVERNANCE_RISK = "ai_governance_risk"
    SUPPLIER_FRICTION = "supplier_friction"
    MARKET_ENTRY_FRICTION = "market_entry_friction"
    UNUSED_DATA = "unused_data"
    INTEGRATION_FAILURE = "integration_failure"
    OPERATIONAL_EXCEPTION_OVERLOAD = "operational_exception_overload"


class MonetizationRail(StrEnum):
    FREE_DIAGNOSTIC = "free_diagnostic"
    PAID_DIAGNOSTIC = "paid_diagnostic"
    PAID_SPRINT = "paid_sprint"
    FIXED_SCOPE_IMPLEMENTATION = "fixed_scope_implementation"
    CUSTOMER_PILOT = "customer_pilot"
    MANAGED_SERVICE = "managed_service"
    MONTHLY_RETAINER = "monthly_retainer"
    SAAS_SUBSCRIPTION = "saas_subscription"
    SEAT_BASED = "seat_based"
    USAGE_BASED_API = "usage_based_api"
    CONSUMPTION_BILLING = "consumption_billing"
    PRIVATE_VPC_DEPLOYMENT = "private_vpc_deployment"
    ENTERPRISE_LICENSE = "enterprise_license"
    WHITE_LABEL = "white_label"
    CO_DELIVERY_REVENUE_SHARE = "co_delivery_revenue_share"
    REFERRAL = "referral"
    RESELLER = "reseller"
    PARTNER_MARGIN = "partner_margin"
    MARKETPLACE_APP = "marketplace_app"
    CLOUD_MARKETPLACE = "cloud_marketplace"
    DATA_INTELLIGENCE_SUB = "data_intelligence_sub"
    TRAINING_ACADEMY = "training_academy"
    TEMPLATES_PLAYBOOKS = "templates_playbooks"
    SUPPORT_SLA = "support_sla"
    IP_LICENSING = "ip_licensing"


class DistributionRail(StrEnum):
    WEBSITE_INBOUND = "website_inbound"
    SEO = "seo"
    AEO_AI_SEARCH = "aeo_ai_search"
    FOUNDER_CONTENT = "founder_content"
    CONSENT_EMAIL = "consent_email"
    EXISTING_RELATIONSHIPS = "existing_relationships"
    WARM_INTROS = "warm_intros"
    CUSTOMER_REFERRALS = "customer_referrals"
    PARTNER_REFERRALS = "partner_referrals"
    AGENCIES = "agencies"
    CONSULTANCIES = "consultancies"
    SYSTEMS_INTEGRATORS = "systems_integrators"
    DISTRIBUTORS = "distributors"
    VENDOR_ECOSYSTEMS = "vendor_ecosystems"
    EVENTS_CONFERENCES = "events_conferences"
    CHAMBERS_ASSOCIATIONS = "chambers_associations"
    SUPPLIER_PORTALS = "supplier_portals"
    PROCUREMENT_PORTALS = "procurement_portals"
    ETIMAD_INTELLIGENCE = "etimad_intelligence"
    SAUDI_ECOSYSTEMS = "saudi_ecosystems"
    MISA_INVEST_SAUDI = "misa_invest_saudi"
    CLOUD_MARKETPLACES = "cloud_marketplaces"
    APP_MARKETPLACES = "app_marketplaces"
    TECH_ALLIANCES = "tech_alliances"
    SANDBOX_PROGRAMS = "sandbox_programs"
    ACADEMY_COMMUNITY = "academy_community"
    PROOF_DISTRIBUTION = "proof_distribution"


class ProcurementRail(StrEnum):
    DIRECT_PURCHASE = "direct_purchase"
    VENDOR_ONBOARDING = "vendor_onboarding"
    SUPPLIER_PORTAL = "supplier_portal"
    RFQ = "rfq"
    RFP = "rfp"
    TENDER = "tender"
    FRAMEWORK_AGREEMENT = "framework_agreement"
    PRIME_CONTRACTOR = "prime_contractor"
    SUBCONTRACTOR = "subcontractor"
    RESELLER = "reseller"
    CHANNEL_PARTNER = "channel_partner"
    MARKETPLACE_PROCUREMENT = "marketplace_procurement"
    CLOUD_MARKETPLACE_PROCUREMENT = "cloud_marketplace_procurement"
    GOVERNMENT_PROCUREMENT = "government_procurement"


class EvidenceLevel(StrEnum):
    L0_ANECDOTAL = "L0_anecdotal"
    L1_PUBLIC_SOURCE = "L1_public_source"
    L2_THIRD_PARTY = "L2_third_party"
    L3_DIRECT_INTERACTION = "L3_direct_interaction"
    L4_CONTRACTUAL = "L4_contractual"
    L5_CUSTOMER_VALIDATED = "L5_customer_validated"


class LifecycleState(StrEnum):
    DISCOVERED = "discovered"
    WATCH = "watch"
    RESEARCH = "research"
    VALIDATE = "validate"
    QUALIFIED = "qualified"
    ACTIVE_LIGHT = "active_light"
    CANDIDATE_DEEP = "candidate_deep"
    ACTIVE_DEEP = "active_deep"
    DELIVERING = "delivering"
    PROVEN = "proven"
    PRODUCTIZE = "productize"
    SCALE = "scale"
    BLOCKED = "blocked"
    PAUSED = "paused"
    KILLED = "killed"
    RETIRED = "retired"


class PromotionGate(StrEnum):
    GATE_1_REAL_SIGNAL = "gate_1_real_signal"
    GATE_2_BUYER = "gate_2_buyer"
    GATE_3_ECONOMIC_PAIN = "gate_3_economic_pain"
    GATE_4_ACCESS = "gate_4_access"
    GATE_5_PROCUREMENT = "gate_5_procurement"
    GATE_6_DELIVERY = "gate_6_delivery"
    GATE_7_ECONOMICS = "gate_7_economics"
    GATE_8_PROOF = "gate_8_proof"
    GATE_9_REPEATABILITY = "gate_9_repeatability"
    GATE_10_RISK = "gate_10_risk"


class KillTrigger(StrEnum):
    NO_CUSTOMER_PROBLEM = "no_customer_problem"
    NO_BUYER = "no_buyer"
    NO_ACQUISITION_PATH = "no_acquisition_path"
    NO_PROCUREMENT_ROUTE = "no_procurement_route"
    NEGATIVE_ECONOMICS = "negative_economics"
    UNACCEPTABLE_RISK = "unacceptable_risk"
    EXTREME_DELIVERY_BURDEN = "extreme_delivery_burden"
    EXCESSIVE_FOUNDER_DEPENDENCY = "excessive_founder_dependency"
    NO_MEASURABLE_ACCEPTANCE = "no_measurable_acceptance"
    DUPLICATE_CAPABILITY = "duplicate_capability"
    NO_MOVEMENT_AFTER_EXPERIMENTS = "no_movement_after_experiments"
    CUSTOMER_REJECTION = "customer_rejection"
    STRONGER_SUBSTITUTE = "stronger_substitute"
    TECHNICAL_IMPOSSIBILITY = "technical_impossibility"
    COMPLIANCE_BARRIER = "compliance_barrier"
    EVIDENCE_DETERIORATION = "evidence_deterioration"


UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"


# ─── Core Models ───────────────────────────────────────────────────────


class Identity(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    cell_id: str = Field(..., min_length=1)
    canonical_name: str = Field(..., min_length=1)
    version: int = Field(default=1, ge=1)
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class Market(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    geography: Geography = Geography.KSA
    sector: Sector
    subsector: str = ""
    organization_type: OrganizationType = OrganizationType.LARGE_ENTERPRISE
    organization_size: OrganizationSize = OrganizationSize.ENTERPRISE


class Buyer(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    buyer_group: BuyerGroup
    economic_buyer: str = ""
    champion_role: str = ""
    operational_user: str = ""
    procurement_actor: str = ""
    security_actor: str = ""


class Problem(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    problem_class: ProblemClass
    pain_statement: str = ""
    frequency: str = ""
    current_workaround: str = ""
    measurable_loss_type: str = ""
    urgency: str = "UNKNOWN"
    trigger: str = ""


class Value(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    revenue_upside: str = UNKNOWN
    cost_avoidance: str = UNKNOWN
    time_saved: str = UNKNOWN
    risk_reduction: str = UNKNOWN
    decision_latency_reduction: str = UNKNOWN
    working_capital_effect: str = UNKNOWN
    founder_minutes_saved: str = UNKNOWN
    customer_experience_effect: str = UNKNOWN


class Offer(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    offer_family: str = ""
    entry_offer: str = ""
    expansion_offer: str = ""
    acceptance_criteria: str = ""


class Monetization(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    monetization_rail: MonetizationRail = MonetizationRail.FREE_DIAGNOSTIC
    one_time_or_recurring: str = "unknown"
    billing_basis: str = "unknown"
    margin_hypothesis: str = UNKNOWN
    pricing_evidence_state: str = UNKNOWN


class Distribution(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    distribution_rail: DistributionRail = DistributionRail.WEBSITE_INBOUND
    relationship_requirement: str = ""
    consent_requirement: str = ""
    acquisition_cost_evidence: str = UNKNOWN
    proof_requirement: str = ""


class Procurement(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    procurement_rail: ProcurementRail = ProcurementRail.DIRECT_PURCHASE
    vendor_registration_requirement: str = ""
    tender_requirement: str = ""
    framework_requirement: str = ""
    partner_requirement: str = ""
    procurement_friction: str = "unknown"


class Execution(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    capability_dependencies: list[str] = Field(default_factory=list)
    reusable_factory_dependencies: list[str] = Field(default_factory=list)
    integration_dependencies: list[str] = Field(default_factory=list)
    delivery_complexity: str = "unknown"
    support_burden: str = "unknown"
    founder_dependency: str = "unknown"
    compute_dependency: str = "unknown"


class Evidence(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    evidence_level: EvidenceLevel = EvidenceLevel.L0_ANECDOTAL
    evidence_sources: list[str] = Field(default_factory=list)
    evidence_age: str = UNKNOWN
    relationship_evidence: str = UNKNOWN
    customer_problem_evidence: str = UNKNOWN
    willingness_to_pay_evidence: str = UNKNOWN
    delivery_evidence: str = UNKNOWN
    customer_validation_evidence: str = UNKNOWN


class Economics(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    probability_adjusted_value: str = UNKNOWN
    time_to_cash: str = UNKNOWN
    recurring_value_potential: str = UNKNOWN
    gross_margin_hypothesis: str = UNKNOWN
    cost_to_validate: str = UNKNOWN
    cost_to_sell: str = UNKNOWN
    cost_to_deliver: str = UNKNOWN
    compute_cost: str = UNKNOWN
    maintenance_cost: str = UNKNOWN
    capital_requirement: str = UNKNOWN


class Risk(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    commercial_risk: str = "unknown"
    delivery_risk: str = "unknown"
    cybersecurity_risk: str = "unknown"
    privacy_risk: str = "unknown"
    regulatory_risk: str = "unknown"
    reputational_risk: str = "unknown"
    irreversibility: str = "unknown"
    dependency_risk: str = "unknown"


class Portfolio(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    lifecycle_state: LifecycleState = LifecycleState.DISCOVERED
    economic_score: float = Field(default=0.0, ge=0.0)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    promotion_gate: PromotionGate | None = None
    kill_gate: KillTrigger | None = None
    next_evidence_needed: list[str] = Field(default_factory=list)
    next_action: str = ""
    assigned_agent: str = ""
    deep_wip_slot: bool = False
    stop_loss: str = ""


class Proof(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    proof_events: list[str] = Field(default_factory=list)
    proof_strength: str = UNKNOWN
    customer_validated: bool = False
    public_use_authorized: bool = False


class EconomicCell(BaseModel):
    """Complete economic cell — addressable, evidence-aware, portfolio-ready."""

    model_config = ConfigDict(extra="forbid")

    identity: Identity
    market: Market
    buyer: Buyer
    problem: Problem
    value: Value
    offer: Offer
    monetization: Monetization
    distribution: Distribution
    procurement: Procurement
    execution: Execution
    evidence: Evidence
    economics: Economics
    risk: Risk
    portfolio: Portfolio
    proof: Proof

    @field_validator("identity", mode="before")
    @classmethod
    def _ensure_identity(cls, v: dict[str, Any] | Identity) -> Identity:
        if isinstance(v, Identity):
            return v
        if isinstance(v, dict):
            cell_id = v.get("cell_id") or cls._generate_cell_id(v)
            return Identity(
                cell_id=cell_id,
                canonical_name=v.get("canonical_name", "unnamed"),
                version=v.get("version", 1),
            )
        raise ValueError("identity must be dict or Identity")

    @staticmethod
    def _generate_cell_id(data: dict[str, Any]) -> str:
        parts = [
            data.get("market", {}).get("sector", ""),
            data.get("buyer", {}).get("buyer_group", ""),
            data.get("problem", {}).get("problem_class", ""),
            data.get("monetization", {}).get("monetization_rail", ""),
            data.get("distribution", {}).get("distribution_rail", ""),
        ]
        key = "|".join(str(p) for p in parts if p)
        return f"cell_{hashlib.sha256(key.encode()).hexdigest()[:12]}"

    def fingerprint(self) -> str:
        """Deterministic fingerprint for deduplication."""
        payload = self.model_dump(mode="json", exclude={"identity": {"created_at", "updated_at", "version"}})
        return hashlib.sha256(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()[:16]

    def is_active_deep(self) -> bool:
        return self.portfolio.lifecycle_state == LifecycleState.ACTIVE_DEEP

    def is_candidate_deep(self) -> bool:
        return self.portfolio.lifecycle_state == LifecycleState.CANDIDATE_DEEP

    def promotion_ready(self) -> bool:
        return self.portfolio.lifecycle_state in {
            LifecycleState.QUALIFIED,
            LifecycleState.ACTIVE_LIGHT,
        }

    def kill_evaluated(self) -> bool:
        return self.portfolio.kill_gate is not None


# ─── Template System for Sparse Materialization ────────────────────────


class CellTemplate(BaseModel):
    """Template for generating economic cells without full manual specification."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    template_id: str
    name: str
    description: str
    sector: Sector
    buyer_group: BuyerGroup
    problem_class: ProblemClass
    monetization_rail: MonetizationRail = MonetizationRail.FREE_DIAGNOSTIC
    distribution_rail: DistributionRail = DistributionRail.WEBSITE_INBOUND
    procurement_rail: ProcurementRail = ProcurementRail.DIRECT_PURCHASE
    default_evidence_level: EvidenceLevel = EvidenceLevel.L0_ANECDOTAL
    default_lifecycle: LifecycleState = LifecycleState.DISCOVERED
    capability_tags: list[str] = Field(default_factory=list)
    factory_dependencies: list[str] = Field(default_factory=list)


# Pre-defined templates for common patterns
DEFAULT_TEMPLATES: tuple[CellTemplate, ...] = (
    CellTemplate(
        template_id="rev_cmd_pilot",
        name="Revenue Command Pilot",
        description="30-day governed pilot for revenue operations automation",
        sector=Sector.TECHNOLOGY_SAAS_SI,
        buyer_group=BuyerGroup.CEO,
        problem_class=ProblemClass.REVENUE_LEAKAGE,
        monetization_rail=MonetizationRail.CUSTOMER_PILOT,
        distribution_rail=DistributionRail.WARM_INTROS,
        capability_tags=["revenue_command", "pilot_delivery", "proof_builder"],
        factory_dependencies=["revenue_ops_factory", "proof_factory"],
    ),
    CellTemplate(
        template_id="company_brain_sprint",
        name="Company Brain Governed AI Sprint",
        description="Bounded AI workflow assessment with authority audit",
        sector=Sector.TECHNOLOGY_SAAS_SI,
        buyer_group=BuyerGroup.CTO,
        problem_class=ProblemClass.KNOWLEDGE_LOSS,
        monetization_rail=MonetizationRail.PAID_SPRINT,
        distribution_rail=DistributionRail.WARM_INTROS,
        capability_tags=["company_brain", "governed_ai", "workflow_design"],
        factory_dependencies=["company_brain_factory", "ai_workflow_factory"],
    ),
    CellTemplate(
        template_id="saudi_market_access",
        name="Saudi Market Access Sprint",
        description="Regulatory + commercial entry for foreign companies",
        sector=Sector.EXPORT_IMPORT_RHQ,
        buyer_group=BuyerGroup.CEO,
        problem_class=ProblemClass.MARKET_ENTRY_FRICTION,
        monetization_rail=MonetizationRail.PAID_SPRINT,
        distribution_rail=DistributionRail.MISA_INVEST_SAUDI,
        procurement_rail=ProcurementRail.GOVERNMENT_PROCUREMENT,
        capability_tags=["market_entry", "regulatory", "procurement_intel"],
        factory_dependencies=["market_intel_factory", "procurement_factory"],
    ),
    CellTemplate(
        template_id="construction_doc_to_cash",
        name="Construction Document-to-Cash",
        description="Document intelligence for EPC payment acceleration",
        sector=Sector.CONSTRUCTION_EPC,
        buyer_group=BuyerGroup.CFO,
        problem_class=ProblemClass.COLLECTION_DELAY,
        monetization_rail=MonetizationRail.FIXED_SCOPE_IMPLEMENTATION,
        distribution_rail=DistributionRail.SYSTEMS_INTEGRATORS,
        capability_tags=["document_intel", "payment_acceleration", "fatoora"],
        factory_dependencies=["document_factory", "payment_factory"],
    ),
    CellTemplate(
        template_id="tender_intelligence",
        name="Tender/RFP Intelligence Desk",
        description="Government tender monitoring and response automation",
        sector=Sector.GOVERNMENT_B2G,
        buyer_group=BuyerGroup.PROCUREMENT_DIRECTOR,
        problem_class=ProblemClass.PROCUREMENT_DELAY,
        monetization_rail=MonetizationRail.MONTHLY_RETAINER,
        distribution_rail=DistributionRail.ETIMAD_INTELLIGENCE,
        procurement_rail=ProcurementRail.TENDER,
        capability_tags=["tender_intel", "rfp_automation", "b2g_readiness"],
        factory_dependencies=["tender_factory", "b2g_factory"],
    ),
)


__all__ = [
    # Enums
    "Sector",
    "Geography",
    "BuyerGroup",
    "OrganizationType",
    "OrganizationSize",
    "ProblemClass",
    "MonetizationRail",
    "DistributionRail",
    "ProcurementRail",
    "EvidenceLevel",
    "LifecycleState",
    "PromotionGate",
    "KillTrigger",
    "UNKNOWN",
    # Dimension Models
    "Identity",
    "Market",
    "Buyer",
    "Problem",
    "Value",
    "Offer",
    "Monetization",
    "Distribution",
    "Procurement",
    "Execution",
    "Evidence",
    "Economics",
    "Risk",
    "Portfolio",
    "Proof",
    # Core
    "EconomicCell",
    # Templates
    "CellTemplate",
    "DEFAULT_TEMPLATES",
]
