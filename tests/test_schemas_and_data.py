"""Validate bundled JSON schemas and the data files that must conform to them."""

import json
import os

import pytest

from core.safety.schema_check import validate, load_schema

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_DIR = os.path.join(ROOT, "schemas")

SCHEMA_FILES = [
    "suppression.schema.json",
    "vendor.schema.json",
    "legal_review.schema.json",
    "case_study_permission.schema.json",
    "productized_service.schema.json",
]


@pytest.mark.parametrize("name", SCHEMA_FILES)
def test_schema_is_valid_json(name):
    schema = load_schema(os.path.join(SCHEMA_DIR, name))
    assert schema.get("$schema")
    assert schema.get("type") == "object"
    assert "required" in schema


def test_vendors_data_conforms():
    schema = load_schema(os.path.join(SCHEMA_DIR, "vendor.schema.json"))
    path = os.path.join(ROOT, "data", "procurement", "vendors.jsonl")
    with open(path, "r", encoding="utf-8") as f:
        rows = [json.loads(l) for l in f if l.strip()]
    assert rows
    for row in rows:
        ok, errors = validate(row, schema)
        assert ok, f"vendor {row.get('id')} invalid: {errors}"


def test_services_data_conforms():
    yaml = pytest.importorskip("yaml")  # CI installs PyYAML; skip if absent locally
    schema = load_schema(os.path.join(SCHEMA_DIR, "productized_service.schema.json"))
    path = os.path.join(ROOT, "data", "productized_services", "services.yaml")
    with open(path, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    services = doc.get("services", [])
    assert services
    for svc in services:
        ok, errors = validate(svc, schema)
        assert ok, f"service {svc.get('id')} invalid: {errors}"


def test_suppression_example_conforms():
    schema = load_schema(os.path.join(SCHEMA_DIR, "suppression.schema.json"))
    example = {
        "contact": "ceo@example.sa",
        "reason": "unsubscribe",
        "added_at": "2026-06-03T10:00:00+03:00",
        "source": "reply_handling",
    }
    ok, errors = validate(example, schema)
    assert ok, errors


def test_validator_rejects_bad_enum():
    schema = load_schema(os.path.join(SCHEMA_DIR, "suppression.schema.json"))
    bad = {"contact": "x@y.sa", "reason": "nonsense", "added_at": "t", "source": "s"}
    ok, errors = validate(bad, schema)
    assert ok is False and errors
