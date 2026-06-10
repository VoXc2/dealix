"""Tests for founder commercial KPI registry apply script."""

from __future__ import annotations

from pathlib import Path

import yaml

_REPO = Path(__file__).resolve().parents[1]


def test_registry_loads_commercial_entries():
    reg = _REPO / "dealix/transformation/kpi_founder_commercial_registry.yaml"
    data = yaml.safe_load(reg.read_text(encoding="utf-8"))
    entries = data.get("commercial_entries") or {}
    assert "measured_customer_value_sar" in entries
    assert "conversion_discovery_to_pilot" in entries


def test_patch_snapshot_line_updates_value_and_ref():
    from scripts.apply_kpi_founder_commercial import _patch_snapshot_line

    text = """snapshots:
  conversion_discovery_to_pilot:
    value_numeric: null
    source_ref: ""
"""
    out = _patch_snapshot_line(text, "conversion_discovery_to_pilot", 18.5, "crm:test:2026")
    assert "value_numeric: 18.5" in out
    assert 'source_ref: "crm:test:2026"' in out


def test_verify_cutover_pr_body_requires_markers():
    from scripts.verify_cutover_pr_body import validate

    errs = validate("PROOF_LEDGER_BACKEND=postgres")
    assert len(errs) == 2
    ok = validate(
        "PROOF_LEDGER_BACKEND=dual\nexternal_signal: pilot_scope_locked\n"
        "contract_or_pilot_ref: acct-001"
    )
    assert ok == []


def test_forbidden_commercial_source_ref():
    from scripts.apply_kpi_founder_commercial import _validate_ref

    assert _validate_ref("x", "crm:REPLACE:foo") is not None
    assert _validate_ref("x", "crm:hubspot:deal:1;period=2026-Q1") is None
