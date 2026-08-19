"""Focused edge contracts for the fresh PostgreSQL bootstrap."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.ops.bootstrap_fresh_database import (
    _database_connect_args,
    _database_connection_settings,
    _database_url,
)

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_SOURCE = (ROOT / "scripts" / "ops" / "bootstrap_fresh_database.py").read_text(
    encoding="utf-8"
)


def test_database_url_translates_managed_sslmode_to_asyncpg_connect_arg(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://user:pass@example.invalid:5432/dealix?sslmode=require",
    )

    normalized, connect_args = _database_connection_settings()

    assert normalized == "postgresql+asyncpg://user:pass@example.invalid:5432/dealix"
    assert connect_args == {"ssl": "require"}
    assert _database_url() == normalized
    assert _database_connect_args() == connect_args


def test_database_url_preserves_unrelated_query_parameters(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg://user:pass@example.invalid:5432/dealix"
        "?application_name=dealix-bootstrap&sslmode=verify-full",
    )

    normalized, connect_args = _database_connection_settings()

    assert normalized == (
        "postgresql+asyncpg://user:pass@example.invalid:5432/dealix"
        "?application_name=dealix-bootstrap"
    )
    assert connect_args == {"ssl": "verify-full"}


def test_database_url_rejects_conflicting_ssl_modes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://user:pass@example.invalid:5432/dealix"
        "?sslmode=require&ssl=disable",
    )

    with pytest.raises(RuntimeError, match="conflicting ssl/sslmode"):
        _database_connection_settings()


def test_database_url_rejects_unknown_ssl_mode(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://user:pass@example.invalid:5432/dealix?sslmode=surprise",
    )

    with pytest.raises(RuntimeError, match="unsupported sslmode"):
        _database_connection_settings()


def test_occupancy_guard_includes_replication_and_large_object_catalogs() -> None:
    for catalog in (
        "pg_catalog.pg_publication",
        "pg_catalog.pg_subscription",
        "pg_catalog.pg_largeobject_metadata",
    ):
        assert catalog in BOOTSTRAP_SOURCE
    assert "| publications" in BOOTSTRAP_SOURCE
    assert "| subscriptions" in BOOTSTRAP_SOURCE
    assert "| large_objects" in BOOTSTRAP_SOURCE
