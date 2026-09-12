from __future__ import annotations

import json
from pathlib import Path

from scripts.ops.software_evolution_tick import run_tick


def test_tick_submits_only_bounded_research_jobs(tmp_path: Path) -> None:
    sources = tmp_path / "sources.json"
    sources.write_text(
        json.dumps(
            {
                "schema": "dealix.software_acquisition_sources.v1",
                "categories": [
                    {
                        "id": f"cat-{index}",
                        "priority": 100 - index,
                        "purpose": "test",
                        "official_sources": [f"https://example.invalid/{index}"],
                    }
                    for index in range(5)
                ],
            }
        ),
        encoding="utf-8",
    )
    session_state = tmp_path / "session"
    state_dir = tmp_path / "software"
    receipt = run_tick(
        base_sha="deadbeef",
        source_path=sources,
        registry_path=tmp_path / "missing.json",
        state_dir=state_dir,
        session_state=session_state,
        enqueue_scouts=True,
        enqueue_candidates=False,
        max_scouts=3,
    )
    assert len(receipt["scout_jobs"]) == 3
    assert all(item["ok"] for item in receipt["scout_jobs"])
    assert all(item["status"] == "READY" for item in receipt["scout_jobs"])
    assert receipt["external_effects_executed"] == 0
    assert receipt["l5_executed"] == "NONE"
    assert receipt["scheduler_created"] is False
    queue = json.loads((session_state / "AUTONOMOUS_JOB_QUEUE.json").read_text())
    assert queue["counts"]["READY"] == 3
