"""Smoke test for runtime contracts script."""

from __future__ import annotations

import json
import subprocess


def test_runtime_contract_script_passes() -> None:
    proc = subprocess.run(
        ["python3", "scripts/check_runtime_contracts.py"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True
    assert len(payload["checks"]) >= 4
