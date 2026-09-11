#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

# Bounded runtime guard for the existing Dealix VPS AI layer.
# It does not start Hermes, create a new scheduler, deploy production, or touch secrets.

MODEL="${DEALIX_LOCAL_MODEL:-qwen3:4b-instruct-2507-q4_K_M}"
LEGACY_MODEL="dealix-qwen3-4b-64k"
DROPIN_DIR="/etc/systemd/system/ollama.service.d"
DROPIN="$DROPIN_DIR/zzzzz-dealix-8k-guard.conf"
ROUTER_DROPIN_DIR="/etc/systemd/system/dealix-llm-router.service.d"
ROUTER_DROPIN="$ROUTER_DROPIN_DIR/zzzzz-dealix-local-ai-8k.conf"
STAMP="$(date +%Y%m%d-%H%M%S)"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "BLOCKED: run as root on the Dealix VPS"
  exit 2
fi

command -v ollama >/dev/null 2>&1 || { echo "BLOCKED: ollama not installed"; exit 3; }

mkdir -p "$DROPIN_DIR"
if [[ -f "$DROPIN" ]]; then
  cp -a "$DROPIN" "${DROPIN}.bak-${STAMP}"
fi

cat >"$DROPIN" <<'EOF'
[Service]
Environment="OLLAMA_HOST=127.0.0.1:11434"
Environment="OLLAMA_CONTEXT_LENGTH=8192"
Environment="OLLAMA_KEEP_ALIVE=15m"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_NUM_PARALLEL=1"
EOF
chmod 0644 "$DROPIN"

# Keep the canonical Dealix router aligned with the same bounded local model.
# A lexically-final drop-in prevents stale service defaults from resurrecting
# the retired 64K alias or overriding the 8K request context.
if systemctl cat dealix-llm-router.service >/dev/null 2>&1; then
  mkdir -p "$ROUTER_DROPIN_DIR"
  cat >"$ROUTER_DROPIN" <<EOF
[Service]
Environment=DEALIX_LOCAL_MODEL=$MODEL
Environment=DEALIX_LOCAL_NUM_CTX=8192
EOF
  chmod 0644 "$ROUTER_DROPIN"
fi

# A legacy 64K alias must never be a silent fallback on this 16 GB CPU node.
# Stop/remove only that local model alias; the canonical 4B model is preserved.
ollama stop "$LEGACY_MODEL" >/dev/null 2>&1 || true
if ollama list 2>/dev/null | awk 'NR>1 {print $1}' | sed 's/:latest$//' | grep -Fxq "$LEGACY_MODEL"; then
  ollama rm "$LEGACY_MODEL" >/dev/null
  echo "LEGACY_64K_MODEL_REMOVED=PASS"
else
  echo "LEGACY_64K_MODEL_REMOVED=NOT_PRESENT"
fi

systemctl daemon-reload
systemctl restart ollama

for _ in $(seq 1 20); do
  if curl -fsS --max-time 3 http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
    break
  fi
  sleep 1
done
curl -fsS --max-time 3 http://127.0.0.1:11434/api/tags >/dev/null

if systemctl cat dealix-llm-router.service >/dev/null 2>&1; then
  systemctl restart dealix-llm-router.service
  ROUTER_READY=0
  for _ in $(seq 1 20); do
    if curl -fsS --max-time 2 http://127.0.0.1:11999/healthz >/dev/null 2>&1; then
      ROUTER_READY=1
      break
    fi
    sleep 1
  done
  [[ "$ROUTER_READY" == "1" ]] || { echo "OLLAMA_8K_GUARD=FAIL router_health"; exit 11; }
fi

# Verify effective environment without printing unrelated environment/secrets.
EFFECTIVE="$(systemctl show ollama --property=Environment --value)"
grep -Fq 'OLLAMA_CONTEXT_LENGTH=8192' <<<"$EFFECTIVE" || { echo "OLLAMA_8K_GUARD=FAIL context"; exit 4; }
grep -Fq 'OLLAMA_HOST=127.0.0.1:11434' <<<"$EFFECTIVE" || { echo "OLLAMA_8K_GUARD=FAIL host"; exit 5; }
grep -Fq 'OLLAMA_MAX_LOADED_MODELS=1' <<<"$EFFECTIVE" || { echo "OLLAMA_8K_GUARD=FAIL loaded_models"; exit 6; }
grep -Fq 'OLLAMA_NUM_PARALLEL=1' <<<"$EFFECTIVE" || { echo "OLLAMA_8K_GUARD=FAIL parallel"; exit 7; }

if systemctl cat dealix-llm-router.service >/dev/null 2>&1; then
  ROUTER_EFFECTIVE="$(systemctl show dealix-llm-router --property=Environment --value)"
  grep -Fq "DEALIX_LOCAL_MODEL=$MODEL" <<<"$ROUTER_EFFECTIVE" || { echo "OLLAMA_8K_GUARD=FAIL router_model"; exit 9; }
  grep -Fq 'DEALIX_LOCAL_NUM_CTX=8192' <<<"$ROUTER_EFFECTIVE" || { echo "OLLAMA_8K_GUARD=FAIL router_context"; exit 10; }
fi

# Ensure the desired primary model exists. Do not pull large models automatically.
if ollama list 2>/dev/null | awk 'NR>1 {print $1}' | sed 's/:latest$//' | grep -Fxq "$MODEL"; then
  echo "PRIMARY_MODEL=PASS model=$MODEL"
else
  echo "PRIMARY_MODEL=DEGRADED model_not_installed=$MODEL"
fi

if ollama list 2>/dev/null | grep -Fq "$LEGACY_MODEL"; then
  echo "OLLAMA_8K_GUARD=FAIL legacy_model_still_present"
  exit 8
fi

echo "OLLAMA_8K_GUARD=PASS"
echo "CONTEXT=8192"
echo "HOST=127.0.0.1:11434"
