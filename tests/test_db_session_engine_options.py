"""Regression coverage for backend-compatible async DB engine options."""

from __future__ import annotations

from db.session import _engine_options


def test_sqlite_memory_omits_queuepool_only_options() -> None:
    options = _engine_options("sqlite+aiosqlite:///:memory:", echo=False)

    assert options["echo"] is False
    assert options["pool_pre_ping"] is True
    assert options["pool_recycle"] == 1800
    assert "pool_size" not in options
    assert "max_overflow" not in options
    assert "pool_timeout" not in options


def test_postgres_preserves_production_pool_tuning() -> None:
    options = _engine_options(
        "postgresql+asyncpg://user:password@localhost:5432/dealix",
        echo=True,
    )

    assert options["echo"] is True
    assert options["pool_pre_ping"] is True
    assert options["pool_recycle"] == 1800
    assert options["pool_size"] == 20
    assert options["max_overflow"] == 30
    assert options["pool_timeout"] == 30
