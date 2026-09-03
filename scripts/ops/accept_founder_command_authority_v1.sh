#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

ROOT="$(git rev-parse --show-toplevel)"
EXPECTED_SHA="${1:-}"
ACTUAL_SHA="$(git -C "$ROOT" rev-parse HEAD)"
RUN_USER="dealix"
OPENCLAW_HOME="/home/${RUN_USER}/.openclaw"
OPENCLAW_BIN="${OPENCLAW_HOME}/bin/openclaw"
CONFIG="${OPENCLAW_HOME}/openclaw.json"
PROOF_ROOT="${DEALIX_FOUNDER_COMMAND_PROOF_ROOT:-/opt/dealix/control/proof/founder-command/${ACTUAL_SHA}}"

if [[ -z "$EXPECTED_SHA" ]]; then
  echo "DEALIX_FOUNDER_COMMAND_ACCEPTANCE=BLOCKED_EXPECTED_SHA_REQUIRED"
  exit 2
fi

if [[ "$ACTUAL_SHA" != "$EXPECTED_SHA" ]]; then
  echo "DEALIX_FOUNDER_COMMAND_ACCEPTANCE=BLOCKED_HEAD_MISMATCH"
  echo "expected=$EXPECTED_SHA"
  echo "actual=$ACTUAL_SHA"
  exit 2
fi

if [[ "$(id -u)" -ne 0 ]]; then
  echo "DEALIX_FOUNDER_COMMAND_ACCEPTANCE=BLOCKED_ROOT_REQUIRED_FOR_READ_ONLY_RUNTIME_EVIDENCE"
  exit 3
fi

mkdir -p "$PROOF_ROOT"
chmod 0700 "$PROOF_ROOT"

export DEALIX_EXTERNAL_SEND=0
export DEALIX_EMAIL_LIVE_SEND=0
export DEALIX_WHATSAPP_OUTBOUND=0
export DEALIX_PUBLIC_PUBLISH=0
export DEALIX_PAID_SPEND=0
export DEALIX_PAYMENT_EXECUTION=0
export DEALIX_PRODUCTION_MUTATION=0
export DEALIX_DNS_MUTATION=0
export DEALIX_DB_MUTATION=0
export DEALIX_SECRET_MUTATION=0
export DEALIX_IDENTITY_MUTATION=0
export DEALIX_AGENT_SELF_AUTHORITY=0
export DEALIX_AUTONOMY_LEVEL=4
export DEALIX_MODE=draft-only

# OpenClaw may use a private bundled Node runtime that is absent from the login
# shell PATH. Discover it read-only; never install or mutate runtime state here.
OPENCLAW_NODE_DIR="${DEALIX_OPENCLAW_NODE_DIR:-}"
if [[ -z "$OPENCLAW_NODE_DIR" && -d "$OPENCLAW_HOME/tools" ]]; then
  OPENCLAW_NODE_DIR="$(
    find "$OPENCLAW_HOME/tools" -maxdepth 3 -type f -name node -path '*/bin/node' -perm -111 -printf '%h\n' 2>/dev/null \
      | sort -V \
      | tail -1
  )"
fi
OPENCLAW_PATH="${OPENCLAW_NODE_DIR}:${OPENCLAW_HOME}/bin:/home/${RUN_USER}/.local/bin:/usr/local/bin:/usr/bin:/bin"

oc() {
  sudo -iu "$RUN_USER" env \
    HOME="/home/${RUN_USER}" \
    PATH="$OPENCLAW_PATH" \
    "$OPENCLAW_BIN" "$@"
}

BINARY_OK=0
NODE_OK=0
CONFIG_PRESENT=0
[[ -x "$OPENCLAW_BIN" ]] && BINARY_OK=1
[[ -n "$OPENCLAW_NODE_DIR" && -x "$OPENCLAW_NODE_DIR/node" ]] && NODE_OK=1
[[ -f "$CONFIG" && ! -L "$CONFIG" ]] && CONFIG_PRESENT=1

CONFIG_EVIDENCE="$({
  /usr/bin/python3 - "$CONFIG" "$OPENCLAW_HOME" "$RUN_USER" <<'PY'
from __future__ import annotations

import hashlib
import json
import os
import pwd
import re
import sqlite3
import stat
import sys
from pathlib import Path
from typing import Any

config_path = Path(sys.argv[1])
home = Path(sys.argv[2])
run_user = sys.argv[3]

result: dict[str, Any] = {
    "config_safety_ok": False,
    "owner_identity_proven": False,
    "dm_access_proven": False,
    "secret_reference_ok": False,
    "owner_fingerprint": None,
    "issues": [],
}
issues: list[str] = result["issues"]

try:
    run_uid = pwd.getpwnam(run_user).pw_uid
except KeyError:
    issues.append("dealix_user_missing")
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0)

if not config_path.is_file() or config_path.is_symlink():
    issues.append("openclaw_config_missing_or_symlink")
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0)

st = config_path.stat()
if stat.S_IMODE(st.st_mode) & 0o077:
    issues.append("openclaw_config_permissions_too_broad")

try:
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
except Exception:
    issues.append("openclaw_config_invalid_json")
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0)


def get_path(obj: Any, *keys: str, default: Any = None) -> Any:
    cur = obj
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def strings(value: Any) -> list[str]:
    out: list[str] = []
    if isinstance(value, str):
        out.append(value)
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        out.append(str(value))
    elif isinstance(value, list):
        for item in value:
            out.extend(strings(item))
    elif isinstance(value, dict):
        for item in value.values():
            out.extend(strings(item))
    return out


def normalize_sender(value: str) -> str | None:
    value = value.strip()
    m = re.fullmatch(r"(?:telegram:|tg:)?([0-9]{4,20})", value, flags=re.IGNORECASE)
    return m.group(1) if m else None

# Core gateway posture.
if get_path(cfg, "gateway", "mode") != "local":
    issues.append("gateway_mode_not_local")
if get_path(cfg, "gateway", "bind") != "loopback":
    issues.append("gateway_bind_not_loopback")
if int(get_path(cfg, "gateway", "port", default=0) or 0) != 18789:
    issues.append("gateway_port_not_18789")

telegram = get_path(cfg, "channels", "telegram", default={})
if not isinstance(telegram, dict):
    telegram = {}
    issues.append("telegram_config_missing")
if telegram.get("enabled") is not True:
    issues.append("telegram_not_enabled")
if telegram.get("dmPolicy") != "pairing":
    issues.append("telegram_dm_policy_not_pairing")
if telegram.get("groups", {}) != {}:
    issues.append("telegram_groups_not_empty")
if telegram.get("groupAllowFrom", []) not in ([], None):
    issues.append("telegram_group_allow_from_not_empty")

allow_from_raw = strings(telegram.get("allowFrom", []))
if any(item.strip() == "*" for item in allow_from_raw):
    issues.append("telegram_dm_wildcard_present")
explicit_dm_ids = {norm for item in allow_from_raw if (norm := normalize_sender(item))}

# Secret-bearing Telegram credential must be referenced through a private file.
if telegram.get("botToken") not in (None, ""):
    issues.append("telegram_inline_bot_token_present")
token_file_raw = telegram.get("tokenFile")
if not isinstance(token_file_raw, str) or not token_file_raw.startswith("/"):
    issues.append("telegram_token_file_missing_or_not_absolute")
else:
    token_file = Path(token_file_raw)
    allowed_secret_root = Path(f"/home/{run_user}/.config/dealix-secrets")
    try:
        token_file.relative_to(allowed_secret_root)
    except ValueError:
        issues.append("telegram_token_file_outside_dealix_secret_root")
    if not token_file.is_file() or token_file.is_symlink():
        issues.append("telegram_token_file_missing_or_symlink")
    else:
        token_stat = token_file.stat()
        if token_stat.st_uid != run_uid:
            issues.append("telegram_token_file_wrong_owner")
        if stat.S_IMODE(token_stat.st_mode) != 0o600:
            issues.append("telegram_token_file_permissions_not_0600")
        if not issues or not any(code.startswith("telegram_token_file_") for code in issues):
            result["secret_reference_ok"] = True

# Owner-only privileged command identity must be exactly one Telegram numeric ID.
owner_values = strings(get_path(cfg, "commands", "ownerAllowFrom", default=[]))
owner_ids: list[str] = []
for value in owner_values:
    match = re.fullmatch(r"telegram:([0-9]{4,20})", value.strip(), flags=re.IGNORECASE)
    if match:
        owner_ids.append(match.group(1))
    else:
        issues.append("non_telegram_or_invalid_command_owner")
owner_ids = sorted(set(owner_ids))
if len(owner_ids) != 1:
    issues.append("exactly_one_telegram_command_owner_required")
    owner_id = None
else:
    owner_id = owner_ids[0]
    result["owner_identity_proven"] = True
    result["owner_fingerprint"] = "sha256:" + hashlib.sha256(
        f"telegram:{owner_id}".encode("utf-8")
    ).hexdigest()[:20]

# commands.allowFrom, when present in this OpenClaw generation, is a separate
# command authorization boundary. It must never contain a wildcard. If Telegram
# has an explicit command allowlist, it must contain only the exact owner.
command_allow = get_path(cfg, "commands", "allowFrom", default=None)
if command_allow is not None:
    if any(value.strip() == "*" for value in strings(command_allow)):
        issues.append("command_allow_from_wildcard_present")
    if isinstance(command_allow, dict) and owner_id:
        telegram_cmd = command_allow.get("telegram")
        if telegram_cmd is not None:
            command_ids = {norm for item in strings(telegram_cmd) if (norm := normalize_sender(item))}
            if command_ids != {owner_id}:
                issues.append("telegram_command_allowlist_not_exact_owner")

# Tool surface must remain messaging-only and explicitly deny runtime/fs writes.
tools = get_path(cfg, "tools", default={})
if not isinstance(tools, dict):
    tools = {}
if tools.get("profile") != "messaging":
    issues.append("tools_profile_not_messaging")
required_denies = {"group:runtime", "group:fs", "exec", "process", "write", "edit", "apply_patch"}
deny_values = set(strings(tools.get("deny", [])))
if not required_denies <= deny_values:
    issues.append("required_tool_denies_missing")
elevated_enabled = get_path(cfg, "tools", "elevated", "enabled", default=False)
if elevated_enabled is True:
    issues.append("elevated_tools_enabled")

# Verify the owner has actual DM admission evidence. OpenClaw 2026.7.1-2 uses
# credential allowFrom files; newer installations may migrate this state to
# SQLite. Read both forms without exposing the sender ID.
approved_ids: set[str] = set(explicit_dm_ids)
credentials = home / "credentials"
if credentials.is_dir():
    for path in credentials.glob("telegram*-allowFrom.json"):
        try:
            if path.is_file() and not path.is_symlink():
                payload = json.loads(path.read_text(encoding="utf-8"))
                for value in strings(payload):
                    if norm := normalize_sender(value):
                        approved_ids.add(norm)
        except Exception:
            issues.append("telegram_pairing_store_unreadable")

state_db = home / "state/openclaw.sqlite"
if state_db.is_file() and not state_db.is_symlink():
    try:
        conn = sqlite3.connect(f"file:{state_db}?mode=ro", uri=True)
        try:
            exists = conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name='channel_pairing_allow_entries'"
            ).fetchone()
            if exists:
                rows = conn.execute(
                    "SELECT entry FROM channel_pairing_allow_entries WHERE lower(channel_key)='telegram'"
                ).fetchall()
                for (entry,) in rows:
                    if norm := normalize_sender(str(entry)):
                        approved_ids.add(norm)
        finally:
            conn.close()
    except Exception:
        issues.append("telegram_pairing_state_db_unreadable")

if owner_id and owner_id in approved_ids:
    result["dm_access_proven"] = True
else:
    issues.append("telegram_owner_not_found_in_dm_admission_state")

# Safety posture excludes owner/pairing availability and secret-file presence;
# those are acceptance prerequisites that should HOLD rather than falsely PASS.
safety_issue_prefixes = (
    "gateway_",
    "telegram_dm_policy_",
    "telegram_groups_",
    "telegram_group_allow_",
    "telegram_dm_wildcard_",
    "telegram_inline_",
    "command_allow_",
    "telegram_command_allowlist_",
    "tools_profile_",
    "required_tool_denies_",
    "elevated_tools_",
    "non_telegram_or_invalid_command_owner",
)
result["config_safety_ok"] = not any(issue.startswith(safety_issue_prefixes) for issue in issues)

print(json.dumps(result, sort_keys=True))
PY
} 2>/dev/null)"

CONFIG_SAFETY_OK="$(/usr/bin/python3 -c 'import json,sys; print(1 if json.loads(sys.argv[1]).get("config_safety_ok") else 0)' "$CONFIG_EVIDENCE")"
OWNER_PROVEN="$(/usr/bin/python3 -c 'import json,sys; print(1 if json.loads(sys.argv[1]).get("owner_identity_proven") else 0)' "$CONFIG_EVIDENCE")"
DM_ACCESS_PROVEN="$(/usr/bin/python3 -c 'import json,sys; print(1 if json.loads(sys.argv[1]).get("dm_access_proven") else 0)' "$CONFIG_EVIDENCE")"
SECRET_REF_OK="$(/usr/bin/python3 -c 'import json,sys; print(1 if json.loads(sys.argv[1]).get("secret_reference_ok") else 0)' "$CONFIG_EVIDENCE")"
OWNER_FINGERPRINT="$(/usr/bin/python3 -c 'import json,sys; print(json.loads(sys.argv[1]).get("owner_fingerprint") or "unknown")' "$CONFIG_EVIDENCE")"
ISSUES_JSON="$(/usr/bin/python3 -c 'import json,sys; print(json.dumps(json.loads(sys.argv[1]).get("issues", []), separators=(",",":")))' "$CONFIG_EVIDENCE")"

VERSION="unknown"
GATEWAY_RPC_OK=0
TELEGRAM_PROBE_OK=0
PAIRING_CLI_OK=0
LOOPBACK_LISTENER_OK=0

if [[ "$BINARY_OK" -eq 1 && "$NODE_OK" -eq 1 ]]; then
  VERSION="$(oc --version 2>/dev/null | head -1 | tr -cd '[:alnum:].+_- ' || true)"
  if oc gateway status --require-rpc >/dev/null 2>&1; then
    GATEWAY_RPC_OK=1
  fi
  if oc channels status --channel telegram --probe >/dev/null 2>&1; then
    TELEGRAM_PROBE_OK=1
  fi
  if oc pairing list telegram --json >/dev/null 2>&1; then
    PAIRING_CLI_OK=1
  fi
fi

LISTENERS="$(ss -ltnH 2>/dev/null | awk '$4 ~ /:18789$/ {print $4}' || true)"
if [[ -n "$LISTENERS" ]]; then
  LOOPBACK_LISTENER_OK=1
  while IFS= read -r addr; do
    case "$addr" in
      127.0.0.1:18789|[[]::1[]]:18789|::1:18789) ;;
      *) LOOPBACK_LISTENER_OK=0 ;;
    esac
  done <<< "$LISTENERS"
fi

FINAL="PASS"
EXIT_CODE=0
if [[ "$CONFIG_SAFETY_OK" -ne 1 || "$LOOPBACK_LISTENER_OK" -ne 1 ]]; then
  FINAL="FAIL"
  EXIT_CODE=1
elif [[ \
  "$BINARY_OK" -ne 1 || \
  "$NODE_OK" -ne 1 || \
  "$CONFIG_PRESENT" -ne 1 || \
  "$OWNER_PROVEN" -ne 1 || \
  "$DM_ACCESS_PROVEN" -ne 1 || \
  "$SECRET_REF_OK" -ne 1 || \
  "$GATEWAY_RPC_OK" -ne 1 || \
  "$TELEGRAM_PROBE_OK" -ne 1 || \
  "$PAIRING_CLI_OK" -ne 1 \
]]; then
  FINAL="HOLD"
  EXIT_CODE=4
fi

CREATED_AT="$(date -u +%FT%TZ)"
/usr/bin/python3 - \
  "$PROOF_ROOT/receipt.json" \
  "$ACTUAL_SHA" \
  "$CREATED_AT" \
  "$VERSION" \
  "$FINAL" \
  "$OWNER_FINGERPRINT" \
  "$ISSUES_JSON" \
  "$BINARY_OK" \
  "$NODE_OK" \
  "$CONFIG_PRESENT" \
  "$CONFIG_SAFETY_OK" \
  "$OWNER_PROVEN" \
  "$DM_ACCESS_PROVEN" \
  "$SECRET_REF_OK" \
  "$GATEWAY_RPC_OK" \
  "$TELEGRAM_PROBE_OK" \
  "$PAIRING_CLI_OK" \
  "$LOOPBACK_LISTENER_OK" <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path

(
    receipt_path,
    sha,
    created_at,
    version,
    verdict,
    owner_fp,
    issues_json,
    binary_ok,
    node_ok,
    config_present,
    config_safety_ok,
    owner_proven,
    dm_access_proven,
    secret_ref_ok,
    gateway_rpc_ok,
    telegram_probe_ok,
    pairing_cli_ok,
    loopback_listener_ok,
) = sys.argv[1:]

def b(value: str) -> bool:
    return value == "1"

receipt = {
    "schema": "dealix.founder-command-runtime-receipt.v1",
    "source_sha": sha,
    "created_at": created_at,
    "verdict": verdict,
    "authority_class": "L4_READ_ONLY_RUNTIME_ACCEPTANCE",
    "external_effects": "NONE_FAIL_CLOSED",
    "openclaw_version": version,
    "telegram_owner_identity": "VERIFIED" if b(owner_proven) and b(dm_access_proven) else "UNKNOWN_NOT_EVIDENCE_BACKED",
    "telegram_owner_fingerprint": owner_fp if owner_fp != "unknown" else None,
    "telegram_unknown_identity_deny": "VERIFIED" if b(config_safety_ok) else "FAILED",
    "telegram_gateway_loopback": "VERIFIED" if b(loopback_listener_ok) else "FAILED",
    "telegram_groups_disabled_by_default": "VERIFIED" if b(config_safety_ok) else "FAILED",
    "openclaw_secretref_audit": "VERIFIED" if b(secret_ref_ok) else "UNKNOWN_NOT_EVIDENCE_BACKED",
    "checks": {
        "openclaw_binary": b(binary_ok),
        "bundled_node_runtime": b(node_ok),
        "config_present_regular_file": b(config_present),
        "config_safety": b(config_safety_ok),
        "exact_telegram_owner": b(owner_proven),
        "owner_has_dm_admission": b(dm_access_proven),
        "telegram_token_external_private_file": b(secret_ref_ok),
        "gateway_rpc": b(gateway_rpc_ok),
        "telegram_probe": b(telegram_probe_ok),
        "pairing_cli_read": b(pairing_cli_ok),
        "port_18789_loopback_only": b(loopback_listener_ok),
    },
    "issues": json.loads(issues_json),
    "secret_values_printed": False,
    "openclaw_config_mutated": False,
    "gateway_restarted": False,
}
Path(receipt_path).write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY
chmod 0600 "$PROOF_ROOT/receipt.json"
sha256sum "$PROOF_ROOT/receipt.json" > "$PROOF_ROOT/receipt.sha256"
chmod 0600 "$PROOF_ROOT/receipt.sha256"

echo "DEALIX_FOUNDER_COMMAND_ACCEPTANCE=$FINAL"
echo "source_sha=$ACTUAL_SHA"
echo "openclaw_version=$VERSION"
echo "owner_identity_fingerprint=$OWNER_FINGERPRINT"
echo "gateway_rpc=$([[ "$GATEWAY_RPC_OK" -eq 1 ]] && echo PASS || echo NOT_PASS)"
echo "telegram_probe=$([[ "$TELEGRAM_PROBE_OK" -eq 1 ]] && echo PASS || echo NOT_PASS)"
echo "loopback_listener=$([[ "$LOOPBACK_LISTENER_OK" -eq 1 ]] && echo PASS || echo NOT_PASS)"
echo "secret_values_printed=false"
echo "openclaw_config_mutated=false"
echo "receipt=$PROOF_ROOT/receipt.json"

exit "$EXIT_CODE"
