"""Policy logic for agent-governance evaluations."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.agent_governance.schemas import (
    ActionEvaluation,
    AutonomyLevel,
    ToolCategory,
    ToolPermission,
)

# Forbidden by default at the platform level. NO agent may use these
# regardless of autonomy level. Mirrors the runtime block in
# auto_client_acquisition/v3/agents.py:SafeAgentRuntime.restricted_actions.
FORBIDDEN_TOOLS: frozenset[ToolCategory] = frozenset({
    ToolCategory.SEND_WHATSAPP_LIVE,
    ToolCategory.LINKEDIN_AUTOMATION,
    ToolCategory.SCRAPE_WEB,
    ToolCategory.CHARGE_PAYMENT_LIVE,
    ToolCategory.SEND_EMAIL_LIVE,
})


# Tool categories that require approval even at L3+ (no auto-execute).
APPROVAL_REQUIRED_TOOLS: frozenset[ToolCategory] = frozenset({
    ToolCategory.GENERATE_PROOF_PACK,
    ToolCategory.CREATE_INVOICE_DRAFT,
    ToolCategory.DRAFT_EMAIL,
    ToolCategory.DRAFT_WHATSAPP_REPLY,
    ToolCategory.DRAFT_MESSAGE,
})


def _autonomy_rank(level: AutonomyLevel) -> int:
    """Higher number = more autonomy. L5 is special — blocked-for-external."""
    return {
        AutonomyLevel.L0_READ_ONLY: 0,
        AutonomyLevel.L1_DRAFT_ONLY: 1,
        AutonomyLevel.L2_APPROVAL_REQUIRED: 2,
        AutonomyLevel.L3_APPROVED_EXECUTE: 3,
        AutonomyLevel.L4_INTERNAL_AUTOMATION_ONLY: 4,
        AutonomyLevel.L5_BLOCKED_FOR_EXTERNAL: 5,
    }[level]


def evaluate_action(
    *,
    agent_id: str,
    tool: ToolCategory | str,
    autonomy_level: AutonomyLevel | str,
    allowed_tools: list[ToolCategory | str] | None = None,
) -> ActionEvaluation:
    """Decide whether an agent may take an action.

    The decision tree:
      1. Tool is on FORBIDDEN_TOOLS → FORBIDDEN regardless of level.
      2. Autonomy = L5 → BLOCKED for any external-effect tool.
      3. Tool not in allowed_tools list → FORBIDDEN.
      4. Tool requires approval AND autonomy < L3 → REQUIRES_APPROVAL.
      5. Tool requires approval AND autonomy ≥ L3 → REQUIRES_APPROVAL
         (still — these tools NEVER skip human review).
      6. Read-only tool → ALLOWED.
    """
    tool_enum = tool if isinstance(tool, ToolCategory) else ToolCategory(tool)
    level = (
        autonomy_level
        if isinstance(autonomy_level, AutonomyLevel)
        else AutonomyLevel(autonomy_level)
    )
    allowed = list(allowed_tools or [])
    allowed_normalized = [
        t if isinstance(t, ToolCategory) else ToolCategory(t)
        for t in allowed
    ]

    safety_notes = [
        "default_external_action_mode_is_approval_required_or_blocked",
        "no_cold_outreach",
        "no_scraping",
        "no_linkedin_automation",
    ]

    # 1. Forbidden tool — never permitted.
    if tool_enum in FORBIDDEN_TOOLS:
        return ActionEvaluation(
            permitted=False,
            permission=ToolPermission.FORBIDDEN,
            reason=(
                f"tool {tool_enum.value} is on the platform-level "
                "FORBIDDEN_TOOLS set; no autonomy level can override"
            ),
            autonomy_level=level,
            tool=tool_enum,
            safety_notes=safety_notes,
        )

    # 2. L5 blocks any external-effect tool. Read-only tools stay allowed.
    if level == AutonomyLevel.L5_BLOCKED_FOR_EXTERNAL:
        if tool_enum in {
            ToolCategory.READ_PUBLIC_WEB,
            ToolCategory.READ_INTERNAL_DOCS,
        }:
            return ActionEvaluation(
                permitted=True,
                permission=ToolPermission.ALLOWED,
                reason="L5 + read-only tool — read access permitted",
                autonomy_level=level,
                tool=tool_enum,
                safety_notes=safety_notes,
            )
        return ActionEvaluation(
            permitted=False,
            permission=ToolPermission.FORBIDDEN,
            reason=f"agent at L5 may not use external-effect tool {tool_enum.value}",
            autonomy_level=level,
            tool=tool_enum,
            safety_notes=safety_notes,
        )

    # 3. Tool must be on the agent's allowed_tools list.
    if tool_enum not in allowed_normalized:
        return ActionEvaluation(
            permitted=False,
            permission=ToolPermission.FORBIDDEN,
            reason=(
                f"tool {tool_enum.value} not in agent {agent_id!r} allowed_tools"
            ),
            autonomy_level=level,
            tool=tool_enum,
            safety_notes=safety_notes,
        )

    # 4. Approval-required tools NEVER auto-execute, even at L3+.
    if tool_enum in APPROVAL_REQUIRED_TOOLS:
        return ActionEvaluation(
            permitted=True,
            permission=ToolPermission.REQUIRES_APPROVAL,
            reason=(
                f"tool {tool_enum.value} produces external-visible output; "
                "human approval required regardless of autonomy level"
            ),
            autonomy_level=level,
            tool=tool_enum,
            safety_notes=safety_notes,
        )

    # 5. Read-only / internal tools at L0-L1 are allowed.
    if tool_enum in {
        ToolCategory.READ_PUBLIC_WEB,
        ToolCategory.READ_INTERNAL_DOCS,
    }:
        return ActionEvaluation(
            permitted=True,
            permission=ToolPermission.ALLOWED,
            reason="read-only tool at any non-L5 level",
            autonomy_level=level,
            tool=tool_enum,
            safety_notes=safety_notes,
        )

    # 6. Anything else default to approval-required at L2 or below.
    if _autonomy_rank(level) < _autonomy_rank(AutonomyLevel.L3_APPROVED_EXECUTE):
        return ActionEvaluation(
            permitted=True,
            permission=ToolPermission.REQUIRES_APPROVAL,
            reason="default approval-required at L2 or below",
            autonomy_level=level,
            tool=tool_enum,
            safety_notes=safety_notes,
        )

    # L3-L4 with non-approval-required tool: allowed but logged.
    return ActionEvaluation(
        permitted=True,
        permission=ToolPermission.ALLOWED,
        reason=f"autonomy {level.value} permits internal tool {tool_enum.value}",
        autonomy_level=level,
        tool=tool_enum,
        safety_notes=safety_notes,
    )


def summary() -> dict[str, Any]:
    """Documentation endpoint — what the policy enforces."""
    return {
        "schema_version": 1,
        "default_autonomy_level": AutonomyLevel.L2_APPROVAL_REQUIRED.value,
        "forbidden_tools": sorted(t.value for t in FORBIDDEN_TOOLS),
        "approval_required_tools": sorted(t.value for t in APPROVAL_REQUIRED_TOOLS),
        "autonomy_levels": [
            {"level": al.value, "rank": _autonomy_rank(al)}
            for al in AutonomyLevel
        ],
        "guardrails": {
            "no_live_send": True,
            "no_scraping": True,
            "no_linkedin_automation": True,
            "no_live_charge": True,
            "approval_required_for_external_actions": True,
        },
    }
