"""Evidence-bound opt-in handoff from an anonymous diagnostic to Human Review.

This module deliberately does not send a message, create a verified relationship,
grant marketing consent, or grant quote/payment/execution authority. It only
prepares a minimized, deterministic handoff after explicit purpose-specific
contact permission, documented consent timing/method, retention notice
acknowledgement, a bounded retention/follow-up window, and a referenced
suppression check.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from hashlib import sha256
from typing import Literal

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"

ContactChannel = Literal["email", "phone", "whatsapp_business", "other_consented"]
ConsentMethod = Literal["web_form", "email_reply", "in_person", "event_form", "other_documented"]
SuppressionState = Literal["CLEAR", "SUPPRESSED", "UNKNOWN_NOT_EVIDENCE_BACKED"]

_ALLOWED_CHANNELS = {"email", "phone", "whatsapp_business", "other_consented"}
_ALLOWED_CONSENT_METHODS = {"web_form", "email_reply", "in_person", "event_form", "other_documented"}
_ALLOWED_SUPPRESSION_STATES = {"CLEAR", "SUPPRESSED", UNKNOWN}


def _parse_aware_timestamp(value: str, *, field: str) -> datetime:
    text = value.strip()
    if not text:
        raise ValueError(f"{field} is required")
    normalized = f"{text[:-1]}+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include a timezone")
    return parsed.astimezone(UTC)


def _iso_utc(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class HumanReviewOptInRequest:
    diagnostic_id: str
    contact_value: str
    contact_channel: ContactChannel
    consent_ref: str
    consent_obtained_at: str
    consent_method: ConsentMethod
    evaluated_at: str
    follow_up_expires_at: str
    retention_until: str
    retention_notice_version: str
    retention_notice_acknowledged: bool
    suppression_check_ref: str
    suppression_state: SuppressionState
    contact_permission_scope: str = "human_review_follow_up_only"
    marketing_consent: bool = False


@dataclass(frozen=True)
class HumanReviewHandoff:
    handoff_id: str
    diagnostic_id: str
    contact_channel: str
    contact_fingerprint: str
    contact_fingerprint_scope: str
    state: str
    eligible_for_manual_follow_up: bool
    blocked_reason: str
    consent_ref: str
    consent_obtained_at: str
    consent_method: str
    evaluated_at: str
    follow_up_expires_at: str
    retention_until: str
    retention_notice_version: str
    suppression_check_ref: str
    suppression_state: str
    contact_permission_scope: str
    marketing_consent: bool = False
    relationship_verified: bool = False
    external_send_authority: bool = False
    quote_authority: bool = False
    payment_authority: bool = False
    public_publish_authority: bool = False
    customer_value_claim: bool = False

    def to_dict(self) -> dict[str, object]:
        """Return a receipt-safe pseudonymous representation; raw contact is excluded."""
        return asdict(self)


class HumanReviewOptIn:
    """Prepare a privacy-minimized Human Review handoff with fail-closed gates."""

    @staticmethod
    def prepare(request: HumanReviewOptInRequest) -> HumanReviewHandoff:
        diagnostic_id = request.diagnostic_id.strip()
        contact_value = request.contact_value.strip()
        contact_channel = request.contact_channel.strip().lower()
        consent_ref = request.consent_ref.strip()
        consent_method = request.consent_method.strip().lower()
        retention_notice_version = request.retention_notice_version.strip()
        suppression_check_ref = request.suppression_check_ref.strip()
        suppression_state = request.suppression_state.strip().upper()
        permission_scope = request.contact_permission_scope.strip()

        if not diagnostic_id:
            raise ValueError("diagnostic_id is required")
        if not contact_value:
            raise ValueError("contact_value is required")
        if contact_channel not in _ALLOWED_CHANNELS:
            raise ValueError("contact_channel is not supported")
        if not consent_ref:
            raise ValueError("consent_ref is required")
        if consent_method not in _ALLOWED_CONSENT_METHODS:
            raise ValueError("consent_method is not supported")
        if not retention_notice_version:
            raise ValueError("retention_notice_version is required")
        if not suppression_check_ref:
            raise ValueError("suppression_check_ref is required")
        if suppression_state not in _ALLOWED_SUPPRESSION_STATES:
            raise ValueError("suppression_state is not supported")
        if permission_scope != "human_review_follow_up_only":
            raise ValueError("contact permission must be limited to Human Review follow-up")
        if request.marketing_consent:
            raise ValueError("Human Review opt-in cannot create or infer marketing consent")

        consent_at = _parse_aware_timestamp(request.consent_obtained_at, field="consent_obtained_at")
        evaluated_at = _parse_aware_timestamp(request.evaluated_at, field="evaluated_at")
        follow_up_expires_at = _parse_aware_timestamp(
            request.follow_up_expires_at,
            field="follow_up_expires_at",
        )
        retention_until = _parse_aware_timestamp(request.retention_until, field="retention_until")

        if evaluated_at < consent_at:
            raise ValueError("evaluated_at cannot precede consent_obtained_at")
        if follow_up_expires_at <= consent_at:
            raise ValueError("follow_up_expires_at must be after consent_obtained_at")
        if retention_until < follow_up_expires_at:
            raise ValueError("retention_until cannot precede follow_up_expires_at")

        blocked_reason = ""
        if not request.retention_notice_acknowledged:
            blocked_reason = "RETENTION_NOTICE_NOT_ACKNOWLEDGED"
        elif suppression_state == "SUPPRESSED":
            blocked_reason = "SUPPRESSED"
        elif suppression_state != "CLEAR":
            blocked_reason = "SUPPRESSION_STATE_UNKNOWN"
        elif evaluated_at > follow_up_expires_at:
            blocked_reason = "FOLLOW_UP_PERMISSION_EXPIRED"
        elif evaluated_at > retention_until:
            blocked_reason = "RETENTION_WINDOW_EXPIRED"

        eligible = blocked_reason == ""
        state = "CONSENTED_HUMAN_REVIEW_REQUEST" if eligible else "HUMAN_REVIEW_BLOCKED"

        # This is a diagnostic-scoped pseudonym, not anonymization. Scoping prevents
        # the receipt from creating a stable cross-diagnostic contact identifier.
        normalized_contact = contact_value.casefold()
        contact_fingerprint = sha256(
            f"{diagnostic_id}\x00{normalized_contact}".encode("utf-8")
        ).hexdigest()

        identity_payload = "|".join(
            [
                diagnostic_id,
                contact_channel,
                contact_fingerprint,
                consent_ref,
                _iso_utc(consent_at),
                consent_method,
                _iso_utc(follow_up_expires_at),
                _iso_utc(retention_until),
                retention_notice_version,
                suppression_check_ref,
                suppression_state,
                permission_scope,
            ]
        )
        handoff_id = "hr_" + sha256(identity_payload.encode("utf-8")).hexdigest()[:24]

        return HumanReviewHandoff(
            handoff_id=handoff_id,
            diagnostic_id=diagnostic_id,
            contact_channel=contact_channel,
            contact_fingerprint=contact_fingerprint,
            contact_fingerprint_scope="diagnostic_scoped_pseudonym_not_anonymization",
            state=state,
            eligible_for_manual_follow_up=eligible,
            blocked_reason=blocked_reason,
            consent_ref=consent_ref,
            consent_obtained_at=_iso_utc(consent_at),
            consent_method=consent_method,
            evaluated_at=_iso_utc(evaluated_at),
            follow_up_expires_at=_iso_utc(follow_up_expires_at),
            retention_until=_iso_utc(retention_until),
            retention_notice_version=retention_notice_version,
            suppression_check_ref=suppression_check_ref,
            suppression_state=suppression_state,
            contact_permission_scope=permission_scope,
        )


__all__ = [
    "UNKNOWN",
    "HumanReviewHandoff",
    "HumanReviewOptIn",
    "HumanReviewOptInRequest",
]
