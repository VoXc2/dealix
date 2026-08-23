#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

RUN_USER="dealix"
OPENCLAW_BIN="/home/${RUN_USER}/.openclaw/bin/openclaw"
OPENCLAW_HOME="/home/${RUN_USER}/.openclaw"
CONFIG="${OPENCLAW_HOME}/openclaw.json"
MEMORY_DIR="${OPENCLAW_HOME}/workspace/memory"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="${CONFIG}.pre-gateway-repair-${STAMP}.bak"
PROOF="/opt/dealix/logs/openclaw-gateway-repair-${STAMP}.log"
EMBED_MODEL="nomic-embed-text"
GATEWAY_READY_TIMEOUT="${DEALIX_OPENCLAW_READY_TIMEOUT:-60}"
EARLY_ROLLBACK_ARMED=0
MEMORY_ROLLBACK_ARMED=0

# OpenClaw can install a private Node runtime that is intentionally absent from
# the login-shell PATH. Resolve the newest bundled runtime deterministically and
# pass it explicitly to every CLI invocation so acceptance does not depend on
# SSH/session profile state. An operator may override it for a reviewed runtime.
OPENCLAW_NODE_DIR="${DEALIX_OPENCLAW_NODE_DIR:-}"
if [[ -z "$OPENCLAW_NODE_DIR" ]]; then
  OPENCLAW_NODE_DIR="$(
    find "$OPENCLAW_HOME/tools" -maxdepth 3 -type f -name node -path '*/bin/node' -perm -111 -printf '%h\n' 2>/dev/null \
      | sort -V \
      | tail -1
  )"
fi
OPENCLAW_PATH="${OPENCLAW_NODE_DIR}:${OPENCLAW_HOME}/bin:/home/${RUN_USER}/.local/bin:/usr/local/bin:/usr/bin:/bin"

mkdir -p /opt/dealix/logs
touch "$PROOF"
chmod 0600 "$PROOF"
exec > >(tee -a "$PROOF") 2>&1

redact() {
  sed -E \
    -e 's#([0-9]{6,}:[A-Za-z0-9_-]{20,})#[REDACTED_TELEGRAM_TOKEN]#g' \
    -e 's#(gateway\.auth\.token[= :]+)[^ ,}\"]+#\1[REDACTED]#Ig' \
    -e 's#(Authorization: Bearer )[A-Za-z0-9._-]+#\1[REDACTED]#Ig' \
    -e 's#((apiKey|token|secret|password)[= :]+)[^ ,}\"]+#\1[REDACTED]#Ig'
}

oc() {
  sudo -iu "$RUN_USER" env \
    HOME="/home/${RUN_USER}" \
    PATH="$OPENCLAW_PATH" \
    "$OPENCLAW_BIN" "$@"
}

set_required() {
  local key="$1"
  local value="$2"
  shift 2
  if ! oc config set "$key" "$value" "$@" >/dev/null; then
    echo "BLOCKED: OpenClaw rejected required config key: $key"
    return 1
  fi
}

set_optional() {
  local key="$1"
  local value="$2"
  shift 2
  if oc config set "$key" "$value" "$@" >/dev/null 2>&1; then
    echo "optional_config_${key}=APPLIED"
  else
    echo "optional_config_${key}=UNSUPPORTED_SKIP"
  fi
}

restore_config_from() {
  local source="$1"
  cp -a "$source" "$CONFIG"
  chown "$RUN_USER:$RUN_USER" "$CONFIG"
  chmod 0600 "$CONFIG"
}

wait_for_gateway_ready() {
  local deadline=$((SECONDS + GATEWAY_READY_TIMEOUT))
  local status_tmp="/tmp/dealix-openclaw-ready.$$.txt"

  while (( SECONDS < deadline )); do
    if oc gateway status --require-rpc >"$status_tmp" 2>&1 \
       && ss -ltnH 2>/dev/null | awk '$4 ~ /:18789$/ {found=1} END {exit !found}'; then
      redact <"$status_tmp" || true
      rm -f "$status_tmp"
      echo "gateway_readiness=PASS"
      return 0
    fi
    sleep 2
  done

  echo "gateway_readiness=TIMEOUT seconds=${GATEWAY_READY_TIMEOUT}"
  redact <"$status_tmp" 2>/dev/null || true
  rm -f "$status_tmp"
  return 1
}

early_rollback() {
  local rc=$?
  trap - ERR
  if [[ "${EARLY_ROLLBACK_ARMED:-0}" == "1" ]]; then
    set +e
    echo "early_repair_rollback=START"
    restore_config_from "$BACKUP" || true
    oc gateway restart 2>&1 | redact || true
    echo "early_repair_rollback=COMPLETE"
  fi
  exit "$rc"
}

memory_rollback() {
  local rc=$?
  trap - ERR
  if [[ "${MEMORY_ROLLBACK_ARMED:-0}" == "1" \
     && -n "${MEMORY_BASE:-}" \
     && -f "$MEMORY_BASE" ]]; then
    set +e
    echo "memory_transaction_rollback=START"
    restore_config_from "$MEMORY_BASE" || true
    oc gateway restart 2>&1 | redact || true
    echo "memory_transaction_rollback=COMPLETE"
  fi
  exit "$rc"
}

sanitize_known_memory_keys() {
  local tmp="${CONFIG}.memory-sanitize-${STAMP}.tmp"
  /usr/bin/python3 - "$CONFIG" "$tmp" <<'PY'
import json
import sys
from pathlib import Path

source = Path(sys.argv[1])
target = Path(sys.argv[2])
data = json.loads(source.read_text(encoding="utf-8"))

memory = data.get("memory")
if isinstance(memory, dict):
    memory.pop("search", None)

agents = data.get("agents")
if isinstance(agents, dict):
    defaults = agents.get("defaults")
    if isinstance(defaults, dict):
        defaults.pop("memorySearch", None)

target.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
PY
  chown "$RUN_USER:$RUN_USER" "$tmp"
  chmod 0600 "$tmp"
  mv "$tmp" "$CONFIG"
}

if [[ "$(id -u)" -ne 0 ]]; then
  echo "BLOCKED: run as root"
  exit 2
fi

if ! [[ "$GATEWAY_READY_TIMEOUT" =~ ^[0-9]+$ ]] \
   || (( GATEWAY_READY_TIMEOUT < 10 || GATEWAY_READY_TIMEOUT > 180 )); then
  echo "BLOCKED: DEALIX_OPENCLAW_READY_TIMEOUT must be an integer from 10 to 180 seconds"
  exit 2
fi

if [[ ! -x "$OPENCLAW_BIN" ]]; then
  echo "BLOCKED: OpenClaw binary missing: $OPENCLAW_BIN"
  exit 3
fi

if [[ -z "$OPENCLAW_NODE_DIR" || ! -x "$OPENCLAW_NODE_DIR/node" ]]; then
  echo "BLOCKED: OpenClaw bundled Node runtime missing; set DEALIX_OPENCLAW_NODE_DIR only to a reviewed Node bin directory"
  exit 3
fi
echo "openclaw_node_runtime=$OPENCLAW_NODE_DIR/node"

if [[ ! -f "$CONFIG" ]]; then
  echo "BLOCKED: OpenClaw config missing: $CONFIG"
  exit 4
fi

cp -a "$CONFIG" "$BACKUP"
chown "$RUN_USER:$RUN_USER" "$BACKUP"
chmod 0600 "$BACKUP"

# From the first mutation through creation of the validated pre-memory baseline,
# any unexpected error restores the complete original config. This closes the
# failure window where schema sanitization or a required gateway write could
# otherwise leave a partially rewritten openclaw.json.
EARLY_ROLLBACK_ARMED=1
trap early_rollback ERR

# The merged repair may have left a docs-era memory.search subtree that the
# installed 2026.7.1-2 runtime cannot validate. Remove only the two known
# semantic-memory subtrees from the working copy before issuing any `config set`
# command. The full original config is retained in BACKUP and no value is printed.
echo "===== MEMORY BASELINE SANITIZE ====="
sanitize_known_memory_keys
echo "memory_baseline_sanitized=PASS"

echo "===== OPENCLAW PRE-REPAIR ====="
oc --version || true
oc status --all 2>&1 | redact || true
oc gateway probe 2>&1 | redact || true
oc gateway status 2>&1 | redact || true

echo
echo "===== DOCTOR READ-ONLY ====="
oc doctor 2>&1 | redact || true

# Re-assert only the Dealix-safe invariants required by this repair. Do not run
# broad `doctor --fix`: plugin/credential/config changes outside this scope are
# not needed to close the memory-schema defect.
echo
echo "===== REASSERT SAFE GATEWAY CONFIG ====="
set_required gateway.mode local
set_required gateway.bind loopback
set_required gateway.port 18789
set_required tools.profile messaging
set_required tools.deny '["group:runtime","group:fs","exec","process","write","edit","apply_patch"]' --strict-json
set_optional tools.elevated.enabled false
set_required channels.telegram.enabled true
set_required channels.telegram.dmPolicy pairing
# Founder control is DM-only by default. Never enable wildcard Telegram groups.
set_required channels.telegram.groups '{}' --strict-json
set_required channels.telegram.groupAllowFrom '[]' --strict-json

# OpenClaw memory is a local retrieval cache, not a second Company Brain.
# Probe each known schema atomically from the same validated pre-memory baseline.
echo
echo "===== LOCAL MEMORY CONFIG ====="
MEMORY_BASE="${CONFIG}.pre-memory-compat-${STAMP}.bak"
cp -a "$CONFIG" "$MEMORY_BASE"
chown "$RUN_USER:$RUN_USER" "$MEMORY_BASE"
chmod 0600 "$MEMORY_BASE"
# The validated pre-memory baseline is now the rollback source for the rest of
# the memory transaction. Keep ERR rollback armed through every fallible config,
# embedding, service, and acceptance operation; disarm only on terminal success
# or immediately before the explicit degraded rollback below.
EARLY_ROLLBACK_ARMED=0
MEMORY_ROLLBACK_ARMED=1
trap memory_rollback ERR
MEMORY_PREFIX=""

configure_memory_prefix() {
  local prefix="$1"
  restore_config_from "$MEMORY_BASE"

  oc config set "${prefix}.enabled" true >/dev/null 2>&1 || true
  oc config set "${prefix}.provider" ollama >/dev/null 2>&1 || return 1
  oc config set "${prefix}.model" "$EMBED_MODEL" >/dev/null 2>&1 || return 1
  oc config set "${prefix}.fallback" none >/dev/null 2>&1 || true
  oc config set "${prefix}.rememberAcrossConversations" false >/dev/null 2>&1 || true

  oc config get "${prefix}.provider" >/dev/null 2>&1 || return 1
  return 0
}

if configure_memory_prefix memory.search; then
  MEMORY_PREFIX="memory.search"
  echo "memory_schema=memory.search"
elif configure_memory_prefix agents.defaults.memorySearch; then
  MEMORY_PREFIX="agents.defaults.memorySearch"
  echo "memory_schema=agents.defaults.memorySearch"
else
  echo "BLOCKED: installed OpenClaw rejected both supported memory-search schemas"
  MEMORY_ROLLBACK_ARMED=0
  trap - ERR
  restore_config_from "$MEMORY_BASE"
  rm -f "$MEMORY_BASE"
  exit 11
fi

set_required "${MEMORY_PREFIX}.provider" ollama
set_required "${MEMORY_PREFIX}.model" "$EMBED_MODEL"
set_optional "${MEMORY_PREFIX}.fallback" none
set_optional "${MEMORY_PREFIX}.rememberAcrossConversations" false

# Ensure the local memory workspace exists before indexing. This is an internal
# filesystem prerequisite only; it creates no user-visible or external memory.
install -d -m 0700 -o "$RUN_USER" -g "$RUN_USER" "$MEMORY_DIR"
echo "memory_directory=READY path=$MEMORY_DIR"

# Ensure local Ollama is healthy and make embedding readiness deterministic.
echo
echo "===== OLLAMA ====="
if ! curl -fsS --max-time 10 http://127.0.0.1:11434/api/tags >/dev/null; then
  echo "ollama_api=FAIL"
  MEMORY_ROLLBACK_ARMED=0
  trap - ERR
  restore_config_from "$MEMORY_BASE"
  rm -f "$MEMORY_BASE"
  exit 12
fi
echo "ollama_api=PASS"

if ! ollama list 2>/dev/null \
  | awk 'NR>1 {name=$1; sub(/:latest$/, "", name); print name}' \
  | grep -Fxq "$EMBED_MODEL"; then
  echo "embedding_model=ABSENT_PULLING_LOCAL"
  if ! sudo -iu "$RUN_USER" ollama pull "$EMBED_MODEL"; then
    echo "embedding_model=PULL_FAIL"
    MEMORY_ROLLBACK_ARMED=0
    trap - ERR
    restore_config_from "$MEMORY_BASE"
    rm -f "$MEMORY_BASE"
    exit 13
  fi
else
  echo "embedding_model=PRESENT"
fi

EMBED_RESPONSE="$(mktemp /tmp/dealix-openclaw-embed.XXXXXX.json)"
if curl -fsS --max-time 60 \
  -H 'Content-Type: application/json' \
  -d '{"model":"nomic-embed-text","input":"Dealix local memory readiness probe"}' \
  http://127.0.0.1:11434/api/embed \
  > "$EMBED_RESPONSE" \
  && grep -q '"embeddings"' "$EMBED_RESPONSE"; then
  EMBED_RC=0
  echo "ollama_embedding_probe=PASS"
else
  EMBED_RC=1
  echo "ollama_embedding_probe=FAIL"
fi
rm -f "$EMBED_RESPONSE"

# Keep user service running after SSH logout.
loginctl enable-linger "$RUN_USER" >/dev/null 2>&1 || true

# Reinstall service metadata with current OpenClaw binary, then restart.
echo
echo "===== GATEWAY SERVICE REPAIR ====="
oc gateway install --force 2>&1 | redact || true
oc gateway restart 2>&1 | redact || true

# Gateway startup can legitimately take longer than a fixed sleep while Node,
# plugins and a local embedding model warm. Poll both RPC and the TCP listener
# inside a bounded window so a two-second warm-up is not misclassified as down.
if ! wait_for_gateway_ready; then
  echo "gateway_first_restart=FAIL"
  echo
  echo "===== REDACTED USER SERVICE JOURNAL ====="
  sudo -iu "$RUN_USER" bash -lc 'journalctl --user -u openclaw-gateway.service -n 120 --no-pager' 2>&1 | redact || true
  echo
  echo "===== SECOND RESTART ====="
  oc gateway restart 2>&1 | redact || true
  if ! wait_for_gateway_ready; then
    echo "gateway_second_restart=FAIL"
  fi
fi

echo
echo "===== MEMORY INDEX INITIALIZATION ====="
set +e
oc memory status --index --agent main 2>&1 | redact
INDEX_RC=${PIPESTATUS[0]}
set -e
if [[ $INDEX_RC -eq 0 ]]; then
  echo "memory_index_bootstrap=PASS"
else
  echo "memory_index_bootstrap=FAIL rc=${INDEX_RC}"
fi

echo
echo "===== FINAL OPENCLAW PROOF ====="
set +e
oc status --all 2>&1 | redact
STATUS_RC=${PIPESTATUS[0]}
oc gateway probe 2>&1 | redact
PROBE_RC=${PIPESTATUS[0]}
oc gateway status --require-rpc 2>&1 | redact
GATEWAY_RC=${PIPESTATUS[0]}
oc channels status --probe 2>&1 | redact
CHANNEL_RC=${PIPESTATUS[0]}
oc pairing list telegram 2>&1 | redact
PAIR_RC=${PIPESTATUS[0]}

MEMORY_OUTPUT="$(mktemp /tmp/dealix-openclaw-memory.XXXXXX.txt)"
oc memory status --deep >"$MEMORY_OUTPUT" 2>&1
MEMORY_RC=$?
redact <"$MEMORY_OUTPUT" || true
if grep -qiE 'no API key|missing.*openai|provider.*openai' "$MEMORY_OUTPUT"; then
  MEMORY_PROVIDER_RC=1
  echo "memory_provider_check=FAIL_REMOTE_OPENAI_DEPENDENCY"
else
  MEMORY_PROVIDER_RC=0
  echo "memory_provider_check=PASS_NO_REMOTE_OPENAI_DEPENDENCY"
fi
rm -f "$MEMORY_OUTPUT"
set -e

echo
echo "===== SECRET RESIDUE AUDIT (READ-ONLY) ====="
# Secret migration remains a separate controlled action because configure is
# interactive and can alter credential storage. Audit only in this repair.
oc secrets audit --check 2>&1 | redact || true

echo
echo "===== RESULT ====="
echo "status_rc=${STATUS_RC}"
echo "probe_rc=${PROBE_RC}"
echo "gateway_rc=${GATEWAY_RC}"
echo "channel_rc=${CHANNEL_RC}"
echo "pairing_rc=${PAIR_RC}"
echo "memory_index_rc=${INDEX_RC}"
echo "memory_rc=${MEMORY_RC}"
echo "memory_provider_rc=${MEMORY_PROVIDER_RC}"
echo "embedding_rc=${EMBED_RC}"
echo "memory_prefix=${MEMORY_PREFIX}"
echo "config_backup=${BACKUP}"
echo "proof=${PROOF}"

if [[ $STATUS_RC -eq 0 \
   && $GATEWAY_RC -eq 0 \
   && $PROBE_RC -eq 0 \
   && $CHANNEL_RC -eq 0 \
   && $INDEX_RC -eq 0 \
   && $MEMORY_RC -eq 0 \
   && $MEMORY_PROVIDER_RC -eq 0 \
   && $EMBED_RC -eq 0 ]]; then
  MEMORY_ROLLBACK_ARMED=0
  trap - ERR
  rm -f "$MEMORY_BASE"
  echo "OPENCLAW_GATEWAY_AND_MEMORY=PASS"
  exit 0
fi

# A failed acceptance must not leave the experimental memory configuration
# active. Restore the last validated loopback/Telegram/tool-safe baseline and
# restart the gateway. The original pre-repair config remains in BACKUP too.
MEMORY_ROLLBACK_ARMED=0
trap - ERR
echo "OPENCLAW_GATEWAY_AND_MEMORY=DEGRADED"
echo "memory_repair_rollback=START"
restore_config_from "$MEMORY_BASE"
rm -f "$MEMORY_BASE"
oc gateway restart 2>&1 | redact || true
echo "memory_repair_rollback=COMPLETE"
exit 20
