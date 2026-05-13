"""Dealix Non-Negotiables — frozen list + action check.

See ``docs/operating_manual/DEALIX_NON_NEGOTIABLES.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class NonNegotiable(str, Enum):
    NO_SCRAPING = "no_scraping_systems"
    NO_COLD_WHATSAPP = "no_cold_whatsapp_automation"
    NO_LINKEDIN_AUTOMATION = "no_linkedin_automation"
    NO_FAKE_PROOF = "no_fake_proof"
    NO_GUARANTEED_SALES_CLAIMS = "no_guaranteed_sales_claims"
    NO_PII_IN_LOGS = "no_pii_in_logs"
    NO_SOURCELESS_KNOWLEDGE_ANSWERS = "no_sourceless_knowledge_answers"
    NO_EXTERNAL_ACTION_WITHOUT_APPROVAL = "no_external_action_without_approval"
    NO_AI_OUTPUT_WITHOUT_GOVERNANCE_STATUS = "no_ai_output_without_governance_status"
    NO_PROJECT_CLOSE_WITHOUT_PROOF_PACK = "no_project_close_without_proof_pack"
    NO_PROJECT_WITHOUT_CAPITAL_ASSET = "no_project_without_capital_asset"


DEALIX_NON_NEGOTIABLES: tuple[NonNegotiable, ...] = tuple(NonNegotiable)


@dataclass(frozen=True)
class NonNegotiableCheck:
    """Describes a proposed action against the non-negotiables list."""

    action: str
    uses_scraping: bool = False
    uses_cold_whatsapp: bool = False
    uses_linkedin_automation: bool = False
    claims_unverified_proof: bool = False
    claims_guaranteed_sales: bool = False
    writes_pii_to_logs: bool = False
    answers_without_sources: bool = False
    performs_external_action_without_approval: bool = False
    emits_ai_output_without_governance: bool = False
    closes_project_without_proof_pack: bool = False
    closes_project_without_capital_asset: bool = False


@dataclass(frozen=True)
class NonNegotiableResult:
    allowed: bool
    violations: tuple[NonNegotiable, ...]


def check_action_against_non_negotiables(
    check: NonNegotiableCheck,
) -> NonNegotiableResult:
    violations: list[NonNegotiable] = []

    if check.uses_scraping:
        violations.append(NonNegotiable.NO_SCRAPING)
    if check.uses_cold_whatsapp:
        violations.append(NonNegotiable.NO_COLD_WHATSAPP)
    if check.uses_linkedin_automation:
        violations.append(NonNegotiable.NO_LINKEDIN_AUTOMATION)
    if check.claims_unverified_proof:
        violations.append(NonNegotiable.NO_FAKE_PROOF)
    if check.claims_guaranteed_sales:
        violations.append(NonNegotiable.NO_GUARANTEED_SALES_CLAIMS)
    if check.writes_pii_to_logs:
        violations.append(NonNegotiable.NO_PII_IN_LOGS)
    if check.answers_without_sources:
        violations.append(NonNegotiable.NO_SOURCELESS_KNOWLEDGE_ANSWERS)
    if check.performs_external_action_without_approval:
        violations.append(NonNegotiable.NO_EXTERNAL_ACTION_WITHOUT_APPROVAL)
    if check.emits_ai_output_without_governance:
        violations.append(NonNegotiable.NO_AI_OUTPUT_WITHOUT_GOVERNANCE_STATUS)
    if check.closes_project_without_proof_pack:
        violations.append(NonNegotiable.NO_PROJECT_CLOSE_WITHOUT_PROOF_PACK)
    if check.closes_project_without_capital_asset:
        violations.append(NonNegotiable.NO_PROJECT_WITHOUT_CAPITAL_ASSET)

    return NonNegotiableResult(
        allowed=not violations,
        violations=tuple(violations),
    )
