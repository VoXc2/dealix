"""Tests for the model registry (schema-conformant).

Validates data/ai_ops/model_registry.yaml against the existing
schemas/model_registry.schema.json (the dealix.sa "Model Registry Entry"
schema). Asserts:
- the file is well-formed (parses),
- the schema validates the parsed result,
- every model_id is unique,
- every entry has at least one allowed_task,
- cost_class is in the allowed enum,
- forbidden tasks do not appear in allowed tasks for the same entry.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

REGISTRY_PATH = ROOT / "data" / "ai_ops" / "model_registry.yaml"
SCHEMA_PATH = ROOT / "schemas" / "model_registry.schema.json"

VALID_TASKS = {"R1", "R2", "R3"}
VALID_COST_CLASS = {"free", "low", "medium", "high"}
VALID_PII = {"allow", "redact", "forbid"}
VALID_STATUS = {"active", "deprecated", "testing", "paused"}


def _yaml_or_skip():
    try:
        import yaml  # type: ignore

        return yaml
    except ImportError:
        return None


def _load_registry():
    if not REGISTRY_PATH.exists():
        pytest.skip(f"Registry not found at {REGISTRY_PATH}")
    yaml = _yaml_or_skip()
    if yaml is None:
        pytest.skip("PyYAML not installed; skipping registry parse test")
    return yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))


def _load_schema():
    if not SCHEMA_PATH.exists():
        pytest.skip(f"Schema not found at {SCHEMA_PATH}")
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def test_registry_loads():
    data = _load_registry()
    assert isinstance(data, dict)
    # The dealix.sa schema validates per-entry, not the whole file.
    # The YAML wraps the list under `entries: [...]`.
    assert "entries" in data
    assert isinstance(data["entries"], list)
    assert len(data["entries"]) >= 1


def test_each_entry_validates_against_schema():
    data = _load_registry()
    schema = _load_schema()
    try:
        import jsonschema  # type: ignore

    except ImportError:
        pytest.skip("jsonschema not installed; skipping schema validation test")
    for entry in data["entries"]:
        # YAML parses ISO date-times as datetime.datetime; the schema declares
        # them as strings. Coerce before validation.
        if "added_at" in entry and hasattr(entry["added_at"], "isoformat"):
            entry["added_at"] = entry["added_at"].isoformat()
        jsonschema.validate(instance=entry, schema=schema)


def test_model_ids_are_unique():
    data = _load_registry()
    ids = [e["model_id"] for e in data["entries"]]
    assert len(ids) == len(set(ids)), f"Duplicate model_ids: {ids}"


def test_every_entry_has_at_least_one_allowed_task():
    data = _load_registry()
    for e in data["entries"]:
        assert e.get("allowed_tasks"), f"Entry {e.get('model_id')} has no allowed_tasks"


def test_cost_class_is_valid():
    data = _load_registry()
    for e in data["entries"]:
        assert e.get("cost_class") in VALID_COST_CLASS, e.get("model_id")


def test_pii_policy_is_valid():
    data = _load_registry()
    for e in data["entries"]:
        assert e.get("pii_policy") in VALID_PII, e.get("model_id")


def test_status_is_valid():
    data = _load_registry()
    for e in data["entries"]:
        assert e.get("status") in VALID_STATUS, e.get("model_id")


def test_forbidden_tasks_do_not_overlap_allowed_tasks():
    data = _load_registry()
    for e in data["entries"]:
        allowed = set(e.get("allowed_tasks") or [])
        forbidden = set(e.get("forbidden_tasks") or [])
        overlap = allowed & forbidden
        assert not overlap, (
            f"Entry {e.get('model_id')}: tasks {overlap} are both allowed and forbidden"
        )


def test_all_tasks_are_in_known_taxonomy():
    data = _load_registry()
    for e in data["entries"]:
        for task in e.get("allowed_tasks") or []:
            assert task in VALID_TASKS, f"{e.get('model_id')}: unknown allowed task {task}"
        for task in e.get("forbidden_tasks") or []:
            assert task in VALID_TASKS, f"{e.get('model_id')}: unknown forbidden task {task}"
