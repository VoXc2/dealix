"""Safety contracts for existing-database Alembic capacity handling."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.ops.check_alembic_version_capacity import _database_url

ROOT = Path(__file__).resolve().parents[1]
CHECKER = (ROOT / "scripts" / "ops" / "check_alembic_version_capacity.py").read_text(
    encoding="utf-8"
)
WIDENER = (ROOT / "scripts" / "ops" / "widen_alembic_version_capacity.py").read_text(
    encoding="utf-8"
)
PREDEPLOY = (ROOT / "scripts" / "railway_predeploy.sh").read_text(encoding="utf-8")


def test_predeploy_does_not_execute_capacity_check_or_upgrade() -> None:
    assert "python scripts/ops/check_alembic_version_capacity.py" not in PREDEPLOY
    assert "alembic upgrade head" not in PREDEPLOY
    assert "persistent Railway variables are not action-bound L5 authority" in PREDEPLOY
    assert "ACTION_HASH" in PREDEPLOY
    assert "exit 75" in PREDEPLOY


def test_read_only_checker_has_no_schema_mutation() -> None:
    upper = CHECKER.upper()
    assert "ALTER TABLE" not in upper
    assert "DROP TABLE" not in upper
    assert "CREATE TABLE" not in upper
    assert "required_revision_capacity" in CHECKER
    assert "ScriptDirectory.from_config" in CHECKER
    assert "walk_revisions" in CHECKER


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (
            "postgres://user:pass@example.invalid:5432/dealix",
            "postgresql+asyncpg://user:pass@example.invalid:5432/dealix",
        ),
        (
            "postgresql://user:pass@example.invalid:5432/dealix",
            "postgresql+asyncpg://user:pass@example.invalid:5432/dealix",
        ),
        (
            "postgresql+psycopg://user:pass@example.invalid:5432/dealix",
            "postgresql+asyncpg://user:pass@example.invalid:5432/dealix",
        ),
        (
            "postgresql+asyncpg://user:pass@example.invalid:5432/dealix",
            "postgresql+asyncpg://user:pass@example.invalid:5432/dealix",
        ),
    ],
)
def test_capacity_checker_accepts_supported_postgres_provider_urls(
    monkeypatch: pytest.MonkeyPatch,
    raw: str,
    expected: str,
) -> None:
    monkeypatch.setenv("DATABASE_URL", raw)
    assert _database_url() == expected


def test_capacity_checker_rejects_non_postgres_urls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DATABASE_URL", "sqlite:///dealix.db")
    with pytest.raises(RuntimeError, match="supports PostgreSQL only"):
        _database_url()


def test_widener_requires_two_explicit_guards() -> None:
    assert 'ACK_ENV = "DEALIX_ALLOW_ALEMBIC_VERSION_WIDEN"' in WIDENER
    assert "--confirm-existing-db-ddl" in WIDENER
    assert "refusing DDL unless" in WIDENER
    assert "refusing DDL without" in WIDENER


def test_widener_only_targets_standard_version_column() -> None:
    assert "ALTER TABLE alembic_version" in WIDENER
    assert "ALTER COLUMN version_num TYPE VARCHAR" in WIDENER
    assert "TARGET_CAPACITY = 255" in WIDENER
