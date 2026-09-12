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
MODEL="${DEALIX_OPENCLAW_MODEL:-qwen3:4b-instruct-2507-q4_K_M}"
CONTEXT_TOKENS="${DEALIX_OPENCLAW_CONTEXT_TOKENS:-32768}"
MAX_TOKENS="${DEALIX_OPENCLAW_MAX_TOKENS:-1024}"
RESERVE_TOKENS="${DEALIX_OPENCLAW_RESERVE_TOKENS:-16384}"
RESERVE_FLOOR="${DEALIX_OPENCLAW_RESERVE_FLOOR:-20000}"
KEEP_RECENT="${DEALIX_OPENCLAW_KEEP_RECENT:-8192}"
SESSION_KEY="${DEALIX_OPENCLAW_SESSION_KEY:-agent:founder-president:main}"
SESSION_AGENT="${DEALIX_OPENCLAW_SESSION_AGENT:-founder-president}"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "BLOCKED: run as root"
  exit 2
fi

for pair in \
  "CONTEXT_TOKENS:$CONTEXT_TOKENS:16384:131072" \
  "MAX_TOKENS:$MAX_TOKENS:256:8192" \
  "RESERVE_TOKENS:$RESERVE_TOKENS:0:65536" \
  "RESERVE_FLOOR:$RESERVE_FLOOR:0:65536" \
  "KEEP_RECENT:$KEEP_RECENT:1000:32000"; do
  IFS=: read -r name value min max <<<"$pair"
  if ! [[ "$value" =~ ^[0-9]+$ ]] || (( value < min || value > max )); then
    echo "BLOCKED: $name=$value outside [$min,$max]"
    exit 3
  fi
done

if (( KEEP_RECENT >= CONTEXT_TOKENS )); then
  echo "BLOCKED: keepRecentTokens must be smaller than contextTokens"
  exit 3
fi

if [[ ! -x "$OPENCLAW_BIN" || ! -f "$CONFIG" ]]; then
  echo "BLOCKED: OpenClaw binary/config missing"
  exit 4
fi

mkdir -p "$PROOF_DIR"
touch "$PROOF"
chmod 0600 "$PROOF"
exec > >(tee -a "$PROOF") 2>&1

OPENCLAW_NODE_DIR="$(find "$OPENCLAW_HOME/tools" -maxdepth 3 -type f -name node -path '*/bin/node' -perm -111 -printf '%h\n' 2>/dev/null | sort -V | tail -1)"
OPENCLAW_PATH="${OPENCLAW_NODE_DIR}:${OPENCLAW_HOME}/bin:/home/${RUN_USER}/.local/bin:/usr/local/bin:/usr/bin:/bin"
oc() { sudo -iu "$RUN_USER" env HOME="/home/${RUN_USER}" PATH="$OPENCLAW_PATH" "$OPENCLAW_BIN" "$@"; }
redact() {
  sed -E \
    -e 's#([0-9]{6,}:[A-Za-z0-9_-]{20,})#[REDACTED_TELEGRAM_TOKEN]#g' \
    -e 's#((apiKey|token|secret|password)[= :]+)[^ ,}\"]+#\1[REDACTED]#Ig'
}
set_required() {
  local key="$1" value="$2"; shift 2
  oc config set "$key" "$value" "$@" >/dev/null
  echo "required_config_${key}=APPLIED"
}
set_optional() {
  local key="$1" value="$2"; shift 2
  if oc config set "$key" "$value" "$@" >/dev/null 2>&1; then
    echo "optional_config_${key}=APPLIED"
  else
    echo "optional_config_${key}=UNSUPPORTED_SKIP"
  fi
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
echo "mem_available_kb=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)"
echo "model=$MODEL"
echo "target_context_tokens=$CONTEXT_TOKENS"

echo "===== PRECHECK ====="
oc gateway status --require-rpc 2>&1 | redact
curl -fsS --max-time 10 http://127.0.0.1:11434/api/tags >/dev/null
echo "precheck_gateway_ollama=PASS"

# The live Jobs failure advertised a 32K context window while effective
# contextTokens and Ollama num_ctx were still pinned to 8K. Keep metadata and
# the actual request context aligned so compaction has real headroom.
OLLAMA_PROVIDER_JSON="$(python3 - "$MODEL" "$CONTEXT_TOKENS" "$MAX_TOKENS" <<'PY'
import json, sys
model, context, max_tokens = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
print(json.dumps({
  "baseUrl":"http://127.0.0.1:11434",
  "apiKey":"ollama-local",
  "api":"ollama",
  "timeoutSeconds":300,
  "models":[{
    "id":model,
    "name":model,
    "contextWindow":context,
    "contextTokens":context,
    "maxTokens":max_tokens,
    "params":{
      "num_ctx":context,
      "num_predict":max_tokens,
      "thinking":False,
      "keep_alive":"30m"
    }
  }]
}))
PY
)"
set_required models.providers.ollama "$OLLAMA_PROVIDER_JSON" --strict-json --merge
unset OLLAMA_PROVIDER_JSON

# The Dealix router intentionally rejects stream=true. Tell OpenClaw's custom
# provider model not to stream, then keep founder-president local-first so a
# router format mismatch cannot break Telegram/Jobs liveness.
CURRENT_ROUTER="$(oc config get models.providers.dealix-router 2>/dev/null || true)"
if [[ -n "$CURRENT_ROUTER" ]]; then
  ROUTER_JSON="$(python3 -c 'import json,sys; d=json.load(sys.stdin); [m.setdefault("params",{}).__setitem__("streaming",False) for m in d.get("models",[]) if isinstance(m,dict)]; print(json.dumps(d))' <<<"$CURRENT_ROUTER")"
  set_required models.providers.dealix-router "$ROUTER_JSON" --strict-json --merge
  unset ROUTER_JSON CURRENT_ROUTER
else
  echo "router_provider=ABSENT_SKIP"
fi

python3 - "$CONFIG" "$MODEL" "$SESSION_AGENT" <<'PY'
import json, os, sys
from pathlib import Path
p=Path(sys.argv[1]); model=sys.argv[2]; agent_id=sys.argv[3]
data=json.loads(p.read_text(encoding="utf-8"))
local=f"ollama/{model}"
found=False
for agent in data.get("agents",{}).get("list",[]):
    if isinstance(agent,dict) and agent.get("id")==agent_id:
        old=agent.get("model") if isinstance(agent.get("model"),dict) else {}
        fallbacks=[]
        old_primary=old.get("primary")
        if old_primary and old_primary != local:
            fallbacks.append(old_primary)
        for item in old.get("fallbacks",[]) or []:
            if item and item != local and item not in fallbacks:
                fallbacks.append(item)
        agent["model"]={"primary":local,"fallbacks":fallbacks}
        found=True
        break
if not found:
    raise SystemExit(f"agent not found: {agent_id}")
tmp=p.with_name(p.name+".tmp-repair")
tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
os.chmod(tmp,0o600)
os.replace(tmp,p)
PY
chown "$RUN_USER:$RUN_USER" "$CONFIG"
chmod 0600 "$CONFIG"
echo "founder_route=LOCAL_FIRST"

# Core values are supported by the installed runtime. The floor is >=20K as
# recommended by the observed OpenClaw failure, with a bounded recent tail.
set_required agents.defaults.compaction.mode safeguard
set_required agents.defaults.compaction.reserveTokens "$RESERVE_TOKENS" --strict-json
set_required agents.defaults.compaction.reserveTokensFloor "$RESERVE_FLOOR" --strict-json
set_required agents.defaults.compaction.keepRecentTokens "$KEEP_RECENT" --strict-json

# Newer protections are opportunistic for version compatibility.
set_optional agents.defaults.compaction.enabled true --strict-json
set_optional agents.defaults.compaction.midTurnPrecheck.enabled true --strict-json
set_optional agents.defaults.compaction.qualityGuard.enabled true --strict-json
set_optional agents.defaults.compaction.qualityGuard.maxRetries 1 --strict-json
set_optional agents.defaults.compaction.truncateAfterCompaction true --strict-json
set_optional agents.defaults.compaction.maxActiveTranscriptBytes '10mb'
set_optional agents.defaults.compaction.notifyUser true --strict-json
set_optional agents.defaults.compaction.postIndexSync async

oc config get agents.defaults.compaction >/dev/null
oc config get models.providers.ollama >/dev/null
echo "config_validation=PASS"

loginctl enable-linger "$RUN_USER" >/dev/null 2>&1 || true
oc gateway restart 2>&1 | redact
sleep 3
oc gateway status --require-rpc >/dev/null
curl -fsS --max-time 10 http://127.0.0.1:11434/api/tags >/dev/null
echo "gateway_after_restart=PASS"
echo "ollama_after_restart=PASS"

# Recover the wedged Jobs key. A recently compacted but still blocked session is
# rotated with sessions.reset; OpenClaw preserves the prior compaction checkpoint
# in the session metadata rather than deleting the historical transcript.
set +e
COMPACT_OUT="$(oc sessions compact "$SESSION_KEY" --agent "$SESSION_AGENT" --timeout 180000 --json 2>&1)"
COMPACT_RC=$?
set -e
printf '%s\n' "$COMPACT_OUT" | redact
if [[ $COMPACT_RC -eq 0 ]] && grep -Eq '"(ok|compacted)"[[:space:]]*:[[:space:]]*true' <<<"$COMPACT_OUT"; then
  echo "session_recovery=COMPACTED"
elif grep -Eqi 'already[_ ]compacted|Already compacted' <<<"$COMPACT_OUT"; then
  PARAMS="$(python3 - "$SESSION_KEY" "$SESSION_AGENT" <<'PY'
import json,sys
print(json.dumps({"key":sys.argv[1],"agentId":sys.argv[2]}))
PY
)"
  set +e
  RESET_OUT="$(oc gateway call sessions.reset --params "$PARAMS" --timeout 30000 --json 2>&1)"
  RESET_RC=$?
  set -e
  printf '%s\n' "$RESET_OUT" | redact
  if [[ $RESET_RC -ne 0 ]] || ! grep -Eq '"ok"[[:space:]]*:[[:space:]]*true' <<<"$RESET_OUT"; then
    echo "session_reset=FAIL rc=$RESET_RC"
    false
  fi
  echo "session_recovery=RESET_AFTER_RECENT_COMPACTION"
else
  echo "session_compaction=FAIL rc=$COMPACT_RC"
  false
fi

# OpenClaw-path canary: no --deliver, no external side effect, explicit local
# model, and a fresh isolated session key.
CANARY_KEY="agent:${SESSION_AGENT}:compaction-repair-canary-${STAMP}"
set +e
CANARY_OUT="$(oc agent --agent "$SESSION_AGENT" --model "ollama/${MODEL}" --session-key "$CANARY_KEY" --message 'Reply exactly DEALIX_JOBS_LOCAL_OK' --timeout 300 --json 2>&1)"
CANARY_RC=$?
set -e
printf '%s\n' "$CANARY_OUT" | redact | tail -80
if [[ $CANARY_RC -ne 0 ]] || ! grep -q 'DEALIX_JOBS_LOCAL_OK' <<<"$CANARY_OUT"; then
  echo "local_canary=FAIL rc=$CANARY_RC"
  false
fi
echo "local_canary=PASS"

# Main Jobs key canary, also without delivery, proves the repaired mapping is
# usable through the exact founder-president lane.
set +e
MAIN_OUT="$(oc agent --agent "$SESSION_AGENT" --model "ollama/${MODEL}" --session-key "$SESSION_KEY" --message 'Reply exactly DEALIX_JOBS_MAIN_OK' --timeout 300 --json 2>&1)"
MAIN_RC=$?
set -e
printf '%s\n' "$MAIN_OUT" | redact | tail -80
if [[ $MAIN_RC -ne 0 ]] || ! grep -q 'DEALIX_JOBS_MAIN_OK' <<<"$MAIN_OUT"; then
  echo "main_jobs_canary=FAIL rc=$MAIN_RC"
  false
fi
echo "main_jobs_canary=PASS"

python3 - "$CONFIG" "$MODEL" "$SESSION_AGENT" <<'PY'
import json, sys
from pathlib import Path
data=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
model=sys.argv[2]; agent_id=sys.argv[3]
comp=data.get('agents',{}).get('defaults',{}).get('compaction',{})
provider=data.get('models',{}).get('providers',{}).get('ollama',{})
models=provider.get('models',[]) if isinstance(provider,dict) else []
selected=next((m for m in models if isinstance(m,dict) and m.get('id')==model), {})
agent=next((a for a in data.get('agents',{}).get('list',[]) if isinstance(a,dict) and a.get('id')==agent_id), {})
router=data.get('models',{}).get('providers',{}).get('dealix-router',{})
rmodels=router.get('models',[]) if isinstance(router,dict) else []
print('compaction_mode=' + str(comp.get('mode','unknown')))
print('reserveTokens=' + str(comp.get('reserveTokens','unknown')))
print('reserveTokensFloor=' + str(comp.get('reserveTokensFloor','unknown')))
print('keepRecentTokens=' + str(comp.get('keepRecentTokens','unknown')))
print('midTurnPrecheck=' + str(comp.get('midTurnPrecheck',{}).get('enabled','unsupported')).lower())
print('contextTokens=' + str(selected.get('contextTokens','unknown')))
print('ollama_num_ctx=' + str(selected.get('params',{}).get('num_ctx','unknown')))
print('founder_primary=' + str((agent.get('model') or {}).get('primary','unknown')))
print('router_streaming_false=' + str(all(m.get('params',{}).get('streaming') is False for m in rmodels) if rmodels else 'absent').lower())
PY

trap - ERR
echo "OPENCLAW_COMPACTION_REPAIR=PASS"
echo "proof=$PROOF"
