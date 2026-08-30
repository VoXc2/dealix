"""Guarded Gmail sender for *already approved* exact Dealix action packets.

The module does not create approval.  It verifies the exact packet again,
verifies the message hash, checks the effective runtime switches, then calls the
Gmail API once with an idempotency-controlled action owned by the caller.
"""
from __future__ import annotations

import base64
from datetime import UTC, datetime
from email.message import EmailMessage
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from dealix.commercial.external_execution_gate import (
    ApprovalEnvelope,
    ExternalActionPacket,
    RuntimeAuthority,
    canonical_content_sha256,
    evaluate_external_action,
)

GMAIL_SEND_SCOPE = "https://www.googleapis.com/auth/gmail.send"


class GmailArtifact(BaseModel):
    model_config = ConfigDict(extra="forbid")

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
    model_config = ConfigDict(extra="forbid")

    provider: str = "gmail_api"
    action_fingerprint: str
    idempotency_key: str
    status: str
    provider_message_id: str = ""
    provider_thread_id: str = ""
    executed_at: str
    destination_sha256: str
    body_or_subject_logged: bool = False


def _build_service(token_file: str) -> Any:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    credentials = Credentials.from_authorized_user_file(token_file, scopes=[GMAIL_SEND_SCOPE])
    return build("gmail", "v1", credentials=credentials, cache_discovery=False)


def send_approved_gmail_message(
    artifact: GmailArtifact,
    *,
    packet: ExternalActionPacket,
    approval: ApprovalEnvelope,
    runtime: RuntimeAuthority,
    service: Any | None = None,
    token_file: str | None = None,
) -> ProviderReceipt:
    decision = evaluate_external_action(packet, approval=approval, runtime=runtime)
    if not decision.provider_execution_allowed:
        raise PermissionError(f"external action not executable: {decision.verdict}:{','.join(decision.reasons)}")
    if packet.action_class not in {"EMAIL_SEND", "CUSTOMER_QUOTE_SEND", "CONTRACT_COMMITMENT"}:
        raise PermissionError("Gmail provider only handles approved email-class actions")
    if packet.provider != "gmail_api":
        raise PermissionError("packet provider does not match gmail_api")
    if packet.destination.strip().lower() != str(artifact.to).strip().lower():
        raise PermissionError("destination changed after approval")
    if packet.content_sha256 != artifact.content_sha256:
        raise PermissionError("message content changed after approval")

    gmail = service
    if gmail is None:
        if not token_file:
            raise PermissionError("Gmail token file is required outside test injection")
        gmail = _build_service(token_file)

    message = EmailMessage()
    message["To"] = str(artifact.to)
    message["Subject"] = artifact.subject
    message.set_content(artifact.body_text)
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("ascii")
    result = gmail.users().messages().send(userId="me", body={"raw": raw}).execute()

    import hashlib

    return ProviderReceipt(
        action_fingerprint=packet.action_fingerprint,
        idempotency_key=packet.idempotency_key,
        status="PROVIDER_ACCEPTED_SEND_REQUEST",
        provider_message_id=str(result.get("id", "")),
        provider_thread_id=str(result.get("threadId", "")),
        executed_at=datetime.now(UTC).isoformat(),
        destination_sha256=hashlib.sha256(str(artifact.to).strip().lower().encode("utf-8")).hexdigest(),
    )


__all__ = ["GMAIL_SEND_SCOPE", "GmailArtifact", "ProviderReceipt", "send_approved_gmail_message"]
