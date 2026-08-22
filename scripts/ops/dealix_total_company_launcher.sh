#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

REPO="Dealix-sa/dealix"
PR="1120"
USER_NAME="dealix"
ROOT="/opt/dealix/workspace/dealix"
MODEL="${DEALIX_LOCAL_MODEL:-qwen3:4b-instruct-2507-q4_K_M}"
TMP="$(mktemp -d /tmp/dealix-launcher.XXXXXX)"
STAMP="$(date +%Y%m%d-%H%M%S)"
LOG="/opt/dealix/logs/total-company-launcher-${STAMP}.log"
LOCK="/run/lock/dealix-total-company-launcher.lock"
OC="/home/dealix/.openclaw/bin/openclaw"
HERMES="/home/dealix/.local/bin/hermes"
COUNCIL="/opt/dealix/control/bin/dealix_agent_council.sh"

mkdir -p /opt/dealix/logs
exec 9>"$LOCK"
flock -n 9 || { echo "SKIP: launcher already running"; exit 0; }
touch "$LOG" && chmod 0600 "$LOG"
exec > >(tee -a "$LOG") 2>&1
trap 'rm -rf "$TMP"' EXIT

log(){ printf '[%s] %s\n' "$(date -Is)" "$*"; }

[[ "$(id -u)" -eq 0 ]] || { echo "BLOCKED: run as root"; exit 2; }
id "$USER_NAME" >/dev/null 2>&1 || { echo "BLOCKED: missing dealix user"; exit 3; }
[[ -d "$ROOT/.git" ]] || { echo "BLOCKED: missing canonical repo"; exit 4; }
sudo -iu "$USER_NAME" gh auth status >/dev/null 2>&1 || { echo "BLOCKED: gh not authenticated"; exit 5; }
[[ "$(sudo -iu "$USER_NAME" gh api "repos/$REPO" --jq '.private')" == "true" ]] || { echo "BLOCKED: repo must be private"; exit 6; }
[[ "$(sudo -iu "$USER_NAME" gh api user --jq '.login')" == "VoXc2" ]] || { echo "BLOCKED: wrong GitHub identity"; exit 7; }
HEAD_SHA="$(sudo -iu "$USER_NAME" gh pr view "$PR" --repo "$REPO" --json headRefOid --jq '.headRefOid')"
log "pr_head=$HEAD_SHA"

fetch(){ sudo -iu "$USER_NAME" gh api -H 'Accept: application/vnd.github.raw+json' "repos/$REPO/contents/$1?ref=$HEAD_SHA" >"$2"; test -s "$2"; }
run(){ local p="$1" f="$TMP/$(basename "$p")"; fetch "$p" "$f"; bash -n "$f"; chmod 700 "$f"; bash "$f"; }

log "===== BASELINE ====="
free -h || true
df -h / || true
for s in docker ollama tailscaled fail2ban; do echo "$s=$(systemctl is-active "$s" 2>/dev/null || true)"; done

log "===== STOP LEGACY HEAVY AI ====="
systemctl stop hermes-dealix.service 2>/dev/null || true
systemctl disable hermes-dealix.service 2>/dev/null || true
for u in dealix-hermes-live.timer dealix-hermes-daily.timer dealix-hermes-weekly.timer dealix-agent-council.timer; do systemctl disable --now "$u" 2>/dev/null || true; done
pkill -TERM -u dealix -x hermes 2>/dev/null || true

log "===== OLLAMA 8K ====="
mkdir -p /etc/systemd/system/ollama.service.d
[[ ! -f /etc/systemd/system/ollama.service.d/dealix.conf ]] || cp -a /etc/systemd/system/ollama.service.d/dealix.conf "/etc/systemd/system/ollama.service.d/dealix.conf.bak-$STAMP"
cat >/etc/systemd/system/ollama.service.d/dealix.conf <<'EOF'
[Service]
Environment="OLLAMA_HOST=127.0.0.1:11434"
Environment="OLLAMA_KEEP_ALIVE=2m"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_CONTEXT_LENGTH=8192"
CPUQuota=300%
MemoryMax=8G
EOF
systemctl daemon-reload
ollama stop dealix-qwen3-4b-64k >/dev/null 2>&1 || true
ollama stop "$MODEL" >/dev/null 2>&1 || true
systemctl restart ollama
sleep 4
curl -fsS http://127.0.0.1:11434/api/tags >/dev/null
REPLY="$(curl -fsS --max-time 180 http://127.0.0.1:11434/api/chat -H 'Content-Type: application/json' -d @- <<JSON | jq -r '.message.content // empty'
{"model":"$MODEL","stream":false,"keep_alive":"20s","options":{"num_ctx":8192,"temperature":0},"messages":[{"role":"user","content":"Reply with exactly: DEALIX_OLLAMA_8K_OK"}]}
JSON
)" || true
[[ "$REPLY" == "DEALIX_OLLAMA_8K_OK" ]] && log "DEALIX_OLLAMA_8K_OK" || log "OLLAMA_ACCEPTANCE=FAIL"

log "===== CANONICAL AUTOPILOT + ISSUE BRIDGE ====="
run scripts/ops/install_dealix_company_autopilot_ubuntu24_compat.sh || run scripts/ops/install_dealix_company_autopilot.sh || true
run scripts/ops/install_dealix_vps_issue_bridge.sh || true

log "===== OPENCLAW / TELEGRAM ====="
if [[ -x "$OC" ]]; then
  run scripts/ops/repair_dealix_openclaw_gateway.sh || true
else
  log "OpenClaw missing. Installer may request Telegram BotFather token via hidden TTY input."
  run scripts/ops/install_dealix_agent_stack.sh || true
fi
if [[ -x "$OC" ]]; then
  sudo -iu dealix "$OC" config set tools.profile messaging >/dev/null 2>&1 || true
  sudo -iu dealix "$OC" config set tools.deny '["exec","process","write","edit","apply_patch","group:runtime","group:fs"]' --strict-json >/dev/null 2>&1 || true
  sudo -iu dealix "$OC" config set tools.elevated.enabled false >/dev/null 2>&1 || true
  sudo -iu dealix "$OC" config set channels.telegram.dmPolicy pairing >/dev/null 2>&1 || true
  sudo -iu dealix "$OC" gateway restart >/dev/null 2>&1 || true
  sudo -iu dealix "$OC" gateway status --require-rpc || true
  sudo -iu dealix "$OC" channels status --probe || true
  sudo -iu dealix "$OC" security audit --deep || true
  sudo -iu dealix "$OC" pairing list telegram || true
fi

log "===== HERMES ACCEPTANCE ====="
HERMES_OK=0
if [[ -x "$HERMES" && "$REPLY" == "DEALIX_OLLAMA_8K_OK" ]]; then
  sudo -iu dealix "$HERMES" config set terminal.cwd "$ROOT" >/dev/null 2>&1 || true
  sudo -iu dealix "$HERMES" config set approvals.mode manual >/dev/null 2>&1 || true
  sudo -iu dealix "$HERMES" config set approvals.cron_mode deny >/dev/null 2>&1 || true
  sudo -iu dealix "$HERMES" config set checkpoints.enabled true >/dev/null 2>&1 || true
  sudo -iu dealix "$HERMES" config set memory.write_approval true >/dev/null 2>&1 || true
  sudo -iu dealix "$HERMES" config set skills.write_approval true >/dev/null 2>&1 || true
  # Hermes 0.20.4 has a known oneshot bug where -z silently ignores
  # --ignore-rules. The documented chat one-shot path honors the flag while
  # retaining the configured local provider/model. Keep the probe bounded to
  # one harmless clarify tool schema and one turn.
  OUT="$(timeout 300 sudo -iu dealix bash -lc 'export PATH="$HOME/.local/bin:$HOME/.hermes/bin:$PATH"; cd /opt/dealix/workspace/dealix; hermes chat -Q --ignore-rules --toolsets clarify --max-turns 1 -q "Do not use tools. Reply with exactly: DEALIX_HERMES_8K_OK"' 2>&1 || true)"
  printf '%s\n' "$OUT" | grep -Fxq DEALIX_HERMES_8K_OK && HERMES_OK=1 || { log "HERMES_8K=FAIL_CLOSED"; printf '%s\n' "$OUT" | tail -30; }
fi

log "===== COMPANY AGENTS ====="
run scripts/ops/install_dealix_company_agents.sh || true
systemctl disable --now dealix-agent-council.timer 2>/dev/null || true
if [[ -f "$COUNCIL" ]]; then
  cp -a "$COUNCIL" "$COUNCIL.bak-$STAMP"
  python3 - "$COUNCIL" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
marker='DEALIX PROOF INTEGRITY — NON-NEGOTIABLE'
if marker not in s:
    policy="""
PROOF_INTEGRITY_POLICY=$(cat <<'POLICY_EOF'
DEALIX PROOF INTEGRITY — NON-NEGOTIABLE
Never manufacture customer, acknowledgement, meeting, delivery, invoice, payment, proof-pack, agreement, partnership, revenue, or production evidence.
Synthetic/demo/test/placeholder information never satisfies a real commercial proof gate.
Missing evidence must be a Proof Gap. A recommendation is not an executed action.
API, frontend route, CI, deployment and business-proof health are separate dimensions.
Never instruct writing a fake real event into evidence_events_tracker.csv or another Proof Ledger.
POLICY_EOF
)
"""
    s=s.replace('run_role() {', policy+'\nrun_role() {', 1)
needle='Do not invent customers, revenue, payments, proof, partnerships, or production state.\n'
if '${PROOF_INTEGRITY_POLICY}' not in s:
    s=s.replace(needle, needle+'\n${PROOF_INTEGRITY_POLICY}\n', 1)
p.write_text(s)
PY
  bash -n "$COUNCIL"
  chown dealix:dealix "$COUNCIL"; chmod 0750 "$COUNCIL"
fi
if [[ "$HERMES_OK" -eq 1 ]]; then systemctl enable --now dealix-agent-council.timer || true; log "AGENT_COUNCIL=ENABLED"; else log "AGENT_COUNCIL=DISABLED_FAIL_CLOSED"; fi

log "===== N8N SECURITY AUDIT ====="
PORTS="$(docker ps --filter name=dealix-n8n --format '{{.Ports}}' 2>/dev/null || true)"
echo "n8n_ports=$PORTS"
[[ "$PORTS" == *"0.0.0.0"* || "$PORTS" == *":::"* ]] && log "N8N_PUBLIC_BIND=RISK" || true
docker ps --format '{{.Names}}' | grep -Fxq dealix-n8n && timeout 120 docker exec dealix-n8n n8n audit || true

log "===== WHATSAPP BUSINESS PREPARATION ONLY ====="
run scripts/ops/prepare_dealix_second_number_whatsapp.sh || true

log "===== EXTERNAL EFFECT KILL SWITCHES ====="
export DEALIX_EXTERNAL_OUTREACH_ENABLED=false EXTERNAL_OUTREACH_ENABLED=false AUTO_SEND_ENABLED=false AGENT_APPROVAL_MODE=required WHATSAPP_ALLOW_LIVE_SEND=false MOYASAR_LIVE_MODE=0
systemctl disable --now hermes-dealix.service 2>/dev/null || true

log "===== SAFE PROOF ====="
CTL=/opt/dealix/control/bin/dealix_vps_control.sh
if [[ -x "$CTL" ]]; then
  for c in status autopilot-heartbeat autopilot-production autopilot-repo-watch autopilot-status; do echo "--- $c ---"; timeout 300 "$CTL" "$c" || true; done
fi
systemctl list-timers 'dealix-*' --all --no-pager || true
free -h || true
ollama ps || true

cat <<EOF
DEALIX_TOTAL_COMPANY_LAUNCHER=COMPLETE_GOVERNED
PR_HEAD=$HEAD_SHA
OLLAMA_8K=$([[ "$REPLY" == DEALIX_OLLAMA_8K_OK ]] && echo PASS || echo FAIL)
HERMES_8K=$([[ "$HERMES_OK" -eq 1 ]] && echo PASS || echo FAIL_CLOSED)
EXTERNAL_SEND=false
MERGE_TO_MAIN=false
PRODUCTION_MUTATION=false
PAYMENT_EXECUTION=false
SECRET_VALUES_PRINTED=false
PROOF=$LOG
EOF
