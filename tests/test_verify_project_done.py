"""Project closure templates and Definition of Done exist."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_verify_project_done_script_passes() -> None:
    r = subprocess.run(  # noqa: S603
        [sys.executable, str(REPO / "scripts" / "verify_project_done.py")],
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr or r.stdout
