from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "railway_predeploy.sh"


def _bash_executable() -> str:
    bash = shutil.which("bash")
    assert bash, "bash is required for the Railway predeploy contract test"
    return bash


def _run(value: str | None, extra: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    if value is None:
        env.pop("RUN_RAILWAY_PRE_DEPLOY_MIGRATE", None)
    else:
        env["RUN_RAILWAY_PRE_DEPLOY_MIGRATE"] = value
    env.update(extra or {})
    return subprocess.run(
        [_bash_executable(), str(SCRIPT)],
        cwd=ROOT,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def test_non_authoritative_flags_are_safe_skip() -> None:
    for value in (None, "", "0", "yes", "true", "2"):
        result = _run(value)
        assert result.returncode == 0
        combined = result.stdout + result.stderr
        assert "SKIP migrations" in combined
        assert "MIGRATION_EXECUTION=NOT_EXECUTED" in combined


def test_legacy_migration_intent_holds_without_bricking_deploy() -> None:
    result = _run("1", {
        "DEALIX_DB_MIGRATION_AUTHORIZED": "1",
        "DATABASE_URL": "postgresql://invalid/never-used",
    })
    assert result.returncode == 0
    combined = result.stdout + result.stderr
    assert "HOLD migrations" in combined
    assert "MIGRATION_EXECUTION=NOT_EXECUTED" in combined
    assert "persistent Railway variables are not action-bound L5 authority" in combined
    assert "ACTION_HASH" in combined
    assert "checking Alembic" not in combined
    assert "alembic upgrade head" not in combined


def test_normal_predeploy_contains_no_database_mutation_command() -> None:
    source = SCRIPT.read_text(encoding="utf-8").lower()
    assert "database_url" not in source
    for forbidden in (
        "alembic upgrade",
        "alembic downgrade",
        "psql ",
        "drop database",
        "create table",
        "alter table",
        "sqlalchemy",
    ):
        assert forbidden not in source
