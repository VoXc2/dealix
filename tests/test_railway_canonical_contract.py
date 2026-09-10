"""Regression tests for the Railway config-as-code contract.

These tests are intentionally stdlib-only. They protect the repo's canonical
Railway settings from drifting back to a duplicate direct uvicorn command while
allowing the JSON config to carry the canonical source watch-path contract.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_railway_config_matches_canonical_runtime_contract() -> None:
    canonical = _read("dealix/config/railway_ui_canonical.yaml")
    toml = _read("railway.toml")
    railway_json = json.loads(_read("railway.json"))
    dockerfile = _read("Dockerfile")

    assert 'start_command_ui: ""' in canonical
    assert "start_command_canonical: /app/start.sh" in canonical
    assert "restart_max_retries: 3" in canonical

    assert re.search(r"(?m)^\s*startCommand\s*=", toml) is None
    assert railway_json["deploy"]["startCommand"] is None

    assert 'builder = "DOCKERFILE"' in toml
    assert railway_json["build"]["builder"] == "DOCKERFILE"
    assert railway_json["build"]["dockerfilePath"] == "Dockerfile"

    watch_patterns = set(railway_json["build"].get("watchPatterns", []))
    assert {
        "/*.py",
        "/**/*.py",
        "/Dockerfile",
        "/railway.json",
        "/pyproject.toml",
        "/requirements*.txt",
        "/scripts/railway_predeploy.sh",
        "/api/**",
        "/app/**",
        "/db/**",
        "/config/**",
        "/templates/**",
        "/prompts/**",
    } <= watch_patterns

    assert 'healthcheckPath = "/healthz"' in toml
    assert railway_json["deploy"]["healthcheckPath"] == "/healthz"
    assert "healthcheckTimeout = 300" in toml
    assert railway_json["deploy"]["healthcheckTimeout"] == 300

    assert 'restartPolicyType = "ON_FAILURE"' in toml
    assert railway_json["deploy"]["restartPolicyType"] == "ON_FAILURE"
    assert "restartPolicyMaxRetries = 3" in toml
    assert railway_json["deploy"]["restartPolicyMaxRetries"] == 3
    assert "numReplicas = 1" in toml
    assert railway_json["deploy"]["numReplicas"] == 1

    assert "/app/scripts/railway_predeploy.sh" in toml
    assert "/app/scripts/railway_predeploy.sh" in railway_json["deploy"]["preDeployCommand"]
    assert "/app/start.sh" in dockerfile


def test_forbidden_direct_uvicorn_start_command_is_absent() -> None:
    toml = _read("railway.toml")
    railway_json = json.loads(_read("railway.json"))

    assert "uvicorn api.main:app" not in toml
    assert railway_json["deploy"]["startCommand"] is None


def test_health_contract_is_healthz_not_retired_health_alias() -> None:
    """Railway's production readiness contract is the explicit /healthz path."""
    toml = _read("railway.toml")
    railway_json = json.loads(_read("railway.json"))

    assert 'healthcheckPath = "/healthz"' in toml
    assert railway_json["deploy"]["healthcheckPath"] == "/healthz"
