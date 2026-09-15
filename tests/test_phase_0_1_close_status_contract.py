from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_check_dod_is_a_status_mode_without_fake_event() -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/phase_0_1_close_helper.py"), "--check-dod"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode in {0, 1}, proc.stderr
    assert proc.returncode != 2
    assert "FIRST_PAID_DIAGNOSTIC DoD" in proc.stdout
    assert "APPENDED" not in proc.stdout


def test_append_mode_still_requires_an_explicit_event() -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/phase_0_1_close_helper.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 2
    assert "--event is required unless --check-dod is used" in proc.stderr


def test_founder_money_uses_status_only_phase_close_check() -> None:
    source = (ROOT / "scripts/ops/dealix_founder_money_command.sh").read_text(encoding="utf-8")
    assert "run_py_if_exists phase_0_1_close scripts/phase_0_1_close_helper.py --check-dod" in source
