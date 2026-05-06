"""Pilot close pack script — dry-run only in test."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "dealix_pilot_499_close_pack.py"


def test_pilot_pack_contains_499_and_no_guarantee() -> None:
    out = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=True)
    text = out.stdout.lower()
    assert "499" in text
    assert "ضمان" not in out.stdout
    assert "guaranteed leads" not in text
