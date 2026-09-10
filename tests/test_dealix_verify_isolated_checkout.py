from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY_SCRIPT = ROOT / "scripts" / "dealix_verify.py"


def _load_verify_module():
    spec = importlib.util.spec_from_file_location("dealix_verify_under_test", VERIFY_SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return proc.stdout.strip()


def test_isolated_checkout_does_not_register_source_worktree(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    _git(source, "init", "-q")
    _git(source, "config", "user.email", "test@dealix.local")
    _git(source, "config", "user.name", "Dealix Test")
    (source / "probe.txt").write_text("exact\n", encoding="utf-8")
    _git(source, "add", "probe.txt")
    _git(source, "commit", "-qm", "probe")
    expected = _git(source, "rev-parse", "HEAD")

    module = _load_verify_module()
    tmp_root, checkout, actual = module.create_worktree(source, "HEAD")
    try:
        assert actual == expected
        assert _git(checkout, "rev-parse", "HEAD") == expected
        assert _git(checkout, "status", "--porcelain") == ""
        assert not (source / ".git" / "worktrees").exists()
        assert (checkout / ".git").is_dir()
    finally:
        module.cleanup_worktree(source, tmp_root, checkout)

    assert not tmp_root.exists()


def test_verifier_source_avoids_canonical_worktree_mutation() -> None:
    text = VERIFY_SCRIPT.read_text(encoding="utf-8")
    assert '"clone"' in text
    assert '"--local"' in text
    assert '"--no-hardlinks"' in text
    assert '"--no-checkout"' in text
    assert '"worktree", "add"' not in text
    assert '"worktree", "prune"' not in text
