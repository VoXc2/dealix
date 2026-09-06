#!/usr/bin/env python3
"""Private GitHub Issue -> Dealix VPS allowlisted command bridge.

Security model:
- repository must be private
- only comments authored by the configured founder login are considered
- command must be an exact `!dealix <allowlisted-command>` line
- no arbitrary shell evaluation
- no L5 operations
- command output is redacted and capped before it is posted back to GitHub
- durable state prevents automatic redispatch; ambiguous outcomes fail closed
- explicit bootstrap skips ALL historical comments; missing/corrupt state never resets
- receipt publication can retry without rerunning a completed command
- native issue-comment events are a failover path over the same dispatcher/state,
  not a second authority system
"""

from __future__ import annotations

import fcntl
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterator
from urllib.parse import urlencode

REPO = "Dealix-sa/dealix"
ISSUE = 1119
FOUNDER = "VoXc2"
PREFIX = "!dealix "
CONTROL = Path("/opt/dealix/control/bin/dealix_vps_control.sh")
STATE = Path("/opt/dealix/control/state/issue_bridge.json")
LOCK = Path("/opt/dealix/control/state/issue_bridge.lock")
MAX_OUTPUT_CHARS = 6000
DEFAULT_NATIVE_GRACE_SECONDS = 75
MAX_COMMENT_PAGES = 100
PROOF_AUTHORS = {FOUNDER, "github-actions[bot]"}

ALLOWED = {
    "status",
    "repo-inspect",
    "verify",
    "autonomous-dry-run",
    "daily",
    "sales-arena",
    "ollama-status",
    "n8n-status",
    "security-status",
    "autopilot-status",
    "autopilot-heartbeat",
    "autopilot-production",
    "autopilot-repo-watch",
    "autopilot-preflight",
    "autopilot-morning-fallback",
    "autopilot-midday",
    "autopilot-evening",
    "autopilot-nightly",
    "autopilot-weekly",
    "autopilot-local-ai",
}

SECRET_PATTERNS = (
    re.compile(r"(?i)(authorization:\s*bearer\s+)[^\s]+"),
    re.compile(r"\bgh[opsu]_[A-Za-z0-9_\-]{10,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_\-]{10,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_\-]{10,}\b"),
    re.compile(r"(?i)\b([A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)[A-Z0-9_]*)\s*=\s*[^\s]+"),
)


def now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def run(args: list[str], *, check: bool = True, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        text=True,
        capture_output=True,
        check=check,
        timeout=timeout,
        env={**os.environ, "GH_PAGER": "cat", "PAGER": "cat"},
    )


def gh_json(endpoint: str, *, method: str = "GET") -> Any:
    proc = run(["gh", "api", "--method", method, endpoint])
    return json.loads(proc.stdout)


def gh_comment(body: str) -> None:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as handle:
        handle.write(body)
        temp_name = handle.name
    try:
        run(
            [
                "gh",
                "api",
                "--method",
                "POST",
                f"repos/{REPO}/issues/{ISSUE}/comments",
                "-F",
                f"body=@{temp_name}",
            ],
            timeout=60,
        )
    finally:
        Path(temp_name).unlink(missing_ok=True)


def _timestamp(value: Any) -> str:
    if not isinstance(value, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z", value
    ):
        raise ValueError("invalid timestamp")
    datetime.fromisoformat(value.replace("Z", "+00:00"))
    return value


def _comment_id(value: Any, *, allow_zero: bool = False) -> int:
    if type(value) is not int or value < (0 if allow_zero else 1):
        raise ValueError("invalid comment id")
    return value


def load_state() -> dict[str, Any]:
    """Never recover missing/corrupt state by replaying the historical queue."""
    if STATE.is_symlink() or not STATE.is_file():
        raise RuntimeError("BRIDGE_HOLD_STATE_MISSING_OR_UNSAFE")
    try:
        payload = json.loads(STATE.read_text(encoding="utf-8"))
        _comment_id(payload["last_comment_id"], allow_zero=True)
        _timestamp(payload["last_created_at"])
        pending = payload.get("pending")
        if pending is not None:
            if not isinstance(pending, dict):
                raise ValueError("invalid pending state")
            if _comment_id(pending["id"]) <= payload["last_comment_id"]:
                raise ValueError("pending id is behind cursor")
            _timestamp(pending["created_at"])
            _timestamp(pending["started_at"])
            if pending["command"] not in ALLOWED:
                raise ValueError("invalid pending command")
            if pending["phase"] not in {"STARTED", "FINISHED"}:
                raise ValueError("invalid pending phase")
            if pending["phase"] == "FINISHED":
                proof = pending["proof"]
                if (type(pending["exit_code"]) is not int
                        or not isinstance(proof, str)
                        or len(proof) > MAX_OUTPUT_CHARS + 2000
                        or not proof.startswith("DEALIX_VPS_COMMAND_PROOF\n")
                        or f'- source_comment_id: `{pending["id"]}`' not in proof.splitlines()
                        or f'- command: `{pending["command"]}`' not in proof.splitlines()):
                    raise ValueError("invalid finished proof")
        return payload
    except (OSError, ValueError, KeyError, TypeError):
        raise RuntimeError("BRIDGE_HOLD_STATE_INVALID") from None


def _write_state(payload: dict[str, Any]) -> None:
    """Caller holds execution_lock; atomically replace and fsync one state file."""
    STATE.parent.mkdir(parents=True, exist_ok=True)
    if STATE.is_symlink():
        raise RuntimeError("BRIDGE_HOLD_STATE_SYMLINK")
    payload = {**payload, "updated_at": now_iso()}
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=STATE.parent, prefix=".issue-bridge-", delete=False
    ) as handle:
        temporary = Path(handle.name)
        try:
            os.fchmod(handle.fileno(), 0o600)
            handle.write(json.dumps(payload, indent=2) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
            os.replace(temporary, STATE)
            directory = os.open(STATE.parent, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
        finally:
            temporary.unlink(missing_ok=True)


def save_state(comment_id: int, created_at: str) -> None:
    state = load_state()
    if _comment_id(comment_id, allow_zero=True) < state["last_comment_id"]:
        raise RuntimeError("BRIDGE_HOLD_CURSOR_REGRESSION")
    _write_state({
        "last_comment_id": comment_id,
        "last_created_at": _timestamp(created_at),
        "pending": None,
    })


@contextmanager
def execution_lock() -> Iterator[None]:
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    with LOCK.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def redact(text: str) -> str:
    cleaned = text.replace("\x00", "")
    for pattern in SECRET_PATTERNS:
        if pattern.groups:
            cleaned = pattern.sub(lambda m: f"{m.group(1)}[REDACTED]", cleaned)
        else:
            cleaned = pattern.sub("[REDACTED]", cleaned)
    cleaned = re.sub(
        r"(?i)([?&](?:token|key|secret|password|signature)=)[^&\s]+",
        r"\1[REDACTED]",
        cleaned,
    )
    if len(cleaned) > MAX_OUTPUT_CHARS:
        cleaned = "[OUTPUT TRUNCATED]\n" + cleaned[-MAX_OUTPUT_CHARS:]
    return cleaned


def parse_command(body: str) -> str | None:
    stripped = body.strip()
    if not stripped.startswith(PREFIX):
        return None
    if "\n" in stripped or "\r" in stripped:
        return None
    command = stripped[len(PREFIX) :].strip()
    return command if command in ALLOWED else "__DENIED__"


def ensure_private_repo() -> None:
    repo = gh_json(f"repos/{REPO}")
    if repo.get("private") is not True:
        raise RuntimeError("repository is not private")


def list_comments(*, since: str | None = None) -> list[dict[str, Any]]:
    """Read a bounded complete snapshot, including pages of edited old comments.

    GitHub's `since` selects update time, not just creation time. A first page
    containing only old IDs must not starve newer commands on subsequent pages.
    No cursor is advanced on partial reads or a pagination-cap failure.
    """
    found: dict[int, dict[str, Any]] = {}
    for page in range(1, MAX_COMMENT_PAGES + 1):
        query: dict[str, Any] = {"per_page": 100, "page": page}
        if since is not None:
            query["since"] = _timestamp(since)
        rows = gh_json(f"repos/{REPO}/issues/{ISSUE}/comments?{urlencode(query)}")
        if not isinstance(rows, list):
            raise RuntimeError("BRIDGE_HOLD_COMMENT_PAGE_INVALID")
        try:
            for row in rows:
                ident = _comment_id(row["id"])
                _timestamp(row["created_at"])
                if not isinstance(row.get("body"), str) or not isinstance(row.get("user"), dict):
                    raise ValueError("malformed comment")
                if ident in found and row != found[ident]:
                    raise ValueError("comment changed during pagination")
                found[ident] = row
        except (ValueError, KeyError, TypeError):
            raise RuntimeError("BRIDGE_HOLD_COMMENT_INVALID_OR_CHANGED") from None
        if len(rows) < 100:
            return [found[key] for key in sorted(found)]
    raise RuntimeError("BRIDGE_HOLD_PAGINATION_LIMIT")


def _since(created_at: str) -> str:
    # Overlap one second; exact comment IDs provide deduplication.
    stamp = datetime.fromisoformat(_timestamp(created_at).replace("Z", "+00:00"))
    return (stamp - timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%SZ")


def bootstrap_state() -> int:
    """Explicit first initialization skips history; never reset existing state."""
    with execution_lock():
        if STATE.exists() or STATE.is_symlink():
            raise RuntimeError("BRIDGE_HOLD_BOOTSTRAP_STATE_EXISTS")
        comments = list_comments()
        latest = comments[-1] if comments else None
        _write_state({
            "last_comment_id": latest["id"] if latest else 0,
            "last_created_at": latest["created_at"] if latest else now_iso(),
            "pending": None,
        })
    return 0


def proof_exists(comment_id: int, command: str | None = None, *, since: str | None = None) -> bool:
    comments = list_comments(since=since)
    needle = f"- source_comment_id: `{comment_id}`"
    for item in comments:
        body = item["body"]
        if (item["user"].get("login") in PROOF_AUTHORS
                and body.startswith("DEALIX_VPS_COMMAND_PROOF\n")
                and needle in body.splitlines()
                and (command is None or f"- command: `{command}`" in body.splitlines())):
            return True
    return False


def event_comment(event: dict[str, Any]) -> dict[str, Any] | None:
    if str(event.get("action") or "") != "created":
        return None
    repository = event.get("repository") or {}
    if str(repository.get("full_name") or "") != REPO or repository.get("private") is not True:
        return None
    issue = event.get("issue") or {}
    if int(issue.get("number") or 0) != ISSUE:
        return None
    comment = event.get("comment") or {}
    author = str((comment.get("user") or {}).get("login") or "")
    if author != FOUNDER:
        return None
    return comment


def resume_pending() -> int:
    """Retry receipt publication, NEVER redispatch an ambiguous command.

    This is at-most-once automatic dispatch, not a distributed exactly-once
    guarantee. A crash after STARTED requires evidence review. A completed
    command with a temporarily unavailable GitHub API is safely publishable.
    """
    state = load_state()
    pending = state.get("pending")
    if pending is None:
        return 0
    if pending["phase"] != "FINISHED":
        raise RuntimeError("BRIDGE_HOLD_AMBIGUOUS_DISPATCH_REVIEW_REQUIRED")
    if not proof_exists(pending["id"], pending["command"], since=_since(pending["created_at"])):
        gh_comment(pending["proof"])
    save_state(pending["id"], pending["created_at"])
    return pending["exit_code"]


def execute_comment(comment: dict[str, Any]) -> int:
    """Called only under the shared lock after sequential queue selection."""
    state = load_state()
    if state.get("pending") is not None:
        raise RuntimeError("BRIDGE_HOLD_PENDING_COMMAND")
    comment_id = _comment_id(comment["id"])
    created_at = _timestamp(comment["created_at"])
    if comment_id <= state["last_comment_id"]:
        return 0
    author = str((comment.get("user") or {}).get("login") or "")
    command = parse_command(str(comment.get("body") or ""))
    if author != FOUNDER or command is None:
        # Founder notes and proof comments must advance the durable cursor too.
        save_state(comment_id, created_at)
        return 0
    if command == "__DENIED__":
        save_state(comment_id, created_at)
        print("DEALIX_VPS_COMMAND=DENIED_ALLOWLIST")
        return 0
    if proof_exists(comment_id, command, since=_since(created_at)):
        save_state(comment_id, created_at)
        return 0

    started = now_iso()
    pending = {"id": comment_id, "created_at": created_at, "command": command,
               "started_at": started, "phase": "STARTED"}
    _write_state({**state, "pending": pending})
    proc = subprocess.run(
        [str(CONTROL), command], text=True, capture_output=True, check=False,
        timeout=3300,
        env={**os.environ, "PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin")},
    )
    safe_output = redact((proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else ""))
    proof = (
        f"DEALIX_VPS_COMMAND_PROOF\n\n"
        f"- source_comment_id: `{comment_id}`\n"
        f"- command: `{command}`\n"
        f"- started_at: `{started}`\n"
        f"- finished_at: `{now_iso()}`\n"
        f"- exit_code: `{proc.returncode}`\n"
        f"- host: `srv1916256`\n\n"
        f"```text\n{safe_output}\n```"
    )
    pending.update(phase="FINISHED", proof=proof, exit_code=proc.returncode)
    _write_state({**state, "pending": pending})
    return resume_pending()


def drain_queue(*, target: dict[str, Any] | None = None) -> int:
    """Both poll and native events drain in order; native events cannot leapfrog."""
    result = resume_pending()
    if result:
        return result
    state = load_state()
    if target is not None and _comment_id(target["id"]) <= state["last_comment_id"]:
        return 0
    comments = list_comments(since=_since(state["last_created_at"]))
    if target is not None:
        matches = [row for row in comments if row["id"] == target["id"]]
        if not matches:
            raise RuntimeError("BRIDGE_HOLD_EVENT_NOT_VISIBLE")
        current = matches[0]
        if any(current.get(key) != target.get(key) for key in ("body", "created_at")) or (
            current["user"].get("login") != (target.get("user") or {}).get("login")
        ):
            raise RuntimeError("BRIDGE_HOLD_EVENT_CHANGED")
        comments = [row for row in comments if row["id"] <= target["id"]]
    for comment in comments:
        result = execute_comment(comment)
        if result:
            return result
    return 0


def process_native_event() -> int:
    ensure_private_repo()
    if not CONTROL.is_file():
        raise RuntimeError(f"control dispatcher missing: {CONTROL}")

    event_path = Path(os.environ.get("GITHUB_EVENT_PATH", ""))
    if not event_path.is_file():
        raise RuntimeError("GITHUB_EVENT_PATH missing")
    event = json.loads(event_path.read_text(encoding="utf-8"))
    comment = event_comment(event)
    if comment is None:
        print("DEALIX_VPS_NATIVE_EVENT=IGNORED")
        return 0

    command = parse_command(str(comment.get("body") or ""))
    if command is None:
        print("DEALIX_VPS_NATIVE_EVENT=IGNORED_NO_COMMAND")
        return 0

    grace = max(0, int(os.environ.get("DEALIX_NATIVE_EVENT_GRACE_SECONDS", DEFAULT_NATIVE_GRACE_SECONDS)))
    if grace:
        time.sleep(grace)

    with execution_lock():
        result = drain_queue(target=comment)

    print(f"DEALIX_VPS_NATIVE_EVENT=QUEUE_DRAINED exit_code={result}")
    return result


def process_poll_cycle() -> int:
    ensure_private_repo()
    if not CONTROL.is_file():
        raise RuntimeError(f"control dispatcher missing: {CONTROL}")
    with execution_lock():
        return drain_queue()


def main() -> int:
    if "--bootstrap" in sys.argv:
        ensure_private_repo()
        return bootstrap_state()
    if "--event" in sys.argv:
        return process_native_event()
    return process_poll_cycle()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.TimeoutExpired:
        print("BRIDGE_HOLD_TIMEOUT_OUTCOME_UNKNOWN", file=sys.stderr)
        raise SystemExit(124)
    except Exception as exc:
        reason = str(exc) if re.fullmatch(r"BRIDGE_HOLD_[A-Z_]+", str(exc)) else type(exc).__name__
        print(f"bridge blocked: {reason}", file=sys.stderr)
        raise SystemExit(1)
