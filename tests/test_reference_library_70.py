"""Verify the v10 reference library YAML stays clean."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
YAML_PATH = REPO_ROOT / "docs" / "v10" / "REFERENCE_LIBRARY_70.yaml"


@pytest.fixture(scope="module")
def data() -> dict:
    assert YAML_PATH.exists()
    return yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))


def test_yaml_loads(data: dict):
    assert isinstance(data, dict)
    assert isinstance(data.get("projects"), list)


def test_at_least_70_tools(data: dict):
    assert len(data["projects"]) >= 70


def test_all_ids_unique(data: dict):
    ids = [p["id"] for p in data["projects"]]
    assert len(ids) == len(set(ids))


def test_required_keys_present(data: dict):
    required = {
        "id", "name", "repo", "category", "dealix_value",
        "tier", "priority", "status", "risks",
        "license_to_verify", "founder_decision_required",
    }
    for p in data["projects"]:
        missing = required - set(p.keys())
        assert not missing, f"{p.get('id', '?')}: missing {missing}"


def test_no_real_dependency_without_founder_decision(data: dict):
    for p in data["projects"]:
        if p["tier"] == "real_dependency":
            assert p["founder_decision_required"] is True, (
                f"{p['id']}: real_dependency requires founder_decision_required=true"
            )


def test_top_10_p0_picks_include_open_design(data: dict):
    p0 = [
        p for p in data["projects"]
        if p["priority"] == "P0" and p["status"] in {"shipped", "selected"}
    ]
    ids = {p["id"] for p in p0}
    assert "open_design" in ids
    # Sanity: at least 5 P0 picks
    assert len(p0) >= 5


def test_open_design_marked_shipped(data: dict):
    for p in data["projects"]:
        if p["id"] == "open_design":
            assert p["status"] == "shipped"
            return
    raise AssertionError("open_design entry missing")


def test_no_scraping_tool_defaults_to_real_dependency(data: dict):
    for p in data["projects"]:
        haystack = " ".join([
            str(p.get("dealix_value", "")),
            " ".join(p.get("patterns_to_adapt") or []),
        ]).lower()
        if "scrape" in haystack or "scraping" in haystack:
            assert p["tier"] != "real_dependency", (
                f"{p['id']}: scraping-capable tool cannot default to real_dependency"
            )


def test_verifier_script_runs_clean():
    """Run scripts/verify_reference_library_70.py and assert exit 0."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    try:
        import verify_reference_library_70 as v
    finally:
        sys.path.pop(0)

    rc = v.main([])
    assert rc == 0


def test_categories_align_with_12_layer_plan(data: dict):
    valid_categories = {
        "ai_workforce", "workflow_durability", "crm_revops",
        "customer_inbox", "growth_analytics", "knowledge_rag",
        "llm_gateway", "observability", "safety_evals",
        "platform_auth", "designops_artifacts", "founder_command_center",
    }
    found = {p["category"] for p in data["projects"]}
    invalid = found - valid_categories
    assert not invalid, f"unknown categories: {invalid}"
