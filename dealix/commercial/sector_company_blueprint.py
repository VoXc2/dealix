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


class SectorCompanyBlueprint(BaseModel):
    model_config = ConfigDict(extra="forbid")

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
    major_buyer_types: list[str] = Field(default_factory=list)
    buyers: list[BuyerCell] = Field(default_factory=list)
    business_models: list[str] = Field(default_factory=list)
    value_chains: list[str] = Field(default_factory=list)
    top_problems: list[str] = Field(default_factory=list)
    problem_cells: list[ProblemCell] = Field(default_factory=list)
    top_cost_centers: list[str] = Field(default_factory=list)
    top_revenue_levers: list[str] = Field(default_factory=list)
    digital_maturity: str = UNKNOWN
    ai_maturity: str = UNKNOWN
    automation_opportunities: list[str] = Field(default_factory=list)
    data_opportunities: list[str] = Field(default_factory=list)
    compliance_constraints: list[str] = Field(default_factory=list)
    procurement_paths: list[str] = Field(default_factory=list)
    tender_paths: list[str] = Field(default_factory=list)
    partner_types: list[str] = Field(default_factory=list)
    competitor_types: list[str] = Field(default_factory=list)
    trigger_events: list[str] = Field(default_factory=list)
    free_diagnostic: str = UNKNOWN
    discovery_playbook: str = "discovery"
    offer_ladder: list[str] = Field(default_factory=list)
    pilot_options: list[str] = Field(default_factory=list)
    delivery_pack: str = UNKNOWN
    acceptance_criteria: list[str] = Field(default_factory=list)
    proof_requirements: list[str] = Field(default_factory=list)
    seo_topics: list[str] = Field(default_factory=list)
    content_topics: list[str] = Field(default_factory=list)
    distribution_channels: list[str] = Field(default_factory=list)
    economic_score: str = UNKNOWN
    market_score: str = UNKNOWN
    delivery_readiness: str = UNKNOWN
    proof_readiness: str = UNKNOWN
    maturity_status: str = "DISCOVERED"
    completeness_pct: int = 0
    truth_class: str = "PATTERN"
    is_customer_fact: bool = False
    generated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

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
        "ar_name",
        "en_name",
        "isic_sections",
        "saudi_strategic_overlay",
        "regulator_labels",
        "buyers",
        "value_chains",
        "top_problems",
        "problem_cells",
        "automation_opportunities",
        "compliance_constraints",
        "procurement_paths",
        "partner_types",
        "free_diagnostic",
        "offer_ladder",
        "acceptance_criteria",
        "proof_requirements",
        "seo_topics",
        "content_topics",
        "distribution_channels",
    ]
    filled = 0
    for key in checkable:
        value = observed.get(key)
        if value not in (None, "", UNKNOWN, [], {}):
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
    procurement = str(intel.get("procurement", "direct"))
    is_b2g = any(marker in procurement.lower() for marker in B2G_PROCUREMENT_MARKERS)
    blueprint = SectorCompanyBlueprint(
        sector_id=sector.value,
        ar_name=ar_name,
        en_name=en_name,
        isic_sections=taxonomy.isic_sections,
        isic_section_names=taxonomy.isic_section_names,
        isic_mapping_status=taxonomy.isic_mapping_status,
        saudi_strategic_overlay=taxonomy.saudi_strategic_overlay,
        saudi_mapping_status=taxonomy.saudi_mapping_status,
        regulator_labels=taxonomy.regulator_labels,
        major_buyer_types=["buyer_roles"] + (["b2g"] if is_b2g else []),
        buyers=_buyer_cells(intel),
        business_models=[],
        value_chains=list(intel.get("workflows", [])),
        top_problems=problems,
        problem_cells=problem_cells,
        automation_opportunities=[f"automate::{workflow}" for workflow in intel.get("workflows", [])],
        compliance_constraints=list(intel.get("compliance", [])),
        procurement_paths=[procurement] if procurement else [],
        tender_paths=["Etimad"] if is_b2g else [],
        partner_types=list(PARTNER_TYPES),
        trigger_events=[],
        free_diagnostic=f"sector_pack::{sector.value}",
        offer_ladder=list(intel.get("offers", [])),
        pilot_options=["free_diagnostic", "qualified_discovery", "customer_specific_pilot"],
        delivery_pack=f"delivery_pack::{sector.value}",
        acceptance_criteria=["baseline_recorded", "intervention_defined", "result_measured", "customer_validates"],
        proof_requirements=list(pack.proof_requirements),
        seo_topics=[f"{en_name} — {problem.replace('_', ' ')}" for problem in problems],
        content_topics=[f"{ar_name}: {FAMILY_AR.get(cell.diagnostic_families[0], cell.problem) if cell.diagnostic_families else cell.problem}" for cell in problem_cells],
        distribution_channels=list(intel.get("channels", [])),
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
                "ar_name": item.ar_name,
                "en_name": item.en_name,
                "isic_sections": item.isic_sections,
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
    "SectorCompanyBlueprint",
    "build_blueprint",
    "build_all_blueprints",
    "portfolio_index",
    "maturity_for",
]
