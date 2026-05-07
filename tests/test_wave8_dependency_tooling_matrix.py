"""Wave 8 — Dependency & Tooling Matrix tests."""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MATRIX_JSON = REPO_ROOT / "docs" / "wave8" / "dependency_tooling_matrix.json"
MATRIX_MD = REPO_ROOT / "docs" / "WAVE8_DEPENDENCY_AND_TOOLING_MATRIX.md"
REQUIREMENTS_TXT = REPO_ROOT / "requirements.txt"


def test_matrix_json_exists():
    assert MATRIX_JSON.exists(), "dependency_tooling_matrix.json must exist"


def test_matrix_md_exists():
    assert MATRIX_MD.exists(), "WAVE8_DEPENDENCY_AND_TOOLING_MATRIX.md must exist"


def test_matrix_json_valid():
    data = json.loads(MATRIX_JSON.read_text(encoding="utf-8"))
    assert data["wave"] == "8"
    assert isinstance(data["matrix"], list)
    assert len(data["matrix"]) > 0


def test_matrix_json_no_new_heavy_deps():
    data = json.loads(MATRIX_JSON.read_text(encoding="utf-8"))
    assert data["new_heavy_deps_wave8"] == [], "No new heavy deps should be added in Wave 8"


def test_matrix_json_schema():
    data = json.loads(MATRIX_JSON.read_text(encoding="utf-8"))
    required_keys = {
        "tool_or_library", "category", "present", "version_or_source",
        "where_used", "needed_for_first_customer", "optional_future",
        "risk_level", "install_now", "reason", "notes"
    }
    for entry in data["matrix"]:
        missing = required_keys - set(entry.keys())
        assert not missing, f"Entry {entry.get('tool_or_library')} missing keys: {missing}"


def test_requirements_txt_exists():
    assert REQUIREMENTS_TXT.exists(), "requirements.txt must exist"


def test_no_high_risk_deps():
    data = json.loads(MATRIX_JSON.read_text(encoding="utf-8"))
    high_risk = [e["tool_or_library"] for e in data["matrix"] if e.get("risk_level") == "HIGH"]
    assert not high_risk, f"HIGH risk deps found: {high_risk}"
