#!/usr/bin/env python3
"""Render a fail-closed Hermes launcher for the canonical Session Factory."""
from __future__ import annotations

import argparse
import os
import re
import shlex
import tempfile
from pathlib import Path

FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
DEFAULT_REPO = Path("/opt/dealix/workspace/dealix")
DEFAULT_STATE = Path("/opt/dealix/control/state/session_factory")
DEFAULT_LOCK = Path("/home/dealix/.hermes/locks/session-factory.lock")


def validate_sha(value: str) -> str:
    value = value.strip()
    if not FULL_SHA.fullmatch(value):
        raise ValueError("accepted SHA must be an exact 40-character lowercase git SHA")
    return value


def render_launcher(
    accepted_sha: str,
    *,
    repo: Path = DEFAULT_REPO,
    state_dir: Path = DEFAULT_STATE,
    lock_file: Path = DEFAULT_LOCK,
) -> str:
    accepted_sha = validate_sha(accepted_sha)
    repo_q = shlex.quote(str(repo))
    state_q = shlex.quote(str(state_dir))
    lock_q = shlex.quote(str(lock_file))
    return f'''#!/usr/bin/env bash
set -Eeuo pipefail
REPO={repo_q}
EXPECTED_SHA={accepted_sha}
STATE={state_q}
LOCK={lock_q}
PY="$REPO/.venv/bin/python"

actual_sha="$(git -C "$REPO" rev-parse HEAD 2>/dev/null || true)"
if [[ "$actual_sha" != "$EXPECTED_SHA" ]]; then
  echo "DEALIX_HERMES_SESSION_FACTORY=HOLD_SOURCE_IDENTITY" >&2
  echo "EXPECTED_SHA=$EXPECTED_SHA" >&2
  echo "ACTUAL_SHA=${{actual_sha:-UNKNOWN}}" >&2
  exit 75
fi
if [[ -n "$(git -C "$REPO" status --porcelain --untracked-files=no)" ]]; then
  echo "DEALIX_HERMES_SESSION_FACTORY=HOLD_DIRTY_SOURCE" >&2
  exit 75
fi
if [[ ! -x "$PY" ]]; then
  echo "DEALIX_HERMES_SESSION_FACTORY=HOLD_PYTHON_MISSING" >&2
  exit 75
fi
exec 9>"$LOCK"
flock -n 9 || exit 0
watch="$(mktemp)"
rec="$(mktemp)"
tick="$(mktemp)"
stat="$(mktemp)"
trap 'rm -f "$watch" "$rec" "$tick" "$stat"' EXIT

set +e
"$PY" "$REPO/scripts/ops/session_factory_watchdog.py" --state-dir "$STATE" --json >"$watch" 2>&1
wrc=$?
set -e
if [[ "$wrc" -ne 0 ]]; then
  echo "DEALIX_SESSION_FACTORY_WATCHDOG=ALERT"
  cat "$watch"
  exit "$wrc"
fi

"$PY" "$REPO/scripts/ops/session_factory.py" recover --state-dir "$STATE" --json >"$rec"
"$PY" "$REPO/scripts/ops/session_factory.py" tick --state-dir "$STATE" --json >"$tick"
"$PY" "$REPO/scripts/ops/session_factory.py" status --state-dir "$STATE" --json >"$stat"
"$PY" - "$rec" "$tick" "$stat" <<'PY'
import json
import sys
with open(sys.argv[1], encoding="utf-8") as fh:
    recovered_doc = json.load(fh)
with open(sys.argv[2], encoding="utf-8") as fh:
    tick_doc = json.load(fh)
with open(sys.argv[3], encoding="utf-8") as fh:
    status_doc = json.load(fh)

processed = tick_doc.get("processed") or []
recovered = int(recovered_doc.get("count", 0) or 0)
if not processed and not recovered:
    raise SystemExit(0)
print("DEALIX_AUTONOMOUS_DEVELOPMENT_FACTORY=ACTIVE")
print("RECOVERED="+str(recovered))
print("PROCESSED="+str(len(processed)))
for item in processed[:10]:
    print("JOB={{}} STATUS={{}}".format(item.get("JOB_ID"), item.get("status")))
print("ACTIVE_LEASES="+str(status_doc.get("active_leases")))
print("DEEP_WIP_AVAILABLE="+str(status_doc.get("deep_wip_available")))
print("L5_POLICY="+str(status_doc.get("l5_policy")))
PY
'''


def write_output(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp_name, 0o700)
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--accepted-sha", required=True)
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--state-dir", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--lock-file", type=Path, default=DEFAULT_LOCK)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    content = render_launcher(
        args.accepted_sha, repo=args.repo, state_dir=args.state_dir, lock_file=args.lock_file
    )
    if args.output:
        write_output(args.output, content)
        print(f"RENDERED={args.output}")
    else:
        print(content, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
