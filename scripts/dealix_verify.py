#!/usr/bin/env python3
"""Dealix canonical sovereign verification contract.

One deterministic entrypoint reused by humans, OpenCode, systemd adapters and
(optional) CI providers. Verification logic lives here; schedulers and status
reporters are adapters only.

Safety model:
- PR/source modes never run runtime or production checks.
- Runtime and production probes are explicit separate modes.
- Child checks receive a scrubbed environment (no common credential variables).
- Receipts contain metadata and log paths, not captured stdout/stderr.
- External-action operations (merge/deploy/DNS/payment/customer-send) do not
  exist in this program.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import getpass
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROOF_ROOT = ROOT / "reports" / "verification"
PROOF_ROOT = Path(os.getenv("DEALIX_VERIFY_PROOF_ROOT", str(DEFAULT_PROOF_ROOT)))
LOCK_FILE = PROOF_ROOT / ".verify.lock"


def preferred_python(root: Path) -> str:
    candidates = [
        root / ".venv" / "bin" / "python",
        Path("/opt/dealix/workspace/dealix/.venv/bin/python"),
    ]
    for candidate in candidates:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    return sys.executable


PYTHON = preferred_python(ROOT)

# (id, argv, timeout seconds)
SOURCE_CHECKS: list[tuple[str, list[str], int]] = [
    ("env-contract", [PYTHON, "scripts/check_env_contract.py"], 90),
    ("alembic-head", [PYTHON, "scripts/check_alembic_single_head.py"], 90),
    ("security-smoke", [PYTHON, "scripts/security_smoke.py"], 120),
    (
        "landing-guards",
        [PYTHON, "-m", "pytest", "tests/test_landing_forbidden_claims.py", "-q"],
        120,
    ),
]

TEST_CHECKS: list[tuple[str, list[str], int]] = [
    (
        "pytest",
        [PYTHON, "-m", "pytest", "-q", "--disable-warnings", "--maxfail=1"],
        1800,
    ),
]

SECURITY_CHECKS: list[tuple[str, list[str], int]] = [
    ("security-smoke", [PYTHON, "scripts/security_smoke.py"], 120),
]

RUNTIME_CHECKS: list[tuple[str, list[str], int]] = [
    ("boot-acceptance", ["bash", "scripts/ops/boot_acceptance.sh"], 120),
    (
        "ollama-health",
        [
            "curl",
            "-fsS",
            "--max-time",
            "5",
            "http://127.0.0.1:11434/api/tags",
            "-o",
            "/dev/null",
        ],
        15,
    ),
    (
        "n8n-health",
        ["bash", "-c", "docker inspect -f '{{.State.Running}}' dealix-n8n | grep -q true"],
        20,
    ),
    (
        "fleet-state",
        ["bash", "-c", "compgen -G '/opt/dealix/control/state/living_fleet/*.state.json' >/dev/null"],
        20,
    ),
]

PRODUCTION_CHECKS: list[tuple[str, list[str], int]] = [
    (
        "api-health",
        ["curl", "-fsS", "--max-time", "10", "https://api.dealix.me/health", "-o", "/dev/null"],
        20,
    ),
    (
        "root-health",
        ["curl", "-fsS", "--max-time", "10", "https://dealix.me", "-o", "/dev/null"],
        20,
    ),
]

# Commercial verification checks truth and readiness; it must never fabricate a
# lead/revenue state merely to obtain a green result. The first-paid tracker is
# intentionally allowed to report zero paid diagnostics while exiting cleanly.
COMMERCIAL_CHECKS: list[tuple[str, list[str], int]] = [
    (
        "commercial-launch-ready",
        [PYTHON, "scripts/verify_commercial_launch_ready.py"],
        900,
    ),
    (
        "first-paid-truth",
        [PYTHON, "scripts/verify_first_paid_diagnostic_tracker.py", "--json"],
        120,
    ),
]

MODE_GROUPS: dict[str, list[str]] = {
    "changed": ["source"],
    "pr": ["source", "tests"],
    "trust": ["source"],
    "security": ["security"],
    "runtime": ["runtime"],
    "production": ["production"],
    "commercial": ["commercial"],
    "full": ["source", "tests", "runtime", "production", "commercial"],
}

GROUPS = {
    "source": SOURCE_CHECKS,
    "tests": TEST_CHECKS,
    "security": SECURITY_CHECKS,
    "runtime": RUNTIME_CHECKS,
    "production": PRODUCTION_CHECKS,
    "commercial": COMMERCIAL_CHECKS,
}

# Arbitrary/exact-SHA verification must never invoke host runtime or production.
SHA_SAFE_MODES = {"changed", "pr", "trust", "security"}

SECRET_MARKERS = (
    "TOKEN",
    "SECRET",
    "PASSWORD",
    "API_KEY",
    "PRIVATE_KEY",
    "DATABASE_URL",
    "RAILWAY_",
    "TELEGRAM_",
    "OPENAI_",
    "ANTHROPIC_",
    "GITHUB_",
    "GH_TOKEN",
    "MOYASAR_",
)


def utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def resource_snapshot() -> dict[str, float | int | None]:
    load1: float | None = None
    available_mb: int | None = None
    try:
        load1 = os.getloadavg()[0]
    except OSError:
        pass
    try:
        for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
            if line.startswith("MemAvailable:"):
                available_mb = int(line.split()[1]) // 1024
                break
    except OSError:
        pass
    return {"load1": load1, "available_mb": available_mb}


def scrubbed_env() -> dict[str, str]:
    env: dict[str, str] = {}
    for key, value in os.environ.items():
        upper = key.upper()
        if any(marker in upper for marker in SECRET_MARKERS):
            continue
        env[key] = value
    env["APP_ENV"] = "test"
    env["PYTHONNOUSERSITE"] = "1"
    return env


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    encoded = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with tmp.open("wb") as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(tmp, 0o600)
    os.replace(tmp, path)
    try:
        directory_fd = os.open(str(path.parent), os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except OSError:
        pass


def run_check(
    check_id: str,
    argv: list[str],
    timeout: int,
    *,
    cwd: Path,
    log_dir: Path,
) -> dict[str, Any]:
    started = time.monotonic()
    log_path = log_dir / f"{check_id}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run(
            argv,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
            check=False,
            env=scrubbed_env(),
        )
        output = result.stdout or ""
        rc = result.returncode
    except subprocess.TimeoutExpired as exc:
        raw = exc.stdout or ""
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8", errors="replace")
        output = str(raw) + "\nTIMEOUT\n"
        rc = 124
    log_path.write_text(output, encoding="utf-8", errors="replace")
    os.chmod(log_path, 0o600)
    return {
        "id": check_id,
        "status": "PASS" if rc == 0 else "FAIL",
        "exit_code": rc,
        "duration_sec": round(time.monotonic() - started, 3),
        "log_path": str(log_path),
    }


def resolve_sha(root: Path, ref: str) -> str:
    proc = subprocess.run(
        ["git", "rev-parse", "--verify", f"{ref}^{{commit}}"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout.strip()


def create_worktree(root: Path, ref: str) -> tuple[Path, Path, str]:
    expected = resolve_sha(root, ref)
    tmp_root = Path(tempfile.mkdtemp(prefix="dealix-verify-"))
    worktree = tmp_root / "wt"
    subprocess.run(
        ["git", "worktree", "add", "--detach", str(worktree), expected],
        cwd=root,
        check=True,
        capture_output=True,
    )
    actual = resolve_sha(worktree, "HEAD")
    if actual != expected:
        raise RuntimeError(f"worktree SHA mismatch: expected={expected} actual={actual}")
    return tmp_root, worktree, expected


def cleanup_worktree(root: Path, tmp_root: Path | None, worktree: Path | None) -> None:
    if worktree and worktree.exists():
        subprocess.run(
            ["git", "worktree", "remove", "--force", str(worktree)],
            cwd=root,
            check=False,
            capture_output=True,
        )
    subprocess.run(["git", "worktree", "prune"], cwd=root, check=False, capture_output=True)
    if tmp_root:
        shutil.rmtree(tmp_root, ignore_errors=True)


def checks_for_mode(mode: str) -> list[tuple[str, list[str], int]]:
    checks: list[tuple[str, list[str], int]] = []
    seen: set[str] = set()
    for group in MODE_GROUPS[mode]:
        for check in GROUPS[group]:
            if check[0] not in seen:
                checks.append(check)
                seen.add(check[0])
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix canonical sovereign verification")
    parser.add_argument("mode", choices=sorted(MODE_GROUPS))
    parser.add_argument("--sha", help="exact git commit/ref to verify in detached worktree")
    parser.add_argument("--worktree", action="store_true", help="verify origin/main in detached worktree")
    parser.add_argument("--out", type=Path, help="summary receipt path override")
    args = parser.parse_args()

    if (args.sha or args.worktree) and args.mode not in SHA_SAFE_MODES:
        parser.error(
            f"mode {args.mode!r} is host/runtime scoped and cannot run against arbitrary --sha/--worktree; "
            f"use one of {sorted(SHA_SAFE_MODES)}"
        )

    run_id = (
        f"verify-{args.mode}-"
        f"{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-"
        f"{uuid.uuid4().hex[:8]}"
    )
    run_dir = PROOF_ROOT / run_id
    summary_path = args.out or (run_dir / "summary.json")
    log_dir = run_dir / "logs"
    started_at = utcnow()
    wall_start = time.monotonic()
    before = resource_snapshot()

    min_available_mb = int(os.getenv("DEALIX_VERIFY_MIN_AVAILABLE_MB", "800"))
    available = before.get("available_mb")
    if isinstance(available, int) and available < min_available_mb:
        receipt = {
            "schema_version": "dealix.verify.v2",
            "run_id": run_id,
            "started_at": started_at,
            "finished_at": utcnow(),
            "mode": args.mode,
            "git_sha": resolve_sha(ROOT, "HEAD"),
            "host": platform.node(),
            "user": getpass.getuser(),
            "verdict": "BLOCKED_EXPECTED",
            "reason": f"resource_guard available_mb={available} < {min_available_mb}",
            "checks": [],
            "failed_checks": [],
            "blocked_expected": ["resource_guard"],
            "skipped_checks": [],
            "duration_seconds": round(time.monotonic() - wall_start, 3),
            "resource_summary": before,
        }
        atomic_json(summary_path, receipt)
        print(f"[BLOCKED_EXPECTED] resource_guard available_mb={available}")
        print(f"Receipt: {summary_path}")
        return 2

    PROOF_ROOT.mkdir(parents=True, exist_ok=True)
    lock_handle = LOCK_FILE.open("a+")
    tmp_root: Path | None = None
    worktree: Path | None = None
    effective_root = ROOT
    verified_sha = resolve_sha(ROOT, "HEAD")

    try:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        if args.sha or args.worktree:
            ref = args.sha or "origin/main"
            tmp_root, worktree, verified_sha = create_worktree(ROOT, ref)
            effective_root = worktree

        # Recompute interpreter from the target tree when a local .venv exists.
        global PYTHON
        PYTHON = preferred_python(effective_root)

        results: list[dict[str, Any]] = []
        for check_id, argv, timeout in checks_for_mode(args.mode):
            # Replace any pre-resolved Python executable with the target-runtime Python.
            resolved_argv = [
                PYTHON if item == sys.executable or item.endswith("/.venv/bin/python") else item
                for item in argv
            ]
            result = run_check(check_id, resolved_argv, timeout, cwd=effective_root, log_dir=log_dir)
            results.append(result)
            print(f"[{result['status']}] {check_id} ({result['duration_sec']}s)")
            if result["status"] == "FAIL" and os.getenv("DEALIX_VERIFY_FAIL_FAST", "1") == "1":
                break

        failed = [item for item in results if item["status"] == "FAIL"]
        verdict = "FAIL" if failed else "PASS"
        receipt = {
            "schema_version": "dealix.verify.v2",
            "run_id": run_id,
            "started_at": started_at,
            "finished_at": utcnow(),
            "git_sha": verified_sha,
            "ref": args.sha or ("origin/main" if args.worktree else "HEAD"),
            "mode": args.mode,
            "host": platform.node(),
            "user": getpass.getuser(),
            "verdict": verdict,
            "checks": results,
            "failed_checks": [item["id"] for item in failed],
            "blocked_expected": [],
            "skipped_checks": [],
            "duration_seconds": round(time.monotonic() - wall_start, 3),
            "resource_summary": before,
            "tool_versions": {"python": platform.python_version()},
        }
        atomic_json(summary_path, receipt)
        print(f"Receipt: {summary_path}")
        print(f"Status: {verdict} ({len(failed)} failed, {len(results)} executed)")
        return 0 if verdict == "PASS" else 1
    finally:
        cleanup_worktree(ROOT, tmp_root, worktree)
        try:
            lock_handle.close()
        except OSError:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
