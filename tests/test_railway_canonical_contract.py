"""Regression tests for the Railway config-as-code contract.

These tests are intentionally stdlib-only. They protect the repo's canonical
Railway settings from drifting back to a duplicate direct uvicorn command while
allowing the JSON config to carry the canonical source watch-path contract.
"""

from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_railway_config_matches_canonical_runtime_contract() -> None:
    canonical = _read("dealix/config/railway_ui_canonical.yaml")
    toml_text = _read("railway.toml")
    toml = tomllib.loads(toml_text)
    railway_json = json.loads(_read("railway.json"))
    dockerfile = _read("Dockerfile")

    assert 'start_command_ui: ""' in canonical
    assert "start_command_canonical: /app/start.sh" in canonical
    assert "restart_max_retries: 3" in canonical

    assert re.search(r"(?m)^\s*startCommand\s*=", toml_text) is None
    assert railway_json["deploy"]["startCommand"] is None

    assert toml["build"]["builder"] == "DOCKERFILE"
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

    assert toml["deploy"]["healthcheckPath"] == "/healthz"
    assert railway_json["deploy"]["healthcheckPath"] == "/healthz"
    assert toml["deploy"]["healthcheckTimeout"] == 300
    assert railway_json["deploy"]["healthcheckTimeout"] == 300

    assert toml["deploy"]["restartPolicyType"] == "ON_FAILURE"
    assert railway_json["deploy"]["restartPolicyType"] == "ON_FAILURE"
    assert toml["deploy"]["restartPolicyMaxRetries"] == 3
    assert railway_json["deploy"]["restartPolicyMaxRetries"] == 3
    assert toml["deploy"]["numReplicas"] == 1
    assert railway_json["deploy"]["numReplicas"] == 1

    assert "preDeployCommand" not in toml["deploy"]
    assert "preDeployCommand" not in railway_json["deploy"]
    assert "/app/start.sh" in dockerfile


def test_forbidden_direct_uvicorn_start_command_is_absent() -> None:
    toml_text = _read("railway.toml")
    railway_json = json.loads(_read("railway.json"))

    assert "uvicorn api.main:app" not in toml_text
    assert railway_json["deploy"]["startCommand"] is None


def test_health_contract_is_healthz_not_retired_health_alias() -> None:
    toml = tomllib.loads(_read("railway.toml"))
    railway_json = json.loads(_read("railway.json"))

    assert toml["deploy"]["healthcheckPath"] == "/healthz"
    assert railway_json["deploy"]["healthcheckPath"] == "/healthz"


def test_automatic_predeploy_is_disabled_fail_closed() -> None:
    toml = tomllib.loads(_read("railway.toml"))
    railway_json = json.loads(_read("railway.json"))

    assert "preDeployCommand" not in toml["deploy"]
    assert "preDeployCommand" not in railway_json["deploy"]
    script = _read("scripts/railway_predeploy.sh")
    assert "MIGRATION_EXECUTION=NOT_EXECUTED" in script
