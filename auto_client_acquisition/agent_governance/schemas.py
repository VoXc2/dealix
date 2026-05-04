"""Typed records for the agent-governance plane."""
from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AutonomyLevel(StrEnum):
    L0_READ_ONLY = "L0_read_only"
    L1_DRAFT_ONLY = "L1_draft_only"
    L2_APPROVAL_REQUIRED = "L2_approval_required"
    L3_APPROVED_EXECUTE = "L3_approved_execute"
    L4_INTERNAL_AUTOMATION_ONLY = "L4_internal_automation_only"
    L5_BLOCKED_FOR_EXTERNAL = "L5_blocked_for_external"


class ToolCategory(StrEnum):
    READ_PUBLIC_WEB = "read_public_web"
    READ_INTERNAL_DOCS = "read_internal_docs"
    DRAFT_MESSAGE = "draft_message"
    DRAFT_EMAIL = "draft_email"
    DRAFT_WHATSAPP_REPLY = "draft_whatsapp_reply"
    GENERATE_PROOF_PACK = "generate_proof_pack"
    CREATE_INVOICE_DRAFT = "create_invoice_draft"
    SEND_EMAIL_LIVE = "send_email_live"
    SEND_WHATSAPP_LIVE = "send_whatsapp_live"
    LINKEDIN_AUTOMATION = "linkedin_automation"
    SCRAPE_WEB = "scrape_web"
    CHARGE_PAYMENT_LIVE = "charge_payment_live"


class ToolPermission(StrEnum):
    ALLOWED = "allowed"
    REQUIRES_APPROVAL = "requires_approval"
    FORBIDDEN = "forbidden"


class AgentSpec(BaseModel):
    """One agent's governance contract."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    agent_id: str
    purpose_ar: str
    purpose_en: str
    max_autonomy: AutonomyLevel = AutonomyLevel.L2_APPROVAL_REQUIRED
    allowed_tools: list[ToolCategory] = Field(default_factory=list)
    forbidden_tools: list[ToolCategory] = Field(default_factory=list)
    requires_human_review: bool = True
    logging_required: bool = True
    notes: str = ""


class ActionEvaluation(BaseModel):
    """Verdict on whether an agent may take a specific action."""

    model_config = ConfigDict(use_enum_values=True)

    permitted: bool
    permission: ToolPermission
    reason: str
    autonomy_level: AutonomyLevel
    tool: ToolCategory
    safety_notes: list[str] = Field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")
