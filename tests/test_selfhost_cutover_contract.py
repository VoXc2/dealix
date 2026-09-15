from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_selfhost_cutover_contract() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/ops/verify_selfhost_production_cutover_contract.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "SELFHOST_CUTOVER_CONTRACT=PASS" in result.stdout


def test_single_runnable_selfhost_plane() -> None:
    """deploy/selfhost/compose.yml is the only runnable plane; the retired
    stack must not define any runnable service."""
    canonical = (ROOT / "deploy/selfhost/compose.yml").read_text(encoding="utf-8")
    retired = (ROOT / "docker-compose.prod.yml").read_text(encoding="utf-8")
    assert "services: {}" in retired
    assert "container_name: dealix" not in retired
    assert "api:" in canonical and "web:" in canonical
    assert "127.0.0.1:${DEALIX_SELFHOST_API_PORT" in canonical
    assert "127.0.0.1:${DEALIX_SELFHOST_WEB_PORT" in canonical


def test_exact_sha_and_explicit_cutover_gates() -> None:
    """Exact full-SHA gates plus explicit flags; no silent cutover path."""
    canary = (ROOT / "scripts/ops/deploy_selfhosted_canary.sh").read_text(encoding="utf-8")
    rollback = (ROOT / "scripts/ops/selfhost_release_rollback.sh").read_text(encoding="utf-8")
    migrate = (ROOT / "scripts/ops/migrate_railway_backup_to_selfhost.py").read_text(encoding="utf-8")
    assert "DEALIX_EXPECTED_SHA" in canary
    assert "exact-head mismatch" in canary
    assert "[0-9a-f]{40}" in rollback
    assert "DEALIX_DB_MIGRATION" in migrate
    assert "PUBLIC_CUTOVER=NOT_EXECUTED" in canary


def test_no_production_secrets_in_repo() -> None:
    """Real .env.prod is never tracked; only the CHANGE_ME template ships."""
    tracked = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.splitlines()
    assert ".env.prod" not in tracked
    assert ".env.prod.example" in tracked
    template = (ROOT / ".env.prod.example").read_text(encoding="utf-8")
    assert "CHANGE_ME" in template
