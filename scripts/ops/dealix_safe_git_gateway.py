#!/usr/bin/env python3
"""DEALIX SAFE GIT GATEWAY — bounded source-integration autonomy (no force, no bypass).

Ordinary SAFE SOURCE changes (feature push, draft->ready, head-pinned merge,
superseded-close) go through exact gates here instead of raw dangerous commands:

* feature-push : branch!=main, no force, remote==origin, secret scan, then push.
* pr-ready     : full verify bundle on the EXACT PR head, then `gh pr ready`.
* pr-merge     : all merge gates (§10 A-O) on the EXACT head incl. affected
                 tests in an isolated worktree, then head-pinned
                 `gh pr merge --merge --match-head-commit SHA`. Any head move
                 aborts; re-verify, never force.
* pr-close     : only with --superseded-by N where N is MERGED.
* reconcile    : main HEAD + open-PR table for post-merge recalculation.
* status       : repo/remote/auth presence summary (no secrets).

Exit codes: 0 = executed/verified PASS; 2 = gate-blocked (GATE= reason);
1 = operational error. --dry-run runs every gate except the final mutation.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
EXPECTED_REMOTE = "https://github.com/Dealix-sa/dealix.git"
PROTECTED_BRANCHES = {"main", "master", "production"}
SCHEMA = "dealix.safe-git-gateway.v1"

SECRET_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|client[_-]?secret|access[_-]?token)\s*[:=]\s*['\"][^'\"]{8,}"),
    re.compile(r"(?i)(password|passwd|pwd)\s*[:=]\s*['\"][^'\"]{6,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\b(ghp|gho|github_pat)_[A-Za-z0-9_]{10,}"),
    re.compile(r"\bsk-(live|test)-[A-Za-z0-9]{8,}"),
    re.compile(r"\bxox[bap]-"),
)

# changed-path prefix -> verification bundle (run in exact-head worktree).
TEST_BUNDLES: list[tuple[str, list[list[str]]]] = [
    ("scripts/ops/", [["-m", "pytest", "tests/test_go_resource_broker.py",
                       "tests/test_model_cost_firewall.py",
                       "tests/test_opencode_model_broker.py",
                       "tests/test_opencode_go_provider_overage_guard.py",
                       "tests/test_session_factory.py",
                       "-q", "--no-cov", "-p", "no:cacheprovider"]]),
    ("dealix/commercial/universal_diagnostic_factory.py", [["-m", "pytest",
                       "tests/test_universal_diagnostic_bilingual_v2.py",
                       "tests/test_diagnostic_free_governance.py",
                       "tests/test_diagnostic_router.py",
                       "tests/test_commercial_diagnostic_evidence_bound.py",
                       "-q", "--no-cov", "-p", "no:cacheprovider"]]),
]

FRONTEND_TYPECHECK = ["npm", "run", "typecheck", "--prefix", "frontend"]
FRONTEND_BUILD = ["npm", "run", "build", "--prefix", "frontend"]
GATE_TIMEOUT_S = 600


def _run(cmd: list[str], cwd: Path | None = None, timeout: int = 120,
         env: dict | None = None) -> tuple[int, str]:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                              check=False, cwd=str(cwd) if cwd else None,
                              env=env)
        return proc.returncode, (proc.stdout + proc.stderr)[-6000:]
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 124, f"EXEC_FAIL: {type(exc).__name__}: {exc}"


def _gh(args: list[str], timeout: int = 60) -> tuple[int, str]:
    gh = shutil.which("gh")
    if not gh:
        return 127, "gh CLI not found"
    return _run([gh, *args], cwd=REPO_ROOT, timeout=timeout)


def _git(args: list[str], cwd: Path = REPO_ROOT, timeout: int = 120) -> tuple[int, str]:
    return _run(["git", *args], cwd=cwd, timeout=timeout)


def _gate(gates: list, name: str, ok: bool, detail: str = "") -> dict | None:
    gates.append({"gate": name, "pass": ok, "detail": detail[:300]})
    if not ok:
        return {"verdict": "BLOCKED", "blocked_by": name, "detail": detail[:500],
                "gates": gates}
    return None


def repo_preflight(gates: list) -> dict | None:
    rc, top = _git(["rev-parse", "--show-toplevel"])
    if rc != 0 or Path(top.strip()) != REPO_ROOT:
        return _gate(gates, "canonical_repo", False, f"toplevel={top.strip()}")
    _gate(gates, "canonical_repo", True, str(REPO_ROOT))
    rc, url = _git(["config", "--get", "remote.origin.url"])
    if rc != 0 or url.strip() != EXPECTED_REMOTE:
        return _gate(gates, "expected_origin", False, f"url={url.strip()[:80]}")
    _gate(gates, "expected_origin", True, "origin matches")
    return None


def origin_main_sha() -> str:
    rc, out = _git(["ls-remote", "origin", "refs/heads/main"])
    if rc != 0 or not out.strip():
        return "UNKNOWN"
    return out.split()[0]


def pr_facts(number: int) -> dict:
    rc, out = _gh(["pr", "view", str(number), "--json",
                   "number,title,headRefOid,headRefName,baseRefName,isDraft,"
                   "mergeable,mergeStateStatus,state"])
    if rc != 0:
        return {"error": out[-300:]}
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {"error": "unparsable gh output"}


def pr_files(number: int) -> list[str]:
    rc, out = _gh(["api", f"repos/Dealix-sa/dealix/pulls/{number}/files",
                   "--paginate", "--jq", ".[].filename"])
    if rc != 0:
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]


def pr_diff(number: int) -> str:
    rc, out = _gh(["pr", "diff", str(number)])
    return out if rc == 0 else ""


def secret_scan(diff: str) -> list[str]:
    hits = []
    for i, line in enumerate(diff.splitlines()):
        if not line.startswith("+") or line.startswith("+++"):
            continue
        for pat in SECRET_PATTERNS:
            if pat.search(line):
                hits.append(f"line+{i}:{line[:90]}")
                break
    return hits[:10]


def whitespace_check(diff: str) -> tuple[bool, str]:
    """git diff --check semantics on added lines (gh pr diff is not always
    git-apply-parseable, so enforce the core rules directly)."""
    if not diff.strip():
        return False, "empty diff"
    errors = []
    for i, line in enumerate(diff.splitlines()):
        if not line.startswith("+") or line.startswith("+++"):
            continue
        body = line[1:]
        if body != body.rstrip():
            errors.append(f"line+{i}: trailing whitespace")
        if re.match(r"^ +\t", body):
            errors.append(f"line+{i}: space before tab")
        if len(errors) >= 5:
            break
    if errors:
        return False, "; ".join(errors)
    return True, "clean"


def verify_head_worktree(head_sha: str, files: list[str], repo: Path,
                         timeout_each: int = GATE_TIMEOUT_S) -> tuple[bool, list[dict]]:
    """Create exact-head isolated worktree, run surface-mapped bundles. Returns
    (ok, evidence). Worktree is always removed."""
    results: list[dict] = []
    tmpdir = Path(tempfile.mkdtemp(prefix="dealix-gw-verify-"))
    wt = tmpdir / "wt"
    try:
        rc, out = _run(["git", "worktree", "add", "--detach", str(wt), head_sha],
                       cwd=repo, timeout=180)
        if rc != 0:
            return False, [{"step": "worktree", "pass": False, "detail": out[-300:]}]
        results.append({"step": "worktree", "pass": True, "detail": f"head={head_sha[:8]}"})
        env = dict(os.environ, PYTHONPATH=str(wt))
        venv_py = repo / ".venv" / "bin" / "python"
        env_venv = os.environ.get("DEALIX_VENV")
        if venv_py.is_file():
            py = [str(venv_py)]
        elif env_venv and Path(env_venv).is_file():
            py = [env_venv]
        else:
            py = [sys.executable]
        results.append({"step": "interpreter", "pass": True, "detail": py[0][-40:]})
        cmds: list[list[str]] = []
        for prefix, bundle in TEST_BUNDLES:
            if any(f == prefix or f.startswith(prefix) for f in files):
                cmds.extend([py + c for c in bundle])
        if any(f.startswith("frontend/") for f in files):
            node_mods = repo / "frontend" / "node_modules"
            if (node_mods).is_dir():
                link = wt / "frontend" / "node_modules"
                try:
                    if not link.exists():
                        link.symlink_to(node_mods, target_is_directory=True)
                except OSError as exc:
                    return False, results + [{"step": "node_modules",
                                              "pass": False, "detail": str(exc)[:200]}]
                results.append({"step": "node_modules", "pass": True,
                                "detail": "symlinked from invoking repo"})
            else:
                return False, results + [{"step": "node_modules", "pass": False,
                                          "detail": "frontend/node_modules absent"}]
            cmds.append(FRONTEND_TYPECHECK)
            cmds.append(FRONTEND_BUILD)
        if any(f.startswith("tests/playwright/") and f.endswith(".js") for f in files):
            for f in files:
                if f.startswith("tests/playwright/") and f.endswith(".js"):
                    rc, out = _run(["node", "--check", str(wt / f)], timeout=60)
                    results.append({"step": f"node-check:{f}", "pass": rc == 0,
                                    "detail": out[-200:]})
                    if rc != 0:
                        return False, results
        test_files = [f for f in files if f.startswith("tests/") and f.endswith(".py")]
        if test_files and not cmds:
            cmds.append(py + ["-m", "pytest", *test_files, "-q", "--no-cov",
                              "-p", "no:cacheprovider"])
        if not cmds:
            results.append({"step": "tests", "pass": True,
                            "detail": "docs/config-only surface; structural gates suffice"})
            return True, results
        for cmd in cmds:
            rc, out = _run(cmd, cwd=wt, timeout=timeout_each, env=env)
            step = " ".join(cmd[-3:] if cmd[0] == "npm" else cmd[1:4])
            results.append({"step": step, "pass": rc == 0, "detail": out[-400:]})
            if rc != 0:
                return False, results
        return True, results
    finally:
        _run(["git", "worktree", "remove", "--force", str(wt)], cwd=repo, timeout=120)
        _run(["git", "worktree", "prune"], cwd=repo, timeout=60)
        shutil.rmtree(tmpdir, ignore_errors=True)


def cmd_status(args) -> dict:
    gates: list = []
    blocked = repo_preflight(gates)
    if blocked:
        return blocked
    rc, auth = _gh(["auth", "status"])
    _gate(gates, "github_auth", rc == 0, auth.strip().splitlines()[0][:120] if auth else "")
    main_sha = origin_main_sha()
    _gate(gates, "origin_main_resolves", main_sha != "UNKNOWN", main_sha[:12])
    fails = [g for g in gates if not g["pass"]]
    return {"schema": SCHEMA, "command": "status",
            "verdict": "BLOCKED" if fails else "PASS",
            "origin_main": main_sha, "gates": gates}


def cmd_feature_push(args) -> dict:
    gates: list = []
    blocked = repo_preflight(gates)
    if blocked:
        return blocked
    branch = args.branch
    if branch in PROTECTED_BRANCHES:
        return _gate(gates, "unprotected_branch", False, f"branch={branch}") or {}
    if args.force:
        blocked = _gate(gates, "no_force", False, "--force refused")
        if blocked:
            return blocked
    rc, cur = _git(["branch", "--show-current"])
    _gate(gates, "branch_known", rc == 0, cur.strip())
    rc, ahead = _git(["rev-list", "--count", f"origin/{branch}..{branch}"])
    if rc != 0 or not ahead.strip().isdigit() or int(ahead.strip()) < 1:
        blocked = _gate(gates, "commit_exists", False, "nothing to push")
        if blocked:
            return blocked
    _gate(gates, "commit_exists", True, f"ahead={ahead.strip()}")
    rc, full_diff = _git(["diff", f"origin/{branch}...{branch}"])
    hits = secret_scan(full_diff)
    blocked = _gate(gates, "secret_scan", not hits, f"hits={len(hits)}")
    if blocked:
        return blocked
    if args.dry_run:
        return {"schema": SCHEMA, "command": "feature-push", "verdict": "DRY_RUN_PASS",
                "branch": branch, "gates": gates}
    rc, out = _git(["push", "origin", branch], timeout=300)
    blocked = _gate(gates, "push", rc == 0, out[-300:])
    if blocked:
        return blocked
    return {"schema": SCHEMA, "command": "feature-push", "verdict": "PASS",
            "branch": branch, "gates": gates}


def _verify_pr(number: int, expected_head: str, gates: list, repo: Path) -> dict | None:
    """Shared verify bundle for pr-ready/pr-merge. Returns receipt-part or BLOCKED."""
    facts = pr_facts(number)
    if "error" in facts:
        blocked = _gate(gates, "pr_resolves", False, facts["error"])
        return {"receipt": None, "blocked": blocked}
    _gate(gates, "pr_resolves", True, f"#{number} {facts.get('title','')[:60]}")
    head = facts.get("headRefOid", "")
    blocked = _gate(gates, "head_pinned",
                    head == expected_head and len(head) == 40,
                    f"expected={expected_head[:8]} actual={head[:8]}")
    if blocked:
        return {"receipt": None, "blocked": blocked}
    blocked = _gate(gates, "base_is_main", facts.get("baseRefName") == "main",
                    str(facts.get("baseRefName")))
    if blocked:
        return {"receipt": None, "blocked": blocked}
    mergeable = facts.get("mergeable")
    if mergeable == "UNKNOWN":
        facts = pr_facts(number)
        mergeable = facts.get("mergeable")
    blocked = _gate(gates, "mergeable", mergeable == "MERGEABLE", str(mergeable))
    if blocked:
        return {"receipt": None, "blocked": blocked}
    files = pr_files(number)
    _gate(gates, "diff_understood", bool(files), f"files={len(files)}")
    diff = pr_diff(number)
    ws_ok, ws_detail = whitespace_check(diff)
    blocked = _gate(gates, "diff_check", ws_ok, ws_detail)
    if blocked:
        return {"receipt": None, "blocked": blocked}
    hits = secret_scan(diff)
    blocked = _gate(gates, "secret_scan", not hits, f"hits={len(hits)}")
    if blocked:
        return {"receipt": None, "blocked": blocked}
    ok, evidence = verify_head_worktree(head, files, repo)
    _gate(gates, "affected_tests", ok, json.dumps(evidence)[:800])
    if not ok:
        return {"receipt": None,
                "blocked": {"verdict": "BLOCKED", "blocked_by": "affected_tests",
                            "detail": json.dumps(evidence)[-500:], "gates": gates}}
    return {"receipt": {"head": head, "files": files, "evidence": evidence},
            "blocked": None}


def cmd_pr_ready(args) -> dict:
    gates: list = []
    blocked = repo_preflight(gates)
    if blocked:
        return blocked
    facts = pr_facts(args.pr)
    if facts.get("isDraft") is False:
        _gate(gates, "is_draft", True, "already ready")
    else:
        _gate(gates, "is_draft", True, "draft -> will mark ready after verify")
    res = _verify_pr(args.pr, args.head, gates, REPO_ROOT)
    if res["blocked"]:
        return res["blocked"]
    if args.dry_run:
        return {"schema": SCHEMA, "command": "pr-ready", "verdict": "DRY_RUN_PASS",
                "pr": args.pr, "head": res["receipt"]["head"][:8], "gates": gates}
    if facts.get("isDraft"):
        rc, out = _gh(["pr", "ready", str(args.pr)])
        blocked = _gate(gates, "mark_ready", rc == 0, out[-200:])
        if blocked:
            return blocked
    return {"schema": SCHEMA, "command": "pr-ready", "verdict": "PASS",
            "pr": args.pr, "head": res["receipt"]["head"][:8], "gates": gates}


def cmd_pr_merge(args) -> dict:
    gates: list = []
    blocked = repo_preflight(gates)
    if blocked:
        return blocked
    if args.method != "merge":
        blocked = _gate(gates, "merge_method", False, f"method={args.method} (only merge)")
        if blocked:
            return blocked
    if args.admin:
        blocked = _gate(gates, "no_admin_bypass", False, "--admin refused")
        if blocked:
            return blocked
    res = _verify_pr(args.pr, args.head, gates, REPO_ROOT)
    if res["blocked"]:
        return res["blocked"]
    if args.dry_run:
        return {"schema": SCHEMA, "command": "pr-merge", "verdict": "DRY_RUN_PASS",
                "pr": args.pr, "head": res["receipt"]["head"][:8], "gates": gates}
    rc, out = _gh(["pr", "merge", str(args.pr), "--merge",
                   "--match-head-commit", res["receipt"]["head"]])
    blocked = _gate(gates, "merge", rc == 0, out[-300:])
    if blocked:
        return blocked
    _git(["fetch", "origin", "main"], timeout=120)
    new_main = origin_main_sha()
    _gate(gates, "post_merge_reconcile", new_main != "UNKNOWN", new_main[:12])
    return {"schema": SCHEMA, "command": "pr-merge", "verdict": "PASS",
            "pr": args.pr, "head": res["receipt"]["head"][:8],
            "new_main": new_main[:12], "gates": gates}


def cmd_pr_close(args) -> dict:
    gates: list = []
    blocked = repo_preflight(gates)
    if blocked:
        return blocked
    if not args.superseded_by:
        blocked = _gate(gates, "superseded_by_required", False, "need --superseded-by N")
        if blocked:
            return blocked
    sup = pr_facts(args.superseded_by)
    blocked = _gate(gates, "superseder_merged", sup.get("state") == "MERGED",
                    f"#{args.superseded_by} state={sup.get('state')}")
    if blocked:
        return blocked
    if args.dry_run:
        return {"schema": SCHEMA, "command": "pr-close", "verdict": "DRY_RUN_PASS",
                "pr": args.pr, "gates": gates}
    rc, out = _gh(["pr", "close", str(args.pr), "--comment",
                   f"Superseded by #{args.superseded_by} (merged). {args.reason}".strip()])
    blocked = _gate(gates, "close", rc == 0, out[-200:])
    if blocked:
        return blocked
    return {"schema": SCHEMA, "command": "pr-close", "verdict": "PASS",
            "pr": args.pr, "gates": gates}


def cmd_reconcile(args) -> dict:
    _git(["fetch", "origin"], timeout=120)
    rc, out = _gh(["pr", "list", "--limit", "50", "--json",
                   "number,title,headRefOid,baseRefName,isDraft,mergeable,state",
                   "--jq", "map({n:.number,t:.title,h:.headRefOid[0:8],"
                           "b:.baseRefName,d:.isDraft,m:.mergeable})"])
    prs = json.loads(out) if rc == 0 else []
    return {"schema": SCHEMA, "command": "reconcile",
            "generated_at": datetime.now(UTC).isoformat(),
            "origin_main": origin_main_sha()[:12], "open_prs": prs}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="dealix_safe_git_gateway")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    fp = sub.add_parser("feature-push")
    fp.add_argument("--branch", required=True)
    fp.add_argument("--force", action="store_true")
    pr = sub.add_parser("pr-ready")
    pr.add_argument("pr", type=int)
    pr.add_argument("--head", required=True)
    pm = sub.add_parser("pr-merge")
    pm.add_argument("pr", type=int)
    pm.add_argument("--head", required=True)
    pm.add_argument("--method", default="merge")
    pm.add_argument("--admin", action="store_true")
    pc = sub.add_parser("pr-close")
    pc.add_argument("pr", type=int)
    pc.add_argument("--superseded-by", type=int, default=None)
    pc.add_argument("--reason", default="")
    sub.add_parser("reconcile")
    args = ap.parse_args(argv)
    fn = {"status": cmd_status, "feature-push": cmd_feature_push,
          "pr-ready": cmd_pr_ready, "pr-merge": cmd_pr_merge,
          "pr-close": cmd_pr_close, "reconcile": cmd_reconcile}[args.command]
    receipt = fn(args)
    receipt["dry_run"] = args.dry_run
    if args.json:
        print(json.dumps(receipt, ensure_ascii=False))
    else:
        print(f"GATEWAY_{args.command.upper()}={receipt.get('verdict')}")
        for g in receipt.get("gates", []):
            print(f"  {'PASS' if g['pass'] else 'FAIL'} {g['gate']}: {g.get('detail','')[:100]}")
        for key in ("blocked_by", "detail", "new_main", "origin_main", "head"):
            if key in receipt:
                print(f"  {key}={receipt[key]}")
    verdict = receipt.get("verdict", "")
    return 0 if verdict in ("PASS", "DRY_RUN_PASS") else 2


if __name__ == "__main__":
    raise SystemExit(main())
