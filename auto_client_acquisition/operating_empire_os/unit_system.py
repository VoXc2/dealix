"""Dealix business unit profiles (empire layer registry)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class DealixBusinessUnit(StrEnum):
    REVENUE = "dealix_revenue"
    BRAIN = "dealix_brain"
    GOVERNANCE = "dealix_governance"
    OPERATIONS = "dealix_operations"


@dataclass(frozen=True, slots=True)
class UnitSystemProfile:
    unit: DealixBusinessUnit
    primary_offer: str
    recurring_offer: str
    product_module: str
    proof_type: str
    kpi_keys: tuple[str, ...]


UNIT_REGISTRY: dict[DealixBusinessUnit, UnitSystemProfile] = {
    DealixBusinessUnit.REVENUE: UnitSystemProfile(
        unit=DealixBusinessUnit.REVENUE,
        primary_offer="Revenue Intelligence Sprint",
        recurring_offer="Monthly RevOps OS",
        product_module="Revenue OS",
        proof_type="Revenue Proof Pack",
        kpi_keys=(
            "accounts_scored",
            "pipeline_value",
            "draft_packs_approved",
            "retainer_conversion",
        ),
    ),
    DealixBusinessUnit.BRAIN: UnitSystemProfile(
        unit=DealixBusinessUnit.BRAIN,
        primary_offer="Company Brain Sprint",
        recurring_offer="Monthly Company Brain",
        product_module="Knowledge OS",
        proof_type="Knowledge Proof Pack",
        kpi_keys=(
            "docs_indexed",
            "citation_rate",
            "insufficient_evidence_rate",
            "knowledge_gaps_closed",
        ),
    ),
    DealixBusinessUnit.GOVERNANCE: UnitSystemProfile(
        unit=DealixBusinessUnit.GOVERNANCE,
        primary_offer="AI Governance Review",
        recurring_offer="Monthly Governance",
        product_module="Governance Runtime",
        proof_type="Risk Proof Pack",
        kpi_keys=(
            "rules_created",
            "risky_actions_blocked",
            "approvals_logged",
            "audit_coverage",
        ),
    ),
    DealixBusinessUnit.OPERATIONS: UnitSystemProfile(
        unit=DealixBusinessUnit.OPERATIONS,
        primary_offer="AI Quick Win Sprint",
        recurring_offer="Monthly AI Ops",
        product_module="Workflow OS",
        proof_type="Time/Quality Proof Pack",
        kpi_keys=(
            "hours_saved",
            "workflows_created",
            "approvals_completed",
            "error_reduction",
        ),
    ),
}


def get_unit_profile(unit: DealixBusinessUnit) -> UnitSystemProfile:
    return UNIT_REGISTRY[unit]
