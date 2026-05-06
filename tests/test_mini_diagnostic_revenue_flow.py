"""Diagnostic CLI — JSON mode has approval and guardrails."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "dealix_diagnostic.py"


def test_diagnostic_json_guardrails() -> None:
    out = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--company",
            "Test Co",
            "--sector",
            "b2b_services",
            "--region",
            "riyadh",
            "--pipeline-state",
            "inbound only",
            "--json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(out.stdout)
    assert data["approval_status"] == "approval_required"
    assert data["guardrails"]["no_live_send"] is True
    assert data["guardrails"]["no_cold_outreach"] is True
