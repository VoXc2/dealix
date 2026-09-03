#!/usr/bin/env python3
"""Bounded Slack Socket Mode ingress for the canonical Dealix Company Autopilot."""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
import signal
import subprocess
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"
REPO_ROOT = Path(os.environ.get("DEALIX_REPO_ROOT", "/opt/dealix/workspace/dealix"))
AUTOPILOT = Path(os.environ.get("DEALIX_CANONICAL_AUTOPILOT", "/opt/dealix/control/bin/dealix_company_autopilot.sh"))
RECEIPT_DIR = Path(os.environ.get("DEALIX_SLACK_RECEIPT_DIR", "/opt/dealix/control/runs/slack-founder-receipts"))
COMMAND_CHANNEL_ID = os.environ.get("DEALIX_SLACK_COMMAND_CHANNEL_ID", "")
FOUNDER_USER_ID = os.environ.get("DEALIX_SLACK_FOUNDER_USER_ID", "")


def _bounded_env_int(name: str, default: int, minimum: int, maximum: int) -> int:
    raw = os.environ.get(name, str(default))
    try:
        value = int(raw)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be an integer") from exc
    if value < minimum or value > maximum:
        raise RuntimeError(f"{name} must be between {minimum} and {maximum}")
    return value


MAX_COMMAND_CHARS = _bounded_env_int("DEALIX_SLACK_MAX_COMMAND_CHARS", 600, 1, 4000)
RUN_TIMEOUT_SECONDS = _bounded_env_int("DEALIX_SLACK_RUN_TIMEOUT_SECONDS", 300, 5, 1800)
MENTION_RE = re.compile(r"<@[A-Z0-9]+>")
WHITESPACE_RE = re.compile(r"\s+")
SHA_RE = re.compile(r"[0-9a-f]{40}")
WORKLOAD_RE = re.compile(r"slack-[0-9a-f]{20}")
LOCK_KEY_RE = re.compile(r"slack-[A-Za-z0-9_-]{8,64}")

MODE_ALIASES = {
    "STATUS": "status",
    "\u062d\u0627\u0644\u0629": "status",
    "HEARTBEAT": "heartbeat",
    "\u0646\u0628\u0636": "heartbeat",
    "PRODUCTION": "production",
    "\u0627\u0646\u062a\u0627\u062c": "production",
    "\u0625\u0646\u062a\u0627\u062c": "production",
    "REPO": "repo-watch",
    "REPO-WATCH": "repo-watch",
    "\u0645\u0633\u062a\u0648\u062f\u0639": "repo-watch",
    "PREFLIGHT": "preflight",
    "VERIFY": "preflight",
    "\u062a\u062d\u0642\u0642": "preflight",
    "MARKET": "market-radar",
    "RADAR": "market-radar",
    "\u0633\u0648\u0642": "market-radar",
    "MIDDAY": "midday",
    "PULSE": "midday",
    "CYCLE": "midday",
    "\u062f\u0648\u0631\u0629": "midday",
    "EVENING": "evening",
    "\u0645\u0633\u0627\u0621": "evening",
    "NIGHTLY": "nightly",
    "\u0644\u064a\u0644\u064a": "nightly",
    "WEEKLY": "weekly",
    "\u0627\u0633\u0628\u0648\u0639\u064a": "weekly",
    "\u0623\u0633\u0628\u0648\u0639\u064a": "weekly",
    "LOCAL-AI": "local-ai",
    "LOCAL_AI": "local-ai",
    "\u0630\u0643\u0627\u0621-\u0645\u062d\u0644\u064a": "local-ai",
}
CANONICAL_MODES = frozenset(MODE_ALIASES.values())

L5_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bSEND\b",
        r"\bPUBLISH\b",
        r"\bPOST\b.*\bPUBLIC\b",
        r"\bMERGE\b",
        r"\bDEPLOY\b",
        r"\bPAY\b",
        r"\bREFUND\b",
        r"\bSPEND\b",
        r"\bDNS\b",
        r"\bSECRET\b",
        r"\bTOKEN\b",
        r"\bDELETE\b",
        r"\bDROP\b",
        r"\bWHATSAPP\b.*\bSEND\b",
        r"\bLINKEDIN\b.*\b(?:DM|MESSAGE|CONNECT)\b",
        "(?:\u0623\u0631\u0633\u0644|\u0627\u0631\u0633\u0644|\u0625\u0631\u0633\u0627\u0644|\u0627\u0631\u0633\u0627\u0644)",
        "(?:\u0627\u0646\u0634\u0631|\u0646\u0634\u0631 \u0639\u0627\u0645)",
        "(?:\u0627\u062f\u0645\u062c|\u0625\u062f\u0645\u062c|\u062f\u0645\u062c.*(?:main|\u0645\u064a\u0646))",
        "(?:\u0628\u0631\u0648\u062f\u0643\u0634\u0646|\u0625\u0646\u062a\u0627\u062c|\u0627\u0646\u062a\u0627\u062c).*(?:\u0627\u0646\u0634\u0631|\u0646\u0634\u0631)",
        "(?:\u0627\u062f\u0641\u0639|\u062f\u0641\u0639|\u0627\u0633\u062a\u0631\u062f\u0627\u062f|\u0627\u0633\u062a\u0631\u062c\u0627\u0639)",
        "(?:\u0627\u062d\u0630\u0641|\u062d\u0630\u0641)",
        "\u0648\u0627\u062a\u0633\u0627\u0628.*(?:\u0623\u0631\u0633\u0644|\u0627\u0631\u0633\u0644|\u0625\u0631\u0633\u0627\u0644|\u0627\u0631\u0633\u0627\u0644)",
        "\u0644\u064a\u0646\u0643\u062f.?\u0627\u0646.*(?:\u0631\u0633\u0627\u0644\u0629|\u0627\u062a\u0635\u0627\u0644|\u062a\u0648\u0627\u0635\u0644)",
    )
)

FAIL_CLOSED_ENV = {
    "DEALIX_EXTERNAL_SEND": "0",
    "DEALIX_EXTERNAL_OUTREACH_ENABLED": "false",
    "EXTERNAL_OUTREACH_ENABLED": "false",
    "AUTO_SEND_ENABLED": "false",
    "DEALIX_EMAIL_LIVE_SEND": "0",
    "DEALIX_WHATSAPP_OUTBOUND": "0",
    "WHATSAPP_ALLOW_LIVE_SEND": "false",
    "DEALIX_PUBLIC_PUBLISH": "0",
    "DEALIX_PAID_SPEND": "0",
    "DEALIX_PAYMENT_EXECUTION": "0",
    "DEALIX_PRODUCTION_MUTATION": "0",
    "DEALIX_DNS_MUTATION": "0",
    "DEALIX_DB_MUTATION": "0",
    "DEALIX_SECRET_MUTATION": "0",
    "DEALIX_AGENT_SELF_AUTHORITY": "0",
    "AGENT_APPROVAL_MODE": "required",
    "MOYASAR_LIVE_MODE": "0",
}


class ReceiptStateError(RuntimeError):
    pass


class IndeterminatePriorAttempt(RuntimeError):
    pass


@dataclass(frozen=True)
class CommandDecision:
    authority_class: str
    execution_boundary: str
    result: str
    mode: str | None
    action: str
    state_after: str
    next_action: str


@dataclass(frozen=True)
class RuntimeRepoState:
    sha: str
    branch: str
    origin_main_sha: str
    clean: bool
    canonical: bool


@dataclass(frozen=True)
class AutopilotRun:
    returncode: int
    elapsed_ms: int
    log_path: Path
    log_sha256: str
    timed_out: bool


def normalize_command(text: str) -> str:
    value = MENTION_RE.sub(" ", text or "")
    return WHITESPACE_RE.sub(" ", value).strip()[:MAX_COMMAND_CHARS]


def classify_command(text: str) -> CommandDecision:
    command = normalize_command(text)
    if any(pattern.search(command) for pattern in L5_PATTERNS):
        return CommandDecision(
            "APPROVAL_REQUIRED",
            "L5_BLOCKED",
            "APPROVAL_REQUIRED",
            None,
            "L5_INTENT_BLOCKED_AT_AUTHORITY_GATE",
            "BLOCKED_AT_AUTHORITY_GATE",
            "Create a specific action-bound approval packet; generic Slack command authority cannot execute material external effects.",
        )
    token = command.split(" ", 1)[0] if command else "STATUS"
    mode = MODE_ALIASES.get(token.upper()) or MODE_ALIASES.get(token)
    if mode is None:
        return CommandDecision(
            "L0_L4",
            "L0-L4_INTERNAL_FAIL_CLOSED",
            "FAILED",
            None,
            "UNSUPPORTED_FOUNDER_COMMAND",
            "FAILED",
            "Use an allowlisted command: STATUS, HEARTBEAT, PRODUCTION, REPO, VERIFY, MARKET, CYCLE, EVENING, NIGHTLY, WEEKLY, LOCAL-AI.",
        )
    return CommandDecision(
        "L0_L4",
        "L0-L4_INTERNAL_FAIL_CLOSED",
        "EXECUTED",
        mode,
        f"RUN_CANONICAL_AUTOPILOT_MODE:{mode}",
        "CANONICAL_AUTOPILOT_COMPLETED",
        "Inspect the bound runner log and canonical Company Autopilot evidence; escalate only a verified blocker.",
    )


def workload_id(channel: str, timestamp: str, user: str) -> str:
    material = f"{channel}|{timestamp}|{user}".encode("utf-8")
    return f"slack-{hashlib.sha256(material).hexdigest()[:20]}"


def _ensure_receipt_dir() -> None:
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    if RECEIPT_DIR.is_symlink():
        raise RuntimeError("receipt directory must not be a symlink")
    os.chmod(RECEIPT_DIR, 0o750)


def _receipt_path(work_id: str) -> Path:
    return RECEIPT_DIR / f"{work_id}.json"


def _runner_log_path(work_id: str) -> Path:
    return RECEIPT_DIR / f"{work_id}.runner.log"


@contextmanager
def workload_lock(work_id: str) -> Iterator[None]:
    if not LOCK_KEY_RE.fullmatch(work_id):
        raise ValueError("invalid workload lock key")
    _ensure_receipt_dir()
    path = RECEIPT_DIR / f".{work_id}.lock"
    flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags, 0o640)
    os.fchmod(fd, 0o640)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def _git(repo_root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo_root), *args],
        text=True,
        stderr=subprocess.DEVNULL,
        timeout=15,
    ).strip()


def runtime_repo_state(repo_root: Path = REPO_ROOT) -> RuntimeRepoState:
    sha = _git(repo_root, "rev-parse", "HEAD")
    branch = _git(repo_root, "rev-parse", "--abbrev-ref", "HEAD")
    origin_main_sha = _git(repo_root, "rev-parse", "origin/main")
    dirty = bool(_git(repo_root, "status", "--porcelain", "--untracked-files=normal"))
    if not SHA_RE.fullmatch(sha) or not SHA_RE.fullmatch(origin_main_sha):
        raise RuntimeError("runtime repository returned an invalid git SHA")
    clean = not dirty
    return RuntimeRepoState(sha, branch, origin_main_sha, clean, branch == "main" and clean and sha == origin_main_sha)


def source_sha(repo_root: Path = REPO_ROOT) -> str:
    state = runtime_repo_state(repo_root)
    if not state.canonical:
        raise RuntimeError("runtime repository is not clean canonical main")
    return state.sha


def fail_closed_env(base_env: dict[str, str] | None = None) -> dict[str, str]:
    env = dict(os.environ if base_env is None else base_env)
    for key in list(env):
        upper = key.upper()
        if upper.startswith("SLACK_") or ("SLACK" in upper and ("TOKEN" in upper or "SECRET" in upper)):
            env.pop(key, None)
    env.update(FAIL_CLOSED_ENV)
    return env


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _terminate_process_group(process: subprocess.Popen[bytes]) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=5)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait(timeout=5)


def run_autopilot_with_evidence(mode: str, work_id: str) -> AutopilotRun:
    if mode not in CANONICAL_MODES:
        raise ValueError("mode is not in the canonical allowlist")
    if not WORKLOAD_RE.fullmatch(work_id):
        raise ValueError("invalid workload_id")
    _ensure_receipt_dir()
    log_path = _runner_log_path(work_id)
    if log_path.exists():
        raise IndeterminatePriorAttempt("runner log exists without a trusted terminal receipt; blind retry blocked")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    log_fd = os.open(log_path, flags, 0o600)
    started = time.monotonic()
    timed_out = False
    with os.fdopen(log_fd, "wb", closefd=True) as log_handle:
        process = subprocess.Popen(
            [str(AUTOPILOT), mode],
            cwd=str(REPO_ROOT),
            env=fail_closed_env(),
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        try:
            returncode = process.wait(timeout=RUN_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            timed_out = True
            _terminate_process_group(process)
            returncode = 124
        log_handle.flush()
        os.fsync(log_handle.fileno())
    return AutopilotRun(
        returncode,
        int((time.monotonic() - started) * 1000),
        log_path,
        _sha256_file(log_path),
        timed_out,
    )


def run_autopilot(mode: str) -> tuple[int, int]:
    if mode not in CANONICAL_MODES:
        raise ValueError("mode is not in the canonical allowlist")
    started = time.monotonic()
    process = subprocess.Popen(
        [str(AUTOPILOT), mode],
        cwd=str(REPO_ROOT),
        env=fail_closed_env(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    try:
        returncode = process.wait(timeout=RUN_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        _terminate_process_group(process)
        raise
    return returncode, int((time.monotonic() - started) * 1000)


def make_receipt(
    *,
    work_id: str,
    slack_ref: str,
    sha: str,
    decision: CommandDecision,
    elapsed_ms: int,
    runner_rc: int | None,
    source_branch: str | None = None,
    origin_main_sha: str | None = None,
    source_clean: bool | None = None,
    source_canonical: bool | None = None,
    runner_log_path: Path | None = None,
    runner_log_sha256: str | None = None,
) -> dict[str, Any]:
    result = decision.result
    state_after = decision.state_after
    if decision.mode is not None and runner_rc is not None and runner_rc != 0:
        result = "FAILED"
        state_after = "CANONICAL_AUTOPILOT_FAILED"
    output_refs = [str(_receipt_path(work_id))]
    if runner_log_path is not None:
        output_refs.append(str(runner_log_path))
    receipt: dict[str, Any] = {
        "schema_version": "1.0",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "system_id": "command_os",
        "workload_id": work_id,
        "agent": "dealix-pm",
        "runner": str(AUTOPILOT),
        "source_sha": sha,
        "trigger": "slack-founder-room",
        "input_evidence_refs": [slack_ref],
        "state_before": "FOUNDER_COMMAND_RECEIVED",
        "action": decision.action,
        "execution_boundary": decision.execution_boundary,
        "authority_class": decision.authority_class,
        "result": result,
        "output_evidence_refs": output_refs,
        "next_evidence": "bound_runner_log_and_canonical_company_autopilot_receipt",
        "next_action": decision.next_action,
        "idempotency_key": work_id,
        "founder_minutes": UNKNOWN,
        "agent_minutes": UNKNOWN,
        "elapsed_ms": elapsed_ms,
        "ai_cost": UNKNOWN,
        "tool_cost": UNKNOWN,
        "risk_class": "HIGH_EXTERNAL_BLOCKED" if decision.authority_class == "APPROVAL_REQUIRED" else "LOW_INTERNAL",
        "economic_delta": UNKNOWN,
        "learning_signal": "slack_founder_command",
        "state_after": state_after,
    }
    optional = {
        "runner_rc": runner_rc,
        "source_branch": source_branch,
        "origin_main_sha": origin_main_sha,
        "source_clean": source_clean,
        "source_canonical": source_canonical,
        "runner_log_sha256": runner_log_sha256,
    }
    receipt.update({key: value for key, value in optional.items() if value is not None})
    return receipt


def write_receipt(receipt: dict[str, Any]) -> Path:
    _ensure_receipt_dir()
    work_id = str(receipt.get("workload_id", ""))
    if not WORKLOAD_RE.fullmatch(work_id):
        raise ValueError("invalid workload_id")
    path = _receipt_path(work_id)
    if path.exists():
        raise ReceiptStateError("terminal receipt already exists")
    tmp = RECEIPT_DIR / f".{work_id}.{os.getpid()}.tmp"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(tmp, flags, 0o640)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", closefd=True) as handle:
            json.dump(receipt, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
        dir_fd = os.open(RECEIPT_DIR, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    finally:
        if tmp.exists():
            tmp.unlink()
    return path


def existing_receipt(work_id: str) -> dict[str, Any] | None:
    path = _receipt_path(work_id)
    if not path.exists():
        return None
    if path.is_symlink():
        raise ReceiptStateError("receipt path must not be a symlink")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReceiptStateError("existing receipt is unreadable or invalid JSON") from exc
    if not isinstance(value, dict) or value.get("workload_id") != work_id:
        raise ReceiptStateError("existing receipt identity mismatch")
    if value.get("schema_version") != "1.0" or not isinstance(value.get("output_evidence_refs"), list):
        raise ReceiptStateError("existing receipt schema is invalid")
    return value


def format_reply(receipt: dict[str, Any]) -> str:
    refs = receipt.get("output_evidence_refs") or [UNKNOWN]
    return (
        f"Dealix President - {receipt.get('result', 'FAILED')}\n"
        f"workload_id: `{receipt.get('workload_id', UNKNOWN)}`\n"
        f"source_sha: `{receipt.get('source_sha', UNKNOWN)}`\n"
        f"authority: `{receipt.get('authority_class', UNKNOWN)}`\n"
        f"receipt: `{refs[0]}`\n"
        f"next: {receipt.get('next_action', 'Inspect the canonical evidence.')}"
    )


def _runtime_failure_decision(action: str, next_action: str) -> CommandDecision:
    return CommandDecision("L0_L4", "L0-L4_INTERNAL_FAIL_CLOSED", "FAILED", None, action, "FAILED", next_action)


def validate_runtime_env() -> None:
    required = {
        "SLACK_BOT_TOKEN": os.environ.get("SLACK_BOT_TOKEN", ""),
        "SLACK_APP_TOKEN": os.environ.get("SLACK_APP_TOKEN", ""),
        "DEALIX_SLACK_COMMAND_CHANNEL_ID": COMMAND_CHANNEL_ID,
        "DEALIX_SLACK_FOUNDER_USER_ID": FOUNDER_USER_ID,
    }
    missing = [key for key, value in required.items() if not value]
    if missing:
        raise RuntimeError(f"missing required runtime environment keys: {', '.join(missing)}")
    if not required["SLACK_BOT_TOKEN"].startswith("xoxb-"):
        raise RuntimeError("SLACK_BOT_TOKEN must be a bot token")
    if not required["SLACK_APP_TOKEN"].startswith("xapp-"):
        raise RuntimeError("SLACK_APP_TOKEN must be a Socket Mode app token")
    if not AUTOPILOT.is_file() or not os.access(AUTOPILOT, os.X_OK):
        raise RuntimeError(f"canonical Company Autopilot missing or not executable: {AUTOPILOT}")
    if not (REPO_ROOT / ".git").exists():
        raise RuntimeError(f"canonical repository missing: {REPO_ROOT}")


def build_app():
    from slack_bolt import App

    app = App(token=os.environ["SLACK_BOT_TOKEN"])

    @app.event("app_mention")
    def on_app_mention(event, say, logger):  # type: ignore[no-untyped-def]
        channel = str(event.get("channel", ""))
        user = str(event.get("user", ""))
        ts = str(event.get("ts", ""))
        if channel != COMMAND_CHANNEL_ID or user != FOUNDER_USER_ID or not ts:
            return
        work_id = workload_id(channel, ts, user)
        try:
            with workload_lock(work_id):
                try:
                    cached = existing_receipt(work_id)
                except ReceiptStateError:
                    say(text=f"Dealix President - BLOCKED\nworkload_id: `{work_id}`\nnext: Existing receipt is corrupt; reconcile it before retrying.", thread_ts=ts)
                    return
                if cached is not None:
                    say(text=format_reply(cached), thread_ts=ts)
                    return
                decision = classify_command(str(event.get("text", "")))
                slack_ref = f"slack:{channel}:{ts}"
                try:
                    repo_state = runtime_repo_state()
                except Exception as exc:
                    logger.error("Dealix Slack bridge runtime truth check failed: %s", type(exc).__name__)
                    say(text=f"Dealix President - BLOCKED\nworkload_id: `{work_id}`\nnext: Canonical repository truth is unavailable; no command executed.", thread_ts=ts)
                    return
                if decision.mode is not None and not repo_state.canonical:
                    decision = _runtime_failure_decision("RUNTIME_REPOSITORY_NOT_CANONICAL", "Require clean main with HEAD equal to origin/main before execution.")
                run: AutopilotRun | None = None
                if decision.mode is not None:
                    try:
                        run = run_autopilot_with_evidence(decision.mode, work_id)
                    except IndeterminatePriorAttempt:
                        decision = _runtime_failure_decision("INDETERMINATE_PRIOR_ATTEMPT", "Reconcile the prior runner log before any retry.")
                    except Exception as exc:
                        logger.error("Dealix Slack bridge runner failed: %s", type(exc).__name__)
                        decision = _runtime_failure_decision("CANONICAL_AUTOPILOT_INVOCATION_FAILED", "Inspect the restricted runner log and runtime permissions; do not retry blindly.")
                receipt = make_receipt(
                    work_id=work_id,
                    slack_ref=slack_ref,
                    sha=repo_state.sha,
                    decision=decision,
                    elapsed_ms=run.elapsed_ms if run is not None else 0,
                    runner_rc=run.returncode if run is not None else None,
                    source_branch=repo_state.branch,
                    origin_main_sha=repo_state.origin_main_sha,
                    source_clean=repo_state.clean,
                    source_canonical=repo_state.canonical,
                    runner_log_path=run.log_path if run is not None else None,
                    runner_log_sha256=run.log_sha256 if run is not None else None,
                )
                write_receipt(receipt)
                say(text=format_reply(receipt), thread_ts=ts)
        except Exception as exc:
            logger.error("Dealix Slack bridge command handling failed: %s", type(exc).__name__)
            say(text=f"Dealix President - BLOCKED\nworkload_id: `{work_id}`\nnext: Internal command handling failed closed; inspect service logs.", thread_ts=ts)

    return app


def main() -> int:
    validate_runtime_env()
    from slack_bolt.adapter.socket_mode import SocketModeHandler

    SocketModeHandler(build_app(), os.environ["SLACK_APP_TOKEN"]).start()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
