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


def test_migration_requires_separate_db_authorization() -> None:
    env = os.environ.copy()
    env.update({
        "RUN_RAILWAY_PRE_DEPLOY_MIGRATE": "1",
        "DATABASE_URL": "postgresql://invalid/never-used",
    })
    env.pop("DEALIX_DB_MIGRATION_AUTHORIZED", None)
    result = subprocess.run(
        [_bash_executable(), str(SCRIPT)],
        cwd=ROOT,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert "DEALIX_DB_MIGRATION_AUTHORIZED must equal 1" in result.stdout
    assert "checking Alembic" not in result.stdout
    assert "alembic upgrade head" not in result.stdout
