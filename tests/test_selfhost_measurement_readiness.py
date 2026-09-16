from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "scripts/ops/verify_measurement_readiness.py"


def run(env_file: Path) -> str:
    proc = subprocess.run(
        ["python3", str(VERIFY), "--env-file", str(env_file)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return proc.stdout


def test_selfhost_posthog_build_wiring_and_privacy_contract() -> None:
    dockerfile = (ROOT / "apps/web/Dockerfile").read_text()
    compose = (ROOT / "deploy/selfhost/compose.yml").read_text()
    posthog = (ROOT / "apps/web/lib/analytics/posthog.tsx").read_text()
    assert 'ARG NEXT_PUBLIC_POSTHOG_KEY=""' in dockerfile
    assert 'ARG NEXT_PUBLIC_POSTHOG_HOST="https://us.i.posthog.com"' in dockerfile
    assert "NEXT_PUBLIC_POSTHOG_KEY: ${NEXT_PUBLIC_POSTHOG_KEY:-}" in compose
    assert "NEXT_PUBLIC_POSTHOG_HOST: ${NEXT_PUBLIC_POSTHOG_HOST:-https://us.i.posthog.com}" in compose
    for token in (
        'consent !== "granted"', "autocapture: false", "capture_pageview: false",
        "capture_pageleave: false", "disable_session_recording: true",
        'person_profiles: "identified_only"',
    ):
        assert token in posthog


def test_missing_runtime_config_is_not_interpreted_as_zero_demand(tmp_path: Path) -> None:
    env_file = tmp_path / "prod.env"
    env_file.write_text("DEALIX_APP_ENV=production\n", encoding="utf-8")
    out = run(env_file)
    assert "MEASUREMENT_SOURCE_WIRING=PASS" in out
    assert "POSTHOG_KEY_CONFIGURED=NO" in out
    assert "MEASUREMENT_STATE=MEASUREMENT_NOT_PROVEN" in out
    assert "TRAFFIC_OR_DEMAND_INFERENCE=PROHIBITED_WITHOUT_EVENTS" in out


def test_configured_key_is_still_not_event_proof(tmp_path: Path) -> None:
    env_file = tmp_path / "prod.env"
    env_file.write_text(
        "NEXT_PUBLIC_POSTHOG_KEY=phc_test_public_project_key\n"
        "NEXT_PUBLIC_POSTHOG_HOST=https://us.i.posthog.com\n",
        encoding="utf-8",
    )
    out = run(env_file)
    assert "POSTHOG_KEY_CONFIGURED=YES" in out
    assert "POSTHOG_HOST_EXPLICIT=YES" in out
    assert "MEASUREMENT_STATE=CONFIGURED_NOT_EVENT_PROOF" in out
    assert "phc_test" not in out
