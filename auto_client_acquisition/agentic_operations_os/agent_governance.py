"""Agent governance runtime — pre-action governance envelope (MVP-safe)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AgentGovernanceDecision:
    agent_id: str
    proposed_action: str
    decision: str
    risk_level: str
    matched_rules: tuple[str, ...]
    allowed_next_step: str


def governance_decision_for_proposed_action(
    *,
    agent_id: str,
    proposed_action: str,
    contains_pii: bool,
    external_channel: bool,
) -> AgentGovernanceDecision:
    rules: list[str] = []
    if contains_pii:
        rules.append("pii_requires_review")
    if external_channel or "whatsapp" in proposed_action.lower() or "email" in proposed_action.lower():
        rules.append("external_action_requires_approval")
    if "whatsapp" in proposed_action.lower():
        rules.append("no_cold_whatsapp_automation")
    decision = "DRAFT_ONLY"
    risk = "medium" if rules else "low"
    return AgentGovernanceDecision(
        agent_id=agent_id,
        proposed_action=proposed_action,
        decision=decision,
        risk_level=risk,
        matched_rules=tuple(rules) if rules else ("governance_baseline",),
        allowed_next_step="create draft for human review only",
    )
