"""Tests for scripts/log_invoice_event.py — invoice requires capital asset."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "log_invoice_event.py"
_spec = importlib.util.spec_from_file_location("log_invoice_event_mod", _SCRIPT)
inv = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(inv)


def _seed_capital_index(tmp_path: Path, asset_id: str) -> Path:
    p = tmp_path / "capital_index.json"
    p.write_text(json.dumps({
        "index_id": "TEST",
        "entries": [
            {
                "entry_id": asset_id,
                "asset_type": "proof_example",
                "title": "Test asset",
                "description": "D",
                "evidence": "E",
                "project_id": "p",
                "client_id": "c",
                "created_at": "2026-05-14T00:00:00+00:00",
                "git_author": "test@example.com",
            }
        ],
    }))
    return p


def test_refuses_when_capital_asset_id_missing_from_index(monkeypatch, tmp_path):
    monkeypatch.setattr(inv, "LOG_PATH", tmp_path / "log.json")
    monkeypatch.setattr(inv, "CAPITAL_INDEX", tmp_path / "absent.json")
    with pytest.raises(SystemExit):
        inv.log_invoice(
            capital_asset_id="not-found",
            buyer="Buyer",
            scope="Sprint",
            proof_target="1 Proof Pack",
        )


def test_refuses_when_capital_asset_id_does_not_match_existing(monkeypatch, tmp_path):
    capital = _seed_capital_index(tmp_path, "real-asset-id")
    monkeypatch.setattr(inv, "CAPITAL_INDEX", capital)
    monkeypatch.setattr(inv, "LOG_PATH", tmp_path / "log.json")
    with pytest.raises(SystemExit):
        inv.log_invoice(
            capital_asset_id="different-id",
            buyer="Buyer",
            scope="Sprint",
            proof_target="P",
        )


def test_succeeds_when_capital_asset_id_exists(monkeypatch, tmp_path):
    capital = _seed_capital_index(tmp_path, "real-asset-id")
    monkeypatch.setattr(inv, "CAPITAL_INDEX", capital)
    log_path = tmp_path / "log.json"
    monkeypatch.setattr(inv, "LOG_PATH", log_path)
    entry = inv.log_invoice(
        capital_asset_id="real-asset-id",
        buyer="Buyer A",
        scope="Revenue Intelligence Sprint",
        proof_target="1 Proof Pack + 1 Value Ledger entry",
        amount_sar=25000,
    )
    assert entry["capital_asset_id"] == "real-asset-id"
    assert entry["entry_id"]
    data = json.loads(log_path.read_text())
    assert data["invoice_sent_count"] == 1
    assert data["ceo_complete"] is True
    # amount_sar stored internally; verified in the public-API safety test.
    assert data["entries"][0]["amount_sar_disclosed_internally"] == 25000


def test_cli_refuses_without_really_flag(monkeypatch, tmp_path, capsys):
    capital = _seed_capital_index(tmp_path, "asset-x")
    monkeypatch.setattr(inv, "CAPITAL_INDEX", capital)
    monkeypatch.setattr(inv, "LOG_PATH", tmp_path / "log.json")
    rc = inv.main([
        "--capital-asset-id", "asset-x",
        "--buyer", "Buyer",
        "--scope", "Sprint",
        "--proof-target", "P",
    ])
    assert rc == 2  # REFUSED
    err = capsys.readouterr().err
    assert "REFUSED" in err


def test_counter_in_lockstep_with_entries(monkeypatch, tmp_path):
    capital = _seed_capital_index(tmp_path, "asset-1")
    monkeypatch.setattr(inv, "CAPITAL_INDEX", capital)
    log_path = tmp_path / "log.json"
    monkeypatch.setattr(inv, "LOG_PATH", log_path)
    for _ in range(2):
        inv.log_invoice(
            capital_asset_id="asset-1",
            buyer="B",
            scope="S",
            proof_target="P",
        )
    data = json.loads(log_path.read_text())
    assert data["invoice_sent_count"] == 2 == len(data["entries"])
