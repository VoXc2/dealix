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


_REQUIRED_FORBIDDEN = (
    "cold_whatsapp",
    "scrape",
    "send_messages",
)


def evaluate_agent_gate(inp: "AgentGateInput") -> "AgentGateResult":
    """HTTP helper — stricter MVP checks than the structural `AgentDecisionGate` tuple."""
    from auto_client_acquisition.board_decision_os.schemas import AgentGateInput, AgentGateResult

    reasons_ar: list[str] = []
    reasons_en: list[str] = []

    forbidden_lower = [x.lower() for x in inp.forbidden_actions]
    for token in _REQUIRED_FORBIDDEN:
        if not any(token in f for f in forbidden_lower):
            reasons_ar.append(f"يجب أن تتضمن قائمة الممنوعات إشارة صريحة إلى: {token}")
            reasons_en.append(f"forbidden_actions must explicitly cover '{token}'")

    if inp.autonomy_level > 3:
        reasons_ar.append("مستوى الاستقلالية أعلى من 3 غير مسموح في MVP.")
        reasons_en.append("autonomy_level > 3 is not allowed in MVP.")

    if not inp.audit_required:
        reasons_ar.append("يجب تفعيل التدقيق (audit_required=true).")
        reasons_en.append("audit_required must be true.")

    if len(inp.allowed_tools) == 0:
        reasons_ar.append("قائمة الأدوات المسموحة فارغة.")
        reasons_en.append("allowed_tools is empty.")

    approved = len(reasons_ar) == 0
    return AgentGateResult(approved=approved, reasons_ar=reasons_ar, reasons_en=reasons_en)
