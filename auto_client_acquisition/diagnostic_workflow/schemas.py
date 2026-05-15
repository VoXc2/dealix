"""Pydantic v2 schemas for the diagnostic workflow.

Wraps the founder-side happy-path: warm intro → diagnostic → service →
pilot offer → delivery plan → proof plan. Every input model is
``extra='forbid'`` and never stores raw email/phone — the customer is
identified by a public ``customer_handle`` placeholder only.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.company_brain_v6 import CompanyBrainV6

SourceLiteral = Literal["warm_intro", "inbound", "founder_network"]


class IntakeRequest(BaseModel):
    """Founder-supplied warm-intro intake.

    ``contact_handle`` is the customer's PUBLIC handle (e.g. anonymized
    ID, username). NEVER raw email or phone. Validation cannot detect
    every accidental leak, so the parser also re-anonymizes downstream.
    """

    model_config = ConfigDict(extra="forbid")

    company: str = Field(..., min_length=1)
    sector: str = "b2b_services"
    region: str = "ksa"
    contact_handle: str = "PLACEHOLDER-HANDLE"
    pipeline_state: str = ""
    source: SourceLiteral = "warm_intro"
    language_preference: str = "ar"


class IntakeRecord(BaseModel):
    """Anonymized intake snapshot — stored shape for downstream stages."""

    model_config = ConfigDict(extra="forbid")

    company: str
    sector: str
    region: str
    contact_handle: str
    pipeline_state: str
    source: SourceLiteral
    language_preference: str
    intake_id: str
    received_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    customer_handle: str
    consent_recorded: bool = False


class DiagnosticBundle(BaseModel):
    """Full diagnostic snapshot — never auto-sent, always approval-gated."""

    model_config = ConfigDict(extra="forbid")

    company: str
    recommended_bundle: str
    brain: CompanyBrainV6
    brief_markdown_ar_en: str
    gaps: list[str] = Field(default_factory=list)
    approval_status: str = "approval_required"


class PilotOffer(BaseModel):
    """Bilingual pilot offer — fixed at 499 SAR (Literal)."""

    model_config = ConfigDict(extra="forbid")

    company: str
    recommended_bundle: str
    amount_sar: Literal[499] = 499
    description_ar: str
    description_en: str
    terms_ar: str
    terms_en: str
    payment_url: str | None = None


class ProofPlan(BaseModel):
    """Plan of expected proof events — anchored to ProofEventType."""

    model_config = ConfigDict(extra="forbid")

    company: str
    expected_proof_events: list[str] = Field(default_factory=list)
    publishable_with_consent: bool = False
    summary_ar: str
    summary_en: str

    def as_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")
