#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

REPO="Dealix-sa/dealix"
FOUNDER="VoXc2"
RUN_USER="dealix"
ROOT="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
SOURCE_REF="${DEALIX_SOURCE_REF:-main}"
LEGACY_BRANCH="ops/dealix-vps-self-hosted-control-20260820"
MODEL="${DEALIX_LOCAL_MODEL:-qwen3:4b-instruct-2507-q4_K_M}"
STAMP="$(date +%Y%m%d-%H%M%S)"
TMP="$(mktemp -d /tmp/dealix-main-activate.XXXXXX)"
BACKUP="/opt/dealix/runtime-backups/main-activation-${STAMP}"
LOG="/opt/dealix/logs/main-activation-${STAMP}.log"

mkdir -p /opt/dealix/logs "$BACKUP"
chmod 0700 "$BACKUP"
exec > >(tee -a "$LOG") 2>&1
trap 'rm -rf "$TMP"' EXIT

log() { printf '[%s] %s\n' "$(date -Is)" "$*"; }

if [[ "$(id -u)" -ne 0 ]]; then
  echo "BLOCKED: run as root on the Dealix VPS"
  exit 2
fi
if ! id "$RUN_USER" >/dev/null 2>&1; then
  echo "BLOCKED: missing OS user $RUN_USER"
  exit 3
fi
if [[ ! -d "$ROOT/.git" ]]; then
  echo "BLOCKED: canonical repository missing at $ROOT"
  exit 4
fi
if ! sudo -iu "$RUN_USER" gh auth status >/dev/null 2>&1; then
  echo "BLOCKED: GitHub CLI is not authenticated for $RUN_USER"
  exit 5
fi
LOGIN="$(sudo -iu "$RUN_USER" gh api user --jq '.login' 2>/dev/null || true)"
PRIVATE="$(sudo -iu "$RUN_USER" gh api "repos/${REPO}" --jq '.private' 2>/dev/null || true)"
if [[ "$LOGIN" != "$FOUNDER" || "$PRIVATE" != "true" ]]; then
  echo "BLOCKED: expected founder GitHub identity and private repository"
  exit 6
fi

SOURCE_SHA="$(sudo -iu "$RUN_USER" gh api "repos/${REPO}/commits/${SOURCE_REF}" --jq '.sha')"
[[ -n "$SOURCE_SHA" ]] || { echo "BLOCKED: could not resolve source ref $SOURCE_REF"; exit 7; }
log "source_ref=$SOURCE_REF source_sha=$SOURCE_SHA"

# Keep the parent SSH session safe and restore configured swap if a previous
# diagnostic session disabled it. No swap file is created or reformatted here.
swapon -a 2>/dev/null || true

log "===== QUIESCE DEALIX REPO WRITERS ====="
for unit in \
  dealix-vps-issue-bridge.timer \
  dealix-company-heartbeat.timer \
  dealix-company-production.timer \
  dealix-company-repo-watch.timer \
  dealix-company-preflight.timer \
  dealix-company-morning-fallback.timer \
  dealix-company-midday.timer \
  dealix-company-evening.timer \
  dealix-company-local-ai.timer \
  dealix-company-nightly.timer \
  dealix-company-weekly.timer \
  dealix-agent-council.timer
 do
  systemctl stop "$unit" 2>/dev/null || true
done
systemctl stop hermes-dealix.service 2>/dev/null || true

log "===== PRESERVE LOCAL WORKTREE ====="
sudo -iu "$RUN_USER" git -C "$ROOT" status -sb | tee "$BACKUP/git-status-before.txt" || true
sudo -iu "$RUN_USER" git -C "$ROOT" diff --binary >"$BACKUP/worktree.patch" || true
sudo -iu "$RUN_USER" git -C "$ROOT" diff --cached --binary >"$BACKUP/index.patch" || true
DIRTY="$(sudo -iu "$RUN_USER" git -C "$ROOT" status --porcelain=v1)"
STASH_REF="none"
if [[ -n "$DIRTY" ]]; then
  sudo -iu "$RUN_USER" git -C "$ROOT" stash push -u -m "pre-main-activation-${STAMP}"
  STASH_REF="$(sudo -iu "$RUN_USER" git -C "$ROOT" stash list -1 --format='%gd' || true)"
  log "local_changes_preserved=$STASH_REF backup=$BACKUP"
else
  log "local_worktree=clean"
fi

log "===== FAST-FORWARD CANONICAL REPOSITORY ====="
sudo -iu "$RUN_USER" git -C "$ROOT" fetch origin main --prune
ORIGIN_MAIN="$(sudo -iu "$RUN_USER" git -C "$ROOT" rev-parse origin/main)"
if [[ "$SOURCE_REF" == "main" && "$ORIGIN_MAIN" != "$SOURCE_SHA" ]]; then
  echo "BLOCKED: GitHub main and origin/main disagree"
  exit 8
fi
sudo -iu "$RUN_USER" git -C "$ROOT" checkout main
sudo -iu "$RUN_USER" git -C "$ROOT" merge --ff-only "$SOURCE_SHA"
LOCAL_SHA="$(sudo -iu "$RUN_USER" git -C "$ROOT" rev-parse HEAD)"
[[ "$LOCAL_SHA" == "$SOURCE_SHA" ]] || { echo "BLOCKED: local HEAD mismatch"; exit 9; }
log "repo_head=$LOCAL_SHA"

patch_source_ref() {
  local file="$1"
  python3 - "$file" "$SOURCE_SHA" "$LEGACY_BRANCH" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
sha = sys.argv[2]
legacy = sys.argv[3]
s = p.read_text(encoding="utf-8")
s = s.replace(f'BRANCH="{legacy}"', f'BRANCH="{sha}"')
p.write_text(s, encoding="utf-8")
PY
}

run_patched() {
  local rel="$1"
  local out="$TMP/$(basename "$rel")"
  cp "$ROOT/$rel" "$out"
  patch_source_ref "$out"
  bash -n "$out"
  chmod 0700 "$out"
  bash "$out"
}

log "===== BOUNDED LOCAL AI ====="
mkdir -p /etc/systemd/system/ollama.service.d
cat >/etc/systemd/system/ollama.service.d/99-dealix-main-safe.conf <<'EOF'
[Service]
Environment="OLLAMA_HOST=127.0.0.1:11434"
Environment="OLLAMA_KEEP_ALIVE=2m"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_CONTEXT_LENGTH=8192"
CPUQuota=300%
MemoryMax=8G
EOF
chmod 0644 /etc/systemd/system/ollama.service.d/99-dealix-main-safe.conf
systemctl daemon-reload
ollama stop dealix-qwen3-4b-64k >/dev/null 2>&1 || true
ollama stop "$MODEL" >/dev/null 2>&1 || true
systemctl restart ollama
sleep 4
curl -fsS --max-time 10 http://127.0.0.1:11434/api/tags >/dev/null
REPLY="$(curl -fsS --max-time 240 http://127.0.0.1:11434/api/chat -H 'Content-Type: application/json' -d @- <<JSON | jq -r '.message.content // empty'
{"model":"$MODEL","stream":false,"keep_alive":"20s","options":{"num_ctx":8192,"temperature":0},"messages":[{"role":"user","content":"Reply with exactly: DEALIX_OLLAMA_8K_OK"}]}
JSON
)" || true
[[ "$REPLY" == "DEALIX_OLLAMA_8K_OK" ]] || { echo "BLOCKED: Ollama 8K acceptance failed"; exit 10; }
echo "DEALIX_OLLAMA_8K_OK"

log "===== COMPANY AUTOPILOT ====="
AUTOPILOT_INSTALLER="$TMP/install_dealix_company_autopilot.sh"
cp "$ROOT/scripts/ops/install_dealix_company_autopilot.sh" "$AUTOPILOT_INSTALLER"
patch_source_ref "$AUTOPILOT_INSTALLER"
# Ubuntu 24.04/systemd on this host requires explicit weekday lists.
sed -i 's/Sun\.\.Thu/Sun,Mon,Tue,Wed,Thu/g' "$AUTOPILOT_INSTALLER"
# Patch the nested bridge installer after it is fetched from the immutable SHA;
# that installer historically contained the now-deleted feature-branch name.
python3 - "$AUTOPILOT_INSTALLER" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text(encoding="utf-8")
needle='chmod 0700 "$TMP_BRIDGE_INSTALLER"'
if needle in s and 'main-safe nested bridge ref' not in s:
    injection=(
        '# main-safe nested bridge ref\n'
        'sed -i "s|BRANCH=\\\"ops/dealix-vps-self-hosted-control-20260820\\\"|BRANCH=\\\"${BRANCH}\\\"|g" "$TMP_BRIDGE_INSTALLER"\n'
    )
    s=s.replace(needle, injection+needle, 1)
p.write_text(s, encoding="utf-8")
PY
bash -n "$AUTOPILOT_INSTALLER"
set +e
bash "$AUTOPILOT_INSTALLER"
AUTOPILOT_RC=$?
set -e
log "autopilot_install_rc=$AUTOPILOT_RC"

log "===== PRIVATE ISSUE BRIDGE ====="
set +e
run_patched scripts/ops/install_dealix_vps_issue_bridge.sh
BRIDGE_RC=$?
set -e
log "issue_bridge_rc=$BRIDGE_RC"

log "===== OPENCLAW FOUNDER GATEWAY ====="
OC="/home/dealix/.openclaw/bin/openclaw"
set +e
if [[ -x "$OC" ]]; then
  bash "$ROOT/scripts/ops/repair_dealix_openclaw_gateway.sh"
  OPENCLAW_RC=$?
else
  run_patched scripts/ops/install_dealix_agent_stack.sh
  OPENCLAW_RC=$?
fi
set -e
if [[ -x "$OC" ]]; then
  sudo -iu "$RUN_USER" "$OC" config set tools.profile messaging >/dev/null 2>&1 || true
  sudo -iu "$RUN_USER" "$OC" config set tools.deny '["exec","process","write","edit","apply_patch","group:runtime","group:fs"]' --strict-json >/dev/null 2>&1 || true
  sudo -iu "$RUN_USER" "$OC" config set tools.elevated.enabled false >/dev/null 2>&1 || true
  sudo -iu "$RUN_USER" "$OC" config set channels.telegram.dmPolicy pairing >/dev/null 2>&1 || true
  sudo -iu "$RUN_USER" "$OC" gateway restart >/dev/null 2>&1 || true
  sudo -iu "$RUN_USER" "$OC" gateway status --require-rpc || true
  sudo -iu "$RUN_USER" "$OC" channels status --probe || true
  sudo -iu "$RUN_USER" "$OC" security audit --deep || true
  sudo -iu "$RUN_USER" "$OC" pairing list telegram || true
fi
log "openclaw_rc=$OPENCLAW_RC"

log "===== HERMES ONE-SHOT ACCEPTANCE ====="
HERMES="/home/dealix/.local/bin/hermes"
HERMES_OK=0
if [[ -x "$HERMES" ]]; then
  sudo -iu "$RUN_USER" "$HERMES" config set terminal.cwd "$ROOT" >/dev/null 2>&1 || true
  sudo -iu "$RUN_USER" "$HERMES" config set approvals.mode manual >/dev/null 2>&1 || true
  sudo -iu "$RUN_USER" "$HERMES" config set approvals.cron_mode deny >/dev/null 2>&1 || true
  sudo -iu "$RUN_USER" "$HERMES" config set checkpoints.enabled true >/dev/null 2>&1 || true
  OUT="$(timeout 300 sudo -iu "$RUN_USER" bash -lc 'export PATH="$HOME/.local/bin:$HOME/.hermes/bin:$PATH"; cd /opt/dealix/workspace/dealix; hermes --ignore-rules --toolsets terminal -z "Do not use tools. Reply with exactly: DEALIX_HERMES_8K_OK"' 2>&1 || true)"
  if printf '%s\n' "$OUT" | grep -Fxq DEALIX_HERMES_8K_OK; then
    HERMES_OK=1
    echo "DEALIX_HERMES_8K_OK"
  else
    echo "HERMES_8K=FAIL_CLOSED"
    printf '%s\n' "$OUT" | tail -30
  fi
fi

log "===== COMPANY AGENTS ====="
set +e
run_patched scripts/ops/install_dealix_company_agents.sh
AGENTS_RC=$?
set -e
systemctl disable --now dealix-agent-council.timer 2>/dev/null || true
if [[ "$HERMES_OK" -eq 1 ]]; then
  systemctl enable --now dealix-agent-council.timer 2>/dev/null || true
fi
log "company_agents_rc=$AGENTS_RC council_enabled=$(systemctl is-enabled dealix-agent-council.timer 2>/dev/null || true)"

log "===== N8N SECURITY ====="
N8N_PORTS="$(docker ps --filter name=dealix-n8n --format '{{.Ports}}' 2>/dev/null || true)"
echo "n8n_ports=$N8N_PORTS"
if [[ "$N8N_PORTS" == *"0.0.0.0"* || "$N8N_PORTS" == *":::"* ]]; then
  echo "N8N_PUBLIC_BIND=RISK"
fi
docker ps --format '{{.Names}}' | grep -Fxq dealix-n8n && timeout 120 docker exec dealix-n8n n8n audit || true

log "===== WHATSAPP BUSINESS PREPARATION ONLY ====="
set +e
run_patched scripts/ops/prepare_dealix_second_number_whatsapp.sh
WHATSAPP_RC=$?
set -e
log "whatsapp_prepare_rc=$WHATSAPP_RC live_send=false"

# Reassert L5 kill switches. This activator never sends, publishes, charges,
# merges, deletes data, or mutates Railway/DNS/production.
export DEALIX_EXTERNAL_OUTREACH_ENABLED=false
export EXTERNAL_OUTREACH_ENABLED=false
export AUTO_SEND_ENABLED=false
export AGENT_APPROVAL_MODE=required
export WHATSAPP_ALLOW_LIVE_SEND=false
export MOYASAR_LIVE_MODE=0
systemctl disable --now hermes-dealix.service 2>/dev/null || true

log "===== CANONICAL AUTOPILOT VERIFIER ====="
set +e
sudo -iu "$RUN_USER" bash -lc "cd '$ROOT' && python3 scripts/ops/verify_canonical_company_autopilot.py"
VERIFY_RC=$?
set -e

log "===== CANONICAL REVENUE CYCLE ====="
set +e
sudo -iu "$RUN_USER" bash -lc "cd '$ROOT' && DEALIX_REPO_ROOT='$ROOT' bash scripts/ops/dealix_canonical_revenue_cycle.sh status"
REVENUE_STATUS_RC=$?
sudo -iu "$RUN_USER" bash -lc "cd '$ROOT' && DEALIX_REPO_ROOT='$ROOT' bash scripts/ops/dealix_canonical_revenue_cycle.sh daily"
REVENUE_DAILY_RC=$?
set -e

log "===== FOUNDER MONEY COMMAND ====="
set +e
sudo -iu "$RUN_USER" bash -lc "cd '$ROOT' && DEALIX_REPO_ROOT='$ROOT' bash scripts/ops/dealix_founder_money_command.sh"
MONEY_RC=$?
set -e

log "===== FINAL SAFE PROOF ====="
CTL="/opt/dealix/control/bin/dealix_vps_control.sh"
if [[ -x "$CTL" ]]; then
  for command in status autopilot-status autopilot-heartbeat autopilot-repo-watch; do
    echo "--- $command ---"
    timeout 300 "$CTL" "$command" || true
  done
fi
systemctl list-timers 'dealix-*' --all --no-pager || true
free -h || true
swapon --show || true
ollama ps || true
docker ps --filter name=dealix-n8n --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' || true
sudo -iu "$RUN_USER" git -C "$ROOT" status -sb || true

cat <<EOF

DEALIX_MAIN_ACTIVATION=COMPLETE_GOVERNED
SOURCE_REF=$SOURCE_REF
SOURCE_SHA=$SOURCE_SHA
LOCAL_SHA=$LOCAL_SHA
STASH_REF=$STASH_REF
WORKTREE_BACKUP=$BACKUP
OLLAMA_8K=PASS
HERMES_8K=$([[ "$HERMES_OK" -eq 1 ]] && echo PASS || echo FAIL_CLOSED)
AUTOPILOT_INSTALL_RC=$AUTOPILOT_RC
ISSUE_BRIDGE_RC=$BRIDGE_RC
OPENCLAW_RC=$OPENCLAW_RC
COMPANY_AGENTS_RC=$AGENTS_RC
CANONICAL_VERIFY_RC=$VERIFY_RC
REVENUE_STATUS_RC=$REVENUE_STATUS_RC
REVENUE_DAILY_RC=$REVENUE_DAILY_RC
FOUNDER_MONEY_RC=$MONEY_RC
DESTRUCTIVE_LOCAL_MODEL_DELETE=false
EXTERNAL_SEND=false
PUBLISH=false
PAYMENT_EXECUTION=false
MERGE_TO_MAIN=false
PRODUCTION_MUTATION=false
SECRET_VALUES_PRINTED=false
PROOF_LOG=$LOG
EOF
