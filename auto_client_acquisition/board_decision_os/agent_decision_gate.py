"""Agent decision gate — stricter board checks before adding agents."""

from __future__ import annotations

from dataclasses import dataclass

AGENT_DECISION_GATE_FIELDS: tuple[str, ...] = (
    "purpose_clear",
    "owner_clear",
    "allowed_tools_defined",
    "forbidden_actions_clear",
    "autonomy_level_at_most_three",
    "audit_required",
    "decommission_rule_exists",
)


@dataclass(frozen=True, slots=True)
class AgentDecisionGate:
    purpose_clear: bool
    owner_clear: bool
    allowed_tools_defined: bool
    forbidden_actions_clear: bool
    autonomy_level_at_most_three: bool
    audit_required: bool
    decommission_rule_exists: bool


def agent_decision_gate_passes(gate: AgentDecisionGate) -> tuple[bool, tuple[str, ...]]:
    missing: list[str] = []
    if not gate.purpose_clear:
        missing.append("purpose_unclear")
    if not gate.owner_clear:
        missing.append("owner_unclear")
    if not gate.allowed_tools_defined:
        missing.append("allowed_tools_undefined")
    if not gate.forbidden_actions_clear:
        missing.append("forbidden_actions_unclear")
    if not gate.autonomy_level_at_most_three:
        missing.append("autonomy_too_high_for_mvp")
    if not gate.audit_required:
        missing.append("audit_not_required")
    if not gate.decommission_rule_exists:
        missing.append("decommission_rule_missing")
    return not missing, tuple(missing)
