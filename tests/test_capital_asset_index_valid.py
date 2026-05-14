"""Doctrine commitment #10: Capital Asset registration before invoice.

This test ensures `data/capital_asset_index.json`:
  - exists and is valid JSON,
  - every entry passes `capital_ledger_event_valid()`,
  - every entry has `entry_id`, `created_at`, `git_author`.

The verifier matrix references this exact test name.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = REPO_ROOT / "data" / "capital_asset_index.json"


def test_capital_asset_index_file_exists():
    assert INDEX_PATH.exists(), (
        f"missing {INDEX_PATH.relative_to(REPO_ROOT)}. "
        "Run `python scripts/generate_capital_asset_index.py`."
    )


def test_capital_asset_index_is_valid_json():
    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    assert "entries" in data
    assert isinstance(data["entries"], list)


def test_every_capital_asset_entry_passes_validator():
    from auto_client_acquisition.capital_os.asset_types import CapitalAssetType
    from auto_client_acquisition.capital_os.capital_ledger import (
        CapitalLedgerEvent,
        capital_ledger_event_valid,
    )

    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    valid_types = {t.value for t in CapitalAssetType}

    for i, entry in enumerate(data.get("entries") or []):
        # Provenance fields.
        for key in ("entry_id", "created_at", "git_author"):
            val = entry.get(key)
            assert isinstance(val, str) and val.strip(), (
                f"entry[{i}] missing {key}"
            )
        # Asset type must be known.
        atype = str(entry.get("asset_type") or "")
        assert atype in valid_types, f"entry[{i}] unknown asset_type {atype!r}"
        # CapitalLedgerEvent contract.
        ev = CapitalLedgerEvent(
            capital_event_id=str(entry["entry_id"]),
            project_id=str(entry.get("project_id") or ""),
            client_id=str(entry.get("client_id") or ""),
            asset_type=atype,
            title=str(entry.get("title") or ""),
            description=str(entry.get("description") or ""),
            evidence=str(entry.get("evidence") or ""),
        )
        assert capital_ledger_event_valid(ev), (
            f"entry[{i}] fails capital_ledger_event_valid"
        )
