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


def test_resource_governor_is_bounded() -> None:
    assert factory.compute_max_concurrent_deep({"mem_available_mb": 1000, "cpu_count": 4, "load1": 0}) == 1
    assert factory.compute_max_concurrent_deep({"mem_available_mb": 8000, "cpu_count": 4, "load1": 0}) == 3
    assert factory.compute_max_concurrent_deep({"mem_available_mb": 8000, "cpu_count": 4, "load1": 100}) == 1
    for mem in (500, 3000, 8000):
        value = factory.compute_max_concurrent_deep({"mem_available_mb": mem, "cpu_count": 8, "load1": 0})
        assert 1 <= value <= factory.DEEP_WIP_MAX


def test_submit_l5_waits_and_never_runs(tmp_path: Path) -> None:
    job = factory.make_job(
        owner_agent="dealix-sales",
        business_goal="material send",
        job_class="COMMERCIAL_REASONING",
        authority_level="L5",
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
    def _capture(argv, cwd, timeout=600, env=None, stdin=None):
        captured["argv"] = argv
        return {"ok": True, "returncode": 0, "stdout": "ok", "stderr": "", "duration_s": 0}
    monkeypatch.setattr(factory, "run_argv", _capture)
    job = factory.make_job(owner_agent="dealix-engineer", business_goal="canary", job_class="REVIEW", authority_level="L2", modifying=False, executor={"prompt":"inspect"})
    result = factory.execute_opencode(job, tmp_path, db_dir=tmp_path)
    assert result["ok"] is True
    argv = captured["argv"]
    assert argv[:3] == [str(binary), "run", "--auto"]


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
    monkeypatch.setattr(factory, "discover_catalog", lambda refresh=False: [])
    monkeypatch.setattr(factory, "discover_ollama_models", lambda: [])
    monkeypatch.setattr(factory, "discover_router_models", lambda: [])
    def _capture(argv, cwd, timeout=600, env=None, stdin=None):
        captured["argv"] = argv
        return {"ok": True, "returncode": 0, "stdout": "ok", "stderr": "", "duration_s": 0}
    monkeypatch.setattr(factory, "run_argv", _capture)
    job = factory.make_job(owner_agent="dealix-engineer", business_goal="canary", job_class="REVIEW", authority_level="L2", modifying=False, executor={"prompt":"inspect"})
    result = factory.execute_opencode(job, tmp_path, db_dir=tmp_path)
    assert result["ok"] is True
    argv = captured["argv"]
    assert argv[0:3] == [str(binary), "run", "--auto"]
    assert argv[3:5] == ["-m", "opencode/example-free"]


def test_execute_opencode_uses_go_broker_for_r4(tmp_path: Path, monkeypatch) -> None:
    binary = tmp_path / "opencode"
    binary.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    binary.chmod(0o700)
    policy = tmp_path / "permissions.json"
    policy.write_text("{}", encoding="utf-8")
    captured: dict[str, object] = {}
    monkeypatch.setattr(factory, "resolve_opencode_binary", lambda: str(binary))
    monkeypatch.setenv("DEALIX_OPENCODE_PERMISSION_POLICY", str(policy))
    monkeypatch.setattr(factory, "discover_catalog", lambda refresh=False: ["opencode-go/deepseek-v4.1-flash"])
    monkeypatch.setattr(factory, "discover_ollama_models", lambda: ["qwen3:4b"])
    monkeypatch.setattr(factory, "discover_router_models", lambda: ["dealix-local"])
    def _capture(argv, cwd, timeout=600, env=None, stdin=None):
        captured["argv"] = argv
        return {"ok": True, "returncode": 0, "stdout": "ok", "stderr": "", "duration_s": 0}
    monkeypatch.setattr(factory, "run_argv", _capture)
    job = factory.make_job(owner_agent="dealix-engineer", business_goal="canary", job_class="REVIEW", authority_level="L2", modifying=False, executor={"prompt":"inspect"})
    assert factory.execute_opencode(job, tmp_path, db_dir=tmp_path)["ok"] is True
    assert captured["argv"][3:5] == ["-m", "opencode-go/deepseek-v4.1-flash"]


def _opencode_job(**overrides):
    kwargs = {
        "owner_agent": "dealix-engineer",
        "business_goal": "control-path canary",
        "job_class": "REVIEW",
        "authority_level": "L2",
        "modifying": False,
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
    result = factory.execute_opencode(_opencode_job(), tmp_path)
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
    result = factory.execute_opencode(_opencode_job(), tmp_path, db_dir=blocker / "opencode")
    assert result["ok"] is False
    assert result["returncode"] == 73
    assert "control-db-unavailable" in result["stderr"]


def test_opencode_isolates_control_path_and_stdin(tmp_path: Path, monkeypatch) -> None:
    policy = tmp_path / "permissions.json"
    policy.write_text('{"bash":{"*":"allow"}}', encoding="utf-8")
    monkeypatch.setenv("DEALIX_OPENCODE_PERMISSION_POLICY", str(policy))
    monkeypatch.setattr(factory, "resolve_opencode_binary", lambda: "/usr/bin/true")
    captured: dict[str, object] = {}

    def _capture(argv, cwd, timeout=600, env=None, stdin=None):
        captured.update(argv=argv, env=env, stdin=stdin)
        return {"ok": True, "returncode": 0, "stdout": "ok", "stderr": "", "duration_s": 0}

    monkeypatch.setattr(factory, "run_argv", _capture)
    job = _opencode_job()
    assert factory.execute_opencode(job, tmp_path, db_dir=tmp_path / "oc")["ok"] is True
    argv = captured["argv"]
    env = captured["env"]
    assert argv[:3] == ["/usr/bin/true", "run", "--auto"]
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
        executor={"prompt": "brief", "timeout_seconds": 75, "num_predict": 160},
        acceptance={"criteria": "bounded local analysis"},
    )
    result = factory.execute_local_ai(job, tmp_path)
    assert result["ok"] is True
    assert captured["timeout"] == 75
    assert captured["body"]["options"]["num_predict"] == 160


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
        executor={"prompt": "brief", "timeout_seconds": 999, "num_predict": 9999},
        acceptance={"criteria": "bounded local analysis"},
    )
    assert factory.execute_local_ai(job, tmp_path)["ok"] is True
    assert captured["timeout"] == 120
    assert captured["body"]["options"]["num_predict"] == 256
