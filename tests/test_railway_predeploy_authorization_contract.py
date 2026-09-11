from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "railway_predeploy.sh"


def _bash_executable() -> str:
    if os.name == "nt":
        candidates = [
            Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Git" / "bin" / "bash.exe",
            Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Git" / "bin" / "bash.exe",
        ]
        for candidate in candidates:
            if candidate.is_file():
                return str(candidate)
    bash = shutil.which("bash")
    assert bash, "bash is required for the Railway predeploy contract test"
    return bash


def _run(env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [_bash_executable(), str(SCRIPT)], cwd=ROOT, env=env, text=True,
        encoding="utf-8", errors="replace", capture_output=True, check=False,
    )


def test_migrations_disabled_is_safe_skip() -> None:
    env = os.environ.copy()
    env["RUN_RAILWAY_PRE_DEPLOY_MIGRATE"] = "0"
    result = _run(env)
    assert result.returncode == 0
    assert "SKIP migrations" in result.stdout


def test_persistent_flags_cannot_authorize_production_ddl() -> None:
    env = os.environ.copy()
    env.update({
        "RUN_RAILWAY_PRE_DEPLOY_MIGRATE": "1",
        "DEALIX_DB_MIGRATION_AUTHORIZED": "1",
        "DATABASE_URL": "postgresql://invalid/never-used",
    })
    result = _run(env)
    assert result.returncode == 75
    combined = result.stdout + result.stderr
    assert "persistent Railway variables are not action-bound L5 authority" in combined
    assert "ACTION_HASH" in combined
    assert "checking Alembic" not in combined
    assert "alembic upgrade head" not in combined
