#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

RUN_USER="dealix"
OPENCLAW_HOME="/home/${RUN_USER}/.openclaw"
OPENCLAW_BIN="${OPENCLAW_HOME}/bin/openclaw"
CONFIG="${OPENCLAW_HOME}/openclaw.json"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="${CONFIG}.pre-compaction-repair-${STAMP}.bak"
PROOF_DIR="/opt/dealix/logs"
PROOF="${PROOF_DIR}/openclaw-compaction-repair-${STAMP}.log"
CONTEXT_WINDOW="${DEALIX_OPENCLAW_CONTEXT_WINDOW:-32768}"
MAX_TOKENS="${DEALIX_OPENCLAW_MAX_TOKENS:-4096}"
RESERVE_FLOOR="${DEALIX_OPENCLAW_RESERVE_FLOOR:-24000}"
KEEP_RECENT="${DEALIX_OPENCLAW_KEEP_RECENT:-8000}"
MODEL="${DEALIX_OPENCLAW_MODEL:-qwen3:4b-instruct-2507-q4_K_M}"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "BLOCKED: run as root"
  exit 2
fi

for pair in \
  "CONTEXT_WINDOW:$CONTEXT_WINDOW:16384:131072" \
  "MAX_TOKENS:$MAX_TOKENS:1024:16384" \
  "RESERVE_FLOOR:$RESERVE_FLOOR:0:65536" \
  "KEEP_RECENT:$KEEP_RECENT:1000:32000"; do
  IFS=: read -r name value min max <<<"$pair"
  if ! [[ "$value" =~ ^[0-9]+$ ]] || (( value < min || value > max )); then
    echo "BLOCKED: $name=$value outside [$min,$max]"
    exit 3
  fi
done

if (( KEEP_RECENT >= CONTEXT_WINDOW )); then
  echo "BLOCKED: keepRecentTokens must be smaller than contextWindow"
  exit 3
fi

if [[ ! -x "$OPENCLAW_BIN" ]]; then
  echo "BLOCKED: OpenClaw binary missing: $OPENCLAW_BIN"
  exit 4
fi
if [[ ! -f "$CONFIG" ]]; then
  echo "BLOCKED: OpenClaw config missing: $CONFIG"
  exit 5
fi

mkdir -p "$PROOF_DIR"
touch "$PROOF"
chmod 0600 "$PROOF"
exec > >(tee -a "$PROOF") 2>&1

OPENCLAW_NODE_DIR="$(
  find "$OPENCLAW_HOME/tools" -maxdepth 3 -type f -name node -path '*/bin/node' -perm -111 -printf '%h\n' 2>/dev/null \
    | sort -V \
    | tail -1
)"
OPENCLAW_PATH="${OPENCLAW_NODE_DIR}:${OPENCLAW_HOME}/bin:/home/${RUN_USER}/.local/bin:/usr/local/bin:/usr/bin:/bin"

oc() {
  sudo -iu "$RUN_USER" env HOME="/home/${RUN_USER}" PATH="$OPENCLAW_PATH" "$OPENCLAW_BIN" "$@"
}

redact() {
  sed -E \
    -e 's#([0-9]{6,}:[A-Za-z0-9_-]{20,})#[REDACTED_TELEGRAM_TOKEN]#g' \
    -e 's#((apiKey|token|secret|password)[= :]+)[^ ,}\"]+#\1[REDACTED]#Ig'
}

rollback() {
  local rc=$?
  trap - ERR
  set +e
  echo "rollback=START rc=$rc"
  cp -a "$BACKUP" "$CONFIG"
  chown "$RUN_USER:$RUN_USER" "$CONFIG"
  chmod 0600 "$CONFIG"
  oc gateway restart 2>&1 | redact || true
  echo "rollback=COMPLETE"
  exit "$rc"
}

cp -a "$CONFIG" "$BACKUP"
chown "$RUN_USER:$RUN_USER" "$BACKUP"
chmod 0600 "$BACKUP"
trap rollback ERR

echo "timestamp=$(date -Is)"
echo "openclaw_version=$(oc --version 2>/dev/null || true)"
echo "model=$MODEL"
echo "target_context_window=$CONTEXT_WINDOW"
echo "target_max_tokens=$MAX_TOKENS"

echo "===== PRECHECK ====="
oc status --all 2>&1 | redact || true
oc gateway status 2>&1 | redact || true

# Expand the local Ollama model context. OpenClaw's compaction reserve is capped
# against the active model context, so the previous 8K window left too little
# headroom for a long-lived Telegram/Jobs session and its compaction summary.
OLLAMA_PROVIDER_JSON="$(python3 - "$MODEL" "$CONTEXT_WINDOW" "$MAX_TOKENS" <<'PY'
import json, sys
model, context, max_tokens = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
print(json.dumps({
  "baseUrl":"http://127.0.0.1:11434",
  "apiKey":"ollama-local",
  "api":"ollama",
  "timeoutSeconds":300,
  "contextWindow":context,
  "maxTokens":max_tokens,
  "models":[{
    "id":model,
    "name":model,
    "contextWindow":context,
    "maxTokens":max_tokens,
    "params":{"num_ctx":context,"thinking":False,"keep_alive":"10m"}
  }]
}))
PY
)"
oc config set models.providers.ollama "$OLLAMA_PROVIDER_JSON" --strict-json --merge >/dev/null
unset OLLAMA_PROVIDER_JSON
oc models set "ollama/${MODEL}" >/dev/null 2>&1 || true

# Safeguard compaction is deliberately more aggressive than the generic default:
# preserve a bounded recent tail, reserve enough housekeeping space, pre-check
# pressure during long tool turns, and rotate large transcripts after success.
oc config set agents.defaults.compaction.enabled true --strict-json >/dev/null
oc config set agents.defaults.compaction.mode safeguard >/dev/null 2>&1 || true
oc config set agents.defaults.compaction.reserveTokensFloor "$RESERVE_FLOOR" --strict-json >/dev/null
oc config set agents.defaults.compaction.keepRecentTokens "$KEEP_RECENT" --strict-json >/dev/null
oc config set agents.defaults.compaction.midTurnPrecheck.enabled true --strict-json >/dev/null 2>&1 || true
oc config set agents.defaults.compaction.qualityGuard.enabled true --strict-json >/dev/null 2>&1 || true
oc config set agents.defaults.compaction.qualityGuard.maxRetries 1 --strict-json >/dev/null 2>&1 || true
oc config set agents.defaults.compaction.truncateAfterCompaction true --strict-json >/dev/null 2>&1 || true
oc config set agents.defaults.compaction.maxActiveTranscriptBytes '20mb' >/dev/null 2>&1 || true
oc config set agents.defaults.compaction.notifyUser true --strict-json >/dev/null 2>&1 || true

# Validate config before restart. Never print the complete config because it may
# contain credential references or tokens.
oc config get agents.defaults.compaction >/dev/null
oc config get models.providers.ollama >/dev/null

echo "config_validation=PASS"

loginctl enable-linger "$RUN_USER" >/dev/null 2>&1 || true
oc gateway restart 2>&1 | redact
sleep 3

if ! oc gateway status --require-rpc >/dev/null 2>&1; then
  echo "gateway_after_restart=FAIL"
  false
fi
if ! curl -fsS --max-time 10 http://127.0.0.1:11434/api/tags >/dev/null; then
  echo "ollama_after_restart=FAIL"
  false
fi

echo "gateway_after_restart=PASS"
echo "ollama_after_restart=PASS"

# Print only non-secret compaction/model facts as the durable receipt.
python3 - "$CONFIG" "$MODEL" <<'PY'
import json, sys
from pathlib import Path
p=Path(sys.argv[1]); model=sys.argv[2]
data=json.loads(p.read_text(encoding='utf-8'))
comp=data.get('agents',{}).get('defaults',{}).get('compaction',{})
provider=data.get('models',{}).get('providers',{}).get('ollama',{})
models=provider.get('models',[]) if isinstance(provider,dict) else []
selected=next((m for m in models if isinstance(m,dict) and m.get('id')==model), {})
print('compaction_enabled=' + str(comp.get('enabled')).lower())
print('compaction_mode=' + str(comp.get('mode','unknown')))
print('reserveTokensFloor=' + str(comp.get('reserveTokensFloor','unknown')))
print('keepRecentTokens=' + str(comp.get('keepRecentTokens','unknown')))
print('midTurnPrecheck=' + str(comp.get('midTurnPrecheck',{}).get('enabled','unknown')).lower())
print('contextWindow=' + str(selected.get('contextWindow', provider.get('contextWindow','unknown'))))
print('maxTokens=' + str(selected.get('maxTokens', provider.get('maxTokens','unknown'))))
PY

trap - ERR
echo "OPENCLAW_COMPACTION_REPAIR=PASS"
echo "proof=$PROOF"
