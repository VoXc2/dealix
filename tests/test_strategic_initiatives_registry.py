"""Strategic initiatives registry and verify hook."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]


def test_registry_has_100_initiatives() -> None:
    data = yaml.safe_load(
        (REPO / "dealix/transformation/strategic_initiatives_registry.yaml").read_text(encoding="utf-8")
    )
    initiatives = data.get("initiatives") or []
    assert len(initiatives) == 100
    ids = {r["id"] for r in initiatives}
    assert ids == set(range(1, 101))


def test_verify_check_initiatives_passes() -> None:
    proc = subprocess.run(
        [sys.executable, "scripts/verify_global_ai_transformation.py", "--check-initiatives"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
