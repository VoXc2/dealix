"""Smoke: verify_dealix_ready gate script."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_verify_dealix_ready_skip_tests_exits_zero() -> None:
    code = subprocess.call(  # noqa: S603
        [sys.executable, str(REPO / "scripts" / "verify_dealix_ready.py"), "--skip-tests"],
        cwd=REPO,
    )
    assert code == 0


def test_print_service_readiness_matrix_exits_zero() -> None:
    code = subprocess.call(  # noqa: S603
        [sys.executable, str(REPO / "scripts" / "print_service_readiness_matrix.py")],
        cwd=REPO,
    )
    assert code == 0
