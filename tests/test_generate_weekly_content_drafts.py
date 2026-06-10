"""Unit tests for weekly LinkedIn content draft generator."""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
_MOD_PATH = REPO_ROOT / "scripts" / "generate_weekly_content_drafts.py"
_spec = importlib.util.spec_from_file_location("generate_weekly_content_drafts", _MOD_PATH)
assert _spec and _spec.loader
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

BANNED_PHRASES = _mod.BANNED_PHRASES
build_drafts = _mod.build_drafts
parse_aeo_weeks = _mod.parse_aeo_weeks

AEO_PATH = REPO_ROOT / "docs/commercial/operations/AEO_CONTENT_CALENDAR_AR.md"


def test_parse_aeo_calendar_has_rows() -> None:
    rows = parse_aeo_weeks(AEO_PATH)
    assert len(rows) >= 10
    assert rows[0]["slug"]
    assert rows[0]["title_ar"]


def test_build_five_drafts_no_banned_phrases() -> None:
    drafts = build_drafts(count=5)
    assert len(drafts) == 5
    for d in drafts:
        body = str(d["body"]).lower()
        for banned in BANNED_PHRASES:
            assert banned.lower() not in body
        assert d["status"] == "draft_pending_approval"
        assert d["channel"] == "linkedin"


def test_main_writes_json(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(_mod, "OUT_DIR", tmp_path)
    assert _mod.main([]) == 0
    files = list(tmp_path.glob("*.json"))
    assert len(files) == 1
    payload = json.loads(files[0].read_text(encoding="utf-8"))
    assert payload["draft_count"] == 5
    assert re.match(r"\d{4}-W\d{2}", payload["iso_week"])
