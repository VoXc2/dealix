"""Doctrine-as-code: every entry in a marker log must carry git provenance.

Specifically, every entry must include non-empty:
  - entry_id
  - git_author

This blocks the simplest cheat — hand-editing a JSON file to add a fake
entry without going through scripts/log_partner_outreach.py or
scripts/log_invoice_event.py.

For data/capital_asset_index.json: also asserts created_at exists.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

MARKER_FILES = (
    REPO_ROOT / "data" / "partner_outreach_log.json",
    REPO_ROOT / "data" / "first_invoice_log.json",
    REPO_ROOT / "data" / "capital_asset_index.json",
)

REQUIRED_PER_ENTRY = ("entry_id", "git_author")


def _entries(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return list(data.get("entries") or [])


def test_every_entry_has_entry_id_and_git_author():
    failures: list[str] = []
    for path in MARKER_FILES:
        for i, entry in enumerate(_entries(path)):
            for key in REQUIRED_PER_ENTRY:
                val = entry.get(key)
                if not (isinstance(val, str) and val.strip()):
                    failures.append(f"{path.name}[{i}] missing {key}")
    assert not failures, failures


def test_capital_asset_entries_have_created_at():
    failures: list[str] = []
    p = REPO_ROOT / "data" / "capital_asset_index.json"
    for i, entry in enumerate(_entries(p)):
        ts = entry.get("created_at")
        if not (isinstance(ts, str) and ts.strip()):
            failures.append(f"capital_asset_index.json[{i}] missing created_at")
    assert not failures, failures
