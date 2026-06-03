"""Pydantic v2 schemas for the AI Workforce orchestrator.

Defines the contracts for the 12 specialized agents the founder can
spin up over the existing v5/v6 layers. No LLM, no external HTTP.
"""
from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class AutonomyLevel(StrEnum):
    OBSERVE_ONLY = "observe_only"
    ANALYZE_ONLY = "analyze_only"
    DRAFT_ONLY = "draft_only"
    APPROVAL_REQUIRED = "approval_required"
    APPROVED_MANUAL_ACTION = "approved_manual_action"
    BLOCKED = "blocked"


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKED = "blocked"


class AgentSpec(BaseModel):
    """Static description of one agent's contract + autonomy budget."""

    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    agent_id: str
    role_ar: str
    role_en: str
    allowed_inputs: list[str] = Field(default_factory=list)
    allowed_outputs: list[str] = Field(default_factory=list)
    allowed_tools: list[str] = Field(default_factory=list)
    forbidden_tools: list[str] = Field(default_factory=list)
    autonomy_level: AutonomyLevel
    default_action_mode: str
    risk_level: RiskLevel
    requires_approval: bool = True
    cost_budget_usd: float = 0.50
    evidence_required: bool = True


class WorkforceGoal(BaseModel):
    """Founder-supplied goal for a workforce run."""

    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    company_handle: str = Field(..., min_length=1)
    company_context: str = ""
    goal_ar: str = ""
    goal_en: str = ""
    desired_outcome: str = ""
    available_assets: list[str] = Field(default_factory=list)
    approved_channels: list[str] = Field(default_factory=list)
    blocked_channels: list[str] = Field(default_factory=list)
    budget_sar: float | None = None
    urgency: Literal["low", "medium", "high"] = "medium"
    language_preference: Literal["ar", "en", "bilingual"] = "ar"
    founder_mode: bool = False


class AgentTask(BaseModel):
    """One agent's contribution to a workforce run."""

    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    agent_id: str
    role_ar: str
    role_en: str
    action_summary_ar: str
    action_summary_en: str
    output: dict[str, Any] = Field(default_factory=dict)
    action_mode: str
    approval_status: str = "approval_required"
    risk_level: RiskLevel
    cost_estimate_usd: float = 0.0
    evidence_pointers: list[str] = Field(default_factory=list)


class WorkforceRun(BaseModel):
    """Aggregated result of one workforce orchestration run."""

    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    run_id: str = Field(default_factory=lambda: f"run_{uuid4().hex[:12]}")
    summary_ar: str = ""
    summary_en: str = ""
    assigned_agents: list[str] = Field(default_factory=list)
    task_plan: list[AgentTask] = Field(default_factory=list)
    recommended_service: str = "growth_starter"
    approval_requests: list[dict[str, Any]] = Field(default_factory=list)
    blocked_actions: list[dict[str, Any]] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    next_best_action: str = ""
    cost_estimate_usd: float = 0.0
    risk_summary: dict[str, Any] = Field(default_factory=dict)
    guardrails: dict[str, bool] = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
