"""Agent society coordination primitives (System 57)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AgentNode:
    agent_id: str
    role: str
    specialization: str
    autonomy_level: int
    boundary_tags: frozenset[str]
    can_escalate: bool = True


@dataclass(frozen=True, slots=True)
class SocietyTaskPlan:
    requested_action: str
    requires_external_action: bool
    required_boundary_tag: str


def agent_society_governed(
    agents: tuple[AgentNode, ...],
    plan: SocietyTaskPlan,
) -> dict[str, object]:
    """Evaluate if a society can execute while preserving governance boundaries."""
    eligible = [
        a
        for a in agents
        if plan.required_boundary_tag in a.boundary_tags and a.autonomy_level >= 2
    ]
    decision = "block"
    next_action = "escalate"
    if not eligible:
        blockers = ("no_agent_with_required_boundary",)
    else:
        blockers = ()
        has_reviewer = any(a.role == "reviewer" for a in eligible)
        has_executor = any(a.role in {"executor", "orchestrator"} for a in eligible)
        if has_reviewer and has_executor:
            decision = "allow_with_review"
            next_action = "route_to_reviewer_then_execute"
        elif any(a.can_escalate for a in eligible):
            decision = "allow_with_escalation"
            next_action = "escalate_for_review"
        if plan.requires_external_action and decision == "allow_with_escalation":
            blockers = ("external_action_requires_preassigned_reviewer",)
            decision = "draft_only"
            next_action = "human_review"
    return {
        "decision": decision,
        "next_action": next_action,
        "eligible_agents": tuple(a.agent_id for a in eligible),
        "blockers": blockers,
    }
