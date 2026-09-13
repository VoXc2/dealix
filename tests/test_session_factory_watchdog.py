"""Contracts for the zero-token session factory watchdog (silent when healthy)."""
from __future__ import annotations

import importlib.util
import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str) -> object:
    path = ROOT / "scripts" / "ops" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


watchdog = _load("session_factory_watchdog")


def _write_lease(state_dir: Path, job_id: str, *, expires: float) -> None:
    leases = state_dir / "leases"
    leases.mkdir(parents=True, exist_ok=True)
    (leases / f"{job_id}.json").write_text(
        json.dumps({"JOB_ID": job_id, "LEASE_EXPIRES_EPOCH": expires, "OWNER": "test"}), encoding="utf-8"
    )


def _write_job(state_dir: Path, job_id: str, **fields) -> None:
    jobs = state_dir / "jobs"
    jobs.mkdir(parents=True, exist_ok=True)
    payload = {"JOB_ID": job_id, **fields}
    (jobs / f"{job_id}.json").write_text(json.dumps(payload), encoding="utf-8")


def test_healthy_state_is_silent(tmp_path: Path) -> None:
    assert watchdog.evaluate(tmp_path, now=1000.0) == []


def test_expired_lease_is_detected(tmp_path: Path) -> None:
    _write_lease(tmp_path, "JOB-1", expires=500.0)
    findings = watchdog.evaluate(tmp_path, now=1000.0)
    assert any(item["kind"] == "STUCK_LEASE" for item in findings)


def test_orphan_runner_is_detected(tmp_path: Path) -> None:
    _write_job(tmp_path, "JOB-2", STATUS="RUNNING", MODIFYING=True)
    findings = watchdog.evaluate(tmp_path, now=1000.0)
    assert any(item["kind"] == "ORPHAN_RUNNER" for item in findings)


def test_failure_spike_is_detected(tmp_path: Path) -> None:
    recent = datetime.now(UTC).isoformat()
    for index in range(5):
        _write_job(tmp_path, f"JOB-F{index}", STATUS="FAILED", UPDATED_AT=recent)
    findings = watchdog.evaluate(tmp_path)
    assert any(item["kind"] == "FAILURE_SPIKE" and item["count"] >= 5 for item in findings)


def test_deep_wip_exceeded_is_detected(tmp_path: Path) -> None:
    for index in range(4):
        _write_job(tmp_path, f"JOB-D{index}", STATUS="RUNNING", MODIFYING=True, LEASE={"JOB_ID": f"JOB-D{index}"})
    findings = watchdog.evaluate(tmp_path, now=1000.0)
    assert any(item["kind"] == "DEEP_WIP_EXCEEDED" for item in findings)


def test_governor_capacity_overrides_monitoring_default(tmp_path: Path) -> None:
    for index in range(4):
        _write_job(tmp_path, f"JOB-G{index}", STATUS="RUNNING", MODIFYING=True, LEASE={"JOB_ID": f"JOB-G{index}"})
    (tmp_path / "RESOURCE_GOVERNOR_STATE.json").write_text(
        json.dumps({"schema": "dealix.resource_governor.v1", "max_concurrent_deep": 8}), encoding="utf-8"
    )
    assert watchdog._governor_capacity(tmp_path) == 8
    findings = watchdog.evaluate(tmp_path, now=1000.0)
    assert [item for item in findings if item.get("kind") == "DEEP_WIP_EXCEEDED"] == []


def test_main_is_silent_and_zero_when_healthy(tmp_path: Path, capsys) -> None:
    code = watchdog.main(["--state-dir", str(tmp_path)])
    assert code == 0
    assert capsys.readouterr().out == ""
