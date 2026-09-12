"""Dynamic Offer Input Contract — deterministic, evidence-backed offer construction.

Commercial Reset is authoritative: ALL diagnostics are FREE, NO card required.
Historical public fixed prices are NOT pricing authority.

Commercial truth path:
Market Signal → Evidence → Real Interaction → Qualified Problem
→ Free Diagnostic → Discovery → Customer-Specific Solution
→ Customer-Specific Quote → Pilot Decision → Invoice
→ Verified Payment → Delivery → Customer-Validated Proof
→ Expansion / Referral / Productization

This module reconciles a deterministic offer input contract.
Unknown information must remain explicit (UNKNOWN).
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.economic_cell import (
    BuyerGroup,
    DistributionRail,
    EvidenceLevel,
    MonetizationRail,
    ProcurementRail,
    ProblemClass,
    Sector,
    UNKNOWN,
)

FREE = "FREE"


class OfferInputTruthClass(StrEnum):
    """Truth classification for offer input fields."""
    PATTERN = "PATTERN"           # Sector-level pattern knowledge
    OBSERVED = "OBSERVED"         # Public source / market signal
    DIRECT_INTERACTION = "DIRECT_INTERACTION"  # Real customer interaction
    CUSTOMER_VERIFIED = "CUSTOMER_VERIFIED"    # Customer confirmed
    UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"


class DynamicOfferInput(BaseModel):
    """
    Deterministic offer input contract.

    Every field is either evidence-backed or explicitly UNKNOWN.
    No invented customer facts. No fixed public pricing authority.
    """
    model_config = ConfigDict(extra="forbid")

    # Required context
    sector: Sector
    company: str = UNKNOWN  # Company name or UNKNOWN
    buyer: BuyerGroup = BuyerGroup.CEO
    verified_problem: ProblemClass = ProblemClass.REVENUE_LEAKAGE

    # Evidence-backed context
    workflow: str = UNKNOWN
    evidence: list[str] = Field(default_factory=list)  # Evidence refs
    urgency: str = UNKNOWN
    current_systems: list[str] = Field(default_factory=list)
    available_data: list[str] = Field(default_factory=list)
    regulatory_constraints: list[str] = Field(default_factory=list)
    integration_constraints: list[str] = Field(default_factory=list)

    # Feasibility & proof
    delivery_feasibility: str = UNKNOWN
    acceptance_criteria: list[str] = Field(default_factory=list)
    proof_potential: str = UNKNOWN

    # Commercial
    commercial_risk: list[str] = Field(default_factory=list)

    # Truth tracking
    truth_class: OfferInputTruthClass = OfferInputTruthClass.PATTERN
    is_customer_fact: bool = False
    generated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


class OfferConstructionResult(BaseModel):
    """Result of constructing an offer from dynamic inputs."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    offer_id: str
    offer_name: str
    basis: list[str]
    truth_class: OfferInputTruthClass
    requires_customer_specific_scope: bool = True
    diagnostic_price: str = FREE
    monetization_rail: MonetizationRail = MonetizationRail.FREE_DIAGNOSTIC
    distribution_rail: DistributionRail = DistributionRail.WEBSITE_INBOUND
    procurement_rail: ProcurementRail = ProcurementRail.DIRECT_PURCHASE
    known_inputs: list[str] = Field(default_factory=list)
    unknown_inputs: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    generated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


# Canonical offer families (from sector_commercial_factory)
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


def construct_offer_from_input(inp: DynamicOfferInput) -> OfferConstructionResult:
    """
    Construct a deterministic offer from dynamic inputs.

    Rules:
    - Only canonical offers
    - All diagnostics FREE
    - Unknown stays UNKNOWN
    - No fixed public pricing authority restored
    - Evidence required for customer-specific offers
    """
    known = []
    unknown = []
    warnings = []
    basis = []

    # Validate sector
    if inp.sector:
        basis.append(f"sector::{inp.sector.value}")
        known.append("sector")
    else:
        unknown.append("sector")
        warnings.append("sector is required")

    # Company
    if inp.company != UNKNOWN:
        basis.append(f"company::{inp.company}")
        known.append("company")
    else:
        unknown.append("company")
        warnings.append("company unknown — offer will be sector-pattern only")

    # Buyer
    if inp.buyer != BuyerGroup.CEO or inp.company != UNKNOWN:
        basis.append(f"buyer::{inp.buyer.value}")
        known.append("buyer")
    else:
        unknown.append("buyer")

    # Verified problem
    if inp.verified_problem != ProblemClass.REVENUE_LEAKAGE or inp.company != UNKNOWN:
        basis.append(f"problem::{inp.verified_problem.value}")
        known.append("verified_problem")
    else:
        unknown.append("verified_problem")
        warnings.append("problem not customer-verified — pattern only")

    # Workflow
    if inp.workflow != UNKNOWN:
        basis.append(f"workflow::{inp.workflow}")
        known.append("workflow")
    else:
        unknown.append("workflow")

    # Evidence
    if inp.evidence:
        basis.extend(f"evidence::{ref}" for ref in inp.evidence[:3])
        known.append("evidence")
    else:
        unknown.append("evidence")
        warnings.append("no evidence refs — offer basis is pattern only")

    # Urgency
    if inp.urgency != UNKNOWN:
        basis.append(f"urgency::{inp.urgency}")
        known.append("urgency")
    else:
        unknown.append("urgency")

    # Current systems
    if inp.current_systems:
        basis.append(f"systems::{','.join(inp.current_systems[:3])}")
        known.append("current_systems")
    else:
        unknown.append("current_systems")

    # Available data
    if inp.available_data:
        known.append("available_data")
    else:
        unknown.append("available_data")

    # Regulatory constraints
    if inp.regulatory_constraints:
        basis.append(f"regulatory::{','.join(inp.regulatory_constraints[:3])}")
        known.append("regulatory_constraints")
    else:
        unknown.append("regulatory_constraints")

    # Integration constraints
    if inp.integration_constraints:
        known.append("integration_constraints")
    else:
        unknown.append("integration_constraints")

    # Delivery feasibility
    if inp.delivery_feasibility != UNKNOWN:
        known.append("delivery_feasibility")
    else:
        unknown.append("delivery_feasibility")

    # Acceptance criteria
    if inp.acceptance_criteria:
        basis.append(f"acceptance::{','.join(inp.acceptance_criteria[:3])}")
        known.append("acceptance_criteria")
    else:
        unknown.append("acceptance_criteria")
        warnings.append("no acceptance criteria defined — cannot measure delivery success")

    # Proof potential
    if inp.proof_potential != UNKNOWN:
        known.append("proof_potential")
    else:
        unknown.append("proof_potential")

    # Commercial risk
    if inp.commercial_risk:
        basis.append(f"risk::{','.join(inp.commercial_risk[:3])}")
        known.append("commercial_risk")
    else:
        unknown.append("commercial_risk")

    # Determine offer match from canonical offers
    offer_name = _match_canonical_offer(inp)
    offer_id = f"offer_{inp.sector.value}_{inp.verified_problem.value}_{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}"

    # Determine truth class
    if inp.truth_class == OfferInputTruthClass.CUSTOMER_VERIFIED and inp.evidence:
        result_truth = OfferInputTruthClass.CUSTOMER_VERIFIED
    elif inp.truth_class == OfferInputTruthClass.DIRECT_INTERACTION and inp.evidence:
        result_truth = OfferInputTruthClass.DIRECT_INTERACTION
    elif inp.evidence:
        result_truth = OfferInputTruthClass.OBSERVED
    else:
        result_truth = OfferInputTruthClass.PATTERN

    # Requires customer-specific scope unless fully verified
    requires_specific = result_truth != OfferInputTruthClass.CUSTOMER_VERIFIED

    return OfferConstructionResult(
        offer_id=offer_id,
        offer_name=offer_name,
        basis=sorted(set(basis)),
        truth_class=result_truth,
        requires_customer_specific_scope=requires_specific,
        diagnostic_price=FREE,
        monetization_rail=_determine_monetization(inp, result_truth),
        distribution_rail=_determine_distribution(inp),
        procurement_rail=_determine_procurement(inp),
        known_inputs=sorted(set(known)),
        unknown_inputs=sorted(set(unknown)),
        warnings=warnings,
    )


def _match_canonical_offer(inp: DynamicOfferInput) -> str:
    """Match input to best canonical offer."""
    # Sector-specific mappings
    sector_offers = {
        Sector.GOVERNMENT_B2G: ["B2G Readiness Sprint", "Saudi Opportunity Snapshot"],
        Sector.EXPORT_IMPORT_RHQ: ["Saudi Market Access Sprint", "Partner / Distributor Desk", "Saudi Opportunity Snapshot"],
        Sector.CREATIVE_SPORTS_GAMING: ["Revenue Command Pilot", "Partner / Distributor Desk"],
        Sector.PROFESSIONAL_SERVICES: ["Revenue Command Pilot", "Revenue Command Room"],
        Sector.TECHNOLOGY_SAAS_SI: ["Revenue Command Room", "AI Company OS Setup"],
        Sector.RETAIL_COMMERCE_ECOMMERCE: ["Revenue Command Pilot", "AI Company OS Setup"],
        Sector.TOURISM_HOSPITALITY: ["Revenue Command Pilot", "AI Company OS Setup"],
        Sector.TELECOM_MEDIA_MARKETING: ["Revenue Command Pilot", "AI Company OS Setup"],
    }

    offers = sector_offers.get(inp.sector, ["AI Company OS Setup", "Revenue Proof Sprint"])

    # Problem-specific refinements
    if inp.verified_problem in {ProblemClass.COMPLIANCE_BURDEN, ProblemClass.PROCUREMENT_DELAY}:
        if "B2G Readiness Sprint" in offers:
            return "B2G Readiness Sprint"
    if inp.verified_problem in {ProblemClass.MARKET_ENTRY_FRICTION}:
        if "Saudi Market Access Sprint" in offers:
            return "Saudi Market Access Sprint"
    if inp.verified_problem in {ProblemClass.REVENUE_LEAKAGE, ProblemClass.QUOTE_DELAY, ProblemClass.COLLECTION_DELAY}:
        if "Revenue Command Pilot" in offers:
            return "Revenue Command Pilot"
    if inp.verified_problem in {ProblemClass.AI_GOVERNANCE_RISK, ProblemClass.KNOWLEDGE_LOSS}:
        if "AI Company OS Setup" in offers:
            return "AI Company OS Setup"

    return offers[0]


def _determine_monetization(inp: DynamicOfferInput, truth: OfferInputTruthClass) -> MonetizationRail:
    """Determine monetization rail based on evidence and offer type."""
    # All diagnostics are FREE
    if truth in {OfferInputTruthClass.PATTERN, OfferInputTruthClass.OBSERVED}:
        return MonetizationRail.FREE_DIAGNOSTIC

    # Customer-verified problems can progress to paid sprints/pilots
    if truth == OfferInputTruthClass.CUSTOMER_VERIFIED:
        if inp.verified_problem in {ProblemClass.REVENUE_LEAKAGE, ProblemClass.QUOTE_DELAY, ProblemClass.COLLECTION_DELAY}:
            return MonetizationRail.CUSTOMER_PILOT
        if inp.verified_problem in {ProblemClass.AI_GOVERNANCE_RISK, ProblemClass.KNOWLEDGE_LOSS}:
            return MonetizationRail.PAID_SPRINT
        if inp.verified_problem == ProblemClass.MARKET_ENTRY_FRICTION:
            return MonetizationRail.PAID_SPRINT

    return MonetizationRail.FREE_DIAGNOSTIC


def _determine_distribution(inp: DynamicOfferInput) -> DistributionRail:
    """Determine distribution rail based on sector and buyer."""
    if inp.sector == Sector.GOVERNMENT_B2G:
        return DistributionRail.ETIMAD_INTELLIGENCE
    if inp.sector == Sector.EXPORT_IMPORT_RHQ:
        return DistributionRail.MISA_INVEST_SAUDI
    if inp.buyer in {BuyerGroup.CEO, BuyerGroup.FOUNDER_OWNER}:
        return DistributionRail.WARM_INTROS
    return DistributionRail.WEBSITE_INBOUND


def _determine_procurement(inp: DynamicOfferInput) -> ProcurementRail:
    """Determine procurement rail based on sector."""
    if inp.sector == Sector.GOVERNMENT_B2G:
        return ProcurementRail.TENDER
    if inp.sector == Sector.EXPORT_IMPORT_RHQ:
        return ProcurementRail.GOVERNMENT_PROCUREMENT
    if inp.company != UNKNOWN and inp.evidence:
        return ProcurementRail.DIRECT_PURCHASE
    return ProcurementRail.DIRECT_PURCHASE


def validate_offer_input(inp: DynamicOfferInput) -> dict[str, Any]:
    """Validate offer input and return validation report."""
    result = construct_offer_from_input(inp)

    return {
        "valid": len(result.warnings) == 0,
        "offer_id": result.offer_id,
        "offer_name": result.offer_name,
        "truth_class": result.truth_class.value,
        "diagnostic_free": result.diagnostic_price == FREE,
        "requires_customer_specific_scope": result.requires_customer_specific_scope,
        "known_inputs": result.known_inputs,
        "unknown_inputs": result.unknown_inputs,
        "warnings": result.warnings,
        "monetization_rail": result.monetization_rail.value,
        "distribution_rail": result.distribution_rail.value,
        "procurement_rail": result.procurement_rail.value,
        "basis": result.basis,
    }


__all__ = [
    "FREE",
    "OfferInputTruthClass",
    "DynamicOfferInput",
    "OfferConstructionResult",
    "CANONICAL_OFFERS",
    "construct_offer_from_input",
    "validate_offer_input",
]