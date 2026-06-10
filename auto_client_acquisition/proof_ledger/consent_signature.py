"""Consent signature workflow for Proof Pack publication.

A `ConsentSignature` is a deterministic record that the customer
agreed to publish a proof event publicly (case study, social, etc.).

Hard rules:
- consent must be SIGNED (not just requested) before publish
- consent has scope (one event, one pack, or all-future)
- document_hash makes the consent tied to a specific narrative
- once signed, immutable (only revoke = create new revocation record)

Persistence: JSONL append-only (data/consent_signatures.jsonl).
"""
from __future__ import annotations

import hashlib
import json
import os
import uuid
from datetime import UTC, datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

ConsentScope = Literal["single_event", "single_pack", "all_future"]
ConsentStatus = Literal["requested", "signed", "declined", "revoked"]

_JSONL_PATH = os.path.join("data", "consent_signatures.jsonl")
_INDEX: dict[str, ConsentSignature] = {}


class ConsentSignature(BaseModel):
    model_config = ConfigDict(extra="forbid")

    signature_id: str
    customer_handle: str
    scope: ConsentScope
    target_event_ids: list[str] = Field(default_factory=list)
    target_pack_id: str | None = None
    document_hash: str  # sha256 of the narrative being consented to
    signed_by: str | None = None  # name/title of customer signer
    status: ConsentStatus = "requested"
    requested_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    signed_at: datetime | None = None
    safety_summary: str = "no_publish_without_signed_status"


def _ensure_dir() -> None:
    os.makedirs(os.path.dirname(_JSONL_PATH), exist_ok=True)


def _persist(sig: ConsentSignature) -> None:
    _ensure_dir()
    _INDEX[sig.signature_id] = sig
    with open(_JSONL_PATH, "a", encoding="utf-8") as f:
        f.write(sig.model_dump_json() + "\n")


def hash_document(narrative: str) -> str:
    return hashlib.sha256(narrative.encode("utf-8")).hexdigest()


def request_consent(
    *,
    customer_handle: str,
    scope: ConsentScope,
    narrative: str,
    target_event_ids: list[str] | None = None,
    target_pack_id: str | None = None,
) -> ConsentSignature:
    sig = ConsentSignature(
        signature_id=f"sig_{uuid.uuid4().hex[:10]}",
        customer_handle=customer_handle,
        scope=scope,
        target_event_ids=target_event_ids or [],
        target_pack_id=target_pack_id,
        document_hash=hash_document(narrative),
        status="requested",
    )
    _persist(sig)
    return sig


def record_signature(
    *,
    signature_id: str,
    signed_by: str,
    confirmed_document_hash: str,
) -> ConsentSignature:
    """Record the customer's signature.

    Hard check: confirmed_document_hash MUST match the original
    document_hash. This prevents a signature for narrative A being
    re-used to publish narrative B.
    """
    sig = _INDEX.get(signature_id)
    if sig is None:
        raise ValueError(f"signature {signature_id} not found")
    if sig.status != "requested":
        raise ValueError(f"signature {signature_id} is {sig.status}; cannot re-sign")
    if confirmed_document_hash != sig.document_hash:
        raise ValueError("document_hash mismatch — cannot sign different narrative")
    sig.signed_by = signed_by
    sig.status = "signed"
    sig.signed_at = datetime.now(UTC)
    _persist(sig)
    return sig


def decline(*, signature_id: str, declined_by: str) -> ConsentSignature:
    sig = _INDEX.get(signature_id)
    if sig is None:
        raise ValueError(f"signature {signature_id} not found")
    if sig.status != "requested":
        raise ValueError(f"signature {signature_id} is {sig.status}; cannot decline")
    sig.status = "declined"
    sig.signed_by = declined_by
    sig.signed_at = datetime.now(UTC)
    _persist(sig)
    return sig


def revoke(*, signature_id: str, revoked_by: str) -> ConsentSignature:
    sig = _INDEX.get(signature_id)
    if sig is None:
        raise ValueError(f"signature {signature_id} not found")
    if sig.status != "signed":
        raise ValueError("only signed consents can be revoked")
    sig.status = "revoked"
    sig.signed_by = revoked_by
    sig.signed_at = datetime.now(UTC)
    _persist(sig)
    return sig


def get_signature(signature_id: str) -> ConsentSignature | None:
    return _INDEX.get(signature_id)


def is_consent_valid(*, signature_id: str, narrative: str) -> bool:
    """True if the signature is signed AND its hash matches the narrative."""
    sig = _INDEX.get(signature_id)
    if sig is None:
        return False
    if sig.status != "signed":
        return False
    return sig.document_hash == hash_document(narrative)
