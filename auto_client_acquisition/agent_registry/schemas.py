"""Pydantic schema for the Agent Registry — doctrine #9.

Doctrine #9: no AI agent runs without a named owner, an explicit scope
and an audit hook. ``AgentSpec`` carries all three plus an allowed-tool
allowlist and a risk class.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

RiskClass = Literal["safe_auto", "draft_only", "approval_required", "blocked"]


class AgentSpec(BaseModel):
    """One agent's governance contract.

    ``owner`` and ``scope`` are mandatory and non-empty — ``registry.verify``
    hard-fails when either is blank.
    """

    model_config = ConfigDict(extra="forbid")

    agent_name: str = Field(..., min_length=1)
    owner: str = Field(..., min_length=1)
    scope: str = Field(..., min_length=1)
    allowed_tools: list[str] = Field(default_factory=list)
    risk_class: RiskClass = "draft_only"
    audit_hook: str = "default_audit_hook"


__all__ = ["AgentSpec", "RiskClass"]
