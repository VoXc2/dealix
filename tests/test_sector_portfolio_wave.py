"""Contracts for the 20-sector / five-agent portfolio wave."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "scripts" / "ops" / "sector_portfolio_wave.py"
spec = importlib.util.spec_from_file_location("sector_portfolio_wave", PATH)
wave = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(wave)


def test_plan_covers_all_sectors_once_with_five_agents() -> None:
    plan = wave.build_plan("a" * 40)
    assert plan["coverage"]["canonical_sectors"] == 20
    assert plan["coverage"]["sectors_covered"] == 20
    assert plan["coverage"]["coverage_percent"] == 100
    assert plan["coverage"]["all_diagnostics_free"] is True
    assert plan["job_count"] == 5
    assert set(plan["permanent_agents"]) == {
        "dealix-pm", "dealix-sales", "dealix-delivery",
        "dealix-engineer", "dealix-content",
    }


def test_first_tick_intent_matches_three_economic_lanes() -> None:
    plan = wave.build_plan("b" * 40)
    selected = wave.select_deep_jobs(plan["jobs"], slots=3)
    assert [job["OWNER_AGENT"] for job in selected] == [
        "dealix-sales", "dealix-engineer", "dealix-delivery"
    ]


def test_every_job_is_internal_and_has_bounded_receipt() -> None:
    plan = wave.build_plan("c" * 40)
    for job in plan["jobs"]:
        assert job["AUTHORITY_LEVEL"] in {"L3", "L4"}
        assert job["STATUS"] == "QUEUED"
        assert job["MODIFYING"] is True
        assert job["ACCEPTANCE"]["checks"][0]["kind"] == "file_exists"
        assert "docs/company-os/sector-wave/" in job["ACCEPTANCE"]["checks"][0]["path"]
        assert "L5_EXECUTED=NONE" in job["EXECUTOR"]["prompt"]


def test_enqueue_submits_five_jobs_without_l5(tmp_path: Path) -> None:
    plan = wave.build_plan("d" * 40)
    result = wave.enqueue_plan(plan, tmp_path)
    assert result["submitted"] == 5
    assert result["waiting_l5"] == 0
    assert result["statuses"] == ["READY"] * 5
