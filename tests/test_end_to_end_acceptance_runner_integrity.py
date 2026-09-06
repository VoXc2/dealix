"""Synthetic, offline wrapper tests; these are not VPS or customer acceptance."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import shlex
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/ops/accept_end_to_end_company_v1.sh"
SCRIPTS = (
    "scripts/ops/verify_autonomous_quarantine.py",
    "scripts/ops/verify_end_to_end_company_acceptance_v1.py",
    "scripts/ops/verify_autonomous_company_machine_v2.py",
    "scripts/verify_continuous_company_operations_v1.py",
    "scripts/verify_governed_channel_runtime_v1.py",
    "scripts/verify_commercial_execution_fabric_v2.py",
)
STUB = '''import os
import subprocess
from pathlib import Path
name = Path(__file__).name
with open(os.environ["FIXTURE_TRACE"], "a", encoding="utf-8") as out:
    out.write(name + "\\n")
if name == os.environ.get("FIXTURE_FAIL"):
    raise SystemExit(17)
if name == "pytest.py" and os.environ.get("FIXTURE_MUTATE") == "dirty":
    Path("unexpected.txt").write_text("synthetic mutation", encoding="utf-8")
if name == "pytest.py" and os.environ.get("FIXTURE_MUTATE") == "head":
    subprocess.run(["git", "-c", "commit.gpgsign=false", "commit", "--allow-empty", "-m", "synthetic head move"], check=True, capture_output=True)
print("SYNTHETIC_WRAPPER_FIXTURE_ONLY " + name)
'''


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


@pytest.fixture
def fixture_repo(tmp_path: Path) -> tuple[Path, str, dict[str, str]]:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.name", "Synthetic Fixture")
    git(repo, "config", "user.email", "fixture@example.invalid")
    for rel in SCRIPTS:
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(STUB, encoding="utf-8")
    (repo / "pytest.py").write_text(STUB, encoding="utf-8")
    (repo / "unittest.py").write_text(STUB, encoding="utf-8")
    (repo / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
    shutil.copyfile(RUNNER, repo / "scripts/ops/accept_end_to_end_company_v1.sh")
    git(repo, "add", ".")
    git(repo, "-c", "commit.gpgsign=false", "commit", "-qm", "synthetic fixture")
    env = {k: v for k, v in os.environ.items() if not k.startswith(("DEALIX_", "FIXTURE_", "GIT_"))}
    env.update({
        "DEALIX_AUTOMATION_PYTHON": sys.executable,
        "DEALIX_E2E_PROOF_ROOT": str(tmp_path / "proof"),
        "FIXTURE_TRACE": str(tmp_path / "trace.txt"),
        "TMPDIR": str(tmp_path),
    })
    return repo, git(repo, "rev-parse", "HEAD"), env


def invoke(repo: Path, env: dict[str, str], *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", "scripts/ops/accept_end_to_end_company_v1.sh", *args],
        cwd=repo, env=env, capture_output=True, text=True, check=False, timeout=25,
    )


def proof(env: dict[str, str]) -> dict:
    return json.loads((Path(env["DEALIX_E2E_PROOF_ROOT"]) / "receipt.json").read_text())


def test_all_stages_include_quarantine_and_hash_bound_receipt(fixture_repo) -> None:
    repo, sha, env = fixture_repo
    result = invoke(repo, env, sha)
    assert result.returncode == 0, result.stdout + result.stderr
    receipt = proof(env)
    assert receipt["result"] == "PASS"
    assert receipt["git_sha"] == sha
    assert receipt["acceptance_ceiling"] == "A0_A1_ONLY"
    assert receipt["autonomous_quarantine"] == "PASS"
    assert len(receipt["log_sha256"]) == 8
    assert receipt["deployed_production_verified"] is False
    assert receipt["tenant_isolation_verified"] is False
    path = Path(env["DEALIX_E2E_PROOF_ROOT"])
    digest = hashlib.sha256((path / "receipt.json").read_bytes()).hexdigest()
    assert (path / "receipt.sha256").read_text().startswith(digest)
    assert Path(env["FIXTURE_TRACE"]).read_text().splitlines()[:2] == ["unittest.py", "verify_autonomous_quarantine.py"]
    assert git(repo, "status", "--porcelain") == ""


@pytest.mark.parametrize("failed", [Path(p).name for p in SCRIPTS] + ["pytest.py", "unittest.py"])
def test_any_failed_stage_cannot_leave_pass(fixture_repo, failed: str) -> None:
    repo, sha, env = fixture_repo
    env["FIXTURE_FAIL"] = failed
    result = invoke(repo, env, sha)
    assert result.returncode == 17
    assert proof(env)["result"] == "FAIL"
    assert proof(env)["exit_code"] == 17
    trace = Path(env["FIXTURE_TRACE"]).read_text().splitlines()
    assert trace[-1] == failed


@pytest.mark.parametrize("argument", [None, "main", "0" * 40])
def test_exact_head_is_mandatory(fixture_repo, argument) -> None:
    repo, _, env = fixture_repo
    result = invoke(repo, env, *([] if argument is None else [argument]))
    assert result.returncode != 0
    assert "BLOCKED_" in result.stdout
    assert not Path(env["FIXTURE_TRACE"]).exists()
    assert not Path(env["DEALIX_E2E_PROOF_ROOT"]).exists()


def test_existing_proof_directory_is_never_reused(fixture_repo) -> None:
    repo, sha, env = fixture_repo
    assert invoke(repo, env, sha).returncode == 0
    old = (Path(env["DEALIX_E2E_PROOF_ROOT"]) / "receipt.json").read_bytes()
    env["FIXTURE_FAIL"] = "verify_autonomous_quarantine.py"
    result = invoke(repo, env, sha)
    assert result.returncode != 0
    assert "BLOCKED_PROOF_PATH_EXISTS" in result.stdout
    assert (Path(env["DEALIX_E2E_PROOF_ROOT"]) / "receipt.json").read_bytes() == old


def test_default_runs_get_distinct_receipts(fixture_repo) -> None:
    repo, sha, env = fixture_repo
    env.pop("DEALIX_E2E_PROOF_ROOT")
    first = invoke(repo, env, sha)
    env["FIXTURE_FAIL"] = "verify_autonomous_quarantine.py"
    second = invoke(repo, env, sha)
    paths = [next(line.split("=", 1)[1] for line in r.stdout.splitlines() if line.startswith("proof_root=")) for r in (first, second)]
    assert paths[0] != paths[1]
    assert json.loads((Path(paths[0]) / "receipt.json").read_text())["result"] == "PASS"
    assert json.loads((Path(paths[1]) / "receipt.json").read_text())["result"] == "FAIL"


@pytest.mark.parametrize("mutation", ["dirty", "head"])
def test_post_execution_integrity_is_required(fixture_repo, mutation: str) -> None:
    repo, sha, env = fixture_repo
    env["FIXTURE_MUTATE"] = mutation
    result = invoke(repo, env, sha)
    assert result.returncode != 0
    assert proof(env)["result"] == "FAIL"
    assert proof(env)["last_stage"] == "final_worktree_integrity"


def test_dirty_start_is_blocked(fixture_repo) -> None:
    repo, sha, env = fixture_repo
    (repo / "untracked.txt").write_text("dirty", encoding="utf-8")
    result = invoke(repo, env, sha)
    assert "BLOCKED_DIRTY_WORKTREE" in result.stdout
    assert result.returncode != 0
    assert not Path(env["FIXTURE_TRACE"]).exists()


def test_proof_cannot_pollute_source_tree(fixture_repo) -> None:
    repo, sha, env = fixture_repo
    env["DEALIX_E2E_PROOF_ROOT"] = str(repo / "proof")
    result = invoke(repo, env, sha)
    assert "BLOCKED_PROOF_INSIDE_WORKTREE" in result.stdout
    assert result.returncode != 0
    assert git(repo, "status", "--porcelain") == ""


def test_proof_symlink_is_blocked(fixture_repo) -> None:
    repo, sha, env = fixture_repo
    Path(env["DEALIX_E2E_PROOF_ROOT"]).symlink_to(repo.parent / "missing")
    result = invoke(repo, env, sha)
    assert "BLOCKED_PROOF_PATH_EXISTS" in result.stdout
    assert result.returncode != 0


def test_failed_receipt_writer_cannot_leave_pass(fixture_repo) -> None:
    repo, sha, env = fixture_repo
    interpreter = repo.parent / "receipt-python"
    interpreter.write_text(
        """#!/bin/sh
if [ "${1:-}" = "-" ]; then
  echo '{"result":"PASS"}' > "$2/receipt.json"
  exit 19
fi
""" + "exec " + shlex.quote(sys.executable) + ' "$@"\n',
        encoding="utf-8",
    )
    interpreter.chmod(0o700)
    env["DEALIX_AUTOMATION_PYTHON"] = str(interpreter)
    result = invoke(repo, env, sha)
    assert result.returncode != 0
    assert "FAIL_RECEIPT_WRITE" in result.stdout
    assert not (Path(env["DEALIX_E2E_PROOF_ROOT"]) / "receipt.json").exists()
