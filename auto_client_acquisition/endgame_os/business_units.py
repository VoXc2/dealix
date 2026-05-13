"""Dealix Business Units — definitions and the promotion gate.

See ``docs/endgame/BUSINESS_UNITS.md``.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BusinessUnit:
    code: str
    name: str
    primary_offer: str
    recurring_offer: str
    product_module: str
    proof_type: str
    kpis: tuple[str, ...]


BUSINESS_UNITS: tuple[BusinessUnit, ...] = (
    BusinessUnit(
        code="REVENUE",
        name="Dealix Revenue",
        primary_offer="Revenue Intelligence Sprint",
        recurring_offer="Monthly RevOps OS",
        product_module="revenue_os",
        proof_type="Revenue Proof Pack",
        kpis=(
            "accounts_scored",
            "pipeline_value",
            "draft_packs_approved",
            "retainer_conversion",
        ),
    ),
    BusinessUnit(
        code="BRAIN",
        name="Dealix Brain",
        primary_offer="Company Brain Sprint",
        recurring_offer="Monthly Company Brain",
        product_module="brain_os",
        proof_type="Knowledge Proof Pack",
        kpis=(
            "docs_indexed",
            "citation_coverage",
            "insufficient_evidence_rate",
            "knowledge_gaps_closed",
        ),
    ),
    BusinessUnit(
        code="GOVERNANCE",
        name="Dealix Governance",
        primary_offer="AI Governance Review",
        recurring_offer="Monthly Governance",
        product_module="governance_os",
        proof_type="Risk Proof Pack",
        kpis=(
            "rules_created",
            "risky_actions_blocked",
            "approvals_logged",
            "audit_coverage",
        ),
    ),
    BusinessUnit(
        code="OPERATIONS",
        name="Dealix Operations",
        primary_offer="AI Quick Win Sprint",
        recurring_offer="Monthly AI Ops",
        product_module="operations_os",
        proof_type="Time/Quality Proof Pack",
        kpis=(
            "hours_saved",
            "workflows_created",
            "approvals_completed",
            "error_reduction",
        ),
    ),
)


@dataclass(frozen=True)
class BusinessUnitPromotionGate:
    """The objective gate that promotes a capability into a Business Unit."""

    paid_engagements: int
    active_retainers: int
    qa_pass_rate: float          # 0..1
    has_product_module: bool
    healthy_margin: bool
    named_owner: bool
    proof_assets: int

    MIN_PAID_ENGAGEMENTS = 5
    MIN_ACTIVE_RETAINERS = 2
    MIN_QA_PASS_RATE = 0.80
    MIN_PROOF_ASSETS = 3


@dataclass(frozen=True)
class PromotionEvaluation:
    passes: bool
    failed_checks: tuple[str, ...]


def evaluate_promotion(gate: BusinessUnitPromotionGate) -> PromotionEvaluation:
    failures: list[str] = []
    if gate.paid_engagements < gate.MIN_PAID_ENGAGEMENTS:
        failures.append("paid_engagements_below_threshold")
    if gate.active_retainers < gate.MIN_ACTIVE_RETAINERS:
        failures.append("active_retainers_below_threshold")
    if gate.qa_pass_rate < gate.MIN_QA_PASS_RATE:
        failures.append("qa_pass_rate_below_threshold")
    if not gate.has_product_module:
        failures.append("missing_product_module")
    if not gate.healthy_margin:
        failures.append("unhealthy_margin")
    if not gate.named_owner:
        failures.append("missing_named_owner")
    if gate.proof_assets < gate.MIN_PROOF_ASSETS:
        failures.append("proof_assets_below_threshold")
    return PromotionEvaluation(passes=not failures, failed_checks=tuple(failures))
