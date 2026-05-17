"""Governed Revenue + AI Ops factory policy.

This module encodes the operating doctrine as deterministic policy decisions:

Signal → Source → Approval → Action → Evidence → Decision → Value → Asset

Rules:
- Level 1 actions are internal automation and can run automatically.
- Level 2 actions are recommendations; agents assist and founder chooses.
- Level 3 actions are high-impact and require founder approval.
- Missing required evidence blocks execution (no drift, no invented state).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class AutomationLevel(StrEnum):
    LEVEL_1_FULLY_AUTOMATED = "level_1_fully_automated"
    LEVEL_2_AGENT_ASSISTED = "level_2_agent_assisted"
    LEVEL_3_FOUNDER_APPROVAL = "level_3_founder_approval"


class PolicyRisk(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DecisionStatus(StrEnum):
    ALLOW = "allow"
    NEEDS_FOUNDER_APPROVAL = "needs_founder_approval"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class GovernedActionPolicy:
    action_key: str
    level: AutomationLevel
    risk: PolicyRisk
    required_evidence: tuple[str, ...] = ()
    notes: str = ""


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    action_key: str
    status: DecisionStatus
    reason: str
    level: AutomationLevel | None
    risk: PolicyRisk | None
    missing_evidence: tuple[str, ...] = ()


ACTION_POLICY: dict[str, GovernedActionPolicy] = {
    # Level 1 — fully automated (internal)
    "lead_capture": GovernedActionPolicy(
        action_key="lead_capture",
        level=AutomationLevel.LEVEL_1_FULLY_AUTOMATED,
        risk=PolicyRisk.LOW,
        notes="Capture inbound lead into system of record.",
    ),
    "crm_create": GovernedActionPolicy(
        action_key="crm_create",
        level=AutomationLevel.LEVEL_1_FULLY_AUTOMATED,
        risk=PolicyRisk.LOW,
    ),
    "lead_scoring": GovernedActionPolicy(
        action_key="lead_scoring",
        level=AutomationLevel.LEVEL_1_FULLY_AUTOMATED,
        risk=PolicyRisk.LOW,
    ),
    "meeting_brief_draft": GovernedActionPolicy(
        action_key="meeting_brief_draft",
        level=AutomationLevel.LEVEL_1_FULLY_AUTOMATED,
        risk=PolicyRisk.LOW,
    ),
    "scope_draft": GovernedActionPolicy(
        action_key="scope_draft",
        level=AutomationLevel.LEVEL_1_FULLY_AUTOMATED,
        risk=PolicyRisk.MEDIUM,
        required_evidence=("scope_requested",),
    ),
    "invoice_draft": GovernedActionPolicy(
        action_key="invoice_draft",
        level=AutomationLevel.LEVEL_1_FULLY_AUTOMATED,
        risk=PolicyRisk.MEDIUM,
        required_evidence=("scope_approved",),
    ),
    "proof_pack_skeleton": GovernedActionPolicy(
        action_key="proof_pack_skeleton",
        level=AutomationLevel.LEVEL_1_FULLY_AUTOMATED,
        risk=PolicyRisk.MEDIUM,
    ),
    "delivery_checklist": GovernedActionPolicy(
        action_key="delivery_checklist",
        level=AutomationLevel.LEVEL_1_FULLY_AUTOMATED,
        risk=PolicyRisk.MEDIUM,
        required_evidence=("invoice_paid",),
    ),
    "weekly_report": GovernedActionPolicy(
        action_key="weekly_report",
        level=AutomationLevel.LEVEL_1_FULLY_AUTOMATED,
        risk=PolicyRisk.LOW,
    ),
    "evidence_logging": GovernedActionPolicy(
        action_key="evidence_logging",
        level=AutomationLevel.LEVEL_1_FULLY_AUTOMATED,
        risk=PolicyRisk.LOW,
    ),
    # Level 2 — agent-assisted recommendations
    "icp_recommendation": GovernedActionPolicy(
        action_key="icp_recommendation",
        level=AutomationLevel.LEVEL_2_AGENT_ASSISTED,
        risk=PolicyRisk.LOW,
    ),
    "message_angle_recommendation": GovernedActionPolicy(
        action_key="message_angle_recommendation",
        level=AutomationLevel.LEVEL_2_AGENT_ASSISTED,
        risk=PolicyRisk.MEDIUM,
    ),
    "pricing_recommendation": GovernedActionPolicy(
        action_key="pricing_recommendation",
        level=AutomationLevel.LEVEL_2_AGENT_ASSISTED,
        risk=PolicyRisk.MEDIUM,
    ),
    "next_action_recommendation": GovernedActionPolicy(
        action_key="next_action_recommendation",
        level=AutomationLevel.LEVEL_2_AGENT_ASSISTED,
        risk=PolicyRisk.LOW,
    ),
    "upsell_recommendation": GovernedActionPolicy(
        action_key="upsell_recommendation",
        level=AutomationLevel.LEVEL_2_AGENT_ASSISTED,
        risk=PolicyRisk.MEDIUM,
    ),
    "partner_recommendation": GovernedActionPolicy(
        action_key="partner_recommendation",
        level=AutomationLevel.LEVEL_2_AGENT_ASSISTED,
        risk=PolicyRisk.MEDIUM,
    ),
    # Level 3 — founder approval required
    "external_message_send": GovernedActionPolicy(
        action_key="external_message_send",
        level=AutomationLevel.LEVEL_3_FOUNDER_APPROVAL,
        risk=PolicyRisk.HIGH,
        required_evidence=("message_draft_prepared",),
    ),
    "scope_send": GovernedActionPolicy(
        action_key="scope_send",
        level=AutomationLevel.LEVEL_3_FOUNDER_APPROVAL,
        risk=PolicyRisk.HIGH,
        required_evidence=("scope_requested",),
    ),
    "invoice_send": GovernedActionPolicy(
        action_key="invoice_send",
        level=AutomationLevel.LEVEL_3_FOUNDER_APPROVAL,
        risk=PolicyRisk.HIGH,
        required_evidence=("scope_approved",),
    ),
    "diagnostic_finalization": GovernedActionPolicy(
        action_key="diagnostic_finalization",
        level=AutomationLevel.LEVEL_3_FOUNDER_APPROVAL,
        risk=PolicyRisk.HIGH,
        required_evidence=("diagnostic_draft_ready",),
    ),
    "case_study_publish": GovernedActionPolicy(
        action_key="case_study_publish",
        level=AutomationLevel.LEVEL_3_FOUNDER_APPROVAL,
        risk=PolicyRisk.HIGH,
        required_evidence=("case_study_client_approval",),
    ),
    "security_claim_publish": GovernedActionPolicy(
        action_key="security_claim_publish",
        level=AutomationLevel.LEVEL_3_FOUNDER_APPROVAL,
        risk=PolicyRisk.CRITICAL,
        required_evidence=("security_claim_source",),
    ),
    "agent_tool_action_high_impact": GovernedActionPolicy(
        action_key="agent_tool_action_high_impact",
        level=AutomationLevel.LEVEL_3_FOUNDER_APPROVAL,
        risk=PolicyRisk.CRITICAL,
        required_evidence=("risk_assessment_completed",),
    ),
    "delivery_start": GovernedActionPolicy(
        action_key="delivery_start",
        level=AutomationLevel.LEVEL_3_FOUNDER_APPROVAL,
        risk=PolicyRisk.HIGH,
        required_evidence=("invoice_paid",),
    ),
    "revenue_recognized": GovernedActionPolicy(
        action_key="revenue_recognized",
        level=AutomationLevel.LEVEL_3_FOUNDER_APPROVAL,
        risk=PolicyRisk.HIGH,
        required_evidence=("payment_proof",),
    ),
}


def evaluate_governed_action(
    *,
    action_key: str,
    evidence_events: set[str] | None = None,
    founder_approved: bool = False,
) -> PolicyDecision:
    """Evaluate one action request under the governed revenue doctrine."""
    policy = ACTION_POLICY.get(action_key)
    if policy is None:
        return PolicyDecision(
            action_key=action_key,
            status=DecisionStatus.BLOCKED,
            reason="unknown_action_drift",
            level=None,
            risk=None,
        )

    evidence = evidence_events or set()
    missing = tuple(ev for ev in policy.required_evidence if ev not in evidence)
    if missing:
        return PolicyDecision(
            action_key=action_key,
            status=DecisionStatus.BLOCKED,
            reason="missing_required_evidence",
            level=policy.level,
            risk=policy.risk,
            missing_evidence=missing,
        )

    if (
        policy.level == AutomationLevel.LEVEL_3_FOUNDER_APPROVAL
        and not founder_approved
    ):
        return PolicyDecision(
            action_key=action_key,
            status=DecisionStatus.NEEDS_FOUNDER_APPROVAL,
            reason="founder_approval_required",
            level=policy.level,
            risk=policy.risk,
        )

    return PolicyDecision(
        action_key=action_key,
        status=DecisionStatus.ALLOW,
        reason="policy_allow",
        level=policy.level,
        risk=policy.risk,
    )


def founder_approval_action_keys() -> set[str]:
    """Return all action keys that must always pass founder approval."""
    return {
        action_key
        for action_key, policy in ACTION_POLICY.items()
        if policy.level == AutomationLevel.LEVEL_3_FOUNDER_APPROVAL
    }

