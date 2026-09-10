from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "commercial" / "run_dealix_master_company_cycle_v1.py"
INSTALLER = ROOT / "scripts" / "ops" / "install_dealix_omega_master_company_v1.sh"
BINDING = ROOT / "config" / "company" / "dealix_master_prompt_binding_v1.json"


def load_runner():
    spec = importlib.util.spec_from_file_location("dealix_master_runner_v2_test", RUNNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_binding_v2_requires_installed_hash_identity_and_all_arms() -> None:
    data = json.loads(BINDING.read_text(encoding="utf-8"))
    assert data["schema_version"] == 2
    assert data["binding_generation"] == "SERVER_FIRST_V2"
    assert data["runtime_binding_mode"] == "INSTALLED_ARTIFACTS_SHA256_FAIL_CLOSED"
    assert data["required_runtime_artifact_hash_match"] is True
    assert data["expected_arm_count"] == 44
    assert len(data["permanent_agents"]) == 5
    assert data["deep_wip_max"] == 3


def test_resolve_artifact_accepts_matching_installed_copy(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_runner()
    canonical = tmp_path / "canonical.txt"
    runtime = tmp_path / "runtime.txt"
    canonical.write_text("same", encoding="utf-8")
    runtime.write_text("same", encoding="utf-8")
    monkeypatch.setenv("DX_PATH", str(runtime))
    monkeypatch.setenv("DX_SHA", digest(runtime))
    path, sha, mode = module.resolve_artifact(canonical=canonical, path_env="DX_PATH", sha_env="DX_SHA")
    assert path == runtime
    assert sha == digest(canonical)
    assert mode == "INSTALLED_HASH_BOUND"


def test_resolve_artifact_rejects_declared_or_content_drift(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_runner()
    canonical = tmp_path / "canonical.txt"
    runtime = tmp_path / "runtime.txt"
    canonical.write_text("canonical", encoding="utf-8")
    runtime.write_text("drifted", encoding="utf-8")
    monkeypatch.setenv("DX_PATH", str(runtime))
    monkeypatch.setenv("DX_SHA", digest(runtime))
    with pytest.raises(RuntimeError, match="installed artifact drift"):
        module.resolve_artifact(canonical=canonical, path_env="DX_PATH", sha_env="DX_SHA")
    runtime.write_text("canonical", encoding="utf-8")
    monkeypatch.setenv("DX_SHA", "0" * 64)
    with pytest.raises(RuntimeError, match="declared SHA mismatch"):
        module.resolve_artifact(canonical=canonical, path_env="DX_PATH", sha_env="DX_SHA")


def test_installer_copies_binding_prompt_meta_and_never_creates_scheduler() -> None:
    text = INSTALLER.read_text(encoding="utf-8")
    for token in ("BINDING_TARGET", "PROMPT_TARGET", "META_TARGET", "DEALIX_MASTER_BINDING_SHA256", "DEALIX_COMPANY_MASTER_PROMPT_SHA256", "DEALIX_META_CONTROL_SHA256"):
        assert token in text
    for flag in json.loads(BINDING.read_text(encoding="utf-8"))["required_kill_switches"]:
        assert f"export {flag}=0" in text
    assert "systemctl enable" not in text
    assert "systemctl start" not in text


def test_master_runner_writes_durable_receipt_and_forces_l5_off() -> None:
    text = RUNNER.read_text(encoding="utf-8")
    assert "dealix.master-company-cycle.v2" in text
    assert 'env["DEALIX_UNIVERSAL_L5"] = "0"' in text
    assert '"material_external_effects_executed": False' in text
    assert "kill_switches_forced_off" in text


def test_installer_fails_closed_when_source_head_cannot_be_proven() -> None:
    text = INSTALLER.read_text(encoding="utf-8")
    assert 'SOURCE_HEAD="$(git -c safe.directory="$ROOT" -C "$ROOT" rev-parse --verify HEAD' in text
    assert "MASTER_COMPANY_INSTALL=BLOCKED_SOURCE_HEAD_UNRESOLVED" in text
    assert "MASTER_COMPANY_INSTALL=BLOCKED_SOURCE_HEAD_INVALID" in text
    assert "printf unknown" not in text
