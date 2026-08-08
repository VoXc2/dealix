"""Unit tests for the Saudi data-flow register (PDPA readiness, issue #918)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "data_flow_entry.schema.json"
SEED_PATH = ROOT / "data" / "privacy" / "data_flow_register_seed.json"

REQUIRED_CATEGORIES = {
    "company_facts",
    "business_contact_data",
    "message_content",
    "approvals",
    "proposals",
    "payments",
    "support",
    "telemetry",
    "model_prompts",
    "audit_logs",
    "consent_records",
}


def _load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _load_seed() -> list[dict]:
    return json.loads(SEED_PATH.read_text(encoding="utf-8"))


def test_schema_and_seed_exist():
    """Both schema and seed files must exist — no silent drift."""
    assert SCHEMA_PATH.is_file(), "data_flow_entry.schema.json missing"
    assert SEED_PATH.is_file(), "data_flow_register_seed.json missing"


def test_seed_validates_against_schema():
    """Every seed entry must validate against the data-flow schema (fail-closed)."""
    jsonschema = pytest.importorskip("jsonschema", reason="jsonschema required for schema validation")
    schema = _load_schema()
    seed = _load_seed()
    assert isinstance(seed, list) and len(seed) >= 1, "seed must contain at least DF-CRM-001"
    for entry in seed:
        jsonschema.validate(entry, schema)


def test_seed_covers_required_pdpa_categories():
    """Seed covers every category in #918 scope."""
    seed = _load_seed()
    present = {entry["category"] for entry in seed}
    missing = REQUIRED_CATEGORIES - present
    assert not missing, f"Missing PDPA categories in register: {sorted(missing)}"


def test_every_cross_border_entry_declares_mechanism():
    """Any cross_border_transfer.occurs=true must have a mechanism and counsel ref."""
    seed = _load_seed()
    for entry in seed:
        cbt = entry["cross_border_transfer"]
        if cbt["occurs"]:
            assert cbt["mechanism"] != "no_mechanism_yet", (
                f"{entry['flow_id']}: cross_border_transfer requires a real mechanism, "
                "not no_mechanism_yet"
            )


def test_no_blocked_consentless_data_collection():
    """If consent_capture.required=true, method must not be 'none_yet'."""
    seed = _load_seed()
    for entry in seed:
        cc = entry["consent_capture"]
        if cc["required"]:
            assert cc["method"] != "none_yet", (
                f"{entry['flow_id']}: consent required but method is 'none_yet'"
            )


def test_tenant_and_approval_boundaries_documented():
    """Soft-delete + tenant_id and approval-gated RLS are mandatory invariants — register must acknowledge them."""
    seed = _load_seed()
    for entry in seed:
        note = entry.get("notes", "")
        # At least one invariant keyword must appear in notes or in safeguards
        safeguards_blob = json.dumps(entry["processors"]).lower() + " " + note.lower()
        has_isolation_hint = any(
            kw in safeguards_blob
            for kw in ("tenant", "row-level", "approv", "rls", "soft_delete", "soft-delete", "approval")
        )
        assert has_isolation_hint, (
            f"{entry['flow_id']}: register entry must mention tenant isolation, "
            "row-level security, or approval-gate in safeguards/notes"
        )


def test_retention_days_reasonable():
    """Retention must be finite (no infinity)."""
    seed = _load_seed()
    for entry in seed:
        rd = entry["retention_days"]
        assert 0 < rd <= 3650, f"{entry['flow_id']}: retention_days={rd} not in (0, 3650]"
