"""Agent factory — build-time validation and registration of governed agents.
مصنع الوكلاء — التحقق من الوكلاء وتسجيلهم في وقت البناء.

``build_agent`` takes an ``AgentBlueprint``, runs it through every existing
governance / risk / permission / lifecycle gate, and on success registers an
``AgentCard`` in the ``agent_os`` registry. Rejections are returned as a
structured ``BuildResult`` with enumerated violation codes — never silent.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from auto_client_acquisition.agent_factory.blueprint import (
    AgentBlueprint,
    blueprint_structurally_valid,
)
from auto_client_acquisition.agent_factory.memory_binding import binding_valid
from auto_client_acquisition.agent_os.agent_card import AgentCard
from auto_client_acquisition.agent_os.agent_lifecycle import AgentLifecycleState
from auto_client_acquisition.agent_os.agent_registry import register_agent
from auto_client_acquisition.agent_os.autonomy_levels import AutonomyLevel
from auto_client_acquisition.agent_os.tool_permissions import tool_allowed_mvp
from auto_client_acquisition.agentic_operations_os.agent_auditability_card import (
    AgentAuditabilityCard,
    agent_auditability_card_valid,
)
from auto_client_acquisition.agentic_operations_os.agent_governance import (
    governance_decision_for_proposed_action,
)
from auto_client_acquisition.agentic_operations_os.agent_lifecycle import (
    deploy_prerequisites_met,
)
from auto_client_acquisition.agentic_operations_os.agent_permissions import (
    ToolClass,
    agent_tool_forbidden,
    tool_class_allowed_in_mvp,
)
from auto_client_acquisition.agentic_operations_os.agent_risk_score import (
    agent_risk_band,
    agent_risk_score,
)

_DEPLOY_TARGETS: frozenset[str] = frozenset(
    {AgentLifecycleState.STAGING.value, AgentLifecycleState.PRODUCTION.value},
)
_RECOMMEND: int = int(AutonomyLevel.RECOMMEND)


class BuildOutcome(StrEnum):
    BUILT = "built"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class BuildResult:
    outcome: BuildOutcome
    agent_id: str
    risk_score: int
    risk_band: str
    violations: tuple[str, ...]
    registered: bool


def build_agent(blueprint: AgentBlueprint) -> BuildResult:
    """Validate ``blueprint`` through all governance gates; register on success."""
    violations: list[str] = []

    # 1. Structural integrity (blueprint + memory binding).
    _ok, errs = blueprint_structurally_valid(blueprint)
    violations.extend(errs)
    _mem_ok, mem_errs = binding_valid(blueprint.memory)
    violations.extend(f"memory:{e}" for e in mem_errs)

    # 2. Tool deny-list (no_scraping / no_live_send live here).
    for tool in blueprint.tools:
        if agent_tool_forbidden(tool) or not tool_allowed_mvp(tool):
            violations.append(f"tool_forbidden:{tool}")

    # 3. Tool classes — MVP allows A/B/C only (D needs approval, E/F blocked).
    for cls in blueprint.tool_classes:
        if not tool_class_allowed_in_mvp(ToolClass(cls), internal_write_approved=False):
            violations.append(f"tool_class_blocked:{cls}")

    # 4. Risk band — a restricted agent is never built.
    score = agent_risk_score(blueprint.risk_dimensions)
    band = agent_risk_band(score)
    if band == "restricted_not_allowed":
        violations.append("risk_band_restricted")

    # 5. Governance baseline — MVP posture must stay draft-only.
    governance = governance_decision_for_proposed_action(
        agent_id=blueprint.agent_id,
        proposed_action=blueprint.role,
        contains_pii=False,
        external_channel=False,
    )
    if governance.decision not in ("DRAFT_ONLY", "ALLOW"):
        violations.append("governance_autonomy_mismatch")

    # 6. no_unbounded_agents — elevated autonomy needs a kill-switch owner.
    autonomy = int(blueprint.autonomy_level)
    if autonomy >= _RECOMMEND and not blueprint.kill_switch_owner.strip():
        violations.append("no_unbounded_agents:kill_switch_owner_required")

    # 7. no_unaudited_changes — every agent must be auditable.
    if not blueprint.auditability_enabled or not blueprint.audit_scope:
        violations.append("no_unaudited_changes:auditability_required")
    else:
        card = AgentAuditabilityCard(
            agent_id=blueprint.agent_id,
            audit_scope=tuple(blueprint.audit_scope),
            action_recoverability="reversible_draft_only",
            lifecycle_coverage="full",
            policy_checkability="checkable",
            responsibility_attribution=blueprint.owner,
            evidence_integrity="append_only_ledger",
            external_actions_allowed=False,
        )
        _card_ok, card_errs = agent_auditability_card_valid(card)
        violations.extend(f"auditability:{e}" for e in card_errs)

    # 8. Lifecycle deploy prerequisites — only when targeting staging/prod.
    if blueprint.lifecycle_target in _DEPLOY_TARGETS:
        present = {"agent_identity_card", "permission_card", "governance_tests"}
        if blueprint.auditability_enabled and blueprint.audit_scope:
            present.add("auditability_card")
        if blueprint.owner.strip():
            present.add("owner_assigned")
        if blueprint.kill_switch_owner.strip() or autonomy < _RECOMMEND:
            present.add("decommission_rule")
        _prereq_ok, missing = deploy_prerequisites_met(frozenset(present))
        violations.extend(f"deploy_prereq_missing:{m}" for m in missing)

    # 9. Escalation completeness — elevated autonomy needs a human-in-loop rule.
    if autonomy >= _RECOMMEND and not blueprint.escalation_rules:
        violations.append("escalation_rule_required")

    if violations:
        return BuildResult(
            outcome=BuildOutcome.REJECTED,
            agent_id=blueprint.agent_id,
            risk_score=score,
            risk_band=band,
            violations=tuple(violations),
            registered=False,
        )

    card = AgentCard(
        agent_id=blueprint.agent_id,
        name=blueprint.name,
        owner=blueprint.owner,
        purpose=blueprint.purpose,
        autonomy_level=autonomy,
        status="built",
    )
    try:
        register_agent(card)
    except ValueError as exc:
        # no_silent_failures — a registry rejection surfaces as a violation.
        return BuildResult(
            outcome=BuildOutcome.REJECTED,
            agent_id=blueprint.agent_id,
            risk_score=score,
            risk_band=band,
            violations=(f"registration_failed:{exc}",),
            registered=False,
        )
    return BuildResult(
        outcome=BuildOutcome.BUILT,
        agent_id=blueprint.agent_id,
        risk_score=score,
        risk_band=band,
        violations=(),
        registered=True,
    )


__all__ = ["BuildOutcome", "BuildResult", "build_agent"]
