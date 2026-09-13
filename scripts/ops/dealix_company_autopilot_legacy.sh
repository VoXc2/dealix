#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

MODE="${1:-status}"
ROOT="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
AUTOPILOT_ROOT="${DEALIX_AUTOPILOT_ROOT:-/opt/dealix/company-autopilot}"
LOG_DIR="${AUTOPILOT_ROOT}/logs"
STATE_DIR="${AUTOPILOT_ROOT}/state"
REPORT_DIR="${AUTOPILOT_ROOT}/reports"
SIGNAL_INBOX_DIR="${DEALIX_MARKET_RADAR_INBOX_DIR:-${AUTOPILOT_ROOT}/inbox}"
ISSUE_REPO="Dealix-sa/dealix"
ISSUE_NUMBER="1119"
LOCAL_MODEL_PRIMARY="${DEALIX_LOCAL_MODEL:-qwen3:4b-instruct-2507-q4_K_M}"
LOCAL_MODEL_FALLBACK="${DEALIX_LOCAL_MODEL:-qwen3:4b-instruct-2507-q4_K_M}"

export TZ="${TZ:-Asia/Riyadh}"
export PYTHONIOENCODING=utf-8
export DEALIX_EXTERNAL_OUTREACH_ENABLED=false
export EXTERNAL_OUTREACH_ENABLED=false
export AUTO_SEND_ENABLED=false
export AGENT_APPROVAL_MODE=required
export WHATSAPP_ALLOW_LIVE_SEND=false
export MOYASAR_LIVE_MODE=0

mkdir -p "$LOG_DIR" "$STATE_DIR" "$REPORT_DIR" "$SIGNAL_INBOX_DIR"
chmod 0750 "$AUTOPILOT_ROOT" "$LOG_DIR" "$STATE_DIR" "$REPORT_DIR" "$SIGNAL_INBOX_DIR" 2>/dev/null || true

if ! git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "BLOCKED: canonical Dealix repository missing at $ROOT"
  exit 2
fi
cd "$ROOT"

RUN_STAMP="$(date +%Y%m%d-%H%M%S)"
RUN_LOG="${LOG_DIR}/${MODE}-${RUN_STAMP}.log"
LATEST_LOG="${LOG_DIR}/${MODE}-latest.log"
RUN_FAILED=0

redact_stream() {
  python3 -u -c '
import re, sys
patterns = [
    re.compile(r"(?i)(authorization:\s*bearer\s+)[^\s]+"),
    re.compile(r"\bgh[opsu]_[A-Za-z0-9_-]{10,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_-]{10,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{10,}\b"),
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
  printf '[%s] %s\n' "$(date -Is)" "$*" | tee -a "$RUN_LOG"
}

run_step() {
  local label="$1"
  shift
  log "STEP_START: $label"
  set +e
  "$@" 2>&1 | redact_stream | tee -a "$RUN_LOG"
  local rc=${PIPESTATUS[0]}
  set -e
  if [[ $rc -eq 0 ]]; then
    log "STEP_OK: $label"
  else
    log "STEP_FAIL: $label rc=$rc"
    RUN_FAILED=1
  fi
  return 0
}

notify_private() {
  local message="$1"
  if ! command -v gh >/dev/null 2>&1; then
    return 0
  fi
  local tmp
  tmp="$(mktemp)"
  chmod 0600 "$tmp"
  printf '%b\n' "$message" >"$tmp"
  gh api --method POST "repos/${ISSUE_REPO}/issues/${ISSUE_NUMBER}/comments" -F "body=@${tmp}" >/dev/null 2>&1 || true
  rm -f "$tmp"
}

transition_notify() {
  local key="$1"
  local status="$2"
  local message="$3"
  local state_file="${STATE_DIR}/${key}.state"
  local previous="unknown"
  [[ -f "$state_file" ]] && previous="$(cat "$state_file" 2>/dev/null || echo unknown)"
  printf '%s\n' "$status" >"$state_file"
  chmod 0640 "$state_file" 2>/dev/null || true
  if [[ "$previous" != "$status" ]]; then
    notify_private "DEALIX_AUTOPILOT_TRANSITION\n\n- check: ${key}\n- from: ${previous}\n- to: ${status}\n- host: srv1916256\n- time: $(date -Is)\n- repo_head: $(git rev-parse --short HEAD 2>/dev/null || echo unknown)\n\n${message}"
  fi
}

light_lock() {
  exec 8>"${STATE_DIR}/${MODE}.lock"
  if ! flock -n 8; then
    log "SKIP: mode already running: $MODE"
    exit 0
  fi
}

heavy_lock() {
  exec 9>"${STATE_DIR}/heavy.lock"
  if ! flock -n 9; then
    log "SKIP: another heavy Dealix cycle is already running"
    exit 0
  fi
}

resource_guard() {
  local min_available_mb="${1:-1800}"
  local available_kb load1
  available_kb="$(awk '/MemAvailable:/ {print $2}' /proc/meminfo)"
  load1="$(awk '{print $1}' /proc/loadavg)"
  local available_mb=$((available_kb / 1024))
  log "RESOURCE_GUARD: available_mb=${available_mb} load1=${load1}"
  if (( available_mb < min_available_mb )); then
    log "SKIP: memory guard below ${min_available_mb}MB"
    return 1
  fi
  return 0
}

cleanup_logs() {
  find "$LOG_DIR" -type f -name '*.log' -mtime +14 -delete 2>/dev/null || true
  find "$REPORT_DIR" -type f -mtime +30 -delete 2>/dev/null || true
}

service_state() {
  local name="$1" state
  state="$(systemctl is-active "$name" 2>/dev/null || true)"
  printf '%s\n' "${state:-inactive}"
}

http_code() {
  local url="$1" code
  code="$(curl -L -sS -o /dev/null -w '%{http_code}' --connect-timeout 5 --max-time 15 "$url" 2>/dev/null || true)"
  printf '%s\n' "${code:-000}"
}

is_http_ok() {
  [[ "${1:-000}" =~ ^[23][0-9][0-9]$ ]]
}

heartbeat() {
  light_lock
  local bad=0
  log "===== HEARTBEAT ====="
  for svc in docker ollama tailscaled fail2ban; do
    local state
    state="$(service_state "$svc")"
    log "service_${svc}=${state}"
    [[ "$state" == "active" ]] || bad=1
  done

  local bridge_timer
  bridge_timer="$(systemctl is-active dealix-vps-issue-bridge.timer 2>/dev/null || true)"
  bridge_timer="${bridge_timer:-inactive}"
  log "bridge_timer=${bridge_timer}"
  [[ "$bridge_timer" == "active" ]] || bad=1

  if docker inspect dealix-n8n >/dev/null 2>&1; then
    local n8n_running
    n8n_running="$(docker inspect -f '{{.State.Running}}' dealix-n8n 2>/dev/null || echo false)"
    log "n8n_running=${n8n_running}"
    if [[ "$n8n_running" != "true" ]]; then
      log "SELF_HEAL: starting existing dealix-n8n container"
      docker start dealix-n8n 2>&1 | redact_stream | tee -a "$RUN_LOG" || true
      sleep 2
      n8n_running="$(docker inspect -f '{{.State.Running}}' dealix-n8n 2>/dev/null || echo false)"
      log "n8n_running_after_heal=${n8n_running}"
    fi
    [[ "$n8n_running" == "true" ]] || bad=1
  else
    log "n8n_container=missing"
    bad=1
  fi

  if curl -fsS --max-time 5 http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
    log "ollama_api=ok"
  else
    log "ollama_api=fail"
    bad=1
  fi

  local disk_pct mem_mb
  disk_pct="$(df -P / | awk 'NR==2 {gsub(/%/,"",$5); print $5}')"
  mem_mb="$(( $(awk '/MemAvailable:/ {print $2}' /proc/meminfo) / 1024 ))"
  log "root_disk_used_pct=${disk_pct}"
  log "mem_available_mb=${mem_mb}"
  (( disk_pct < 90 )) || bad=1
  (( mem_mb > 700 )) || bad=1

  if (( bad == 0 )); then
    transition_notify heartbeat GREEN "Core VPS services, n8n and Ollama are healthy."
  else
    transition_notify heartbeat RED "One or more infrastructure checks failed. Inspect the private VPS proof/logs."
    RUN_FAILED=1
  fi
}

production() {
  light_lock
  log "===== PRODUCTION TRUST ====="
  local api_health api_healthz site_root site_ar bad=0
  api_health="$(http_code https://api.dealix.me/health)"
  api_healthz="$(http_code https://api.dealix.me/healthz)"
  site_root="$(http_code https://dealix.me/)"
  site_ar="$(http_code https://dealix.me/ar)"
  log "api_health_http=${api_health}"
  log "api_healthz_http=${api_healthz}"
  log "site_root_http=${site_root}"
  log "site_ar_http=${site_ar}"

  is_http_ok "$api_health" || is_http_ok "$api_healthz" || bad=1
  is_http_ok "$site_root" || bad=1
  # /ar is a Next.js route served by the canonical Railway frontend
  # (docs/ops/DEALIX_ME_FRONTEND_DNS_RAILWAY_AR.md). Until the DNS cutover
  # lands, the interim static host returns 404 here by design. Log it as a
  # pending warning instead of failing every probe cycle (false-alert
  # elimination); the root/API hard checks above still catch real outages.
  if is_http_ok "$site_ar"; then
    log "site_ar_status=ok"
  else
    log "site_ar_status=pending_railway_cutover"
  fi

  local counter_file="${STATE_DIR}/production_failures"
  local failures=0
  [[ -f "$counter_file" ]] && failures="$(cat "$counter_file" 2>/dev/null || echo 0)"
  if (( bad == 0 )); then
    printf '0\n' >"$counter_file"
    transition_notify production GREEN "Public API/site probes are responding."
  else
    failures=$((failures + 1))
    printf '%s\n' "$failures" >"$counter_file"
    log "production_consecutive_failures=${failures}"
    if (( failures >= 3 )); then
      transition_notify production RED "Production failed at least three consecutive 15-minute probes. No production mutation was attempted."
    fi
    RUN_FAILED=1
  fi
}

repo_watch() {
  light_lock
  log "===== REPOSITORY / CI WATCH ====="
  run_step "git fetch origin main" git fetch origin main --quiet
  log "local_head=$(git rev-parse HEAD)"
  log "origin_main=$(git rev-parse origin/main)"
  log "branch=$(git branch --show-current)"
  git status -sb 2>&1 | redact_stream | tee -a "$RUN_LOG"

  if command -v gh >/dev/null 2>&1; then
    run_step "latest GitHub runs" gh run list --branch main --limit 12 --json name,status,conclusion,createdAt
  fi
}

preflight() {
  heavy_lock
  resource_guard 1500 || return 0
  log "===== BUSINESS PRE-FLIGHT ====="
  run_step "repository fetch" git fetch origin main --quiet
  run_step "full autonomous plan dry-run" python3 scripts/run_dealix_complete_autonomous_day.py --dry-run
  if [[ -f scripts/founder_comprehensive_plan_status.py ]]; then
    run_step "founder comprehensive status" python3 scripts/founder_comprehensive_plan_status.py
  fi
  if [[ -f scripts/run_founder_production_gates.py ]]; then
    run_step "founder production gates" python3 scripts/run_founder_production_gates.py --api-base https://api.dealix.me
  fi
}

workflow_success_today() {
  local workflow="$1"
  local payload created status conclusion today
  payload="$(gh run list --workflow "$workflow" --limit 1 --json status,conclusion,createdAt 2>/dev/null || true)"
  [[ -n "$payload" && "$payload" != "[]" ]] || return 1
  created="$(printf '%s' "$payload" | jq -r '.[0].createdAt // ""' 2>/dev/null || true)"
  status="$(printf '%s' "$payload" | jq -r '.[0].status // ""' 2>/dev/null || true)"
  conclusion="$(printf '%s' "$payload" | jq -r '.[0].conclusion // ""' 2>/dev/null || true)"
  today="$(date -u +%F)"
  log "workflow=${workflow} created=${created} status=${status} conclusion=${conclusion}"
  [[ "${created:0:10}" == "$today" && "$status" == "completed" && "$conclusion" == "success" ]]
}

morning_fallback() {
  heavy_lock
  resource_guard 1800 || return 0
  log "===== MORNING FAILOVER ====="
  if ! command -v gh >/dev/null 2>&1 || ! command -v jq >/dev/null 2>&1; then
    log "BLOCKED: gh+jq required for duplicate-safe GitHub workflow failover"
    RUN_FAILED=1
    return 0
  fi

  if workflow_success_today daily-revenue-machine.yml; then
    log "SKIP: Daily Revenue Machine already succeeded today"
  else
    log "FALLBACK: Daily Revenue Machine not green today; running canonical local revenue day"
    run_step "founder revenue day fallback" bash scripts/run_founder_revenue_day.sh
  fi

  if workflow_success_today governed-full-ops-daily.yml; then
    log "SKIP: Governed Full Ops already succeeded today"
  else
    log "FALLBACK: Governed Full Ops not green today; running local governed core"
    run_step "governed full ops fallback" python3 scripts/run_dealix_complete_autonomous_day.py --skip-commercial-day
  fi
}

market_radar_run() {
  local radar_script input_file output_file
  radar_script="${ROOT}/scripts/commercial/run_universal_market_radar_v1.py"
  input_file="${DEALIX_MARKET_RADAR_SIGNALS_FILE:-${SIGNAL_INBOX_DIR}/market-radar-signals.json}"
  output_file="${REPORT_DIR}/universal-market-radar-${RUN_STAMP}.json"

  if [[ ! -f "$radar_script" ]]; then
    log "MARKET_RADAR_BLOCKED: runner missing at $radar_script"
    RUN_FAILED=1
    return 0
  fi
  if [[ ! -f "$input_file" ]]; then
    log "MARKET_RADAR_STATE=WAITING_FOR_CANONICAL_SIGNAL_INPUT"
    log "MARKET_RADAR_INPUT=NONE (no collector or connector has supplied a source-bound handoff)"
    return 0
  fi
  if [[ ! -r "$input_file" ]]; then
    log "MARKET_RADAR_BLOCKED: signal handoff is not readable"
    RUN_FAILED=1
    return 0
  fi

  log "MARKET_RADAR_INPUT=SOURCE_BOUND_HANDOFF"
  run_step "read-only market radar brief" python3 "$radar_script" --signals "$input_file" --out "$output_file"
  if [[ -s "$output_file" ]]; then
    chmod 0640 "$output_file" 2>/dev/null || true
    log "MARKET_RADAR_REPORT=${output_file}"
  else
    log "MARKET_RADAR_BLOCKED: runner did not produce a report"
    RUN_FAILED=1
  fi
}

market_radar() {
  heavy_lock
  resource_guard 1200 || return 0
  log "===== MARKET RADAR READ-ONLY ====="
  market_radar_run
}

midday() {
  heavy_lock
  resource_guard 1600 || return 0
  log "===== MIDDAY COMPANY PULSE ====="
  market_radar_run
  if [[ -f scripts/founder_comprehensive_plan_status.py ]]; then
    run_step "comprehensive plan" python3 scripts/founder_comprehensive_plan_status.py
  fi
  if [[ -f scripts/founder_all_motions_pipeline.py ]]; then
    run_step "all motions pipeline" python3 scripts/founder_all_motions_pipeline.py --top-n 5
  fi
  if [[ -f scripts/commercial_war_room_sync.py ]]; then
    run_step "war room sync" python3 scripts/commercial_war_room_sync.py
  fi
  if [[ -f scripts/export_value_plan_snapshot.py ]]; then
    run_step "value plan snapshot" python3 scripts/export_value_plan_snapshot.py
  fi
  if [[ -f scripts/verify_first_paid_diagnostic_tracker.py ]]; then
    run_step "paid diagnostic tracker" python3 scripts/verify_first_paid_diagnostic_tracker.py
  fi
}

evening() {
  heavy_lock
  resource_guard 1600 || return 0
  log "===== EVENING CLOSE ====="
  if [[ -f scripts/founder_cadence.sh ]]; then
    run_step "founder evening evidence" bash scripts/founder_cadence.sh --evening
  fi
  if [[ -f scripts/founder_comprehensive_plan_status.py ]]; then
    run_step "end-of-day status" python3 scripts/founder_comprehensive_plan_status.py
  fi
}

nightly() {
  heavy_lock
  resource_guard 1400 || return 0
  log "===== NIGHTLY TRUST / LEARNING ====="
  if [[ -f scripts/verify_full_autonomous_ops_stack.py ]]; then
    run_step "full autonomous stack" python3 scripts/verify_full_autonomous_ops_stack.py --skip-api
  fi
  if [[ -f scripts/audit_agent_team.py ]]; then
    run_step "agent governance audit" python3 scripts/audit_agent_team.py
  fi
  if command -v make >/dev/null 2>&1; then
    run_step "security smoke" make security-smoke
  fi
  if [[ -f scripts/company_ready_verify.sh ]]; then
    run_step "company ready docs" bash scripts/company_ready_verify.sh --docs-only --skip-go-live
  fi
  if [[ -f scripts/founder_weekly_metrics_bundle.py ]]; then
    # rc=2 means the bundle wrote its artifact but the verdict is BLOCKED on
    # founder-side integrations (moyasar_live, whatsapp_business,
    # gmail_external). That is an expected pending state, not broken
    # automation - log it explicitly instead of degrading every nightly run.
    log "STEP_START: metrics refresh"
    set +e
    python3 scripts/founder_weekly_metrics_bundle.py --write 2>&1 | redact_stream | tee -a "$RUN_LOG"
    metrics_rc=${PIPESTATUS[0]}
    set -e
    if [[ $metrics_rc -eq 0 ]]; then
      log "STEP_OK: metrics refresh"
    elif [[ $metrics_rc -eq 2 ]]; then
      log "STEP_BLOCKED_EXPECTED: metrics refresh (founder-side integrations pending; see FOUNDER_WEEKLY_METRICS_VERDICT)"
    else
      log "STEP_FAIL: metrics refresh rc=${metrics_rc}"
      RUN_FAILED=1
    fi
  fi
}

weekly() {
  heavy_lock
  resource_guard 1600 || return 0
  log "===== WEEKLY CEO LOOP ====="
  if [[ -f scripts/founder_weekly_loop.sh ]]; then
    run_step "founder weekly loop" bash scripts/founder_weekly_loop.sh
  fi
  if [[ -f scripts/commercial/run_weekly_proof_pack.py ]]; then
    run_step "weekly proof pack" python3 scripts/commercial/run_weekly_proof_pack.py
  fi
}

local_ai() {
  heavy_lock
  resource_guard 2600 || return 0
  log "===== LOCAL OLLAMA CEO SYNTHESIS ====="

  if ! curl -fsS --max-time 5 http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
    log "BLOCKED: Ollama API unavailable"
    RUN_FAILED=1
    return 0
  fi
  if ! command -v jq >/dev/null 2>&1; then
    log "BLOCKED: jq unavailable"
    RUN_FAILED=1
    return 0
  fi

  local model="$LOCAL_MODEL_PRIMARY"
  local models
  models="$(ollama list 2>/dev/null | awk 'NR>1 {print $1}' | sed 's/:latest$//' || true)"
  if ! grep -Fxq "$model" <<<"$models"; then
    model="$LOCAL_MODEL_FALLBACK"
  fi
  if ! grep -Fxq "$model" <<<"$models"; then
    log "BLOCKED: neither local Dealix model is installed"
    RUN_FAILED=1
    return 0
  fi

  local source_file="${STATE_DIR}/ai-source-${RUN_STAMP}.txt"
  local payload_file="${STATE_DIR}/ai-payload-${RUN_STAMP}.json"
  local output_file="${REPORT_DIR}/ceo-local-ai-${RUN_STAMP}.md"
  : >"$source_file"
  chmod 0600 "$source_file"

  python3 - "$ROOT" "$source_file" <<'PY'
from pathlib import Path
import sys
root = Path(sys.argv[1])
out = Path(sys.argv[2])
candidates = []
for pattern in ("data/founder_briefs/*.md", "data/war_room_today.json", "reports/autopilot/*.md"):
    candidates.extend(root.glob(pattern))
files = [p for p in candidates if p.is_file()]
files = sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)[:5]
chunks = []
for p in files:
    try:
        text = p.read_text(encoding="utf-8", errors="replace")[:12000]
    except OSError:
        continue
    chunks.append(f"\n### SOURCE {p.relative_to(root)}\n{text}")
out.write_text("\n".join(chunks)[:15000], encoding="utf-8")
PY

  if [[ ! -s "$source_file" ]]; then
    log "SKIP: no current founder/war-room artifacts available for local synthesis"
    rm -f "$source_file"
    return 0
  fi

  python3 - "$model" "$source_file" "$payload_file" <<'PY'
import json, sys
from pathlib import Path
model = sys.argv[1]
source = Path(sys.argv[2]).read_text(encoding="utf-8", errors="replace")
prompt = """You are the internal Dealix CEO synthesis model. Use only the supplied internal material.
Do not invent customers, revenue, payments, results, or proof. Do not output email addresses, phone numbers, personal names, tokens, credentials, secrets, or other PII. Aggregate and anonymize.
Return concise Markdown with exactly these headings:
# Current State
# Money-Now
# Production / Operational Risk
# Approvals Waiting
# Proof Captured
# Learning
# Highest Next Action
If evidence is missing, say MISSING EVIDENCE.

INTERNAL MATERIAL:\n""" + source
payload = {
    "model": model,
    "messages": [{"role": "user", "content": prompt}],
    "stream": False,
    "keep_alive": "10m",
    "options": {"num_ctx": 8192, "num_predict": 900, "temperature": 0.2},
}
Path(sys.argv[3]).write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
PY
  chmod 0600 "$payload_file"

  set +e
  curl --fail --silent --show-error --max-time 900 \
    http://127.0.0.1:11434/api/chat \
    -H 'Content-Type: application/json' \
    --data-binary "@${payload_file}" \
    | jq -r '.message.content // .error // "NO_CONTENT"' \
    | redact_stream >"$output_file"
  local rc=${PIPESTATUS[0]}
  set -e
  chmod 0640 "$output_file" 2>/dev/null || true
  rm -f "$source_file" "$payload_file"

  if [[ $rc -eq 0 && -s "$output_file" ]]; then
    log "LOCAL_AI_OK: report=${output_file} model=${model}"
  else
    log "LOCAL_AI_FAIL: rc=${rc}"
    RUN_FAILED=1
  fi

  ollama stop "$model" >/dev/null 2>&1 || true
}

status() {
  light_lock
  log "===== DEALIX COMPANY AUTOPILOT STATUS ====="
  log "host=$(hostname)"
  log "repo_head=$(git rev-parse HEAD)"
  log "repo_branch=$(git branch --show-current)"
  log "autopilot_root=${AUTOPILOT_ROOT}"
  echo
  systemctl list-timers 'dealix-company-*' --no-pager 2>&1 | redact_stream | tee -a "$RUN_LOG" || true
  echo
  for key in heartbeat production; do
    if [[ -f "${STATE_DIR}/${key}.state" ]]; then
      log "${key}_state=$(cat "${STATE_DIR}/${key}.state")"
    fi
  done
  log "ollama=$(service_state ollama)"
  log "docker=$(service_state docker)"
  local bridge_state
  bridge_state="$(systemctl is-active dealix-vps-issue-bridge.timer 2>/dev/null || true)"
  log "bridge_timer=${bridge_state:-inactive}"
  docker ps --filter name=dealix-n8n --format 'n8n={{.Status}} {{.Ports}}' 2>&1 | redact_stream | tee -a "$RUN_LOG" || true
  free -h 2>&1 | tee -a "$RUN_LOG"
}

case "$MODE" in
  heartbeat) heartbeat ;;
  production) production ;;
  repo-watch) repo_watch ;;
  preflight) preflight ;;
  morning-fallback) morning_fallback ;;
  midday) midday ;;
  evening) evening ;;
  nightly) nightly ;;
  market-radar) market_radar ;;
  weekly) weekly ;;
  local-ai) local_ai ;;
  status) status ;;
  *)
    echo "DENIED: unsupported mode '$MODE'"
    echo "Allowed: status heartbeat production repo-watch preflight morning-fallback midday evening nightly market-radar weekly local-ai"
    exit 64
    ;;
esac

cleanup_logs
ln -sfn "$RUN_LOG" "$LATEST_LOG" 2>/dev/null || true
log "RUN_COMPLETE: mode=${MODE} result=$([[ $RUN_FAILED -eq 0 ]] && echo PASS || echo DEGRADED)"

# Living Fleet hand-off (Phase 8.1): the canonical cadence wakes role owners.
# heartbeat stays sensor-only; production/preflight have no fleet seats yet.
case "${MODE}" in
  morning)   FLEET_EVENT="morning" ;;
  midday)    FLEET_EVENT="midday" ;;
  evening)   FLEET_EVENT="evening" ;;
  nightly)   FLEET_EVENT="nightly" ;;
  market-radar) FLEET_EVENT="heartbeat" ;; # reuse existing event; no new fleet event
  repo-watch) FLEET_EVENT="repo_watch" ;;
  local-ai)  FLEET_EVENT="strategic" ;;
  *)         FLEET_EVENT="heartbeat" ;; # preflight/morning-fallback/production/heartbeat
esac
if command -v /opt/dealix/control/bin/living_fleet_dispatch.sh >/dev/null 2>&1; then
  set +e
  /opt/dealix/control/bin/living_fleet_dispatch.sh "${FLEET_EVENT}" >/dev/null 2>&1 || true
  set -e
fi
exit "$RUN_FAILED"
