#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

REPO_ROOT="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
COUNCIL_ROOT="${DEALIX_AGENT_COUNCIL_ROOT:-/opt/dealix/company-agents}"
REPORT_DIR="${COUNCIL_ROOT}/reports"
LOG_DIR="${COUNCIL_ROOT}/logs"
STATE_DIR="${COUNCIL_ROOT}/state"
HERMES_BIN="${HERMES_BIN:-/home/dealix/.local/bin/hermes}"
MODEL_PRIMARY="${DEALIX_LOCAL_MODEL:-qwen3:4b-instruct-2507-q4_K_M}"
STAMP="$(date +%Y%m%d-%H%M%S)"
DAY="$(date +%F)"
RUN_DIR="${REPORT_DIR}/${DAY}/${STAMP}"
RUN_LOG="${LOG_DIR}/council-${STAMP}.log"
LATEST_COMMAND="${REPORT_DIR}/LATEST_DAILY_COMMAND.md"
LOCK="${STATE_DIR}/agent-council.lock"

export TZ="${TZ:-Asia/Riyadh}"
export DEALIX_EXTERNAL_OUTREACH_ENABLED=false
export EXTERNAL_OUTREACH_ENABLED=false
export AUTO_SEND_ENABLED=false
export AGENT_APPROVAL_MODE=required
export WHATSAPP_ALLOW_LIVE_SEND=false
export MOYASAR_LIVE_MODE=0

mkdir -p "$RUN_DIR" "$LOG_DIR" "$STATE_DIR"
chmod 0750 "$COUNCIL_ROOT" "$REPORT_DIR" "$LOG_DIR" "$STATE_DIR" "$RUN_DIR" 2>/dev/null || true

touch "$RUN_LOG"
chmod 0640 "$RUN_LOG"
exec > >(tee -a "$RUN_LOG") 2>&1

redact() {
  python3 -u -c '
import re, sys
patterns = [
    re.compile(r"(?i)(authorization:\s*bearer\s+)[^\s]+"),
    re.compile(r"\bgh[opsu]_[A-Za-z0-9_-]{10,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_-]{10,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{10,}\b"),
    re.compile(r"\b\d{6,}:[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"(?i)\b([A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)[A-Z0-9_]*)\s*=\s*[^\s]+"),
]
email = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
phone = re.compile(r"(?<!\d)(?:\+?966|0)?5\d{8}(?!\d)")
for line in sys.stdin:
    for p in patterns:
        if p.groups:
            line = p.sub(lambda m: f"{m.group(1)}[REDACTED]", line)
        else:
            line = p.sub("[REDACTED]", line)
    line = re.sub(r"(?i)([?&](?:token|key|secret|password|signature)=)[^&\s]+", r"\1[REDACTED]", line)
    line = email.sub("[EMAIL_REDACTED]", line)
    line = phone.sub("[PHONE_REDACTED]", line)
    sys.stdout.write(line)
'
}

log() {
  printf '[%s] %s\n' "$(date -Is)" "$*"
}

if [[ ! -d "$REPO_ROOT/.git" ]]; then
  log "BLOCKED: canonical repository missing at $REPO_ROOT"
  exit 2
fi
if [[ ! -x "$HERMES_BIN" ]]; then
  log "BLOCKED: Hermes CLI missing at $HERMES_BIN"
  exit 3
fi
if ! curl -fsS --max-time 5 http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
  log "BLOCKED: local Ollama API unavailable"
  exit 4
fi

exec 9>"$LOCK"
if ! flock -n 9; then
  log "SKIP: Agent Council is already running"
  exit 0
fi

AVAILABLE_MB="$(( $(awk '/MemAvailable:/ {print $2}' /proc/meminfo) / 1024 ))"
log "memory_available_mb=${AVAILABLE_MB}"
if (( AVAILABLE_MB < 3500 )); then
  log "SKIP: memory guard below 3500MB"
  exit 0
fi

cd "$REPO_ROOT"
PACKET="${RUN_DIR}/company_packet.txt"
{
  echo "DEALIX AGENT COUNCIL INPUT PACKET"
  echo "generated_at=$(date -Is)"
  echo "repo_head=$(git rev-parse HEAD 2>/dev/null || echo unknown)"
  echo "repo_branch=$(git branch --show-current 2>/dev/null || echo unknown)"
  echo "origin_main=$(git rev-parse origin/main 2>/dev/null || echo unknown)"
  echo
  echo "== WORKTREE =="
  git status -sb 2>/dev/null || true
  echo
  echo "== PUBLIC PRODUCTION CODES =="
  for url in https://api.dealix.me/health https://api.dealix.me/healthz https://dealix.me/ar; do
    code="$(curl -L -sS -o /dev/null -w '%{http_code}' --connect-timeout 5 --max-time 15 "$url" 2>/dev/null || echo 000)"
    printf '%s %s\n' "$code" "$url"
  done
  echo
  echo "== VPS CORE =="
  for svc in docker ollama tailscaled fail2ban; do
    printf '%s=%s\n' "$svc" "$(systemctl is-active "$svc" 2>/dev/null || true)"
  done
  printf 'issue_bridge=%s\n' "$(systemctl is-active dealix-vps-issue-bridge.timer 2>/dev/null || true)"
  if docker inspect dealix-n8n >/dev/null 2>&1; then
    printf 'n8n_running=%s\n' "$(docker inspect -f '{{.State.Running}}' dealix-n8n 2>/dev/null || echo false)"
  else
    echo 'n8n_running=missing'
  fi
  printf 'disk_used_pct=%s\n' "$(df -P / | awk 'NR==2 {print $5}')"
  printf 'memory_available_mb=%s\n' "$AVAILABLE_MB"
  echo
  echo "== RECENT AUTOPILOT PROOF =="
  for mode in heartbeat production repo-watch preflight midday evening nightly local-ai; do
    f="/opt/dealix/company-autopilot/logs/${mode}-latest.log"
    if [[ -f "$f" ]]; then
      echo "--- ${mode} ---"
      tail -n 30 "$f" 2>/dev/null || true
    fi
  done
  echo
  echo "== OPEN DRAFT/ACTIVE PRS =="
  if command -v gh >/dev/null 2>&1; then
    gh pr list --repo Dealix-sa/dealix --state open --limit 20 \
      --json number,title,isDraft,mergeable,headRefName,updatedAt 2>/dev/null || true
    echo
    echo "== RECENT MAIN WORKFLOWS =="
    gh run list --repo Dealix-sa/dealix --branch main --limit 12 \
      --json name,status,conclusion,createdAt 2>/dev/null || true
  fi
  echo
  echo "== CANONICAL RULES =="
  echo "No external send. No merge to main. No production/DNS mutation. No payments/refunds."
  echo "Synthetic evidence is not customer/revenue/payment/delivery proof."
  echo "Company Brain, Opportunity Graph, Approval Center, Proof/Learning and Strategy systems remain canonical in Dealix."
} | redact >"$PACKET"
chmod 0640 "$PACKET"

run_role() {
  local role_id="$1"
  local mandate="$2"
  local focus="$3"
  local out="${RUN_DIR}/${role_id}.md"
  local prompt="${RUN_DIR}/${role_id}.prompt.txt"

  cat >"$prompt" <<EOF
You are a bounded internal member of the Dealix Agent Council.

ROLE: ${role_id}
MANDATE: ${mandate}
FOCUS: ${focus}

You are not allowed to execute or authorize external effects. You are analyzing a sanitized current-state packet. Use web research only when it materially verifies a time-sensitive public fact. Do not invent customers, revenue, payments, proof, partnerships, or production state.

Separate FACTS from INFERENCES. Prioritize Business Impact x Urgency x Ease x Evidence / Risk.

Return concise Markdown with exactly these headings:
# ${role_id}
## Facts
## Risks
## Opportunities
## Safe Internal Actions
## Approval Items
## Proof Gaps
## Highest Next Action

Approval Items must contain only actions that truly require founder approval. Safe Internal Actions must not include send, publish, merge, production/DNS mutation, payments/refunds, secret changes, deletion, or legal commitments.

CURRENT PACKET:
$(cat "$PACKET")
EOF

  log "ROLE_START: ${role_id}"
  set +e
  "$HERMES_BIN" --ignore-rules chat --toolsets safe --max-turns 6 --query "$(cat "$prompt")" \
    2>&1 | redact | tee "$out"
  rc=${PIPESTATUS[0]}
  set -e
  rm -f "$prompt"
  if [[ $rc -ne 0 ]]; then
    log "ROLE_FAIL: ${role_id} rc=${rc}"
    printf '\nROLE_RUNTIME_ERROR=%s\n' "$rc" >>"$out"
  else
    log "ROLE_OK: ${role_id}"
  fi
}

run_role "EXECUTIVE_OPERATIONS" \
  "Act as COO/Chief of Staff over the existing Dealix operating spine." \
  "cross-department priorities, dependencies, founder workload, execution sequencing"

run_role "REVENUE_SALES" \
  "Act as Revenue Intelligence and Sales Strategy leadership." \
  "money-now action, closeability, qualified pipeline, diagnostics, proposal/follow-up readiness, objections"

run_role "MARKET_PARTNERSHIPS" \
  "Act as Saudi/GCC Market Intelligence and Partnerships leadership." \
  "sourced market triggers, accounts, sectors, partners, Saudi market-access opportunities; no spam"

run_role "CUSTOMER_DELIVERY" \
  "Act as Customer Value, Managed Operations and Delivery leadership." \
  "delivery readiness, onboarding, support patterns, value proof, churn/expansion signals, operating blockers"

run_role "PRODUCT_ENGINEERING" \
  "Act as Product and Engineering portfolio leadership without changing code." \
  "production trust, CI/PR state, product gaps, technical debt, highest-leverage safe engineering work"

run_role "GOVERNANCE_FINANCE" \
  "Act as Governance, Risk, Proof and Finance control leadership." \
  "approval boundaries, proof integrity, security/privacy, invoice/payment evidence, costs, margin/risk posture"

SYNTHESIS="${RUN_DIR}/CEO_DAILY_COMMAND.md"
SYNTH_PROMPT="${RUN_DIR}/ceo.prompt.txt"
{
  cat <<'EOF'
You are the Dealix CEO Agent Council Chair. Synthesize the specialist reports below into one evidence-first Daily Company Command for the founder.

Do not invent missing facts. Do not execute external actions. Do not turn a recommendation into a claim of completion.

Resolve conflicts by this priority order:
P0 Production Trust/Security
P1 Revenue/Closeability
P2 Founder workload
P3 Customer value/delivery
P4 Proof quality
P5 Growth automation
P6 Optimization
P7 New features

Return concise Markdown with exactly these headings:
# Dealix Daily Company Command
## Production Status
## Money-Now Action
## Technical Blocker
## Commercial Blocker
## Top Opportunities
## Department Actions
## Approval Queue
## Proof Gaps
## Learning
## Highest Next Action
## Proof Log

For Department Actions, include an owner seat and only safe internal actions. Approval Queue must include exact target/action/risk/rollback and never imply approval has been granted.

SPECIALIST REPORTS
EOF
  for f in "$RUN_DIR"/*.md; do
    [[ "$f" == "$SYNTHESIS" ]] && continue
    echo
    echo "===== $(basename "$f") ====="
    cat "$f"
  done
} >"$SYNTH_PROMPT"

log "ROLE_START: CEO_CHAIR"
set +e
"$HERMES_BIN" --ignore-rules chat --toolsets safe --max-turns 8 --query "$(cat "$SYNTH_PROMPT")" \
  2>&1 | redact | tee "$SYNTHESIS"
CEO_RC=${PIPESTATUS[0]}
set -e
rm -f "$SYNTH_PROMPT"

if [[ $CEO_RC -eq 0 ]]; then
  cp "$SYNTHESIS" "$LATEST_COMMAND"
  chmod 0640 "$LATEST_COMMAND"
  log "ROLE_OK: CEO_CHAIR"
else
  log "ROLE_FAIL: CEO_CHAIR rc=${CEO_RC}"
fi

cat >"${RUN_DIR}/PROOF.json" <<EOF
{
  "run_id": "agent-council-${STAMP}",
  "timestamp": "$(date -Is)",
  "repo_head": "$(git rev-parse HEAD 2>/dev/null || echo unknown)",
  "packet": "${PACKET}",
  "reports": 6,
  "ceo_exit_code": ${CEO_RC},
  "external_actions_executed": 0,
  "merge_to_main": false,
  "production_mutation": false,
  "payment_execution": false,
  "synthetic_is_commercial_proof": false
}
EOF
chmod 0640 "${RUN_DIR}/PROOF.json"

# Free model memory after the council. Ignore if Hermes used another local alias.
ollama stop "$MODEL_PRIMARY" >/dev/null 2>&1 || true
ollama stop "${MODEL_PRIMARY}:latest" >/dev/null 2>&1 || true

find "$REPORT_DIR" -type d -mindepth 2 -mtime +30 -exec rm -rf {} + 2>/dev/null || true
find "$LOG_DIR" -type f -name '*.log' -mtime +14 -delete 2>/dev/null || true

log "AGENT_COUNCIL_COMPLETE: reports=${RUN_DIR} ceo_rc=${CEO_RC} external_actions=0"
exit "$CEO_RC"
