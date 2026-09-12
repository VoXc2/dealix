"""Sector Company Blueprint — one complete, governed virtual business unit spec.

A blueprint is PATTERN knowledge inside the single Dealix company machine: it
reuses the canonical sector intelligence, taxonomy, governed sector packs and
the universal diagnostic factory. It never creates a second company, never
asserts customer facts, and never invents scores: unknown stays `UNKNOWN`.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.economic_cell import Sector
from dealix.commercial.sector_company_factory import SECTOR_INTEL
from dealix.commercial.sector_pack_governance import SectorPackMaturity, SectorPackRegistry
from dealix.commercial.sector_taxonomy import UNKNOWN, taxonomy_for
from dealix.commercial.universal_diagnostic_factory import (
    FAMILY_AR,
    DiagnosticDepth,
    UniversalDiagnosticFactory,
)

MATURITY_LADDER = (
    "DISCOVERED",
    "RESEARCHED",
    "INTERNAL_READY",
    "MARKET_TEST_READY",
    "QUALIFIED_SIGNAL",
    "CUSTOMER_VALIDATED",
    "DELIVERY_PROVEN",
    "SCALE_READY",
)

PACK_TO_LADDER = {
    SectorPackMaturity.DRAFT: "DISCOVERED",
    SectorPackMaturity.RESEARCHED: "RESEARCHED",
    SectorPackMaturity.INTERNAL_READY: "INTERNAL_READY",
    SectorPackMaturity.VALIDATED: "INTERNAL_READY",
    SectorPackMaturity.PUBLIC_READY: "MARKET_TEST_READY",
    SectorPackMaturity.COMMERCIAL_SIGNAL: "QUALIFIED_SIGNAL",
    SectorPackMaturity.DELIVERY_PROVEN: "DELIVERY_PROVEN",
}

B2G_PROCUREMENT_MARKERS = ("etimad", "nupco", "government", "tender")
PARTNER_TYPES = ["implementation_partner", "consulting_partner", "cloud_partner", "industry_specialist"]


class BuyerCell(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    role: str
    segment: str
    truth_class: str = "PATTERN"
    kpis: list[str] = Field(default_factory=list)
    evidence_status: str = "UNKNOWN"


class ProblemCell(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    problem: str
    diagnostic_families: list[str] = Field(default_factory=list)
    automation_candidates: list[str] = Field(default_factory=list)
    truth_class: str = "PATTERN"
    evidence_status: str = "UNKNOWN"


class MarketContext(BaseModel):
    """Machine-readable market context — pattern knowledge only."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    sector_id: str
    ar_name: str = UNKNOWN
    en_name: str = UNKNOWN
    isic_sections: list[str] = Field(default_factory=list)
    isic_section_names: list[str] = Field(default_factory=list)
    isic_mapping_status: str = UNKNOWN
    saudi_strategic_overlay: list[str] = Field(default_factory=list)
    saudi_mapping_status: str = UNKNOWN
    regulator_labels: list[str] = Field(default_factory=list)
    regulator_validation_status: str = "REQUIRES_OFFICIAL_VERIFICATION"
    market_size_estimate: str = UNKNOWN
    growth_signals: list[str] = Field(default_factory=list)
    market_evidence_status: str = "UNKNOWN"


class ICPProfile(BaseModel):
    """Ideal Customer Profile — pattern knowledge only."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    icp_segments: list[str] = Field(default_factory=list)
    company_sizes: list[str] = Field(default_factory=list)
    business_models: list[str] = Field(default_factory=list)
    geography: list[str] = Field(default_factory=list)
    digital_maturity_levels: list[str] = Field(default_factory=list)
    evidence_status: str = "UNKNOWN"


class BuyerRoles(BaseModel):
    """Buyer roles with evidence status."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    major_buyer_types: list[str] = Field(default_factory=list)
    buyers: list[BuyerCell] = Field(default_factory=list)
    economic_buyer_role: str = UNKNOWN
    champion_role: str = UNKNOWN
    technical_buyer_role: str = UNKNOWN
    user_roles: list[str] = Field(default_factory=list)
    evidence_status: str = "UNKNOWN"


class OrganizationArchetypes(BaseModel):
    """Organization archetypes — pattern knowledge only."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    archetypes: list[str] = Field(default_factory=list)
    typical_sizes: list[str] = Field(default_factory=list)
    typical_structures: list[str] = Field(default_factory=list)
    evidence_status: str = "UNKNOWN"


class ProblemsAndWorkflows(BaseModel):
    """Problems and workflows — pattern knowledge only."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    top_problems: list[str] = Field(default_factory=list)
    problem_cells: list[ProblemCell] = Field(default_factory=list)
    workflows: list[str] = Field(default_factory=list)
    value_chains: list[str] = Field(default_factory=list)
    trigger_events: list[str] = Field(default_factory=list)
    evidence_status: str = "UNKNOWN"


class SignalsAndRegulation(BaseModel):
    """Signals and regulation — pattern knowledge only."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    growth_signals: list[str] = Field(default_factory=list)
    regulatory_triggers: list[str] = Field(default_factory=list)
    procurement_triggers: list[str] = Field(default_factory=list)
    cost_triggers: list[str] = Field(default_factory=list)
    risk_triggers: list[str] = Field(default_factory=list)
    regulation: list[str] = Field(default_factory=list)
    compliance_constraints: list[str] = Field(default_factory=list)
    evidence_status: str = "UNKNOWN"


class ProcurementPaths(BaseModel):
    """Procurement paths — pattern knowledge only."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    procurement_paths: list[str] = Field(default_factory=list)
    tender_paths: list[str] = Field(default_factory=list)
    b2b_paths: list[str] = Field(default_factory=list)
    b2g_paths: list[str] = Field(default_factory=list)
    partner_paths: list[str] = Field(default_factory=list)
    evidence_status: str = "UNKNOWN"


class PartnersAndCompetitors(BaseModel):
    """Partners and competitors — pattern knowledge only."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    partner_types: list[str] = Field(default_factory=list)
    competitor_types: list[str] = Field(default_factory=list)
    substitutes: list[str] = Field(default_factory=list)
    evidence_status: str = "UNKNOWN"


class TechnologyReadiness(BaseModel):
    """Technology readiness assessment — pattern knowledge only."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    existing_technology: list[str] = Field(default_factory=list)
    ai_readiness: str = UNKNOWN
    data_readiness: str = UNKNOWN
    infrastructure_readiness: str = UNKNOWN
    systems_typically_used: list[str] = Field(default_factory=list)
    data_sources: list[str] = Field(default_factory=list)
    integration_surfaces: list[str] = Field(default_factory=list)
    evidence_status: str = "UNKNOWN"


class DealixCapabilitiesAndOffers(BaseModel):
    """Dealix capabilities and offers for this sector."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    free_diagnostic_families: list[str] = Field(default_factory=list)
    dealix_capabilities: list[str] = Field(default_factory=list)
    offer_ladder: list[str] = Field(default_factory=list)
    pilot_options: list[str] = Field(default_factory=list)
    evidence_status: str = "UNKNOWN"


class DeliveryAndProof(BaseModel):
    """Delivery acceptance criteria and proof requirements."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    delivery_pack: str = UNKNOWN
    acceptance_criteria: list[str] = Field(default_factory=list)
    proof_requirements: list[str] = Field(default_factory=list)
    discovery_playbook: str = "discovery"
    evidence_status: str = "UNKNOWN"


class NextBestActions(BaseModel):
    """Next best actions — pattern knowledge only."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    actions: list[str] = Field(default_factory=list)
    seo_topics: list[str] = Field(default_factory=list)
    content_topics: list[str] = Field(default_factory=list)
    distribution_channels: list[str] = Field(default_factory=list)
    evidence_status: str = "UNKNOWN"


class SectorCompanyBlueprint(BaseModel):
    """Complete sector company blueprint with machine-readable context."""
    model_config = ConfigDict(extra="forbid")

    sector_id: str
    # Machine-readable context sections
    market: MarketContext
    icp: ICPProfile
    buyer_roles: BuyerRoles
    organization_archetypes: OrganizationArchetypes
    problems: ProblemsAndWorkflows
    signals: SignalsAndRegulation
    procurement: ProcurementPaths
    partners: PartnersAndCompetitors
    technology: TechnologyReadiness
    dealix_offers: DealixCapabilitiesAndOffers
    delivery_proof: DeliveryAndProof
    next_best_actions: NextBestActions
    # Metadata
    maturity_status: str = "DISCOVERED"
    completeness_pct: int = 0
    truth_class: str = "PATTERN"
    is_customer_fact: bool = False
    generated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    # ------------------------------------------------------------------
    # Backward-compatible read interface.
    #
    # The V5 contract stores richer sector context in nested models, but
    # existing Dealix consumers still rely on the legacy flat accessors.
    # These properties intentionally derive from the canonical nested truth
    # instead of creating a second source of truth.
    # ------------------------------------------------------------------

    @property
    def ar_name(self) -> str:
        return str(getattr(self.market, "ar_name", UNKNOWN))

    @property
    def en_name(self) -> str:
        return str(getattr(self.market, "en_name", UNKNOWN))

    @property
    def economic_score(self) -> str:
        # Pattern knowledge must never fabricate an economic score.
        return UNKNOWN

    @property
    def market_score(self) -> str:
        return UNKNOWN

    @property
    def delivery_readiness(self) -> str:
        value = getattr(self.delivery_proof, "delivery_readiness", UNKNOWN)
        return str(value or UNKNOWN)

    @property
    def proof_readiness(self) -> str:
        value = getattr(self.delivery_proof, "proof_readiness", UNKNOWN)
        return str(value or UNKNOWN)

    @property
    def buyers(self) -> list[BuyerCell]:
        """Legacy buyer-cell view derived from the nested buyer-role contract."""
        raw = getattr(self.buyer_roles, "roles", None)

        if raw is None:
            raw = getattr(self.buyer_roles, "buyer_roles", None)

        if raw is None and hasattr(self.buyer_roles, "model_dump"):
            payload = self.buyer_roles.model_dump()
            raw = (
                payload.get("roles")
                or payload.get("buyer_roles")
                or payload.get("buyers")
                or []
            )

        roles: list[str] = []
        for item in raw or []:
            if isinstance(item, str):
                roles.append(item)
            elif isinstance(item, dict):
                role = item.get("role") or item.get("name")
                if role:
                    roles.append(str(role))
            else:
                role = getattr(item, "role", None) or getattr(item, "name", None)
                if role:
                    roles.append(str(role))

        if not roles:
            intel = SECTOR_INTEL.get(Sector(self.sector_id), {})
            roles = list(intel.get("buyers", []))

        if not roles:
            roles = ["ceo"]

        return [
            BuyerCell(
                role=role,
                segment=("b2g" if self.sector_id == Sector.GOVERNMENT_B2G.value else "enterprise"),
            )
            for role in roles
        ]

    @property
    def top_problems(self) -> list[str]:
        raw = getattr(self.problems, "problems", None)

        if raw is None and hasattr(self.problems, "model_dump"):
            payload = self.problems.model_dump()
            raw = payload.get("problems") or payload.get("top_problems") or []

        if raw:
            return [str(x) for x in raw]

        intel = SECTOR_INTEL.get(Sector(self.sector_id), {})
        return list(intel.get("problems", []))


    # ------------------------------------------------------------------
    # V5 legacy read compatibility.
    # Canonical truth remains in the nested V5 models above.
    # These accessors are projections only, not duplicate truth fields.
    # ------------------------------------------------------------------

    @property
    def regulator_validation_status(self) -> str:
        """Legacy projection of governed regulator verification state."""
        value = getattr(
            self.market,
            "regulator_validation_status",
            "REQUIRES_OFFICIAL_VERIFICATION",
        )
        return str(value or "REQUIRES_OFFICIAL_VERIFICATION")

    @property
    def digital_maturity(self) -> str:
        """Legacy field remains UNKNOWN unless canonical evidence defines it."""
        return UNKNOWN

    @property
    def ai_maturity(self) -> str:
        """Legacy projection from the canonical technology readiness contract."""
        value = getattr(self.technology, "ai_readiness", UNKNOWN)
        return str(value or UNKNOWN)

    @property
    def problem_cells(self) -> list[Any]:
        """Legacy problem-cell view derived from nested problem truth."""
        cells = getattr(self.problems, "problem_cells", None)

        if cells is not None:
            return list(cells)

        if hasattr(self.problems, "model_dump"):
            payload = self.problems.model_dump()
            raw = payload.get("problem_cells") or []

            # The nested canonical model normally returns typed cells above.
            # Do not fabricate replacements when only serialized data exists.
            return list(raw)

        return []


    @property
    def isic_sections(self) -> list[str]:
        """Legacy ISIC projection from the canonical nested market context."""
        value = getattr(self.market, "isic_sections", None)

        if value is None and hasattr(self.market, "model_dump"):
            value = self.market.model_dump().get("isic_sections", [])

        return [str(section) for section in (value or [])]

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def _buyer_cells(intel: dict[str, Any]) -> list[BuyerCell]:
    roles = list(intel.get("buyers", []))
    if not roles:
        roles = ["ceo"]
    procurement = str(intel.get("procurement", "")).lower()
    segments = ["sme", "enterprise"]
    if any(marker in procurement for marker in B2G_PROCUREMENT_MARKERS):
        segments.append("b2g")
    cells: list[BuyerCell] = []
    for index, role in enumerate(roles):
        cells.append(BuyerCell(role=role, segment=segments[index % len(segments)]))
    return cells


def _problem_cells(sector: Sector, intel: dict[str, Any], factory: UniversalDiagnosticFactory) -> list[ProblemCell]:
    cells: list[ProblemCell] = []
    workflows = list(intel.get("workflows", []))
    for index, problem in enumerate(intel.get("problems", [])):
        families = factory.compose(sector.value, "sme", "ceo", problem, DiagnosticDepth.D1_RAPID)
        workflow = workflows[index % len(workflows)] if workflows else UNKNOWN
        cells.append(
            ProblemCell(
                problem=problem,
                diagnostic_families=[family.family_id for family in families[:3]],
                automation_candidates=[f"automate::{workflow}"] if workflow != UNKNOWN else [],
            )
        )
    return cells


def maturity_for(sector: Sector, registry: SectorPackRegistry | None = None) -> str:
    registry = registry or SectorPackRegistry()
    pack = registry.get(sector.value)
    return PACK_TO_LADDER.get(pack.maturity, "DISCOVERED")


def _completeness(blueprint: SectorCompanyBlueprint) -> int:
    observed = blueprint.model_dump()
    checkable = [
        "market",
        "icp",
        "buyer_roles",
        "organization_archetypes",
        "problems",
        "signals",
        "procurement",
        "partners",
        "technology",
        "dealix_offers",
        "delivery_proof",
        "next_best_actions",
    ]
    filled = 0
    for key in checkable:
        value = observed.get(key)
        if value not in (None, "", UNKNOWN, [], {}):
            if isinstance(value, dict):
                if any(v not in (None, "", UNKNOWN, [], {}) for v in value.values()):
                    filled += 1
            else:
                filled += 1
    return round(filled / len(checkable) * 100)


def build_blueprint(
    sector: Sector,
    registry: SectorPackRegistry | None = None,
    factory: UniversalDiagnosticFactory | None = None,
) -> SectorCompanyBlueprint:
    registry = registry or SectorPackRegistry()
    factory = factory or UniversalDiagnosticFactory()
    intel = SECTOR_INTEL[sector]
    taxonomy = taxonomy_for(sector)
    pack = registry.get(sector.value)
    problem_cells = _problem_cells(sector, intel, factory)
    ar_name = str(intel.get("ar", UNKNOWN))
    en_name = str(intel.get("en", UNKNOWN))
    problems = list(intel.get("problems", []))
    workflows = list(intel.get("workflows", []))
    procurement = str(intel.get("procurement", "direct"))
    is_b2g = any(marker in procurement.lower() for marker in B2G_PROCUREMENT_MARKERS)
    buyers = _buyer_cells(intel)
    buyer_roles_list = list(intel.get("buyers", []))
    diagnostic_families = [cell.diagnostic_families[0] for cell in problem_cells if cell.diagnostic_families]
    offer_ladder = list(intel.get("offers", []))
    compliance = list(intel.get("compliance", []))
    channels = list(intel.get("channels", []))

    blueprint = SectorCompanyBlueprint(
        sector_id=sector.value,
        market=MarketContext(
            sector_id=sector.value,
            ar_name=ar_name,
            en_name=en_name,
            isic_sections=taxonomy.isic_sections,
            isic_section_names=taxonomy.isic_section_names,
            isic_mapping_status=taxonomy.isic_mapping_status,
            saudi_strategic_overlay=taxonomy.saudi_strategic_overlay,
            saudi_mapping_status=taxonomy.saudi_mapping_status,
            regulator_labels=taxonomy.regulator_labels,
            regulator_validation_status="REQUIRES_OFFICIAL_VERIFICATION",
        ),
        icp=ICPProfile(
            icp_segments=["sme", "enterprise"] + (["b2g"] if is_b2g else []),
            company_sizes=["SME", "mid-market", "enterprise"],
            business_models=[],
            geography=["Saudi Arabia"],
            digital_maturity_levels=["manual", "digitized", "integrated", "AI-ready"],
        ),
        buyer_roles=BuyerRoles(
            major_buyer_types=buyer_roles_list + (["b2g"] if is_b2g else []),
            buyers=buyers,
            economic_buyer_role=buyer_roles_list[0] if buyer_roles_list else "ceo",
            champion_role=buyer_roles_list[1] if len(buyer_roles_list) > 1 else "coo",
            technical_buyer_role=buyer_roles_list[2] if len(buyer_roles_list) > 2 else "cto",
            user_roles=["process_owner", "operator"],
        ),
        organization_archetypes=OrganizationArchetypes(
            archetypes=["government" if is_b2g else "private"],
            typical_sizes=["SME", "mid-market", "enterprise"],
            typical_structures=["functional", "divisional", "matrix"],
        ),
        problems=ProblemsAndWorkflows(
            top_problems=problems,
            problem_cells=problem_cells,
            workflows=workflows,
            value_chains=workflows,
            trigger_events=[],
        ),
        signals=SignalsAndRegulation(
            growth_signals=[],
            regulatory_triggers=[],
            procurement_triggers=["new_RFP_or_tender", "vendor_onboarding", "framework_renewal"],
            cost_triggers=["manual_work", "exception_volume", "rework"],
            risk_triggers=["control_gap", "compliance_change", "data_or_security_concern"],
            regulation=compliance,
            compliance_constraints=compliance,
        ),
        procurement=ProcurementPaths(
            procurement_paths=[procurement] if procurement else [],
            tender_paths=["Etimad"] if is_b2g else [],
            b2b_paths=["direct_purchase", "vendor_onboarding", "RFP"],
            b2g_paths=["Etimad", "vendor_registration", "prime_contractor"] if is_b2g else [],
            partner_paths=["systems_integrator", "sector_specialist", "distributor_referral"],
        ),
        partners=PartnersAndCompetitors(
            partner_types=list(PARTNER_TYPES),
            competitor_types=["legacy_vendors", "local_integrators", "internal_build"],
            substitutes=["manual_processes", "spreadsheets", "generic_erp"],
        ),
        technology=TechnologyReadiness(
            existing_technology=["ERP", "CRM", "document_management"],
            ai_readiness=UNKNOWN,
            data_readiness=UNKNOWN,
            infrastructure_readiness=UNKNOWN,
            systems_typically_used=["ERP", "CRM", "DMS"],
            data_sources=["operational_records", "financial_data", "customer_interactions"],
            integration_surfaces=["API", "database", "file_import"],
        ),
        dealix_offers=DealixCapabilitiesAndOffers(
            free_diagnostic_families=diagnostic_families,
            dealix_capabilities=["diagnostic", "workflow_automation", "proof_builder", "governed_ai"],
            offer_ladder=offer_ladder,
            pilot_options=["free_diagnostic", "qualified_discovery", "customer_specific_pilot"],
        ),
        delivery_proof=DeliveryAndProof(
            delivery_pack=f"delivery_pack::{sector.value}",
            acceptance_criteria=["baseline_recorded", "intervention_defined", "result_measured", "customer_validates"],
            proof_requirements=list(pack.proof_requirements),
            discovery_playbook="discovery",
        ),
        next_best_actions=NextBestActions(
            actions=["run_free_diagnostic", "qualify_problem", "schedule_discovery"],
            seo_topics=[f"{en_name} — {problem.replace('_', ' ')}" for problem in problems],
            content_topics=[f"{ar_name}: {FAMILY_AR.get(cell.diagnostic_families[0], cell.problem) if cell.diagnostic_families else cell.problem}" for cell in problem_cells],
            distribution_channels=channels,
        ),
        maturity_status=maturity_for(sector, registry),
    )
    blueprint.completeness_pct = _completeness(blueprint)
    return blueprint


def build_all_blueprints() -> list[SectorCompanyBlueprint]:
    registry = SectorPackRegistry()
    factory = UniversalDiagnosticFactory()
    return [build_blueprint(sector, registry, factory) for sector in Sector]


def portfolio_index(blueprints: list[SectorCompanyBlueprint] | None = None) -> dict[str, Any]:
    blueprints = blueprints or build_all_blueprints()
    by_status: dict[str, int] = {}
    for blueprint in blueprints:
        by_status[blueprint.maturity_status] = by_status.get(blueprint.maturity_status, 0) + 1
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "sectors_total": len(blueprints),
        "by_maturity": by_status,
        "avg_completeness_pct": round(sum(item.completeness_pct for item in blueprints) / max(1, len(blueprints))),
        "truth_class": "PATTERN",
        "is_customer_fact": False,
        "sectors": [
            {
                "sector_id": item.sector_id,
                "ar_name": item.market.ar_name,
                "en_name": item.market.en_name,
                "isic_sections": item.market.isic_sections,
                "maturity_status": item.maturity_status,
                "completeness_pct": item.completeness_pct,
            }
            for item in blueprints
        ],
    }


__all__ = [
    "MATURITY_LADDER",
    "BuyerCell",
    "ProblemCell",
    "MarketContext",
    "ICPProfile",
    "BuyerRoles",
    "OrganizationArchetypes",
    "ProblemsAndWorkflows",
    "SignalsAndRegulation",
    "ProcurementPaths",
    "PartnersAndCompetitors",
    "TechnologyReadiness",
    "DealixCapabilitiesAndOffers",
    "DeliveryAndProof",
    "NextBestActions",
    "SectorCompanyBlueprint",
    "build_blueprint",
    "build_all_blueprints",
    "portfolio_index",
    "maturity_for",
]
