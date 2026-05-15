"""45-day Enterprise AI Transformation orchestrator — multi-workstream + persist."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.delivery_factory.transformation_program import (
    advance_workstream,
    clear_for_test,
    get_program,
    list_programs,
    start_program,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv(
        "DEALIX_TRANSFORMATION_RUNS_PATH", str(tmp_path / "txp.jsonl")
    )
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "fr.jsonl"))
    clear_for_test()
    yield
    clear_for_test()


def test_start_program_schedules_workstreams_across_45_days() -> None:
    p = start_program(
        customer_id="acme",
        offering_id="enterprise_transformation_sprint",
        tier_id="sprint_growth",
    )
    assert p.duration_days == 45
    assert len(p.workstreams) >= 5
    assert p.status == "in_progress"
    # Workstreams span the timeline and run on parallel tracks.
    assert {w.track for w in p.workstreams} <= {1, 2, 3}
    assert all(1 <= w.day_start <= w.day_end <= 45 for w in p.workstreams)
    assert any(w.track != p.workstreams[0].track for w in p.workstreams)


def test_start_program_rejects_unknown_offering() -> None:
    with pytest.raises(ValueError, match="unknown_enterprise_offering"):
        start_program(customer_id="acme", offering_id="nope", tier_id="x")


def test_program_persists_and_reloads() -> None:
    p = start_program(
        customer_id="acme",
        offering_id="ai_operating_system",
        tier_id="ai_os_growth",
    )
    reloaded = get_program(p.program_run_id)
    assert reloaded is not None
    assert reloaded.customer_id == "acme"
    assert len(reloaded.workstreams) == len(p.workstreams)


def test_advance_workstream_updates_progress() -> None:
    p = start_program(
        customer_id="acme",
        offering_id="ai_revenue_transformation",
        tier_id="rev_growth",
    )
    first = p.workstreams[0].name
    updated = advance_workstream(
        program_run_id=p.program_run_id,
        workstream_name=first,
        new_status="done",
        outputs={"note": "kickoff complete"},
    )
    assert updated.progress_pct > 0
    assert any(w.status == "done" for w in updated.workstreams)


def test_program_completes_when_all_workstreams_done() -> None:
    p = start_program(
        customer_id="acme",
        offering_id="ai_governance_program",
        tier_id="gov_growth",
    )
    for w in p.workstreams:
        result = advance_workstream(
            program_run_id=p.program_run_id,
            workstream_name=w.name,
            new_status="done",
        )
    assert result.status == "completed"
    assert result.progress_pct == 100.0


def test_blocked_workstream_blocks_program() -> None:
    p = start_program(
        customer_id="acme",
        offering_id="ai_operations_automation",
        tier_id="ops_growth",
    )
    result = advance_workstream(
        program_run_id=p.program_run_id,
        workstream_name=p.workstreams[0].name,
        new_status="blocked",
        notes="integration credentials missing",
    )
    assert result.status == "blocked"


def test_advance_rejects_invalid_status() -> None:
    p = start_program(
        customer_id="acme",
        offering_id="ai_knowledge_platform",
        tier_id="kn_growth",
    )
    with pytest.raises(ValueError, match="invalid status"):
        advance_workstream(
            program_run_id=p.program_run_id,
            workstream_name=p.workstreams[0].name,
            new_status="teleported",
        )


def test_list_programs_scoped_by_customer() -> None:
    start_program(
        customer_id="acme", offering_id="ai_operating_system", tier_id="ai_os_basic"
    )
    start_program(
        customer_id="other", offering_id="ai_operating_system", tier_id="ai_os_basic"
    )
    assert len(list_programs(customer_id="acme")) == 1
    assert len(list_programs()) == 2


# ── API surface ──────────────────────────────────────────────────────


def test_transformation_api_start_and_timeline() -> None:
    start = client.post(
        "/api/v1/transformation/start",
        json={
            "customer_id": "acme",
            "offering_id": "enterprise_transformation_sprint",
            "tier_id": "sprint_enterprise",
        },
    )
    assert start.status_code == 200, start.text
    run_id = start.json()["program_run_id"]

    tl = client.get(f"/api/v1/transformation/{run_id}/timeline")
    assert tl.status_code == 200
    body = tl.json()
    assert body["duration_days"] == 45
    assert set(body["tracks"].keys()) == {"1", "2", "3"}


def test_transformation_api_advance_and_404() -> None:
    start = client.post(
        "/api/v1/transformation/start",
        json={
            "customer_id": "acme",
            "offering_id": "ai_operating_system",
            "tier_id": "ai_os_growth",
        },
    )
    run_id = start.json()["program_run_id"]
    ws = start.json()["workstreams"][0]["name"]

    adv = client.post(
        f"/api/v1/transformation/{run_id}/advance",
        json={"workstream_name": ws, "new_status": "in_progress"},
    )
    assert adv.status_code == 200, adv.text

    missing = client.get("/api/v1/transformation/TXP-does-not-exist")
    assert missing.status_code == 404
