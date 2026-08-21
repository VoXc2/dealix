#!/usr/bin/env python3
"""Private GitHub Issue -> Dealix VPS allowlisted command bridge.

Security model:
- repository must be private
- only comments authored by the configured founder login are considered
- command must be an exact `!dealix <allowlisted-command>` line
- no arbitrary shell evaluation
- no L5 operations
- command output is redacted and capped before it is posted back to GitHub
- state prevents replay of old comments
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO = "Dealix-sa/dealix"
ISSUE = 1119
FOUNDER = "VoXc2"
PREFIX = "!dealix "
CONTROL = Path("/opt/dealix/control/bin/dealix_vps_control.sh")
STATE = Path("/opt/dealix/control/state/issue_bridge.json")
MAX_OUTPUT_CHARS = 6000

ALLOWED = {
    "status",
    "repo-inspect",
    "verify",
    "autonomous-dry-run",
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


def load_state() -> dict[str, Any]:
    if not STATE.exists():
        return {"last_comment_id": 0, "last_created_at": "1970-01-01T00:00:00Z"}
    try:
        payload = json.loads(STATE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"last_comment_id": 0, "last_created_at": "1970-01-01T00:00:00Z"}
    return {
        "last_comment_id": int(payload.get("last_comment_id") or 0),
        "last_created_at": str(payload.get("last_created_at") or "1970-01-01T00:00:00Z"),
    }


def save_state(comment_id: int, created_at: str) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(
        json.dumps(
            {
                "last_comment_id": int(comment_id),
                "last_created_at": created_at,
                "updated_at": now_iso(),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, STATE)


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


def bootstrap_state() -> int:
    comments = gh_json(f"repos/{REPO}/issues/{ISSUE}/comments?per_page=100")
    if comments:
        latest = comments[-1]
        save_state(int(latest["id"]), str(latest["created_at"]))
    else:
        save_state(0, now_iso())
    return 0


def main() -> int:
    ensure_private_repo()
    if not CONTROL.is_file():
        raise RuntimeError(f"control dispatcher missing: {CONTROL}")

    if "--bootstrap" in sys.argv:
        return bootstrap_state()

    state = load_state()
    last_id = int(state["last_comment_id"])
    since = str(state["last_created_at"])
    comments = gh_json(
        f"repos/{REPO}/issues/{ISSUE}/comments?per_page=100&since={since}"
    )

    for comment in comments:
        comment_id = int(comment.get("id") or 0)
        created_at = str(comment.get("created_at") or now_iso())
        if comment_id <= last_id:
            continue

        author = str((comment.get("user") or {}).get("login") or "")
        body = str(comment.get("body") or "")
        command = parse_command(body)

        if author == FOUNDER and command == "__DENIED__":
            gh_comment(
                "DENIED: unsupported Dealix VPS command. "
                "Only the private bridge allowlist may execute."
            )
        elif author == FOUNDER and command:
            started = now_iso()
            proc = subprocess.run(
                [str(CONTROL), command],
                text=True,
                capture_output=True,
                check=False,
                timeout=3300,
                env={**os.environ, "PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin")},
            )
            finished = now_iso()
            safe_output = redact((proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else ""))
            proof = (
                f"DEALIX_VPS_COMMAND_PROOF\n\n"
                f"- source_comment_id: `{comment_id}`\n"
                f"- command: `{command}`\n"
                f"- started_at: `{started}`\n"
                f"- finished_at: `{finished}`\n"
                f"- exit_code: `{proc.returncode}`\n"
                f"- host: `srv1916256`\n\n"
                f"```text\n{safe_output}\n```"
            )
            gh_comment(proof)

        save_state(comment_id, created_at)
        last_id = comment_id

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.TimeoutExpired as exc:
        print(f"bridge timeout: {exc}", file=sys.stderr)
        raise SystemExit(124)
    except Exception as exc:
        print(f"bridge blocked: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
