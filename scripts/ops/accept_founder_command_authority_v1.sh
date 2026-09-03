#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

ROOT="$(git rev-parse --show-toplevel)"
EXPECTED_SHA="${1:-}"

exec /usr/bin/python3 - "$ROOT" "$EXPECTED_SHA" <<'PY'
from __future__ import annotations

import hashlib
import json
import os
import pwd
import re
import sqlite3
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(sys.argv[1])
EXPECTED_SHA = sys.argv[2]
RUN_USER = "dealix"
OPENCLAW_HOME = Path(f"/home/{RUN_USER}/.openclaw")
OPENCLAW_BIN = OPENCLAW_HOME / "bin/openclaw"
CONFIG = OPENCLAW_HOME / "openclaw.json"


def run(argv: list[str], *, cwd: Path | None = None, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def normalize_sender(value: object) -> str | None:
    text = str(value).strip()
    match = re.fullmatch(r"(?:telegram:|tg:)?([0-9]{4,20})", text, flags=re.IGNORECASE)
    return match.group(1) if match else None


def recursive_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return [str(value)]
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            out.extend(recursive_values(item))
        return out
    if isinstance(value, dict):
        out = []
        for item in value.values():
            out.extend(recursive_values(item))
        return out
    return []


def exact_mode(path: Path, mode: int) -> bool:
    return path.is_file() and not path.is_symlink() and stat.S_IMODE(path.stat().st_mode) == mode


def safe_owner_fingerprint(owner_id: str | None) -> str | None:
    if not owner_id:
        return None
    digest = hashlib.sha256(f"telegram:{owner_id}".encode("utf-8")).hexdigest()[:20]
    return f"sha256:{digest}"


def write_receipt(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(path.parent, 0o700)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.chmod(path, 0o600)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    digest_path = path.with_suffix(".sha256")
    digest_path.write_text(f"{digest}  {path.name}\n", encoding="utf-8")
    os.chmod(digest_path, 0o600)


if not EXPECTED_SHA:
    print("DEALIX_FOUNDER_COMMAND_ACCEPTANCE=BLOCKED_EXPECTED_SHA_REQUIRED")
    raise SystemExit(2)

head = run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture=True).stdout.strip()
if head != EXPECTED_SHA:
    print("DEALIX_FOUNDER_COMMAND_ACCEPTANCE=BLOCKED_HEAD_MISMATCH")
    print(f"expected={EXPECTED_SHA}")
    print(f"actual={head or 'unknown'}")
    raise SystemExit(2)

if os.geteuid() != 0:
    print("DEALIX_FOUNDER_COMMAND_ACCEPTANCE=BLOCKED_ROOT_REQUIRED_FOR_READ_ONLY_RUNTIME_EVIDENCE")
    raise SystemExit(3)

proof_root = Path(
    os.environ.get(
        "DEALIX_FOUNDER_COMMAND_PROOF_ROOT",
        f"/opt/dealix/control/proof/founder-command/{head}",
    )
)
receipt_path = proof_root / "receipt.json"

# Preserve the Company Machine's fail-closed external-effect posture for the
# acceptance process itself. These variables do not mutate OpenClaw config.
os.environ.update(
    {
        "DEALIX_EXTERNAL_SEND": "0",
        "DEALIX_EMAIL_LIVE_SEND": "0",
        "DEALIX_WHATSAPP_OUTBOUND": "0",
        "DEALIX_PUBLIC_PUBLISH": "0",
        "DEALIX_PAID_SPEND": "0",
        "DEALIX_PAYMENT_EXECUTION": "0",
        "DEALIX_PRODUCTION_MUTATION": "0",
        "DEALIX_DNS_MUTATION": "0",
        "DEALIX_DB_MUTATION": "0",
        "DEALIX_SECRET_MUTATION": "0",
        "DEALIX_IDENTITY_MUTATION": "0",
        "DEALIX_AGENT_SELF_AUTHORITY": "0",
        "DEALIX_AUTONOMY_LEVEL": "4",
        "DEALIX_MODE": "draft-only",
    }
)

safety_issues: list[str] = []
hold_reasons: list[str] = []
checks: dict[str, bool] = {}
owner_id: str | None = None
owner_fp: str | None = None
approved_ids: set[str] = set()

try:
    dealix_uid = pwd.getpwnam(RUN_USER).pw_uid
except KeyError:
    dealix_uid = -1
    hold_reasons.append("dealix_runtime_user_missing")

checks["openclaw_binary"] = OPENCLAW_BIN.is_file() and os.access(OPENCLAW_BIN, os.X_OK)
if not checks["openclaw_binary"]:
    hold_reasons.append("openclaw_binary_missing")

# Resolve the bundled Node runtime without installation or PATH mutation on disk.
node_candidates = [
    path
    for path in OPENCLAW_HOME.glob("tools/**/bin/node")
    if path.is_file() and os.access(path, os.X_OK)
]
node_candidates.sort(key=lambda path: str(path))
node_dir = node_candidates[-1].parent if node_candidates else None
checks["bundled_node_runtime"] = node_dir is not None
if node_dir is None:
    hold_reasons.append("openclaw_bundled_node_runtime_missing")

checks["openclaw_config_regular_0600"] = exact_mode(CONFIG, 0o600)
if not CONFIG.is_file() or CONFIG.is_symlink():
    hold_reasons.append("openclaw_config_missing_or_symlink")
elif not checks["openclaw_config_regular_0600"]:
    safety_issues.append("openclaw_config_permissions_not_0600")

config: dict[str, Any] = {}
if CONFIG.is_file() and not CONFIG.is_symlink():
    try:
        loaded = json.loads(CONFIG.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            config = loaded
        else:
            safety_issues.append("openclaw_config_not_object")
    except Exception:
        safety_issues.append("openclaw_config_invalid_json")


def get_path(*keys: str, default: Any = None) -> Any:
    current: Any = config
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


checks["gateway_config_loopback"] = (
    get_path("gateway", "mode") == "local"
    and get_path("gateway", "bind") == "loopback"
    and int(get_path("gateway", "port", default=0) or 0) == 18789
)
if config and not checks["gateway_config_loopback"]:
    safety_issues.append("gateway_config_not_local_loopback_18789")

telegram = get_path("channels", "telegram", default={})
if not isinstance(telegram, dict):
    telegram = {}

checks["telegram_enabled"] = telegram.get("enabled") is True
if config and not checks["telegram_enabled"]:
    hold_reasons.append("telegram_channel_not_enabled")

checks["telegram_dm_pairing"] = telegram.get("dmPolicy") == "pairing"
if config and not checks["telegram_dm_pairing"]:
    safety_issues.append("telegram_dm_policy_not_pairing")

checks["telegram_groups_disabled"] = (
    telegram.get("groups", {}) == {}
    and telegram.get("groupAllowFrom", []) in ([], None)
)
if config and not checks["telegram_groups_disabled"]:
    safety_issues.append("telegram_groups_or_group_senders_enabled")

explicit_allow_values = recursive_values(telegram.get("allowFrom", []))
if any(value.strip() == "*" for value in explicit_allow_values):
    safety_issues.append("telegram_dm_wildcard_present")
explicit_allow_ids = {
    normalized
    for value in explicit_allow_values
    if (normalized := normalize_sender(value)) is not None
}
approved_ids.update(explicit_allow_ids)

# Telegram credential must live outside source/config as a private file. Never
# read or print the secret value.
inline_token = telegram.get("botToken")
if inline_token not in (None, ""):
    safety_issues.append("telegram_inline_bot_token_present")

token_file_value = telegram.get("tokenFile")
checks["telegram_secret_file_private"] = False
if isinstance(token_file_value, str) and token_file_value.startswith("/"):
    token_file = Path(token_file_value)
    secret_root = Path(f"/home/{RUN_USER}/.config/dealix-secrets")
    try:
        token_file.relative_to(secret_root)
        inside_secret_root = True
    except ValueError:
        inside_secret_root = False
    if not inside_secret_root:
        safety_issues.append("telegram_token_file_outside_dealix_secret_root")
    elif not token_file.is_file() or token_file.is_symlink():
        hold_reasons.append("telegram_token_file_missing_or_symlink")
    else:
        token_stat = token_file.stat()
        if token_stat.st_uid != dealix_uid:
            safety_issues.append("telegram_token_file_wrong_owner")
        if stat.S_IMODE(token_stat.st_mode) != 0o600:
            safety_issues.append("telegram_token_file_permissions_not_0600")
        checks["telegram_secret_file_private"] = (
            token_stat.st_uid == dealix_uid and stat.S_IMODE(token_stat.st_mode) == 0o600
        )
else:
    hold_reasons.append("telegram_token_file_reference_missing")

# Founder command owner must be exactly one Telegram numeric identity. The raw
# ID never leaves memory; the durable receipt stores a one-way fingerprint.
owner_values = recursive_values(get_path("commands", "ownerAllowFrom", default=[]))
valid_owner_ids: list[str] = []
invalid_owner_entries = False
for value in owner_values:
    match = re.fullmatch(r"telegram:([0-9]{4,20})", value.strip(), flags=re.IGNORECASE)
    if match:
        valid_owner_ids.append(match.group(1))
    else:
        invalid_owner_entries = True
if invalid_owner_entries or len(set(valid_owner_ids)) > 1:
    safety_issues.append("command_owner_not_exactly_one_telegram_identity")
elif len(set(valid_owner_ids)) == 1:
    owner_id = next(iter(set(valid_owner_ids)))
    owner_fp = safe_owner_fingerprint(owner_id)
else:
    hold_reasons.append("telegram_command_owner_not_configured")
checks["exact_telegram_command_owner"] = owner_id is not None

# In OpenClaw 2026.7.x commands.allowFrom is an independent authorization
# boundary when present. For a one-founder command surface it may be absent, or
# it may contain only the exact Telegram owner. Global/provider-spanning rules
# fail closed.
command_allow = get_path("commands", "allowFrom", default=None)
checks["command_allowlist_narrow"] = True
if command_allow is not None:
    if not isinstance(command_allow, dict):
        safety_issues.append("commands_allow_from_not_object")
        checks["command_allowlist_narrow"] = False
    else:
        if set(command_allow) - {"telegram"}:
            safety_issues.append("commands_allow_from_has_non_telegram_scope")
            checks["command_allowlist_narrow"] = False
        telegram_command_values = recursive_values(command_allow.get("telegram", []))
        if any(value.strip() == "*" for value in telegram_command_values):
            safety_issues.append("commands_allow_from_wildcard_present")
            checks["command_allowlist_narrow"] = False
        command_ids = {
            normalized
            for value in telegram_command_values
            if (normalized := normalize_sender(value)) is not None
        }
        if owner_id and command_ids != {owner_id}:
            safety_issues.append("commands_allow_from_not_exact_founder")
            checks["command_allowlist_narrow"] = False
        elif not owner_id and command_ids:
            safety_issues.append("commands_allow_from_exists_without_exact_owner")
            checks["command_allowlist_narrow"] = False

# The Telegram-facing agent is messaging-only; runtime/filesystem/shell mutation
# must remain denied regardless of founder identity.
tools = get_path("tools", default={})
if not isinstance(tools, dict):
    tools = {}
required_denies = {"group:runtime", "group:fs", "exec", "process", "write", "edit", "apply_patch"}
tool_denies = set(recursive_values(tools.get("deny", [])))
checks["tool_surface_bounded"] = (
    tools.get("profile") == "messaging"
    and required_denies <= tool_denies
    and get_path("tools", "elevated", "enabled", default=False) is not True
)
if config and not checks["tool_surface_bounded"]:
    safety_issues.append("openclaw_tool_surface_not_bounded")

# OpenClaw 2026.7.1-2 stores DM pairing approvals under credentials/*. Newer
# builds may migrate them to SQLite; inspect both forms read-only. The expected
# payload is {"version":1,"allowFrom":["<sender>"]}; only allowFrom values are
# parsed so timestamps/codes can never be mistaken for identities.
pairing_state_readable = True
credentials_dir = OPENCLAW_HOME / "credentials"
if credentials_dir.is_dir():
    for path in credentials_dir.glob("telegram*-allowFrom.json"):
        if not path.is_file() or path.is_symlink():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            allow_values = payload.get("allowFrom", []) if isinstance(payload, dict) else payload
            for value in recursive_values(allow_values):
                if (normalized := normalize_sender(value)) is not None:
                    approved_ids.add(normalized)
        except Exception:
            pairing_state_readable = False

state_db = OPENCLAW_HOME / "state/openclaw.sqlite"
if state_db.is_file() and not state_db.is_symlink():
    try:
        conn = sqlite3.connect(f"file:{state_db}?mode=ro", uri=True)
        try:
            has_table = conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name='channel_pairing_allow_entries'"
            ).fetchone()
            if has_table:
                for (entry,) in conn.execute(
                    "SELECT entry FROM channel_pairing_allow_entries WHERE lower(channel_key)='telegram'"
                ).fetchall():
                    if (normalized := normalize_sender(entry)) is not None:
                        approved_ids.add(normalized)
        finally:
            conn.close()
    except Exception:
        pairing_state_readable = False

checks["pairing_state_readable"] = pairing_state_readable
if not pairing_state_readable:
    hold_reasons.append("telegram_pairing_state_unreadable")

checks["owner_has_dm_admission"] = owner_id is not None and owner_id in approved_ids
if owner_id and not checks["owner_has_dm_admission"]:
    hold_reasons.append("telegram_owner_not_in_dm_admission_state")

checks["dm_admission_exact_owner_only"] = owner_id is not None and approved_ids == {owner_id}
if owner_id and approved_ids - {owner_id}:
    safety_issues.append("telegram_dm_admission_contains_non_owner")

# Runtime probes are read-only: no config set, install, restart, repair, approval,
# publish, send, merge, payment, or production mutation is invoked.
version = "unknown"
node_path = str(node_dir) if node_dir else ""
openclaw_path = ":".join(
    [node_path, str(OPENCLAW_HOME / "bin"), f"/home/{RUN_USER}/.local/bin", "/usr/local/bin", "/usr/bin", "/bin"]
)

def oc_args(*args: str) -> list[str]:
    return [
        "sudo",
        "-iu",
        RUN_USER,
        "env",
        f"HOME=/home/{RUN_USER}",
        f"PATH={openclaw_path}",
        str(OPENCLAW_BIN),
        *args,
    ]

if checks["openclaw_binary"] and checks["bundled_node_runtime"]:
    version_run = run(oc_args("--version"), capture=True)
    if version_run.returncode == 0:
        version = re.sub(r"[^A-Za-z0-9.+_ -]", "", version_run.stdout.strip())[:80] or "unknown"
    checks["gateway_rpc"] = run(oc_args("gateway", "status", "--require-rpc")).returncode == 0
    checks["telegram_probe"] = run(oc_args("channels", "status", "--channel", "telegram", "--probe")).returncode == 0
    checks["pairing_cli_read"] = run(oc_args("pairing", "list", "telegram", "--json")).returncode == 0
else:
    checks["gateway_rpc"] = False
    checks["telegram_probe"] = False
    checks["pairing_cli_read"] = False

for name in ("gateway_rpc", "telegram_probe", "pairing_cli_read"):
    if not checks[name]:
        hold_reasons.append(f"runtime_{name}_not_proven")

listeners_run = run(["ss", "-ltnH"], capture=True)
listener_addresses: list[str] = []
if listeners_run.returncode == 0:
    for line in listeners_run.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 4 and parts[3].endswith(":18789"):
            listener_addresses.append(parts[3])
allowed_listener_addresses = {"127.0.0.1:18789", "[::1]:18789", "::1:18789"}
checks["port_18789_loopback_only"] = bool(listener_addresses) and set(listener_addresses) <= allowed_listener_addresses
if listener_addresses and not checks["port_18789_loopback_only"]:
    safety_issues.append("openclaw_listener_not_loopback_only")
elif not listener_addresses:
    hold_reasons.append("openclaw_listener_not_observed")

unknown_identity_deny_ok = (
    checks["telegram_dm_pairing"]
    and checks["command_allowlist_narrow"]
    and owner_id is not None
    and checks["dm_admission_exact_owner_only"]
)
checks["unknown_identity_deny"] = unknown_identity_deny_ok
if owner_id and not unknown_identity_deny_ok and not safety_issues:
    hold_reasons.append("unknown_identity_deny_not_fully_proven")

# PASS requires every runtime/identity prerequisite. Unsafe authorization or
# secret posture is FAIL. Safe but incomplete runtime evidence is HOLD.
pass_requirements = (
    checks["openclaw_binary"],
    checks["bundled_node_runtime"],
    checks["openclaw_config_regular_0600"],
    checks["gateway_config_loopback"],
    checks["telegram_enabled"],
    checks["telegram_dm_pairing"],
    checks["telegram_groups_disabled"],
    checks["telegram_secret_file_private"],
    checks["exact_telegram_command_owner"],
    checks["command_allowlist_narrow"],
    checks["tool_surface_bounded"],
    checks["pairing_state_readable"],
    checks["owner_has_dm_admission"],
    checks["dm_admission_exact_owner_only"],
    checks["unknown_identity_deny"],
    checks["gateway_rpc"],
    checks["telegram_probe"],
    checks["pairing_cli_read"],
    checks["port_18789_loopback_only"],
)

if safety_issues:
    verdict = "FAIL"
    exit_code = 1
elif all(pass_requirements):
    verdict = "PASS"
    exit_code = 0
else:
    verdict = "HOLD"
    exit_code = 4

receipt = {
    "schema": "dealix.founder-command-runtime-receipt.v1",
    "source_sha": head,
    "verdict": verdict,
    "authority_class": "L4_READ_ONLY_RUNTIME_ACCEPTANCE",
    "external_effects": "NONE_FAIL_CLOSED",
    "openclaw_version": version,
    "telegram_owner_identity": "VERIFIED" if checks["exact_telegram_command_owner"] and checks["owner_has_dm_admission"] else "UNKNOWN_NOT_EVIDENCE_BACKED",
    "telegram_owner_fingerprint": owner_fp,
    "telegram_unknown_identity_deny": "VERIFIED" if checks["unknown_identity_deny"] else "UNKNOWN_NOT_EVIDENCE_BACKED",
    "telegram_gateway_loopback": "VERIFIED" if checks["gateway_config_loopback"] and checks["port_18789_loopback_only"] else "UNKNOWN_NOT_EVIDENCE_BACKED",
    "telegram_groups_disabled_by_default": "VERIFIED" if checks["telegram_groups_disabled"] else "FAILED",
    "openclaw_secretref_audit": "VERIFIED" if checks["telegram_secret_file_private"] else "UNKNOWN_NOT_EVIDENCE_BACKED",
    "checks": checks,
    "safety_issues": sorted(set(safety_issues)),
    "hold_reasons": sorted(set(hold_reasons)),
    "secret_values_printed": False,
    "owner_raw_id_printed": False,
    "openclaw_config_mutated": False,
    "gateway_restarted": False,
}
write_receipt(receipt_path, receipt)

print(f"DEALIX_FOUNDER_COMMAND_ACCEPTANCE={verdict}")
print(f"source_sha={head}")
print(f"openclaw_version={version}")
print(f"owner_identity_fingerprint={owner_fp or 'unknown'}")
print(f"gateway_rpc={'PASS' if checks['gateway_rpc'] else 'NOT_PASS'}")
print(f"telegram_probe={'PASS' if checks['telegram_probe'] else 'NOT_PASS'}")
print(f"loopback_listener={'PASS' if checks['port_18789_loopback_only'] else 'NOT_PASS'}")
print("secret_values_printed=false")
print("owner_raw_id_printed=false")
print("openclaw_config_mutated=false")
print(f"receipt={receipt_path}")
raise SystemExit(exit_code)
PY
