#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

# Bounded runtime guard for the existing Dealix VPS AI layer.
# It does not start Hermes, create a new scheduler, deploy production, or touch secrets.

MODEL="${DEALIX_LOCAL_MODEL:-qwen3:4b-instruct-2507-q4_K_M}"
LEGACY_MODEL="dealix-qwen3-4b-64k"
DROPIN_DIR="/etc/systemd/system/ollama.service.d"
DROPIN="$DROPIN_DIR/dealix-8k-guard.conf"
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
Environment="OLLAMA_KEEP_ALIVE=2m"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_NUM_PARALLEL=1"
EOF
chmod 0644 "$DROPIN"

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

# Verify effective environment without printing unrelated environment/secrets.
EFFECTIVE="$(systemctl show ollama --property=Environment --value)"
grep -Fq 'OLLAMA_CONTEXT_LENGTH=8192' <<<"$EFFECTIVE" || { echo "OLLAMA_8K_GUARD=FAIL context"; exit 4; }
grep -Fq 'OLLAMA_HOST=127.0.0.1:11434' <<<"$EFFECTIVE" || { echo "OLLAMA_8K_GUARD=FAIL host"; exit 5; }
grep -Fq 'OLLAMA_MAX_LOADED_MODELS=1' <<<"$EFFECTIVE" || { echo "OLLAMA_8K_GUARD=FAIL loaded_models"; exit 6; }
grep -Fq 'OLLAMA_NUM_PARALLEL=1' <<<"$EFFECTIVE" || { echo "OLLAMA_8K_GUARD=FAIL parallel"; exit 7; }

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
