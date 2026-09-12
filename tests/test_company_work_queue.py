"""Contracts for the canonical Company Work Queue (change detection + truth)."""
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


queue = _load("company_work_queue")


def test_priority_score_monotonic_in_economic_probability() -> None:
    low = queue.priority_score({"economic_probability": 0.1, "value": 0.5, "urgency": 0.5})
    high = queue.priority_score({"economic_probability": 0.9, "value": 0.5, "urgency": 0.5})
    assert high > low


def test_priority_score_penalizes_founder_minutes_cost_risk_and_deps() -> None:
    base = {"economic_probability": 0.5, "value": 0.5, "urgency": 0.5}
    cheap = queue.priority_score(base)
    assert queue.priority_score({**base, "founder_minutes": 120}) < cheap
    assert queue.priority_score({**base, "estimated_cost": 1.0}) < cheap
    assert queue.priority_score({**base, "risk": 1.0}) < cheap
    assert queue.priority_score({**base, "dependencies": ["a", "b", "c"]}) < cheap


def test_read_tsv_parses_header_and_rows(tmp_path: Path) -> None:
    path = tmp_path / "q.tsv"
    path.write_text("priority\tscore\towner\n1\t100\tdealix-pm\n", encoding="utf-8")
    rows = queue.read_tsv(path)
    assert rows == [{"priority": "1", "score": "100", "owner": "dealix-pm"}]
    assert queue.read_tsv(tmp_path / "missing.tsv") == []


def test_action_queue_items_keep_autonomy_and_never_count_as_revenue(tmp_path: Path, monkeypatch) -> None:
    queues = tmp_path / "queues"
    queues.mkdir()
    (queues / "ACTION_QUEUE.tsv").write_text(
        "priority\tscore\tdomain\towner\tstatus\tautonomy\n"
        "1\t100\tRevenue & Cash\trevenue-copilot\tREADY\tL0-L3_INTERNAL\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(queue, "QUEUES", queues)
    items = queue.items_from_action_queue()
    assert len(items) == 1
    item = items[0]
    assert item["owner"] == "revenue-copilot"
    assert item["autonomy"] == "L0-L3_INTERNAL"
    assert item["counts_as_revenue"] is False
    assert item["counts_as_pipeline"] is False


def test_approval_queue_items_are_pending_founder_and_never_auto_execute(tmp_path: Path, monkeypatch) -> None:
    queues = tmp_path / "queues"
    queues.mkdir()
    (queues / "APPROVAL_QUEUE.tsv").write_text(
        "id\taction\tautonomy\nAP-1\tdeploy release\tL5\n", encoding="utf-8"
    )
    monkeypatch.setattr(queue, "QUEUES", queues)
    items = queue.items_from_approval_queue()
    assert items[0]["status"] == "PENDING_FOUNDER"
    assert items[0]["autonomy"] == "L5"
    assert items[0]["counts_as_revenue"] is False


def test_v18_moves_map_relationship_to_probability_without_pipeline_inflation() -> None:
    command = {
        "top_moves": [
            {
                "item_id": "pi-imini-001",
                "lane": "WARM_NETWORK",
                "company": "iMini / Jannie",
                "current_stage": "NEGOTIATION",
                "relationship_state": "real_relationship",
                "evidence_strength": 3,
                "expected_next_evidence": "payment proof",
            }
        ]
    }
    items = queue.items_from_v18(command)
    assert len(items) == 1
    assert items[0]["economic_probability"] == 0.7
    assert items[0]["counts_as_pipeline"] is False
    assert items[0]["target"] == "iMini / Jannie"


def test_build_queue_is_sorted_descending() -> None:
    items = queue.build_queue()
    priorities = [item["priority"] for item in items]
    assert priorities == sorted(priorities, reverse=True)


def test_fingerprint_changes_with_content_and_is_stable_otherwise(tmp_path: Path) -> None:
    source = tmp_path / "source.tsv"
    source.write_text("a\tb\n", encoding="utf-8")
    first = queue.fingerprint([source])
    assert first == queue.fingerprint([source])
    source.write_text("a\tc\n", encoding="utf-8")
    assert queue.fingerprint([source]) != first
    missing = tmp_path / "missing.tsv"
    assert queue.fingerprint([missing]) == queue.fingerprint([missing])


def test_save_artifacts_writes_runtime_contract(tmp_path: Path, monkeypatch) -> None:
    queues = tmp_path / "queues"
    queues.mkdir()
    monkeypatch.setattr(queue, "QUEUES", queues)
    monkeypatch.setattr(queue, "STATE_PATH", queues / "STATE.json")
    monkeypatch.setattr(queue, "OUT_JSON", queues / "QUEUE.json")
    monkeypatch.setattr(queue, "OUT_MD", queues / "QUEUE.md")
    items = [{"priority": 50.0, "area": "TEST", "owner": "dealix-pm", "status": "READY", "next_action": "x"}]
    queue.save_artifacts(items, "fp123")
    payload = json.loads((queues / "QUEUE.json").read_text(encoding="utf-8"))
    assert payload["counts_as_revenue"] is False
    assert payload["fingerprint"] == "fp123"
    assert (queues / "STATE.json").exists()
    assert (queues / "QUEUE.md").exists()
