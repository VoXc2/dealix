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


def test_all_twenty_canonical_sectors_are_routed() -> None:
    from dealix.commercial.economic_cell import Sector

    payload = _payload()
    assert payload["route_count"] == len(list(Sector)) == 20
    assert {route["sector_id"] for route in payload["routes"]} == {sector.value for sector in Sector}
    assert payload["evidence_backed_count"] == 20
    assert payload["pattern_only_count"] == 0
    for route in payload["routes"]:
        assert route["market_evidence_status"] == "EVIDENCE_BACKED"
        assert route["market_evidence_scope"] == "PUBLIC_MARKET_SIGNAL_ONLY_NOT_BUYER_DEMAND"
        assert route["buyer_demand_status"] == "UNKNOWN_NOT_EVIDENCE_BACKED"
        assert route["commercial_pattern"]["offer_ladder"]
        assert route["commercial_pattern"]["acceptance_criteria"]
        assert "fresh official market signal" not in route["discovery_prep"]["evidence_gaps"]
        assert route["counts_as_pipeline"] is False
        assert route["counts_as_revenue"] is False


def test_former_generic_sectors_have_specific_commercial_intelligence() -> None:
    from dealix.commercial.economic_cell import Sector
    from dealix.commercial.sector_company_factory import SECTOR_INTEL

    sectors = [
        Sector.MINING_METALS, Sector.RETAIL_COMMERCE_ECOMMERCE, Sector.TOURISM_HOSPITALITY,
        Sector.TELECOM_MEDIA_MARKETING, Sector.EDUCATION_TRAINING, Sector.AGRICULTURE_FOOD_WATER,
        Sector.MOBILITY_AUTOMOTIVE, Sector.EXPORT_IMPORT_RHQ, Sector.CREATIVE_SPORTS_GAMING,
        Sector.ASSOCIATIONS_NONPROFITS,
    ]
    for sector in sectors:
        intel = SECTOR_INTEL[sector]
        assert len(intel["buyers"]) >= 3
        assert len(intel["problems"]) >= 3
        assert len(intel["workflows"]) >= 2
        assert len(intel["offers"]) >= 2
        assert intel["problems"] != ["revenue_leakage", "operational_exception_overload"]
