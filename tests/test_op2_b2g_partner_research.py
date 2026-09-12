"""Contracts for the OP2 B2G / partner research artifact."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "commercial" / "op2_b2g_partner_research_v1.json"


def _load_module():
    path = ROOT / "scripts" / "commercial" / "op2_b2g_partner_research.py"
    spec = importlib.util.spec_from_file_location("op2_b2g", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


b2g = _load_module()


def _payload() -> dict:
    return json.loads(PATH.read_text(encoding="utf-8"))


def test_default_posture_is_partner_or_no_bid() -> None:
    payload = _payload()
    assert payload["default_bid_posture"] == "PARTNER_OR_NO_BID"
    for item in payload["b2g_items"]:
        assert item["bid_posture"] == "PARTNER_OR_NO_BID"


def test_everything_is_research_only() -> None:
    payload = _payload()
    assert all(not v for v in payload["authority"].values())
    for partner in payload["partner_candidates"]:
        assert partner["relationship_state"] == "RESEARCH_ONLY"


def test_partner_candidates_are_ranked_and_sector_bound() -> None:
    partners = _payload()["partner_candidates"]
    assert len(partners) >= 3
    scores = [p["economic_score"] for p in partners]
    assert scores == sorted(scores, reverse=True)
    for partner in partners:
        assert partner["sector_fit"]


def test_builder_is_deterministic() -> None:
    rebuilt = b2g.build()
    stored = _payload()
    assert [p["partner_id"] for p in rebuilt["partner_candidates"]] == [p["partner_id"] for p in stored["partner_candidates"]]
