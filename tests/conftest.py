"""Shared pytest helpers for the Dealix factory checks."""
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def run_check():
    """Run a repo-relative check script and return the completed process."""
    def _run(rel_path, *args):
        proc = subprocess.run(
            [sys.executable, str(ROOT / rel_path), *args],
            capture_output=True,
            text=True,
        )
        return proc
    return _run
