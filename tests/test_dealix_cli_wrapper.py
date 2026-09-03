from __future__ import annotations

import os
import subprocess
from pathlib import Path


def _run_verify_wrapper(cli: Path, cwd: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["DEALIX_AUTOMATION_PYTHON"] = "/bin/echo"

    return subprocess.run(
        [str(cli), "verify", "trust", "--sha", "deadbeef"],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )


def _assert_absolute_verifier_dispatch(
    completed: subprocess.CompletedProcess[str], verifier: Path
) -> None:
    assert completed.stdout.strip() == f"{verifier} trust --sha deadbeef"
    assert completed.stderr == ""


def test_dealix_verify_wrapper_is_cwd_independent(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    cli = repo_root / "bin" / "dealix"
    verifier = repo_root / "scripts" / "dealix_verify.py"

    completed = _run_verify_wrapper(cli, tmp_path)

    _assert_absolute_verifier_dispatch(completed, verifier)


def test_dealix_verify_wrapper_resolves_external_relative_symlink(
    tmp_path: Path,
) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    cli = repo_root / "bin" / "dealix"
    verifier = repo_root / "scripts" / "dealix_verify.py"

    link_dir = tmp_path / "path"
    caller_dir = tmp_path / "caller"
    link_dir.mkdir()
    caller_dir.mkdir()

    cli_link = link_dir / "dealix"
    cli_link.symlink_to(os.path.relpath(cli, start=link_dir))

    completed = _run_verify_wrapper(cli_link, caller_dir)

    _assert_absolute_verifier_dispatch(completed, verifier)
