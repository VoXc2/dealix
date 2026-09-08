#!/usr/bin/env python3
"""Real PostgreSQL acceptance for Dealix durable consent.

This verifier accepts only an explicitly named loopback ephemeral database.
It proves the canonical consent module against a real PostgreSQL ledger without
printing credentials or touching Production.
"""
from __future__ import annotations

import argparse
import os
from datetime import UTC, datetime, timedelta

from sqlalchemy.engine import make_url

from app.outbound import consent

DB_PREFIX = "dealix_consent_acceptance_"
ALLOWED_HOSTS = {"127.0.0.1", "localhost", "::1"}


def fail(message: str) -> None:
    raise SystemExit(f"DEALIX_DURABLE_CONSENT_POSTGRES_ACCEPTANCE=FAIL:{message}")


def validate_database_url(raw: str) -> None:
    if not raw:
        fail("DATABASE_URL_REQUIRED")
    try:
        url = make_url(raw)
    except Exception:
        fail("INVALID_DATABASE_URL")
    if not url.drivername.startswith("postgresql"):
        fail("POSTGRESQL_REQUIRED")
    if (url.host or "") not in ALLOWED_HOSTS:
        fail("LOOPBACK_DATABASE_REQUIRED")
    if not str(url.database or "").startswith(DB_PREFIX):
        fail("EPHEMERAL_DATABASE_NAME_REQUIRED")
    if not url.password:
        fail("TEST_DATABASE_PASSWORD_REQUIRED")


def count_rows() -> int:
    with consent._postgres_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM outbound_consent_events")
        row = cur.fetchone()
        conn.rollback()
        return int(row[0] if row else 0)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def setup_phase() -> None:
    require(consent.persistent_consent_ready(), "PERSISTENT_BACKEND_NOT_READY")

    base = datetime(2026, 9, 8, 1, 0, tzinfo=UTC)
    contact = {
        "tenant_id": "tenant-acceptance-a",
        "contact_id": "contact-acceptance-1",
        "email": "Consent.Acceptance@Example.COM",
    }

    consent.record_consent(
        "email",
        contact,
        source="synthetic_acceptance",
        purpose="direct_marketing",
        evidence_ref="synthetic://consent/grant-1",
        evidence_digest="a" * 64,
        policy_version="acceptance-v1",
        occurred_at=base,
        event_id="accept-grant-1",
    )
    require(consent.has_consent("email", contact, "direct_marketing"), "GRANT_NOT_EFFECTIVE")

    consent.record_consent(
        "email",
        contact,
        source="synthetic_acceptance",
        purpose="direct_marketing",
        evidence_ref="synthetic://consent/grant-1",
        evidence_digest="a" * 64,
        policy_version="acceptance-v1",
        occurred_at=base,
        event_id="accept-grant-1",
    )
    require(count_rows() == 1, "IDEMPOTENT_REPLAY_DUPLICATED_EVENT")

    try:
        consent.record_consent(
            "email",
            contact,
            source="synthetic_acceptance",
            purpose="direct_marketing",
            evidence_ref="synthetic://consent/grant-1",
            evidence_digest="b" * 64,
            policy_version="acceptance-v1",
            occurred_at=base,
            event_id="accept-grant-1",
        )
    except RuntimeError as exc:
        require(str(exc) == "consent_event_key_conflict", "WRONG_EVENT_KEY_CONFLICT")
    else:
        fail("CONFLICTING_REPLAY_DID_NOT_FAIL")

    consent.withdraw_consent(
        "email",
        contact,
        source="synthetic_withdrawal",
        purpose="direct_marketing",
        evidence_ref="synthetic://consent/withdraw-1",
        evidence_digest="c" * 64,
        policy_version="acceptance-v1",
        occurred_at=base + timedelta(seconds=1),
        event_id="accept-withdraw-1",
    )
    require(not consent.has_consent("email", contact, "direct_marketing"), "WITHDRAWAL_NOT_EFFECTIVE")

    consent.record_consent(
        "email",
        contact,
        source="synthetic_reconsent",
        purpose="direct_marketing",
        evidence_ref="synthetic://consent/regrant-1",
        evidence_digest="d" * 64,
        policy_version="acceptance-v1",
        occurred_at=base + timedelta(seconds=2),
        event_id="accept-regrant-1",
    )
    require(consent.has_consent("email", contact, "direct_marketing"), "RECONSENT_NOT_EFFECTIVE")

    require(not consent.has_consent("email", contact, "partner_discovery"), "PURPOSE_AUTHORITY_LEAK")
    other_tenant = dict(contact, tenant_id="tenant-acceptance-b")
    require(not consent.has_consent("email", other_tenant, "direct_marketing"), "TENANT_AUTHORITY_LEAK")

    tie_time = base + timedelta(seconds=3)
    consent.record_consent(
        "email",
        contact,
        source="synthetic_tie_grant",
        purpose="support",
        evidence_ref="synthetic://consent/tie-grant",
        evidence_digest="e" * 64,
        policy_version="acceptance-v1",
        occurred_at=tie_time,
        event_id="accept-tie-grant",
    )
    consent.withdraw_consent(
        "email",
        contact,
        source="synthetic_tie_withdrawal",
        purpose="support",
        evidence_ref="synthetic://consent/tie-withdraw",
        evidence_digest="f" * 64,
        policy_version="acceptance-v1",
        occurred_at=tie_time,
        event_id="accept-tie-withdraw",
    )
    require(not consent.has_consent("email", contact, "support"), "WITHDRAWAL_TIE_DID_NOT_FAIL_CLOSED")
    require(count_rows() == 5, "UNEXPECTED_SETUP_EVENT_COUNT")

    print("CONSENT_POSTGRES_SCHEMA_READY=PASS")
    print("CONSENT_POSTGRES_GRANT_WITHDRAW_RECONSENT=PASS")
    print("CONSENT_POSTGRES_EVENT_REPLAY_IDEMPOTENCY=PASS")
    print("CONSENT_POSTGRES_EVENT_CONFLICT=PASS")
    print("CONSENT_POSTGRES_TENANT_PURPOSE_ISOLATION=PASS")
    print("CONSENT_POSTGRES_WITHDRAWAL_TIE_FAIL_CLOSED=PASS")
    print("CONSENT_POSTGRES_EVENT_COUNT=5")


def restart_phase() -> None:
    require(consent.persistent_consent_ready(), "PERSISTENT_BACKEND_NOT_READY_AFTER_RESTART")
    contact = {
        "tenant_id": "tenant-acceptance-a",
        "contact_id": "contact-acceptance-1",
        "email": "Consent.Acceptance@Example.COM",
    }
    require(consent.has_consent("email", contact, "direct_marketing"), "RECONSENT_NOT_PERSISTED_AFTER_RESTART")
    require(not consent.has_consent("email", contact, "support"), "WITHDRAWAL_NOT_PERSISTED_AFTER_RESTART")
    require(count_rows() == 5, "EVENT_COUNT_CHANGED_AFTER_RESTART")

    consent.withdraw_consent(
        "email",
        contact,
        source="synthetic_post_restart_withdrawal",
        purpose="direct_marketing",
        evidence_ref="synthetic://consent/post-restart-withdraw",
        evidence_digest="0" * 64,
        policy_version="acceptance-v1",
        occurred_at=datetime(2026, 9, 8, 1, 0, 10, tzinfo=UTC),
        event_id="accept-post-restart-withdraw",
    )
    require(not consent.has_consent("email", contact, "direct_marketing"), "POST_RESTART_WRITE_NOT_EFFECTIVE")
    require(count_rows() == 6, "POST_RESTART_EVENT_COUNT_WRONG")

    print("CONSENT_POSTGRES_RESTART_PERSISTENCE=PASS")
    print("CONSENT_POSTGRES_POST_RESTART_WRITE=PASS")
    print("CONSENT_POSTGRES_EVENT_COUNT=6")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", required=True, choices=["setup", "restart"])
    args = parser.parse_args()

    raw = os.getenv("DATABASE_URL", "")
    validate_database_url(raw)
    os.environ["DEALIX_CONSENT_BACKEND"] = "postgres"
    os.environ.pop("DEALIX_CONSENT_DEFAULT_TENANT", None)

    if args.phase == "setup":
        setup_phase()
    else:
        restart_phase()

    print("DEALIX_DURABLE_CONSENT_POSTGRES_ACCEPTANCE=PASS")
    print(f"phase={args.phase}")
    print("real_postgres=true")
    print("production_db=false")
    print("external_send=false")
    print("payment=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
