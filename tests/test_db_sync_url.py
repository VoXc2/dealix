"""Tests for async → sync SQLAlchemy URL helper."""

from __future__ import annotations

from auto_client_acquisition.persistence.db_sync_url import sync_sqlalchemy_url


def test_asyncpg_to_psycopg() -> None:
    u = "postgresql+asyncpg://user:pass@localhost:5432/db"
    out = sync_sqlalchemy_url(u)
    assert out.startswith("postgresql+psycopg://")
    assert "asyncpg" not in out


def test_non_async_url_unchanged() -> None:
    assert sync_sqlalchemy_url("sqlite:///:memory:") == "sqlite:///:memory:"
