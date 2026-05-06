"""Frontend-data tests for the Service Activation Console.

Verifies the JSON exporter produces a payload that:
  - Mirrors the YAML counts (32 services, 0 live, etc.)
  - Includes all 6 bundles
  - Carries the full per-service payload the renderer expects
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
MATRIX = REPO / "docs" / "registry" / "SERVICE_READINESS_MATRIX.yaml"
JSON_OUT = REPO / "landing" / "assets" / "data" / "service-readiness.json"
EXPORTER = REPO / "scripts" / "export_service_readiness_json.py"


def test_exporter_produces_json():
    res = subprocess.run(
        [sys.executable, str(EXPORTER)],
        cwd=str(REPO), capture_output=True, text=True,
    )
    assert res.returncode == 0, res.stderr
    assert JSON_OUT.exists()


def test_json_counts_match_yaml():
    """After Phase K1-K6 (PR #165 + #166 + #167), 6 services flipped
    to live in the YAML. The exporter must produce the same counts."""
    with MATRIX.open("r", encoding="utf-8") as f:
        m = yaml.safe_load(f)
    with JSON_OUT.open("r", encoding="utf-8") as f:
        j = json.load(f)
    assert j["counts"]["total"] == len(m["services"]) == 32
    assert j["counts"]["live"] == 8
    assert j["counts"]["pilot"] == 0
    assert j["counts"]["partial"] == 0
    assert j["counts"]["target"] == 24
    assert j["counts"]["blocked"] == 0


def test_json_includes_all_bundles():
    with JSON_OUT.open("r", encoding="utf-8") as f:
        j = json.load(f)
    ids = {b["id"] for b in j["bundles"]}
    assert {
        "growth_starter", "data_to_revenue", "executive_growth_os",
        "partnership_growth", "full_control_tower", "internal",
    }.issubset(ids)


def test_json_services_carry_required_fields():
    with JSON_OUT.open("r", encoding="utf-8") as f:
        j = json.load(f)
    needed = {
        "service_id", "name_ar", "name_en", "bundle", "status",
        "customer_value_ar", "customer_value_en",
        "next_activation_step_ar", "next_activation_step_en",
        "deliverables", "proof_metrics", "blocked_actions",
        "safe_action_policy", "tests_required", "evidence",
    }
    for svc in j["services"]:
        missing = needed - svc.keys()
        assert not missing, f"{svc.get('service_id')}: {missing}"


def test_json_metadata_present():
    with JSON_OUT.open("r", encoding="utf-8") as f:
        j = json.load(f)
    assert j.get("source_file") == "docs/registry/SERVICE_READINESS_MATRIX.yaml"
    assert j.get("last_updated")
    assert j.get("owner")
