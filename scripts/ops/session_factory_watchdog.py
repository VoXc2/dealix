#!/usr/bin/env python3
"""DEALIX_SESSION_FACTORY_WATCHDOG — zero-token health probe for the factory.

Deterministic and read-only. Healthy systems stay silent (empty stdout, exit 0).
Only a meaningful failure emits output (exit 1). Intended for a Hermes
``no-agent`` cron job so no model tokens are ever spent monitoring.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

DEFAULT_STATE = Path("/opt/dealix/control/state/session_factory")

FAILURE_SPIKE_WINDOW_S = 3600
FAILURE_SPIKE_THRESHOLD = 5


def _governor_capacity(state_dir: Path) -> int | None:
    """Return the ResourceGovernor's live deep capacity, or None when absent.

    The watchdog never invents capacity authority: without governor state it
    falls back to a conservative legacy-safe default instead of asserting a
    global cap.
    """
    path = state_dir / "RESOURCE_GOVERNOR_STATE.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(payload, dict):
        return None
    try:
        capacity = int(payload.get("max_concurrent_deep"))
    except (TypeError, ValueError):
        return None
    return capacity if capacity > 0 else None


# Conservative monitoring default when no governor state exists. This is not
# runtime capacity authority (ResourceGovernor is); it only bounds alerting.
WATCHDOG_DEFAULT_CAPACITY = 3


def _load(path: Path, default):
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def _all_jobs(state_dir: Path) -> list[dict]:
    directory = state_dir / "jobs"
    if not directory.is_dir():
        return []
    jobs = []
    for path in sorted(directory.glob("*.json")):
        job = _load(path, None)
        if job:
            jobs.append(job)
    return jobs


def evaluate(state_dir: Path, *, now: float | None = None) -> list[dict]:
    """Return a list of findings. Empty list == healthy."""
    now = now if now is not None else time.time()
    findings: list[dict] = []
    jobs = _all_jobs(state_dir)
    jobs_by_id = {job.get("JOB_ID"): job for job in jobs}

    lease_dir = state_dir / "leases"
    if lease_dir.is_dir():
        for path in sorted(lease_dir.glob("*.json")):
            lease = _load(path, None)
            if not lease:
                continue
            expires = lease.get("LEASE_EXPIRES_EPOCH")
            if expires is not None and now >= float(expires):
                findings.append(
                    {
                        "kind": "STUCK_LEASE",
                        "JOB_ID": lease.get("JOB_ID"),
                        "expired_for_s": round(now - float(expires), 1),
                        "owner": lease.get("OWNER"),
                    }
                )

    for job in jobs:
        if job.get("STATUS") not in ("RUNNING", "CLAIMED"):
            continue
        if not job.get("LEASE"):
            findings.append({"kind": "ORPHAN_RUNNER", "JOB_ID": job.get("JOB_ID"), "status": job.get("STATUS")})

    recent_failures = [
        job
        for job in jobs
        if job.get("STATUS") == "FAILED"
        and _is_recent(job.get("UPDATED_AT") or job.get("CREATED_AT"), now)
    ]
    if len(recent_failures) >= FAILURE_SPIKE_THRESHOLD:
        findings.append({"kind": "FAILURE_SPIKE", "count": len(recent_failures), "window_s": FAILURE_SPIKE_WINDOW_S})

    capacity = _governor_capacity(state_dir)
    deep_wip_max = capacity if capacity is not None else WATCHDOG_DEFAULT_CAPACITY
    active = sum(1 for job in jobs if job.get("STATUS") == "RUNNING" and job.get("MODIFYING"))
    if active > deep_wip_max:
        findings.append(
            {
                "kind": "DEEP_WIP_EXCEEDED",
                "active": active,
                "max": deep_wip_max,
                "governor_derived": capacity is not None,
            }
        )

    return findings


def _is_recent(timestamp: str | None, now: float) -> bool:
    if not timestamp:
        return False
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return False
    return (now - parsed.timestamp()) <= FAILURE_SPIKE_WINDOW_S


def render(findings: list[dict]) -> str:
    return "\n".join(f"SESSION_FACTORY_ALERT={json.dumps(item, ensure_ascii=False)}" for item in findings)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Session factory watchdog (zero-token, silent when healthy)")
    parser.add_argument("--state-dir", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    findings = evaluate(args.state_dir)
    if findings:
        print(json.dumps(findings, indent=2, ensure_ascii=False) if args.json else render(findings))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
