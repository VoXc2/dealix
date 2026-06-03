"""Schemas must be valid JSON Schema documents, and sample data must conform.

Uses `jsonschema` if available; otherwise falls back to lightweight structural
checks so the suite still runs in a minimal environment.
"""

import json
from pathlib import Path

import pytest

from conftest import load_json

try:
    import jsonschema  # type: ignore
    HAVE_JSONSCHEMA = True
except Exception:  # pragma: no cover
    HAVE_JSONSCHEMA = False

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"

SCHEMA_FILES = [
    "outreach_draft.schema.json",
    "approval_item.schema.json",
    "prospect.schema.json",
    "proposal.schema.json",
    "client_health.schema.json",
    "payment_handoff.schema.json",
]


@pytest.mark.parametrize("name", SCHEMA_FILES)
def test_schema_is_valid_json(name):
    schema = load_json(SCHEMA_DIR / name)
    assert schema.get("$schema"), f"{name} missing $schema"
    assert schema.get("title"), f"{name} missing title"
    assert schema.get("type") == "object", f"{name} should describe an object"


@pytest.mark.parametrize("name", SCHEMA_FILES)
def test_schema_compiles_with_jsonschema(name):
    if not HAVE_JSONSCHEMA:
        pytest.skip("jsonschema not installed")
    schema = load_json(SCHEMA_DIR / name)
    jsonschema.Draft202012Validator.check_schema(schema)


def test_approval_queue_conforms_to_schema(company_os):
    schema = load_json(SCHEMA_DIR / "approval_item.schema.json")
    queue = load_json(company_os / "governance" / "approval_queue.json")
    if HAVE_JSONSCHEMA:
        validator = jsonschema.Draft202012Validator(schema)
        for item in queue:
            errors = sorted(validator.iter_errors(item), key=lambda e: e.path)
            assert not errors, f"{item.get('id')}: {[e.message for e in errors]}"
    else:
        required = schema["required"]
        for item in queue:
            for field in required:
                assert field in item, f"{item.get('id')} missing {field}"


def test_client_health_conforms_to_schema(company_os):
    schema = load_json(SCHEMA_DIR / "client_health.schema.json")
    records = load_json(company_os / "customer_success" / "client_health.json")
    required = schema["required"]
    for rec in records:
        for field in required:
            assert field in rec, f"{rec.get('client')} missing {field}"
        assert 0 <= rec["score"] <= 100
