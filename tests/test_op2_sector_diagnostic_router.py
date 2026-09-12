"""Contracts for the OP2 sector diagnostic router artifact."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ROOT / "data" / "commercial" / "op2_sector_diagnostic_routes_v1.json"


def _load_module():
    path = ROOT / "scripts" / "commercial" / "op2_sector_diagnostic_router.py"
    spec = importlib.util.spec_from_file_location("op2_diag_router", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


router = _load_module()


def _payload() -> dict:
    return json.loads(ROUTES.read_text(encoding="utf-8"))


def test_routes_are_free_and_canonical() -> None:
    payload = _payload()
    assert payload["route_count"] >= 1
    for route in payload["routes"]:
        entry = route["diagnostic_entry"]
        assert entry["route"] == "/book"
        assert entry["card_required"] is False
        assert entry["roi_promised"] is False
        assert set(entry["free_depths"]) <= set(router.FREE_DEPTHS)


def test_routes_handoff_to_five_canonical_agents() -> None:
    for route in _payload()["routes"]:
        assert route["crm_handoff"]["canonical_agents"] == router.CANONICAL_AGENTS


def test_routes_are_research_only() -> None:
    payload = _payload()
    assert all(not v for v in payload["authority"].values())
    assert payload["counts_as_pipeline"] is False
    assert payload["counts_as_revenue"] is False
    for route in payload["routes"]:
        assert route["allowed_use"] == ["INTERNAL_RESEARCH_ONLY"]


def test_router_is_deterministic() -> None:
    rebuilt = router.build_routes()
    stored = _payload()
    assert [r["sector_id"] for r in rebuilt["routes"]] == [r["sector_id"] for r in stored["routes"]]
