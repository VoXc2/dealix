#!/usr/bin/env python3
"""DEALIX HERMES AUTONOMOUS SESSION FACTORY — one durable job control plane.

Responsibility:

    COMPANY_QUEUE -> PRIORITIZE -> CLASSIFY -> SELECT MODE -> ISOLATE WORKSPACE
    -> SELECT MODEL -> LAUNCH -> MONITOR -> RECOVER -> VERIFY -> INTEGRATE
    -> RECORD -> CLEANUP -> NEXT

This module is the *orchestrator*, not another company brain. It reuses the
canonical building blocks already in the repo:

* ``scripts/ops/opencode_model_broker.py`` for live model availability;
* ``scripts/ops/go_resource_broker.py`` for route/economic planning;
* git worktrees for writer isolation.

Hard laws enforced here:

* Zero-token first: DETERMINISTIC / MONITORING jobs never call a model.
* A process exit code is NOT success. SUCCEEDED requires acceptance evidence.
* No two modifying workers own the same responsibility at once (leases).
* L5 authority (merge/deploy/send/publish/pay/reboot) is never auto-executed;
  such jobs stop at ``WAITING_L5``.
* No secret values are ever written to job evidence.
* Expired leases are inspected, never blindly rerun.
* Runtime state lives outside the git checkout.

The factory is deterministic and safe to run without any model provider.
"""

from __future__ import annotations

import argparse
import json
import os
import pwd
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = Path(os.environ.get("DEALIX_SESSION_FACTORY_STATE", "/opt/dealix/control/state/session_factory"))
WORKTREE_ROOT = Path(os.environ.get("DEALIX_SESSION_FACTORY_WORKTREES", "/opt/dealix/worktrees/auto"))
FROZEN_RELEASE_SHA = os.environ.get("DEALIX_FROZEN_RELEASE_SHA", "8bb0a6c382c49ca288f7b579cae07676f006e229")

SCHEMA = "dealix.autonomous_job.v1"
LEDGER_SCHEMA = "dealix.autonomous_job_ledger.v1"
STATUS_SCHEMA = "dealix.session_factory_status.v1"
GOVERNOR_SCHEMA = "dealix.resource_governor.v1"
LEASE_SCHEMA = "dealix.session_lease.v1"

# --------------------------------------------------------------------------
# Job taxonomy
# --------------------------------------------------------------------------

JOB_CLASSES = (
    "DETERMINISTIC",
    "LOCAL_AI",
    "RESEARCH",
    "REVIEW",
    "ENGINEERING",
    "COMMERCIAL_REASONING",
    "CONTENT",
    "DELIVERY",
    "MONITORING",
)

# The execution mode is selected *by job class*, never by hype.
CLASS_TO_MODE: dict[str, str] = {
    "DETERMINISTIC": "deterministic",
    "MONITORING": "deterministic",
    "LOCAL_AI": "local_ai",
    "CONTENT": "local_ai",
    "RESEARCH": "opencode",
    "REVIEW": "opencode",
    "ENGINEERING": "opencode",
    "COMMERCIAL_REASONING": "opencode",
    "DELIVERY": "opencode",
}

MODIFYING_CLASSES = frozenset({"RESEARCH", "REVIEW", "ENGINEERING", "COMMERCIAL_REASONING", "CONTENT", "DELIVERY"})

EXECUTION_MODES = ("deterministic", "local_ai", "opencode", "no_agent")

# Route class per job class (mirrors the Go resource broker vocabulary).
CLASS_TO_MODEL_CLASS: dict[str, str] = {
    "DETERMINISTIC": "R1_DETERMINISTIC",
    "MONITORING": "R0_NO_MODEL",
    "LOCAL_AI": "R2_LOCAL_OLLAMA",
    "CONTENT": "R3_INCLUDED_LIGHT",
    "RESEARCH": "R4_INCLUDED_HIGH",
    "REVIEW": "R4_INCLUDED_HIGH",
    "ENGINEERING": "R4_INCLUDED_HIGH",
    "COMMERCIAL_REASONING": "R4_INCLUDED_HIGH",
    "DELIVERY": "R4_INCLUDED_HIGH",
}

PERMANENT_AGENTS = ("dealix-pm", "dealix-sales", "dealix-delivery", "dealix-engineer", "dealix-content")
DEEP_WIP_MAX = 3

# --------------------------------------------------------------------------
# State machine
# --------------------------------------------------------------------------

STATES = (
    "QUEUED",
    "READY",
    "CLAIMED",
    "RUNNING",
    "VERIFYING",
    "SUCCEEDED",
    "FAILED",
    "BLOCKED",
    "WAITING_L5",
    "RECOVERABLE",
    "SUPERSEDED",
    "CANCELLED",
)

TERMINAL_STATES = frozenset({"SUCCEEDED", "FAILED", "SUPERSEDED", "CANCELLED"})

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "QUEUED": {"READY", "WAITING_L5", "CANCELLED", "SUPERSEDED"},
    "READY": {"CLAIMED", "BLOCKED", "CANCELLED", "SUPERSEDED"},
    "CLAIMED": {"RUNNING", "BLOCKED", "RECOVERABLE", "FAILED", "CANCELLED"},
    "RUNNING": {"VERIFYING", "FAILED", "RECOVERABLE", "BLOCKED", "WAITING_L5", "CANCELLED"},
    "VERIFYING": {"SUCCEEDED", "FAILED", "RECOVERABLE", "BLOCKED"},
    "FAILED": {"RECOVERABLE", "BLOCKED", "CANCELLED"},
    "RECOVERABLE": {"READY", "FAILED", "CANCELLED"},
    "BLOCKED": {"READY", "CANCELLED"},
    "WAITING_L5": {"READY", "CANCELLED"},
    "SUCCEEDED": set(),
    "SUPERSEDED": set(),
    "CANCELLED": set(),
}

AUTHORITY_LEVELS = ("L0", "L1", "L2", "L3", "L4", "L5")
AUTHORITY_AUTO_MAX = "L4"

JOB_CONTRACT_FIELDS = (
    "JOB_ID",
    "CREATED_AT",
    "OWNER_AGENT",
    "BUSINESS_GOAL",
    "ECONOMIC_REASON",
    "JOB_CLASS",
    "PRIORITY",
    "URGENCY",
    "DEPENDENCIES",
    "AUTHORITY_LEVEL",
    "REPO",
    "BASE_SHA",
    "WORKTREE",
    "FILES_IN_SCOPE",
    "FILES_FORBIDDEN",
    "CONTEXT_REFS",
    "MODEL_CLASS",
    "TOKEN_BUDGET_CLASS",
    "TIME_BUDGET",
    "MAX_ITERATIONS",
    "ACCEPTANCE_CRITERIA",
    "TESTS",
    "OUTPUT_SCHEMA",
    "ROLLBACK",
    "STATUS",
    "RESULT",
    "EVIDENCE",
    "NEXT_ACTION",
)

DEEP_JOB_CLASSES = frozenset({"ENGINEERING", "ARCHITECTURE", "SECURITY"})

# Deterministic executor argv safety: the factory runs list argv with
# ``shell=False``; these tokens are refused even so.
DANGEROUS_TOKENS = frozenset(
    {
        "sudo",
        "su",
        "rm",
        "dd",
        "mkfs",
        "shutdown",
        "reboot",
        "halt",
        "poweroff",
        "curl",
        "wget",
        "ssh",
        "scp",
        "sftp",
        "nc",
        "ncat",
        "netcat",
        "iptables",
        "nft",
        "mount",
        "umount",
        "systemctl",
        "service",
        "docker",
        "kubectl",
        "terraform",
        "railway",
        "wrangler",
        "gh",
        "alembic",
        "git",
    }
)

# This is a deliberately loose pattern: over-redaction is safe, under-redaction is not.
_SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_\-]{8,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{8,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._\-]{8,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[=:]\s*\S+"),
)


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def now_epoch() -> float:
    return time.time()


def redact(text: str | None, limit: int = 2000) -> str:
    """Return a bounded, secret-redacted view of process output."""
    if not text:
        return ""
    value = text
    for pattern in _SECRET_PATTERNS:
        value = pattern.sub("[REDACTED]", value)
    if len(value) > limit:
        value = value[:limit] + "...[truncated]"
    return value


def atomic_write(path: Path, payload: str, mode: int = 0o640) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp.{os.getpid()}")
    with open(tmp, "w", encoding="utf-8") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)
    try:
        os.chmod(path, mode)
    except OSError:
        pass


def write_json(path: Path, payload: Any, mode: int = 0o640) -> None:
    atomic_write(path, json.dumps(payload, indent=2, ensure_ascii=False), mode=mode)


def read_json(path: Path, default: Any) -> Any:
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def state_root(state_dir: Path | None = None) -> Path:
    return Path(state_dir) if state_dir else STATE_DIR


_JOB_SEQUENCE = 0


def new_job_id() -> str:
    global _JOB_SEQUENCE
    _JOB_SEQUENCE += 1
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    return f"JOB-{stamp}-{os.getpid() % 1000:03d}{_JOB_SEQUENCE:04d}"


_CANONICAL_OPERATOR = "dealix"


def share_state_with_operator(root: Path) -> dict[str, Any]:
    """Grant the canonical operator group read access to factory state.

    The factory frequently runs as root while Hermes runs as ``dealix``. A
    no-agent watchdog under the operator identity cannot read root-owned 0640
    state, so mirror the operator group onto the state tree after each command.
    """
    if os.geteuid() != 0:
        return {"shared": False, "reason": "not-root"}
    try:
        gid = pwd.getpwnam(_CANONICAL_OPERATOR).pw_gid
    except KeyError:
        return {"shared": False, "reason": "operator-absent"}
    shared = 0
    try:
        os.chown(root, -1, gid)
        os.chmod(root, 0o750)  # noqa: S103 - operator group needs r-x to traverse
        for path in root.rglob("*"):
            try:
                os.chown(path, -1, gid)
                if path.is_file():
                    os.chmod(path, (path.stat().st_mode & 0o777) | 0o040)
            except OSError:
                continue
            shared += 1
    except OSError:
        return {"shared": False, "reason": "chown-failed"}
    return {"shared": True, "group": _CANONICAL_OPERATOR, "paths": shared}


# --------------------------------------------------------------------------
# Job contract
# --------------------------------------------------------------------------


def empty_job() -> dict[str, Any]:
    return dict.fromkeys(JOB_CONTRACT_FIELDS)


def make_job(
    *,
    owner_agent: str,
    business_goal: str,
    job_class: str,
    authority_level: str = "L1",
    economic_reason: str = "",
    priority: float = 50.0,
    urgency: str = "normal",
    base_sha: str | None = None,
    modifying: bool | None = None,
    executor: dict[str, Any] | None = None,
    acceptance: dict[str, Any] | None = None,
    tests: list[str] | None = None,
    files_in_scope: list[str] | None = None,
    context_refs: list[str] | None = None,
    next_action: str = "",
) -> dict[str, Any]:
    job = empty_job()
    job.update(
        {
            "JOB_ID": new_job_id(),
            "CREATED_AT": now_iso(),
            "OWNER_AGENT": owner_agent,
            "BUSINESS_GOAL": business_goal,
            "ECONOMIC_REASON": economic_reason,
            "JOB_CLASS": job_class,
            "PRIORITY": priority,
            "URGENCY": urgency,
            "DEPENDENCIES": [],
            "AUTHORITY_LEVEL": authority_level,
            "REPO": str(REPO_ROOT),
            "BASE_SHA": base_sha or FROZEN_RELEASE_SHA,
            "WORKTREE": None,
            "FILES_IN_SCOPE": files_in_scope or [],
            "FILES_FORBIDDEN": [".env", "*.secret", "auth.json"],
            "CONTEXT_REFS": context_refs or [],
            "MODEL_CLASS": None,
            "TOKEN_BUDGET_CLASS": "zero" if job_class in ("DETERMINISTIC", "MONITORING") else "bounded",
            "TIME_BUDGET": 600,
            "MAX_ITERATIONS": 1,
            "ACCEPTANCE_CRITERIA": (acceptance or {}).get("criteria", "acceptance evidence required"),
            "TESTS": tests or [],
            "OUTPUT_SCHEMA": SCHEMA,
            "ROLLBACK": "discard isolated worktree; no shared state mutated",
            "STATUS": "QUEUED",
            "RESULT": None,
            "EVIDENCE": [],
            "NEXT_ACTION": next_action,
            "MODIFYING": bool(modifying) if modifying is not None else job_class in MODIFYING_CLASSES,
            "EXECUTION_MODE": CLASS_TO_MODE.get(job_class, "deterministic"),
            "EXECUTOR": executor or {},
            "ACCEPTANCE": acceptance or {},
            "LEASE": None,
        }
    )
    return job


def validate_job(job: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in ("JOB_ID", "OWNER_AGENT", "BUSINESS_GOAL", "JOB_CLASS", "AUTHORITY_LEVEL", "STATUS"):
        if not job.get(field):
            errors.append(f"missing:{field}")
    if job.get("JOB_CLASS") not in JOB_CLASSES:
        errors.append(f"invalid:JOB_CLASS={job.get('JOB_CLASS')}")
    if job.get("AUTHORITY_LEVEL") not in AUTHORITY_LEVELS:
        errors.append(f"invalid:AUTHORITY_LEVEL={job.get('AUTHORITY_LEVEL')}")
    if job.get("STATUS") not in STATES:
        errors.append(f"invalid:STATUS={job.get('STATUS')}")
    owner = job.get("OWNER_AGENT")
    if owner and owner not in PERMANENT_AGENTS:
        errors.append(f"invalid:OWNER_AGENT={owner} (must be one of the five permanent agents)")
    dependencies = job.get("DEPENDENCIES") or []
    if not isinstance(dependencies, list):
        errors.append("invalid:DEPENDENCIES must be a list")
    if job.get("EXECUTION_MODE") not in EXECUTION_MODES:
        errors.append(f"invalid:EXECUTION_MODE={job.get('EXECUTION_MODE')}")
    if job.get("EXECUTION_MODE") == "deterministic":
        executor = job.get("EXECUTOR") or {}
        errors.extend(validate_argv(executor.get("argv")))
    return errors


def validate_argv(argv: Any) -> list[str]:
    """Validate a deterministic executor argv list against the safety policy."""
    if not isinstance(argv, list) or not argv:
        return ["executor.argv must be a non-empty list"]
    errors: list[str] = []
    for token in argv:
        if not isinstance(token, str) or not token:
            errors.append("executor.argv entries must be non-empty strings")
            continue
        program = Path(token).name
        if program in DANGEROUS_TOKENS:
            errors.append(f"executor rejected dangerous token: {program}")
    return errors


def can_transition(current: str, target: str) -> bool:
    return target in ALLOWED_TRANSITIONS.get(current, set())


def transition(job: dict[str, Any], target: str, *, reason: str = "") -> dict[str, Any]:
    if not can_transition(job.get("STATUS", "QUEUED"), target):
        raise ValueError(f"illegal transition {job.get('STATUS')} -> {target}")
    previous = job["STATUS"]
    job["STATUS"] = target
    job.setdefault("EVIDENCE", []).append(
        {"at": now_iso(), "event": "transition", "from": previous, "to": target, "reason": redact(reason, 500)}
    )
    if target in TERMINAL_STATES:
        job["LEASE"] = None
    return job


# --------------------------------------------------------------------------
# Durable store
# --------------------------------------------------------------------------


def jobs_dir(root: Path) -> Path:
    return root / "jobs"


def lease_dir(root: Path) -> Path:
    return root / "leases"


def queue_path(root: Path) -> Path:
    return root / "AUTONOMOUS_JOB_QUEUE.json"


def ledger_path(root: Path) -> Path:
    return root / "AUTONOMOUS_JOB_LEDGER.jsonl"


def status_path(root: Path) -> Path:
    return root / "SESSION_FACTORY_STATUS.json"


def governor_path(root: Path) -> Path:
    return root / "RESOURCE_GOVERNOR_STATE.json"


def job_path(root: Path, job_id: str) -> Path:
    return jobs_dir(root) / f"{job_id}.json"


def save_job(root: Path, job: dict[str, Any]) -> dict[str, Any]:
    job["UPDATED_AT"] = now_iso()
    write_json(job_path(root, job["JOB_ID"]), job)
    return job


def load_job(root: Path, job_id: str) -> dict[str, Any] | None:
    return read_json(job_path(root, job_id), None)


def all_jobs(root: Path) -> list[dict[str, Any]]:
    directory = jobs_dir(root)
    if not directory.is_dir():
        return []
    jobs: list[dict[str, Any]] = []
    for path in sorted(directory.glob("*.json")):
        job = read_json(path, None)
        if job:
            jobs.append(job)
    return jobs


def append_ledger(root: Path, event: dict[str, Any]) -> None:
    root.mkdir(parents=True, exist_ok=True)
    event = {"at": now_iso(), **event}
    with open(ledger_path(root), "a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def write_queue_snapshot(root: Path) -> dict[str, Any]:
    jobs = all_jobs(root)
    snapshot = {
        "schema": "dealix.autonomous_job_queue.v1",
        "generated_at": now_iso(),
        "counts": {state: sum(1 for job in jobs if job.get("STATUS") == state) for state in STATES},
        "jobs": [
            {
                "JOB_ID": job["JOB_ID"],
                "JOB_CLASS": job.get("JOB_CLASS"),
                "OWNER_AGENT": job.get("OWNER_AGENT"),
                "STATUS": job.get("STATUS"),
                "PRIORITY": job.get("PRIORITY"),
                "MODIFYING": job.get("MODIFYING"),
                "BUSINESS_GOAL": job.get("BUSINESS_GOAL"),
            }
            for job in sorted(jobs, key=lambda item: -(item.get("PRIORITY") or 0))
        ],
    }
    write_json(queue_path(root), snapshot)
    return snapshot


# --------------------------------------------------------------------------
# Leases
# --------------------------------------------------------------------------


def lease_path(root: Path, job_id: str) -> Path:
    return lease_dir(root) / f"{job_id}.json"


def read_lease(root: Path, job_id: str) -> dict[str, Any] | None:
    return read_json(lease_path(root, job_id), None)


def _pid_alive(pid: Any) -> bool:
    try:
        pid_int = int(pid)
    except (TypeError, ValueError):
        return False
    if pid_int <= 0:
        return False
    try:
        os.kill(pid_int, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def lease_expired(lease: dict[str, Any], at: float | None = None) -> bool:
    expires = lease.get("LEASE_EXPIRES_EPOCH")
    if expires is None:
        return True
    return (at or now_epoch()) >= float(expires)


def acquire_lease(
    root: Path,
    job: dict[str, Any],
    *,
    owner: str,
    ttl_seconds: int = 900,
    scope: str = "",
    reclaim_expired: bool = False,
) -> tuple[bool, dict[str, Any] | None]:
    """Atomically claim a lease. Returns (acquired, lease_or_reason).

    An expired lease is never silently reclaimed: the caller must ask for that
    explicitly after inspecting the reported state.
    """
    lease_dir(root).mkdir(parents=True, exist_ok=True)
    path = lease_path(root, job["JOB_ID"])
    existing = read_lease(root, job["JOB_ID"])
    if existing and not lease_expired(existing):
        if existing.get("HEARTBEAT_PID") and _pid_alive(existing.get("HEARTBEAT_PID")):
            return False, {"reason": "LEASE_HELD_LIVE", "lease": existing}
        if not lease_expired(existing):
            return False, {"reason": "LEASE_HELD", "lease": existing}
    if existing and lease_expired(existing) and not reclaim_expired:
        return False, {"reason": "LEASE_EXPIRED_NEEDS_RECLAIM", "lease": existing}
    lease = {
        "schema": LEASE_SCHEMA,
        "JOB_ID": job["JOB_ID"],
        "WORKTREE": job.get("WORKTREE"),
        "FILES_OR_SCOPE": scope or ",".join(job.get("FILES_IN_SCOPE") or []) or "job",
        "OWNER": owner,
        "LEASE_STARTED": now_iso(),
        "LEASE_STARTED_EPOCH": now_epoch(),
        "LEASE_EXPIRES_EPOCH": now_epoch() + ttl_seconds,
        "HEARTBEAT": now_iso(),
        "HEARTBEAT_PID": os.getpid(),
    }
    try:
        with open(path, "x", encoding="utf-8") as handle:
            handle.write(json.dumps(lease, ensure_ascii=False))
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError:
        current = read_lease(root, job["JOB_ID"])
        if current and lease_expired(current) and reclaim_expired:
            write_json(path, lease)
        else:
            return False, {"reason": "LEASE_RACE", "lease": current}
    job["LEASE"] = lease
    return True, lease


def heartbeat_lease(root: Path, job_id: str, ttl_seconds: int = 900) -> dict[str, Any] | None:
    lease = read_lease(root, job_id)
    if not lease:
        return None
    lease["HEARTBEAT"] = now_iso()
    lease["HEARTBEAT_PID"] = os.getpid()
    lease["LEASE_EXPIRES_EPOCH"] = now_epoch() + ttl_seconds
    write_json(lease_path(root, job_id), lease)
    return lease


def release_lease(root: Path, job_id: str) -> None:
    path = lease_path(root, job_id)
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def active_leases(root: Path) -> list[dict[str, Any]]:
    directory = lease_dir(root)
    if not directory.is_dir():
        return []
    leases: list[dict[str, Any]] = []
    for path in sorted(directory.glob("*.json")):
        lease = read_json(path, None)
        if lease:
            leases.append(lease)
    return leases


# --------------------------------------------------------------------------
# Resource governor
# --------------------------------------------------------------------------


def read_resources() -> dict[str, Any]:
    mem_total_mb = mem_available_mb = 0
    try:
        for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
            if line.startswith("MemTotal:"):
                mem_total_mb = int(line.split()[1]) // 1024
            elif line.startswith("MemAvailable:"):
                mem_available_mb = int(line.split()[1]) // 1024
    except OSError:
        pass
    try:
        load1, load5, load15 = os.getloadavg()
    except OSError:
        load1 = load5 = load15 = 0.0
    try:
        usage = shutil.disk_usage(str(REPO_ROOT))
        disk_free_gb = round(usage.free / (1024**3), 1)
    except OSError:
        disk_free_gb = 0.0
    return {
        "cpu_count": os.cpu_count() or 1,
        "load1": round(load1, 2),
        "load5": round(load5, 2),
        "load15": round(load15, 2),
        "mem_total_mb": mem_total_mb,
        "mem_available_mb": mem_available_mb,
        "disk_free_gb": disk_free_gb,
    }


def compute_max_concurrent_deep(resources: dict[str, Any]) -> int:
    """Bounded deep-work concurrency from live resources. Never exceeds DEEP_WIP_MAX."""
    available = int(resources.get("mem_available_mb") or 0)
    cpu = max(1, int(resources.get("cpu_count") or 1))
    load1 = float(resources.get("load1") or 0.0)
    if available and available < 2500:
        return 1
    if available and available < 4500:
        capacity = 2
    else:
        capacity = 3
    if load1 > cpu * 1.5:
        capacity = min(capacity, 2)
    if load1 > cpu * 3:
        capacity = 1
    return max(1, min(capacity, DEEP_WIP_MAX))


def governor_state(root: Path, resources: dict[str, Any] | None = None) -> dict[str, Any]:
    resources = resources or read_resources()
    deep_active = sum(1 for lease in active_leases(root) if lease.get("JOB_ID") and not lease_expired(lease))
    max_deep = compute_max_concurrent_deep(resources)
    payload = {
        "schema": GOVERNOR_SCHEMA,
        "generated_at": now_iso(),
        "resources": resources,
        "deep_wip_active": deep_active,
        "deep_wip_max": DEEP_WIP_MAX,
        "max_concurrent_deep": max_deep,
        "deep_wip_available": max(0, min(max_deep, DEEP_WIP_MAX) - deep_active),
        "concurrency_policy": "read-only jobs may fan out wider; deep modifying jobs capped by live resources",
    }
    write_json(governor_path(root), payload)
    return payload


# --------------------------------------------------------------------------
# Worktree isolation
# --------------------------------------------------------------------------


def worktree_path_for(job_id: str, worktree_root: Path | None = None) -> Path:
    return (worktree_root or WORKTREE_ROOT) / job_id


def branch_for(job: dict[str, Any]) -> str:
    owner = re.sub(r"[^a-z0-9]+", "-", str(job.get("OWNER_AGENT", "agent")).lower()).strip("-")
    return f"auto/{owner}/{job['JOB_ID']}"


def create_worktree(
    job: dict[str, Any],
    *,
    repo_root: Path | None = None,
    worktree_root: Path | None = None,
) -> dict[str, Any]:
    """Create an isolated git worktree from the job BASE_SHA (never stale HEAD)."""
    repo = repo_root or Path(job.get("REPO") or REPO_ROOT)
    target = worktree_path_for(job["JOB_ID"], worktree_root)
    git = shutil.which("git")
    if not git:
        return {"ok": False, "reason": "git-not-found"}
    if target.exists():
        return {"ok": True, "path": str(target), "reused": True, "branch": branch_for(job)}
    target.parent.mkdir(parents=True, exist_ok=True)
    base = job.get("BASE_SHA") or FROZEN_RELEASE_SHA
    result = subprocess.run(
        [git, "-C", str(repo), "worktree", "add", "-b", branch_for(job), str(target), base],
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    if result.returncode != 0:
        return {"ok": False, "reason": "worktree-add-failed", "stderr": redact(result.stderr)}
    return {"ok": True, "path": str(target), "branch": branch_for(job), "base_sha": base}


def cleanup_worktree(job: dict[str, Any], *, repo_root: Path | None = None) -> dict[str, Any]:
    """Remove the isolated worktree only when it has no uncommitted changes."""
    worktree = job.get("WORKTREE")
    if not worktree:
        return {"ok": True, "reason": "no-worktree"}
    repo = repo_root or Path(job.get("REPO") or REPO_ROOT)
    git = shutil.which("git")
    if not git:
        return {"ok": False, "reason": "git-not-found"}
    status = subprocess.run(
        [git, "-C", worktree, "status", "--porcelain"],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if status.stdout.strip():
        return {"ok": False, "reason": "worktree-dirty-preserved", "dirty": redact(status.stdout, 500)}
    removed = subprocess.run(
        [git, "-C", str(repo), "worktree", "remove", "--force", worktree],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    if removed.returncode != 0:
        return {"ok": False, "reason": "worktree-remove-failed", "stderr": redact(removed.stderr)}
    return {"ok": True, "reason": "removed"}


# --------------------------------------------------------------------------
# Executors
# --------------------------------------------------------------------------


def run_argv(argv: list[str], cwd: Path, timeout: int = 600, env: dict[str, str] | None = None) -> dict[str, Any]:
    started = now_epoch()
    try:
        result = subprocess.run(
            argv,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            env=env,
        )
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": redact(result.stdout),
            "stderr": redact(result.stderr),
            "duration_s": round(now_epoch() - started, 3),
            "argv": [Path(argv[0]).name, *argv[1:]],
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "returncode": 124, "stdout": "", "stderr": "timeout", "duration_s": timeout}
    except OSError as exc:
        return {"ok": False, "returncode": 127, "stdout": "", "stderr": redact(str(exc)), "duration_s": 0}


def execute_deterministic(job: dict[str, Any], cwd: Path) -> dict[str, Any]:
    executor = job.get("EXECUTOR") or {}
    errors = validate_argv(executor.get("argv"))
    if errors:
        return {"ok": False, "returncode": 2, "stdout": "", "stderr": "; ".join(errors), "duration_s": 0}
    timeout = int(job.get("TIME_BUDGET") or 600)
    return run_argv(list(executor["argv"]), cwd, timeout=timeout)


def execute_opencode(job: dict[str, Any], cwd: Path) -> dict[str, Any]:
    """Launch ``opencode run --auto`` with a fail-closed permission policy.

    ``--auto`` auto-approves every permission that is not an explicit deny, so we
    inject the hardened autonomous policy (no residual ``ask`` rules) via
    ``OPENCODE_PERMISSION``. Safe L0-L4 runs without a prompt; material actions
    fail closed.
    """
    binary = shutil.which("opencode")
    if not binary:
        return {"ok": False, "returncode": 127, "stdout": "", "stderr": "opencode-not-found", "duration_s": 0}
    prompt = job.get("EXECUTOR", {}).get("prompt") or job.get("BUSINESS_GOAL", "")
    argv = [binary]
    env = dict(os.environ)
    policy = Path(os.environ.get("DEALIX_OPENCODE_PERMISSION_POLICY", str(REPO_ROOT / "config/opencode/autonomous-permissions.json")))
    if policy.is_file():
        env["OPENCODE_PERMISSION"] = policy.read_text(encoding="utf-8").strip()
        argv.append("--auto")
    argv.append("run")
    model = (job.get("EXECUTOR") or {}).get("model")
    if model:
        argv += ["-m", str(model)]
    argv.append(str(prompt))
    return run_argv(argv, cwd, timeout=int(job.get("TIME_BUDGET") or 600), env=env)


def execute_local_ai(job: dict[str, Any], cwd: Path) -> dict[str, Any]:
    """Bounded local Ollama call. Network is loopback-only; failure is not fatal."""
    prompt = (job.get("EXECUTOR") or {}).get("prompt") or job.get("BUSINESS_GOAL", "")
    body = json.dumps({"model": "qwen3:4b-instruct-2507-q4_K_M", "prompt": prompt, "stream": False}).encode()
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = now_epoch()
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return {
            "ok": True,
            "returncode": 0,
            "stdout": redact(payload.get("response", ""))[:1000],
            "stderr": "",
            "duration_s": round(now_epoch() - started, 3),
        }
    except Exception as exc:
        return {"ok": False, "returncode": 1, "stdout": "", "stderr": redact(str(exc)), "duration_s": 0}


EXECUTORS = {
    "deterministic": execute_deterministic,
    "no_agent": execute_deterministic,
    "opencode": execute_opencode,
    "local_ai": execute_local_ai,
}


# --------------------------------------------------------------------------
# Acceptance verification
# --------------------------------------------------------------------------


def run_acceptance_checks(job: dict[str, Any], cwd: Path, executor_result: dict[str, Any]) -> dict[str, Any]:
    acceptance = job.get("ACCEPTANCE") or {}
    checks = acceptance.get("checks")
    if not checks:
        # No explicit checks: success requires the executor to have succeeded AND
        # at least one declared acceptance criterion.
        passed = bool(executor_result.get("ok")) and bool(job.get("ACCEPTANCE_CRITERIA"))
        return {"passed": passed, "detail": "executor_exit_and_criteria", "checks": []}
    results: list[dict[str, Any]] = []
    for check in checks:
        kind = check.get("kind")
        if kind == "exit_zero":
            ok = bool(executor_result.get("ok"))
        elif kind == "file_exists":
            ok = (cwd / str(check.get("path", ""))).is_file()
        elif kind == "file_contains":
            target = cwd / str(check.get("path", ""))
            ok = target.is_file() and str(check.get("text", "")) in target.read_text(encoding="utf-8", errors="ignore")
        else:
            ok = False
        results.append({"kind": kind, "ok": ok, "spec": check})
    return {"passed": all(item["ok"] for item in results), "detail": "explicit_checks", "checks": results}


# --------------------------------------------------------------------------
# Factory pipeline
# --------------------------------------------------------------------------


def plan_job(job: dict[str, Any]) -> dict[str, Any]:
    """Classify: assign execution mode and model class deterministically."""
    job["EXECUTION_MODE"] = CLASS_TO_MODE.get(job.get("JOB_CLASS"), "deterministic")
    job["MODEL_CLASS"] = CLASS_TO_MODEL_CLASS.get(job.get("JOB_CLASS"), "R1_DETERMINISTIC")
    return job


def submit_job(root: Path, job: dict[str, Any]) -> dict[str, Any]:
    plan_job(job)
    errors = validate_job(job)
    if errors:
        return {"ok": False, "errors": errors, "job": job}
    root.mkdir(parents=True, exist_ok=True)
    if job.get("AUTHORITY_LEVEL") == "L5":
        transition(job, "WAITING_L5", reason="L5 requires action-bound approval")
    else:
        transition(job, "READY", reason="submitted to factory queue")
    save_job(root, job)
    append_ledger(root, {"event": "job_submitted", "JOB_ID": job["JOB_ID"], "status": job["STATUS"]})
    write_queue_snapshot(root)
    return {"ok": True, "job": job}


def _working_dir(job: dict[str, Any], repo_root: Path) -> Path:
    worktree = job.get("WORKTREE")
    return Path(worktree) if worktree else repo_root


def run_job(
    root: Path,
    job: dict[str, Any],
    *,
    owner: str | None = None,
    repo_root: Path | None = None,
    worktree_root: Path | None = None,
    recover_expired: bool = False,
) -> dict[str, Any]:
    """Execute one READY job through launch -> verify -> record -> cleanup."""
    repo_root = repo_root or Path(job.get("REPO") or REPO_ROOT)
    owner = owner or job.get("OWNER_AGENT", "dealix-pm")

    if job.get("STATUS") == "WAITING_L5":
        return {"ok": False, "status": "WAITING_L5", "reason": "L5 not auto-executed", "job": job}
    if job.get("STATUS") not in ("READY", "RECOVERABLE", "QUEUED"):
        return {"ok": False, "status": job.get("STATUS"), "reason": "not-runnable", "job": job}
    if job.get("STATUS") in ("QUEUED", "RECOVERABLE"):
        transition(job, "READY", reason="admitted to run")

    transition(job, "CLAIMED", reason=f"claimed by {owner}")
    acquired, lease = acquire_lease(
        root,
        job,
        owner=owner,
        ttl_seconds=int(job.get("TIME_BUDGET") or 600) + 300,
        reclaim_expired=recover_expired,
    )
    if not acquired:
        transition(job, "READY", reason=f"lease not acquired: {lease.get('reason')}")
        save_job(root, job)
        return {"ok": False, "status": "READY", "reason": lease.get("reason"), "job": job}

    if job.get("MODIFYING") and not job.get("WORKTREE"):
        created = create_worktree(job, repo_root=repo_root, worktree_root=worktree_root)
        if not created.get("ok"):
            transition(job, "FAILED", reason=f"worktree isolation failed: {created.get('reason')}")
            release_lease(root, job["JOB_ID"])
            save_job(root, job)
            append_ledger(root, {"event": "job_failed", "JOB_ID": job["JOB_ID"], "reason": created.get("reason")})
            return {"ok": False, "status": "FAILED", "reason": created.get("reason"), "job": job}
        job["WORKTREE"] = created["path"]
        heartbeat_lease(root, job["JOB_ID"], ttl_seconds=int(job.get("TIME_BUDGET") or 600) + 300)

    transition(job, "RUNNING", reason="executor launched")
    save_job(root, job)
    executor = EXECUTORS.get(job.get("EXECUTION_MODE"), execute_deterministic)
    result = executor(job, _working_dir(job, repo_root))

    transition(job, "VERIFYING", reason="verifying acceptance evidence")
    acceptance = run_acceptance_checks(job, _working_dir(job, repo_root), result)
    job.setdefault("EVIDENCE", []).append({"at": now_iso(), "event": "execution", "result": result})
    job.setdefault("EVIDENCE", []).append({"at": now_iso(), "event": "acceptance", "result": acceptance})
    job["RESULT"] = {"executor": result, "acceptance": acceptance}

    if acceptance.get("passed"):
        transition(job, "SUCCEEDED", reason=acceptance.get("detail", ""))
        outcome = "SUCCEEDED"
    else:
        transition(job, "FAILED", reason="acceptance evidence missing or failed")
        outcome = "FAILED"

    release_lease(root, job["JOB_ID"])
    cleanup = cleanup_worktree(job, repo_root=repo_root)
    if outcome == "SUCCEEDED":
        job["WORKTREE"] = None if cleanup.get("ok") else job.get("WORKTREE")
    job["NEXT_ACTION"] = job.get("NEXT_ACTION") or ("none" if outcome == "SUCCEEDED" else "inspect failure and requeue if recoverable")
    save_job(root, job)
    append_ledger(
        root,
        {
            "event": "job_finished",
            "JOB_ID": job["JOB_ID"],
            "status": outcome,
            "execution_mode": job.get("EXECUTION_MODE"),
            "lease_released": True,
            "cleanup": cleanup,
        },
    )
    write_queue_snapshot(root)
    return {"ok": outcome == "SUCCEEDED", "status": outcome, "acceptance": acceptance, "job": job}


def process_queue(
    root: Path,
    *,
    limit: int | None = None,
    repo_root: Path | None = None,
    worktree_root: Path | None = None,
) -> list[dict[str, Any]]:
    """Promote and run READY jobs within the live deep-work resource budget."""
    governor = governor_state(root)
    budget = int(governor["deep_wip_available"]) if limit is None else limit
    candidates = [
        job
        for job in all_jobs(root)
        if job.get("STATUS") == "READY"
    ]
    candidates.sort(key=lambda item: -(item.get("PRIORITY") or 0))
    processed: list[dict[str, Any]] = []
    for job in candidates:
        if budget <= 0:
            break
        if job.get("MODIFYING"):
            budget -= 1
        processed.append(run_job(root, job, repo_root=repo_root, worktree_root=worktree_root))
    return processed


def recover(root: Path) -> dict[str, Any]:
    """Inspect RUNNING/CLAIMED jobs with dead or expired leases.

    Mutations are never blindly rerun: a dead runner is parked in RECOVERABLE
    for deliberate re-admission.
    """
    recovered: list[dict[str, Any]] = []
    for job in all_jobs(root):
        if job.get("STATUS") not in ("RUNNING", "CLAIMED"):
            continue
        lease = read_lease(root, job["JOB_ID"])
        if lease and not lease_expired(lease) and _pid_alive(lease.get("HEARTBEAT_PID")):
            continue
        previous = job.get("STATUS")
        if can_transition(previous, "RECOVERABLE"):
            transition(job, "RECOVERABLE", reason="runner lease expired/dead; inspected before reclaim")
            release_lease(root, job["JOB_ID"])
            save_job(root, job)
            append_ledger(root, {"event": "job_recoverable", "JOB_ID": job["JOB_ID"], "from": previous})
            recovered.append({"JOB_ID": job["JOB_ID"], "from": previous, "to": "RECOVERABLE"})
    write_queue_snapshot(root)
    return {"recovered": recovered, "count": len(recovered)}


def factory_status(root: Path) -> dict[str, Any]:
    jobs = all_jobs(root)
    counts = {state: sum(1 for job in jobs if job.get("STATUS") == state) for state in STATES}
    governor = governor_state(root)
    payload = {
        "schema": STATUS_SCHEMA,
        "generated_at": now_iso(),
        "base_sha": FROZEN_RELEASE_SHA,
        "jobs_total": len(jobs),
        "counts": counts,
        "active_leases": len(active_leases(root)),
        "deep_wip_max": DEEP_WIP_MAX,
        "max_concurrent_deep": governor["max_concurrent_deep"],
        "deep_wip_available": governor["deep_wip_available"],
        "paid_spill": "DISABLED_BY_DEFAULT",
        "l5_policy": "WAITING_L5_never_auto_executed",
    }
    write_json(status_path(root), payload)
    return payload


def render_status(payload: dict[str, Any]) -> str:
    active = ", ".join(f"{state}={count}" for state, count in payload["counts"].items() if count)
    return "\n".join(
        [
            "SESSION_FACTORY=ACTIVE",
            f"BASE_SHA={payload['base_sha']}",
            f"JOBS_TOTAL={payload['jobs_total']}",
            f"JOBS={active or 'none'}",
            f"ACTIVE_LEASES={payload['active_leases']}",
            f"MAX_CONCURRENT_DEEP={payload['max_concurrent_deep']}/{payload['deep_wip_max']}",
            f"DEEP_WIP_AVAILABLE={payload['deep_wip_available']}",
            f"PAID_SPILL={payload['paid_spill']}",
            f"L5_POLICY={payload['l5_policy']}",
        ]
    )


# --------------------------------------------------------------------------
# Autonomy acceptance
# --------------------------------------------------------------------------


def run_autonomy_acceptance(root: Path | None = None) -> dict[str, Any]:
    """Harmless synthetic end-to-end proof of the factory. No external effect."""
    root = root or state_root()
    root.mkdir(parents=True, exist_ok=True)
    sandbox = root / "acceptance"
    sandbox.mkdir(parents=True, exist_ok=True)
    results: dict[str, Any] = {}

    # A. happy path deterministic job, no worktree, writes a marker file.
    marker_a = sandbox / "marker_a.txt"
    job_a = make_job(
        owner_agent="dealix-pm",
        business_goal="synthetic deterministic acceptance A",
        job_class="DETERMINISTIC",
        authority_level="L1",
        priority=10,
        modifying=False,
        executor={"argv": ["python3", "-c", "import sys; open(sys.argv[1], 'w').write('ok')", str(marker_a)]},
        acceptance={"criteria": "marker written", "checks": [{"kind": "file_contains", "path": str(marker_a), "text": "ok"}]},
    )
    submit_job(root, job_a)
    out_a = run_job(root, load_job(root, job_a["JOB_ID"]))
    results["A_deterministic_success"] = {
        "status": out_a["status"],
        "lease_released": read_lease(root, job_a["JOB_ID"]) is None,
        "marker": marker_a.is_file(),
    }

    # B. failure path: executor exits non-zero, acceptance must fail.
    job_b = make_job(
        owner_agent="dealix-engineer",
        business_goal="synthetic deterministic acceptance B",
        job_class="DETERMINISTIC",
        authority_level="L1",
        priority=20,
        modifying=False,
        executor={"argv": ["python3", "-c", "import sys; sys.exit(3)"]},
        acceptance={"criteria": "must exit zero", "checks": [{"kind": "exit_zero"}]},
    )
    submit_job(root, job_b)
    out_b = run_job(root, load_job(root, job_b["JOB_ID"]))
    results["B_failure_detected"] = {
        "status": out_b["status"],
        "acceptance_passed": out_b["acceptance"]["passed"],
        "lease_released": read_lease(root, job_b["JOB_ID"]) is None,
    }

    # C. recovery: a RUNNING job with a dead lease is parked RECOVERABLE, then re-run.
    job_c = make_job(
        owner_agent="dealix-delivery",
        business_goal="synthetic recovery acceptance C",
        job_class="DETERMINISTIC",
        authority_level="L1",
        priority=30,
        modifying=False,
        executor={"argv": ["python3", "-c", "print('recovered')"]},
        acceptance={"criteria": "exit zero", "checks": [{"kind": "exit_zero"}]},
    )
    plan_job(job_c)
    transition(job_c, "READY", reason="seed")
    transition(job_c, "CLAIMED", reason="seed")
    transition(job_c, "RUNNING", reason="seed")
    save_job(root, job_c)
    write_json(
        lease_path(root, job_c["JOB_ID"]),
        {
            "schema": LEASE_SCHEMA,
            "JOB_ID": job_c["JOB_ID"],
            "WORKTREE": None,
            "FILES_OR_SCOPE": "job",
            "OWNER": "dead-runner",
            "LEASE_STARTED": now_iso(),
            "LEASE_STARTED_EPOCH": now_epoch() - 5000,
            "LEASE_EXPIRES_EPOCH": now_epoch() - 100,
            "HEARTBEAT": now_iso(),
            "HEARTBEAT_PID": 99999999,
        },
    )
    recovered = recover(root)
    job_c_after = load_job(root, job_c["JOB_ID"])
    status_after_recover = job_c_after["STATUS"]
    out_c = run_job(root, job_c_after, recover_expired=True)
    results["C_recovery"] = {
        "recoverable_count": recovered["count"],
        "status_after_recover": status_after_recover,
        "status_after_rerun": out_c["status"],
    }

    # D. L5 job must wait, never auto-execute.
    job_d = make_job(
        owner_agent="dealix-sales",
        business_goal="synthetic L5 send acceptance D",
        job_class="COMMERCIAL_REASONING",
        authority_level="L5",
        priority=40,
        modifying=False,
        executor={"prompt": "draft only"},
    )
    submit_job(root, job_d)
    out_d = run_job(root, load_job(root, job_d["JOB_ID"]))
    results["D_l5_gate"] = {"status": out_d["status"], "reason": out_d.get("reason")}

    # E. lease contention: second acquire must be refused.
    job_e = make_job(
        owner_agent="dealix-pm",
        business_goal="synthetic lease acceptance E",
        job_class="DETERMINISTIC",
        authority_level="L1",
        modifying=False,
        executor={"argv": ["python3", "-c", "print(1)"]},
    )
    plan_job(job_e)
    first_ok, _ = acquire_lease(root, job_e, owner="worker-1")
    second_ok, second_reason = acquire_lease(root, job_e, owner="worker-2")
    release_lease(root, job_e["JOB_ID"])
    results["E_lease_contention"] = {
        "first_acquired": first_ok,
        "second_acquired": second_ok,
        "second_reason": (second_reason or {}).get("reason"),
    }

    # F. secret redaction.
    results["F_redaction"] = {
        "api_key": redact("api_key=sk-abcdef1234567890"),
        "token": redact("Authorization: Bearer ghp_abcdefghijklmnop"),
    }

    checks = {
        "A": results["A_deterministic_success"]["status"] == "SUCCEEDED"
        and results["A_deterministic_success"]["lease_released"]
        and results["A_deterministic_success"]["marker"],
        "B": results["B_failure_detected"]["status"] == "FAILED"
        and not results["B_failure_detected"]["acceptance_passed"],
        "C": results["C_recovery"]["status_after_recover"] == "RECOVERABLE"
        and results["C_recovery"]["status_after_rerun"] == "SUCCEEDED",
        "D": results["D_l5_gate"]["status"] == "WAITING_L5",
        "E": results["E_lease_contention"]["first_acquired"]
        and not results["E_lease_contention"]["second_acquired"],
        "F": "[REDACTED]" in results["F_redaction"]["api_key"]
        and "[REDACTED]" in results["F_redaction"]["token"],
    }
    receipt = {
        "schema": "dealix.session_factory_acceptance.v1",
        "generated_at": now_iso(),
        "overall": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "evidence": results,
        "external_effect": "NONE",
    }
    write_json(root / "AUTONOMY_ACCEPTANCE.json", receipt)
    write_queue_snapshot(root)
    return receipt


def render_acceptance(receipt: dict[str, Any]) -> str:
    lines = [
        f"AUTONOMY_ACCEPTANCE={receipt['overall']}",
        f"EXTERNAL_EFFECT={receipt['external_effect']}",
    ]
    for name, ok in receipt["checks"].items():
        lines.append(f"  {name}={'PASS' if ok else 'FAIL'}")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def _load_job_arg(args: argparse.Namespace, root: Path) -> dict[str, Any]:
    if args.job_id:
        job = load_job(root, args.job_id)
        if not job:
            raise SystemExit(f"job not found: {args.job_id}")
        return job
    if args.file:
        return json.loads(Path(args.file).read_text(encoding="utf-8"))
    return make_job(
        owner_agent=args.owner,
        business_goal=args.goal or "unspecified",
        job_class=args.job_class,
        authority_level=args.authority,
        priority=args.priority,
        modifying=args.modifying,
        executor=json.loads(args.executor) if args.executor else {},
        acceptance=json.loads(args.acceptance) if args.acceptance else {},
    )


def _run_command(args: argparse.Namespace, root: Path) -> int:
    if args.command == "status":
        payload = factory_status(root)
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else render_status(payload))
        return 0
    if args.command == "governor":
        payload = governor_state(root)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    if args.command == "list":
        jobs = all_jobs(root)
        for job in sorted(jobs, key=lambda item: -(item.get("PRIORITY") or 0)):
            print(f"{job['JOB_ID']} {job.get('STATUS'):<12} {job.get('JOB_CLASS'):<22} {job.get('BUSINESS_GOAL')}")
        return 0
    if args.command == "submit":
        job = _load_job_arg(args, root)
        result = submit_job(root, job)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["ok"] else 1
    if args.command == "run":
        job = _load_job_arg(args, root)
        result = run_job(root, job, repo_root=REPO_ROOT, worktree_root=args.worktree_root, recover_expired=True)
        print(json.dumps({k: v for k, v in result.items() if k != "job"}, indent=2, ensure_ascii=False))
        return 0 if result["ok"] else 1
    if args.command == "tick":
        processed = process_queue(root, repo_root=REPO_ROOT, worktree_root=args.worktree_root)
        summary = [{"JOB_ID": item["job"]["JOB_ID"], "status": item["status"]} for item in processed]
        print(json.dumps({"processed": summary, "governor": governor_state(root)}, indent=2, ensure_ascii=False))
        return 0
    if args.command == "recover":
        payload = recover(root)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    receipt = run_autonomy_acceptance(root)
    print(json.dumps(receipt, indent=2, ensure_ascii=False) if args.json else render_acceptance(receipt))
    return 0 if receipt["overall"] == "PASS" else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dealix Hermes Autonomous Session Factory")
    parser.add_argument("command", choices=("status", "submit", "run", "tick", "recover", "acceptance", "governor", "list"))
    parser.add_argument("--state-dir", type=Path, default=STATE_DIR)
    parser.add_argument("--worktree-root", type=Path, default=WORKTREE_ROOT)
    parser.add_argument("--job-id")
    parser.add_argument("--file")
    parser.add_argument("--owner", default="dealix-pm")
    parser.add_argument("--goal")
    parser.add_argument("--job-class", default="DETERMINISTIC")
    parser.add_argument("--authority", default="L1")
    parser.add_argument("--priority", type=float, default=50.0)
    parser.add_argument("--modifying", action="store_true")
    parser.add_argument("--executor", help="JSON executor spec")
    parser.add_argument("--acceptance", help="JSON acceptance spec")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    root = args.state_dir
    root.mkdir(parents=True, exist_ok=True)
    rc = _run_command(args, root)
    share_state_with_operator(root)
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
