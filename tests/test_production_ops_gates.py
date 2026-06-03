#!/usr/bin/env python3
"""Smoke tests for production ops gate scripts."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_action_catalog_has_risk_tier() -> None:
    from auto_client_acquisition.revenue_os.action_catalog import list_action_catalog

    rows = list_action_catalog()
    assert rows
    assert all(r.get("risk_tier") in {"green", "yellow", "red"} for r in rows)


def test_railway_frontend_dns_gate_runs() -> None:
    env = {**dict(os.environ), "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts/railway_frontend_dns_gate.py"), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
        env=env,
    )
    assert r.returncode in (0, 1)
    assert "layer_4_ok" in (r.stdout or r.stderr)


def test_verify_integrations_activation_runs() -> None:
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts/verify_integrations_activation.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert "INTEGRATIONS_ACTIVATION_VERDICT=" in r.stdout
