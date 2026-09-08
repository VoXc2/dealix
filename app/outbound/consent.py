"""Canonical outbound consent authority.

The default backend remains process memory for draft/testing workflows. A
PostgreSQL event ledger can be selected explicitly for durable consent proof:

    DEALIX_CONSENT_BACKEND=postgres
    DATABASE_URL=<existing Dealix PostgreSQL URL>
    DEALIX_CONSENT_DEFAULT_TENANT=<optional explicit Dealix tenant scope>

The PostgreSQL path is fail-closed. Database errors, schema drift, missing
privileges, unknown channel/purpose, or ambiguous recipient normalization never
become permission to send. Consent is stored as an append-only event ledger so
withdrawal/re-consent history remains auditable; a later explicit grant may
supersede a withdrawal, but an independent suppression record remains a
separate gate owned by ``app.outbound.suppression``.

No message body, provider secret, or credential is required as consent evidence.
"""

from __future__ import annotations

import os
import re
import time
import uuid
from contextlib import contextmanager
from datetime import UTC, datetime
from threading import Lock
from typing import Any, Iterator, Mapping

_LOCK = Lock()
_MEMORY_BACKEND = "memory"
_POSTGRES_BACKEND = "postgres"
_ALLOWED_CHANNELS = {"email", "whatsapp", "sms"}
_ALLOWED_PURPOSES = {
    "direct_marketing",
    "partner_discovery",
    "customer_success",
    "support",
    "transactional",
}

# Draft-only current-state mirror. Durable PostgreSQL uses an append-only ledger.
# key = (tenant_scope, normalized_recipient, channel, purpose)
_CONSENT: dict[tuple[str, str, str, str], dict[str, Any]] = {}


def consent_backend_kind() -> str:
    """Return the configured consent backend; unknown values fail to memory."""

    value = os.getenv("DEALIX_CONSENT_BACKEND", _MEMORY_BACKEND).strip().lower()
    return _POSTGRES_BACKEND if value == _POSTGRES_BACKEND else _MEMORY_BACKEND


def _postgres_dsn() -> str | None:
    value = os.getenv("DATABASE_URL", "").strip()
    if not value:
        return None
    if value.startswith("postgresql+asyncpg://"):
        return "postgresql://" + value.removeprefix("postgresql+asyncpg://")
    if value.startswith("postgres://"):
        return "postgresql://" + value.removeprefix("postgres://")
    if value.startswith("postgresql://"):
        return value
    return None


@contextmanager
def _postgres_connection() -> Iterator[Any]:
    dsn = _postgres_dsn()
    if not dsn:
        raise RuntimeError("postgres consent backend requires PostgreSQL DATABASE_URL")

    import psycopg

    with psycopg.connect(dsn, connect_timeout=3, autocommit=False) as conn:
        yield conn


def _postgres_table_ready() -> bool:
    """Read-only proof that the event ledger exists with required privileges."""

    required_columns = {
        "id",
        "event_key",
        "tenant_scope",
        "contact_id",
        "recipient",
        "channel",
        "purpose",
        "state",
        "occurred_at",
        "source",
        "evidence_ref",
        "evidence_digest",
        "policy_version",
        "created_at",
    }
    try:
        with _postgres_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    to_regclass('public.outbound_consent_events') IS NOT NULL
                    AND has_table_privilege(
                        current_user,
                        'public.outbound_consent_events',
                        'SELECT'
                    )
                    AND has_table_privilege(
                        current_user,
                        'public.outbound_consent_events',
                        'INSERT'
                    )
                """
            )
            row = cur.fetchone()
            if not row or row[0] is not True:
                return False
            cur.execute(
                """
                SELECT column_name
                  FROM information_schema.columns
                 WHERE table_schema = 'public'
                   AND table_name = 'outbound_consent_events'
                """
            )
            columns = {str(item[0]) for item in cur.fetchall()}
            conn.rollback()
            return required_columns.issubset(columns)
    except Exception:
        return False


def persistent_consent_ready() -> bool:
    """Whether durable consent evidence is independently proven read-only."""

    if consent_backend_kind() != _POSTGRES_BACKEND:
        return False
    return _postgres_table_ready()


def consent_backend_status() -> dict[str, Any]:
    backend = consent_backend_kind()
    persistent = persistent_consent_ready()
    if backend == _MEMORY_BACKEND:
        reason = "in_memory_consent_is_not_durable"
    elif persistent:
        reason = "postgres_consent_event_ledger_and_privileges_verified"
    else:
        reason = "postgres_consent_not_verified"
    return {
        "backend": backend,
        "persistent": persistent,
        "live_send_eligible": persistent,
        "reason": reason,
    }


def _normalize_channel(channel: str) -> str:
    value = (channel or "").strip().lower()
    return value if value in _ALLOWED_CHANNELS else ""


def _normalize_purpose(purpose: str) -> str:
    value = re.sub(r"[^a-z0-9_]+", "_", (purpose or "").strip().lower()).strip("_")
    return value if value in _ALLOWED_PURPOSES else ""


def _identifier_for(channel: str, contact: Mapping[str, Any]) -> str:
    if channel == "email":
        return str(contact.get("email", ""))
    if channel == "whatsapp":
        return str(contact.get("whatsapp", ""))
    if channel == "sms":
        return str(contact.get("phone", ""))
    return ""


def _normalize_recipient(channel: str, value: str, *, strict: bool) -> str:
    raw = (value or "").strip()
    if channel == "email":
        normalized = raw.lower()
        if not normalized or "@" not in normalized or normalized.startswith("@"):
            return ""
        return normalized

    if raw.lower().startswith("whatsapp:"):
        raw = raw.split(":", 1)[1]
    compact = re.sub(r"[\s\-().]", "", raw)
    if compact.startswith("00"):
        compact = "+" + compact[2:]
    if strict:
        if not compact.startswith("+") or not compact[1:].isdigit():
            return ""
    elif not (compact.startswith("+") and compact[1:].isdigit()) and not compact.isdigit():
        return ""
    return compact


def _tenant_scope(contact: Mapping[str, Any], *, strict: bool) -> str:
    for key in ("tenant_id", "account_id", "organization_id"):
        value = str(contact.get(key, "")).strip().lower()
        if value:
            return value
    configured = os.getenv("DEALIX_CONSENT_DEFAULT_TENANT", "").strip().lower()
    if configured:
        return configured
    return "" if strict else "__draft__"


def _contact_id(contact: Mapping[str, Any]) -> str | None:
    for key in ("contact_id", "id"):
        value = str(contact.get(key, "")).strip()
        if value:
            return value[:128]
    return None


def _key(
    channel: str,
    contact: Mapping[str, Any],
    purpose: str,
    *,
    strict: bool,
) -> tuple[str, str, str, str] | None:
    normalized_channel = _normalize_channel(channel)
    normalized_purpose = _normalize_purpose(purpose)
    scope = _tenant_scope(contact, strict=strict)
    recipient = _normalize_recipient(
        normalized_channel,
        _identifier_for(normalized_channel, contact),
        strict=strict,
    )
    if not all((normalized_channel, normalized_purpose, scope, recipient)):
        return None
    return scope, recipient, normalized_channel, normalized_purpose


def _coerce_occurred_at(value: datetime | float | int | None) -> datetime:
    if value is None:
        return datetime.now(UTC)
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)
    return datetime.fromtimestamp(float(value), tz=UTC)


def _postgres_latest(
    key: tuple[str, str, str, str],
) -> dict[str, Any] | None:
    scope, recipient, channel, purpose = key
    try:
        with _postgres_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, event_key, state, occurred_at, source,
                       evidence_ref, evidence_digest, policy_version,
                       contact_id, created_at
                  FROM outbound_consent_events
                 WHERE tenant_scope = %s
                   AND recipient = %s
                   AND channel = %s
                   AND purpose = %s
                 ORDER BY occurred_at DESC,
                          (state = 'withdrawn') DESC,
                          created_at DESC,
                          id DESC
                 LIMIT 1
                """,
                (scope, recipient, channel, purpose),
            )
            row = cur.fetchone()
            conn.rollback()
            if not row:
                return None
            return {
                "id": row[0],
                "event_key": row[1],
                "state": row[2],
                "occurred_at": row[3],
                "source": row[4],
                "evidence_ref": row[5],
                "evidence_digest": row[6],
                "policy_version": row[7],
                "contact_id": row[8],
                "created_at": row[9],
            }
    except Exception:
        return None


def _postgres_append(
    *,
    state: str,
    key: tuple[str, str, str, str],
    contact: Mapping[str, Any],
    source: str,
    evidence_ref: str,
    evidence_digest: str,
    policy_version: str,
    occurred_at: datetime | float | int | None,
    event_id: str | None,
) -> None:
    scope, recipient, channel, purpose = key
    event_key = (event_id or uuid.uuid4().hex).strip()[:128]
    if not event_key:
        raise RuntimeError("consent_event_key_required")
    occurred = _coerce_occurred_at(occurred_at)
    row_id = uuid.uuid4().hex

    with _postgres_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO outbound_consent_events (
                id, event_key, tenant_scope, contact_id, recipient,
                channel, purpose, state, occurred_at, source,
                evidence_ref, evidence_digest, policy_version
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (event_key) DO NOTHING
            """,
            (
                row_id,
                event_key,
                scope,
                _contact_id(contact),
                recipient,
                channel,
                purpose,
                state,
                occurred,
                (source or "manual")[:128],
                (evidence_ref or "")[:512] or None,
                (evidence_digest or "")[:128] or None,
                (policy_version or "")[:64] or None,
            ),
        )
        if cur.rowcount == 0:
            cur.execute(
                """
                SELECT tenant_scope, recipient, channel, purpose, state,
                       occurred_at, source, evidence_ref, evidence_digest,
                       policy_version
                  FROM outbound_consent_events
                 WHERE event_key = %s
                """,
                (event_key,),
            )
            existing = cur.fetchone()
            expected = (
                scope,
                recipient,
                channel,
                purpose,
                state,
                occurred,
                (source or "manual")[:128],
                (evidence_ref or "")[:512] or None,
                (evidence_digest or "")[:128] or None,
                (policy_version or "")[:64] or None,
            )
            if existing != expected:
                conn.rollback()
                raise RuntimeError("consent_event_key_conflict")
        conn.commit()


def has_consent(
    channel: str,
    contact: Mapping[str, Any],
    purpose: str = "direct_marketing",
) -> bool:
    """True only when the active authority has a matching current grant.

    The durable backend requires explicit tenant scope and strict phone
    normalization. The memory backend retains legacy draft-only eligibility
    fallbacks; those fallbacks never make ``persistent_consent_ready`` true.
    """

    durable = consent_backend_kind() == _POSTGRES_BACKEND
    key = _key(channel, contact, purpose, strict=durable)
    if key is None:
        return False

    if durable:
        record = _postgres_latest(key)
        return bool(record and record.get("state") == "granted")

    with _LOCK:
        record = _CONSENT.get(key)
        if record is not None:
            return record.get("state") == "granted"

    normalized_channel = key[2]
    if normalized_channel == "email":
        if contact.get("email_opt_out") is True:
            return False
        return contact.get("verification_status") == "approved_to_send"
    if normalized_channel == "whatsapp":
        return contact.get("whatsapp_opt_in") is True
    if normalized_channel == "sms":
        return contact.get("sms_opt_in") is True
    return False


def record_consent(
    channel: str,
    contact: Mapping[str, Any],
    source: str = "manual",
    *,
    purpose: str = "direct_marketing",
    evidence_ref: str = "",
    evidence_digest: str = "",
    policy_version: str = "",
    occurred_at: datetime | float | int | None = None,
    event_id: str | None = None,
) -> None:
    """Append a grant event to the active consent authority."""

    durable = consent_backend_kind() == _POSTGRES_BACKEND
    key = _key(channel, contact, purpose, strict=durable)
    if key is None:
        if durable:
            raise RuntimeError("durable_consent_key_is_ambiguous_or_unsupported")
        return
    if durable:
        _postgres_append(
            state="granted",
            key=key,
            contact=contact,
            source=source,
            evidence_ref=evidence_ref,
            evidence_digest=evidence_digest,
            policy_version=policy_version,
            occurred_at=occurred_at,
            event_id=event_id,
        )
        return

    occurred = _coerce_occurred_at(occurred_at)
    with _LOCK:
        _CONSENT[key] = {
            "state": "granted",
            "ts": occurred.timestamp(),
            "source": source,
            "purpose": key[3],
            "evidence_ref": evidence_ref or None,
            "evidence_digest": evidence_digest or None,
            "policy_version": policy_version or None,
            "event_key": event_id,
        }


def withdraw_consent(
    channel: str,
    contact: Mapping[str, Any],
    *,
    purpose: str = "direct_marketing",
    source: str = "manual_withdrawal",
    evidence_ref: str = "",
    evidence_digest: str = "",
    policy_version: str = "",
    occurred_at: datetime | float | int | None = None,
    event_id: str | None = None,
) -> None:
    """Append a withdrawal event; withdrawal is fail-closed for live eligibility."""

    durable = consent_backend_kind() == _POSTGRES_BACKEND
    key = _key(channel, contact, purpose, strict=durable)
    if key is None:
        if durable:
            raise RuntimeError("durable_consent_key_is_ambiguous_or_unsupported")
        return
    if durable:
        _postgres_append(
            state="withdrawn",
            key=key,
            contact=contact,
            source=source,
            evidence_ref=evidence_ref,
            evidence_digest=evidence_digest,
            policy_version=policy_version,
            occurred_at=occurred_at,
            event_id=event_id,
        )
        return

    occurred = _coerce_occurred_at(occurred_at)
    with _LOCK:
        _CONSENT[key] = {
            "state": "withdrawn",
            "ts": occurred.timestamp(),
            "source": source,
            "purpose": key[3],
            "evidence_ref": evidence_ref or None,
            "evidence_digest": evidence_digest or None,
            "policy_version": policy_version or None,
            "event_key": event_id,
        }


def clear_consent() -> None:
    """Clear process-local test state; durable history can never be bulk-cleared."""

    if consent_backend_kind() == _POSTGRES_BACKEND:
        raise RuntimeError("clear_consent is disabled for durable consent")
    with _LOCK:
        _CONSENT.clear()


def consent_record(
    channel: str,
    contact: Mapping[str, Any],
    purpose: str = "direct_marketing",
) -> dict[str, Any] | None:
    """Return the current record without exposing database credentials."""

    durable = consent_backend_kind() == _POSTGRES_BACKEND
    key = _key(channel, contact, purpose, strict=durable)
    if key is None:
        return None
    if durable:
        record = _postgres_latest(key)
        return dict(record) if record else None
    with _LOCK:
        record = _CONSENT.get(key)
        return dict(record) if record else None
