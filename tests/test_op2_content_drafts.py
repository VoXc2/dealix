"""Contracts for the OP2 content drafts artifact."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "data" / "commercial" / "op2_content_drafts_v1.json"


def _load_module():
    path = ROOT / "scripts" / "commercial" / "op2_content_drafts.py"
    spec = importlib.util.spec_from_file_location("op2_content", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


content = _load_module()


def _payload() -> dict:
    return json.loads(DRAFTS.read_text(encoding="utf-8"))


def test_drafts_are_unpublished_and_require_approval() -> None:
    payload = _payload()
    assert payload["publish_authority"] is False
    assert payload["draft_count"] >= 1
    for draft in payload["drafts"]:
        assert draft["status"] == "draft"
        assert draft["published"] is False
        assert draft["approval_required"] is True


def test_drafts_are_sourced_from_real_signals() -> None:
    for draft in _payload()["drafts"]:
        assert draft["source_ref"].startswith("http")
        assert draft["authority_ref"]
        assert draft["evidence_refs"]


def test_drafts_have_bilingual_atoms_and_no_roi_promise() -> None:
    for draft in _payload()["drafts"]:
        locales = {atom["locale"] for atom in draft["atoms"]}
        assert "ar" in locales and "en" in locales
        text = " ".join(atom["body"] for atom in draft["atoms"]).lower()
        for banned in content.BANNED:
            assert banned.lower() not in text, (draft["draft_id"], banned)


def test_drafts_are_research_only_drafts() -> None:
    for draft in _payload()["drafts"]:
        assert draft["allowed_use"] == ["INTERNAL_DRAFT_ONLY"]
        assert draft["counts_as_relationship"] is False
        assert draft["counts_as_pipeline"] is False
