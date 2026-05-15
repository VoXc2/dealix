"""Pydantic contracts for commercial engagement sprint runners."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class LeadIntelligenceSprintInput(BaseModel):
    """Account-style dict rows; ``company`` is accepted as alias for company name."""

    model_config = ConfigDict(extra="allow")

    accounts: list[dict[str, Any]] = Field(default_factory=list, max_length=500)
    top_n: int = Field(default=50, ge=1, le=500)
    sector_weight: float = Field(default=0.12, ge=0.0, le=0.5)
    city_weight: float = Field(default=0.08, ge=0.0, le=0.5)


class LeadIntelligenceSprintReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    data_quality: dict[str, Any]
    accounts_ranked: list[dict[str, Any]]
    dedupe_hints: list[dict[str, Any]]
    action_plan: list[str]
    draft_audits: list[dict[str, Any]]
    governance_notes: list[str]
    proof_pack_suggestions: list[str] = Field(
        default_factory=list,
        description="Suggested ProofEventType values to record as the sprint completes.",
    )


class SupportDeskMessageIn(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    text: str | None = None
    body: str | None = None


class SupportDeskSprintInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    messages: list[str | SupportDeskMessageIn | dict[str, Any]] = Field(
        default_factory=list, max_length=200
    )


class SupportDeskSprintReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[dict[str, Any]]
    summary: dict[str, int]


class QuickWinOpsInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    weekly_rows: list[dict[str, Any]] = Field(default_factory=list, max_length=10_000)
    group_by: str = Field(default="channel")
    checklist_phases: tuple[Literal["build", "validate"], ...] = ("build", "validate")


class QuickWinOpsReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rollup: dict[str, Any]
    checklists: dict[str, list[str]]


class CampaignIntelligenceSprintInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    offer_title: str = Field(min_length=1, max_length=200)
    sector: str = Field(default="", max_length=120)
    audience_notes: str = Field(default="", max_length=2000)
    locale: Literal["ar", "en"] = "ar"


class CampaignIntelligenceSprintReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    angles: list[str]
    message_hooks: list[str]
    risk_flags: list[str]
    draft_snippets: list[dict[str, Any]]
