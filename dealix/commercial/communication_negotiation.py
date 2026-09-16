"""Communication & Negotiation — authority-hardened, fail-closed, canonical external execution gate."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"


class NegotiationState(StrEnum):
    PREPARING = "preparing"
    DRAFT = "draft"
    APPROVED = "approved"
    SENT = "sent"
    NEGOTIATING = "negotiating"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"


class SenderIdentityEvidence(BaseModel):
    """Evidence-backed sender identity — no placeholder defaults."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    email: str = Field(..., min_length=1, description="Verified sender email with evidence_ref")
    phone: str = Field(..., min_length=1, description="Verified sender phone with evidence_ref")
    evidence_ref: str = Field(..., min_length=1, description="Reference to identity verification evidence")
    verified_at: str = Field(..., min_length=1, description="ISO-8601 timestamp of verification")

    @field_validator("email")
    @classmethod
    def _reject_placeholder_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized in {"founder@dealix.me", "unknown", UNKNOWN.lower()}:
            raise ValueError("placeholder or UNKNOWN sender email is not identity authority")
        return value.strip()

    @field_validator("phone")
    @classmethod
    def _reject_placeholder_phone(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized or normalized.upper() == UNKNOWN or "X" in normalized.upper():
            raise ValueError("placeholder, XXXX, or UNKNOWN sender phone is not identity authority")
        return normalized


class SiteReadinessEvidence(BaseModel):
    """Site/provider readiness — fail closed unless evidenced."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    site_ready: bool = False
    provider_ready: bool = False
    social_ready: bool = False
    evidence_ref: str = Field(..., min_length=1, description="Reference to readiness verification evidence")
    checked_at: str = Field(..., min_length=1, description="ISO-8601 timestamp of readiness check")


class CommunicationTask(BaseModel):
    """Communication task — draft-only, no sender authority, no queue/scheduler."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_id: str
    channel: str
    recipient: str
    subject: str = UNKNOWN
    body_ar: str = UNKNOWN
    body_en: str = UNKNOWN
    sender_identity_ref: str = Field(..., min_length=1, description="Reference to SenderIdentityEvidence")
    site_readiness_ref: str = Field(..., min_length=1, description="Reference to SiteReadinessEvidence")
    negotiation_state: NegotiationState = NegotiationState.DRAFT
    social_automated: bool = False
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    approval_required: bool = True
    sent: bool = False

    @model_validator(mode="after")
    def _enforce_draft_only_state(self) -> "CommunicationTask":
        if self.negotiation_state is not NegotiationState.DRAFT:
            raise ValueError("negotiation_state must be DRAFT for draft-only CommunicationTask")
        if self.social_automated:
            raise ValueError("social_automated must be False for draft-only CommunicationTask")
        if self.sent:
            raise ValueError("sent must be False for draft-only CommunicationTask")
        if not self.approval_required:
            raise ValueError("approval_required must remain True for draft-only CommunicationTask")
        return self


class CommunicationNegotiationEngine:
    """
    Authority-hardened communication engine.

    - No placeholder sender identity (founder@dealix.me, +9665XXXXXXXX)
    - Site/provider/social readiness fail closed unless evidenced
    - create_task produces DRAFT only, social_automated=False
    - approve_and_send removed — delegates to canonical external_execution_gate
    - automate_social reports draft/preparation capability only
    - No internal queue/scheduler — reuses canonical contracts
    """

    def __init__(self) -> None:
        pass

    def create_task(
        self,
        channel: str,
        recipient: str,
        subject: str,
        body_ar: str,
        body_en: str,
        *,
        sender_identity_ref: str,
        site_readiness_ref: str,
    ) -> CommunicationTask:
        """Create a DRAFT communication task — requires evidenced sender identity and site readiness."""
        task_id = f"comm_{hashlib.sha256((recipient + subject).encode()).hexdigest()[:8]}"
        return CommunicationTask(
            task_id=task_id,
            channel=channel,
            recipient=recipient,
            subject=subject,
            body_ar=body_ar,
            body_en=body_en,
            sender_identity_ref=sender_identity_ref,
            site_readiness_ref=site_readiness_ref,
            negotiation_state=NegotiationState.DRAFT,
            social_automated=False,
            approval_required=True,
            sent=False,
        )

    def prepare_external_action_packet(
        self,
        task: CommunicationTask,
        *,
        action_class: Literal["EMAIL_SEND", "WHATSAPP_SEND", "COMPANY_SOCIAL_PUBLISH", "CUSTOMER_QUOTE_SEND"],
        purpose_class: Literal["DIRECT_MARKETING", "INBOUND_REPLY", "REQUESTED_FOLLOWUP", "TRANSACTIONAL", "CUSTOMER_QUOTE", "PUBLIC_PUBLISH"],
        artifact_ref: str,
        content_sha256: str,
        identity_or_relationship_ref: str,
        consent_or_channel_eligibility_ref: str,
        suppression_check_ref: str,
        suppression_clear: bool,
        claim_evidence_refs: list[str],
        sender_identity_ref: str,
        opt_out_mechanism_ref: str,
        risk_class: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"],
        exact_scope: str,
        expires_at: str,
        provider: str,
        idempotency_key: str,
    ) -> dict[str, Any]:
        """
        Build an ExternalActionPacket dict for the canonical external_execution_gate.

        Caller must resolve canonical authority via CanonicalAuthorityResolver
        and evaluate via evaluate_resolved_external_action before any provider effect.
        """
        from dealix.commercial.external_execution_gate import (
            build_external_action_packet,
            canonical_content_sha256,
        )

        packet = build_external_action_packet(
            action_id=task.task_id,
            action_class=action_class,
            purpose_class=purpose_class,
            destination=task.recipient,
            channel=task.channel,
            environment="production",
            artifact_ref=artifact_ref,
            content_sha256=content_sha256 or canonical_content_sha256(
                destination=task.recipient,
                subject=task.subject,
                body=task.body_ar if task.channel in {"email", "whatsapp"} else task.body_en,
            ),
            identity_or_relationship_ref=identity_or_relationship_ref,
            consent_or_channel_eligibility_ref=consent_or_channel_eligibility_ref,
            suppression_check_ref=suppression_check_ref,
            suppression_clear=suppression_clear,
            claim_evidence_refs=claim_evidence_refs,
            sender_identity_ref=sender_identity_ref,
            opt_out_mechanism_ref=opt_out_mechanism_ref,
            risk_class=risk_class,
            exact_scope=exact_scope,
            expires_at=expires_at,
            provider=provider,
            idempotency_key=idempotency_key,
        )
        return packet.model_dump()

    def automate_social(self, *, site_readiness_ref: str | None = None) -> dict[str, Any]:
        """
        Report social preparation capability and provider readiness — never fully automated live publish.

        Returns draft/preparation status only. Live publish requires:
        - Evidenced SiteReadinessEvidence with social_ready=True
        - Canonical ExternalActionPacket with action_class=COMPANY_SOCIAL_PUBLISH
        - Resolved authority via CanonicalAuthorityResolver
        - evaluate_resolved_external_action verdict=READY_FOR_PROVIDER_EXECUTION
        """
        return {
            "platforms": ["linkedin", "x", "instagram", "tiktok", "youtube", "facebook"],
            "automated": False,
            "preparation_capable": True,
            "draft_only": True,
            "provider_readiness": {
                "linkedin": "unknown",
                "x": "unknown",
                "instagram": "unknown",
                "tiktok": "unknown",
                "youtube": "unknown",
                "facebook": "unknown",
            },
            "site_ready": False,
            "site_readiness_ref": site_readiness_ref or "NOT_PROVIDED",
            "channels": 0,
            "requires": [
                "Evidenced SiteReadinessEvidence with social_ready=True",
                "Canonical ExternalActionPacket for COMPANY_SOCIAL_PUBLISH",
                "Resolved authority via CanonicalAuthorityResolver",
                "evaluate_resolved_external_action verdict=READY_FOR_PROVIDER_EXECUTION",
            ],
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "social_platforms": 6,
            "site_ready": False,
            "requires_evidence": True,
        }


__all__ = [
    "CommunicationNegotiationEngine",
    "CommunicationTask",
    "NegotiationState",
    "UNKNOWN",
    "SenderIdentityEvidence",
    "SiteReadinessEvidence",
]