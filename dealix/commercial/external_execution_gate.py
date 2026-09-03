"""Fail-closed authority primitives for Dealix L5 commercial side effects.

Packet integrity and approval identity are intentionally separate:
- packet_integrity_sha256: full SHA-256 over every serialized packet field;
- action_hash: repository-wide L5 ACTION_HASH from AGENTS.md:
  sha256(action_type|target|environment|payload)[0:16].

Caller-supplied approval/runtime projections never grant provider authority.
"""
from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Literal, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field, field_validator

ActionClass = Literal[
    "EMAIL_SEND",
    "WHATSAPP_SEND",
    "COMPANY_SOCIAL_PUBLISH",
    "CUSTOMER_QUOTE_SEND",
    "TENDER_SUBMISSION",
    "CONTRACT_COMMITMENT",
    "PAYMENT",
    "REFUND",
    "FOUNDER_LINKEDIN_MANUAL",
]
PurposeClass = Literal[
    "DIRECT_MARKETING",
    "INBOUND_REPLY",
    "REQUESTED_FOLLOWUP",
    "TRANSACTIONAL",
    "CUSTOMER_QUOTE",
    "TENDER_SUBMISSION",
    "PUBLIC_PUBLISH",
    "CONTRACT",
    "PAYMENT",
    "REFUND",
]
ApprovalState = Literal["PENDING", "APPROVED", "REVOKED", "EXPIRED", "UNKNOWN"]
RiskClass = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"
SCHEMA = "dealix.external-action-packet.v2"
ACTION_HASH_LEN = 16
DEFAULT_AUTHORITY_MAX_AGE_SECONDS = 30


def _aware(value: str, *, field: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"{field} must be ISO-8601") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include timezone")
    return parsed.astimezone(UTC)


def _refs(values: list[str], *, field: str) -> list[str]:
    cleaned = [str(value).strip() for value in values if str(value).strip()]
    if len(cleaned) != len(values):
        raise ValueError(f"{field} cannot contain blank references")
    if not cleaned:
        raise ValueError(f"{field} requires evidence")
    return cleaned


def _sha256_hex(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def canonical_content_sha256(*, destination: str, subject: str, body: str) -> str:
    payload = json.dumps(
        {"destination": destination.strip(), "subject": subject, "body": body},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return _sha256_hex(payload)


def canonical_action_hash(*, action_type: str, target: str, environment: str, payload: str) -> str:
    return _sha256_hex(f"{action_type}|{target}|{environment}|{payload}")[:ACTION_HASH_LEN]


def _canonical_json(value: dict[str, object]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _packet_material_dict(
    *,
    schema_version: str,
    action_id: str,
    action_class: ActionClass,
    purpose_class: PurposeClass,
    destination: str,
    channel: str,
    environment: str,
    artifact_ref: str,
    content_sha256: str,
    identity_or_relationship_ref: str,
    consent_or_channel_eligibility_ref: str,
    suppression_check_ref: str,
    suppression_clear: bool,
    claim_evidence_refs: list[str],
    sender_identity_ref: str,
    opt_out_mechanism_ref: str,
    risk_class: RiskClass,
    exact_scope: str,
    expires_at: str,
    provider: str,
    idempotency_key: str,
) -> dict[str, object]:
    return {
        "schema_version": schema_version.strip(),
        "action_id": action_id.strip(),
        "action_class": action_class,
        "purpose_class": purpose_class,
        "destination": destination.strip(),
        "channel": channel.strip(),
        "environment": environment.strip(),
        "artifact_ref": artifact_ref.strip(),
        "content_sha256": content_sha256.strip().lower(),
        "identity_or_relationship_ref": identity_or_relationship_ref.strip(),
        "consent_or_channel_eligibility_ref": consent_or_channel_eligibility_ref.strip(),
        "suppression_check_ref": suppression_check_ref.strip(),
        "suppression_clear": bool(suppression_clear),
        "claim_evidence_refs": sorted(_refs(claim_evidence_refs, field="claim_evidence_refs")),
        "sender_identity_ref": sender_identity_ref.strip(),
        "opt_out_mechanism_ref": opt_out_mechanism_ref.strip(),
        "risk_class": risk_class,
        "exact_scope": exact_scope.strip(),
        "expires_at": expires_at.strip(),
        "provider": provider.strip(),
        "idempotency_key": idempotency_key.strip(),
    }


def _action_payload(material: dict[str, object]) -> str:
    payload = dict(material)
    payload.pop("action_class", None)
    payload.pop("destination", None)
    payload.pop("environment", None)
    return _canonical_json(payload)


class RuntimeAuthority(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    external_send: bool = False
    public_publish: bool = False
    named_quote: bool = False
    tender_submission: bool = False
    legal_commitment: bool = False
    payment_or_refund: bool = False
    connector_write: bool = False


class ExternalActionPacket(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["dealix.external-action-packet.v2"] = SCHEMA
    action_id: str = Field(..., min_length=1)
    action_class: ActionClass
    purpose_class: PurposeClass
    destination: str = Field(..., min_length=1)
    channel: str = Field(..., min_length=1)
    environment: str = Field(..., min_length=1)
    artifact_ref: str = Field(..., min_length=1)
    content_sha256: str = Field(..., min_length=64, max_length=64)
    identity_or_relationship_ref: str = ""
    consent_or_channel_eligibility_ref: str = ""
    suppression_check_ref: str = Field(..., min_length=1)
    suppression_clear: bool = False
    claim_evidence_refs: list[str] = Field(default_factory=list)
    sender_identity_ref: str = Field(..., min_length=1)
    opt_out_mechanism_ref: str = ""
    risk_class: RiskClass = "MEDIUM"
    exact_scope: str = Field(..., min_length=1)
    expires_at: str = Field(..., min_length=1)
    provider: str = Field(..., min_length=1)
    idempotency_key: str = Field(..., min_length=1)
    packet_integrity_sha256: str = Field(..., min_length=64, max_length=64)
    action_hash: str = Field(..., min_length=ACTION_HASH_LEN, max_length=ACTION_HASH_LEN)

    @field_validator("content_sha256", "packet_integrity_sha256")
    @classmethod
    def _hex64(cls, value: str) -> str:
        text = value.strip().lower()
        if len(text) != 64 or any(ch not in "0123456789abcdef" for ch in text):
            raise ValueError("must be a 64-character lowercase SHA-256 hex digest")
        return text

    @field_validator("action_hash")
    @classmethod
    def _hex16(cls, value: str) -> str:
        text = value.strip().lower()
        if len(text) != ACTION_HASH_LEN or any(ch not in "0123456789abcdef" for ch in text):
            raise ValueError("action_hash must be the canonical 16-character lowercase hash")
        return text

    @field_validator("expires_at")
    @classmethod
    def _timestamp(cls, value: str) -> str:
        _aware(value, field="packet.expires_at")
        return value


class ApprovalEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    approval_id: str = Field(..., min_length=1)
    action_hash: str = Field(..., min_length=ACTION_HASH_LEN, max_length=ACTION_HASH_LEN)
    exact_scope: str = Field(..., min_length=1)
    authority_class: str = Field(..., min_length=1)
    approval_state: ApprovalState
    approval_state_ref: str = Field(..., min_length=1)
    state_checked_at: str = Field(..., min_length=1)
    expires_at: str = Field(..., min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)

    @field_validator("action_hash")
    @classmethod
    def _hash(cls, value: str) -> str:
        text = value.strip().lower()
        if len(text) != ACTION_HASH_LEN or any(ch not in "0123456789abcdef" for ch in text):
            raise ValueError("approval action_hash must match canonical ACTION_HASH")
        return text

    @field_validator("evidence_refs")
    @classmethod
    def _evidence(cls, value: list[str]) -> list[str]:
        return _refs(value, field="approval.evidence_refs")

    @field_validator("state_checked_at", "expires_at")
    @classmethod
    def _approval_timestamp(cls, value: str) -> str:
        _aware(value, field="approval timestamp")
        return value


class ResolvedAuthoritySnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    source_ref: str = Field(..., min_length=1)
    resolved_at: str = Field(..., min_length=1)
    approval: ApprovalEnvelope
    runtime: RuntimeAuthority
    identity_or_relationship_ref: str = ""
    consent_or_channel_eligibility_ref: str = ""
    suppression_check_ref: str = Field(..., min_length=1)
    suppression_clear: bool = False
    claim_evidence_refs: list[str] = Field(default_factory=list)
    sender_identity_ref: str = Field(..., min_length=1)
    opt_out_mechanism_ref: str = ""

    @field_validator("resolved_at")
    @classmethod
    def _resolved_timestamp(cls, value: str) -> str:
        _aware(value, field="authority.resolved_at")
        return value


@runtime_checkable
class CanonicalAuthorityResolver(Protocol):
    def resolve_current(self, packet: ExternalActionPacket) -> ResolvedAuthoritySnapshot: ...


class ExecutionDecision(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    verdict: str
    action_hash: str
    packet_integrity_sha256: str
    provider_execution_allowed: bool
    approval_valid: bool
    runtime_authority_pass: bool
    canonical_authority_fresh: bool
    reasons: list[str]
    required_next_action: str


def build_external_action_packet(
    *,
    action_id: str,
    action_class: ActionClass,
    purpose_class: PurposeClass,
    destination: str,
    channel: str,
    environment: str,
    artifact_ref: str,
    content_sha256: str,
    identity_or_relationship_ref: str = "",
    consent_or_channel_eligibility_ref: str = "",
    suppression_check_ref: str,
    suppression_clear: bool,
    claim_evidence_refs: list[str],
    sender_identity_ref: str,
    opt_out_mechanism_ref: str = "",
    risk_class: RiskClass = "MEDIUM",
    exact_scope: str,
    expires_at: str,
    provider: str,
    idempotency_key: str,
) -> ExternalActionPacket:
    material = _packet_material_dict(
        schema_version=SCHEMA,
        action_id=action_id,
        action_class=action_class,
        purpose_class=purpose_class,
        destination=destination,
        channel=channel,
        environment=environment,
        artifact_ref=artifact_ref,
        content_sha256=content_sha256,
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
    integrity = _sha256_hex(_canonical_json(material))
    action_hash = canonical_action_hash(
        action_type=action_class,
        target=str(material["destination"]),
        environment=str(material["environment"]),
        payload=_action_payload(material),
    )
    return ExternalActionPacket(**material, packet_integrity_sha256=integrity, action_hash=action_hash)


def _material_from_packet(packet: ExternalActionPacket) -> dict[str, object]:
    return _packet_material_dict(
        schema_version=packet.schema_version,
        action_id=packet.action_id,
        action_class=packet.action_class,
        purpose_class=packet.purpose_class,
        destination=packet.destination,
        channel=packet.channel,
        environment=packet.environment,
        artifact_ref=packet.artifact_ref,
        content_sha256=packet.content_sha256,
        identity_or_relationship_ref=packet.identity_or_relationship_ref,
        consent_or_channel_eligibility_ref=packet.consent_or_channel_eligibility_ref,
        suppression_check_ref=packet.suppression_check_ref,
        suppression_clear=packet.suppression_clear,
        claim_evidence_refs=list(packet.claim_evidence_refs),
        sender_identity_ref=packet.sender_identity_ref,
        opt_out_mechanism_ref=packet.opt_out_mechanism_ref,
        risk_class=packet.risk_class,
        exact_scope=packet.exact_scope,
        expires_at=packet.expires_at,
        provider=packet.provider,
        idempotency_key=packet.idempotency_key,
    )


def recompute_packet_integrity(packet: ExternalActionPacket) -> str:
    return _sha256_hex(_canonical_json(_material_from_packet(packet)))


def recompute_action_hash(packet: ExternalActionPacket) -> str:
    material = _material_from_packet(packet)
    return canonical_action_hash(
        action_type=packet.action_class,
        target=packet.destination,
        environment=packet.environment,
        payload=_action_payload(material),
    )


def _required_runtime_switches(action_class: ActionClass) -> tuple[str, ...]:
    return {
        "EMAIL_SEND": ("external_send", "connector_write"),
        "WHATSAPP_SEND": ("external_send", "connector_write"),
        "COMPANY_SOCIAL_PUBLISH": ("public_publish", "connector_write"),
        "CUSTOMER_QUOTE_SEND": ("external_send", "named_quote", "connector_write"),
        "TENDER_SUBMISSION": ("tender_submission", "connector_write"),
        "CONTRACT_COMMITMENT": ("legal_commitment", "external_send", "connector_write"),
        "PAYMENT": ("payment_or_refund", "connector_write"),
        "REFUND": ("payment_or_refund", "connector_write"),
        "FOUNDER_LINKEDIN_MANUAL": (),
    }[action_class]


def _packet_integrity_reasons(packet: ExternalActionPacket) -> list[str]:
    reasons: list[str] = []
    if packet.schema_version != SCHEMA:
        reasons.append("UNSUPPORTED_PACKET_SCHEMA")
    if recompute_packet_integrity(packet) != packet.packet_integrity_sha256:
        reasons.append("PACKET_INTEGRITY_MISMATCH")
    if recompute_action_hash(packet) != packet.action_hash:
        reasons.append("ACTION_HASH_MISMATCH")
    return reasons


def _evidence_matches(packet: ExternalActionPacket, authority: ResolvedAuthoritySnapshot) -> list[str]:
    reasons: list[str] = []
    comparisons = (
        (packet.identity_or_relationship_ref, authority.identity_or_relationship_ref, "IDENTITY_OR_RELATIONSHIP"),
        (packet.consent_or_channel_eligibility_ref, authority.consent_or_channel_eligibility_ref, "CONSENT_OR_CHANNEL_ELIGIBILITY"),
        (packet.suppression_check_ref, authority.suppression_check_ref, "SUPPRESSION_CHECK"),
        (packet.sender_identity_ref, authority.sender_identity_ref, "SENDER_IDENTITY"),
        (packet.opt_out_mechanism_ref, authority.opt_out_mechanism_ref, "OPT_OUT_MECHANISM"),
    )
    for expected, actual, label in comparisons:
        if expected.strip() != actual.strip():
            reasons.append(f"FRESH_{label}_MISMATCH")
    if sorted(packet.claim_evidence_refs) != sorted(authority.claim_evidence_refs):
        reasons.append("FRESH_CLAIM_EVIDENCE_MISMATCH")
    if packet.suppression_clear != authority.suppression_clear:
        reasons.append("FRESH_SUPPRESSION_STATE_MISMATCH")
    return reasons


def evaluate_external_action(
    packet: ExternalActionPacket,
    *,
    approval: ApprovalEnvelope | None = None,
    runtime: RuntimeAuthority | None = None,
    evaluated_at: str | None = None,
) -> ExecutionDecision:
    # The evaluator uses the trusted process clock. Keep the legacy argument
    # for compatibility, but never let a caller choose the validation time.
    del approval, runtime, evaluated_at
    now = datetime.now(UTC)
    reasons = _packet_integrity_reasons(packet)
    if _aware(packet.expires_at, field="packet.expires_at") <= now:
        reasons.append("PACKET_EXPIRED")
    reasons.append("CANONICAL_FRESH_AUTHORITY_NOT_RESOLVED")
    return ExecutionDecision(
        verdict="HOLD_CANONICAL_AUTHORITY_REQUIRED",
        action_hash=packet.action_hash,
        packet_integrity_sha256=packet.packet_integrity_sha256,
        provider_execution_allowed=False,
        approval_valid=False,
        runtime_authority_pass=False,
        canonical_authority_fresh=False,
        reasons=reasons,
        required_next_action="RESOLVE_CANONICAL_AUTHORITY_IMMEDIATELY_BEFORE_PROVIDER_EFFECT",
    )


def evaluate_resolved_external_action(
    packet: ExternalActionPacket,
    *,
    authority: ResolvedAuthoritySnapshot,
    evaluated_at: str | None = None,
    max_authority_age_seconds: int = DEFAULT_AUTHORITY_MAX_AGE_SECONDS,
) -> ExecutionDecision:
    # Freshness is authority-owned: caller-provided clock and age overrides
    # are intentionally ignored at the provider trust boundary.
    del evaluated_at, max_authority_age_seconds
    now = datetime.now(UTC)
    reasons = _packet_integrity_reasons(packet)

    if packet.action_class == "FOUNDER_LINKEDIN_MANUAL":
        return ExecutionDecision(
            verdict="MANUAL_NATIVE_ONLY",
            action_hash=packet.action_hash,
            packet_integrity_sha256=packet.packet_integrity_sha256,
            provider_execution_allowed=False,
            approval_valid=False,
            runtime_authority_pass=False,
            canonical_authority_fresh=False,
            reasons=[*reasons, "PERSONAL_LINKEDIN_AUTOMATION_BLOCKED"],
            required_next_action="FOUNDER_MANUAL_NATIVE",
        )

    if _aware(packet.expires_at, field="packet.expires_at") <= now:
        reasons.append("PACKET_EXPIRED")

    resolved_at = _aware(authority.resolved_at, field="authority.resolved_at")
    age = (now - resolved_at).total_seconds()
    canonical_fresh = 0 <= age <= DEFAULT_AUTHORITY_MAX_AGE_SECONDS
    if age < 0:
        reasons.append("AUTHORITY_RESOLVED_IN_FUTURE")
    elif age > DEFAULT_AUTHORITY_MAX_AGE_SECONDS:
        reasons.append("CANONICAL_AUTHORITY_STALE")

    reasons.extend(_evidence_matches(packet, authority))
    if not authority.source_ref.strip():
        reasons.append("CANONICAL_AUTHORITY_SOURCE_MISSING")
    if not authority.suppression_clear:
        reasons.append("SUPPRESSED_OR_SUPPRESSION_NOT_PROVEN_CLEAR")
    if not authority.suppression_check_ref.strip():
        reasons.append("MISSING_FRESH_SUPPRESSION_CHECK_REF")
    if not authority.sender_identity_ref.strip():
        reasons.append("MISSING_FRESH_SENDER_IDENTITY_REF")
    if not authority.claim_evidence_refs:
        reasons.append("MISSING_FRESH_CLAIM_EVIDENCE_REFS")

    is_message = packet.action_class in {"EMAIL_SEND", "WHATSAPP_SEND", "CUSTOMER_QUOTE_SEND", "CONTRACT_COMMITMENT"}
    if is_message and not authority.identity_or_relationship_ref.strip():
        reasons.append("MISSING_FRESH_IDENTITY_OR_RELATIONSHIP_REF")
    if packet.purpose_class == "DIRECT_MARKETING":
        if not authority.consent_or_channel_eligibility_ref.strip():
            reasons.append("DIRECT_MARKETING_CONSENT_NOT_PROVEN_FRESH")
        if not authority.opt_out_mechanism_ref.strip():
            reasons.append("DIRECT_MARKETING_OPT_OUT_NOT_PROVEN_FRESH")
    if packet.action_class == "WHATSAPP_SEND" and not authority.consent_or_channel_eligibility_ref.strip():
        reasons.append("WHATSAPP_FRESH_CONSENT_OR_INBOUND_BASIS_NOT_PROVEN")

    approval = authority.approval
    approval_valid = True
    checked = _aware(approval.state_checked_at, field="approval.state_checked_at")
    approval_expiry = _aware(approval.expires_at, field="approval.expires_at")
    approval_state_age = (now - checked).total_seconds()
    if approval_state_age < 0:
        reasons.append("APPROVAL_STATE_CHECKED_IN_FUTURE")
        approval_valid = False
    elif approval_state_age > DEFAULT_AUTHORITY_MAX_AGE_SECONDS:
        reasons.append("APPROVAL_STATE_STALE")
        approval_valid = False
    if approval.approval_state != "APPROVED":
        reasons.append(f"APPROVAL_STATE_{approval.approval_state}")
        approval_valid = False
    if approval_expiry <= now:
        reasons.append("APPROVAL_EXPIRED")
        approval_valid = False
    if approval.action_hash != packet.action_hash:
        reasons.append("APPROVAL_ACTION_HASH_MISMATCH")
        approval_valid = False
    if approval.exact_scope != packet.exact_scope:
        reasons.append("APPROVAL_SCOPE_MISMATCH")
        approval_valid = False
    if approval.authority_class != packet.action_class:
        reasons.append("APPROVAL_AUTHORITY_CLASS_MISMATCH")
        approval_valid = False
    approval_evidence_valid = bool(approval.evidence_refs) and all(
        isinstance(ref, str) and ref.strip() for ref in approval.evidence_refs
    )
    if not approval.approval_state_ref.strip() or not approval_evidence_valid:
        reasons.append("APPROVAL_EVIDENCE_INCOMPLETE")
        approval_valid = False

    missing_switches = [
        name for name in _required_runtime_switches(packet.action_class)
        if not bool(getattr(authority.runtime, name))
    ]
    runtime_pass = not missing_switches
    if missing_switches:
        reasons.append("RUNTIME_AUTHORITY_DISABLED:" + ",".join(sorted(missing_switches)))

    hard_reasons = [reason for reason in reasons if not reason.startswith("RUNTIME_AUTHORITY_DISABLED:")]
    if hard_reasons:
        verdict = "HOLD_NOT_EXECUTION_ELIGIBLE"
        next_action = "REPAIR_CANONICAL_EVIDENCE_OR_EXACT_APPROVAL"
    elif not runtime_pass:
        verdict = "READY_BUT_RUNTIME_AUTHORITY_DISABLED"
        next_action = "KEEP_HELD_UNTIL_CANONICAL_RUNTIME_AUTHORITY_IS_EXPLICITLY_ENABLED"
    else:
        verdict = "READY_FOR_PROVIDER_EXECUTION"
        next_action = "RESERVE_IDEMPOTENCY_THEN_EXECUTE_ONCE_OR_RECONCILE_UNKNOWN"

    return ExecutionDecision(
        verdict=verdict,
        action_hash=packet.action_hash,
        packet_integrity_sha256=packet.packet_integrity_sha256,
        provider_execution_allowed=verdict == "READY_FOR_PROVIDER_EXECUTION",
        approval_valid=approval_valid,
        runtime_authority_pass=runtime_pass,
        canonical_authority_fresh=canonical_fresh,
        reasons=reasons,
        required_next_action=next_action,
    )


__all__ = [
    "ACTION_HASH_LEN",
    "DEFAULT_AUTHORITY_MAX_AGE_SECONDS",
    "UNKNOWN",
    "SCHEMA",
    "ApprovalEnvelope",
    "CanonicalAuthorityResolver",
    "ExecutionDecision",
    "ExternalActionPacket",
    "ResolvedAuthoritySnapshot",
    "RuntimeAuthority",
    "build_external_action_packet",
    "canonical_action_hash",
    "canonical_content_sha256",
    "evaluate_external_action",
    "evaluate_resolved_external_action",
    "recompute_action_hash",
    "recompute_packet_integrity",
]
