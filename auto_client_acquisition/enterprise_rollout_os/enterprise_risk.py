"""Enterprise rollout risk register — R1–R10 with control levers."""

from __future__ import annotations

ENTERPRISE_ROLLOUT_RISK_IDS: tuple[str, ...] = (
    "R1_no_executive_sponsor",
    "R2_data_owner_unclear",
    "R3_governance_rejects_use_case",
    "R4_users_do_not_adopt_output",
    "R5_approval_process_too_slow",
    "R6_proof_weak",
    "R7_client_asks_prohibited_automation",
    "R8_it_security_blocks_access",
    "R9_stakeholders_expect_guaranteed_outcomes",
    "R10_agent_permissions_too_broad",
)

ENTERPRISE_ROLLOUT_CONTROLS: tuple[str, ...] = (
    "sponsor_gate",
    "source_passport",
    "governance_boundary",
    "adoption_review",
    "approval_matrix",
    "proof_score",
    "no_unsafe_automation_policy",
    "security_brief",
    "expectation_setting",
    "agent_card",
)
