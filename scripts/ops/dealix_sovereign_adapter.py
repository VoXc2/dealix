#!/usr/bin/env python3
"""Dealix sovereign VPS execution adapter.

Verification policy lives only in ``bin/dealix verify`` / ``scripts/dealix_verify.py``.
This adapter owns scheduling, exact-ref fetch, trusted-PR eligibility, resource
protection, receipt routing and bounded GitHub commit statuses.

v1 security boundary: trusted same-repository PRs only. Fork/untrusted execution
remains blocked until Issue #1266 proves stronger identity/process isolation.

This module has no merge, deploy, DNS, DB, secrets, payment, publish or customer-
send operation.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_SLUG = os.getenv("DEALIX_REPO_SLUG", "Dealix-sa/dealix")
STATE_ROOT = Path(os.getenv("DEALIX_SOVEREIGN_CI_ROOT", "/opt/dealix/sovereign-ci"))
TOOL_REPO = STATE_ROOT / "tool-repo"
RUNNER_HOME = STATE_ROOT / "runner-home"
RECEIPTS = STATE_ROOT / "receipts"
ADAPTER_LOGS = STATE_ROOT / "adapter-logs"
STATE_FILE = STATE_ROOT / "state.json"
LOCK_FILE = STATE_ROOT / ".adapter.lock"
TOOL_REF = os.getenv("DEALIX_SOVEREIGN_TOOL_REF", "main")
MAX_PRS_PER_POLL = int(os.getenv("DEALIX_CI_MAX_PRS_PER_POLL", "2"))
MIN_AVAILABLE_MB = int(os.getenv("DEALIX_CI_MIN_AVAILABLE_MB", "4096"))
MAX_LOAD1 = float(os.getenv("DEALIX_CI_MAX_LOAD1", "2.75"))
TRUSTED_ASSOCIATIONS = {"OWNER", "MEMBER", "COLLABORATOR"}

STATUS_SOURCE = "dealix/sovereign-source"
STATUS_PR = "dealix/sovereign-pr"
STATUS_RUNTIME = "dealix/sovereign-runtime"
STATUS_PRODUCTION = "dealix/sovereign-production"
STATUS_COMMERCIAL = "dealix/sovereign-commercial"


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def ensure_dirs() -> None:
    for path in (STATE_ROOT, RUNNER_HOME, RECEIPTS, ADAPTER_LOGS):
        path.mkdir(parents=True, exist_ok=True)
        try:
            path.chmod(0o700)
        except OSError:
            pass


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


def load_state() -> dict[str, Any]:
    default = {"main_sha": None, "prs": {}, "last_poll_at": None}
    if not STATE_FILE.exists():
        return default
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else default
    except (OSError, json.JSONDecodeError):
        return default


def run(
    argv: list[str],
    *,
    cwd: Path | None = None,
    timeout: int = 120,
    env: dict[str, str] | None = None,
    log_name: str | None = None,
) -> subprocess.CompletedProcess[str]:
    started = time.monotonic()
    try:
        proc = subprocess.run(
            argv,
            cwd=str(cwd) if cwd else None,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
            env=env,
        )
    except subprocess.TimeoutExpired as exc:
        raw = exc.stdout or ""
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8", errors="replace")
        proc = subprocess.CompletedProcess(argv, 124, str(raw) + "\nTIMEOUT\n", None)
    setattr(proc, "dealix_duration_s", round(time.monotonic() - started, 3))
    if log_name:
        path = ADAPTER_LOGS / log_name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(proc.stdout or "", encoding="utf-8", errors="replace")
        os.chmod(path, 0o600)
    return proc


def gh_api(endpoint: str, *, method: str = "GET", fields: dict[str, str] | None = None) -> Any:
    argv = ["gh", "api"]
    if method != "GET":
        argv += ["-X", method]
    argv.append(endpoint)
    if fields:
        for key, value in fields.items():
            argv += ["-f", f"{key}={value}"]
    proc = run(argv, timeout=90, env=os.environ.copy())
    if proc.returncode != 0:
        raise RuntimeError(f"GitHub API failed: endpoint={endpoint} rc={proc.returncode}")
    text = (proc.stdout or "").strip()
    return json.loads(text) if text else None


def post_status(sha: str, state: str, context: str, description: str) -> None:
    try:
        gh_api(
            f"repos/{REPO_SLUG}/statuses/{sha}",
            method="POST",
            fields={"state": state, "context": context, "description": description[:140]},
        )
    except Exception as exc:
        print(f"STATUS_SYNC=DEFERRED type={type(exc).__name__}")


def resource_snapshot() -> tuple[float, int]:
    try:
        load1 = float(Path("/proc/loadavg").read_text(encoding="utf-8").split()[0])
    except Exception:
        load1 = 0.0
    available_mb = 0
    try:
        for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
            if line.startswith("MemAvailable:"):
                available_mb = int(line.split()[1]) // 1024
                break
    except Exception:
        pass
    return load1, available_mb


def resources_ok() -> tuple[bool, str]:
    load1, available_mb = resource_snapshot()
    if load1 > MAX_LOAD1:
        return False, f"load1={load1:.2f}>{MAX_LOAD1:.2f}"
    if available_mb and available_mb < MIN_AVAILABLE_MB:
        return False, f"available_mb={available_mb}<{MIN_AVAILABLE_MB}"
    return True, "ok"


def ensure_tool_repo() -> None:
    if (TOOL_REPO / ".git").exists():
        return
    if TOOL_REPO.exists():
        shutil.rmtree(TOOL_REPO)
    proc = run(
        ["gh", "repo", "clone", REPO_SLUG, str(TOOL_REPO)],
        timeout=600,
        env=os.environ.copy(),
        log_name="clone-tool-repo.log",
    )
    if proc.returncode != 0:
        raise RuntimeError("failed to clone tooling repository")


def refresh_tool_repo() -> str:
    ensure_tool_repo()
    fetch = run(
        ["git", "fetch", "--no-tags", "origin", f"+refs/heads/{TOOL_REF}:refs/remotes/origin/{TOOL_REF}"],
        cwd=TOOL_REPO,
        timeout=300,
        env=os.environ.copy(),
        log_name="fetch-tool-ref.log",
    )
    if fetch.returncode != 0:
        raise RuntimeError(f"failed to fetch tool ref {TOOL_REF}")
    checkout = run(
        ["git", "checkout", "--detach", f"refs/remotes/origin/{TOOL_REF}"],
        cwd=TOOL_REPO,
        timeout=120,
        env=os.environ.copy(),
        log_name="checkout-tool-ref.log",
    )
    if checkout.returncode != 0:
        raise RuntimeError(f"failed to checkout tool ref {TOOL_REF}")
    rev = run(["git", "rev-parse", "HEAD"], cwd=TOOL_REPO, timeout=30, env=os.environ.copy())
    sha = (rev.stdout or "").strip()
    if rev.returncode != 0 or not sha:
        raise RuntimeError("failed to resolve tool ref SHA")
    if not (TOOL_REPO / "bin" / "dealix").is_file():
        raise RuntimeError("canonical verifier missing: bin/dealix")
    return sha


def fetch_main() -> str:
    proc = run(
        ["git", "fetch", "--no-tags", "origin", "+refs/heads/main:refs/remotes/origin/main"],
        cwd=TOOL_REPO,
        timeout=300,
        env=os.environ.copy(),
        log_name="fetch-main.log",
    )
    if proc.returncode != 0:
        raise RuntimeError("fetch main failed")
    rev = run(["git", "rev-parse", "refs/remotes/origin/main"], cwd=TOOL_REPO, timeout=30, env=os.environ.copy())
    if rev.returncode != 0:
        raise RuntimeError("resolve main failed")
    return (rev.stdout or "").strip()


def fetch_pr(pr_number: int) -> str:
    ref = f"refs/dealix/sovereign/pr/{pr_number}"
    proc = run(
        ["git", "fetch", "--no-tags", "origin", f"+refs/pull/{pr_number}/head:{ref}"],
        cwd=TOOL_REPO,
        timeout=300,
        env=os.environ.copy(),
        log_name=f"fetch-pr-{pr_number}.log",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"fetch PR #{pr_number} failed")
    rev = run(["git", "rev-parse", ref], cwd=TOOL_REPO, timeout=30, env=os.environ.copy())
    if rev.returncode != 0:
        raise RuntimeError(f"resolve PR #{pr_number} failed")
    return (rev.stdout or "").strip()


def get_pr(pr_number: int) -> dict[str, Any]:
    data = gh_api(f"repos/{REPO_SLUG}/pulls/{pr_number}")
    if not isinstance(data, dict):
        raise RuntimeError(f"invalid PR payload for #{pr_number}")
    return data


def list_open_prs() -> list[dict[str, Any]]:
    data = gh_api(f"repos/{REPO_SLUG}/pulls?state=open&sort=updated&direction=desc&per_page=100")
    return data if isinstance(data, list) else []


def trusted_pr(pr: dict[str, Any]) -> bool:
    head_repo = (((pr.get("head") or {}).get("repo") or {}).get("full_name"))
    association = str(pr.get("author_association") or "").upper()
    return head_repo == REPO_SLUG and association in TRUSTED_ASSOCIATIONS


def runner_env() -> dict[str, str]:
    """Minimal child environment; no inherited credential variables or real HOME."""
    path = os.environ.get("PATH", "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin")
    return {
        "PATH": path,
        "LANG": os.environ.get("LANG", "C.UTF-8"),
        "LC_ALL": os.environ.get("LC_ALL", "C.UTF-8"),
        "HOME": str(RUNNER_HOME),
        "XDG_CONFIG_HOME": str(RUNNER_HOME / ".config"),
        "XDG_CACHE_HOME": str(STATE_ROOT / "runner-cache"),
        "NPM_CONFIG_CACHE": str(STATE_ROOT / "npm-cache"),
        "DEALIX_VERIFY_PROOF_ROOT": str(RECEIPTS),
        "DEALIX_VERIFY_MIN_AVAILABLE_MB": str(MIN_AVAILABLE_MB),
        "PYTHONNOUSERSITE": "1",
    }


def invoke_verify(mode: str, *, sha: str | None = None, receipt_name: str) -> tuple[str, Path, int]:
    okay, reason = resources_ok()
    receipt = RECEIPTS / receipt_name
    if not okay:
        atomic_json(
            receipt,
            {
                "schema_version": "dealix.sovereign-adapter.v1",
                "started_at": utcnow(),
                "finished_at": utcnow(),
                "mode": mode,
                "git_sha": sha,
                "verdict": "BLOCKED_EXPECTED",
                "blocked_expected": [reason],
                "checks": [],
            },
        )
        return "BLOCKED_EXPECTED", receipt, 2

    argv = ["bin/dealix", "verify", mode]
    if sha:
        argv += ["--sha", sha]
    argv += ["--out", str(receipt)]
    proc = run(
        argv,
        cwd=TOOL_REPO,
        timeout=2400,
        env=runner_env(),
        log_name=f"verify-{receipt_name}.log",
    )
    if not receipt.exists():
        return "ERROR", receipt, proc.returncode
    try:
        data = json.loads(receipt.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "ERROR", receipt, proc.returncode
    verdict = str(data.get("verdict") or data.get("status") or "ERROR").upper()
    if not str(data.get("schema_version", "")).startswith("dealix.verify."):
        return "ERROR", receipt, proc.returncode
    if sha and data.get("git_sha") != sha:
        return "ERROR", receipt, proc.returncode
    return verdict, receipt, proc.returncode


def github_state(verdict: str) -> str:
    if verdict == "PASS":
        return "success"
    if verdict == "FAIL":
        return "failure"
    if verdict == "BLOCKED_EXPECTED":
        return "pending"
    return "error"


def verify_main_source(main_sha: str) -> str:
    post_status(main_sha, "pending", STATUS_SOURCE, "Sovereign source verification running")
    verdict, receipt, _ = invoke_verify(
        "trust",
        sha=main_sha,
        receipt_name=f"{run_tag()}-main-{main_sha[:12]}-source.json",
    )
    post_status(main_sha, github_state(verdict), STATUS_SOURCE, f"Sovereign source: {verdict}")
    print(f"MAIN_SOURCE={verdict} SHA={main_sha} RECEIPT={receipt}")
    return verdict


def verify_pr_sha(pr_number: int, sha: str) -> str:
    post_status(sha, "pending", STATUS_PR, f"Sovereign PR #{pr_number} running")
    verdict, receipt, _ = invoke_verify(
        "pr",
        sha=sha,
        receipt_name=f"{run_tag()}-pr-{pr_number}-{sha[:12]}.json",
    )
    post_status(sha, github_state(verdict), STATUS_PR, f"Sovereign PR #{pr_number}: {verdict}")
    print(f"PR={pr_number} SHA={sha} VERDICT={verdict} RECEIPT={receipt}")
    return verdict


def manual_verify_pr(pr_number: int) -> int:
    tool_sha = refresh_tool_repo()
    pr = get_pr(pr_number)
    if str(pr.get("state") or "") != "open":
        print(f"VERIFY_PR=BLOCKED_CLOSED pr={pr_number}")
        return 3
    if not trusted_pr(pr):
        print(f"VERIFY_PR=BLOCKED_UNTRUSTED pr={pr_number}")
        return 3
    api_sha = str((pr.get("head") or {}).get("sha") or "")
    fetched_sha = fetch_pr(pr_number)
    if not api_sha or api_sha != fetched_sha:
        print(f"VERIFY_PR=HEAD_RACE pr={pr_number} api={api_sha} fetched={fetched_sha}")
        return 4
    print(f"TOOL_REF={TOOL_REF} TOOL_SHA={tool_sha}")
    verdict = verify_pr_sha(pr_number, fetched_sha)
    return 0 if verdict in {"PASS", "BLOCKED_EXPECTED"} else 1


def manual_verify_main() -> int:
    tool_sha = refresh_tool_repo()
    main_sha = fetch_main()
    print(f"TOOL_REF={TOOL_REF} TOOL_SHA={tool_sha}")
    verdict = verify_main_source(main_sha)
    return 0 if verdict in {"PASS", "BLOCKED_EXPECTED"} else 1


def poll() -> int:
    tool_sha = refresh_tool_repo()
    state = load_state()
    print(f"TOOL_REF={TOOL_REF} TOOL_SHA={tool_sha}")

    main_sha = fetch_main()
    if state.get("main_sha") != main_sha:
        verdict = verify_main_source(main_sha)
        if verdict not in {"BLOCKED_EXPECTED", "ERROR"}:
            state["main_sha"] = main_sha

    previous_prs = {str(k): str(v) for k, v in (state.get("prs") or {}).items()}
    current: dict[str, str] = {}
    candidates: list[tuple[int, str]] = []
    untrusted = 0
    for pr in list_open_prs():
        number = int(pr["number"])
        key = str(number)
        sha = str((pr.get("head") or {}).get("sha") or "")
        if not sha:
            continue
        current[key] = sha
        if not trusted_pr(pr):
            untrusted += 1
            continue
        if previous_prs.get(key) != sha:
            candidates.append((number, sha))

    processed: set[str] = set()
    for number, api_sha in candidates[:MAX_PRS_PER_POLL]:
        fetched_sha = fetch_pr(number)
        if fetched_sha != api_sha:
            print(f"PR_HEAD_RACE=#{number} api={api_sha} fetched={fetched_sha}")
            continue
        verdict = verify_pr_sha(number, fetched_sha)
        if verdict not in {"BLOCKED_EXPECTED", "ERROR"}:
            processed.add(str(number))
            previous_prs[str(number)] = api_sha

    state["prs"] = {key: value for key, value in previous_prs.items() if key in current}
    state["last_poll_at"] = utcnow()
    atomic_json(STATE_FILE, state)
    print(
        f"OPEN_PRS={len(current)} CANDIDATES={len(candidates)} "
        f"PROCESSED={len(processed)} UNTRUSTED_SKIPPED={untrusted}"
    )
    return 0


def trusted_cycle() -> int:
    tool_sha = refresh_tool_repo()
    main_sha = fetch_main()
    print(f"TRUSTED_TOOL_SHA={tool_sha} MAIN_SHA={main_sha}")
    overall = 0
    for mode, context in (
        ("runtime", STATUS_RUNTIME),
        ("production", STATUS_PRODUCTION),
        ("commercial", STATUS_COMMERCIAL),
    ):
        post_status(main_sha, "pending", context, f"Sovereign {mode} verification running")
        verdict, receipt, _ = invoke_verify(
            mode,
            receipt_name=f"{run_tag()}-trusted-{mode}-{main_sha[:12]}.json",
        )
        post_status(main_sha, github_state(verdict), context, f"Sovereign {mode}: {verdict}")
        print(f"TRUSTED_MODE={mode} VERDICT={verdict} RECEIPT={receipt}")
        if verdict in {"FAIL", "ERROR"}:
            overall = 1
    return overall


def doctor() -> int:
    ensure_dirs()
    checks = {
        "git": shutil.which("git") is not None,
        "gh": shutil.which("gh") is not None,
        "python": bool(sys.executable),
        "state_root": STATE_ROOT.exists(),
    }
    try:
        gh_api(f"repos/{REPO_SLUG}")
        checks["github_api"] = True
    except Exception:
        checks["github_api"] = False
    load1, available_mb = resource_snapshot()
    print(f"REPO={REPO_SLUG}")
    print(f"STATE_ROOT={STATE_ROOT}")
    print(f"TOOL_REPO={TOOL_REPO}")
    print(f"TOOL_REF={TOOL_REF}")
    print(f"LOAD1={load1:.2f} AVAILABLE_MB={available_mb}")
    for key, value in checks.items():
        print(f"{key}={'PASS' if value else 'FAIL'}")
    return 0 if all(checks.values()) else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dealix sovereign VPS adapter")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("poll")
    sub.add_parser("verify-main")
    p_verify = sub.add_parser("verify-pr")
    p_verify.add_argument("pr", type=int)
    sub.add_parser("trusted-cycle")
    sub.add_parser("doctor")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_dirs()
    with LOCK_FILE.open("a+") as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("ADAPTER=SKIP_OVERLAP")
            return 0
        if args.command == "poll":
            return poll()
        if args.command == "verify-main":
            return manual_verify_main()
        if args.command == "verify-pr":
            return manual_verify_pr(args.pr)
        if args.command == "trusted-cycle":
            return trusted_cycle()
        if args.command == "doctor":
            return doctor()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
