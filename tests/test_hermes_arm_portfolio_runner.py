"""Contracts for the one-shot Hermes arm portfolio runner.

The runner plans exactly once and (optionally) hands off to the canonical
session factory queue. It never loops, never installs a scheduler and never
executes a job; L5 material effects stay WAITING_L5.
"""

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


runner = _load("run_hermes_arm_portfolio_once")


def _write_evidence(tmp_path: Path, arms: dict) -> Path:
    path = tmp_path / "evidence.json"
    path.write_text(
        json.dumps({"schema": "dealix.arm_portfolio_evidence.v1", "arms": arms}), encoding="utf-8"
    )
    return path


def test_plan_only_writes_plan_without_enqueue(tmp_path: Path) -> None:
    result = runner.run_once(state_dir=tmp_path / "state", plan_path=tmp_path / "plan.json")
    assert result["overall"] == "PLAN_READY"
    assert result["enqueued"] == []
    assert Path(result["plan_path"]).is_file()
    jobs_dir = tmp_path / "state" / "jobs"
    assert not jobs_dir.exists() or list(jobs_dir.glob("*.json")) == []


def test_enqueue_submits_safe_jobs_and_skips_hold(tmp_path: Path) -> None:
    result = runner.run_once(
        state_dir=tmp_path / "state",
        plan_path=tmp_path / "plan.json",
        enqueue=True,
        max_jobs=50,
    )
    plan = json.loads((tmp_path / "plan.json").read_text(encoding="utf-8"))
    enqueued_ids = {entry["arm_id"] for entry in result["enqueued"]}
    assert len(enqueued_ids) == plan["counts"]["DEEP"] + plan["counts"]["LIGHT"]
    assert "ARM-042" not in enqueued_ids
    factory = runner.controller.session_factory()
    jobs = factory.all_jobs(tmp_path / "state")
    assert len(jobs) == len(enqueued_ids)
    assert all(job["STATUS"] == "READY" for job in jobs)


def test_l5_arm_enqueues_waiting_l5(tmp_path: Path) -> None:
    evidence = _write_evidence(
        tmp_path,
        {"ARM-004": {"customer_evidence_refs": ["evidence://c/1"], "requires_external_send": True}},
    )
    result = runner.run_once(
        state_dir=tmp_path / "state",
        plan_path=tmp_path / "plan.json",
        evidence_path=evidence,
        enqueue=True,
        max_jobs=50,
    )
    l5 = [entry for entry in result["enqueued"] if entry["arm_id"] == "ARM-004"]
    assert l5 and l5[0]["status"] == "WAITING_L5"
    factory = runner.controller.session_factory()
    job = factory.load_job(tmp_path / "state", l5[0]["job_id"])
    assert job["STATUS"] == "WAITING_L5"
    assert factory.read_lease(tmp_path / "state", job["JOB_ID"]) is None


def test_enqueue_is_idempotent(tmp_path: Path) -> None:
    first = runner.run_once(
        state_dir=tmp_path / "state",
        plan_path=tmp_path / "plan.json",
        enqueue=True,
        max_jobs=50,
    )
    assert first["enqueued"]
    second = runner.run_once(
        state_dir=tmp_path / "state",
        plan_path=tmp_path / "plan.json",
        enqueue=True,
        max_jobs=50,
    )
    assert second["enqueued"] == []
    assert any(entry["reason"] == "ALREADY_ENQUEUED" for entry in second["skipped"])


def test_tripwire_refuses_enqueue(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_PUBLIC_PUBLISH", "1")
    result = runner.run_once(
        state_dir=tmp_path / "state",
        plan_path=tmp_path / "plan.json",
        enqueue=True,
    )
    assert result["overall"] == "BLOCKED"
    assert result["enqueued"] == []
    assert result["enqueue_error"].startswith("refused")


def test_runner_source_is_one_shot_and_hands_off() -> None:
    source = (ROOT / "scripts" / "ops" / "run_hermes_arm_portfolio_once.py").read_text(
        encoding="utf-8"
    )
    for token in ("while True", "crontab", "APScheduler", "run_job(", "process_queue("):
        assert token not in source
    assert "session_factory" in source
