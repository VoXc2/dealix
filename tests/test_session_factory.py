"""Contracts for the Hermes Autonomous Session Factory (durable, zero-token first)."""
from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str) -> object:
    path = ROOT / "scripts" / "ops" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


factory = _load("session_factory")


def _deterministic_job(**overrides):
    kwargs = {
        "owner_agent": "dealix-pm",
        "business_goal": "synthetic contract job",
        "job_class": "DETERMINISTIC",
        "authority_level": "L1",
        "modifying": False,
        "executor": {"argv": ["python3", "-c", "print('ok')"]},
        "acceptance": {"criteria": "exit zero", "checks": [{"kind": "exit_zero"}]},
    }
    kwargs.update(overrides)
    return factory.make_job(**kwargs)


def test_deterministic_and_monitoring_are_zero_token() -> None:
    for job_class in ("DETERMINISTIC", "MONITORING"):
        job = factory.make_job(owner_agent="dealix-pm", business_goal="x", job_class=job_class)
        assert job["EXECUTION_MODE"] == "deterministic"
        assert job["TOKEN_BUDGET_CLASS"] == "zero"


def test_engineering_routes_to_opencode_and_modifying() -> None:
    job = factory.make_job(owner_agent="dealix-engineer", business_goal="x", job_class="ENGINEERING")
    assert job["EXECUTION_MODE"] == "opencode"
    assert job["MODIFYING"] is True


def test_validate_rejects_dangerous_executor_argv() -> None:
    job = _deterministic_job(executor={"argv": ["sudo", "ls"]})
    errors = factory.validate_job(job)
    assert any("dangerous" in error for error in errors)


def test_validate_rejects_non_permanent_owner() -> None:
    job = _deterministic_job(owner_agent="dealix-rogue")
    errors = factory.validate_job(job)
    assert any("OWNER_AGENT" in error for error in errors)


def test_run_job_revalidates_direct_entry_before_execution(tmp_path: Path, monkeypatch) -> None:
    job = _deterministic_job(owner_agent="dealix-rogue")
    called = False

    def forbidden_executor(*_args, **_kwargs):
        nonlocal called
        called = True
        raise AssertionError("invalid job reached executor")

    monkeypatch.setitem(factory.EXECUTORS, "deterministic", forbidden_executor)
    outcome = factory.run_job(tmp_path, job)

    assert outcome["ok"] is False
    assert outcome["status"] == "BLOCKED"
    assert outcome["reason"] == "canonical-admission-rejected"
    assert any("OWNER_AGENT" in error for error in outcome["errors"])
    assert called is False
    assert job["STATUS"] == "BLOCKED"
    persisted = factory.read_json(factory.job_path(tmp_path, job["JOB_ID"]), {})
    assert persisted["STATUS"] == "BLOCKED"
    snapshot = factory.read_json(factory.queue_path(tmp_path), {})
    assert snapshot["counts"]["BLOCKED"] == 1
    assert factory.read_lease(tmp_path, job["JOB_ID"]) is None


def test_illegal_transition_is_rejected() -> None:
    job = factory.make_job(owner_agent="dealix-pm", business_goal="x", job_class="DETERMINISTIC")
    with pytest.raises(ValueError):
        factory.transition(job, "RUNNING")


def test_new_job_ids_are_unique() -> None:
    assert len({factory.new_job_id() for _ in range(100)}) == 100


def test_lease_contention_then_expiry_requires_reclaim(tmp_path: Path) -> None:
    job = _deterministic_job()
    factory.plan_job(job)
    first, _ = factory.acquire_lease(tmp_path, job, owner="worker-1", ttl_seconds=60)
    second, reason = factory.acquire_lease(tmp_path, job, owner="worker-2", ttl_seconds=60)
    assert first is True
    assert second is False
    assert reason is not None and reason["reason"] in ("LEASE_HELD", "LEASE_HELD_LIVE")

    lease = factory.read_lease(tmp_path, job["JOB_ID"])
    assert lease is not None
    lease["LEASE_EXPIRES_EPOCH"] = factory.now_epoch() - 1
    lease["HEARTBEAT_PID"] = 99999999
    factory.write_json(factory.lease_path(tmp_path, job["JOB_ID"]), lease)

    third, reason3 = factory.acquire_lease(tmp_path, job, owner="worker-3")
    assert third is False
    assert reason3 is not None and reason3["reason"] == "LEASE_EXPIRED_NEEDS_RECLAIM"
    fourth, _ = factory.acquire_lease(tmp_path, job, owner="worker-3", reclaim_expired=True)
    assert fourth is True


def test_resource_governor_derives_capacity_from_live_resources(monkeypatch) -> None:
    monkeypatch.delenv("DEALIX_DEEP_WIP_CEILING", raising=False)
    # Starved host throttles to one deep worker.
    assert factory.compute_max_concurrent_deep({"mem_available_mb": 1000, "cpu_count": 4, "load1": 0}) == 1
    # Current-host-shaped capacity (~4 CPU / ~9GiB) still computes 3.
    assert factory.compute_max_concurrent_deep({"mem_available_mb": 8875, "cpu_count": 4, "load1": 3.45}) == 3
    # Roomy hosts safely exceed the superseded legacy global cap of 3.
    roomy = {"mem_available_mb": 12288, "cpu_count": 8, "load1": 0.1}
    assert factory.compute_max_concurrent_deep(roomy) > 3
    # Extreme load throttles back to one regardless of headroom.
    assert factory.compute_max_concurrent_deep({"mem_available_mb": 12288, "cpu_count": 8, "load1": 100}) == 1


def test_operational_ceiling_bounds_but_never_unbounds(monkeypatch) -> None:
    roomy = {"mem_available_mb": 65536, "cpu_count": 32, "load1": 0.1}
    monkeypatch.setenv("DEALIX_DEEP_WIP_CEILING", "2")
    assert factory.compute_max_concurrent_deep(roomy) == 2
    assert factory.operational_ceiling() == 2
    monkeypatch.setenv("DEALIX_DEEP_WIP_CEILING", "10000")
    assert factory.operational_ceiling() == factory.DEEP_WIP_CEILING_HARD_MAX
    assert factory.compute_max_concurrent_deep(roomy) <= factory.DEEP_WIP_CEILING_HARD_MAX
    monkeypatch.setenv("DEALIX_DEEP_WIP_CEILING", "not-a-number")
    assert factory.operational_ceiling() == factory.DEEP_WIP_CEILING_DEFAULT


def test_submit_l5_waits_and_never_runs(tmp_path: Path) -> None:
    job = factory.make_job(
        owner_agent="dealix-sales",
        business_goal="material send",
        job_class="COMMERCIAL_REASONING",
        authority_level="L5",
        data_sensitivity="INTERNAL",
        executor={"prompt": "draft only"},
    )
    submitted = factory.submit_job(tmp_path, job)
    assert submitted["ok"] is True
    assert submitted["job"]["STATUS"] == "WAITING_L5"
    outcome = factory.run_job(tmp_path, submitted["job"])
    assert outcome["status"] == "WAITING_L5"
    assert factory.read_lease(tmp_path, job["JOB_ID"]) is None


def test_success_requires_acceptance_evidence(tmp_path: Path) -> None:
    job = _deterministic_job()
    factory.submit_job(tmp_path, job)
    outcome = factory.run_job(tmp_path, factory.load_job(tmp_path, job["JOB_ID"]))
    assert outcome["status"] == "SUCCEEDED"
    assert outcome["acceptance"]["passed"] is True
    assert factory.read_lease(tmp_path, job["JOB_ID"]) is None


def test_nonzero_exit_is_not_success(tmp_path: Path) -> None:
    job = _deterministic_job(executor={"argv": ["python3", "-c", "import sys; sys.exit(3)"]})
    factory.submit_job(tmp_path, job)
    outcome = factory.run_job(tmp_path, factory.load_job(tmp_path, job["JOB_ID"]))
    assert outcome["status"] == "FAILED"
    assert outcome["acceptance"]["passed"] is False


def test_recover_parks_dead_runner_as_recoverable(tmp_path: Path) -> None:
    job = _deterministic_job()
    factory.plan_job(job)
    for state in ("READY", "CLAIMED", "RUNNING"):
        factory.transition(job, state)
    factory.save_job(tmp_path, job)
    factory.write_json(
        factory.lease_path(tmp_path, job["JOB_ID"]),
        {
            "schema": factory.LEASE_SCHEMA,
            "JOB_ID": job["JOB_ID"],
            "OWNER": "dead",
            "LEASE_STARTED_EPOCH": factory.now_epoch() - 5000,
            "LEASE_EXPIRES_EPOCH": factory.now_epoch() - 100,
            "HEARTBEAT_PID": 99999999,
        },
    )
    result = factory.recover(tmp_path)
    assert result["count"] == 1
    assert factory.load_job(tmp_path, job["JOB_ID"])["STATUS"] == "RECOVERABLE"
    assert factory.read_lease(tmp_path, job["JOB_ID"]) is None


def test_redaction_removes_secret_shapes() -> None:
    assert "[REDACTED]" in factory.redact("api_key=sk-abcdef1234567890")
    assert "[REDACTED]" in factory.redact("Authorization: Bearer ghp_abcdefghijklmnop")


def test_worktree_isolation_roundtrip(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@example.com"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "tester"], check=True)
    (repo / "a.txt").write_text("a", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "init"], check=True)
    base = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()

    job = factory.make_job(
        owner_agent="dealix-engineer",
        business_goal="isolation",
        job_class="ENGINEERING",
        base_sha=base,
        modifying=True,
    )
    job["REPO"] = str(repo)
    created = factory.create_worktree(job, repo_root=repo, worktree_root=tmp_path / "wt")
    assert created["ok"] is True
    assert Path(created["path"]).is_dir()
    job["WORKTREE"] = created["path"]
    removed = factory.cleanup_worktree(job, repo_root=repo)
    assert removed["ok"] is True
    assert not Path(created["path"]).exists()


def test_autonomy_acceptance_end_to_end(tmp_path: Path) -> None:
    receipt = factory.run_autonomy_acceptance(tmp_path)
    assert receipt["overall"] == "PASS", receipt["evidence"]
    assert receipt["external_effect"] == "NONE"
    assert all(receipt["checks"].values())


def test_share_state_skipped_for_non_root(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(factory.os, "geteuid", lambda: 1000)
    result = factory.share_state_with_operator(tmp_path)
    assert result == {"shared": False, "reason": "not-root"}


def test_share_state_reports_absent_operator(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(factory.os, "geteuid", lambda: 0)

    def _missing(_name):
        raise KeyError(_name)

    monkeypatch.setattr(factory.pwd, "getpwnam", _missing)
    result = factory.share_state_with_operator(tmp_path)
    assert result == {"shared": False, "reason": "operator-absent"}


def test_share_state_applies_operator_group(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "jobs").mkdir()
    (tmp_path / "jobs" / "J.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(factory.os, "geteuid", lambda: 0)
    monkeypatch.setattr(factory.pwd, "getpwnam", lambda _name: type("PW", (), {"pw_gid": 1234})())
    calls: list[tuple] = []
    monkeypatch.setattr(factory.os, "chown", lambda *a: calls.append(a))
    monkeypatch.setattr(factory.os, "chmod", lambda *a: calls.append(a))
    result = factory.share_state_with_operator(tmp_path)
    assert result["shared"] is True
    assert result["group"] == "dealix"
    assert result["paths"] >= 1
    assert any(len(call) == 3 and call[2] == 1234 for call in calls)
    assert any(len(call) == 2 and call[0] == tmp_path and call[1] == 0o770 for call in calls)
    assert any(len(call) == 2 and isinstance(call[1], int) and (call[1] & 0o060) == 0o060 for call in calls)


def test_resolve_opencode_binary_falls_back_to_home(tmp_path: Path, monkeypatch) -> None:
    binary = tmp_path / ".opencode" / "bin" / "opencode"
    binary.parent.mkdir(parents=True)
    binary.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    binary.chmod(0o700)
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr(factory.shutil, "which", lambda _name: None)
    assert factory.resolve_opencode_binary() == str(binary)


def test_resolve_opencode_binary_returns_none_without_path(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr(factory.shutil, "which", lambda _name: None)
    assert factory.resolve_opencode_binary() is None


def test_execute_opencode_places_auto_after_run(tmp_path: Path, monkeypatch) -> None:
    binary = tmp_path / "opencode"
    binary.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    binary.chmod(0o700)
    policy = tmp_path / "permissions.json"
    policy.write_text("{}", encoding="utf-8")
    captured: dict[str, object] = {}
    monkeypatch.setattr(factory, "resolve_opencode_binary", lambda: str(binary))
    monkeypatch.setenv("DEALIX_OPENCODE_PERMISSION_POLICY", str(policy))
    # Canonical free evidence: the broker resolves an explicit-free catalog model.
    monkeypatch.setattr(factory, "discover_catalog", lambda refresh=False: ["opencode/nemotron-3-ultra-free"])
    monkeypatch.setattr(factory, "discover_ollama_models", lambda: [])
    monkeypatch.setattr(factory, "discover_router_models", lambda: [])
    def _capture(argv, cwd, timeout=600, env=None, stdin=None):
        captured["argv"] = argv
        return {"ok": True, "returncode": 0, "stdout": "ok", "stderr": "", "duration_s": 0}
    monkeypatch.setattr(factory, "run_argv", _capture)
    job = factory.make_job(owner_agent="dealix-engineer", business_goal="canary", job_class="REVIEW", authority_level="L2", modifying=False, data_sensitivity="INTERNAL", executor={"prompt":"inspect"})
    result = factory.execute_opencode_cli(job, tmp_path, db_dir=tmp_path)
    assert result["ok"] is True
    argv = captured["argv"]
    assert argv[:5] == [str(binary), "run", "--auto", "--format", "json"]


def test_execute_opencode_uses_selected_model_file(tmp_path: Path, monkeypatch) -> None:
    binary = tmp_path / "opencode"
    binary.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    binary.chmod(0o700)
    policy = tmp_path / "permissions.json"
    policy.write_text("{}", encoding="utf-8")
    selected = tmp_path / "selected-model"
    selected.write_text("opencode/example-free\n", encoding="utf-8")
    captured: dict[str, object] = {}
    monkeypatch.setattr(factory, "resolve_opencode_binary", lambda: str(binary))
    monkeypatch.setenv("DEALIX_OPENCODE_PERMISSION_POLICY", str(policy))
    monkeypatch.setenv("DEALIX_OPENCODE_SELECTED_MODEL_FILE", str(selected))
    # Current catalog membership is required even for selection-file models.
    monkeypatch.setattr(factory, "discover_catalog", lambda refresh=False: ["opencode/example-free"])
    monkeypatch.setattr(factory, "discover_ollama_models", lambda: [])
    monkeypatch.setattr(factory, "discover_router_models", lambda: [])
    def _capture(argv, cwd, timeout=600, env=None, stdin=None):
        captured["argv"] = argv
        return {"ok": True, "returncode": 0, "stdout": "ok", "stderr": "", "duration_s": 0}
    monkeypatch.setattr(factory, "run_argv", _capture)
    job = factory.make_job(owner_agent="dealix-engineer", business_goal="canary", job_class="REVIEW", authority_level="L2", modifying=False, data_sensitivity="INTERNAL", executor={"prompt":"inspect"})
    result = factory.execute_opencode_cli(job, tmp_path, db_dir=tmp_path)
    assert result["ok"] is True
    argv = captured["argv"]
    assert argv[0:5] == [str(binary), "run", "--auto", "--format", "json"]
    assert argv[5:7] == ["-m", "opencode/example-free"]


def test_execute_opencode_uses_go_broker_for_r4(tmp_path: Path, monkeypatch) -> None:
    binary = tmp_path / "opencode"
    binary.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    binary.chmod(0o700)
    policy = tmp_path / "permissions.json"
    policy.write_text("{}", encoding="utf-8")
    captured: dict[str, object] = {}
    monkeypatch.setattr(factory, "resolve_opencode_binary", lambda: str(binary))
    monkeypatch.setenv("DEALIX_OPENCODE_PERMISSION_POLICY", str(policy))
    monkeypatch.setenv("DEALIX_OPENCODE_GO_USE_BALANCE", "disabled")
    monkeypatch.setenv("DEALIX_OPENCODE_GO_COST_AUTHORITY_REF", "test_verified_disabled")
    monkeypatch.setattr(factory, "discover_catalog", lambda refresh=False: ["opencode-go/glm-5.3"])
    monkeypatch.setattr(factory, "discover_ollama_models", lambda: ["qwen3:4b"])
    monkeypatch.setattr(factory, "discover_router_models", lambda: ["dealix-local"])
    def _capture(argv, cwd, timeout=600, env=None, stdin=None):
        captured["argv"] = argv
        return {"ok": True, "returncode": 0, "stdout": "ok", "stderr": "", "duration_s": 0}
    monkeypatch.setattr(factory, "run_argv", _capture)
    job = factory.make_job(owner_agent="dealix-engineer", business_goal="canary", job_class="REVIEW", authority_level="L2", modifying=False, data_sensitivity="INTERNAL", executor={"prompt":"inspect"})
    assert factory.execute_opencode_cli(job, tmp_path, db_dir=tmp_path)["ok"] is True
    assert captured["argv"][5:7] == ["-m", "opencode-go/glm-5.3"]


def _opencode_job(**overrides):
    kwargs = {
        "owner_agent": "dealix-engineer",
        "business_goal": "control-path canary",
        "job_class": "REVIEW",
        "authority_level": "L2",
        "modifying": False,
        "data_sensitivity": "INTERNAL",
        "executor": {"prompt": "inspect"},
    }
    kwargs.update(overrides)
    return factory.make_job(**kwargs)


def test_opencode_fails_closed_without_permission_policy(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_OPENCODE_PERMISSION_POLICY", str(tmp_path / "missing.json"))
    monkeypatch.setattr(factory, "resolve_opencode_binary", lambda: "/usr/bin/true")

    def _boom(*_args, **_kwargs):
        raise AssertionError("run_argv must not be called without the hardened policy")

    monkeypatch.setattr(factory, "run_argv", _boom)
    result = factory.execute_opencode_cli(_opencode_job(), tmp_path)
    assert result["ok"] is False
    assert result["returncode"] == 78
    assert "policy" in result["stderr"]


def test_opencode_fails_closed_when_control_db_unavailable(tmp_path: Path, monkeypatch) -> None:
    policy = tmp_path / "permissions.json"
    policy.write_text("{}", encoding="utf-8")
    monkeypatch.setenv("DEALIX_OPENCODE_PERMISSION_POLICY", str(policy))
    monkeypatch.setattr(factory, "resolve_opencode_binary", lambda: "/usr/bin/true")

    def _boom(*_args, **_kwargs):
        raise AssertionError("run_argv must not be called without a writable control DB")

    monkeypatch.setattr(factory, "run_argv", _boom)
    blocker = tmp_path / "blocker"
    blocker.write_text("not-a-dir", encoding="utf-8")
    result = factory.execute_opencode_cli(_opencode_job(), tmp_path, db_dir=blocker / "opencode")
    assert result["ok"] is False
    assert result["returncode"] == 73
    assert "control-db-unavailable" in result["stderr"]


def test_opencode_isolates_control_path_and_stdin(tmp_path: Path, monkeypatch) -> None:
    policy = tmp_path / "permissions.json"
    policy.write_text('{"bash":{"*":"allow"}}', encoding="utf-8")
    monkeypatch.setenv("DEALIX_OPENCODE_PERMISSION_POLICY", str(policy))
    monkeypatch.setattr(factory, "resolve_opencode_binary", lambda: "/usr/bin/true")
    # Canonical free evidence so the launch does not depend on host state.
    monkeypatch.setattr(factory, "discover_catalog", lambda refresh=False: ["opencode/nemotron-3-ultra-free"])
    monkeypatch.setattr(factory, "discover_ollama_models", lambda: [])
    monkeypatch.setattr(factory, "discover_router_models", lambda: [])
    captured: dict[str, object] = {}

    def _capture(argv, cwd, timeout=600, env=None, stdin=None):
        captured.update(argv=argv, env=env, stdin=stdin)
        return {"ok": True, "returncode": 0, "stdout": "ok", "stderr": "", "duration_s": 0}

    monkeypatch.setattr(factory, "run_argv", _capture)
    job = _opencode_job()
    assert factory.execute_opencode_cli(job, tmp_path, db_dir=tmp_path / "oc")["ok"] is True
    argv = captured["argv"]
    env = captured["env"]
    assert argv[:5] == ["/usr/bin/true", "run", "--auto", "--format", "json"]
    assert env["OPENCODE_PERMISSION"] == '{"bash":{"*":"allow"}}'
    assert env["OPENCODE_DB"] == str(tmp_path / "oc" / f"{job['JOB_ID']}.db")
    assert env["OPENCODE_DISABLE_AUTOUPDATE"] == "1"
    assert env["OPENCODE_DISABLE_MODELS_FETCH"] == "1"
    assert captured["stdin"] is subprocess.DEVNULL
    assert (tmp_path / "oc").is_dir()


def test_opencode_control_db_is_unique_per_job(tmp_path: Path) -> None:
    first = factory.opencode_db_path(_opencode_job(), tmp_path)
    second = factory.opencode_db_path(_opencode_job(), tmp_path)
    assert first != second
    assert first.parent == second.parent == tmp_path


def test_run_argv_forwards_stdin_to_subprocess(tmp_path: Path, monkeypatch) -> None:
    captured: dict[str, object] = {}

    class _Completed:
        returncode = 0
        stdout = "ok"
        stderr = ""

    def _run(argv, **kwargs):
        captured.update(kwargs)
        return _Completed()

    monkeypatch.setattr(factory.subprocess, "run", _run)
    factory.run_argv(["true"], tmp_path, stdin=subprocess.DEVNULL)
    assert captured["stdin"] is subprocess.DEVNULL


def _receipt_job(stdout: str, marker: str = "ARM_PORTFOLIO_RECEIPT:ARM-001"):
    return _deterministic_job(
        executor={"argv": ["python3", "-c", f"print({stdout!r})"]},
        acceptance={
            "criteria": "receipt marker required",
            "checks": [{"kind": "exit_zero"}, {"kind": "stdout_contains", "text": marker}],
        },
    )


def test_stdout_contains_acceptance_passes_with_marker(tmp_path: Path) -> None:
    job = _receipt_job("ARM_PORTFOLIO_RECEIPT:ARM-001")
    factory.submit_job(tmp_path, job)
    outcome = factory.run_job(tmp_path, factory.load_job(tmp_path, job["JOB_ID"]))
    assert outcome["status"] == "SUCCEEDED"
    assert outcome["acceptance"]["passed"] is True


def test_stdout_contains_acceptance_fails_when_marker_missing(tmp_path: Path) -> None:
    job = _receipt_job("exit zero but no receipt")
    factory.submit_job(tmp_path, job)
    outcome = factory.run_job(tmp_path, factory.load_job(tmp_path, job["JOB_ID"]))
    assert outcome["status"] == "FAILED"
    assert outcome["acceptance"]["passed"] is False
    checks = {item["kind"]: item["ok"] for item in outcome["acceptance"]["checks"]}
    assert checks["exit_zero"] is True
    assert checks["stdout_contains"] is False


def test_stdout_contains_empty_marker_fails_closed(tmp_path: Path) -> None:
    job = _receipt_job("ARM_PORTFOLIO_RECEIPT:ARM-001", marker="")
    factory.submit_job(tmp_path, job)
    outcome = factory.run_job(tmp_path, factory.load_job(tmp_path, job["JOB_ID"]))
    assert outcome["status"] == "FAILED"
    assert outcome["acceptance"]["passed"] is False


def test_stdout_contains_uses_full_output_beyond_evidence_preview(tmp_path: Path) -> None:
    marker = "RECEIPT_AFTER_3000_CHARS"
    job = _deterministic_job(
        executor={"argv": ["python3", "-c", f"print('x' * 3500 + '{marker}')"]},
        acceptance={
            "criteria": "marker required after long stdout",
            "checks": [{"kind": "exit_zero"}, {"kind": "stdout_contains", "text": marker}],
        },
    )
    factory.submit_job(tmp_path, job)
    outcome = factory.run_job(tmp_path, factory.load_job(tmp_path, job["JOB_ID"]))
    assert outcome["status"] == "SUCCEEDED"
    assert outcome["acceptance"]["passed"] is True


def test_persisted_evidence_is_bounded_and_strips_full_stdout(tmp_path: Path) -> None:
    job = _deterministic_job(
        executor={"argv": ["python3", "-c", "print('y' * 5000)"]},
        acceptance={"criteria": "exit zero", "checks": [{"kind": "exit_zero"}]},
    )
    factory.submit_job(tmp_path, job)
    outcome = factory.run_job(tmp_path, factory.load_job(tmp_path, job["JOB_ID"]))
    assert outcome["status"] == "SUCCEEDED"
    persisted = json.loads((tmp_path / "jobs" / f"{job['JOB_ID']}.json").read_text(encoding="utf-8"))
    executor_evidence = persisted["RESULT"]["executor"]
    assert "stdout_full" not in executor_evidence
    assert "stderr_full" not in executor_evidence
    assert executor_evidence["stdout"].endswith("...[truncated]")
    assert len(executor_evidence["stdout"]) <= 2100
    assert "stdout_full" not in json.dumps(persisted["EVIDENCE"])


def test_persisted_evidence_remains_secret_redacted(tmp_path: Path) -> None:
    import base64

    secret = "sk-abcdef1234567890"
    encoded = base64.b64encode(f"api_key={secret}".encode()).decode()
    job = _deterministic_job(
        executor={"argv": ["python3", "-c", f"import base64;print(base64.b64decode('{encoded}').decode())"]},
        acceptance={"criteria": "exit zero", "checks": [{"kind": "exit_zero"}]},
    )
    factory.submit_job(tmp_path, job)
    factory.run_job(tmp_path, factory.load_job(tmp_path, job["JOB_ID"]))
    persisted = (tmp_path / "jobs" / f"{job['JOB_ID']}.json").read_text(encoding="utf-8")
    assert secret not in persisted
    assert "[REDACTED]" in persisted


def test_execute_local_ai_honors_bounded_timeout_and_generation(tmp_path: Path, monkeypatch) -> None:
    captured: dict[str, object] = {}

    class _Response:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return b'{"response":"sector analysis ok"}'

    def _urlopen(request, timeout):
        captured["timeout"] = timeout
        captured["body"] = factory.json.loads(request.data.decode("utf-8"))
        return _Response()

    monkeypatch.setattr(factory.urllib.request, "urlopen", _urlopen)
    job = factory.make_job(
        owner_agent="dealix-sales",
        business_goal="sector canary",
        job_class="LOCAL_AI",
        authority_level="L2",
        modifying=False,
        data_sensitivity="INTERNAL",
        executor={"prompt": "brief", "timeout_seconds": 75, "num_predict": 160},
        acceptance={"criteria": "bounded local analysis"},
    )
    result = factory.execute_local_ai(job, tmp_path)
    assert result["ok"] is True
    assert captured["timeout"] == 75
    assert captured["body"]["options"]["num_predict"] == 160


def test_execute_local_ai_default_timeout_allows_cpu_cold_start(tmp_path: Path, monkeypatch) -> None:
    captured: dict[str, object] = {}

    class _Response:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return b'{"response":"ok"}'

    def _urlopen(request, timeout):
        captured["timeout"] = timeout
        return _Response()

    monkeypatch.setattr(factory.urllib.request, "urlopen", _urlopen)
    job = factory.make_job(
        owner_agent="dealix-sales",
        business_goal="cold-start-safe",
        job_class="LOCAL_AI",
        authority_level="L2",
        modifying=False,
        data_sensitivity="INTERNAL",
        executor={"prompt": "brief"},
    )
    assert factory.execute_local_ai(job, tmp_path)["ok"] is True
    assert captured["timeout"] == 60


def test_execute_local_ai_caps_requested_bounds(tmp_path: Path, monkeypatch) -> None:
    captured: dict[str, object] = {}

    class _Response:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return b'{"response":"ok"}'

    def _urlopen(request, timeout):
        captured["timeout"] = timeout
        captured["body"] = factory.json.loads(request.data.decode("utf-8"))
        return _Response()

    monkeypatch.setattr(factory.urllib.request, "urlopen", _urlopen)
    job = factory.make_job(
        owner_agent="dealix-sales",
        business_goal="bounded",
        job_class="LOCAL_AI",
        authority_level="L2",
        modifying=False,
        data_sensitivity="INTERNAL",
        executor={"prompt": "brief", "timeout_seconds": 999, "num_predict": 9999},
        acceptance={"criteria": "bounded local analysis"},
    )
    assert factory.execute_local_ai(job, tmp_path)["ok"] is True
    assert captured["timeout"] == 120
    assert captured["body"]["options"]["num_predict"] == 256


def _stub_opencode_env(tmp_path: Path, monkeypatch, *, selected_text=None, catalog=None) -> None:
    binary = tmp_path / "opencode"
    binary.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    binary.chmod(0o700)
    policy = tmp_path / "permissions.json"
    policy.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(factory, "resolve_opencode_binary", lambda: str(binary))
    monkeypatch.setenv("DEALIX_OPENCODE_PERMISSION_POLICY", str(policy))
    selected = tmp_path / "selected-model"
    if selected_text is not None:
        selected.write_text(selected_text, encoding="utf-8")
    monkeypatch.setenv("DEALIX_OPENCODE_SELECTED_MODEL_FILE", str(selected))
    monkeypatch.setattr(factory, "discover_catalog", lambda refresh=False: list(catalog) if catalog is not None else [])
    monkeypatch.setattr(factory, "discover_ollama_models", lambda: [])
    monkeypatch.setattr(factory, "discover_router_models", lambda: [])


def _never_launch(monkeypatch) -> list:
    launched: list = []

    def _boom(argv, cwd, timeout=600, env=None, stdin=None):
        launched.append(argv)
        raise AssertionError("executor launched without model authority")

    monkeypatch.setattr(factory, "run_argv", _boom)
    return launched


def test_process_queue_caller_limit_cannot_exceed_governor(tmp_path: Path, monkeypatch) -> None:
    available = int(factory.governor_state(tmp_path)["deep_wip_available"])
    assert available >= 1
    for index in range(available + 2):
        factory.submit_job(tmp_path, _deterministic_job(modifying=True, business_goal=f"cap {index}"))
    calls: list[str] = []

    def _stub(root, job, **kwargs):
        calls.append(job["JOB_ID"])
        return {"ok": True, "status": "SUCCEEDED", "job": job}

    monkeypatch.setattr(factory, "run_job", _stub)
    factory.process_queue(tmp_path, limit=10**6)
    assert len(calls) == available


def test_process_queue_caller_limit_only_reduces(tmp_path: Path, monkeypatch) -> None:
    available = int(factory.governor_state(tmp_path)["deep_wip_available"])
    assert available >= 1
    for index in range(available + 2):
        factory.submit_job(tmp_path, _deterministic_job(modifying=True, business_goal=f"reduce {index}"))
    calls: list[str] = []

    def _stub(root, job, **kwargs):
        calls.append(job["JOB_ID"])
        return {"ok": True, "status": "SUCCEEDED", "job": job}

    monkeypatch.setattr(factory, "run_job", _stub)
    factory.process_queue(tmp_path, limit=1)
    assert len(calls) == min(1, available)


def test_execute_opencode_rejects_stale_nonfree_selected_model(tmp_path: Path, monkeypatch) -> None:
    _stub_opencode_env(tmp_path, monkeypatch, selected_text="opencode/paid-evil\n")
    launched = _never_launch(monkeypatch)
    result = factory.execute_opencode(_opencode_job(), tmp_path, db_dir=tmp_path / "oc")
    assert result["ok"] is False
    assert result["returncode"] == 79
    assert launched == []


def test_execute_opencode_holds_when_model_authority_unavailable(tmp_path: Path, monkeypatch) -> None:
    _stub_opencode_env(tmp_path, monkeypatch, selected_text=None)
    launched = _never_launch(monkeypatch)
    result = factory.execute_opencode(_opencode_job(), tmp_path, db_dir=tmp_path / "oc")
    assert result["ok"] is False
    assert result["returncode"] == 79
    assert "model-authority-unavailable" in result["stderr"]
    assert launched == []


def test_execute_opencode_rejects_caller_paid_model(tmp_path: Path, monkeypatch) -> None:
    _stub_opencode_env(tmp_path, monkeypatch, selected_text="opencode/legit-free\n")
    launched = _never_launch(monkeypatch)
    job = _opencode_job(executor={"prompt": "inspect", "model": "opencode/paid-evil"})
    result = factory.execute_opencode(job, tmp_path, db_dir=tmp_path / "oc")
    assert result["ok"] is False
    assert result["returncode"] == 79
    assert "model-authority-unproven" in result["stderr"]
    assert launched == []


def _init_git_repo(path: Path) -> str:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "t@example.com"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "tester"], check=True)
    (path / "a.txt").write_text("a", encoding="utf-8")
    subprocess.run(["git", "-C", str(path), "add", "."], check=True)
    subprocess.run(["git", "-C", str(path), "commit", "-qm", "init"], check=True)
    return subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()


def test_create_worktree_requires_live_base_for_modifying(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    _init_git_repo(repo)
    job = factory.make_job(
        owner_agent="dealix-engineer",
        business_goal="live base required",
        job_class="ENGINEERING",
        modifying=True,
    )
    job["REPO"] = str(repo)
    job["BASE_SHA"] = None
    missing = factory.create_worktree(job, repo_root=repo, worktree_root=tmp_path / "wt")
    assert missing["ok"] is False
    assert missing["reason"] == "live-base-required-no-frozen-fallback"

    job["BASE_SHA"] = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
    bogus = factory.create_worktree(job, repo_root=repo, worktree_root=tmp_path / "wt")
    assert bogus["ok"] is False
    assert bogus["reason"] == "live-base-unresolvable"


def test_frozen_release_default_has_no_baked_historical_sha() -> None:
    source = (ROOT / "scripts/ops/session_factory.py").read_text(encoding="utf-8")
    assert "8bb0a6c382c49ca288f7b579cae07676f006e229" not in source
    expected = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    assert factory.resolve_source_checkout_sha(ROOT) == expected


def test_make_job_withholds_frozen_base_for_modifying(monkeypatch) -> None:
    # Simulate failed live git resolution: strict lookup yields nothing.
    monkeypatch.setattr(factory, "resolve_live_base_sha", lambda repo_root=None: None)
    monkeypatch.delenv("DEALIX_AGENTIC_BASE_SHA", raising=False)
    modifying = factory.make_job(
        owner_agent="dealix-engineer", business_goal="x", job_class="ENGINEERING", modifying=True
    )
    assert modifying["MODIFYING"] is True
    assert not modifying["BASE_SHA"]
    readonly = factory.make_job(
        owner_agent="dealix-pm", business_goal="x", job_class="DETERMINISTIC", modifying=False
    )
    assert readonly["BASE_SHA"] == factory.FROZEN_RELEASE_SHA
    explicit = factory.make_job(
        owner_agent="dealix-engineer",
        business_goal="x",
        job_class="ENGINEERING",
        modifying=True,
        base_sha="abc123",
    )
    assert explicit["BASE_SHA"] == "abc123"


def test_make_job_to_worktree_chain_fails_closed_without_live_base(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(factory, "resolve_live_base_sha", lambda repo_root=None: None)
    monkeypatch.delenv("DEALIX_AGENTIC_BASE_SHA", raising=False)
    repo = tmp_path / "repo"
    _init_git_repo(repo)
    job = factory.make_job(
        owner_agent="dealix-engineer", business_goal="chain", job_class="ENGINEERING", modifying=True
    )
    job["REPO"] = str(repo)
    created = factory.create_worktree(job, repo_root=repo, worktree_root=tmp_path / "wt")
    assert created["ok"] is False
    assert created["reason"] == "live-base-required-no-frozen-fallback"


def _boom_urlopen(*_args, **_kwargs):
    raise AssertionError("no daemon HTTP before model HOLD")


def test_execute_opencode_rejects_fabricated_free_model(tmp_path: Path, monkeypatch) -> None:
    _stub_opencode_env(tmp_path, monkeypatch, selected_text=None, catalog=["opencode/real-free"])
    monkeypatch.setattr(factory.urllib.request, "urlopen", _boom_urlopen)
    launched = _never_launch(monkeypatch)
    job = _opencode_job(executor={"prompt": "inspect", "model": "opencode/fake-free"})
    result = factory.execute_opencode(job, tmp_path, db_dir=tmp_path / "oc")
    assert result["ok"] is False
    assert result["returncode"] == 79
    assert "model-authority-unproven" in result["stderr"]
    assert launched == []


def test_execute_opencode_rejects_stale_free_selection(tmp_path: Path, monkeypatch) -> None:
    _stub_opencode_env(
        tmp_path, monkeypatch, selected_text="opencode/old-free\n", catalog=["opencode/real-free"]
    )
    monkeypatch.setattr(factory.urllib.request, "urlopen", _boom_urlopen)
    launched = _never_launch(monkeypatch)
    result = factory.execute_opencode(_opencode_job(), tmp_path, db_dir=tmp_path / "oc")
    assert result["ok"] is False
    assert result["returncode"] == 79
    assert "model-authority-unavailable" in result["stderr"]
    assert launched == []


def test_canonical_agent_ids_are_registry_bound() -> None:
    ids = factory.canonical_agent_ids()
    assert ids is not None and len(ids) > 0
    assert "dealix.group.engineering" in ids
    assert "dealix.group.this-agent-does-not-exist" not in ids


def test_validate_rejects_orphan_hierarchical_owner() -> None:
    job = _deterministic_job(owner_agent="dealix.group.this-agent-does-not-exist")
    errors = factory.validate_job(job)
    assert any("OWNER_AGENT" in error for error in errors)


class _FakeDaemonResponse:
    def __init__(self, status: int, text: str) -> None:
        self.status = status
        self._text = text

    def read(self) -> bytes:
        return self._text.encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args) -> bool:
        return False


class _FakeDaemonHTTP:
    def __init__(self, routes) -> None:
        self.routes = list(routes)
        self.calls: list = []
        self.bodies: list = []

    def __call__(self, request, timeout=None):
        method = request.get_method()
        url = request.full_url
        raw = getattr(request, "data", None)
        self.calls.append((method, url))
        self.bodies.append(raw.decode("utf-8") if raw else None)
        for (route_method, needle), (status, payload) in self.routes:
            if route_method == method and needle in url:
                text = payload if isinstance(payload, str) else json.dumps(payload)
                return _FakeDaemonResponse(status, text)
        raise AssertionError(f"unexpected daemon call: {method} {url}")


def _live_success_messages(marker: str = "FREE_API_CANARY_OK") -> dict:
    # Real live payload shape: role/finish nested under info.
    return {
        "messages": [
            {
                "info": {"role": "user", "finish": "stop"},
                "parts": [{"type": "text", "text": "Reply with exactly FREE_API_CANARY_OK"}],
            },
            {
                "info": {"role": "assistant", "finish": "stop"},
                "parts": [{"type": "text", "text": marker}],
            },
        ]
    }


def test_daemon_parser_matches_live_info_nested_shape() -> None:
    done, clean, text, error = factory._daemon_terminal_state(_live_success_messages())
    assert done is True
    assert clean is True
    assert "FREE_API_CANARY_OK" in text
    assert error == ""


def test_daemon_parser_reports_info_nested_error_shape() -> None:
    payload = {
        "messages": [
            {
                "info": {"role": "assistant", "finish": "error", "error": "model overloaded"},
                "parts": [{"type": "text", "text": "partial"}],
            }
        ]
    }
    done, clean, text, error = factory._daemon_terminal_state(payload)
    assert done is True
    assert clean is False
    assert "overloaded" in error


def test_daemon_parser_reports_part_error_shape() -> None:
    payload = {
        "messages": [
            {
                "role": "assistant",
                "finish": "error",
                "parts": [{"type": "text", "text": "x", "error": "part failed"}],
            }
        ]
    }
    done, clean, _text, error = factory._daemon_terminal_state(payload)
    assert done is True
    assert clean is False
    assert "part failed" in error


def _daemon_job(**overrides):
    kwargs = {
        "owner_agent": "dealix-engineer",
        "business_goal": "daemon canary",
        "job_class": "REVIEW",
        "authority_level": "L2",
        "modifying": False,
        "data_sensitivity": "PUBLIC",
        "executor": {"prompt": "Reply with exactly FREE_API_CANARY_OK", "model": "opencode/muse-spark-1.3-contributor-free"},
    }
    kwargs.update(overrides)
    return factory.make_job(**kwargs)


def _daemon_success_routes(marker: str = "FREE_API_CANARY_OK"):
    return [
        (("GET", "/global/health"), (200, {"healthy": True, "version": "1.18.30"})),
        (("POST", "prompt_async"), (204, "")),
        (("GET", "/message"), (200, _live_success_messages(marker))),
        (("POST", "/session?"), (200, {"id": "sess-1"})),
    ]


def test_daemon_executes_bounded_session_with_pinned_model(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(factory, "discover_catalog", lambda refresh=False: ["opencode/muse-spark-1.3-contributor-free"])
    monkeypatch.setattr(factory, "discover_ollama_models", lambda: [])
    monkeypatch.setattr(factory, "discover_router_models", lambda: [])
    fake = _FakeDaemonHTTP(_daemon_success_routes())
    monkeypatch.setattr(factory.urllib.request, "urlopen", fake)

    def _boom(argv, cwd, timeout=600, env=None, stdin=None):
        raise AssertionError("direct CLI must not run when the daemon path succeeds")

    monkeypatch.setattr(factory, "run_argv", _boom)
    job = _daemon_job()
    result = factory.execute_opencode_daemon(job, tmp_path, model="opencode/muse-spark-1.3-contributor-free")
    assert result["ok"] is True
    assert result["via"] == "daemon"
    assert result["session_id"] == "sess-1"
    assert "FREE_API_CANARY_OK" in (result.get("stdout_full") or "")
    create_bodies = [
        json.loads(body)
        for (method, url), body in zip(fake.calls, fake.bodies)
        if method == "POST" and "/session?" in url
    ]
    assert create_bodies and create_bodies[0]["model"] == {
        "providerID": "opencode",
        "id": "muse-spark-1.3-contributor-free",
    }
    prompt_bodies = [
        json.loads(body)
        for (method, url), body in zip(fake.calls, fake.bodies)
        if method == "POST" and "prompt_async" in url
    ]
    assert prompt_bodies and prompt_bodies[0]["model"] == {
        "providerID": "opencode",
        "modelID": "muse-spark-1.3-contributor-free",
    }
    assert prompt_bodies[0]["parts"] == [{"type": "text", "text": "Reply with exactly FREE_API_CANARY_OK"}]


def test_daemon_result_stdout_is_bounded_and_redacted(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(factory.urllib.request, "urlopen", _FakeDaemonHTTP(_daemon_success_routes("api_key=sk-abcdef1234567890")))
    job = _daemon_job()
    result = factory.execute_opencode_daemon(job, tmp_path, model="opencode/muse-spark-1.3-contributor-free")
    assert result["ok"] is True
    assert "sk-abcdef1234567890" not in (result.get("stdout") or "")
    assert "[REDACTED]" in (result.get("stdout") or "")


def test_orchestrator_fails_closed_when_daemon_down_without_opt_in(tmp_path: Path, monkeypatch) -> None:
    _stub_opencode_env(
        tmp_path, monkeypatch, selected_text=None, catalog=["opencode/muse-spark-1.3-contributor-free"]
    )
    monkeypatch.delenv("DEALIX_OPENCODE_ALLOW_CLI_FALLBACK", raising=False)

    import urllib.error

    def _down(*_args, **_kwargs):
        raise urllib.error.URLError("refused")

    monkeypatch.setattr(factory.urllib.request, "urlopen", _down)

    def _boom(argv, cwd, timeout=600, env=None, stdin=None):
        raise AssertionError("CLI fallback requires explicit opt-in")

    monkeypatch.setattr(factory, "run_argv", _boom)
    result = factory.execute_opencode(_daemon_job(), tmp_path, db_dir=tmp_path / "oc")
    assert result["ok"] is False
    assert result["returncode"] == 75
    assert result.get("daemon_unavailable") is True


def test_orchestrator_recovers_from_aborted_daemon_timeout_with_cli(tmp_path: Path, monkeypatch) -> None:
    _stub_opencode_env(
        tmp_path, monkeypatch, selected_text=None, catalog=["opencode/muse-spark-1.3-contributor-free"]
    )
    monkeypatch.delenv("DEALIX_OPENCODE_ALLOW_CLI_FALLBACK", raising=False)

    monkeypatch.setattr(
        factory,
        "execute_opencode_daemon",
        lambda *_args, **_kwargs: {
            "ok": False,
            "returncode": 124,
            "stdout": "",
            "stderr": "daemon-deadline-exceeded: session aborted",
            "duration_s": 10,
            "via": "daemon",
            "session_id": "sess-timeout",
            "model": "opencode/muse-spark-1.3-contributor-free",
        },
    )
    captured: dict[str, object] = {}

    def _capture(argv, cwd, timeout=600, env=None, stdin=None):
        captured["argv"] = argv
        return {"ok": True, "returncode": 0, "stdout": "ok", "stderr": "", "duration_s": 0}

    monkeypatch.setattr(factory, "run_argv", _capture)
    result = factory.execute_opencode(_daemon_job(), tmp_path, db_dir=tmp_path / "oc")
    assert result["ok"] is True
    assert result["fallback_reason"] == "daemon-timeout-after-abort"
    assert result["daemon_session_id"] == "sess-timeout"
    assert captured["argv"][:3] == [str(tmp_path / "opencode"), "run", "--auto"]


def test_orchestrator_cli_fallback_requires_explicit_opt_in(tmp_path: Path, monkeypatch) -> None:
    _stub_opencode_env(
        tmp_path, monkeypatch, selected_text=None, catalog=["opencode/muse-spark-1.3-contributor-free"]
    )
    monkeypatch.setenv("DEALIX_OPENCODE_ALLOW_CLI_FALLBACK", "1")

    import urllib.error

    def _down(*_args, **_kwargs):
        raise urllib.error.URLError("refused")

    monkeypatch.setattr(factory.urllib.request, "urlopen", _down)
    captured: dict[str, object] = {}

    def _capture(argv, cwd, timeout=600, env=None, stdin=None):
        captured["argv"] = argv
        return {"ok": True, "returncode": 0, "stdout": "ok", "stderr": "", "duration_s": 0}

    monkeypatch.setattr(factory, "run_argv", _capture)
    result = factory.execute_opencode(_daemon_job(), tmp_path, db_dir=tmp_path / "oc")
    assert result["ok"] is True
    assert captured["argv"][:5] == [str(tmp_path / "opencode"), "run", "--auto", "--format", "json"]



def test_live_base_guard_rejects_drift_and_allows_exact(monkeypatch) -> None:
    job = _opencode_job(modifying=True)
    job["BASE_SHA"] = "aaa"
    monkeypatch.setattr(factory, "resolve_live_base_sha", lambda repo_root=None: "bbb")
    drift = factory.verify_live_base_matches(job)
    assert drift["ok"] is False
    assert drift["reason"] == "live-base-guard: BASE_SHA drift"
    job["BASE_SHA"] = "bbb"
    assert factory.verify_live_base_matches(job)["ok"] is True
    readonly = _opencode_job(modifying=False)
    readonly["BASE_SHA"] = "stale-is-allowed-for-readonly"
    assert factory.verify_live_base_matches(readonly)["ok"] is True


def test_worktree_base_guard_rejects_stale_reused_worktree(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "Dealix Test"], check=True)
    (repo / "x.txt").write_text("x", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "x.txt"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "base"], check=True)
    head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    job = _opencode_job(modifying=True)
    job["BASE_SHA"] = head
    job["WORKTREE"] = str(repo)
    monkeypatch.setattr(factory, "resolve_live_base_sha", lambda repo_root=None: "new-live-main")
    result = factory.verify_worktree_base_matches(job)
    assert result["ok"] is False
    assert result["reason"] == "live-base-guard: worktree base drift"
    monkeypatch.setattr(factory, "resolve_live_base_sha", lambda repo_root=None: head)
    assert factory.verify_worktree_base_matches(job)["ok"] is True


def test_modifying_opencode_cli_is_forbidden(tmp_path: Path, monkeypatch) -> None:
    job = _opencode_job(modifying=True)
    monkeypatch.setattr(factory, "run_argv", lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("CLI must not launch")))
    result = factory.execute_opencode_cli(job, tmp_path, db_dir=tmp_path / "oc")
    assert result["ok"] is False
    assert result["returncode"] == 78
    assert result["fallback_denied"] == "modifying-worktree-isolation"


def test_run_job_rechecks_live_base_after_executor_before_acceptance(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "Dealix Test"], check=True)
    (repo / "x.txt").write_text("base", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "x.txt"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "base"], check=True)
    base = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()

    state = tmp_path / "state"
    wt = tmp_path / "worktree"
    job = factory.make_job(
        owner_agent="dealix-engineer", business_goal="post executor drift canary",
        job_class="ENGINEERING", authority_level="L4", base_sha=base, modifying=True,
        data_sensitivity="INTERNAL", executor={"prompt": "bounded"},
        acceptance={"criteria": "marker", "checks": [{"kind": "stdout_contains", "text": "SHOULD_NOT_ACCEPT"}]},
    )
    assert factory.submit_job(state, job)["ok"] is True

    live_values = iter([base, base, "new-live-main"])
    monkeypatch.setattr(factory, "resolve_live_base_sha", lambda repo_root=None: next(live_values))
    monkeypatch.setattr(factory, "create_worktree", lambda *_a, **_k: {"ok": True, "path": str(wt)})
    wt.mkdir()
    monkeypatch.setattr(factory, "verify_worktree_base_matches", lambda *_a, **_k: {"ok": True})
    monkeypatch.setitem(factory.EXECUTORS, "opencode", lambda *_a, **_k: {
        "ok": True, "returncode": 0, "stdout": "SHOULD_NOT_ACCEPT",
        "stdout_full": "SHOULD_NOT_ACCEPT", "stderr": "", "duration_s": 1,
    })
    monkeypatch.setattr(factory, "cleanup_worktree", lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("stale candidate must be preserved")))

    result = factory.run_job(state, job, repo_root=repo, worktree_root=tmp_path / "worktrees")
    assert result["ok"] is False
    assert result["status"] == "FAILED"
    assert result["acceptance"]["detail"] == "post_executor_live_base_guard"
    assert job["WORKTREE"] == str(wt)
    assert Path(job["WORKTREE"]).exists()
    assert job["NEXT_ACTION"] == "reconcile preserved candidate onto exact-current main and re-accept"
    assert job["RESULT"]["acceptance"]["passed"] is False


def test_modifying_daemon_timeout_never_falls_back_to_cli(tmp_path: Path, monkeypatch) -> None:
    job = _daemon_job(modifying=True)
    monkeypatch.setattr(factory, "_resolve_opencode_model", lambda _job: ("opencode/muse-spark-1.3-contributor-free", None))
    monkeypatch.setattr(factory, "execute_opencode_daemon", lambda *_a, **_k: {
        "ok": False, "returncode": 124, "stdout": "",
        "stderr": "daemon-deadline-exceeded: session aborted",
        "duration_s": 180, "via": "daemon", "session_id": "sess-timeout",
    })
    monkeypatch.setattr(factory, "execute_opencode_cli", lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("modifying CLI fallback must never run")))
    result = factory.execute_opencode(job, tmp_path, db_dir=tmp_path / "oc")
    assert result["ok"] is False
    assert result["returncode"] == 124
    assert result["fallback_denied"] == "modifying-worktree-isolation"

def test_daemon_rejects_non_loopback_url(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_OPENCODE_DAEMON_URL", "http://example.com:4098")
    monkeypatch.setattr(factory.urllib.request, "urlopen", _boom_urlopen)
    result = factory.execute_opencode_daemon(_daemon_job(), tmp_path, model="opencode/x-free")
    assert result["ok"] is False
    assert result.get("daemon_unavailable") is True


def test_daemon_rejects_version_mismatch(tmp_path: Path, monkeypatch) -> None:
    fake = _FakeDaemonHTTP([(("GET", "/global/health"), (200, {"healthy": True, "version": "2.0.0"}))])
    monkeypatch.setattr(factory.urllib.request, "urlopen", fake)
    result = factory.execute_opencode_daemon(_daemon_job(), tmp_path, model="opencode/x-free")
    assert result["ok"] is False
    assert result.get("daemon_unavailable") is True


def test_daemon_idle_timeout_aborts_before_full_job_deadline(tmp_path: Path, monkeypatch) -> None:
    routes = [
        (("GET", "/global/health"), (200, {"healthy": True, "version": "1.18.30"})),
        (("POST", "prompt_async"), (204, "")),
        (("GET", "/message"), (200, {"messages": []})),
        (("POST", "/session?"), (200, {"id": "sess-idle"})),
        (("POST", "/abort"), (200, {})),
    ]
    fake = _FakeDaemonHTTP(routes)
    monkeypatch.setattr(factory.urllib.request, "urlopen", fake)
    job = _daemon_job()
    job["TIME_BUDGET"] = 300
    result = factory.execute_opencode_daemon(
        job,
        tmp_path,
        model="opencode/muse-spark-1.3-contributor-free",
        timeout_s=2.0,
        idle_timeout_s=0.05,
        poll_interval=0.01,
    )
    assert result["ok"] is False
    assert result["returncode"] == 124
    assert "idle-timeout" in result["stderr"]
    assert result["session_id"] == "sess-idle"
    assert any("abort" in url for _method, url in fake.calls)


def test_daemon_timeout_aborts_session(tmp_path: Path, monkeypatch) -> None:
    routes = [
        (("GET", "/global/health"), (200, {"healthy": True, "version": "1.18.30"})),
        (("POST", "prompt_async"), (204, "")),
        (("GET", "/message"), (200, {"messages": []})),
        (("POST", "/session?"), (200, {"id": "sess-9"})),
        (("POST", "/abort"), (200, {})),
    ]
    fake = _FakeDaemonHTTP(routes)
    monkeypatch.setattr(factory.urllib.request, "urlopen", fake)
    job = _daemon_job()
    result = factory.execute_opencode_daemon(
        job, tmp_path, model="opencode/muse-spark-1.3-contributor-free", timeout_s=0.15, poll_interval=0.01
    )
    assert result["ok"] is False
    assert result["returncode"] == 124
    assert result["session_id"] == "sess-9"
    assert any("abort" in url for _method, url in fake.calls)


def test_daemon_parser_detects_completed_without_finish_field() -> None:
    """OpenCode 1.18.x empty-completion shape: info.time.completed, no finish.

    Captured from a real job (JOB-20260914T114823-9540001) where the provider
    returned an empty assistant message with no `finish` field. Without a
    fallback the poller never observed terminal state and exhausted the full
    job budget.
    """
    payload = {
        "messages": [
            {
                "info": {
                    "role": "user",
                    "time": {"created": 1789386515442},
                    "agent": "build",
                },
                "parts": [{"type": "text", "text": "do the bounded task"}],
            },
            {
                "info": {
                    "role": "assistant",
                    "time": {"created": 1789386517335, "completed": 1789387115763},
                    "agent": "build",
                    "modelID": "muse-spark-1.2-contributor-free",
                    "providerID": "opencode",
                },
                "parts": [],
            },
        ]
    }
    done, clean, _text, error = factory._daemon_terminal_state(payload)
    assert done is True, "completed assistant message must be terminal"
    assert clean is True
    assert error == ""


def test_daemon_parser_does_not_terminate_on_inflight_tool_calls() -> None:
    """Real tool-loop shape: assistant finish='tool-calls' with time.completed.

    Captured from live session ses_f640bfb14ffeDdLGOwU6kCVZoh (27 messages).
    Every intermediate assistant step is complete at the message level
    (time.completed set) but carries finish='tool-calls'. Treating it as
    terminal truncates multi-step jobs into false successes.
    """
    payload = {
        "messages": [
            {"info": {"role": "user", "time": {"created": 1}}, "parts": [{"type": "text", "text": "task"}]},
            {
                "info": {
                    "role": "assistant",
                    "finish": "tool-calls",
                    "time": {"created": 2, "completed": 3},
                },
                "parts": [{"type": "step-start"}, {"type": "tool", "tool": "read"}],
            },
        ]
    }
    done, clean, _text, _error = factory._daemon_terminal_state(payload)
    assert done is False, "finish=tool-calls must not terminate the session"
    assert clean is False


def test_daemon_parser_terminates_on_real_tool_loop_final_stop() -> None:
    """The final assistant message in a real tool loop carries finish='stop'."""
    payload = {
        "messages": [
            {"info": {"role": "user", "time": {"created": 1}}, "parts": [{"type": "text", "text": "task"}]},
            {
                "info": {"role": "assistant", "finish": "tool-calls", "time": {"created": 2, "completed": 3}},
                "parts": [{"type": "tool", "tool": "read"}],
            },
            {
                "info": {"role": "assistant", "finish": "stop", "time": {"created": 4, "completed": 5}},
                "parts": [{"type": "text", "text": "final answer"}],
            },
        ]
    }
    done, clean, text, error = factory._daemon_terminal_state(payload)
    assert done is True
    assert clean is True
    assert "final answer" in text
    assert error == ""


def test_model_job_requires_explicit_data_sensitivity() -> None:
    job = factory.make_job(
        owner_agent="dealix-engineer", business_goal="sensitivity gate",
        job_class="REVIEW", authority_level="L2", modifying=False,
        executor={"prompt": "inspect"},
    )
    errors = factory.validate_job(job)
    assert any("missing:DATA_SENSITIVITY" in error for error in errors)


def test_local_ai_missing_sensitivity_holds_before_network(tmp_path: Path, monkeypatch) -> None:
    job = factory.make_job(
        owner_agent="dealix-sales", business_goal="local sensitivity gate",
        job_class="LOCAL_AI", authority_level="L2", modifying=False,
        executor={"prompt": "brief"},
    )
    monkeypatch.setattr(
        factory.urllib.request, "urlopen",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("network must not be called")),
    )
    result = factory.execute_local_ai(job, tmp_path)
    assert result["ok"] is False
    assert result["returncode"] == 79
    assert "data-sensitivity-untrusted" in result["stderr"]


def test_model_job_rejects_invalid_data_sensitivity() -> None:
    job = factory.make_job(
        owner_agent="dealix-engineer", business_goal="sensitivity gate",
        job_class="REVIEW", authority_level="L2", modifying=False,
        data_sensitivity="secret-ish", executor={"prompt": "inspect"},
    )
    errors = factory.validate_job(job)
    assert any("invalid:DATA_SENSITIVITY=SECRET-ISH" in error for error in errors)


def test_deterministic_job_may_omit_data_sensitivity() -> None:
    errors = factory.validate_job(_deterministic_job())
    assert not any("DATA_SENSITIVITY" in error for error in errors)


def test_opencode_missing_sensitivity_holds_before_catalog(tmp_path: Path, monkeypatch) -> None:
    job = _opencode_job(data_sensitivity=None)
    monkeypatch.setattr(
        factory, "discover_catalog",
        lambda refresh=False: (_ for _ in ()).throw(AssertionError("catalog must not be queried")),
    )
    result = factory.execute_opencode(job, tmp_path, db_dir=tmp_path / "oc")
    assert result["ok"] is False
    assert result["returncode"] == 79
    assert "data-sensitivity-untrusted" in result["stderr"]


@pytest.mark.parametrize("sensitivity", ["CONFIDENTIAL", "RESTRICTED"])
def test_opencode_private_sensitivity_never_uses_remote_model(
    tmp_path: Path, monkeypatch, sensitivity: str
) -> None:
    job = _opencode_job(data_sensitivity=sensitivity)
    monkeypatch.setattr(
        factory, "discover_catalog",
        lambda refresh=False: (_ for _ in ()).throw(AssertionError("catalog must not be queried")),
    )
    result = factory.execute_opencode(job, tmp_path, db_dir=tmp_path / "oc")
    assert result["ok"] is False
    assert result["returncode"] == 79
    assert "data-sensitivity-remote-denied" in result["stderr"]
