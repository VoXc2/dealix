"""revenue_execution_verify.sh exists and is executable."""

from __future__ import annotations

import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "revenue_execution_verify.sh"


def test_verify_script_exists_and_executable() -> None:
    assert SCRIPT.is_file()
    assert os.access(SCRIPT, os.X_OK)
