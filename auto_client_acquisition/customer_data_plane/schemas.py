"""Typed records for consent + contactability."""
from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class ConsentStatus(StrEnum):
    GRANTED = "granted"
    WITHDRAWN = "withdrawn"
    UNKNOWN = "unknown"


class ConsentSource(StrEnum):
    WEBSITE_FORM = "website_form"
    INBOUND_REPLY = "inbound_reply"
    SIGNED_CONTRACT = "signed_contract"
    VERBAL_ON_CALL = "verbal_on_call"
    PARTNER_REFERRAL_INTRO = "partner_referral_intro"
    UNKNOWN = "unknown"


class ChannelKind(StrEnum):
    WHATSAPP_INBOUND = "whatsapp_inbound"
    WHATSAPP_TEMPLATE = "whatsapp_template"
    EMAIL_DRAFT = "email_draft"
    EMAIL_INBOUND = "email_inbound"
    LINKEDIN_MANUAL = "linkedin_manual"
    PHONE_CALL_REQUESTED = "phone_call_requested"
    PARTNER_INTRO = "partner_intro"
    BLOCKED = "blocked"


class ContactabilityVerdict(StrEnum):
    SAFE = "safe"
    NEEDS_REVIEW = "needs_review"
    BLOCKED = "blocked"


class ConsentRecord(BaseModel):
    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    id: str = Field(default_factory=lambda: f"con_{uuid4().hex[:12]}")
    contact_id: str
    channel: ChannelKind
    consent_status: ConsentStatus = ConsentStatus.UNKNOWN
    consent_source: ConsentSource = ConsentSource.UNKNOWN
    consent_timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    consent_method_note: str = ""
    withdrawal_timestamp: datetime | None = None
    allowed_purposes: list[str] = Field(default_factory=list)
    evidence_id: str | None = None

    def is_active(self) -> bool:
        return self.consent_status == ConsentStatus.GRANTED.value and not self.withdrawal_timestamp


class ContactabilityResult(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    contact_id: str
    channel: ChannelKind
    verdict: ContactabilityVerdict
    reason: str
    consent_known: bool
    consent_record_id: str | None = None
    safety_notes: list[str] = Field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")
