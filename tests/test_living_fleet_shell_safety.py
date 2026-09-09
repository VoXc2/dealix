from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DISPATCH = ROOT / "scripts" / "ops" / "living_fleet_dispatch.sh"


def test_owner_execution_uses_structured_argv_not_shell_splitting() -> None:
    text = DISPATCH.read_text(encoding="utf-8")
    assert 'local -a argv=()' in text
    assert 'read -r -a argv <<<"$owner_cmd"' in text
    assert './.venv/bin/python "${argv[@]:1}"' in text
    assert '${cmd#.venv/bin/python }' not in text
    assert "eval " not in text


def test_terminal_pending_move_is_an_exact_path_not_a_fake_glob_loop() -> None:
    text = DISPATCH.read_text(encoding="utf-8")
    assert 'for pj in "$pending_dir/${JOB_ID}.json"; do' not in text
    assert 'pending_job="$pending_dir/${JOB_ID}.json"' in text
    assert 'mv -- "$pending_job"' in text


def test_unused_council_timer_is_not_reintroduced() -> None:
    text = DISPATCH.read_text(encoding="utf-8")
    assert "COUNCIL_T0=" not in text


def test_shellcheck_is_clean_when_available() -> None:
    shellcheck = shutil.which("shellcheck")
    if shellcheck is None:
        pytest.skip("shellcheck not installed in this test environment")
    result = subprocess.run(
        [shellcheck, str(DISPATCH)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
