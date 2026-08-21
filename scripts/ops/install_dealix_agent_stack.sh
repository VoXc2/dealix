#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

REPO="Dealix-sa/dealix"
BRANCH="ops/dealix-vps-self-hosted-control-20260820"
RUN_USER="dealix"
ROOT="/opt/dealix/workspace/dealix"
CONTROL_ROOT="/opt/dealix/control"
PROMPT_DIR="${CONTROL_ROOT}/prompts"
PROOF_DIR="/opt/dealix/logs"
STAMP="$(date +%Y%m%d-%H%M%S)"
PROOF="${PROOF_DIR}/agent-stack-${STAMP}.log"
MODEL="${DEALIX_OPENCLAW_MODEL:-qwen3:4b-instruct-2507-q4_K_M}"
OPENCLAW_PREFIX="/home/${RUN_USER}/.openclaw"
OPENCLAW_BIN="${OPENCLAW_PREFIX}/bin/openclaw"
SECRET_DIR="/home/${RUN_USER}/.config/dealix-secrets"
TG_TOKEN_FILE="${SECRET_DIR}/openclaw-telegram.token"

mkdir -p "$PROOF_DIR"
touch "$PROOF"
chmod 0600 "$PROOF"
exec > >(tee -a "$PROOF") 2>&1

log() { printf '[%s] %s\n' "$(date -Is)" "$*"; }

if [[ "$(id -u)" -ne 0 ]]; then
  echo "BLOCKED: run as root"
  exit 2
fi

if ! id "$RUN_USER" >/dev/null 2>&1; then
  echo "BLOCKED: user '$RUN_USER' is missing"
  exit 3
fi

mkdir -p "$CONTROL_ROOT" "$PROMPT_DIR" "$SECRET_DIR"
chown -R "$RUN_USER:$RUN_USER" "$CONTROL_ROOT" "$SECRET_DIR"
chmod 0700 "$SECRET_DIR"

if ! sudo -iu "$RUN_USER" gh auth status >/dev/null 2>&1; then
  echo "BLOCKED: GitHub CLI is not authenticated for $RUN_USER"
  exit 4
fi

PRIVATE="$(sudo -iu "$RUN_USER" gh api "repos/${REPO}" --jq '.private' 2>/dev/null || true)"
LOGIN="$(sudo -iu "$RUN_USER" gh api user --jq '.login' 2>/dev/null || true)"
if [[ "$PRIVATE" != "true" || "$LOGIN" != "VoXc2" ]]; then
  echo "BLOCKED: expected private repo and founder GitHub identity"
  exit 5
fi

log "repository_private=true"
log "github_login=${LOGIN}"

if [[ ! -d "$ROOT/.git" ]]; then
  echo "BLOCKED: canonical repository missing at $ROOT"
  exit 6
fi

# Keep a local copy of the reusable master prompt without touching main.
sudo -iu "$RUN_USER" gh api \
  -H 'Accept: application/vnd.github.raw+json' \
  "repos/${REPO}/contents/docs/ops/DEALIX_TOTAL_AUTOMATION_MASTER.md?ref=${BRANCH}" \
  > "${PROMPT_DIR}/DEALIX_TOTAL_AUTOMATION_MASTER.md"
chown "$RUN_USER:$RUN_USER" "${PROMPT_DIR}/DEALIX_TOTAL_AUTOMATION_MASTER.md"
chmod 0640 "${PROMPT_DIR}/DEALIX_TOTAL_AUTOMATION_MASTER.md"

log "===== EXISTING STACK INVENTORY ====="
for svc in docker ollama tailscaled fail2ban; do
  printf '%-22s %s\n' "$svc" "$(systemctl is-active "$svc" 2>/dev/null || true)"
done
printf '%-22s %s\n' "issue-bridge" "$(systemctl is-active dealix-vps-issue-bridge.timer 2>/dev/null || true)"
printf '%-22s %s\n' "company-heartbeat" "$(systemctl is-active dealix-company-heartbeat.timer 2>/dev/null || true)"
docker ps --filter name=dealix-n8n --format 'n8n={{.Status}} {{.Ports}}' 2>/dev/null || true

log "===== RAILWAY LOCAL CONTEXT ====="
if sudo -iu "$RUN_USER" bash -lc 'export PATH="$HOME/.railway/bin:$PATH"; railway whoami' >/dev/null 2>&1; then
  if ! sudo -iu "$RUN_USER" bash -lc 'export PATH="$HOME/.railway/bin:$PATH"; cd /opt/dealix/workspace/dealix; railway status' >/dev/null 2>&1; then
    log "Railway is authenticated but this checkout is not linked; attempting local-only project link to Dealix."
    sudo -iu "$RUN_USER" bash -lc 'export PATH="$HOME/.railway/bin:$PATH"; cd /opt/dealix/workspace/dealix; railway link --project Dealix' || true
  fi
  sudo -iu "$RUN_USER" bash -lc 'export PATH="$HOME/.railway/bin:$PATH"; cd /opt/dealix/workspace/dealix; railway status' || true
else
  log "Railway authentication missing; no production mutation attempted."
fi

log "===== OPENCLAW INSTALL ====="
if [[ ! -x "$OPENCLAW_BIN" ]]; then
  sudo -iu "$RUN_USER" bash -lc \
    'curl -fsSL --proto "=https" --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --prefix "$HOME/.openclaw" --version latest'
fi

if [[ ! -x "$OPENCLAW_BIN" ]]; then
  echo "BLOCKED: OpenClaw installation did not produce $OPENCLAW_BIN"
  exit 7
fi

sudo -iu "$RUN_USER" "$OPENCLAW_BIN" --version

# Local gateway only. The token is generated locally and never printed.
GATEWAY_TOKEN="$(openssl rand -hex 32)"
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set gateway.mode local >/dev/null
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set gateway.bind loopback >/dev/null
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set gateway.port 18789 >/dev/null
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set gateway.auth.mode token >/dev/null
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set gateway.auth.token "$GATEWAY_TOKEN" >/dev/null
unset GATEWAY_TOKEN

# Use Ollama native API, not /v1. Explicit model keeps context bounded on this CPU VPS.
OLLAMA_PROVIDER_JSON="$(python3 - "$MODEL" <<'PY'
import json, sys
model=sys.argv[1]
print(json.dumps({
  "baseUrl":"http://127.0.0.1:11434",
  "apiKey":"ollama-local",
  "api":"ollama",
  "timeoutSeconds":300,
  "contextWindow":8192,
  "maxTokens":2048,
  "models":[{
    "id":model,
    "name":model,
    "contextWindow":8192,
    "maxTokens":2048,
    "params":{"num_ctx":8192,"thinking":False,"keep_alive":"10m"}
  }]
}))
PY
)"
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set models.providers.ollama "$OLLAMA_PROVIDER_JSON" --strict-json --merge >/dev/null
unset OLLAMA_PROVIDER_JSON
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" models set "ollama/${MODEL}" || true

# Telegram-facing local model gets messaging-only authority; no shell or file mutation.
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set tools.profile messaging >/dev/null
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set tools.deny '["exec","process","write","edit","apply_patch","group:runtime","group:fs"]' --strict-json >/dev/null
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set tools.elevated.enabled false >/dev/null || true
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set channels.telegram.enabled true >/dev/null
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set channels.telegram.dmPolicy pairing >/dev/null
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set channels.telegram.groups '{"*":{"requireMention":true}}' --strict-json >/dev/null

log "===== TELEGRAM TOKEN ====="
if [[ ! -s "$TG_TOKEN_FILE" ]]; then
  if [[ ! -r /dev/tty ]]; then
    echo "BLOCKED: Telegram token is not configured and no interactive TTY is available."
    exit 8
  fi
  printf 'Paste BotFather Telegram bot token (input hidden; never paste it into chat): ' >/dev/tty
  IFS= read -r -s TG_TOKEN </dev/tty
  printf '\n' >/dev/tty
  if [[ -z "$TG_TOKEN" ]]; then
    echo "BLOCKED: empty Telegram token"
    exit 9
  fi
  printf '%s\n' "$TG_TOKEN" > "$TG_TOKEN_FILE"
  chown "$RUN_USER:$RUN_USER" "$TG_TOKEN_FILE"
  chmod 0600 "$TG_TOKEN_FILE"
else
  TG_TOKEN="$(cat "$TG_TOKEN_FILE")"
fi

# Validate token without printing it.
TG_META="$(curl -fsS --max-time 20 "https://api.telegram.org/bot${TG_TOKEN}/getMe" 2>/dev/null || true)"
unset TG_TOKEN
if ! python3 - "$TG_META" <<'PY'
import json,sys
try:
    d=json.loads(sys.argv[1]); ok=bool(d.get('ok')) and bool(d.get('result',{}).get('is_bot'))
except Exception:
    ok=False
raise SystemExit(0 if ok else 1)
PY
then
  echo "BLOCKED: Telegram getMe validation failed. Regenerate/check the BotFather token locally."
  exit 10
fi
unset TG_META
log "telegram_token_validation=PASS"
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set channels.telegram.tokenFile "$TG_TOKEN_FILE" >/dev/null

# Keep the user service alive after SSH logout.
loginctl enable-linger "$RUN_USER" || true
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" gateway install --force || true
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" gateway restart || sudo -iu "$RUN_USER" "$OPENCLAW_BIN" gateway start || true
sleep 3

log "===== OPENCLAW PROOF ====="
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" models status || true
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" gateway status --require-rpc || true
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" channels status --probe || true
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" security audit --deep || true
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" pairing list telegram || true

log "===== HERMES INTERNAL AGENT ====="
if sudo -iu "$RUN_USER" bash -lc 'export PATH="$HOME/.local/bin:$HOME/.hermes/bin:$PATH"; command -v hermes' >/dev/null 2>&1; then
  sudo -iu "$RUN_USER" bash -lc 'export PATH="$HOME/.local/bin:$HOME/.hermes/bin:$PATH"; hermes --version' || true
  sudo -iu "$RUN_USER" bash -lc 'export PATH="$HOME/.local/bin:$HOME/.hermes/bin:$PATH"; hermes config set approvals.mode manual' || true
  sudo -iu "$RUN_USER" bash -lc 'export PATH="$HOME/.local/bin:$HOME/.hermes/bin:$PATH"; hermes config set approvals.cron_mode deny' || true
  sudo -iu "$RUN_USER" bash -lc 'export PATH="$HOME/.local/bin:$HOME/.hermes/bin:$PATH"; hermes config set checkpoints.enabled true' || true
  sudo -iu "$RUN_USER" bash -lc 'export PATH="$HOME/.local/bin:$HOME/.hermes/bin:$PATH"; hermes config check' || true
  sudo -iu "$RUN_USER" bash -lc 'export PATH="$HOME/.local/bin:$HOME/.hermes/bin:$PATH"; hermes cron status' || true
  sudo -iu "$RUN_USER" bash -lc 'export PATH="$HOME/.local/bin:$HOME/.hermes/bin:$PATH"; hermes cron list' || true
else
  log "Hermes is not installed for dealix; OpenClaw + Company Autopilot remain sufficient."
fi

log "===== N8N ====="
docker ps --filter name=dealix-n8n --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' 2>/dev/null || true

log "===== COMPANY AUTOPILOT TIMERS ====="
systemctl list-timers 'dealix-company-*' --all --no-pager || true

log "===== FINAL ====="
log "openclaw_gateway_owner=telegram"
log "hermes_role=internal-agent-only"
log "ollama_endpoint=http://127.0.0.1:11434"
log "n8n_public_exposure=false"
log "external_send=false"
log "merge_to_main=false"
log "production_mutation=false"
log "payment_execution=false"
log "master_prompt=${PROMPT_DIR}/DEALIX_TOTAL_AUTOMATION_MASTER.md"
log "proof=${PROOF}"
log "NEXT: send a DM to the Telegram bot, then run: sudo -iu dealix ${OPENCLAW_BIN} pairing list telegram"
log "Approve only the founder pairing code with: sudo -iu dealix ${OPENCLAW_BIN} pairing approve telegram <CODE>"
