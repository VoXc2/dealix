"""Contracts for executive company state exports (honest UNKNOWNs, no invention)."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str) -> object:
    path = ROOT / "scripts" / "ops" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


state = _load("company_state_export")

FIXTURE_QUEUE = {
    "fingerprint": "abc",
    "items": [
        {"priority": 10, "area": "Revenue", "owner": "dealix-sales", "status": "READY", "next_action": "prep", "evidence": ["rel-1"]},
        {"priority": 5, "area": "Approvals", "owner": "founder", "status": "PENDING_FOUNDER", "next_action": "decide", "evidence": []},
    ],
}


def test_agent_status_maps_five_agents_without_inflation(tmp_path: Path, monkeypatch) -> None:
    queue_path = tmp_path / "queue.json"
    queue_path.write_text(json.dumps(FIXTURE_QUEUE), encoding="utf-8")
    monkeypatch.setattr(state, "WORK_QUEUE", queue_path)
    payload = state.agent_runtime_status()
    assert payload["permanent_agent_count"] == 5
    assert payload["deep_wip_max"] == 3
    assert set(payload["agents"]) == {
        "dealix-pm",
        "dealix-sales",
        "dealix-delivery",
        "dealix-engineer",
        "dealix-content",
    }
    assert payload["agents"]["dealix-sales"]["state"] == "ACTIVE_HIGH_VALUE_WORK"
    assert payload["agents"]["dealix-delivery"]["state"] == "WAITING_FOR_EVENT"


def test_queue_summary_never_counts_as_revenue(tmp_path: Path, monkeypatch) -> None:
    queue_path = tmp_path / "queue.json"
    queue_path.write_text(json.dumps(FIXTURE_QUEUE), encoding="utf-8")
    monkeypatch.setattr(state, "WORK_QUEUE", queue_path)
    summary = state.queue_summary()
    assert summary["item_count"] == 2
    assert summary["counts_as_revenue"] is False
    assert len(summary["top_items"]) == 2


def test_model_scorecard_is_pending_not_fake(tmp_path: Path, monkeypatch) -> None:
    broker_path = tmp_path / "broker.json"
    broker_path.write_text(json.dumps({"jobs": [{"model": "opencode/deepseek-v4-flash"}]}), encoding="utf-8")
    monkeypatch.setattr(state, "BROKER_STATE", broker_path)
    scorecard = state.model_scorecard()
    assert scorecard["quality_score"] == "UNKNOWN"
    assert scorecard["scorecard_status"] == "PENDING_BOUNDED_BENCHMARKS"
    assert "opencode/deepseek-v4-flash" in scorecard["models_observed_in_jobs"]


def test_write_all_creates_five_artifacts(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(state, "sector_portfolio_index", lambda: {"sectors_total": 20})
    written = state.write_all(tmp_path)
    assert set(written) == {
        "LATEST_TRUTH.md",
        "AGENT_RUNTIME_STATUS.json",
        "MODEL_SCORECARD.json",
        "SECTOR_PORTFOLIO_INDEX.json",
        "COMPANY_QUEUE_SUMMARY.json",
    }
    assert (tmp_path / "SECTOR_PORTFOLIO_INDEX.json").exists()


def test_latest_truth_markdown_flags_synthetic_exclusion() -> None:
    markdown = state.latest_truth_markdown()
    assert "verified_revenue_sar" in markdown
    assert "never revenue or pipeline" in markdown
