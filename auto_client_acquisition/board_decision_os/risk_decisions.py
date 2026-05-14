"""Board-level risk codes → mitigation decision slugs."""

from __future__ import annotations

RISK_REGISTER_CODES: tuple[str, ...] = (
    "R1_agency_trap",
    "R2_premature_saas",
    "R3_governance_incident",
    "R4_weak_proof",
    "R5_founder_bottleneck",
    "R6_partner_brand_damage",
    "R7_model_provider_dependency",
    "R8_agent_over_permission",
    "R9_bad_revenue",
    "R10_saudi_trust_gap",
)

_RISK_TO_DECISION: dict[str, str] = {
    "R1_agency_trap": "enforce_productization_ledger",
    "R2_premature_saas": "require_platform_pull_signals",
    "R3_governance_incident": "freeze_external_actions_until_rule_test",
    "R4_weak_proof": "block_case_study_and_retainer_push",
    "R5_founder_bottleneck": "delivery_playbook_before_hiring",
    "R6_partner_brand_damage": "partner_qa_and_escalation_path",
    "R7_model_provider_dependency": "multi_provider_abstraction_or_budget",
    "R8_agent_over_permission": "reduce_tools_and_autonomy_level",
    "R9_bad_revenue": "reject_or_convert_to_paid_diagnostic",
    "R10_saudi_trust_gap": "arabic_governance_and_proof_pack_push",
}


def risk_register_code_valid(code: str) -> bool:
    return code in RISK_REGISTER_CODES


def risk_to_mitigation_decision(risk_code: str) -> str | None:
    return _RISK_TO_DECISION.get(risk_code)
