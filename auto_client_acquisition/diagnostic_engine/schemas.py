"""
Pydantic v2 schemas for the Diagnostic Engine.
نماذج Pydantic لمحرّك التشخيص.
"""

from __future__ import annotations

from datetime import UTC, datetime, timezone
from typing import List

from pydantic import BaseModel, ConfigDict, Field


def _utcnow_naive() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class DiagnosticRequest(BaseModel):
    """Inbound request body for the diagnostic generator."""

    model_config = ConfigDict(extra="forbid")

    company: str = Field(..., min_length=1)
    sector: str = "b2b_services"
    region: str = "ksa"
    pipeline_state: str = ""


class DiagnosticResult(BaseModel):
    """Bilingual diagnostic brief — never auto-sent, always approval-gated."""

    model_config = ConfigDict(use_enum_values=True)

    company: str
    recommended_bundle: str
    bundle_name_ar: str
    bundle_name_en: str
    services_in_bundle: list[str]
    markdown_ar_en: str
    approval_status: str = "approval_required"
    safety_notes: list[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=_utcnow_naive)
