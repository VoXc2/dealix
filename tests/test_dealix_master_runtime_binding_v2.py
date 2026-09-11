from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest

from auto_client_acquisition.intelligence.dealix_model_router import (
    _compose_bound_master_prompt,
    _fits_local_context,
)

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


def synthetic_master(version: str) -> str:
    return "\n\n".join(
        f"## {number}. CONTROL {number}\n{version} governed control section {number}."
        for number in (0, 2, 7, 8, 14)
    )


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


def test_bound_master_prompt_is_distilled_into_model_prompt(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    prompt = tmp_path / "master.md"
    prompt.write_text(synthetic_master("VERSION_A"), encoding="utf-8")
    monkeypatch.setenv("DEALIX_MASTER_PROMPT_BOUND", "1")
    monkeypatch.setenv("DEALIX_COMPANY_MASTER_PROMPT", str(prompt))
    monkeypatch.setenv("DEALIX_COMPANY_MASTER_PROMPT_SHA256", digest(prompt))

    composed_a = _compose_bound_master_prompt("Prepare the next action")
    assert "DEALIX RUNTIME CONTROL DIGEST" in composed_a
    assert "VERSION_A governed control section 0" in composed_a
    assert composed_a.endswith("Prepare the next action")

    prompt.write_text(synthetic_master("VERSION_B"), encoding="utf-8")
    monkeypatch.setenv("DEALIX_COMPANY_MASTER_PROMPT_SHA256", digest(prompt))
    composed_b = _compose_bound_master_prompt("Prepare the next action")
    assert "VERSION_B governed control section 14" in composed_b
    assert composed_b != composed_a


def test_real_master_runtime_digest_fits_canonical_8192_context(monkeypatch: pytest.MonkeyPatch) -> None:
    binding = json.loads(BINDING.read_text(encoding="utf-8"))
    prompt = ROOT / binding["prompt_ref"]
    monkeypatch.setenv("DEALIX_MASTER_PROMPT_BOUND", "1")
    monkeypatch.setenv("DEALIX_COMPANY_MASTER_PROMPT", str(prompt))
    monkeypatch.setenv("DEALIX_COMPANY_MASTER_PROMPT_SHA256", digest(prompt))
    monkeypatch.setenv("DEALIX_LOCAL_CONTEXT_TOKENS", "8192")
    composed = _compose_bound_master_prompt("Prepare one bounded next action.")
    assert len(composed) < 16_000
    assert _fits_local_context(composed, output_tokens=160) is True


def test_bound_master_prompt_hash_drift_fails_closed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    prompt = tmp_path / "master.md"
    prompt.write_text(synthetic_master("CANONICAL"), encoding="utf-8")
    monkeypatch.setenv("DEALIX_MASTER_PROMPT_BOUND", "1")
    monkeypatch.setenv("DEALIX_COMPANY_MASTER_PROMPT", str(prompt))
    monkeypatch.setenv("DEALIX_COMPANY_MASTER_PROMPT_SHA256", "0" * 64)
    with pytest.raises(RuntimeError, match="SHA mismatch"):
        _compose_bound_master_prompt("task")


def test_installer_copies_binding_prompt_meta_and_never_creates_scheduler() -> None:
    text = INSTALLER.read_text(encoding="utf-8")
    for token in ("BINDING_TARGET", "PROMPT_TARGET", "META_TARGET", "DEALIX_MASTER_BINDING_SHA256", "DEALIX_COMPANY_MASTER_PROMPT_SHA256", "DEALIX_META_CONTROL_SHA256"):
        assert token in text
    for flag in json.loads(BINDING.read_text(encoding="utf-8"))["required_kill_switches"]:
        assert f"export {flag}=0" in text
    assert "systemctl enable" not in text
    assert "systemctl start" not in text


def test_master_runner_uses_unique_invocation_and_forces_l5_off() -> None:
    text = RUNNER.read_text(encoding="utf-8")
    assert "dealix.master-company-cycle.v3" in text
    assert "uuid.uuid4().hex" in text
    assert 'env["DEALIX_COMMAND_ROOM_INVOCATION_ID"] = invocation_id' in text
    assert 'env["DEALIX_EXPECTED_REPOSITORY_HEAD"] = launch_head' in text
    assert 'command_room_receipt.get("invocation_id") == invocation_id' in text
    assert 'command_room_receipt.get("repository_head") == launch_head' in text
    assert 'env["DEALIX_UNIVERSAL_L5"] = "0"' in text
    assert '"material_external_effects_executed": False' in text
    assert "kill_switches_forced_off" in text


def test_installer_fails_closed_when_source_head_cannot_be_proven() -> None:
    text = INSTALLER.read_text(encoding="utf-8")
    assert 'SOURCE_HEAD="$(git -c safe.directory="$ROOT" -C "$ROOT" rev-parse --verify HEAD' in text
    assert "MASTER_COMPANY_INSTALL=BLOCKED_SOURCE_HEAD_UNRESOLVED" in text
    assert "MASTER_COMPANY_INSTALL=BLOCKED_SOURCE_HEAD_INVALID" in text
    assert "printf unknown" not in text
