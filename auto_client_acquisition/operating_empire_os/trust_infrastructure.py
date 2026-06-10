"""Trust infrastructure tenets and attestation scoring."""

from __future__ import annotations

from dataclasses import dataclass

TRUST_INFRASTRUCTURE_TENETS: tuple[str, ...] = (
    "no_scraping",
    "no_cold_whatsapp",
    "no_linkedin_automation",
    "no_fake_proof",
    "no_guaranteed_sales_claims",
    "no_pii_in_logs",
    "no_sourceless_answers",
    "no_external_action_without_approval",
)


@dataclass(frozen=True, slots=True)
class TrustInfrastructureAttestation:
    no_scraping: bool = False
    no_cold_whatsapp: bool = False
    no_linkedin_automation: bool = False
    no_fake_proof: bool = False
    no_guaranteed_sales_claims: bool = False
    no_pii_in_logs: bool = False
    no_sourceless_answers: bool = False
    no_external_action_without_approval: bool = False


def trust_infrastructure_score(att: TrustInfrastructureAttestation) -> int:
    """100 when all eight attestations are True."""
    fields = TRUST_INFRASTRUCTURE_TENETS
    vals = (
        att.no_scraping,
        att.no_cold_whatsapp,
        att.no_linkedin_automation,
        att.no_fake_proof,
        att.no_guaranteed_sales_claims,
        att.no_pii_in_logs,
        att.no_sourceless_answers,
        att.no_external_action_without_approval,
    )
    if len(fields) != len(vals):
        raise RuntimeError("trust tenets out of sync")
    passed = sum(1 for v in vals if v)
    return (passed * 100) // len(vals)
