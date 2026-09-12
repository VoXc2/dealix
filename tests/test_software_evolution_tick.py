from __future__ import annotations

import json
from pathlib import Path

from scripts.ops.software_evolution_tick import run_tick


def test_tick_submits_only_bounded_v2_research_jobs(tmp_path: Path) -> None:
    sources = tmp_path / "sources.json"
    sources.write_text(
        json.dumps(
            {
                "schema": "dealix.software_acquisition_sources.v2",
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
    assert receipt["schema"] == "dealix.software_evolution_tick.v2"
    assert receipt["acquisition"]["schema"] == "dealix.software_acquisition_run.v2"
    assert len(receipt["scout_jobs"]) == 3
    assert all(item["ok"] for item in receipt["scout_jobs"])
    assert all(item["status"] == "READY" for item in receipt["scout_jobs"])
    assert receipt["external_effects_executed"] == 0
    assert receipt["l5_executed"] == "NONE"
    assert receipt["scheduler_created"] is False

    queue = json.loads((session_state / "AUTONOMOUS_JOB_QUEUE.json").read_text())
    assert queue["counts"]["READY"] == 3

    canonical_jobs = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((session_state / "jobs").glob("*.json"))
    ]
    assert len(canonical_jobs) == 3
    for job in canonical_jobs:
        prompt = job["EXECUTOR"]["prompt"]
        assert "dealix.software_candidate.v2" in prompt
        assert "cisa_kev_match" in prompt
        assert "capability_map" in prompt
        assert "Research is not trust" in prompt
