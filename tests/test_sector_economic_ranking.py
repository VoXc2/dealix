"""Contracts for the sector economic ranking built on real radar signals."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str) -> object:
    path = ROOT / "scripts" / "ops" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ranking = _load("sector_economic_ranking")


def test_mapping_covers_every_radar_sector_family() -> None:
    import json

    playbooks = json.loads((ROOT / "data" / "commercial" / "universal_market_playbooks_v1.json").read_text(encoding="utf-8"))
    families = {row["id"] for row in playbooks["sector_families"]}
    assert families <= set(ranking.SECTOR_FAMILY_TO_CANONICAL)


def test_known_mappings_preserve_canonical_sector_ids() -> None:
    assert ranking.SECTOR_FAMILY_TO_CANONICAL["HEALTHCARE_LIFE_SCIENCES"][0] == "healthcare"
    assert ranking.SECTOR_FAMILY_TO_CANONICAL["TRANSPORT_LOGISTICS"][0] == "logistics_supply_chain"
    assert ranking.SECTOR_FAMILY_TO_CANONICAL["FINANCIAL_SERVICES"][0] == "finance_fintech_insurance"
    assert ranking.SECTOR_FAMILY_TO_CANONICAL["ICT"][0] == "technology_saas_si"


def test_aggregates_count_signals_and_stale_flags() -> None:
    brief = {
        "ranked_research_signals": [
            {"sector_family": "ICT", "priority_score": 100.0, "stale": False, "signal_id": "s1", "evidence_refs": ["u1"]},
            {"sector_family": "ICT", "priority_score": 50.0, "stale": True, "signal_id": "s2", "evidence_refs": ["u2"]},
            {"sector_family": "UNKNOWN_FAMILY", "priority_score": 999.0, "stale": False, "signal_id": "s3", "evidence_refs": []},
        ]
    }
    aggregates = ranking.build_sector_aggregates(brief)
    assert "technology_saas_si" in aggregates
    tech = aggregates["technology_saas_si"]
    assert tech["signal_count"] == 2
    assert tech["stale_count"] == 1
    assert tech["signal_ids"] == ["s1", "s2"]
    assert "UNKNOWN_FAMILY" not in str(aggregates)


def test_composite_score_is_monotonic_and_transparent() -> None:
    low, _ = ranking.composite_score({"priority_scores": [50.0], "signal_count": 1}, "A", 99)
    high, _ = ranking.composite_score({"priority_scores": [200.0], "signal_count": 1}, "A", 99)
    assert high > low
    dense, _ = ranking.composite_score({"priority_scores": [50.0, 50.0], "signal_count": 2}, "A", 99)
    assert dense > low
    governed, _ = ranking.composite_score({"priority_scores": [50.0], "signal_count": 1}, "C_GOVERNED", 99)
    assert governed < low
    none, breakdown = ranking.composite_score({"priority_scores": [], "signal_count": 0}, "A", 99)
    assert none == 0.0
    assert breakdown["reason"] == "NO_SCORED_SIGNALS"


def test_ranking_from_real_brief_respects_status_ceiling() -> None:
    result = ranking.build_ranking()
    assert result["schema"] == "dealix.top-economic-cells.v1"
    assert result["counts_as_pipeline"] is False
    assert result["counts_as_revenue"] is False
    assert result["status_ceiling"] == "RESEARCHED_WITH_SIGNALS"
    scores = [sector["research_rank_score"] for sector in result["sectors"]]
    assert scores == sorted(scores, reverse=True)
    for sector in result["sectors"]:
        assert sector["status"] in {"RESEARCHED_WITH_SIGNALS", "INTERNAL_READY_NO_SIGNALS"}
        assert "counts_as_revenue" not in sector
    assert result["top_cells"]
    assert all(cell["counts_as_pipeline"] is False for cell in result["top_cells"])


def test_ranking_summary_renders_top_cells() -> None:
    summary = ranking.render_summary(ranking.build_ranking(), top=3)
    assert "SECTOR_ECONOMIC_RANKING=OK" in summary
    assert "RANK1" in summary
    assert "COUNTS_AS_PIPELINE=False" in summary
