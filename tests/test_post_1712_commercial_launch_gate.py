from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/commercial/verify_post_1712_commercial_launch.py"
REPORT = ROOT / "reports/commercial/post_1712_launch_gate.json"
CANONICAL_AGENTS = ["dealix-pm", "dealix-sales", "dealix-delivery", "dealix-engineer", "dealix-content"]


def safe_env() -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        {
            "OUTBOUND_MODE": "draft_only",
            "EXTERNAL_SEND_ENABLED": "0",
            "EMAIL_SEND_ENABLED": "0",
            "WHATSAPP_SEND_ENABLED": "0",
            "WHATSAPP_ALLOW_LIVE_SEND": "0",
            "SMS_SEND_ENABLED": "0",
        }
    )
    return env


def test_source_gate_passes_without_claiming_deployment() -> None:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        env=safe_env(),
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "DEALIX_POST_1712_COMMERCIAL_LAUNCH=SOURCE_READY_DEPLOYMENT_UNVERIFIED" in proc.stdout
    payload = json.loads(REPORT.read_text(encoding="utf-8"))
    assert payload["status"] == "SOURCE_READY_DEPLOYMENT_UNVERIFIED"
    assert payload["deployment_verified"] is False
    assert payload["external_effects_executed"] is False
    assert payload["sector_routes"] == 20
    assert payload["canonical_agents"] == CANONICAL_AGENTS


def test_gate_contract_keeps_material_effects_outside_source_readiness() -> None:
    source = SCRIPT.read_text(encoding="utf-8")
    assert '"external_effects_executed": False' in source
    assert "source readiness does not prove deployed production identity" in source
    assert "COMMERCIAL_LAUNCH_GREEN" in source
    assert "SOURCE_READY_DEPLOYMENT_UNVERIFIED" in source
