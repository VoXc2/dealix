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

# ---- Throughput controls (speed & throughput program) -----------------
# Complexity-aware turn budgets instead of a blanket max for every seat.
declare -A ROLE_TURNS=(
  [EXECUTIVE_OPERATIONS]=3
  [REVENUE_SALES]=4
  [MARKET_PARTNERSHIPS]=4
  [CUSTOMER_DELIVERY]=3
  [PRODUCT_ENGINEERING]=4
  [GOVERNANCE_FINANCE]=3
)
SYNTH_TURNS=6
ROLE_TURNS_DEFAULT=4
declare -A ROLE_SLICES=(
  [EXECUTIVE_OPERATIONS]=""
  [REVENUE_SALES]="PUBLIC PRODUCTION CODES,RECENT AUTOPILOT PROOF,OPEN DRAFT"
  [MARKET_PARTNERSHIPS]="PUBLIC PRODUCTION CODES"
  [CUSTOMER_DELIVERY]="VPS CORE,RECENT AUTOPILOT PROOF"
  [PRODUCT_ENGINEERING]="WORKTREE,PUBLIC PRODUCTION CODES,VPS CORE,OPEN DRAFT,RECENT MAIN WORKFLOWS"
  [GOVERNANCE_FINANCE]="VPS CORE,PUBLIC PRODUCTION CODES,CANONICAL RULES"
)
ROLE_TIMEOUT="${DEALIX_COUNCIL_ROLE_TIMEOUT:-300}"     # per-seat wall clock (sec); CPU-4B measured >240s per seat
SYNTH_TIMEOUT="${DEALIX_COUNCIL_SYNTH_TIMEOUT:-300}"   # synthesis wall clock (sec); CPU-4B synthesis measured >180s
FAST_ROLES="${DEALIX_COUNCIL_FAST_ROLES:-}"            # comma list; empty = FULL council
FORCE_RUN="${DEALIX_COUNCIL_FORCE:-0}"                 # 1 = ignore input-unchanged skip

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

# ---- SKIP_UNCHANGED: never spend LLM calls on identical state ----------
# Hash a DETERMINISTIC core-state fingerprint (git head + branch + canonical
# state files). The full sanitized packet embeds volatile telemetry
# (memory/GB, probe timestamps), which would make whole-packet hashing
# never match.
INPUT_HASH="$( { cd "$REPO_ROOT" && git rev-parse HEAD 2>/dev/null; git branch --show-current 2>/dev/null; \
  md5sum docs/commercial/DEALIX_OS_EXECUTION_BOARD_SEED.csv \
         dealix/transformation/business_now_cache.yaml \
         dealix/transformation/kpi_baselines.yaml 2>/dev/null | awk '{print $1}'; } \
  | sha256sum | cut -c1-16 )"
LAST_RUN_DIR_FILE="${STATE_DIR}/last_run_dir"
LAST_HASH_FILE="${STATE_DIR}/last_input_hash"
LAST_RUN_DIR=""
[[ -f "$LAST_RUN_DIR_FILE" ]] && LAST_RUN_DIR="$(cat "$LAST_RUN_DIR_FILE" 2>/dev/null || true)"

if [[ "$FORCE_RUN" != "1" && -n "$LAST_RUN_DIR" && "$(cat "$LAST_HASH_FILE" 2>/dev/null || true)" == "$INPUT_HASH" && -f "${LAST_RUN_DIR}/CEO_DAILY_COMMAND.md" ]]; then
  log "SKIP_REASON=input_unchanged reusing=${LAST_RUN_DIR}"
  mkdir -p "$RUN_DIR"
  cp -a "${LAST_RUN_DIR}/." "$RUN_DIR/" 2>/dev/null || true
  printf '{"skipped":"input_unchanged","reused_from":"%s","input_hash":"%s"}\n' "$LAST_RUN_DIR" "$INPUT_HASH" >"${RUN_DIR}/PROOF.json"
  chmod 0640 "${RUN_DIR}/PROOF.json"
  log "AGENT_COUNCIL_COMPLETE: mode=SKIP_UNCHANGED reports=${RUN_DIR} external_actions=0"
  exit 0
fi


# ---- CONTEXT SLICING: each seat reads only its relevant packet sections ----
# Packet sections are delimited by "== NAME ==" markers. Seats declare the
# section-name regexes they need; CANONICAL RULES + header are always included.
slice_packet() {
  local out="$1"; shift
  awk -v keep="$*" '
    /^== / {
      name=substr($0,4)
      want=0
      n=split(keep, arr, ",")
      for(i=1;i<=n;i++) if(index(name, arr[i])>0) want=1
      insec=1
    }
    want || !insec { print }
  ' "$PACKET" >"$out"
}

run_role() {
  local role_id="$1"
  local mandate="$2"
  local focus="$3"
  local out="${RUN_DIR}/${role_id}.md"
  local prompt="${RUN_DIR}/${role_id}.prompt.txt"
  local turns="${ROLE_TURNS[$role_id]:-$ROLE_TURNS_DEFAULT}"
  local t0 t1
  local SLICED_PACKET=""
  local spec="${ROLE_SLICES[$role_id]:-}"
  if [[ -n "$spec" ]]; then
    # CANONICAL RULES are non-negotiable in every seat context.
    SLICED_PACKET="${RUN_DIR}/${role_id}.packet.txt"
    slice_packet "$SLICED_PACKET" "${spec},CANONICAL RULES"
  fi

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
$(cat "${SLICED_PACKET:-$PACKET}")
EOF

  log "ROLE_START: ${role_id}"
  t0="$(date +%s)"
  set +e
  timeout --kill-after=15 --signal=TERM "$ROLE_TIMEOUT" \
    "$HERMES_BIN" --ignore-rules chat --toolsets safe --max-turns "$turns" --query "$(cat "$prompt")" \
    2>&1 | redact | tee "$out"
  rc=${PIPESTATUS[0]}
  set -e
  t1="$(date +%s)"
  rm -f "$prompt"
  if [[ $rc -eq 124 ]] || [[ $rc -eq 137 ]]; then
    log "ROLE_TIMEOUT: ${role_id} after ${ROLE_TIMEOUT}s (partial evidence preserved)"
    printf '\nROLE_RUNTIME_TIMEOUT=%ss\n' "$ROLE_TIMEOUT" >>"$out"
    RUN_FAILED=1
    SEAT_TIMEOUT=$((SEAT_TIMEOUT + 1))
  elif [[ $rc -ne 0 ]]; then
    log "ROLE_FAIL: ${role_id} rc=${rc} duration=$((t1 - t0))s"
    printf '\nROLE_RUNTIME_ERROR=%s\n' "$rc" >>"$out"
  else
    log "ROLE_OK: ${role_id} duration=$((t1 - t0))s turns=${turns}"
  fi
}

# ---- Seat selection: FULL council by default, FAST subset via env --------
# DEALIX_COUNCIL_FAST_ROLES="REVENUE_SALES,PRODUCT_ENGINEERING" runs only
# those seats (+ synthesis). Local provider serializes generation
# (Ollama num_parallel=1), so seat parallelism adds queueing, not speed;
# wall-clock wins come from budgets, timeouts, skip-unchanged and FAST mode.
ALL_SEATS=(
  "EXECUTIVE_OPERATIONS|Act as COO/Chief of Staff over the existing Dealix operating spine.|cross-department priorities, dependencies, founder workload, execution sequencing"
  "REVENUE_SALES|Act as Revenue Intelligence and Sales Strategy leadership.|money-now action, closeability, qualified pipeline, diagnostics, proposal/follow-up readiness, objections"
  "MARKET_PARTNERSHIPS|Act as Saudi/GCC Market Intelligence and Partnerships leadership.|sourced market triggers, accounts, sectors, partners, Saudi market-access opportunities; no spam"
  "CUSTOMER_DELIVERY|Act as Customer Value, Managed Operations and Delivery leadership.|delivery readiness, onboarding, support patterns, value proof, churn/expansion signals, operating blockers"
  "PRODUCT_ENGINEERING|Act as Product and Engineering portfolio leadership without changing code.|production trust, CI/PR state, product gaps, technical debt, highest-leverage safe engineering work"
  "GOVERNANCE_FINANCE|Act as Governance, Risk, Proof and Finance control leadership.|approval boundaries, proof integrity, security/privacy, invoice/payment evidence, costs, margin/risk posture"
)
if [[ -n "$FAST_ROLES" ]]; then
  IFS=',' read -r -a WANTED <<<"$FAST_ROLES"
  SELECTED_SEATS=()
  for row in "${ALL_SEATS[@]}"; do
    for w in "${WANTED[@]}"; do
      [[ "${row%%|*}" == "$w" ]] && SELECTED_SEATS+=("$row") && break
    done
  done
  log "MODE=FAST seats=${SELECTED_SEATS[*]:-none}"
else
  SELECTED_SEATS=("${ALL_SEATS[@]}")
  log "MODE=FULL seats=${#SELECTED_SEATS[@]}"
fi

if (( ${#SELECTED_SEATS[@]} == 0 )); then
  log "BLOCKED: FAST_ROLES matched no known seat; refusing 0-seat council"
  exit 5
fi

COUNCIL_T0="$(date +%s)"
SEAT_TIMEOUT=0
SEAT_FAILED=0
for row in "${SELECTED_SEATS[@]}"; do
  ROLE_ID="${row%%|*}"
  REST="${row#*|}"
  MANDATE="${REST%%|*}"
  FOCUS="${REST#*|}"
  run_role "$ROLE_ID" "$MANDATE" "$FOCUS"
done
log "ROLES_DONE total_duration=$(( $(date +%s) - COUNCIL_T0 ))s seats=${#SELECTED_SEATS[@]}"

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
S0="$(date +%s)"
set +e
timeout --kill-after=15 --signal=TERM "$SYNTH_TIMEOUT" \
  "$HERMES_BIN" --ignore-rules chat --toolsets safe --max-turns "$SYNTH_TURNS" --query "$(cat "$SYNTH_PROMPT")" \
  2>&1 | redact | tee "$SYNTHESIS"
CEO_RC=${PIPESTATUS[0]}
set -e
log "CEO_CHAIR duration=$(( $(date +%s) - S0 ))s turns=${SYNTH_TURNS}"
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
  "seats_configured": ${#SELECTED_SEATS[@]},
  "seats_failed": ${SEAT_FAILED:-0},
  "seats_timeout": ${SEAT_TIMEOUT:-0},
  "mode": "${FAST_ROLES:+fast}${FAST_ROLES:-full}",
  "total_duration_s": "$(( $(date +%s) - COUNCIL_T0 ))",
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

log "AGENT_COUNCIL_COMPLETE: reports=${RUN_DIR} ceo_rc=${CEO_RC} external_actions=0 total_duration=$(( $(date +%s) - COUNCIL_T0 ))s"

# Persist skip-state pointers ONLY after clean synthesis AND zero seat
# failures/timeouts — a degraded run must never be reused as "unchanged"
# truth by SKIP_UNCHANGED, and the exit code must not fake success.
if [[ $CEO_RC -eq 0 && ${RUN_FAILED:-0} -eq 0 ]]; then
  printf '%s\n' "$RUN_DIR" >"$LAST_RUN_DIR_FILE"
  printf '%s\n' "$INPUT_HASH" >"$LAST_HASH_FILE"
fi
if [[ ${RUN_FAILED:-0} -ne 0 ]]; then
  log "COUNCIL_DEGRADED: seat failures/timeouts present; pointers NOT persisted"
  exit 1
fi
exit "$CEO_RC"
