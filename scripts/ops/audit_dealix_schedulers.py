#!/usr/bin/env python3
"""Deterministic Dealix scheduler audit — one job, one owner (read-only, no LLM).

Inventories systemd timers and Hermes cron jobs, then reports duplicate
scheduling paths and possible responsibility overlaps. Never mutates schedulers.
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import re
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]

_RESPONSIBILITY_KEYWORDS = ("watch", "scan", "audit", "proof", "recovery", "dispatch", "bridge", "cycle", "brief")

# Hermes jobs live under the invoking Unix identity's HOME (~/.hermes). The
# canonical Dealix cron owner is `dealix`; audit must locate that identity's
# installation even when run as root (otherwise HERMES_CRON falsely reports 0).
_HERMES_BIN_CANDIDATES = (
    Path("/home/dealix/.local/bin/hermes"),
    Path("/root/.local/bin/hermes"),
)
_HERMES_OWNER_CANDIDATES = ("dealix",)

_HERMES_JOB_RE = re.compile(
    r"Name:\s*(?P<name>.+?)\n\s*Schedule:\s*(?P<schedule>.+?)\n.*?Script:\s*(?P<script>\S+)",
    re.DOTALL,
)


def parse_hermes_cron(text: str) -> list[dict[str, str]]:
    jobs: list[dict[str, str]] = []
    for match in _HERMES_JOB_RE.finditer(text):
        jobs.append(
            {
                "owner": "hermes",
                "name": match.group("name").strip(),
                "schedule": match.group("schedule").strip(),
                "target": match.group("script").strip(),
            }
        )
    return jobs


def parse_exec_start(exec_line: str) -> str:
    match = re.search(r"argv\[\]=(?P<argv>[^;]+)", exec_line)
    if match:
        return match.group("argv").strip()
    match = re.search(r"path=(?P<path>[^;]+)", exec_line)
    if match:
        return match.group("path").strip()
    return "UNKNOWN"


def job_basename(target: str) -> str:
    return Path(target).name if target and target != "UNKNOWN" else "UNKNOWN"


def find_duplicate_targets(jobs: list[dict[str, str]]) -> list[dict[str, Any]]:
    seen: dict[str, list[str]] = {}
    for job in jobs:
        seen.setdefault(job_basename(job.get("target", "UNKNOWN")), []).append(job.get("name", "UNKNOWN"))
    return [
        {"target": target, "owners": names}
        for target, names in sorted(seen.items())
        if len(names) > 1 and target != "UNKNOWN"
    ]


def find_overlap_candidates(jobs: list[dict[str, str]]) -> list[dict[str, Any]]:
    by_keyword: dict[str, list[str]] = {}
    for job in jobs:
        haystack = f"{job.get('name', '')} {job_basename(job.get('target', ''))}".lower()
        for keyword in _RESPONSIBILITY_KEYWORDS:
            if keyword in haystack:
                by_keyword.setdefault(keyword, []).append(job.get("name", "UNKNOWN"))
    return [
        {"keyword": keyword, "jobs": names}
        for keyword, names in sorted(by_keyword.items())
        if len(names) > 1
    ]


def _run(cmd: list[str], timeout: int = 20) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
        return result.stdout
    except (OSError, subprocess.TimeoutExpired):
        return ""


def resolve_hermes_bin() -> str | None:
    """Locate the hermes CLI on PATH or at the canonical per-identity install."""
    found = shutil.which("hermes")
    if found:
        return found
    for candidate in _HERMES_BIN_CANDIDATES:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


def resolve_hermes_owner() -> str | None:
    """Return the Unix identity whose ~/.hermes holds the canonical cron jobs.

    Honors DEALIX_HERMES_USER as an explicit override, then prefers the
    canonical `dealix` identity when running as root so a root audit does not
    silently read /root/.hermes and report zero jobs.
    """
    override = os.environ.get("DEALIX_HERMES_USER", "").strip()
    if override:
        return override
    if os.geteuid() == 0:
        try:
            import pwd

            for name in _HERMES_OWNER_CANDIDATES:
                try:
                    pwd.getpwnam(name)
                    return name
                except KeyError:
                    continue
        except ImportError:
            return None
    return None


def build_hermes_command(hermes_bin: str) -> list[str]:
    """Build a cron-list command, switching identity only when required."""
    owner = resolve_hermes_owner()
    if owner and owner != getpass.getuser() and shutil.which("sudo"):
        return ["sudo", "-n", "-u", owner, "-H", hermes_bin, "cron", "list"]
    return [hermes_bin, "cron", "list"]


def inventory_hermes() -> list[dict[str, str]]:
    hermes_bin = resolve_hermes_bin()
    if not hermes_bin:
        return []
    return parse_hermes_cron(_run(build_hermes_command(hermes_bin), timeout=30))


def inventory_systemd() -> list[dict[str, str]]:
    if not shutil.which("systemctl"):
        return []
    units_raw = _run(["systemctl", "list-units", "dealix-*.timer", "--all", "--plain", "--no-legend", "--no-pager"])
    jobs: list[dict[str, str]] = []
    for line in units_raw.splitlines():
        fields = line.split()
        if not fields or not fields[0].endswith(".timer"):
            continue
        timer = fields[0]
        service_raw = _run(["systemctl", "show", timer, "-p", "Unit", "-p", "NextElapseUSecRealtime"])
        service = "UNKNOWN"
        schedule = "UNKNOWN"
        for prop in service_raw.splitlines():
            if prop.startswith("Unit="):
                service = prop.split("=", 1)[1].strip()
            elif prop.startswith("NextElapseUSecRealtime="):
                schedule = prop.split("=", 1)[1].strip() or "UNKNOWN"
        exec_start = parse_exec_start(_run(["systemctl", "show", service, "-p", "ExecStart"])) if service != "UNKNOWN" else "UNKNOWN"
        jobs.append({"owner": "systemd", "name": f"{timer} -> {service}", "schedule": schedule, "target": exec_start})
    return jobs


def build_audit(jobs: list[dict[str, str]]) -> dict[str, Any]:
    duplicates = find_duplicate_targets(jobs)
    overlaps = find_overlap_candidates(jobs)
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "systemd_timers": len([job for job in jobs if job["owner"] == "systemd"]),
        "hermes_cron": len([job for job in jobs if job["owner"] == "hermes"]),
        "jobs": jobs,
        "duplicate_targets": duplicates,
        "overlap_candidates": overlaps,
        "verdict": "WARN" if duplicates else "PASS",
    }


def render_audit(audit: dict[str, Any]) -> str:
    lines = [
        f"DEALIX_SCHEDULER_AUDIT={audit['verdict']}",
        f"SYSTEMD_TIMERS={audit['systemd_timers']}",
        f"HERMES_CRON={audit['hermes_cron']}",
        f"TOTAL_JOBS={len(audit['jobs'])}",
    ]
    for duplicate in audit["duplicate_targets"]:
        lines.append(f"DUPLICATE_TARGET={duplicate['target']} owners={duplicate['owners']}")
    for overlap in audit["overlap_candidates"]:
        lines.append(f"OVERLAP_KEYWORD={overlap['keyword']} jobs={overlap['jobs']}")
    for job in audit["jobs"]:
        lines.append(f"JOB[{job['owner']}] {job['name']} | {job['schedule']} | {job['target']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix scheduler audit (read-only)")
    parser.add_argument("--json", type=Path, default=None, help="Write JSON report to this path")
    args = parser.parse_args()

    jobs = inventory_systemd() + inventory_hermes()
    audit = build_audit(jobs)
    print(render_audit(audit))
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"WROTE {args.json}")
    return 0 if audit["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
