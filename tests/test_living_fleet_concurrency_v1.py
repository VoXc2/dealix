from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DISPATCH = REPO / "scripts" / "ops" / "living_fleet_dispatch.sh"
ROLE = "DAILY_BUILDER_RND"
EVENT = "new_oss_candidate"


def _fixture(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    repo = tmp_path / "repo"
    py = repo / ".venv" / "bin" / "python"
    py.parent.mkdir(parents=True)
    py.symlink_to(Path(sys.executable))
    (repo / "docs" / "ops").mkdir(parents=True)
    (repo / "docs" / "ops" / "DAILY_BUILDER_CONTRACT.md").write_text("race-v1\n")
    counter = tmp_path / "owner-count.txt"
    (repo / "fake_owner.py").write_text(
        "from pathlib import Path\n"
        "import os\n"
        "p=Path(os.environ['FAKE_OWNER_COUNTER'])\n"
        "n=int(p.read_text()) if p.exists() else 0\n"
        "p.write_text(str(n+1))\n"
    )

    text = DISPATCH.read_text(encoding="utf-8")
    old = '"DAILY_BUILDER_RND|new_oss_candidate|llm|file:docs/ops/DAILY_BUILDER_CONTRACT.md|NONE"'
    new = '"DAILY_BUILDER_RND|new_oss_candidate|llm|file:docs/ops/DAILY_BUILDER_CONTRACT.md|.venv/bin/python fake_owner.py"'
    assert old in text
    text = text.replace(old, new, 1)
    marker = '  chmod 0640 "$RECEIPT"\n'
    assert marker in text
    # Widen the real race window while dispatch still owns the per-role lock.
    text = text.replace(marker, marker + '  sleep "${DEALIX_TEST_TERMINALIZATION_DELAY:-0}"\n', 1)
    variant = tmp_path / "dispatcher-race.sh"
    variant.write_text(text)
    variant.chmod(0o755)
    return repo, counter, tmp_path / "state", variant


def _env(repo: Path, counter: Path, state: Path) -> dict[str, str]:
    return dict(
        os.environ,
        DEALIX_REPO_ROOT=str(repo),
        DEALIX_FLEET_STATE_DIR=str(state),
        DEALIX_FOUNDER_PERSONAL_STATE_DIR=str(state / "founder-personal"),
        DEALIX_FLEET_FORCE="0",
        DEALIX_FLEET_MIN_MEM_MB="0",
        DEALIX_TEST_TERMINALIZATION_DELAY="1.5",
        FAKE_OWNER_COUNTER=str(counter),
    )


def _count(counter: Path) -> int:
    return int(counter.read_text()) if counter.exists() else 0


def test_concurrent_dispatch_and_collect_share_role_lock_and_terminalize_once(tmp_path: Path) -> None:
    repo, counter, state, variant = _fixture(tmp_path)
    env = _env(repo, counter, state)
    dispatch = subprocess.Popen(
        ["bash", str(variant), EVENT],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )

    deadline = time.time() + 8
    pending = None
    receipt = None
    while time.time() < deadline:
        pending_files = list((state / ROLE / "pending").glob("JOB-*.json"))
        receipt_files = list((state / ROLE / "receipts").glob("JOB-*.json"))
        if pending_files and receipt_files:
            pending, receipt = pending_files[0], receipt_files[0]
            break
        if dispatch.poll() is not None:
            break
        time.sleep(0.02)

    assert pending is not None and receipt is not None, "failed to reach widened receipt/pending race window"
    collect = subprocess.run(
        ["bash", str(variant), EVENT, "collect"],
        capture_output=True,
        text=True,
        timeout=10,
        env=env,
    )
    assert collect.returncode == 0, collect.stderr
    assert "COLLECT_SKIP_LOCKED" in collect.stdout

    out, err = dispatch.communicate(timeout=10)
    assert dispatch.returncode == 0, err
    assert "OWNER_EXECUTED" in out
    assert _count(counter) == 1
    assert (state / f"{ROLE}.useful_count").read_text().strip() == "1"
    assert len(list((state / ROLE / "receipts").glob("JOB-*.json"))) == 1
    assert len(list((state / ROLE / "pending" / "consumed").glob("JOB-*.json"))) == 1
    assert not list((state / ROLE / "pending").glob("JOB-*.json"))

    # Later collectors observe no pending job and cannot re-count it.
    again = subprocess.run(
        ["bash", str(variant), EVENT, "collect"],
        capture_output=True,
        text=True,
        timeout=10,
        env=env,
    )
    assert again.returncode == 0, again.stderr
    assert _count(counter) == 1
    assert (state / f"{ROLE}.useful_count").read_text().strip() == "1"


def test_terminal_counter_recovers_after_crash_between_counter_and_handoff_move(tmp_path: Path) -> None:
    repo, counter, state, variant = _fixture(tmp_path)
    text = variant.read_text(encoding="utf-8")
    terminalization = '''    if [[ "$USEFUL" == "true" ]]; then
      counter_once "$FLEET_STATE_DIR/${role}.useful_count" "$terminal_marker" || {
        log "TERMINALIZATION_BLOCKED role=${role} job=${JOB_ID}"
        exit 1
      }
    fi
'''
    assert terminalization in text
    crash_hook = terminalization + '''    if [[ "${DEALIX_TEST_CRASH_AFTER_COUNTER:-0}" == "1" ]]; then
      exit 97
    fi
'''
    variant.write_text(text.replace(terminalization, crash_hook, 1), encoding="utf-8")

    env = _env(repo, counter, state)
    env["DEALIX_TEST_TERMINALIZATION_DELAY"] = "0"
    env["DEALIX_TEST_CRASH_AFTER_COUNTER"] = "1"
    crashed = subprocess.run(
        ["bash", str(variant), EVENT],
        capture_output=True,
        text=True,
        timeout=10,
        env=env,
    )
    assert crashed.returncode == 97, crashed.stderr
    assert _count(counter) == 1
    pending = list((state / ROLE / "pending").glob("JOB-*.json"))
    assert len(pending) == 1
    assert not list((state / ROLE / "pending" / "consumed").glob("JOB-*.json"))
    markers = list((state / ROLE / "terminal").glob("*.useful.json"))
    assert len(markers) == 1
    assert '"STATE": "PREPARED"' in markers[0].read_text()

    env["DEALIX_TEST_CRASH_AFTER_COUNTER"] = "0"
    recovered = subprocess.run(
        ["bash", str(variant), EVENT, "collect"],
        capture_output=True,
        text=True,
        timeout=10,
        env=env,
    )
    assert recovered.returncode == 0, recovered.stderr
    assert _count(counter) == 1
    assert (state / f"{ROLE}.useful_count").read_text().strip() == "1"
    assert len(list((state / ROLE / "pending" / "consumed").glob("JOB-*.json"))) == 1
    assert not list((state / ROLE / "pending").glob("JOB-*.json"))
    assert '"STATE": "COMMITTED"' in markers[0].read_text()


def test_terminal_counter_recovers_when_later_job_advances_role_counter(tmp_path: Path) -> None:
    """A prepared marker may trail a later terminal counter increment."""
    repo, counter, state, variant = _fixture(tmp_path)
    role_dir = state / ROLE
    pending_dir = role_dir / "pending"
    receipt_dir = role_dir / "receipts"
    terminal_dir = role_dir / "terminal"
    pending_dir.mkdir(parents=True)
    receipt_dir.mkdir(parents=True)
    terminal_dir.mkdir(parents=True)

    for job_id in ("JOB-prepared-late", "JOB-later-committed"):
        (pending_dir / f"{job_id}.json").write_text(
            f'{{"JOB_ID":"{job_id}","ROLE":"{ROLE}","STATUS":"RUNNING"}}'
        )
        (receipt_dir / f"{job_id}.json").write_text(
            f'{{"JOB_ID":"{job_id}","ROLE":"{ROLE}","RESULT":"SUCCEEDED",'
            '"OWNER":"fake-owner","USEFUL_OUTPUT":"true"}'
        )

    counter_path = state / f"{ROLE}.useful_count"
    counter_path.write_text("2\n")
    (terminal_dir / "JOB-prepared-late.useful.json").write_text(
        f'{{"COUNTER_FILE":"{counter_path}","COUNTER_BEFORE":0,"COUNTER_AFTER":1,"STATE":"PREPARED"}}'
    )
    (terminal_dir / "JOB-later-committed.useful.json").write_text(
        f'{{"COUNTER_FILE":"{counter_path}","COUNTER_BEFORE":1,"COUNTER_AFTER":2,"STATE":"COMMITTED"}}'
    )

    env = _env(repo, counter, state)
    recovered = subprocess.run(
        ["bash", str(variant), EVENT, "collect"],
        capture_output=True,
        text=True,
        timeout=10,
        env=env,
    )
    assert recovered.returncode == 0, recovered.stderr
    assert counter_path.read_text().strip() == "2"
    assert not list(pending_dir.glob("JOB-*.json"))
    assert len(list((pending_dir / "consumed").glob("JOB-*.json"))) == 2
