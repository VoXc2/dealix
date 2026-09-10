"""Bounded founder-delegation policy for Dealix external conversations.

A delegation session is not a permanent L5 bypass. It is a finite policy envelope
that may make an exact external action eligible for the canonical Approval
Authority to mint an action-bound approval. The existing external execution gate
remains the provider boundary.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from dealix.commercial.external_execution_gate import ExternalActionPacket

DelegationVerdict = Literal[
    "ELIGIBLE_FOR_ACTION_BOUND_APPROVAL",
    "BLOCKED",
]

_ALLOWED_DELEGATED_ACTIONS = {
    "EMAIL_SEND",
    "WHATSAPP_SEND",
}
_ALLOWED_DELEGATED_PURPOSES = {
    "INBOUND_REPLY",
    "REQUESTED_FOLLOWUP",
    "TRANSACTIONAL",
}


def _as_utc(value: str, *, field: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include timezone")
    return parsed.astimezone(UTC)


class FounderDelegationSession(BaseModel):
    """Finite authority policy for a known conversation/recipient set.

    The session never executes a provider call itself. Each message still needs
    its own canonical action hash and current Approval Authority resolution.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["dealix.founder-delegation.v1"] = "dealix.founder-delegation.v1"
    session_id: str = Field(..., min_length=1)
    founder_identity_ref: str = Field(..., min_length=1)
    canonical_approval_ref: str = Field(..., min_length=1)
    channel: str = Field(..., min_length=1)
    provider: str = Field(..., min_length=1)
    conversation_ids: list[str] = Field(default_factory=list)
    recipients: list[str] = Field(default_factory=list)
    allowed_purpose_classes: list[str] = Field(default_factory=list)
    allowed_action_classes: list[str] = Field(default_factory=list)
    sender_persona: Literal["Dealix Founder Office"] = "Dealix Founder Office"
    starts_at: str = Field(..., min_length=1)
    expires_at: str = Field(..., min_length=1)
    max_messages: int = Field(default=20, ge=1, le=200)
    max_calls: int = Field(default=0, ge=0, le=50)
    max_discount_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    binding_quote_allowed: bool = False
    contract_commitment_allowed: bool = False
    payment_or_refund_allowed: bool = False
    public_publish_allowed: bool = False
    paid_spend_allowed: bool = False
    automated_voice: bool = False
    automated_identity_disclosure: str = ""
    consent_or_channel_eligibility_ref: str = Field(..., min_length=1)
    suppression_check_ref: str = Field(..., min_length=1)
    revoked: bool = False

    @field_validator("starts_at", "expires_at")
    @classmethod
    def _timestamp(cls, value: str) -> str:
        _as_utc(value, field="delegation timestamp")
        return value

    @field_validator("conversation_ids", "recipients", "allowed_purpose_classes", "allowed_action_classes")
    @classmethod
    def _nonblank_list(cls, value: list[str]) -> list[str]:
        cleaned = [str(item).strip() for item in value if str(item).strip()]
        if len(cleaned) != len(value):
            raise ValueError("delegation list fields cannot contain blanks")
        return cleaned


class DelegationUsage(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    messages_committed: int = Field(default=0, ge=0)
    calls_committed: int = Field(default=0, ge=0)


class DelegationDecision(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    verdict: DelegationVerdict
    session_id: str
    action_hash: str
    reasons: list[str]
    approval_minting_allowed: bool
    provider_execution_allowed: Literal[False] = False


def evaluate_founder_delegation(
    *,
    session: FounderDelegationSession,
    packet: ExternalActionPacket,
    usage: DelegationUsage,
    now: datetime | None = None,
    conversation_id: str = "",
) -> DelegationDecision:
    """Check whether a packet fits the founder's finite delegation envelope.

    A PASS means only that the canonical approval owner may mint/re-resolve the
    exact packet action hash. Provider execution is deliberately always False
    here; the existing external execution gate owns that decision.
    """

    current = (now or datetime.now(UTC)).astimezone(UTC)
    reasons: list[str] = []

    if session.revoked:
        reasons.append("delegation session is revoked")
    if current < _as_utc(session.starts_at, field="starts_at"):
        reasons.append("delegation session has not started")
    if current >= _as_utc(session.expires_at, field="expires_at"):
        reasons.append("delegation session is expired")
    if packet.channel != session.channel:
        reasons.append("channel is outside delegated scope")
    if packet.provider != session.provider:
        reasons.append("provider is outside delegated scope")
    if session.recipients and packet.destination not in set(session.recipients):
        reasons.append("recipient is outside delegated scope")
    if session.conversation_ids and conversation_id not in set(session.conversation_ids):
        reasons.append("conversation is outside delegated scope")
    if packet.action_class not in set(session.allowed_action_classes):
        reasons.append("action class is outside delegated scope")
    if packet.purpose_class not in set(session.allowed_purpose_classes):
        reasons.append("purpose class is outside delegated scope")
    if packet.action_class not in _ALLOWED_DELEGATED_ACTIONS:
        reasons.append("action class is not delegatable by V1")
    if packet.purpose_class not in _ALLOWED_DELEGATED_PURPOSES:
        reasons.append("purpose class is not delegatable by V1")
    if usage.messages_committed >= session.max_messages:
        reasons.append("delegated message budget exhausted")
    if not packet.suppression_clear:
        reasons.append("suppression state is not clear")
    if not packet.consent_or_channel_eligibility_ref:
        reasons.append("channel eligibility evidence is missing")
    if packet.consent_or_channel_eligibility_ref != session.consent_or_channel_eligibility_ref:
        reasons.append("channel eligibility evidence differs from delegated scope")
    if packet.suppression_check_ref != session.suppression_check_ref:
        reasons.append("suppression evidence differs from delegated scope")

    # Permanent exclusions. A conversation delegation cannot silently grow into
    # commercial/legal/financial/public authority.
    if session.binding_quote_allowed:
        reasons.append("binding quote delegation is not supported by V1")
    if session.contract_commitment_allowed:
        reasons.append("contract commitment delegation is not supported by V1")
    if session.payment_or_refund_allowed:
        reasons.append("payment/refund delegation is not supported by V1")
    if session.public_publish_allowed:
        reasons.append("public publish delegation is not supported by V1")
    if session.paid_spend_allowed:
        reasons.append("paid spend delegation is not supported by V1")

    if session.automated_voice and not session.automated_identity_disclosure.strip():
        reasons.append("automated voice requires identity disclosure")

    eligible = not reasons
    return DelegationDecision(
        verdict="ELIGIBLE_FOR_ACTION_BOUND_APPROVAL" if eligible else "BLOCKED",
        session_id=session.session_id,
        action_hash=packet.action_hash,
        reasons=reasons,
        approval_minting_allowed=eligible,
        provider_execution_allowed=False,
    )
