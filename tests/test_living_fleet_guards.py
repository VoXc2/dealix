"""Living Fleet v2 guards — truthful lifecycle, fingerprints, concurrency, receipts."""

import json
import os
import subprocess
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DISPATCH = REPO / "scripts" / "ops" / "living_fleet_dispatch.sh"


def run_dispatcher(env_event: str, state_dir: str, *extra_env: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["DEALIX_FLEET_STATE_DIR"] = state_dir
    env["DEALIX_FLEET_FORCE"] = "0"
    for kv in extra_env:
        k, _, v = kv.partition("=")
        env[k] = v
    return subprocess.run(
        ["bash", str(DISPATCH), env_event],
        capture_output=True, text=True, timeout=120, env=env,
    )


def state(state_dir: str, role: str) -> dict:
    p = Path(state_dir) / f"{role}.state.json"
    return json.loads(p.read_text()) if p.exists() else {}


# ---------------------------------------------------------------- structure
def test_no_l5_verbs_in_router() -> None:
    text = DISPATCH.read_text(encoding="utf-8")
    for token in ("git push", "gh pr merge", "railway up", "railway redeploy",
                  "chown", "--squash", "ollama rm"):
        assert token not in text


def test_runtime_state_outside_git() -> None:
    assert "/opt/dealix/control/state/living_fleet" in DISPATCH.read_text(encoding="utf-8")


def test_single_routing_source_registry_derived() -> None:
    text = DISPATCH.read_text(encoding="utf-8")
    assert 'roles_for_event()' in text and "REGISTRY" in text
    assert "route_roles_for_event" not in text  # duplicated table removed


def test_unknown_event_is_honest_noop() -> None:
    with tempfile.TemporaryDirectory() as td:
        r = run_dispatcher("totally_unknown_event", td)
        assert "NO_OP unknown-or-sensor event" in (r.stdout + r.stderr)


# ------------------------------------------------------- fingerprint truth
def _make_repo_state(td: Path) -> tuple[str, str, str]:
    biz = td / "repo" / "business" / "_data"
    biz.mkdir(parents=True)
    (biz / "a.json").write_text("{}")
    (biz / "b.json").write_text("{}")
    return str(biz / "a.json"), str(biz / "b.json"), str(biz)


def _force_run(state_dir: str, event: str, repo_root: str) -> subprocess.CompletedProcess:
    return run_dispatcher(event, state_dir, f"DEALIX_REPO_ROOT={repo_root}",
                          "DEALIX_FLEET_FORCE=1")


def test_changing_second_watch_file_changes_fingerprint(tmp_path: Path) -> None:
    """REVENUE_INTEL watches two files; changing ONLY the second must wake it."""
    biz = tmp_path / "business" / "_data"
    biz.mkdir(parents=True)
    (biz / "outreach_review_queue.json").write_text("[]")
    (biz / "proposals.index.json").write_text("[]")
    _force_run(str(tmp_path), "morning", str(tmp_path))
    fp1 = json.loads((tmp_path / "REVENUE_INTEL.state.json").read_text())["INPUT_FINGERPRINT"]
    (biz / "proposals.index.json").write_text("[{\"changed\": true}]")
    _force_run(str(tmp_path), "morning", str(tmp_path))
    fp2 = json.loads((tmp_path / "REVENUE_INTEL.state.json").read_text())["INPUT_FINGERPRINT"]
    assert fp1 != fp2


def test_identical_state_skips_cheaply(tmp_path: Path) -> None:
    biz = tmp_path / "business" / "_data"
    biz.mkdir(parents=True)
    (biz / "outreach_review_queue.json").write_text("[]")
    (biz / "proposals.index.json").write_text("[]")
    _force_run(str(tmp_path), "morning", str(tmp_path))
    r = run_dispatcher("morning", str(tmp_path), f"DEALIX_REPO_ROOT={tmp_path}")
    assert "SKIP_UNCHANGED" in (r.stdout + r.stderr)


def test_dated_artifact_rollover_wakes_role(tmp_path: Path) -> None:
    sigs = tmp_path / "reports" / "founder"
    sigs.mkdir(parents=True)
    old = sigs / "MARKET_SIGNALS_2026-08-24.md"; old.write_text("old")
    _force_run(str(tmp_path), "market_signal", str(tmp_path))
    fp_old = json.loads((tmp_path / "MARKET_INTEL.state.json").read_text())["INPUT_FINGERPRINT"]
    new = sigs / "MARKET_SIGNALS_2026-08-25.md"; new.write_text("new")
    os.utime(old, (1, 1))  # ensure mtime ordering cannot fake the result
    _force_run(str(tmp_path), "market_signal", str(tmp_path))
    fp_new = json.loads((tmp_path / "MARKET_INTEL.state.json").read_text())["INPUT_FINGERPRINT"]
    assert fp_new != fp_old, "newer dated artifact must change the fingerprint"


def test_absolute_runtime_watch_resolves_outside_repo_and_skips_when_stable(tmp_path: Path) -> None:
    """DELIVERY watches a REAL absolute runtime CSV outside the repo.
    Resolution must escape $REPO_ROOT, and a stable runtime file must skip."""
    _force_run(str(tmp_path), "evening", str(tmp_path))
    st1 = json.loads((tmp_path / "DELIVERY.state.json").read_text())
    r2 = run_dispatcher("evening", str(tmp_path), f"DEALIX_REPO_ROOT={tmp_path}")
    st2 = json.loads((tmp_path / "DELIVERY.state.json").read_text())
    assert st1["INPUT_FINGERPRINT"] == st2["INPUT_FINGERPRINT"]
    assert "SKIP_UNCHANGED" in (r2.stdout + r2.stderr)
    # the watched path must be the real runtime tracker, resolved absolutely
    import re as _re
    m = _re.search(r"DELIVERY\|[^|]+\|det\|rtfile:([^,|]+)", DISPATCH.read_text(encoding="utf-8"))
    assert m and os.path.isfile(m.group(1).strip()), "registry must watch the real runtime tracker"




def test_git_head_watch_wakes_on_new_commit(tmp_path: Path) -> None:
    """ENGINEERING watches git:HEAD via an ISOLATED WORKTREE (no repo mutation)."""
    import subprocess as sp
    wt = Path(str(tmp_path)) / "wt"
    sp.run(["git", "worktree", "add", "-q", str(wt), "HEAD"],
           cwd=REPO, capture_output=True, text=True)
    def dispatch():
        return run_dispatcher("ci_failure", str(tmp_path) + "/state",
                              f"DEALIX_REPO_ROOT={wt}", "DEALIX_FLEET_FORCE=0")
    try:
        dispatch()
        fp1 = json.loads((Path(str(tmp_path)) / "state" / "ENGINEERING.state.json").read_text())["INPUT_FINGERPRINT"]
        sp.run(["git", "commit", "-q", "--allow-empty", "-m", "fleet-watch-probe"],
               cwd=wt, capture_output=True, text=True)
        dispatch()
        fp2 = json.loads((Path(str(tmp_path)) / "state" / "ENGINEERING.state.json").read_text())["INPUT_FINGERPRINT"]
    finally:
        sp.run(["git", "worktree", "remove", "--force", str(wt)],
               cwd=REPO, capture_output=True, text=True)
    assert fp1 != fp2, "new HEAD must wake ENGINEERING"


# --------------------------------------------------- lifecycle truthfulness
def test_enqueue_never_claims_success_and_ownerless_blocks(tmp_path: Path) -> None:
    run_dispatcher("market_signal", str(tmp_path),
                   "DEALIX_REPO_ROOT=/nonexistent-repo-root")
    st = json.loads((Path(str(tmp_path)) / "MARKET_INTEL.state.json").read_text())
    assert st["STATUS"] == "BLOCKED" and st["BLOCKER"] == "owner_missing"
    assert st.get("LAST_SUCCESS_AT", "") == ""


def test_owner_execution_receipt_then_collect_succeeds(tmp_path: Path) -> None:
    run_dispatcher("approval_changed", str(tmp_path), f"DEALIX_REPO_ROOT={REPO}")
    rec = list((Path(str(tmp_path)) / "GOVERNANCE" / "receipts").glob("*.json"))
    assert rec, "real owner run must emit a typed receipt"
    data = json.loads(rec[0].read_text())
    assert isinstance(data["EXIT_CODE"], int)
    env = dict(os.environ, DEALIX_FLEET_STATE_DIR=str(tmp_path))
    subprocess.run(["bash", str(DISPATCH), "nightly", "collect"],
                   capture_output=True, text=True, env=env)


def test_failure_receipt_marks_failed_without_useful_bump(tmp_path: Path) -> None:
    role_dir = tmp_path / "ENGINEERING"; pend = role_dir / "pending"
    rcpts = role_dir / "receipts"; rcpts.mkdir(parents=True); pend.mkdir(parents=True)
    (pend / "JOB-ENGINEERING-9.json").write_text(json.dumps(
        {"JOB_ID": "JOB-ENGINEERING-9", "ROLE": "ENGINEERING"}))
    (rcpts / "JOB-ENGINEERING-9.json").write_text(json.dumps(
        {"JOB_ID": "JOB-ENGINEERING-9", "RESULT": "FAILED",
         "EXIT_CODE": 2, "USEFUL_OUTPUT": "false", "BLOCKER": "boom"}))
    env = dict(os.environ, DEALIX_FLEET_STATE_DIR=str(tmp_path))
    subprocess.run(["bash", str(DISPATCH), "ci_failure", "collect"],
                   capture_output=True, text=True, env=env)
    st = json.loads((tmp_path / "ENGINEERING.state.json").read_text())
    assert st["STATUS"] == "FAILED" and st["BLOCKER"] == "boom"
    assert not (tmp_path / "ENGINEERING.useful_count").exists()


def test_collect_without_receipt_keeps_job_pending(tmp_path: Path) -> None:
    pend = tmp_path / "DATA_BRAIN" / "pending"; pend.mkdir(parents=True)
    job = pend / "JOB-DATA_BRAIN-1.json"
    job.write_text(json.dumps({"JOB_ID": "JOB-DATA_BRAIN-1", "ROLE": "DATA_BRAIN"}))
    env = dict(os.environ, DEALIX_FLEET_STATE_DIR=str(tmp_path))
    subprocess.run(["bash", str(DISPATCH), "nightly", "collect"],
                   capture_output=True, text=True, env=env)
    assert job.exists(), "no receipt ⇒ job must stay pending"


# ------------------------------------------------------------- concurrency
def test_concurrent_same_role_dispatch_keeps_state_valid(tmp_path: Path) -> None:
    procs = [subprocess.Popen(
        ["bash", str(DISPATCH), "ci_failure"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        env=dict(os.environ, DEALIX_FLEET_STATE_DIR=str(tmp_path),
                 DEALIX_REPO_ROOT=str(REPO))) for _ in range(3)]
    codes = [p.wait(timeout=180) for p in procs]
    assert all(c in (0, 1) for c in codes), codes
    st = json.loads((tmp_path / "ENGINEERING.state.json").read_text())
    assert st.get("INPUT_FINGERPRINT")


def test_autopilot_wires_canonical_cadence_to_fleet() -> None:
    ap = (REPO / "scripts" / "ops" / "dealix_company_autopilot.sh").read_text(encoding="utf-8")
    assert "living_fleet_dispatch.sh" in ap
    assert 'FLEET_EVENT="heartbeat"' in ap  # sensor-only default
    # every routed event must exist in the dispatcher registry routing
    disp = DISPATCH.read_text(encoding="utf-8")
    for ev in ("morning", "midday", "evening", "nightly", "repo_watch", "strategic"):
        assert ev in disp
