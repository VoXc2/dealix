from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    # dataclasses and postponed annotations expect the defining module to be
    # present in sys.modules while the module body executes.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_secret_scanner_ignores_detector_source_but_flags_literal(tmp_path):
    scanner = load_module("dealix_secret_scan", "scripts/ops/verify_secret_literals.py")

    detector_source = tmp_path / "detector.py"
    detector_source.write_text(
        'PATTERN = r"sk-proj-[A-Za-z0-9_-]{20,}"\n',
        encoding="utf-8",
    )
    assert scanner.scan_file(detector_source) == []

    literal = tmp_path / "candidate.txt"
    literal.write_text("TOKEN=sk-proj-" + "A" * 24 + "\n", encoding="utf-8")
    findings = scanner.scan_file(literal)
    assert findings == [(1, "openai_project_key")]


def test_secret_fixture_allowlist_is_exact_path_detector_and_digest(tmp_path):
    scanner = load_module("dealix_secret_scan_fixture", "scripts/ops/verify_secret_literals.py")

    synthetic = "AKIA" + "0123456789ABCDEF"
    assert scanner.is_allowlisted_fixture(
        "tests/test_v5_layers_pt4.py",
        "aws_access_key",
        synthetic,
    ) is True

    # Same value outside the one exact file remains a finding.
    candidate = tmp_path / "candidate.py"
    candidate.write_text(f"AWS_ACCESS_KEY={synthetic}\n", encoding="utf-8")
    assert scanner.scan_file(candidate, relative_path="tests/another_test.py") == [
        (1, "aws_access_key")
    ]

    # Any value drift in the allowlisted file also remains a finding.
    changed = "AKIA" + "1123456789ABCDEF"
    candidate.write_text(f"AWS_ACCESS_KEY={changed}\n", encoding="utf-8")
    assert scanner.scan_file(
        candidate,
        relative_path="tests/test_v5_layers_pt4.py",
    ) == [(1, "aws_access_key")]


def test_secret_scanner_git_command_uses_exact_process_local_safe_directory(tmp_path):
    scanner = load_module("dealix_secret_scan_git_command", "scripts/ops/verify_secret_literals.py")

    repo = tmp_path / "repo"
    repo.mkdir()
    command = scanner._git_command(repo, "ls-files", "-z")
    resolved = repo.resolve()

    assert command[:3] == ["git", "-c", f"safe.directory={resolved}"]
    assert command[3:5] == ["-C", str(resolved)]
    assert command[5:] == ["ls-files", "-z"]
    assert "safe.directory=*" not in command


def test_secret_scanner_source_has_no_persistent_or_wildcard_trust():
    source = (ROOT / "scripts/ops/verify_secret_literals.py").read_text(encoding="utf-8")
    assert "--global" not in source
    assert "safe.directory=*" not in source


def test_git_metadata_scope_never_walks_worktree(tmp_path):
    guard = load_module("dealix_git_guard", "scripts/ops/git_metadata_permission_guard.py")

    gitdir = tmp_path / ".git"
    (gitdir / "objects" / "aa").mkdir(parents=True)
    (gitdir / "refs" / "remotes").mkdir(parents=True)
    (gitdir / "logs" / "refs").mkdir(parents=True)
    (gitdir / "objects" / "aa" / "object").write_text("x", encoding="utf-8")
    (gitdir / "refs" / "remotes" / "origin").write_text("x", encoding="utf-8")
    (gitdir / "logs" / "refs" / "head").write_text("x", encoding="utf-8")
    (gitdir / "packed-refs").write_text("x", encoding="utf-8")

    worktree_file = tmp_path / "app" / "important.py"
    worktree_file.parent.mkdir()
    worktree_file.write_text("do_not_touch = True\n", encoding="utf-8")

    scoped = {path.resolve() for path, _kind in guard.in_scope_paths(gitdir)}
    assert worktree_file.resolve() not in scoped
    assert all(str(path).startswith(str(gitdir.resolve())) for path in scoped)


def test_git_metadata_git_command_uses_exact_process_local_safe_directory(tmp_path):
    guard = load_module("dealix_git_guard_command", "scripts/ops/git_metadata_permission_guard.py")

    repo = tmp_path / "repo"
    repo.mkdir()
    command = guard._git_command(repo.resolve(), "rev-parse", "--git-common-dir")

    assert command[:3] == ["git", "-c", f"safe.directory={repo.resolve()}"]
    assert command[3:5] == ["-C", str(repo.resolve())]
    assert command[5:] == ["rev-parse", "--git-common-dir"]
    assert "safe.directory=*" not in command


def test_git_metadata_source_has_no_persistent_or_wildcard_trust():
    source = (ROOT / "scripts/ops/git_metadata_permission_guard.py").read_text(encoding="utf-8")
    assert "--global" not in source
    assert "safe.directory=*" not in source


def test_production_trust_acceptance_uses_exact_process_local_safe_directory():
    source = (ROOT / "scripts/ops/accept_production_trust_hardening_v1.sh").read_text(
        encoding="utf-8"
    )
    assert 'git -c "safe.directory=$ROOT" -C "$ROOT" rev-parse HEAD' in source
    assert "safe.directory=*" not in source


def test_verifier_entrypoints_bootstrap_repo_root_before_project_imports():
    self_improvement = (ROOT / "scripts/ops/verify_self_improvement_truth_quarantine.py").read_text(
        encoding="utf-8"
    )
    voice = (ROOT / "scripts/ops/verify_voice_front_desk_realtime_2_1.py").read_text(encoding="utf-8")

    assert self_improvement.index("sys.path.insert") < self_improvement.index("from self_evolving_os import")
    assert voice.index("sys.path.insert") < voice.index("def main()")


def test_selfhost_source_contract_is_canonical():
    verifier = load_module("dealix_selfhost_only", "scripts/ops/verify_selfhost_only_runtime.py")
    assert verifier.ROOT == ROOT
    assert not (ROOT / "railway.json").exists()
    assert not (ROOT / "railway.toml").exists()
    assert (ROOT / "deploy/selfhost/compose.yml").is_file()


def test_selfhost_release_authority_is_source_contract_only():
    authority = json.loads((ROOT / "dealix/config/production_release_authority.json").read_text(encoding="utf-8"))
    assert authority["selfhost_release_target"] == "canonical_vps_only"
    assert authority["github_actions_release_authority"] is False
    assert authority["production_green"] is False
