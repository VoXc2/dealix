"""Partner risk — covenant violations and suspension heuristics."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PartnerCovenantSignals:
    scraping_systems: bool
    cold_whatsapp_automation: bool
    linkedin_automation: bool
    fake_proof: bool
    guaranteed_outcome_claims: bool
    client_output_without_qa: bool
    external_action_without_approval: bool


def partner_should_suspend(signals: PartnerCovenantSignals) -> bool:
    return any(
        (
            signals.scraping_systems,
            signals.cold_whatsapp_automation,
            signals.linkedin_automation,
            signals.fake_proof,
            signals.guaranteed_outcome_claims,
            signals.client_output_without_qa,
            signals.external_action_without_approval,
        ),
    )


def partner_referral_only_weak_qa(*, qa_score_below_threshold: bool, no_suspension_triggers: bool) -> bool:
    return qa_score_below_threshold and no_suspension_triggers
