"""Company OS verify scripts — smoke tests."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]


def _run_script(name: str) -> int:
    return subprocess.call(  # noqa: S603
        [sys.executable, str(REPO / "scripts" / name)],
        cwd=REPO,
    )


def test_service_files_script_exits_zero() -> None:
    assert _run_script("verify_service_files.py") == 0


def test_service_catalog_script_exits_zero() -> None:
    assert _run_script("verify_service_catalog.py") == 0


def test_service_id_map_loads() -> None:
    mp = yaml.safe_load((REPO / "docs" / "company" / "SERVICE_ID_MAP.yaml").read_text(encoding="utf-8"))
    assert mp.get("version") == 1
    folders = {r["folder"] for r in mp["mappings"]}
    assert "lead_intelligence_sprint" in folders
