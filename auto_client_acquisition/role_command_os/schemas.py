"""Typed records for the role command OS."""
from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RoleName(StrEnum):
    CEO = "ceo"
    SALES = "sales"
    GROWTH = "growth"
    PARTNERSHIP = "partnership"
    CUSTOMER_SUCCESS = "cs"
    FINANCE = "finance"
    COMPLIANCE = "compliance"
    DELIVERY = "delivery"
    SUPPORT = "support"
    OPERATIONS = "operations"


class RoleDecision(BaseModel):
    """One actionable decision surfaced to the role."""

    model_config = ConfigDict(extra="forbid")

    title_ar: str
    title_en: str
    rationale_ar: str = ""
    rationale_en: str = ""
    risk_level: str = "low"  # low | medium | high | blocked
    approval_required: bool = True
    proof_event: str | None = None


class RoleBrief(BaseModel):
    """Per-role daily brief — Arabic primary, English secondary."""

    model_config = ConfigDict(use_enum_values=True)

    role: RoleName
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    summary_ar: str
    summary_en: str
    top_decisions: list[RoleDecision]
    risks: list[str] = Field(default_factory=list)
    approvals_needed: list[str] = Field(default_factory=list)
    evidence_pointers: list[str] = Field(default_factory=list)
    next_action_ar: str = ""
    next_action_en: str = ""
    blocked_actions: list[str] = Field(default_factory=list)
    guardrails: dict[str, bool] = Field(default_factory=lambda: {
        "no_live_send": True,
        "no_scraping": True,
        "no_cold_outreach": True,
        "approval_required_for_external_actions": True,
    })

    def as_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")
