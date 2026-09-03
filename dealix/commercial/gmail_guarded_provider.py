"""Quarantined Gmail provider surface for Dealix.

The previous implementation accepted authority and idempotency dependencies from
the action caller. That is not a trust boundary: a caller could fabricate both.
Until the EXISTING canonical Governance/Approval owner exposes a provider-owned,
trusted current-state adapter, the public Gmail execution surface is deliberately
non-executable.

Research, drafting, reply classification and negotiation remain available; this
module cannot create a customer-facing side effect in the quarantined state.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

from dealix.commercial.external_execution_gate import ExternalActionPacket, canonical_content_sha256

GMAIL_SEND_SCOPE = "https://www.googleapis.com/auth/gmail.send"
QUARANTINE_REASON = "LIVE_PROVIDER_QUARANTINED_CANONICAL_PROVIDER_DEPENDENCIES_NOT_WIRED"


class GmailArtifact(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    to: str = Field(..., min_length=3)
    subject: str = Field(..., min_length=1)
    body_text: str = Field(..., min_length=1)

    @field_validator("to")
    @classmethod
    def _emailish(cls, value: str) -> str:
        text = value.strip()
        if "@" not in text or text.startswith("@") or text.endswith("@"):
            raise ValueError("to must be an email-like destination")
        return text

    @property
    def content_sha256(self) -> str:
        return canonical_content_sha256(destination=str(self.to), subject=self.subject, body=self.body_text)


class ProviderReceipt(BaseModel):
    """Schema retained for reconciliation/future provider-owned integration."""

    model_config = ConfigDict(extra="forbid", frozen=True)
    provider: str = "gmail_api"
    action_hash: str
    packet_integrity_sha256: str
    idempotency_key: str
    status: str
    provider_message_id: str = ""
    provider_thread_id: str = ""
    executed_at: str
    destination_sha256: str
    body_or_subject_logged: bool = False
    replayed_from_ledger: bool = False


def send_approved_gmail_message(artifact: GmailArtifact, *, packet: ExternalActionPacket) -> ProviderReceipt:
    """Fail closed until canonical provider-owned dependencies are wired.

    This function intentionally accepts NO resolver, approval snapshot, runtime
    switches, idempotency ledger, service object or token file from the action
    caller. That prevents caller-controlled dependency injection from becoming a
    false-authority path.
    """
    if packet.action_class not in {"EMAIL_SEND", "CUSTOMER_QUOTE_SEND", "CONTRACT_COMMITMENT"}:
        raise PermissionError("Gmail provider only handles email-class actions")
    if packet.provider != "gmail_api":
        raise PermissionError("packet provider does not match gmail_api")
    if packet.destination.strip().lower() != str(artifact.to).strip().lower():
        raise PermissionError("destination changed after packet construction")
    if packet.content_sha256 != artifact.content_sha256:
        raise PermissionError("message content changed after packet construction")
    raise PermissionError(QUARANTINE_REASON)


__all__ = ["GMAIL_SEND_SCOPE", "QUARANTINE_REASON", "GmailArtifact", "ProviderReceipt", "send_approved_gmail_message"]
