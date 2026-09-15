from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "scripts/ops/render_hermes_sector_fabric_launcher.py"
VERIFIER = ROOT / "scripts/ops/verify_hermes_sector_fabric_launcher.py"
INSTALLER = ROOT / "scripts/ops/install_hermes_sector_fabric_launcher.sh"


def _load_renderer():
    spec = importlib.util.spec_from_file_location("sector_launcher_renderer", RENDERER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _git(path: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(path), *args], check=True, text=True, capture_output=True)
    return result.stdout.strip()


def _make_repo(path: Path) -> str:
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    _git(path, "config", "user.email", "test@example.invalid")
    _git(path, "config", "user.name", "Dealix Test")
    (path / "README.md").write_text("fixture\n", encoding="utf-8")
    _git(path, "add", "README.md")
    _git(path, "commit", "-qm", "fixture")
    return _git(path, "rev-parse", "HEAD")


def test_validate_sha_is_exact_lowercase() -> None:
    renderer = _load_renderer()
    good = "a" * 40
    assert renderer.validate_sha(good) == good
    for bad in ("a" * 39, "A" * 40, "not-a-sha"):
        with pytest.raises(ValueError):
            renderer.validate_sha(bad)


def test_rendered_launcher_is_source_bound_and_model_neutral(tmp_path: Path) -> None:
    renderer = _load_renderer()
    sha = "b" * 40
    repo = tmp_path / "repo"
    text = renderer.render_launcher(
        sha,
        repo=repo,
        state_dir=tmp_path / "sector",
        factory_state=tmp_path / "factory",
        lock_file=tmp_path / "sector.lock",
    )
    assert f"EXPECTED_SHA={sha}" in text
    assert "/opt/dealix/control/runtime/sector-fabric-" not in text
    assert 'git -C "$REPO" rev-parse HEAD' in text
    assert "HOLD_SOURCE_IDENTITY" in text
    assert "HOLD_DIRTY_SOURCE" in text
    assert '"$REPO/scripts/commercial/run_sector_hermes_fabric.py"' in text
    lowered = text.lower()
    assert "model=" not in lowered
    assert "provider=" not in lowered


def test_source_identity_mismatch_holds_before_runtime(tmp_path: Path) -> None:
    renderer = _load_renderer()
    repo = tmp_path / "repo"
    repo.mkdir()
    actual = _make_repo(repo)
    launcher = tmp_path / "launcher.sh"
    launcher.write_text(
        renderer.render_launcher(
            "0" * 40,
            repo=repo,
            state_dir=tmp_path / "sector",
            factory_state=tmp_path / "factory",
            lock_file=tmp_path / "sector.lock",
        ),
        encoding="utf-8",
    )
    launcher.chmod(0o750)
    result = subprocess.run([str(launcher)], text=True, capture_output=True, check=False)
    assert result.returncode == 75
    assert "HOLD_SOURCE_IDENTITY" in result.stderr
    assert actual in result.stderr


def test_verifier_and_installer_are_fail_closed() -> None:
    verifier = VERIFIER.read_text(encoding="utf-8")
    installer = INSTALLER.read_text(encoding="utf-8")
    assert "STALE_RUNTIME_PREFIX" in verifier
    assert "APPLY=0" in installer
    assert "--apply" in installer
    assert "HOLD_SOURCE_IDENTITY" in installer
    assert "HOLD_DIRTY_SOURCE" in installer
    assert "BACKUP=" in installer
    assert "ROLLBACK=" in installer
    assert "systemctl restart" not in installer
    assert "service restart" not in installer
