"""Warm intro board generator — placeholders only."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "dealix_first10_warm_intros.py"


def test_script_dry_run_json() -> None:
    out = subprocess.run(
        [sys.executable, str(SCRIPT), "--dry-run"],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(out.stdout)
    assert data["guardrails"]["no_cold_whatsapp"] is True
    assert len(data["slots"]) == 10
    for s in data["slots"]:
        assert "@" not in json.dumps(s)
        assert "+966" not in json.dumps(s)
