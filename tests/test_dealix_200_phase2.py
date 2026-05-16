"""Dealix 200 registry and phase-2 fields."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]


def test_registry_has_200_initiatives() -> None:
    data = yaml.safe_load(
        (REPO / "dealix/transformation/strategic_initiatives_registry.yaml").read_text(encoding="utf-8")
    )
    assert data.get("program") == "dealix_200_strategic_initiatives"
    initiatives = data.get("initiatives") or []
    assert len(initiatives) == 200
    assert {r["id"] for r in initiatives} == set(range(1, 201))
    phase2 = [r for r in initiatives if r.get("phase") == 2]
    assert len(phase2) == 100
    assert all(r.get("wave", 0) >= 11 for r in phase2)


def test_verify_200_initiatives() -> None:
    env = {**dict(__import__("os").environ), "DEALIX_INITIATIVE_TARGET": "200"}
    proc = subprocess.run(
        [sys.executable, "scripts/verify_global_ai_transformation.py", "--check-initiatives"],
        cwd=REPO,
        capture_output=True,
        text=True,
        env=env,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
