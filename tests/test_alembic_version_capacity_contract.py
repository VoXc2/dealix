"""Safety contracts for existing-database Alembic capacity handling."""

from __future__ import annotations

import subprocess
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


def test_predeploy_checks_capacity_before_upgrade() -> None:
    check = "python scripts/ops/check_alembic_version_capacity.py"
    upgrade = "alembic upgrade head"
    assert check in PREDEPLOY
    assert PREDEPLOY.index(check) < PREDEPLOY.rindex(upgrade)


def test_predeploy_preserves_separate_db_authority_gate() -> None:
    migrate_gate = "RUN_RAILWAY_PRE_DEPLOY_MIGRATE"
    authority_gate = "DEALIX_DB_MIGRATION_AUTHORIZED"
    capacity_check = "run_step capacity_check"
    assert PREDEPLOY.index(migrate_gate) < PREDEPLOY.index(authority_gate)
    assert PREDEPLOY.index(authority_gate) < PREDEPLOY.index(capacity_check)


def test_predeploy_emits_step_and_exit_code_without_secret_echo() -> None:
    assert "RAILWAY_PREDEPLOY: START step=${step}" in PREDEPLOY
    assert "RAILWAY_PREDEPLOY: FAIL step=${step} rc=${rc}" in PREDEPLOY
    assert "echo \"${DATABASE_URL}" not in PREDEPLOY


def test_predeploy_run_step_preserves_nonzero_exit_code() -> None:
    function_prefix = PREDEPLOY.split('if [ "${RUN_RAILWAY_PRE_DEPLOY_MIGRATE:-0}"', 1)[0]
    completed = subprocess.run(
        ["bash", "-c", function_prefix + "\nrun_step probe bash -c 'exit 17'"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 17
    assert "RAILWAY_PREDEPLOY: FAIL step=probe rc=17" in completed.stderr


def test_capacity_checker_is_bounded_and_errors_are_redacted() -> None:
    assert "DEFAULT_CONNECT_TIMEOUT_SECONDS" in CHECKER
    assert "DEFAULT_COMMAND_TIMEOUT_SECONDS" in CHECKER
    assert "DEFAULT_TOTAL_TIMEOUT_SECONDS" in CHECKER
    assert "asyncio.wait_for" in CHECKER
    assert "error_type={type(exc).__name__}" in CHECKER
    assert "ALEMBIC_VERSION_CAPACITY_DETAIL=REDACTED" in CHECKER
    assert "str(exc)" not in CHECKER
    assert "repr(exc)" not in CHECKER


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
