"""Bounded parallel admission contracts for the canonical session factory."""
from __future__ import annotations

import importlib.util
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "scripts" / "ops" / "session_factory.py"
spec = importlib.util.spec_from_file_location("session_factory_parallel", PATH)
factory = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(factory)


def _deep(owner: str, job_class: str, priority: float) -> dict:
    return factory.make_job(
        owner_agent=owner,
        business_goal=f"parallel {owner}",
        job_class=job_class,
        authority_level="L3",
        priority=priority,
        modifying=True,
        executor={"prompt": "internal only"},
    )


def test_first_tick_runs_three_economic_lanes_concurrently(tmp_path: Path, monkeypatch) -> None:
    jobs = [
        _deep("dealix-sales", "COMMERCIAL_REASONING", 95),
        _deep("dealix-engineer", "ENGINEERING", 94),
        _deep("dealix-delivery", "DELIVERY", 93),
        _deep("dealix-pm", "RESEARCH", 86),
        _deep("dealix-content", "RESEARCH", 82),
    ]
    for job in jobs:
        assert factory.submit_job(tmp_path, job)["ok"] is True
    monkeypatch.setattr(factory, "governor_state", lambda root: {"deep_wip_available": 3})
    monkeypatch.setattr(factory, "active_leases", lambda root: [])

    barrier = threading.Barrier(3)
    seen: list[tuple[str, int]] = []
    seen_lock = threading.Lock()
    def fake_run(root, job, **kwargs):
        with seen_lock:
            seen.append((job["OWNER_AGENT"], threading.get_ident()))
        barrier.wait(timeout=2)
        return {"ok": True, "status": "SUCCEEDED", "job": job}
    monkeypatch.setattr(factory, "run_job", fake_run)

    processed = factory.process_queue(tmp_path)
    assert len(processed) == 3
    owners = {owner for owner, _thread_id in seen}
    assert owners == {"dealix-sales", "dealix-engineer", "dealix-delivery"}
    assert len({thread_id for _owner, thread_id in seen}) == 3


def test_shallow_job_runs_even_when_no_deep_slot_is_available(tmp_path: Path, monkeypatch) -> None:
    job = factory.make_job(
        owner_agent="dealix-pm",
        business_goal="zero-token status",
        job_class="DETERMINISTIC",
        authority_level="L1",
        modifying=False,
        executor={"argv": ["python", "-c", "print('ok')"]},
    )
    assert factory.submit_job(tmp_path, job)["ok"] is True
    monkeypatch.setattr(factory, "governor_state", lambda root: {"deep_wip_available": 0})
    monkeypatch.setattr(factory, "active_leases", lambda root: [])
    monkeypatch.setattr(
        factory, "run_job",
        lambda root, job, **kwargs: {"ok": True, "status": "SUCCEEDED", "job": job},
    )
    processed = factory.process_queue(tmp_path)
    assert len(processed) == 1
    assert processed[0]["job"]["JOB_ID"] == job["JOB_ID"]
