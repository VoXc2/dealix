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
import pathlib
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from go_resource_broker import (
    GO_COST_VERIFIED_DISABLED,
    discover_catalog,
    discover_ollama_models,
    discover_router_models,
    pick_model,
    provider_cost_authority,
)
from model_cost_policy import (
    PAID_PENDING_APPROVAL,
    is_explicit_free_model,
    is_included_opencode_go_model,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = Path(os.environ.get("DEALIX_SESSION_FACTORY_STATE", "/opt/dealix/control/state/session_factory"))
WORKTREE_ROOT = Path(os.environ.get("DEALIX_SESSION_FACTORY_WORKTREES", "/opt/dealix/worktrees/auto"))
FROZEN_RELEASE_SHA = os.environ.get("DEALIX_FROZEN_RELEASE_SHA", "8bb0a6c382c49ca288f7b579cae07676f006e229")

def resolve_live_base_sha(repo_root: pathlib.Path | str | None = None) -> str | None:
    """Resolve the exact live base for autonomous jobs, or None.

    This never falls back to the frozen release SHA: a None return means live
    git resolution failed and the caller must fail closed (modifying jobs) or
    apply an explicit non-modifying compatibility policy.
    """
    # Prefer explicit env
    explicit = os.environ.get("DEALIX_AGENTIC_BASE_SHA", "").strip()
    if explicit:
        return explicit
    # Prefer origin/main, then HEAD, via git
    git = shutil.which("git")
    repo = pathlib.Path(repo_root or REPO_ROOT)
    if git:
        for candidate in (os.environ.get("DEALIX_AGENTIC_BASE_REF", "origin/main").strip() or "origin/main", "HEAD"):
            try:
                result = subprocess.run(
                    [git, "-C", str(repo), "rev-parse", "--verify", f"{candidate}^{{commit}}"],
                    capture_output=True, text=True, timeout=10, check=False
                )
                sha = result.stdout.strip()
                if result.returncode == 0 and sha:
                    return sha
            except (OSError, subprocess.TimeoutExpired):
                continue
    return None


def resolve_default_base_sha(repo_root: pathlib.Path | str | None = None) -> str:
    """Resolve exact live base for autonomous jobs; never inherit stale frozen default blindly."""
    live = resolve_live_base_sha(repo_root)
    if live:
        return live
    # Fallback to frozen only when live resolution fails (preserves production
    # release path). Modifying job creation must NOT use this fallback: see
    # make_job, which resolves a strict live base for repo-writing work.
    return FROZEN_RELEASE_SHA

# Autonomous OpenCode runs get their own control database. Sharing the single
# interactive ``opencode.db`` lets session creation block on that file's write
# lock (a run then sits at ``init`` for the whole budget with zero output).
OPENCODE_DB_DIR = Path(os.environ.get("DEALIX_OPENCODE_DB_DIR", str(STATE_DIR / "opencode")))

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
# Operational ceiling for deep modifying concurrency. This is a bounded,
# configurable governor input — not the legacy global DEEP_WIP_MAX=3 hard cap,
# which Omega V3 supersedes. Live CPU/RAM/load derive the actual capacity.
DEEP_WIP_CEILING_DEFAULT = 8
DEEP_WIP_CEILING_HARD_MAX = 64

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

# Executor result fields that exist only so acceptance checks can inspect the
# *complete* process output. They are stripped before evidence is persisted, so
# durable state stays secret-redacted and bounded via ``redact``.
EPHEMERAL_RESULT_KEYS = frozenset({"stdout_full", "stderr_full"})


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


def strip_ephemeral(result: dict[str, Any]) -> dict[str, Any]:
    """Drop in-memory-only fields before persisting executor evidence."""
    return {key: value for key, value in result.items() if key not in EPHEMERAL_RESULT_KEYS}


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
    """Grant the canonical operator group controlled read/write access to factory state.

    The factory may bootstrap as root while Hermes runs as ``dealix``. The
    canonical operator must be able to claim/recover jobs without sudo, so the
    state tree is shared only with the operator group and remains closed to
    everyone else.
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
        os.chmod(root, 0o770)  # noqa: S103 - canonical operator owns runtime mutations
        for path in root.rglob("*"):
            try:
                os.chown(path, -1, gid)
                if path.is_dir():
                    os.chmod(path, (path.stat().st_mode & 0o777) | 0o070)  # noqa: S103 - operator group owns state dirs
                elif path.is_file():
                    os.chmod(path, (path.stat().st_mode & 0o777) | 0o060)
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
    effective_modifying = bool(modifying) if modifying is not None else job_class in MODIFYING_CLASSES
    if base_sha:
        resolved_base: str | None = base_sha
    elif effective_modifying:
        # Modifying jobs must never receive frozen fallback authority: when
        # live git resolution fails the base stays empty and worktree creation
        # fails closed end-to-end (live-base-required-no-frozen-fallback).
        resolved_base = resolve_live_base_sha()
    else:
        resolved_base = resolve_default_base_sha()
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
            "BASE_SHA": resolved_base,
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
            "MODIFYING": effective_modifying,
            "EXECUTION_MODE": CLASS_TO_MODE.get(job_class, "deterministic"),
            "EXECUTOR": executor or {},
            "ACCEPTANCE": acceptance or {},
            "LEASE": None,
        }
    )
    return job


_CANONICAL_AGENT_CACHE: dict[str, Any] = {"agents": None, "at": 0.0}
_CANONICAL_AGENT_TTL_S = 300.0


def canonical_agent_ids() -> set[str] | None:
    """Return current canonical logical-agent ids, or None when unavailable.

    Loads ``dealix/agentic_holding/runtime.py`` directly by file path (no
    package ``__init__`` side effects) and caches the roster briefly. A None
    return means the registry cannot be established right now; callers fail
    closed for hierarchical identities rather than trusting caller text.
    """
    now = now_epoch()
    cached = _CANONICAL_AGENT_CACHE.get("agents")
    if cached is not None and now - float(_CANONICAL_AGENT_CACHE.get("at") or 0.0) < _CANONICAL_AGENT_TTL_S:
        return set(cached)
    try:
        import importlib.util

        path = REPO_ROOT / "dealix" / "agentic_holding" / "runtime.py"
        spec = importlib.util.spec_from_file_location("dealix_agentic_holding_runtime_canonical", path)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        # slots=True dataclasses resolve string annotations via sys.modules.
        sys.modules[spec.name] = module
        # runtime.py imports sibling packages (e.g. dealix.commercial.arm_registry).
        # When this module runs as a standalone script (cron/systemd), REPO_ROOT is
        # not on sys.path and the import fails closed to "registry unavailable".
        # Ensure the repo root is importable for the duration of the load only.
        added_root = str(REPO_ROOT) not in sys.path
        if added_root:
            sys.path.insert(0, str(REPO_ROOT))
        try:
            spec.loader.exec_module(module)
            agents = set(module.build_current_registry().agents)
        finally:
            sys.modules.pop(spec.name, None)
            if added_root:
                try:
                    sys.path.remove(str(REPO_ROOT))
                except ValueError:
                    pass
    except Exception:
        return None
    _CANONICAL_AGENT_CACHE["agents"] = agents
    _CANONICAL_AGENT_CACHE["at"] = now
    return set(agents)


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
    # The five permanent names are compatibility executor aliases (routing
    # labels); hierarchical dealix.*.* identities must be registry-bound using
    # the current canonical Agentic Holding registry. Caller text alone can
    # never mint a logical agent identity.
    is_hierarchical = isinstance(owner, str) and owner.startswith("dealix.") and owner.count(".") >= 2
    if owner and owner not in PERMANENT_AGENTS and not is_hierarchical:
        errors.append(f"invalid:OWNER_AGENT={owner} (must be one of the five permanent agents or a hierarchical logical agent dealix.*.*)")
    elif is_hierarchical and owner not in PERMANENT_AGENTS:
        known = canonical_agent_ids()
        if known is None:
            errors.append(f"invalid:OWNER_AGENT={owner} (canonical agent registry unavailable; failing closed)")
        elif owner not in known:
            errors.append(f"invalid:OWNER_AGENT={owner} (unknown logical agent: not in the canonical registry)")
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


def operational_ceiling() -> int:
    """Bounded operational ceiling for deep modifying concurrency.

    Configurable via ``DEALIX_DEEP_WIP_CEILING`` (clamped to a hard maximum so
    concurrency is never unbounded). This replaces the legacy global
    DEEP_WIP_MAX=3 hard cap: roomy hosts may safely compute above 3 while
    constrained hosts throttle down to 1.
    """
    try:
        configured = int(os.environ.get("DEALIX_DEEP_WIP_CEILING", str(DEEP_WIP_CEILING_DEFAULT)))
    except (TypeError, ValueError):
        return DEEP_WIP_CEILING_DEFAULT
    return max(1, min(configured, DEEP_WIP_CEILING_HARD_MAX))


def compute_max_concurrent_deep(resources: dict[str, Any]) -> int:
    """ResourceGovernor-derived deep-work concurrency: live CPU/RAM/load plus the operational ceiling."""
    available = int(resources.get("mem_available_mb") or 0)
    cpu = max(1, int(resources.get("cpu_count") or 1))
    load1 = float(resources.get("load1") or 0.0)
    ceiling = operational_ceiling()
    if available and available < 2500:
        return 1
    # Roughly one deep worker per ~2GiB headroom above a 2GiB reserve, and one
    # per CPU below one reserved for the host supervisor.
    by_mem = max(1, (available - 2048) // 2048) if available else 1
    by_cpu = max(1, cpu - 1)
    capacity = max(1, min(by_mem, by_cpu, ceiling))
    if load1 > cpu * 1.5:
        capacity = min(capacity, 2)
    if load1 > cpu * 3:
        capacity = 1
    return max(1, capacity)


def governor_state(root: Path, resources: dict[str, Any] | None = None) -> dict[str, Any]:
    resources = resources or read_resources()
    deep_active = sum(1 for lease in active_leases(root) if lease.get("JOB_ID") and not lease_expired(lease))
    max_deep = compute_max_concurrent_deep(resources)
    payload = {
        "schema": GOVERNOR_SCHEMA,
        "generated_at": now_iso(),
        "resources": resources,
        "deep_wip_active": deep_active,
        "deep_wip_max": operational_ceiling(),
        "max_concurrent_deep": max_deep,
        "deep_wip_available": max(0, max_deep - deep_active),
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
    base = job.get("BASE_SHA")
    if not base and job.get("MODIFYING"):
        # Modifying jobs require an exact live base. A stale/frozen fallback
        # must never mint base authority for repo-writing work.
        return {"ok": False, "reason": "live-base-required-no-frozen-fallback"}
    base = base or resolve_default_base_sha()
    verify = subprocess.run(
        [git, "-C", str(repo), "rev-parse", "--verify", f"{base}^{{commit}}"],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    resolved = verify.stdout.strip()
    if verify.returncode != 0 or not resolved:
        return {"ok": False, "reason": "live-base-unresolvable", "stderr": redact(verify.stderr)}
    base = resolved
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


def run_argv(
    argv: list[str],
    cwd: Path,
    timeout: int = 600,
    env: dict[str, str] | None = None,
    stdin: Any = None,
) -> dict[str, Any]:
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
            stdin=stdin,
        )
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": redact(result.stdout),
            "stderr": redact(result.stderr),
            "stdout_full": result.stdout or "",
            "stderr_full": result.stderr or "",
            "duration_s": round(now_epoch() - started, 3),
            "argv": [Path(argv[0]).name, *argv[1:]],
        }
    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "returncode": 124,
            "stdout": "",
            "stderr": "timeout",
            "stdout_full": "",
            "stderr_full": "timeout",
            "duration_s": timeout,
        }
    except OSError as exc:
        return {
            "ok": False,
            "returncode": 127,
            "stdout": "",
            "stderr": redact(str(exc)),
            "stdout_full": "",
            "stderr_full": str(exc),
            "duration_s": 0,
        }


def execute_deterministic(job: dict[str, Any], cwd: Path) -> dict[str, Any]:
    executor = job.get("EXECUTOR") or {}
    errors = validate_argv(executor.get("argv"))
    if errors:
        return {"ok": False, "returncode": 2, "stdout": "", "stderr": "; ".join(errors), "duration_s": 0}
    timeout = int(job.get("TIME_BUDGET") or 600)
    return run_argv(list(executor["argv"]), cwd, timeout=timeout)


def resolve_opencode_binary() -> str | None:
    """Resolve OpenCode in both interactive shells and stripped cron environments."""
    binary = shutil.which("opencode")
    if binary:
        return binary
    home = Path(os.environ.get("HOME", str(Path.home()))).expanduser()
    candidate = home / ".opencode" / "bin" / "opencode"
    if candidate.is_file() and os.access(candidate, os.X_OK):
        return str(candidate)
    return None


def opencode_db_path(job: dict[str, Any], db_dir: Path | None = None) -> Path:
    """Per-job control database, isolated from the interactive TUI's ``opencode.db``."""
    base = Path(db_dir) if db_dir else OPENCODE_DB_DIR
    return base / f"{job.get('JOB_ID') or 'job'}.db"


def _resolve_opencode_model(job: dict[str, Any]) -> tuple[str | None, dict[str, Any] | None]:
    """Resolve a catalog-bound model, or ``(None, hold_result)``.

    A ``-free`` suffix alone is NOT authority: caller-supplied and
    selection-file candidates must also be present in the current discovered
    catalog (current canonical availability evidence). Fabricated or stale
    ``*-free`` ids HOLD instead of launching.
    """
    catalog = discover_catalog(refresh=False) or []
    available = set(catalog)
    model = (job.get("EXECUTOR") or {}).get("model")
    if model:
        # A caller-supplied model is never authority on its own. Accept only a
        # currently-catalogued explicit-free id, or a catalogued included-Go id
        # while live provider cost authority verifies balance fallback is
        # disabled. Otherwise HOLD.
        live_cost = str(provider_cost_authority().get("state"))
        caller_allowed = (
            is_explicit_free_model(model)
            or (is_included_opencode_go_model(model) and live_cost == GO_COST_VERIFIED_DISABLED)
        ) and model in available
        if not caller_allowed:
            return None, {
                "ok": False,
                "returncode": 79,
                "stdout": "",
                "stderr": "model-authority-unproven: caller model rejected without current catalog/cost evidence",
                "duration_s": 0,
            }
        return str(model), None
    route = CLASS_TO_MODEL_CLASS.get(str(job.get("JOB_CLASS")), "R4_INCLUDED_HIGH")
    picked = pick_model(route, catalog, discover_ollama_models(), discover_router_models()) if catalog else None
    if not picked or str(picked).endswith("UNKNOWN") or picked in (PAID_PENDING_APPROVAL, "none"):
        selected_path = Path(
            os.environ.get(
                "DEALIX_OPENCODE_SELECTED_MODEL_FILE",
                "/opt/dealix/control/opencode/state/selected-free-model",
            )
        )
        if selected_path.is_file():
            candidate = selected_path.read_text(encoding="utf-8").strip().splitlines()[0].strip()
            # Stale selection files cannot mint model authority: the candidate
            # must be an explicit-free id present in the current catalog.
            if is_explicit_free_model(candidate) and candidate in available:
                picked = candidate
    if not picked or str(picked).endswith("UNKNOWN") or picked in (PAID_PENDING_APPROVAL, "none"):
        # Unknown paid spill fails closed: never launch on a provider default.
        return None, {
            "ok": False,
            "returncode": 79,
            "stdout": "",
            "stderr": "model-authority-unavailable: HOLD (no verified current free model)",
            "duration_s": 0,
        }
    return str(picked), None


OPENCODE_DAEMON_DEFAULT_URL = "http://127.0.0.1:4098"
OPENCODE_DAEMON_HEALTH_PATH = "/global/health"
_TERMINAL_FINISH = frozenset({"stop", "error", "aborted"})


def daemon_base_url(env: dict[str, str] | None = None) -> str | None:
    """Return the configured daemon URL only when it is explicitly loopback-only."""
    src = env if env is not None else os.environ
    raw = str(src.get("DEALIX_OPENCODE_DAEMON_URL") or "").strip() or OPENCODE_DAEMON_DEFAULT_URL
    try:
        parts = urllib.parse.urlparse(raw)
    except ValueError:
        return None
    if parts.scheme != "http":
        return None
    host = (parts.hostname or "").lower()
    if host not in ("127.0.0.1", "localhost", "::1"):
        return None
    port = parts.port or 80
    bracketed = f"[{parts.hostname}]" if ":" in (parts.hostname or "") else (parts.hostname or "")
    return f"http://{bracketed}:{port}"


def split_daemon_model(model: str | None) -> tuple[str, str] | None:
    """Split a pinned ``provider/id`` model for the daemon session contract."""
    value = (model or "").strip()
    if "/" not in value:
        return None
    provider, mid = value.split("/", 1)
    provider, mid = provider.strip(), mid.strip()
    if not provider or not mid or any(ch.isspace() for ch in value):
        return None
    return provider, mid


def _daemon_request(
    base: str, method: str, path: str, payload: dict[str, Any] | None = None, timeout: int = 15
) -> tuple[int | None, str]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        base + path, data=data, headers={"Content-Type": "application/json"}, method=method
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return int(getattr(response, "status", 200)), response.read().decode("utf-8", errors="replace")
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def _daemon_unavailable(reason: str) -> dict[str, Any]:
    return {
        "ok": False,
        "returncode": 75,
        "stdout": "",
        "stderr": f"opencode-daemon-unavailable: {reason}",
        "duration_s": 0,
        "via": "daemon",
        "daemon_unavailable": True,
    }


def daemon_health(base: str, timeout: int = 10) -> dict[str, Any]:
    """Verify the existing daemon is healthy and version-compatible (read-only)."""
    status, body = _daemon_request(base, "GET", OPENCODE_DAEMON_HEALTH_PATH, timeout=timeout)
    if status != 200:
        return {"healthy": False, "version": "", "http_status": status, "detail": redact(body, 300)}
    try:
        payload = json.loads(body or "{}")
    except (json.JSONDecodeError, ValueError, TypeError):
        return {"healthy": False, "version": "", "http_status": status, "detail": "unparseable-health"}
    if not isinstance(payload, dict):
        return {"healthy": False, "version": "", "http_status": status, "detail": "unexpected-health-shape"}
    version = str(payload.get("version") or "")
    major = version.split(".", 1)[0] if version else ""
    return {
        "healthy": bool(payload.get("healthy")) and major == "1",
        "version": version,
        "http_status": status,
    }


def _daemon_session_id(body: str) -> str | None:
    try:
        payload = json.loads(body or "{}")
    except (json.JSONDecodeError, ValueError, TypeError):
        return None
    if not isinstance(payload, dict):
        return None
    for container in (payload, payload.get("session"), payload.get("data")):
        if isinstance(container, dict) and container.get("id"):
            return str(container["id"])
    return None


def _daemon_abort(base: str, session_id: str, dir_query: str) -> None:
    """Best-effort session abort; never raises."""
    try:
        _daemon_request(base, "POST", f"/session/{session_id}/abort?directory={dir_query}", {}, timeout=10)
    except Exception:
        pass


def _daemon_terminal_state(payload: Any) -> tuple[bool, bool, str, str]:
    """Tolerantly parse a session message payload -> (done, clean, text, error)."""
    messages = payload.get("messages") if isinstance(payload, dict) else payload
    if not isinstance(messages, list):
        return False, False, "", ""
    texts: list[str] = []
    finish: str | None = None
    error = ""
    last_completed = False
    last_finish: str | None = None
    for message in messages:
        if not isinstance(message, dict):
            continue
        info = message.get("info") if isinstance(message.get("info"), dict) else {}
        # Live daemon shape nests role/finish/error under info; top-level
        # keys are accepted when present. Prefer top-level, fall back to info.
        role = str(message.get("role") or info.get("role") or "")
        current = message.get("finish") or info.get("finish")
        if current:
            finish = str(current)
        info_error = info.get("error")
        if info_error:
            error = str(info_error)[:500]
        # OpenCode 1.18.x signals assistant-message completion with
        # info.time.completed. Normally `finish` is also present
        # (stop | tool-calls | error | aborted), and intermediate
        # tool-using steps report finish="tool-calls" while still being
        # COMPLETE at the message level. We must therefore only treat a
        # message as terminal for the session when finish is a terminal
        # value, OR when finish is entirely absent (an empty/errored
        # completion that would otherwise never terminate).
        time_info = info.get("time") if isinstance(info.get("time"), dict) else {}
        last_completed = role == "assistant" and bool(time_info.get("completed"))
        last_finish = str(current) if current else None
        parts = message.get("parts") or []
        if not isinstance(parts, list):
            continue
        for part in parts:
            if not isinstance(part, dict):
                continue
            if part.get("type") == "text" and part.get("text"):
                if role == "assistant":
                    texts.append(str(part["text"]))
            part_info = part.get("info") or {}
            part_error = part.get("error") or (part_info.get("error") if isinstance(part_info, dict) else None)
            if part_error:
                error = str(part_error)[:500]
    text = "\n".join(texts)
    completed_without_finish = last_completed and last_finish is None
    if finish in _TERMINAL_FINISH or error or completed_without_finish:
        if finish in ("error", "aborted"):
            clean = False
        else:
            clean = not error
        return True, clean, text, error or ("" if clean else f"finish={finish or 'completed'}")
    return False, False, text, ""


def execute_opencode_daemon(
    job: dict[str, Any],
    cwd: Path,
    *,
    model: str,
    base_url: str | None = None,
    timeout_s: float | None = None,
    poll_interval: float = 2.0,
    idle_timeout_s: float | None = None,
) -> dict[str, Any]:
    """Bounded headless execution against the existing loopback OpenCode daemon.

    Uses only the proven session contract (create -> prompt_async -> poll
    messages -> abort on timeout). Never starts a daemon, never falls back to
    the direct CLI here: transport/health failures return a
    ``daemon_unavailable`` HOLD so the caller can decide explicitly.
    """
    started = now_epoch()
    base = base_url or daemon_base_url()
    if not base:
        return _daemon_unavailable("daemon-url-not-loopback-or-invalid")
    health = daemon_health(base)
    if not health.get("healthy"):
        return _daemon_unavailable(f"daemon-unhealthy version={health.get('version') or 'unknown'}")
    split = split_daemon_model(model)
    if not split:
        return {
            "ok": False,
            "returncode": 79,
            "stdout": "",
            "stderr": "model-authority-unproven: daemon model is not a pinnable provider/id",
            "duration_s": round(now_epoch() - started, 3),
            "via": "daemon",
        }
    provider_id, model_id = split
    directory = str(cwd)
    dir_query = urllib.parse.quote(directory, safe="")
    agent = str(os.environ.get("DEALIX_OPENCODE_DAEMON_AGENT") or "build").strip() or "build"
    title = str(job.get("BUSINESS_GOAL") or job.get("JOB_ID") or "dealix-job")[:120]

    status, body = _daemon_request(
        base,
        "POST",
        f"/session?directory={dir_query}",
        {"title": title, "agent": agent, "model": {"providerID": provider_id, "id": model_id}},
        timeout=30,
    )
    session_id = _daemon_session_id(body) if status in (200, 201) else None
    if not session_id:
        return {
            "ok": False,
            "returncode": 75,
            "stdout": "",
            "stderr": redact(f"daemon-session-rejected: http={status} {body}", 500),
            "stdout_full": "",
            "stderr_full": body,
            "duration_s": round(now_epoch() - started, 3),
            "via": "daemon",
            "session_id": None,
        }

    prompt = str((job.get("EXECUTOR") or {}).get("prompt") or job.get("BUSINESS_GOAL", ""))
    status, body = _daemon_request(
        base,
        "POST",
        f"/session/{session_id}/prompt_async?directory={dir_query}",
        {
            "model": {"providerID": provider_id, "modelID": model_id},
            "agent": agent,
            "parts": [{"type": "text", "text": prompt}],
        },
        timeout=30,
    )
    if status not in (200, 202, 204):
        _daemon_abort(base, session_id, dir_query)
        return {
            "ok": False,
            "returncode": 75,
            "stdout": "",
            "stderr": redact(f"daemon-prompt-rejected: http={status} {body}", 500),
            "stdout_full": "",
            "stderr_full": body,
            "duration_s": round(now_epoch() - started, 3),
            "via": "daemon",
            "session_id": session_id,
        }

    try:
        budget = int(job.get("TIME_BUDGET") or 600)
    except (TypeError, ValueError):
        budget = 600
    computed_deadline = started + max(30, min(budget, 1800))
    deadline = started + timeout_s if timeout_s is not None else computed_deadline
    interval = max(0.01, min(float(poll_interval or 2.0), 30.0))
    explicit_idle_timeout = idle_timeout_s is not None
    if idle_timeout_s is None:
        try:
            idle_timeout_s = float(os.environ.get("DEALIX_OPENCODE_DAEMON_IDLE_TIMEOUT_S", "45"))
        except ValueError:
            idle_timeout_s = 45.0
    idle_floor = 0.01 if explicit_idle_timeout else 15.0
    idle_timeout_s = max(idle_floor, min(float(idle_timeout_s), 300.0))
    last_text = ""
    last_progress_at = now_epoch()
    last_body = ""
    while now_epoch() < deadline:
        time.sleep(interval)
        status, body = _daemon_request(
            base, "GET", f"/session/{session_id}/message?directory={dir_query}", timeout=15
        )
        if status != 200 or not body:
            if now_epoch() - last_progress_at >= idle_timeout_s:
                _daemon_abort(base, session_id, dir_query)
                full = last_text[:20000]
                return {
                    "ok": False,
                    "returncode": 124,
                    "stdout": redact(full),
                    "stderr": "daemon-idle-timeout: session aborted after no observable progress",
                    "stdout_full": full,
                    "stderr_full": "daemon-idle-timeout",
                    "duration_s": round(now_epoch() - started, 3),
                    "via": "daemon",
                    "session_id": session_id,
                    "model": model,
                    "idle_timeout_s": idle_timeout_s,
                }
            continue
        if body != last_body:
            last_progress_at = now_epoch()
            last_body = body
        try:
            payload = json.loads(body)
        except (json.JSONDecodeError, ValueError, TypeError):
            continue
        done, clean, text, error = _daemon_terminal_state(payload)
        last_text = text or last_text
        if done:
            full = last_text[:20000]
            duration = round(now_epoch() - started, 3)
            if clean:
                return {
                    "ok": True,
                    "returncode": 0,
                    "stdout": redact(full),
                    "stderr": "",
                    "stdout_full": full,
                    "stderr_full": "",
                    "duration_s": duration,
                    "via": "daemon",
                    "session_id": session_id,
                    "model": model,
                }
            return {
                "ok": False,
                "returncode": 1,
                "stdout": redact(full),
                "stderr": redact(error or "daemon-finish-error", 500),
                "stdout_full": full,
                "stderr_full": error,
                "duration_s": duration,
                "via": "daemon",
                "session_id": session_id,
                "model": model,
            }
        if now_epoch() - last_progress_at >= idle_timeout_s:
            _daemon_abort(base, session_id, dir_query)
            full = last_text[:20000]
            return {
                "ok": False,
                "returncode": 124,
                "stdout": redact(full),
                "stderr": "daemon-idle-timeout: session aborted after no observable progress",
                "stdout_full": full,
                "stderr_full": "daemon-idle-timeout",
                "duration_s": round(now_epoch() - started, 3),
                "via": "daemon",
                "session_id": session_id,
                "model": model,
                "idle_timeout_s": idle_timeout_s,
            }
    _daemon_abort(base, session_id, dir_query)
    full = last_text[:20000]
    return {
        "ok": False,
        "returncode": 124,
        "stdout": redact(full),
        "stderr": "daemon-deadline-exceeded: session aborted",
        "stdout_full": full,
        "stderr_full": "daemon-deadline-exceeded",
        "duration_s": round(now_epoch() - started, 3),
        "via": "daemon",
        "session_id": session_id,
        "model": model,
    }


def execute_opencode_cli(
    job: dict[str, Any], cwd: Path, *, db_dir: Path | None = None, model: str | None = None
) -> dict[str, Any]:
    """Bounded direct ``opencode run --auto`` launch with isolated state.

    This path uses the same verified model authority and autonomous permission
    policy as the daemon executor. It is retained as a recovery transport for
    an unavailable daemon (explicit opt-in) or an aborted idle daemon session.
    """
    binary = resolve_opencode_binary()
    if not binary:
        return {"ok": False, "returncode": 127, "stdout": "", "stderr": "opencode-not-found", "duration_s": 0}
    policy = Path(
        os.environ.get(
            "DEALIX_OPENCODE_PERMISSION_POLICY",
            str(REPO_ROOT / "config/opencode/autonomous-permissions.json"),
        )
    )
    if not policy.is_file():
        return {
            "ok": False,
            "returncode": 78,
            "stdout": "",
            "stderr": "autonomous-permission-policy-missing",
            "duration_s": 0,
        }
    db_path = opencode_db_path(job, db_dir)
    try:
        db_path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return {
            "ok": False,
            "returncode": 73,
            "stdout": "",
            "stderr": redact(f"opencode-control-db-unavailable: {exc}"),
            "duration_s": 0,
        }

    prompt = job.get("EXECUTOR", {}).get("prompt") or job.get("BUSINESS_GOAL", "")
    # Raw JSON events are the stable non-interactive CLI contract. The default
    # formatted renderer is intended for terminal output and has previously
    # stalled under captured/non-TTY execution on this host.
    argv = [binary, "run", "--auto", "--format", "json"]
    env = dict(os.environ)
    env["OPENCODE_PERMISSION"] = policy.read_text(encoding="utf-8").strip()
    env["OPENCODE_DB"] = str(db_path)
    env.setdefault("OPENCODE_DISABLE_AUTOUPDATE", "1")
    env.setdefault("OPENCODE_DISABLE_MODELS_FETCH", "1")
    if model is None:
        model, hold = _resolve_opencode_model(job)
        if hold is not None:
            return hold
    argv += ["-m", str(model)]
    argv.append(str(prompt))
    return run_argv(
        argv,
        cwd,
        timeout=int(job.get("TIME_BUDGET") or 600),
        env=env,
        stdin=subprocess.DEVNULL,
    )


def execute_opencode(
    job: dict[str, Any], cwd: Path, *, db_dir: Path | None = None, allow_cli_fallback: bool | None = None
) -> dict[str, Any]:
    """Daemon-first headless OpenCode execution for Session Factory jobs.

    The loopback daemon remains the preferred automatic path. A daemon that is
    unavailable still requires explicit CLI opt-in. A daemon session that hits
    its bounded deadline is aborted first and may then recover through the
    same verified-model CLI executor; this prevents a healthy-but-stuck daemon
    from disabling the company while preserving model, permission, and
    worktree isolation.
    """
    model, hold = _resolve_opencode_model(job)
    if hold is not None:
        return hold
    daemon = execute_opencode_daemon(job, cwd, model=model)
    # OpenCode 1.18.x can leave a healthy loopback daemon session running
    # without a terminal assistant message until the bounded deadline. The
    # daemon executor aborts that session before returning 124, so a same-model
    # CLI retry is safe: it stays in the same isolated worktree, keeps the
    # autonomous permission policy, and cannot spill to an unverified paid
    # model because ``_resolve_opencode_model`` already established authority.
    daemon_timed_out_after_abort = (
        daemon.get("via") == "daemon" and int(daemon.get("returncode") or 0) == 124
    )
    if not daemon.get("daemon_unavailable") and not daemon_timed_out_after_abort:
        return daemon
    if allow_cli_fallback is None:
        flag = str(os.environ.get("DEALIX_OPENCODE_ALLOW_CLI_FALLBACK") or "").strip().lower()
        allow_cli_fallback = flag in ("1", "true", "yes", "on") or daemon_timed_out_after_abort
    if allow_cli_fallback:
        cli = execute_opencode_cli(job, cwd, db_dir=db_dir, model=model)
        if daemon_timed_out_after_abort:
            cli["fallback_reason"] = "daemon-timeout-after-abort"
            cli["daemon_session_id"] = daemon.get("session_id")
        return cli
    return daemon


def execute_local_ai(job: dict[str, Any], cwd: Path) -> dict[str, Any]:
    """Bounded local Ollama call with capped latency and generation size."""
    executor = job.get("EXECUTOR") or {}
    prompt = executor.get("prompt") or job.get("BUSINESS_GOAL", "")
    try:
        timeout_seconds = int(executor.get("timeout_seconds", 60))
    except (TypeError, ValueError):
        timeout_seconds = 60
    timeout_seconds = max(5, min(timeout_seconds, 120))
    try:
        num_predict = int(executor.get("num_predict", 128))
    except (TypeError, ValueError):
        num_predict = 128
    num_predict = max(32, min(num_predict, 256))
    body = json.dumps(
        {
            "model": "qwen3:4b-instruct-2507-q4_K_M",
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": num_predict},
        }
    ).encode()
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = now_epoch()
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return {
            "ok": True,
            "returncode": 0,
            "stdout": redact(payload.get("response", ""))[:1000],
            "stdout_full": payload.get("response", "") or "",
            "stderr": "",
            "duration_s": round(now_epoch() - started, 3),
        }
    except Exception as exc:
        return {
            "ok": False,
            "returncode": 1,
            "stdout": "",
            "stdout_full": "",
            "stderr": redact(str(exc)),
            "duration_s": round(now_epoch() - started, 3),
        }


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
        elif kind == "stdout_contains":
            # Fail closed: an empty marker never passes. Match against the full
            # ephemeral process output, never the bounded evidence preview.
            marker = str(check.get("text", ""))
            haystack = executor_result.get("stdout_full")
            if not isinstance(haystack, str):
                haystack = str(executor_result.get("stdout") or "")
            ok = bool(marker) and marker in haystack
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
    errors = validate_job(job)
    if errors:
        return {
            "ok": False,
            "status": "BLOCKED",
            "reason": "canonical-admission-rejected",
            "errors": errors,
            "job": job,
        }

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
    stored_result = strip_ephemeral(result)
    job.setdefault("EVIDENCE", []).append({"at": now_iso(), "event": "execution", "result": stored_result})
    job.setdefault("EVIDENCE", []).append({"at": now_iso(), "event": "acceptance", "result": acceptance})
    job["RESULT"] = {"executor": stored_result, "acceptance": acceptance}

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
    available = int(governor["deep_wip_available"])
    # ResourceGovernor is the hard upper bound: a caller limit may only reduce
    # capacity, never escalate past it.
    budget = available if limit is None else min(int(limit), available)
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
        "base_sha": resolve_default_base_sha(),
        "frozen_release_sha": FROZEN_RELEASE_SHA,
        "jobs_total": len(jobs),
        "counts": counts,
        "active_leases": len(active_leases(root)),
        "deep_wip_max": operational_ceiling(),
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
