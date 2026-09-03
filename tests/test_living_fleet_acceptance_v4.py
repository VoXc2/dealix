"""Sovereign Living Fleet acceptance for FORCE=0 transitions.

These tests use the real dispatcher logic with a temporary fake repo/owner. They
prove FORCE=0 owner transitions, structural supersede behavior, and idempotence
after terminalization. The actual dispatch/collect race is intentionally proved
in tests/test_living_fleet_concurrency_v1.py so a sequential test is never
misrepresented as concurrency evidence.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DISPATCH = REPO / "scripts" / "ops" / "living_fleet_dispatch.sh"
ROLE = "DAILY_BUILDER_RND"
EVENT = "new_oss_candidate"


def _fake_repo(tmp_path: Path) -> tuple[Path, Path]:
    repo = tmp_path / "repo"
    py = repo / ".venv" / "bin" / "python"
    py.parent.mkdir(parents=True)
    py.symlink_to(Path(sys.executable))
    (repo / "docs" / "ops").mkdir(parents=True)
    (repo / "docs" / "ops" / "DAILY_BUILDER_CONTRACT.md").write_text("v1\n")
    counter = tmp_path / "owner-count.txt"
    for name in ("fake_owner.py", "fake_owner_v2.py"):
        (repo / name).write_text(
            "from pathlib import Path\n"
            "import os\n"
            "p=Path(os.environ['FAKE_OWNER_COUNTER'])\n"
            "n=int(p.read_text()) if p.exists() else 0\n"
            "p.write_text(str(n+1))\n"
        )
    return repo, counter


def _variant(tmp_path: Path, owner: str) -> Path:
    lines = DISPATCH.read_text(encoding="utf-8").splitlines()
    found = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(f'"{ROLE}|') and stripped.endswith('"'):
            fields = stripped[1:-1].split("|")
            assert len(fields) == 5
            fields[-1] = owner
            indent = line[: len(line) - len(line.lstrip())]
            lines[index] = indent + '"' + "|".join(fields) + '"'
            found = True
            break
    assert found, f"registry row missing for {ROLE}"
    path = tmp_path / (owner.replace("/", "_").replace(" ", "_") + ".sh")
    path.write_text("\n".join(lines) + "\n")
    path.chmod(0o755)
    return path


def _run(
    dispatcher: Path,
    *,
    state: Path,
    repo: Path,
    counter: Path,
    mode: str = "dispatch",
    force: str = "0",
) -> subprocess.CompletedProcess[str]:
    env = dict(
        os.environ,
        DEALIX_FLEET_STATE_DIR=str(state),
        DEALIX_FOUNDER_PERSONAL_STATE_DIR=str(state / "founder-personal"),
        DEALIX_FLEET_FORCE=force,
        DEALIX_FLEET_MIN_MEM_MB="0",
        DEALIX_REPO_ROOT=str(repo),
        FAKE_OWNER_COUNTER=str(counter),
    )
    argv = ["bash", str(dispatcher), EVENT]
    if mode != "dispatch":
        argv.append(mode)
    return subprocess.run(argv, capture_output=True, text=True, timeout=120, env=env)


def _state(state: Path) -> dict:
    return json.loads((state / f"{ROLE}.state.json").read_text())


def _count(counter: Path) -> int:
    return int(counter.read_text()) if counter.exists() else 0


def _receipts(state: Path) -> list[Path]:
    return sorted((state / ROLE / "receipts").glob("*.json"))


def test_identical_force_zero_dispatch_executes_real_owner_once(tmp_path: Path) -> None:
    repo, counter = _fake_repo(tmp_path)
    state = tmp_path / "state"
    variant = _variant(tmp_path, ".venv/bin/python fake_owner.py")

    first = _run(variant, state=state, repo=repo, counter=counter, force="0")
    assert first.returncode == 0, first.stderr
    assert _count(counter) == 1
    assert len(_receipts(state)) == 1

    second = _run(variant, state=state, repo=repo, counter=counter, force="0")
    assert second.returncode == 0, second.stderr
    assert "SKIP_UNCHANGED" in second.stdout
    assert _count(counter) == 1
    assert len(_receipts(state)) == 1


def test_none_to_real_force_zero_invalidates_dedupe_and_supersedes_handoff(tmp_path: Path) -> None:
    repo, counter = _fake_repo(tmp_path)
    state = tmp_path / "state"

    ownerless = _run(DISPATCH, state=state, repo=repo, counter=counter, force="0")
    assert ownerless.returncode == 0, ownerless.stderr
    before = _state(state)
    assert before["STATUS"] == "BLOCKED"
    assert before["OWNER"] == "NONE"
    old_signature = before["OWNER_SIGNATURE"]
    pending_before = list((state / ROLE / "pending").glob("JOB-*.json"))
    assert len(pending_before) == 1

    variant = _variant(tmp_path, ".venv/bin/python fake_owner.py")
    activated = _run(variant, state=state, repo=repo, counter=counter, force="0")
    assert activated.returncode == 0, activated.stderr
    after = _state(state)
    assert after["OWNER_SIGNATURE"] != old_signature
    assert after["STATUS"] == "SUCCEEDED"
    assert _count(counter) == 1

    superseded = list((state / ROLE / "pending").glob("*.superseded.json"))
    remaining = [
        path
        for path in (state / ROLE / "pending").glob("JOB-*.json")
        if ".superseded." not in path.name
    ]
    assert len(superseded) == 1
    assert not remaining
    payload = json.loads(superseded[0].read_text())
    assert payload["STATUS"] == "SUPERSEDED_BY_OWNER_ACTIVATION"
    assert payload["NEW_OWNER_SIGNATURE"] == after["OWNER_SIGNATURE"]


def test_real_to_real_rotation_executes_at_force_zero(tmp_path: Path) -> None:
    repo, counter = _fake_repo(tmp_path)
    state = tmp_path / "state"
    v1 = _variant(tmp_path, ".venv/bin/python fake_owner.py")
    v2 = _variant(tmp_path, ".venv/bin/python fake_owner_v2.py")

    r1 = _run(v1, state=state, repo=repo, counter=counter, force="0")
    assert r1.returncode == 0, r1.stderr
    sig1 = _state(state)["OWNER_SIGNATURE"]
    assert _count(counter) == 1

    r2 = _run(v2, state=state, repo=repo, counter=counter, force="0")
    assert r2.returncode == 0, r2.stderr
    sig2 = _state(state)["OWNER_SIGNATURE"]
    assert sig2 != sig1
    assert _count(counter) == 2
    assert len(_receipts(state)) == 2


def test_post_dispatch_collect_is_idempotent_after_terminalization(tmp_path: Path) -> None:
    """Sequential collector re-entry cannot double-count a completed dispatch."""
    repo, counter = _fake_repo(tmp_path)
    state = tmp_path / "state"
    variant = _variant(tmp_path, ".venv/bin/python fake_owner.py")

    dispatched = _run(variant, state=state, repo=repo, counter=counter, force="0")
    assert dispatched.returncode == 0, dispatched.stderr
    assert _count(counter) == 1
    assert (state / f"{ROLE}.useful_count").read_text().strip() == "1"
    assert len(_receipts(state)) == 1
    consumed_before = list(
        (state / ROLE / "pending" / "consumed").glob("JOB-*.json")
    )
    assert len(consumed_before) == 1

    for _ in range(2):
        collected = _run(
            variant,
            state=state,
            repo=repo,
            counter=counter,
            mode="collect",
            force="0",
        )
        assert collected.returncode == 0, collected.stderr

    assert _count(counter) == 1
    assert (state / f"{ROLE}.useful_count").read_text().strip() == "1"
    assert len(_receipts(state)) == 1
    assert len(
        list((state / ROLE / "pending" / "consumed").glob("JOB-*.json"))
    ) == 1
