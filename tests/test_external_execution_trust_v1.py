from __future__ import annotations

import asyncio
import sqlite3
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

from api.routers.email_send import send_approved, send_batch
from auto_client_acquisition.email.gmail_send import send_email
from dealix.commercial.external_execution_gate import (
    ApprovalEnvelope,
    RuntimeAuthority,
    build_external_action_packet,
    canonical_content_sha256,
    evaluate_external_action,
)
from dealix.commercial.idempotency_ledger import SqliteIdempotencyLedger
from integrations.email import (
    LIVE_EMAIL_QUARANTINE_REASON,
    EmailClient,
)


def _ts(minutes: int) -> str:
    return (datetime.now(UTC) + timedelta(minutes=minutes)).isoformat()


def _packet(*, key: str = "trust-v1"):
    destination = "buyer@example.com"
    content_hash = canonical_content_sha256(
        destination=destination,
        subject="s",
        body="b",
    )
    return build_external_action_packet(
        action_id="trust-1",
        action_class="EMAIL_SEND",
        purpose_class="REQUESTED_FOLLOWUP",
        destination=destination,
        channel="email",
        environment="production",
        artifact_ref="runtime://trust-1",
        content_sha256=content_hash,
        identity_or_relationship_ref="evidence://interaction/1",
        consent_or_channel_eligibility_ref="evidence://followup/1",
        suppression_check_ref="evidence://suppression/1",
        suppression_clear=True,
        claim_evidence_refs=["evidence://claim/1"],
        sender_identity_ref="policy://sender",
        exact_scope="one-message",
        expires_at=_ts(30),
        provider="gmail_api",
        idempotency_key=key,
    )


def test_schema_version_is_literal_and_bound_into_integrity_and_action_hash() -> None:
    packet = _packet()
    mutated = packet.model_copy(
        update={"schema_version": "dealix.external-action-packet.v999"}
    )
    decision = evaluate_external_action(
        mutated,
        runtime=RuntimeAuthority(external_send=True, connector_write=True),
    )
    assert "UNSUPPORTED_PACKET_SCHEMA" in decision.reasons
    assert "PACKET_INTEGRITY_MISMATCH" in decision.reasons
    assert "ACTION_HASH_MISMATCH" in decision.reasons
    assert decision.provider_execution_allowed is False


def test_legacy_gmail_send_surface_is_quarantined_without_network_effect() -> None:
    result = asyncio.run(
        send_email(
            to_email="buyer@example.com",
            subject="approved-looking subject",
            body_plain="approved-looking body",
        )
    )
    assert result.status == "quarantined"
    assert result.gmail_message_id is None
    assert result.error == (
        "LIVE_GMAIL_SEND_QUARANTINED_CANONICAL_GOVERNANCE_PROVIDER_NOT_WIRED"
    )


def test_legacy_email_http_routes_are_quarantined_before_validation_or_provider() -> None:
    for route in (send_approved, send_batch):
        result = asyncio.run(route({}))
        assert result["status"] == "quarantined"
        assert result["reasons"] == [
            "LIVE_GMAIL_SEND_QUARANTINED_CANONICAL_GOVERNANCE_PROVIDER_NOT_WIRED"
        ]


def test_unified_resend_sendgrid_smtp_paths_are_all_quarantined() -> None:
    """No configured legacy provider may bypass canonical L5 authority."""
    client = EmailClient.__new__(EmailClient)
    client.settings = SimpleNamespace(email_provider="resend")

    generic = asyncio.run(
        client.send(
            to="buyer@example.com",
            subject="approved-looking subject",
            body_text="approved-looking body",
        )
    )
    assert generic.success is False
    assert generic.error == LIVE_EMAIL_QUARANTINE_REASON

    provider_calls = (
        client._send_resend,
        client._send_sendgrid,
        client._send_smtp,
    )
    for call in provider_calls:
        result = asyncio.run(
            call(
                "buyer@example.com",
                "subject",
                "body",
                None,
                None,
            )
        )
        assert result.success is False
        assert result.message_id is None
        assert result.error == LIVE_EMAIL_QUARANTINE_REASON


def test_unknown_can_be_audited_to_committed_and_then_replayed_without_side_effect(
    tmp_path,
) -> None:
    packet = _packet(key="unknown-delivered")
    ledger = SqliteIdempotencyLedger(tmp_path / "ledger.sqlite")
    assert ledger.reserve(
        idempotency_key=packet.idempotency_key,
        action_hash=packet.action_hash,
        packet_integrity_sha256=packet.packet_integrity_sha256,
    ).status == "RESERVED_NEW"
    ledger.mark_unknown(
        idempotency_key=packet.idempotency_key,
        action_hash=packet.action_hash,
        packet_integrity_sha256=packet.packet_integrity_sha256,
    )
    receipt = {
        "provider": "gmail_api",
        "provider_message_id": "confirmed-msg",
        "status": "CONFIRMED_DELIVERED",
    }
    ledger.reconcile_unknown_committed(
        idempotency_key=packet.idempotency_key,
        action_hash=packet.action_hash,
        packet_integrity_sha256=packet.packet_integrity_sha256,
        receipt=receipt,
        evidence_ref="reconciliation://gmail/message/confirmed-msg",
    )
    replay = ledger.reserve(
        idempotency_key=packet.idempotency_key,
        action_hash=packet.action_hash,
        packet_integrity_sha256=packet.packet_integrity_sha256,
    )
    assert replay.status == "REPLAY_COMMITTED"
    assert replay.receipt == receipt
    assert replay.reconciliation["resolution"] == "CONFIRMED_DELIVERED"


def test_reconcile_committed_rejects_empty_provider_receipt(tmp_path) -> None:
    packet = _packet(key="unknown-empty-receipt")
    ledger = SqliteIdempotencyLedger(tmp_path / "ledger.sqlite")
    ledger.reserve(
        idempotency_key=packet.idempotency_key,
        action_hash=packet.action_hash,
        packet_integrity_sha256=packet.packet_integrity_sha256,
    )
    ledger.mark_unknown(
        idempotency_key=packet.idempotency_key,
        action_hash=packet.action_hash,
        packet_integrity_sha256=packet.packet_integrity_sha256,
    )
    try:
        ledger.reconcile_unknown_committed(
            idempotency_key=packet.idempotency_key,
            action_hash=packet.action_hash,
            packet_integrity_sha256=packet.packet_integrity_sha256,
            receipt={},
            evidence_ref="reconciliation://empty-receipt",
        )
    except ValueError as exc:
        assert "receipt" in str(exc)
    else:
        raise AssertionError("empty delivery receipt must be rejected")


def test_unknown_confirmed_not_delivered_aborts_key_and_requires_new_action(
    tmp_path,
) -> None:
    packet = _packet(key="unknown-not-delivered")
    ledger = SqliteIdempotencyLedger(tmp_path / "ledger.sqlite")
    ledger.reserve(
        idempotency_key=packet.idempotency_key,
        action_hash=packet.action_hash,
        packet_integrity_sha256=packet.packet_integrity_sha256,
    )
    ledger.mark_unknown(
        idempotency_key=packet.idempotency_key,
        action_hash=packet.action_hash,
        packet_integrity_sha256=packet.packet_integrity_sha256,
    )
    ledger.reconcile_unknown_not_delivered(
        idempotency_key=packet.idempotency_key,
        action_hash=packet.action_hash,
        packet_integrity_sha256=packet.packet_integrity_sha256,
        evidence_ref="reconciliation://gmail/provider-search/no-message",
    )
    result = ledger.reserve(
        idempotency_key=packet.idempotency_key,
        action_hash=packet.action_hash,
        packet_integrity_sha256=packet.packet_integrity_sha256,
    )
    assert result.status == "RECONCILED_NOT_DELIVERED"
    assert result.state == "ABORTED"
    assert result.reconciliation["next_action"] == (
        "CREATE_NEW_IDEMPOTENCY_KEY_AND_REAUTHORIZE_BEFORE_RETRY"
    )


def test_legacy_sqlite_check_constraint_is_rebuilt_before_aborted_transition(
    tmp_path,
) -> None:
    """Production-style old DBs must migrate by table rebuild, preserving rows."""
    path = tmp_path / "legacy-ledger.sqlite"
    packet = _packet(key="legacy-migration")
    now = datetime.now(UTC).isoformat()
    connection = sqlite3.connect(path)
    connection.execute(
        """
        CREATE TABLE external_effect_idempotency (
            idempotency_key TEXT PRIMARY KEY,
            action_hash TEXT NOT NULL,
            packet_integrity_sha256 TEXT NOT NULL,
            state TEXT NOT NULL CHECK(state IN ('RESERVED','COMMITTED','UNKNOWN')),
            receipt_json TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        INSERT INTO external_effect_idempotency (
            idempotency_key, action_hash, packet_integrity_sha256, state,
            receipt_json, created_at, updated_at
        ) VALUES (?, ?, ?, 'UNKNOWN', NULL, ?, ?)
        """,
        (
            packet.idempotency_key,
            packet.action_hash,
            packet.packet_integrity_sha256,
            now,
            now,
        ),
    )
    connection.commit()
    connection.close()

    ledger = SqliteIdempotencyLedger(path)
    preserved = ledger.get(packet.idempotency_key)
    assert preserved is not None
    assert preserved["state"] == "UNKNOWN"
    assert "reconciliation_json" in preserved

    ledger.reconcile_unknown_not_delivered(
        idempotency_key=packet.idempotency_key,
        action_hash=packet.action_hash,
        packet_integrity_sha256=packet.packet_integrity_sha256,
        evidence_ref="reconciliation://migration/not-delivered",
    )
    migrated = ledger.get(packet.idempotency_key)
    assert migrated is not None
    assert migrated["state"] == "ABORTED"
    assert "CONFIRMED_NOT_DELIVERED" in str(migrated["reconciliation_json"])


def test_blank_approval_evidence_refs_are_rejected() -> None:
    with pytest.raises(ValueError, match="cannot contain blank references"):
        ApprovalEnvelope(
            approval_id="approval-blank",
            action_hash="0" * 16,
            exact_scope="one-email",
            authority_class="EMAIL_SEND",
            approval_state="APPROVED",
            approval_state_ref="approval://blank",
            state_checked_at=_ts(30),
            expires_at=_ts(30),
            evidence_refs=["   "],
        )


def test_empty_or_unconfirmed_delivery_receipt_cannot_commit_unknown(tmp_path) -> None:
    packet = _packet(key="unknown-invalid-receipt")
    ledger = SqliteIdempotencyLedger(tmp_path / "ledger.sqlite")
    ledger.reserve(
        idempotency_key=packet.idempotency_key,
        action_hash=packet.action_hash,
        packet_integrity_sha256=packet.packet_integrity_sha256,
    )
    ledger.mark_unknown(
        idempotency_key=packet.idempotency_key,
        action_hash=packet.action_hash,
        packet_integrity_sha256=packet.packet_integrity_sha256,
    )
    with pytest.raises(ValueError, match="requires nonblank provider"):
        ledger.reconcile_unknown_committed(
            idempotency_key=packet.idempotency_key,
            action_hash=packet.action_hash,
            packet_integrity_sha256=packet.packet_integrity_sha256,
            receipt={},
            evidence_ref="reconciliation://missing-receipt",
        )
    with pytest.raises(ValueError, match="CONFIRMED_DELIVERED"):
        ledger.reconcile_unknown_committed(
            idempotency_key=packet.idempotency_key,
            action_hash=packet.action_hash,
            packet_integrity_sha256=packet.packet_integrity_sha256,
            receipt={
                "provider": "gmail_api",
                "provider_message_id": "msg-1",
                "status": "PROVIDER_ACCEPTED_SEND_REQUEST",
            },
            evidence_ref="reconciliation://unconfirmed",
        )
