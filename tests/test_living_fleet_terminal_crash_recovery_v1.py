from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DISPATCH = REPO / "scripts" / "ops" / "living_fleet_dispatch.sh"
ROLE = "DAILY_BUILDER_RND"
EVENT = "new_oss_candidate"


def test_collect_recovers_after_counter_applied_before_pending_move(tmp_path: Path) -> None:
    """A crash after counter write but before pending move must not recount."""
    repo = tmp_path / "repo"
    repo.mkdir()
    state = tmp_path / "state"
    job_id = "JOB-crash-recovery-1"

    pending_dir = state / ROLE / "pending"
    receipt_dir = state / ROLE / "receipts"
    terminal_dir = state / ROLE / "terminal"
    pending_dir.mkdir(parents=True)
    receipt_dir.mkdir(parents=True)
    terminal_dir.mkdir(parents=True)

    pending = pending_dir / f"{job_id}.json"
    pending.write_text(
        json.dumps(
            {
                "JOB_ID": job_id,
                "ROLE": ROLE,
                "EVENT": EVENT,
                "OWNER": "fake-owner",
                "STATUS": "RUNNING",
            }
        )
    )
    receipt = receipt_dir / f"{job_id}.json"
    receipt.write_text(
        json.dumps(
            {
                "JOB_ID": job_id,
                "ROLE": ROLE,
                "EVENT": EVENT,
                "OWNER": "fake-owner",
                "RESULT": "SUCCEEDED",
                "USEFUL_OUTPUT": "true",
                "BLOCKER": "",
            }
        )
    )

    counter = state / f"{ROLE}.useful_count"
    counter.write_text("2\n")
    marker = terminal_dir / f"{job_id}.useful.json"
    marker.write_text(
        json.dumps(
            {
                "COUNTER_FILE": str(counter),
                "COUNTER_BEFORE": 0,
                "COUNTER_AFTER": 1,
                "STATE": "PREPARED",
            }
        )
    )
    later_marker = terminal_dir / "JOB-later.useful.json"
    later_marker.write_text(
        json.dumps(
            {
                "COUNTER_FILE": str(counter),
                "COUNTER_BEFORE": 1,
                "COUNTER_AFTER": 2,
                "STATE": "COMMITTED",
            }
        )
    )

    env = dict(
        os.environ,
        DEALIX_REPO_ROOT=str(repo),
        DEALIX_FLEET_STATE_DIR=str(state),
        DEALIX_FOUNDER_PERSONAL_STATE_DIR=str(state / "founder-personal"),
        DEALIX_FLEET_FORCE="0",
        DEALIX_FLEET_MIN_MEM_MB="0",
    )
    result = subprocess.run(
        ["bash", str(DISPATCH), EVENT, "collect"],
        capture_output=True,
        text=True,
        timeout=20,
        env=env,
    )
    assert result.returncode == 0, result.stderr
    assert counter.read_text().strip() == "2"

    terminal = json.loads(marker.read_text())
    assert terminal["STATE"] == "COMMITTED"
    assert terminal["TERMINAL_RESULT"] == "SUCCEEDED"
    assert not pending.exists()
    consumed = pending_dir / "consumed" / pending.name
    assert consumed.exists()

    # A later collector has no pending job and still cannot increase the count.
    again = subprocess.run(
        ["bash", str(DISPATCH), EVENT, "collect"],
        capture_output=True,
        text=True,
        timeout=20,
        env=env,
    )
    assert again.returncode == 0, again.stderr
    assert counter.read_text().strip() == "2"
