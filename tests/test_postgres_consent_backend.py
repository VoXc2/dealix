from __future__ import annotations

from datetime import UTC, datetime

import pytest

import app.outbound.consent as consent


def _email_contact(**extra: object) -> dict[str, object]:
    contact: dict[str, object] = {
        "tenant_id": "tenant-a",
        "contact_id": "contact-1",
        "email": "User@Example.COM",
    }
    contact.update(extra)
    return contact


def test_memory_remains_default_and_not_live_eligible(monkeypatch):
    monkeypatch.delenv("DEALIX_CONSENT_BACKEND", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert consent.consent_backend_status() == {
        "backend": "memory",
        "persistent": False,
        "live_send_eligible": False,
        "reason": "in_memory_consent_is_not_durable",
    }


def test_unknown_backend_fails_to_memory(monkeypatch):
    monkeypatch.setenv("DEALIX_CONSENT_BACKEND", "unexpected")
    assert consent.consent_backend_kind() == "memory"
    assert not consent.persistent_consent_ready()


def test_postgres_readiness_requires_verified_table_and_privileges(monkeypatch):
    monkeypatch.setenv("DEALIX_CONSENT_BACKEND", "postgres")
    monkeypatch.setattr(consent, "_postgres_table_ready", lambda: False)
    assert not consent.persistent_consent_ready()
    assert consent.consent_backend_status()["live_send_eligible"] is False

    monkeypatch.setattr(consent, "_postgres_table_ready", lambda: True)
    assert consent.persistent_consent_ready()
    assert consent.consent_backend_status() == {
        "backend": "postgres",
        "persistent": True,
        "live_send_eligible": True,
        "reason": "postgres_consent_event_ledger_and_privileges_verified",
    }


def test_durable_consent_requires_explicit_tenant_scope(monkeypatch):
    monkeypatch.setenv("DEALIX_CONSENT_BACKEND", "postgres")
    monkeypatch.delenv("DEALIX_CONSENT_DEFAULT_TENANT", raising=False)
    contact = {"email": "user@example.com"}

    with pytest.raises(RuntimeError, match="durable_consent_key_is_ambiguous_or_unsupported"):
        consent.record_consent("email", contact)

    assert not consent.has_consent("email", contact)


def test_durable_consent_rejects_unknown_channel_or_purpose(monkeypatch):
    monkeypatch.setenv("DEALIX_CONSENT_BACKEND", "postgres")
    contact = _email_contact()

    with pytest.raises(RuntimeError, match="durable_consent_key_is_ambiguous_or_unsupported"):
        consent.record_consent("telegram", contact)

    with pytest.raises(RuntimeError, match="durable_consent_key_is_ambiguous_or_unsupported"):
        consent.record_consent("email", contact, purpose="anything_goes")


def test_durable_lookup_is_tenant_recipient_channel_and_purpose_bound(monkeypatch):
    monkeypatch.setenv("DEALIX_CONSENT_BACKEND", "postgres")
    observed: list[tuple[str, str, str, str]] = []

    def latest(key: tuple[str, str, str, str]):
        observed.append(key)
        return {"state": "granted"}

    monkeypatch.setattr(consent, "_postgres_latest", latest)
    contact = _email_contact()

    assert consent.has_consent("email", contact, purpose="partner_discovery")
    assert observed == [
        ("tenant-a", "user@example.com", "email", "partner_discovery")
    ]


def test_withdrawal_is_fail_closed_for_durable_lookup(monkeypatch):
    monkeypatch.setenv("DEALIX_CONSENT_BACKEND", "postgres")
    monkeypatch.setattr(
        consent,
        "_postgres_latest",
        lambda _key: {"state": "withdrawn"},
    )
    assert not consent.has_consent("email", _email_contact())


def test_grant_and_withdrawal_append_distinct_auditable_states(monkeypatch):
    monkeypatch.setenv("DEALIX_CONSENT_BACKEND", "postgres")
    calls: list[dict[str, object]] = []

    def append(**kwargs: object) -> None:
        calls.append(dict(kwargs))

    monkeypatch.setattr(consent, "_postgres_append", append)
    occurred = datetime(2026, 9, 8, 0, 0, tzinfo=UTC)
    contact = _email_contact()

    consent.record_consent(
        "email",
        contact,
        source="inbound_reply",
        purpose="partner_discovery",
        evidence_ref="gmail:thread-1",
        evidence_digest="abc123",
        policy_version="v1",
        occurred_at=occurred,
        event_id="grant-1",
    )
    consent.withdraw_consent(
        "email",
        contact,
        source="recipient_withdrawal",
        purpose="partner_discovery",
        evidence_ref="gmail:thread-2",
        evidence_digest="def456",
        policy_version="v1",
        occurred_at=occurred,
        event_id="withdraw-1",
    )

    assert [call["state"] for call in calls] == ["granted", "withdrawn"]
    assert all(
        call["key"]
        == ("tenant-a", "user@example.com", "email", "partner_discovery")
        for call in calls
    )
    assert [call["event_id"] for call in calls] == ["grant-1", "withdraw-1"]


def test_durable_history_cannot_be_bulk_cleared(monkeypatch):
    monkeypatch.setenv("DEALIX_CONSENT_BACKEND", "postgres")
    with pytest.raises(RuntimeError, match="disabled for durable consent"):
        consent.clear_consent()


def test_postgres_dsn_rejects_non_postgres_urls(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///tmp/dealix.db")
    assert consent._postgres_dsn() is None

    monkeypatch.setenv("DATABASE_URL", "postgres://u:p@localhost/db")
    assert consent._postgres_dsn() == "postgresql://u:p@localhost/db"

    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://u:p@localhost/db")
    assert consent._postgres_dsn() == "postgresql://u:p@localhost/db"
