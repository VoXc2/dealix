#!/usr/bin/env python3
"""Dealix Founder OS / Hermes Agents worker.

Production-safe behavior:
- Runs diagnostics repeatedly.
- Keeps Railway worker alive 24/7.
- Never sends external outreach automatically.
- Never performs destructive actions.
- Approval mode is required by default.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTERVAL_SECONDS = int(os.getenv("FOUNDER_OS_INTERVAL_SECONDS", "900"))
APPROVAL_MODE = os.getenv("AGENT_APPROVAL_MODE", "required").lower()

COMMANDS = [
    [sys.executable, "scripts/dealix_status.py"],
    [sys.executable, "scripts/dealix_morning_digest.py", "--print"],
    [sys.executable, "scripts/verify_reference_library_70.py"],
]


def run_command(cmd: list[str]) -> dict[str, object]:
    started = time.time()
    script_path = ROOT / cmd[1]
    if not script_path.exists():
        return {"cmd": cmd, "skipped": "file_not_found"}

    try:
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=240,
            env={
                **os.environ,
                "PYTHONUTF8": "1",
                "PYTHONIOENCODING": "utf-8",
                "AUTO_SEND_ENABLED": os.getenv("AUTO_SEND_ENABLED", "false"),
                "EXTERNAL_OUTREACH_ENABLED": os.getenv("EXTERNAL_OUTREACH_ENABLED", "false"),
                "AGENT_APPROVAL_MODE": APPROVAL_MODE,
            },
        )
        return {
            "cmd": cmd,
            "returncode": proc.returncode,
            "latency_ms": round((time.time() - started) * 1000),
            "stdout_tail": proc.stdout[-4000:],
            "stderr_tail": proc.stderr[-4000:],
        }
    except Exception as exc:
        return {"cmd": cmd, "error": repr(exc), "latency_ms": round((time.time() - started) * 1000)}


def founder_cycle() -> dict[str, object]:
    return {
        "service": "founder-os-worker",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "approval_mode": APPROVAL_MODE,
        "external_actions_allowed": False,
        "auto_send_enabled": os.getenv("AUTO_SEND_ENABLED", "false"),
        "results": [run_command(cmd) for cmd in COMMANDS],
    }


def main() -> int:
    print(json.dumps({
        "service": "founder-os-worker",
        "status": "started",
        "interval_seconds": INTERVAL_SECONDS,
        "approval_mode": APPROVAL_MODE,
        "external_actions_allowed": False,
    }, ensure_ascii=False), flush=True)

    while True:
        print(json.dumps(founder_cycle(), ensure_ascii=False, indent=2), flush=True)
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    raise SystemExit(main())
