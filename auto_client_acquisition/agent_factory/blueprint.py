"""Agent blueprint — the full declarative specification of a governed agent.
مخطّط الوكيل — المواصفة التعريفية الكاملة لوكيل محكوم.

A blueprint is the single input to the Agent Factory. It composes the
existing identity / autonomy / permission / risk vocabulary — it never
redefines it.
"""
from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.agent_factory.memory_binding import AgentMemoryBinding
from auto_client_acquisition.agent_os.agent_lifecycle import AgentLifecycleState
from auto_client_acquisition.agent_os.autonomy_levels import AutonomyLevel
from auto_client_acquisition.agentic_operations_os.agent_permissions import ToolClass
from auto_client_acquisition.agentic_operations_os.agent_risk_score import AgentRiskDimensions


class EscalationTrigger(StrEnum):
    LOW_CONFIDENCE = "low_confidence"
    PII_DETECTED = "pii_detected"
    EXTERNAL_ACTION_REQUESTED = "external_action_requested"
    RISK_THRESHOLD_EXCEEDED = "risk_threshold_exceeded"
    TOOL_DENIED = "tool_denied"


class EvaluationRule(BaseModel):
    """A threshold an agent must meet on a named evaluation metric."""

    model_config = ConfigDict(extra="forbid")

    rule_id: str = Field(..., min_length=1)
    description: str = ""
    metric: Literal[
        "faithfulness",
        "context_relevance",
        "answer_relevance",
        "escalation_rate",
    ]
    min_threshold: float = Field(default=0.0, ge=0.0, le=1.0)


class EscalationRule(BaseModel):
    """When ``trigger`` fires, the agent hands off instead of proceeding."""

    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    trigger: EscalationTrigger
    handoff_to: str = Field(..., min_length=1)
    required_action: str = Field(..., min_length=1)


class AgentBlueprint(BaseModel):
    """The full declarative spec of one governed agent.
    المواصفة التعريفية الكاملة لوكيل محكوم واحد."""

    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    agent_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    owner: str = Field(..., min_length=1)
    purpose: str = Field(..., min_length=1)
    role: str = Field(..., min_length=1)
    goals: list[str] = Field(default_factory=list)

    autonomy_level: AutonomyLevel = AutonomyLevel.READ_ONLY
    lifecycle_target: AgentLifecycleState = AgentLifecycleState.DRAFT

    tools: list[str] = Field(default_factory=list)
    tool_classes: list[ToolClass] = Field(default_factory=list)
    risk_dimensions: AgentRiskDimensions

    memory: AgentMemoryBinding = Field(default_factory=AgentMemoryBinding)
    evaluation_rules: list[EvaluationRule] = Field(default_factory=list)
    escalation_rules: list[EscalationRule] = Field(default_factory=list)
    workflow_scope: list[str] = Field(default_factory=list)
    business_metrics: list[str] = Field(default_factory=list)

    kill_switch_owner: str = ""
    auditability_enabled: bool = False
    audit_scope: list[str] = Field(default_factory=list)


def blueprint_structurally_valid(bp: AgentBlueprint) -> tuple[bool, tuple[str, ...]]:
    """Cheap presence checks — returns ``(ok, errors)`` like ``agent_identity_valid``."""
    errors: list[str] = []
    if not bp.agent_id.strip():
        errors.append("agent_id_required")
    if not bp.name.strip():
        errors.append("name_required")
    if not bp.owner.strip():
        errors.append("owner_required")
    if not bp.purpose.strip():
        errors.append("purpose_required")
    if not bp.role.strip():
        errors.append("role_required")
    if not bp.goals:
        errors.append("at_least_one_goal_required")
    return not errors, tuple(errors)


__all__ = [
    "AgentBlueprint",
    "EscalationRule",
    "EscalationTrigger",
    "EvaluationRule",
    "blueprint_structurally_valid",
]
