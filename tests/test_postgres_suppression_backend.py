from __future__ import annotations

from contextlib import contextmanager

import pytest

import app.outbound.suppression as suppression


def test_postgres_backend_is_opt_in(monkeypatch):
    monkeypatch.delenv("DEALIX_SUPPRESSION_BACKEND", raising=False)
    assert suppression.suppression_backend_kind() == "memory"

    monkeypatch.setenv("DEALIX_SUPPRESSION_BACKEND", "postgres")
    assert suppression.suppression_backend_kind() == "postgres"

    monkeypatch.setenv("DEALIX_SUPPRESSION_BACKEND", "unexpected")
    assert suppression.suppression_backend_kind() == "memory"


def test_asyncpg_database_url_is_normalized_for_psycopg(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://user:pass@db.example/dealix")
    assert suppression._postgres_dsn() == "postgresql://user:pass@db.example/dealix"


def test_postgres_status_requires_verified_table(monkeypatch):
    monkeypatch.setenv("DEALIX_SUPPRESSION_BACKEND", "postgres")
    monkeypatch.setattr(suppression, "_postgres_table_ready", lambda: True)
    assert suppression.suppression_backend_status() == {
        "backend": "postgres",
        "persistent": True,
        "live_send_eligible": True,
        "reason": "postgres_suppression_table_verified",
    }


def test_postgres_query_failure_suppresses_recipient_fail_closed(monkeypatch):
    monkeypatch.setenv("DEALIX_SUPPRESSION_BACKEND", "postgres")

    @contextmanager
    def broken_connection():
        raise RuntimeError("database unavailable")
        yield  # pragma: no cover

    monkeypatch.setattr(suppression, "_postgres_connection", broken_connection)
    assert suppression.is_suppressed("buyer@example.com", channel="email") is True


def test_durable_suppression_cannot_be_bulk_cleared(monkeypatch):
    monkeypatch.setenv("DEALIX_SUPPRESSION_BACKEND", "postgres")
    with pytest.raises(RuntimeError, match="disabled for durable suppression"):
        suppression.clear_suppressions()
