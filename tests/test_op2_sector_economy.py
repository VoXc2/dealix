"""Contracts for the OP2 sector-economy research ranking.

The ranking is a research artifact only. It must never claim relationship,
opportunity, pipeline, quote, payment, or revenue, and must stay at or below
RESEARCHED_WITH_SIGNALS.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RANKING = ROOT / "data" / "commercial" / "op2_sector_economy_ranking_v1.json"
WAVE = ROOT / "data" / "commercial" / "op2_market_intelligence_wave_v1.json"


def _load_module():
    path = ROOT / "scripts" / "commercial" / "op2_sector_economy.py"
    spec = importlib.util.spec_from_file_location("op2_sector_economy", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


economy = _load_module()


def _ranking() -> dict:
    return json.loads(RANKING.read_text(encoding="utf-8"))


def test_ranking_is_research_only() -> None:
    payload = _ranking()
    assert payload["schema"] == "dealix.op2-sector-economy.v1"
    assert payload["status_ceiling"] == "RESEARCHED_WITH_SIGNALS"
    assert payload["counts_as_pipeline"] is False
    assert payload["counts_as_revenue"] is False


def test_every_cell_is_bounded_and_complete() -> None:
    for cell in _ranking()["cells"]:
        assert cell["status"] == "RESEARCHED_WITH_SIGNALS"
        assert cell["truth_class"] == "PATTERN_RESEARCH_RANKING"
        assert cell["counts_as_pipeline"] is False
        assert cell["evidence_refs"], cell["sector_id"]
        vector = cell["vector"]
        for key in ("offer", "channel", "monetization", "delivery", "proof", "automation", "time_to_cash"):
            assert vector[key], (cell["sector_id"], key)


def test_ranking_score_is_monotonic_and_top10_capped() -> None:
    cells = _ranking()["cells"]
    scores = [cell["research_rank_score"] for cell in cells]
    assert scores == sorted(scores, reverse=True)
    assert len(_ranking()["top_cells"]) <= 10
    assert len(_ranking()["deep_wip_top3"]) == min(3, len(cells))


def test_ranking_recomputes_deterministically_from_wave() -> None:
    rebuilt = economy.build_ranking()
    stored = _ranking()
    assert [c["sector_id"] for c in rebuilt["cells"]] == [c["sector_id"] for c in stored["cells"]]


def test_all_twenty_sectors_have_evidence_backed_economic_vectors() -> None:
    from dealix.commercial.economic_cell import Sector

    payload = _ranking()
    assert len(payload["cells"]) == len(list(Sector)) == 20
    assert {cell["sector_id"] for cell in payload["cells"]} == {sector.value for sector in Sector}
    for cell in payload["cells"]:
        vector = cell["vector"]
        assert all(value != economy.UNKNOWN for value in vector.values()), cell["sector_id"]
