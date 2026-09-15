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
