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


def test_postgres_status_requires_verified_table_and_privileges(monkeypatch):
    monkeypatch.setenv("DEALIX_SUPPRESSION_BACKEND", "postgres")
    monkeypatch.setattr(suppression, "_postgres_table_ready", lambda: True)
    assert suppression.suppression_backend_status() == {
        "backend": "postgres",
        "persistent": True,
        "live_send_eligible": True,
        "reason": "postgres_suppression_table_and_privileges_verified",
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


def test_durable_unsuppression_requires_explicit_authority(monkeypatch):
    monkeypatch.setenv("DEALIX_SUPPRESSION_BACKEND", "postgres")
    monkeypatch.delenv("DEALIX_SUPPRESSION_ALLOW_REMOVE", raising=False)
    with pytest.raises(RuntimeError, match="requires explicit authority"):
        suppression.remove_suppression("buyer@example.com", channel="email")


def test_postgres_add_writes_created_at_for_raw_sql_path(monkeypatch):
    """Raw SQL must satisfy the ORM's NOT NULL client-default timestamp contract."""

    calls: list[tuple[str, tuple[object, ...] | None]] = []

    class Cursor:
        def execute(self, sql, params=None):
            calls.append((str(sql), params))

        def fetchone(self):
            return None

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    class Connection:
        def cursor(self):
            return Cursor()

    @contextmanager
    def fake_connection():
        yield Connection()

    monkeypatch.setattr(suppression, "_postgres_connection", fake_connection)

    suppression._postgres_add("buyer@example.com", "email", "acceptance")

    insert_sql, params = calls[-1]
    normalized = " ".join(insert_sql.split()).lower()
    assert "insert into data_suppression_list" in normalized
    assert "created_at" in normalized
    assert "current_timestamp" in normalized
    assert params is not None
    assert params[1:] == ("buyer@example.com", "acceptance")
