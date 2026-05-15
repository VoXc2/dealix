"""Pydantic v2 schemas for the Self-Growth OS.

Every record carries enough metadata for downstream tracking:

  - ``id``                     stable per-record identifier
  - ``language``               ar / en / bilingual
  - ``source``                 free-form provenance tag
  - ``confidence``             0.0-1.0
  - ``risk_level``             low / medium / high / blocked
  - ``approval_status``        defaults to ``approval_required``
  - ``recommended_action``     one short imperative
  - ``service_bundle``         which Dealix bundle the record relates to
  - ``proof_event``            optional reference to a recorded ProofEvent
  - ``created_at``             timezone-aware UTC
"""
from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

# ─── Enums ──────────────────────────────────────────────────────────


class Language(StrEnum):
    AR = "ar"
    EN = "en"
    BILINGUAL = "bilingual"


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKED = "blocked"


class ApprovalStatus(StrEnum):
    DRAFT_ONLY = "draft_only"
    APPROVAL_REQUIRED = "approval_required"
    APPROVED = "approved"
    BLOCKED = "blocked"


class ServiceBundle(StrEnum):
    GROWTH_STARTER = "growth_starter"
    DATA_TO_REVENUE = "data_to_revenue"
    EXECUTIVE_GROWTH_OS = "executive_growth_os"
    PARTNERSHIP_GROWTH = "partnership_growth"
    FULL_CONTROL_TOWER = "full_control_tower"
    INTERNAL = "internal"
    UNKNOWN = "unknown"


class PublishingDecision(StrEnum):
    ALLOWED_DRAFT = "allowed_draft"
    NEEDS_REVIEW = "needs_review"
    BLOCKED = "blocked"


# ─── Base ───────────────────────────────────────────────────────────


def _gen_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


class _Base(BaseModel):
    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    id: str
    language: Language = Language.AR
    source: str = "self_growth_os"
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    risk_level: RiskLevel = RiskLevel.MEDIUM
    target_persona: str = "founder"
    service_bundle: ServiceBundle = ServiceBundle.UNKNOWN
    recommended_action: str = ""
    approval_status: ApprovalStatus = ApprovalStatus.APPROVAL_REQUIRED
    proof_event: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


# ─── Concrete records ───────────────────────────────────────────────


class ServiceActivationCheck(_Base):
    """The result of running the activation matrix over one service."""

    service_id: str
    name_ar: str
    name_en: str
    status: Literal["live", "pilot", "partial", "target", "blocked", "backlog"]
    eight_gate_block_present: bool = False
    blocking_reasons: list[str] = Field(default_factory=list)
    next_activation_step_ar: str = ""
    next_activation_step_en: str = ""

    @classmethod
    def new(cls, **kwargs: Any) -> ServiceActivationCheck:
        kwargs.setdefault("id", _gen_id("sac"))
        return cls(**kwargs)


class SafePublishingResult(_Base):
    """Outcome of running the safe-publishing-gate regex over copy."""

    decision: PublishingDecision
    forbidden_tokens_found: list[str] = Field(default_factory=list)
    sample_excerpts: list[str] = Field(default_factory=list)
    notes: str = ""

    @classmethod
    def new(cls, **kwargs: Any) -> SafePublishingResult:
        kwargs.setdefault("id", _gen_id("spr"))
        return cls(**kwargs)


class ToolCapability(_Base):
    """One row in the optional-tooling matrix."""

    tool_name: str
    installed: bool
    required_for_core: bool
    install_hint: str = ""
    safe_usage_notes: str = ""

    @classmethod
    def new(cls, **kwargs: Any) -> ToolCapability:
        kwargs.setdefault("id", _gen_id("tool"))
        kwargs.setdefault("approval_status", ApprovalStatus.APPROVED)  # tooling rows aren't external actions
        return cls(**kwargs)


class EvidenceRecord(_Base):
    """A small structured event recorded by self-growth runs."""

    event_type: str
    summary: str
    artifact_path: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def new(cls, **kwargs: Any) -> EvidenceRecord:
        kwargs.setdefault("id", _gen_id("evt"))
        kwargs.setdefault("approval_status", ApprovalStatus.APPROVED)
        return cls(**kwargs)
