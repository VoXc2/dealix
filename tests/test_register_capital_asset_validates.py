"""Tests for scripts/register_capital_asset.py."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "register_capital_asset.py"
_spec = importlib.util.spec_from_file_location("register_capital_asset_mod", _SCRIPT)
register = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(register)


def test_register_appends_entry_and_records_provenance(tmp_path, monkeypatch):
    idx = tmp_path / "idx.json"
    monkeypatch.setattr(register, "INDEX_PATH", idx)

    rec = register.register(
        asset_type="proof_example",
        title="T",
        description="D",
        evidence="E",
    )
    assert rec["asset_type"] == "proof_example"
    assert rec["entry_id"]
    assert rec["created_at"]
    assert rec["git_author"]  # set, even if "unknown"
    assert idx.exists()
    data = json.loads(idx.read_text())
    assert len(data["entries"]) == 1


def test_register_rejects_unknown_asset_type(tmp_path, monkeypatch):
    idx = tmp_path / "idx.json"
    monkeypatch.setattr(register, "INDEX_PATH", idx)
    with pytest.raises(SystemExit):
        register.register(
            asset_type="not_a_real_type",
            title="T", description="D", evidence="E",
        )


def test_register_rejects_empty_fields(tmp_path, monkeypatch):
    idx = tmp_path / "idx.json"
    monkeypatch.setattr(register, "INDEX_PATH", idx)
    with pytest.raises(SystemExit):
        register.register(
            asset_type="proof_example",
            title="",  # invalid: empty
            description="D",
            evidence="E",
        )


def test_register_validates_via_capital_ledger_event_valid(tmp_path, monkeypatch):
    """The script must reuse the existing validator (not invent a new one)."""
    idx = tmp_path / "idx.json"
    monkeypatch.setattr(register, "INDEX_PATH", idx)
    # Should succeed for a well-formed entry.
    rec = register.register(
        asset_type="scoring_rule",
        title="Saudi mid-market scoring",
        description="A rubric tuned for Saudi B2B services 40-500 headcount.",
        evidence="auto_client_acquisition/revenue_os/account_scoring.py",
        project_id="dealix-internal",
        client_id="internal",
    )
    assert rec["title"].startswith("Saudi")
    # And the saved entry passes the original validator.
    from auto_client_acquisition.capital_os.capital_ledger import (
        CapitalLedgerEvent,
        capital_ledger_event_valid,
    )
    ev = CapitalLedgerEvent(
        capital_event_id=rec["entry_id"],
        project_id=rec["project_id"],
        client_id=rec["client_id"],
        asset_type=rec["asset_type"],
        title=rec["title"],
        description=rec["description"],
        evidence=rec["evidence"],
    )
    assert capital_ledger_event_valid(ev) is True


def test_register_increments_count_in_place(tmp_path, monkeypatch):
    idx = tmp_path / "idx.json"
    monkeypatch.setattr(register, "INDEX_PATH", idx)
    register.register(asset_type="proof_example", title="A", description="D", evidence="E")
    register.register(asset_type="proof_example", title="B", description="D", evidence="E")
    register.register(asset_type="sector_insight", title="C", description="D", evidence="E")
    data = json.loads(idx.read_text())
    assert len(data["entries"]) == 3
    titles = [e["title"] for e in data["entries"]]
    assert titles == ["A", "B", "C"]
