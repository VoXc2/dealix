#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
# Dealix — install Ollama + pull tier-appropriate local models
# تثبيت Ollama وسحب النماذج المحلية المناسبة للخادم
# ───────────────────────────────────────────────────────────────────
# Usage:
#   sudo bash scripts/local-ai/install_local_ai.sh
#   FORCE_TIER=balanced bash scripts/local-ai/install_local_ai.sh
#   SKIP_PULL=1 bash scripts/local-ai/install_local_ai.sh   # just install daemon
# ═══════════════════════════════════════════════════════════════════
set -euo pipefail

FORCE_TIER="${FORCE_TIER:-}"
SKIP_PULL="${SKIP_PULL:-0}"
MIN_DISK_GB="${MIN_DISK_GB:-6}"
BASE_URL="${LOCAL_LLM_BASE_URL:-http://localhost:11434}"

log()  { printf "\033[1;36m[local-ai]\033[0m %s\n" "$*"; }
warn() { printf "\033[1;33m[local-ai]\033[0m %s\n" "$*" >&2; }
err()  { printf "\033[1;31m[local-ai]\033[0m %s\n" "$*" >&2; }

# ── Detect RAM/disk/GPU ───────────────────────────────────────────
total_ram_gb() {
  awk '/MemTotal/ {printf "%.1f", $2/1024/1024}' /proc/meminfo 2>/dev/null || echo "4.0"
}

free_disk_gb() {
  df -BG --output=avail / 2>/dev/null | tail -n1 | tr -d 'G ' || echo "10"
}

has_gpu() {
  command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi -L >/dev/null 2>&1
}

pick_tier() {
  if [[ -n "$FORCE_TIER" ]]; then echo "$FORCE_TIER"; return; fi
  local ram disk
  ram="$(total_ram_gb)"
  disk="$(free_disk_gb)"
  if (( $(echo "$disk < $MIN_DISK_GB" | bc -l) )); then echo "nano"; return; fi
  if has_gpu; then echo "performance"; return; fi
  if (( $(echo "$ram >= 16" | bc -l) )); then echo "performance"; return; fi
  if (( $(echo "$ram >= 8"  | bc -l) )); then echo "balanced"; return; fi
  if (( $(echo "$ram >= 4"  | bc -l) )); then echo "small"; return; fi
  echo "nano"
}

# Conservative install plan per tier (tag list, smallest first)
models_for_tier() {
  case "$1" in
    nano)        echo "qwen2.5:0.5b" ;;
    small)      echo "qwen2.5:0.5b qwen2.5:3b-instruct" ;;
    balanced)    echo "qwen2.5:0.5b qwen2.5:7b-instruct qwen2.5-coder:7b" ;;
    performance) echo "qwen2.5:0.5b qwen2.5:7b-instruct qwen2.5-coder:7b qwen2.5:14b-instruct" ;;
    *)           echo "qwen2.5:0.5b" ;;
  esac
}

# ── Install Ollama ────────────────────────────────────────────────
install_ollama() {
  if command -v ollama >/dev/null 2>&1; then
    log "Ollama already installed: $(ollama --version 2>/dev/null || true)"
    return
  fi
  log "Installing Ollama via official script…"
  if ! command -v curl >/dev/null 2>&1; then
    err "curl is required. apt-get install -y curl"
    exit 1
  fi
  curl -fsSL https://ollama.com/install.sh | sh
}

start_ollama() {
  if pgrep -x ollama >/dev/null 2>&1; then
    log "Ollama daemon already running."
    return
  fi
  if command -v systemctl >/dev/null 2>&1 && systemctl list-unit-files | grep -q '^ollama\.service'; then
    log "Starting ollama.service via systemd."
    sudo systemctl enable --now ollama || true
  else
    log "Launching ollama serve in background."
    nohup ollama serve >/tmp/ollama.log 2>&1 &
    sleep 2
  fi
}

wait_for_daemon() {
  log "Waiting for Ollama at $BASE_URL …"
  for i in $(seq 1 30); do
    if curl -fsS "$BASE_URL/api/tags" >/dev/null 2>&1; then
      log "Ollama is up."
      return 0
    fi
    sleep 1
  done
  err "Ollama daemon not responding. Check /tmp/ollama.log."
  return 1
}

pull_models() {
  local tier="$1"
  local tags; tags="$(models_for_tier "$tier")"
  log "Pulling models for tier=$tier: $tags"
  for t in $tags; do
    log "→ pulling $t (this may take a while)…"
    if ! ollama pull "$t"; then
      warn "Failed to pull $t — continuing with remaining models."
      continue
    fi
  done
}

health_check() {
  log "Running health check…"
  local tags
  tags=$(curl -fsS "$BASE_URL/api/tags" 2>/dev/null | python3 -c 'import sys,json
try:
  data=json.load(sys.stdin)
  print(" ".join(m.get("name","") for m in data.get("models",[])))
except Exception:
  pass' || true)
  log "Installed model tags: ${tags:-<none>}"
}

print_env_hints() {
  local tier="$1"
  local default_model router_model coder_model reasoner_model
  case "$tier" in
    nano)        default_model="qwen2.5:0.5b";       router_model="qwen2.5:0.5b" ;;
    small)      default_model="qwen2.5:3b-instruct";router_model="qwen2.5:0.5b" ;;
    balanced)    default_model="qwen2.5:7b-instruct";router_model="qwen2.5:0.5b"; coder_model="qwen2.5-coder:7b" ;;
    performance) default_model="qwen2.5:7b-instruct";router_model="qwen2.5:0.5b"; coder_model="qwen2.5-coder:7b"; reasoner_model="qwen2.5:14b-instruct" ;;
  esac

  cat <<EOF

─── Copy into backend .env ───────────────────────────────────────
LOCAL_LLM_ENABLED=1
LOCAL_LLM_BASE_URL=$BASE_URL
LOCAL_LLM_DEFAULT_MODEL=$default_model
LOCAL_LLM_ROUTER_MODEL=$router_model
${coder_model:+LOCAL_LLM_CODER_MODEL=$coder_model}
${reasoner_model:+LOCAL_LLM_REASONER_MODEL=$reasoner_model}
# Optionally set LLM_PRIMARY_PROVIDER=local to prefer local over cloud.
──────────────────────────────────────────────────────────────────

EOF
}

# ── Main ─────────────────────────────────────────────────────────
main() {
  local ram disk gpu tier
  ram="$(total_ram_gb)"
  disk="$(free_disk_gb)"
  gpu="$(has_gpu && echo yes || echo no)"
  tier="$(pick_tier)"

  log "Detected: RAM=${ram}GB, free-disk=${disk}GB, GPU=${gpu}, tier=${tier}"

  install_ollama
  start_ollama
  wait_for_daemon

  if [[ "$SKIP_PULL" != "1" ]]; then
    pull_models "$tier"
  else
    log "SKIP_PULL=1 — skipping model downloads."
  fi

  health_check
  print_env_hints "$tier"
  log "Done. اكتمل التثبيت ✅"
}

main "$@"
