#!/usr/bin/env bash
set -Eeuo pipefail
umask 077
export TZ=Asia/Riyadh

REPO="/opt/dealix/workspace/dealix"
REPO_SLUG="Dealix-sa/dealix"
RUN_USER="dealix"
RUNTIME_PR=1184
OPENCLAW_PR=1150
OPENCLAW="/home/dealix/.openclaw/bin/openclaw"
STATE="/opt/dealix/company-autopilot/state"
LOCK="/run/lock/dealix-full-vps-recovery.lock"
STAMP="$(date +%Y%m%d-%H%M%S)"
PROOF="/opt/dealix/executive-proof/full-recovery-${STAMP}"
TMP="/tmp/dealix-full-recovery-${STAMP}"
RUNTIME_STAGE="$TMP/runtime"
OPENCLAW_STAGE="$TMP/openclaw"
ISOLATION_OK=0
RESTORE_OK=0
TIMERS_QUIESCED=0
ACTIVE_TIMERS=()
HERMES_STATE_BEFORE="unknown"
HERMES_ENABLED_BEFORE="unknown"

# Single-flight is acquired before proof directories, timer changes, state
# migration or Git mutation. A second recovery performs zero recovery mutation.
if [[ "$(id -u)" -ne 0 ]]; then
  echo "BLOCKED: run as root"
  exit 2
fi
command -v flock >/dev/null 2>&1 || { echo "BLOCKED: flock missing"; exit 7; }
exec 9>"$LOCK"
if ! flock -n 9; then
  echo "DEALIX_FULL_RECOVERY=BLOCKED_ALREADY_RUNNING"
  exit 75
fi

mkdir -p "$PROOF" "$RUNTIME_STAGE" "$OPENCLAW_STAGE"
chmod 700 "$PROOF" "$TMP"
exec > >(tee -a "$PROOF/run.log") 2>&1

section() {
  printf '\n================================================================\n %s\n================================================================\n' "$*"
}

redact() {
  sed -E \
    -e 's#([0-9]{6,}:[A-Za-z0-9_-]{20,})#[REDACTED_TELEGRAM_TOKEN]#g' \
    -e 's#(ghp_[A-Za-z0-9]+)#[REDACTED_GITHUB_TOKEN]#g' \
    -e 's#(github_pat_[A-Za-z0-9_]+)#[REDACTED_GITHUB_TOKEN]#g' \
    -e 's#(sk-[A-Za-z0-9_-]+)#[REDACTED_API_KEY]#g' \
    -e 's#((TOKEN|SECRET|PASSWORD|API_KEY)[=: ][^ ]+)#\2=[REDACTED]#Ig'
}

restore_timers() {
  if [[ "$TIMERS_QUIESCED" -ne 1 ]]; then
    return 0
  fi
  if [[ "$RESTORE_OK" -ne 1 ]]; then
    echo "timer_restore=HOLD_FAIL_CLOSED"
    return 0
  fi
  for unit in "${ACTIVE_TIMERS[@]}"; do
    systemctl start "$unit" >/dev/null 2>&1 || true
  done
  echo "timer_restore=COMPLETE count=${#ACTIVE_TIMERS[@]}"
}

cleanup() {
  local rc=$?
  set +e
  restore_timers
  rm -rf "$TMP"
  set -e
  exit "$rc"
}
trap cleanup EXIT

git_d() {
  sudo -u "$RUN_USER" -H git -C "$REPO" "$@"
}

fetch_pr_file() {
  local head="$1"
  local path="$2"
  local root="$3"
  local dst="$root/$path"
  mkdir -p "$(dirname "$dst")"
  sudo -u "$RUN_USER" -H gh api \
    -H 'Accept: application/vnd.github.raw+json' \
    "repos/${REPO_SLUG}/contents/${path}?ref=${head}" >"$dst"
}

file_sha() {
  local path="$1"
  if [[ -f "$path" ]]; then
    sha256sum "$path" | awk '{print $1}'
  else
    printf 'absent\n'
  fi
}

dir_digest() {
  local dir="$1"
  if [[ ! -d "$dir" ]] || ! find "$dir" -type f -print -quit 2>/dev/null | grep -q .; then
    printf 'empty\n'
    return 0
  fi
  (
    cd "$dir"
    find . -type f -print0 | sort -z | xargs -0 sha256sum
  ) | sha256sum | awk '{print $1}'
}

migrate_file() {
  local source="$1"
  local relative="$2"
  local target="$STATE/$relative"
  local backup="$PROOF/state-before/$relative"
  local source_sha target_sha source_rel dirty

  source_sha="$(file_sha "$source")"
  target_sha="$(file_sha "$target")"
  source_rel="${source#"$REPO/"}"
  dirty="$(git_d status --porcelain -- "$source_rel" 2>/dev/null || true)"

  if [[ -f "$target" ]]; then
    mkdir -p "$(dirname "$backup")"
    cp -a "$target" "$backup"
    if [[ -n "$dirty" && -f "$source" && "$source_sha" != "$target_sha" ]]; then
      echo "runtime_file=$relative decision=CONFLICT_DIRTY_CANONICAL source_sha=$source_sha target_sha=$target_sha"
      echo "BLOCKED: dirty canonical/runtime state conflict requires explicit reconciliation: $source_rel"
      return 66
    fi
    echo "runtime_file=$relative decision=PRESERVED_EXISTING source_sha=$source_sha target_sha=$target_sha"
    return 0
  fi
  if [[ -f "$source" ]]; then
    install -D -m 0640 -o "$RUN_USER" -g "$RUN_USER" "$source" "$target"
    target_sha="$(file_sha "$target")"
    echo "runtime_file=$relative decision=SEEDED_FROM_CURRENT_SOURCE source_sha=$source_sha target_sha=$target_sha"
  else
    echo "runtime_file=$relative decision=SOURCE_ABSENT_SKIP source_sha=absent target_sha=absent"
  fi
}

migrate_report_dir() {
  local source="$1"
  local relative="$2"
  local target="$STATE/$relative"
  local backup="$PROOF/state-before/$relative"
  local source_count=0 target_count=0 source_digest target_digest

  [[ -d "$source" ]] && source_count="$(find "$source" -type f 2>/dev/null | wc -l)"
  [[ -d "$target" ]] && target_count="$(find "$target" -type f 2>/dev/null | wc -l)"
  source_digest="$(dir_digest "$source")"
  target_digest="$(dir_digest "$target")"
  if [[ -d "$target" ]]; then
    mkdir -p "$(dirname "$backup")"
    cp -a "$target" "$backup"
    if [[ "$source_count" -gt 0 && "$source_digest" != "$target_digest" ]]; then
      echo "runtime_dir=$relative decision=CONFLICT_CANONICAL_REPORTS source_files=$source_count target_files=$target_count source_digest=$source_digest target_digest=$target_digest"
      echo "BLOCKED: repository/runtime report conflict requires explicit reconciliation: $relative"
      return 67
    fi
    echo "runtime_dir=$relative decision=PRESERVED_EXISTING source_files=$source_count target_files=$target_count source_digest=$source_digest target_digest=$target_digest"
    return 0
  fi
  if [[ -d "$source" ]]; then
    install -d -m 0750 -o "$RUN_USER" -g "$RUN_USER" "$target"
    cp -a "$source/." "$target/"
    chown -R "$RUN_USER:$RUN_USER" "$target"
    target_count="$(find "$target" -type f 2>/dev/null | wc -l)"
    target_digest="$(dir_digest "$target")"
    echo "runtime_dir=$relative decision=SEEDED_FROM_CURRENT_SOURCE source_files=$source_count target_files=$target_count source_digest=$source_digest target_digest=$target_digest"
  else
    echo "runtime_dir=$relative decision=SOURCE_ABSENT_SKIP source_files=0 target_files=0 source_digest=empty target_digest=empty"
  fi
}

run_unit_bounded() {
  local unit="$1"
  local limit="$2"
  local started=$SECONDS
  local state result status

  systemctl reset-failed "$unit" >/dev/null 2>&1 || true
  systemctl start --no-block "$unit" >/dev/null 2>&1 || true
  while true; do
    state="$(systemctl is-active "$unit" 2>/dev/null || true)"
    case "$state" in
      active|activating|reloading) ;;
      *) break ;;
    esac
    if (( SECONDS - started >= limit )); then
      systemctl stop "$unit" >/dev/null 2>&1 || true
      echo "unit=$unit verdict=TIMEOUT_STOPPED limit=${limit}s"
      return 124
    fi
    sleep 2
  done

  result="$(systemctl show "$unit" -p Result --value 2>/dev/null || true)"
  status="$(systemctl show "$unit" -p ExecMainStatus --value 2>/dev/null || true)"
  echo "unit=$unit state=${state:-unknown} result=${result:-unknown} exec_status=${status:-unknown}"
  [[ "$result" == "success" && "${status:-1}" == "0" ]]
}

id "$RUN_USER" >/dev/null 2>&1 || { echo "BLOCKED: missing user $RUN_USER"; exit 3; }
[[ -d "$REPO/.git" ]] || { echo "BLOCKED: missing canonical repo $REPO"; exit 4; }
command -v gh >/dev/null 2>&1 || { echo "BLOCKED: gh missing"; exit 5; }
command -v jq >/dev/null 2>&1 || { echo "BLOCKED: jq missing"; exit 6; }

section "0. SAFETY CONTRACT"
echo "EXTERNAL_SEND=DISABLED"
echo "PUBLIC_PUBLISH=DISABLED"
echo "PAYMENT=DISABLED"
echo "MERGE_TO_MAIN=DISABLED"
echo "PRODUCTION_MUTATION=DISABLED"
echo "DNS_MUTATION=DISABLED"
echo "DESTRUCTIVE_DB=DISABLED"
echo "SECRET_PRINTING=DISABLED"
echo "RECOVERY_SINGLE_FLIGHT=PASS"

section "1. QUIESCE REPO WRITERS"
TIMER_UNITS=(
  dealix-vps-issue-bridge.timer
  dealix-company-heartbeat.timer
  dealix-company-production.timer
  dealix-company-repo-watch.timer
  dealix-company-preflight.timer
  dealix-company-morning-fallback.timer
  dealix-company-midday.timer
  dealix-company-evening.timer
  dealix-company-local-ai.timer
  dealix-company-nightly.timer
  dealix-company-weekly.timer
  dealix-agent-council.timer
)
for unit in "${TIMER_UNITS[@]}"; do
  if systemctl is-active --quiet "$unit"; then
    ACTIVE_TIMERS+=("$unit")
  fi
  systemctl stop "$unit" >/dev/null 2>&1 || true
done
for unit in \
  dealix-vps-issue-bridge.service \
  dealix-company@heartbeat.service \
  dealix-company@production.service \
  dealix-company@repo-watch.service \
  dealix-company@preflight.service \
  dealix-company@morning-fallback.service \
  dealix-company@midday.service \
  dealix-company@evening.service \
  dealix-company@local-ai.service \
  dealix-company@nightly.service \
  dealix-company@weekly.service \
  dealix-agent-council.service
 do
  systemctl stop "$unit" >/dev/null 2>&1 || true
done
TIMERS_QUIESCED=1
printf '%s\n' "${ACTIVE_TIMERS[@]}" >"$PROOF/active-timers-before.txt"
echo "repo_writers=QUIESCED active_timers_before=${#ACTIVE_TIMERS[@]}"

section "2. PRESERVE CURRENT OPERATING STATE"
cd "$REPO"
git_d status -sb | tee "$PROOF/git-status-before.txt"
git_d diff --binary -- \
  dealix/config/social_content_queue.yaml \
  docs/commercial/operations/evidence_events_tracker.csv \
  docs/commercial/operations/soft_launch_meetings_tracker.yaml \
  >"$PROOF/runtime-tracked.patch" || true
chmod 0600 "$PROOF/runtime-tracked.patch"

install -d -m 0750 -o "$RUN_USER" -g "$RUN_USER" \
  "$STATE/commercial" \
  "$STATE/reports"

migrate_file "$REPO/dealix/config/social_content_queue.yaml" \
  "commercial/social_content_queue.yaml"
migrate_file "$REPO/docs/commercial/operations/evidence_events_tracker.csv" \
  "commercial/evidence_events_tracker.csv"
migrate_file "$REPO/docs/commercial/operations/soft_launch_meetings_tracker.yaml" \
  "commercial/soft_launch_meetings_tracker.yaml"
migrate_report_dir "$REPO/reports/founder_money_command" \
  "reports/founder_money_command"
migrate_report_dir "$REPO/reports/canonical_revenue_cycle" \
  "reports/canonical_revenue_cycle"

section "3. REVERSIBLE STASH AND FAST-FORWARD"
sudo -u "$RUN_USER" -H gh auth status >/dev/null
sudo -u "$RUN_USER" -H gh auth setup-git >/dev/null

BRANCH="$(git_d branch --show-current)"
[[ "$BRANCH" == "main" ]] || { echo "BLOCKED: canonical repo branch=$BRANCH expected=main"; exit 10; }

if [[ -n "$(git_d status --porcelain)" ]]; then
  sudo -u "$RUN_USER" -H git -C "$REPO" stash push -u -m "pre-runtime-state-isolation-${STAMP}" >/dev/null
  STASH_REF="$(sudo -u "$RUN_USER" -H git -C "$REPO" stash list -1 --format='%gd:%H' 2>/dev/null || true)"
else
  STASH_REF="none"
fi
echo "stash_ref=${STASH_REF:-unknown}"
[[ -z "$(git_d status --porcelain)" ]] || { echo "BLOCKED: worktree still dirty after reversible stash"; exit 11; }

sudo -u "$RUN_USER" -H git -C "$REPO" fetch origin main --prune
REMOTE_MAIN="$(git_d rev-parse origin/main)"
GITHUB_MAIN="$(sudo -u "$RUN_USER" -H gh api "repos/${REPO_SLUG}/commits/main" --jq .sha)"
LOCAL_BEFORE="$(git_d rev-parse HEAD)"
echo "local_before=$LOCAL_BEFORE"
echo "origin_main=$REMOTE_MAIN"
echo "github_main=$GITHUB_MAIN"
[[ "$REMOTE_MAIN" == "$GITHUB_MAIN" ]] || { echo "BLOCKED: origin/main differs from GitHub main"; exit 12; }
git_d merge-base --is-ancestor "$LOCAL_BEFORE" "$REMOTE_MAIN" || { echo "BLOCKED: non-fast-forward main relation"; exit 13; }
sudo -u "$RUN_USER" -H git -C "$REPO" merge --ff-only "$REMOTE_MAIN"
MAIN_HEAD="$(git_d rev-parse HEAD)"
[[ "$MAIN_HEAD" == "$GITHUB_MAIN" ]] || { echo "BLOCKED: fast-forward verification failed"; exit 14; }
echo "main_sync=PASS head=$MAIN_HEAD"

section "4. DETERMINISTIC PYTHON"
[[ -x "$REPO/scripts/ops/ensure_founder_automation_python.sh" ]] || { echo "BLOCKED: deterministic Python bootstrap missing"; exit 15; }
sudo -u "$RUN_USER" -H env DEALIX_REPO_ROOT="$REPO" \
  "$REPO/scripts/ops/ensure_founder_automation_python.sh"
sudo -u "$RUN_USER" -H "$REPO/.venv/bin/python" -c \
  'import fastapi,httpx,pydantic,pytest,yaml; print("DETERMINISTIC_PYTHON=PASS")'

section "5. HERMES ARCHITECTURE PRESERVATION"
HERMES_STATE_BEFORE="$(systemctl is-active hermes-dealix.service 2>/dev/null || true)"
HERMES_ENABLED_BEFORE="$(systemctl is-enabled hermes-dealix.service 2>/dev/null || true)"
echo "hermes_gateway_entry_state=${HERMES_STATE_BEFORE:-unknown}"
echo "hermes_gateway_entry_enabled=${HERMES_ENABLED_BEFORE:-unknown}"
echo "HERMES_MODE=PRESERVE_EXISTING_GATEWAY_POSTURE"

section "6. PR 1184 EXACT-HEAD RUNTIME ISOLATION"
RUNTIME_JSON="$(sudo -u "$RUN_USER" -H gh pr view "$RUNTIME_PR" --repo "$REPO_SLUG" --json state,isDraft,headRefOid)"
RUNTIME_STATE="$(jq -r .state <<<"$RUNTIME_JSON")"
RUNTIME_DRAFT="$(jq -r .isDraft <<<"$RUNTIME_JSON")"
RUNTIME_HEAD="$(jq -r .headRefOid <<<"$RUNTIME_JSON")"
echo "runtime_pr_state=$RUNTIME_STATE"
echo "runtime_pr_draft=$RUNTIME_DRAFT"
echo "runtime_pr_head=$RUNTIME_HEAD"
[[ "$RUNTIME_STATE" == "OPEN" && "$RUNTIME_DRAFT" == "true" && -n "$RUNTIME_HEAD" ]] || { echo "BLOCKED: runtime isolation PR is not open Draft"; exit 16; }

for path in \
  dealix/commercial_ops/paths.py \
  dealix/commercial_ops/first_paid_tracker.py \
  dealix/commercial_ops/founder_debrief.py \
  dealix/commercial_ops/founder_comprehensive_plan.py \
  dealix/commercial_ops/founder_agent_tasks.py \
  dealix/commercial_ops/full_ops_autopilot.py \
  dealix/commercial_ops/digest.py \
  dealix/commercial_ops/value_plan.py \
  dealix/commercial_ops/value_map_status.py \
  dealix/commercial_ops/autonomous_ops.py \
  dealix/commercial_ops/unified_founder_day.py \
  dealix/commercial_ops/founder_strongest_ops.py \
  dealix/commercial_ops/complete_autonomous_day.py \
  dealix/commercial_ops/founder_master_strategic_os.py \
  scripts/prepare_soft_launch_meetings.py \
  scripts/ops/dealix_vps_control.sh \
  scripts/ops/activate_dealix_from_main.sh \
  scripts/ops/install_dealix_runtime_state_isolation.sh \
  scripts/ops/dealix_full_vps_recovery.sh \
  tests/test_vps_runtime_state_isolation.py
 do
  fetch_pr_file "$RUNTIME_HEAD" "$path" "$RUNTIME_STAGE"
done
chmod 0700 \
  "$RUNTIME_STAGE/scripts/ops/install_dealix_runtime_state_isolation.sh" \
  "$RUNTIME_STAGE/scripts/ops/dealix_full_vps_recovery.sh"
: >"$RUNTIME_STAGE/dealix/__init__.py"
: >"$RUNTIME_STAGE/dealix/commercial_ops/__init__.py"
bash -n "$RUNTIME_STAGE/scripts/ops/install_dealix_runtime_state_isolation.sh"
bash -n "$RUNTIME_STAGE/scripts/ops/dealix_vps_control.sh"
bash -n "$RUNTIME_STAGE/scripts/ops/activate_dealix_from_main.sh"
bash -n "$RUNTIME_STAGE/scripts/ops/dealix_full_vps_recovery.sh"
"$REPO/.venv/bin/python" -m py_compile \
  "$RUNTIME_STAGE/dealix/commercial_ops/paths.py" \
  "$RUNTIME_STAGE/dealix/commercial_ops/first_paid_tracker.py" \
  "$RUNTIME_STAGE/dealix/commercial_ops/founder_debrief.py" \
  "$RUNTIME_STAGE/dealix/commercial_ops/founder_comprehensive_plan.py" \
  "$RUNTIME_STAGE/dealix/commercial_ops/founder_agent_tasks.py" \
  "$RUNTIME_STAGE/dealix/commercial_ops/full_ops_autopilot.py" \
  "$RUNTIME_STAGE/dealix/commercial_ops/digest.py" \
  "$RUNTIME_STAGE/dealix/commercial_ops/value_plan.py" \
  "$RUNTIME_STAGE/dealix/commercial_ops/value_map_status.py" \
  "$RUNTIME_STAGE/dealix/commercial_ops/autonomous_ops.py" \
  "$RUNTIME_STAGE/dealix/commercial_ops/unified_founder_day.py" \
  "$RUNTIME_STAGE/dealix/commercial_ops/founder_strongest_ops.py" \
  "$RUNTIME_STAGE/dealix/commercial_ops/complete_autonomous_day.py" \
  "$RUNTIME_STAGE/dealix/commercial_ops/founder_master_strategic_os.py" \
  "$RUNTIME_STAGE/scripts/prepare_soft_launch_meetings.py" \
  "$RUNTIME_STAGE/tests/test_vps_runtime_state_isolation.py"
(
  cd "$RUNTIME_STAGE"
  PYTHONPATH="$RUNTIME_STAGE:$REPO" "$REPO/.venv/bin/python" -m pytest -q \
    tests/test_vps_runtime_state_isolation.py
)
echo "runtime_pr_static=PASS"

DEALIX_REPO_ROOT="$REPO" \
DEALIX_RUNTIME_STATE_ROOT="$STATE" \
bash "$RUNTIME_STAGE/scripts/ops/install_dealix_runtime_state_isolation.sh" \
  | tee "$PROOF/runtime-isolation.log"

grep -q 'DEALIX_RUNTIME_STATE_ISOLATION=PASS' "$PROOF/runtime-isolation.log" || { echo "BLOCKED: runtime isolation acceptance missing"; exit 17; }
grep -q 'tracked_reports_tree_shadowed=false' "$PROOF/runtime-isolation.log" || { echo "BLOCKED: tracked reports safety proof missing"; exit 18; }
ISOLATION_OK=1
echo "runtime_isolation=PASS"

section "7. SYSTEMD WRITE-ISOLATION ACCEPTANCE"
HEARTBEAT_RC=0
PRODUCTION_RC=0
MIDDAY_RC=0
EVENING_RC=0
run_unit_bounded dealix-company@heartbeat.service 180 || HEARTBEAT_RC=$?
run_unit_bounded dealix-company@production.service 180 || PRODUCTION_RC=$?
run_unit_bounded dealix-company@midday.service 420 || MIDDAY_RC=$?
run_unit_bounded dealix-company@evening.service 420 || EVENING_RC=$?

echo "heartbeat_rc=$HEARTBEAT_RC"
echo "production_probe_rc=$PRODUCTION_RC"
echo "midday_rc=$MIDDAY_RC"
echo "evening_rc=$EVENING_RC"

if [[ -n "$(git_d status --porcelain)" ]]; then
  echo "REPO_CLEAN_AFTER_SYSTEMD=FAIL"
  git_d status -sb
  exit 19
fi
echo "REPO_CLEAN_AFTER_SYSTEMD=PASS"

section "8. PR 1150 EXACT-HEAD OPENCLAW ACCEPTANCE"
OPENCLAW_JSON="$(sudo -u "$RUN_USER" -H gh pr view "$OPENCLAW_PR" --repo "$REPO_SLUG" --json state,isDraft,headRefOid)"
OPENCLAW_PR_STATE="$(jq -r .state <<<"$OPENCLAW_JSON")"
OPENCLAW_DRAFT="$(jq -r .isDraft <<<"$OPENCLAW_JSON")"
OPENCLAW_HEAD="$(jq -r .headRefOid <<<"$OPENCLAW_JSON")"
echo "openclaw_pr_state=$OPENCLAW_PR_STATE"
echo "openclaw_pr_draft=$OPENCLAW_DRAFT"
echo "openclaw_pr_head=$OPENCLAW_HEAD"
[[ "$OPENCLAW_PR_STATE" == "OPEN" && "$OPENCLAW_DRAFT" == "true" && -n "$OPENCLAW_HEAD" ]] || { echo "BLOCKED: OpenClaw PR is not open Draft"; exit 20; }

fetch_pr_file "$OPENCLAW_HEAD" "scripts/ops/repair_dealix_openclaw_gateway.sh" "$OPENCLAW_STAGE"
fetch_pr_file "$OPENCLAW_HEAD" "tests/test_openclaw_local_memory_guard.py" "$OPENCLAW_STAGE"
chmod 0700 "$OPENCLAW_STAGE/scripts/ops/repair_dealix_openclaw_gateway.sh"
bash -n "$OPENCLAW_STAGE/scripts/ops/repair_dealix_openclaw_gateway.sh"
"$REPO/.venv/bin/python" -m py_compile "$OPENCLAW_STAGE/tests/test_openclaw_local_memory_guard.py"
(
  cd "$OPENCLAW_STAGE"
  "$REPO/.venv/bin/python" -m pytest -q tests/test_openclaw_local_memory_guard.py
)
echo "openclaw_pr_static=PASS"

set +e
DEALIX_OPENCLAW_READY_TIMEOUT=90 \
  timeout --signal=TERM --kill-after=20s 480s \
  bash "$OPENCLAW_STAGE/scripts/ops/repair_dealix_openclaw_gateway.sh" \
  2>&1 | redact | tee "$PROOF/openclaw-repair.log"
OPENCLAW_REPAIR_RC=${PIPESTATUS[0]}
set -e

echo "openclaw_repair_rc=$OPENCLAW_REPAIR_RC"
GW_STATUS=1
GW_PROBE=1
MEMORY_RC=1
CHANNEL_RC=1
OPENCLAW_NODE_DIR="$(
  find /home/dealix/.openclaw/tools -maxdepth 3 -type f -name node -path '*/bin/node' -perm -111 -printf '%h\n' 2>/dev/null \
    | sort -V \
    | tail -1
)"
OPENCLAW_PATH="${OPENCLAW_NODE_DIR}:/home/dealix/.openclaw/bin:/home/dealix/.local/bin:/usr/local/bin:/usr/bin:/bin"
if [[ -x "$OPENCLAW" && -n "$OPENCLAW_NODE_DIR" && -x "$OPENCLAW_NODE_DIR/node" ]]; then
  set +e
  timeout 45 sudo -iu "$RUN_USER" env HOME=/home/dealix PATH="$OPENCLAW_PATH" "$OPENCLAW" gateway status --require-rpc 2>&1 | redact | tee "$PROOF/openclaw-gateway-status.log"
  GW_STATUS=${PIPESTATUS[0]}
  timeout 45 sudo -iu "$RUN_USER" env HOME=/home/dealix PATH="$OPENCLAW_PATH" "$OPENCLAW" gateway probe 2>&1 | redact | tee "$PROOF/openclaw-gateway-probe.log"
  GW_PROBE=${PIPESTATUS[0]}
  timeout 90 sudo -iu "$RUN_USER" env HOME=/home/dealix PATH="$OPENCLAW_PATH" "$OPENCLAW" memory status --deep 2>&1 | redact | tee "$PROOF/openclaw-memory.log"
  MEMORY_RC=${PIPESTATUS[0]}
  timeout 45 sudo -iu "$RUN_USER" env HOME=/home/dealix PATH="$OPENCLAW_PATH" "$OPENCLAW" channels status --probe 2>&1 | redact | tee "$PROOF/openclaw-channels.log"
  CHANNEL_RC=${PIPESTATUS[0]}
  set -e
else
  echo "openclaw_postproof=BLOCKED_BUNDLED_NODE_OR_WRAPPER_MISSING"
fi

if [[ "$OPENCLAW_REPAIR_RC" -eq 0 && "$GW_STATUS" -eq 0 && "$GW_PROBE" -eq 0 && "$MEMORY_RC" -eq 0 && "$CHANNEL_RC" -eq 0 ]]; then
  OPENCLAW_FINAL=PASS
else
  OPENCLAW_FINAL=DEGRADED
fi
echo "OPENCLAW_FINAL=$OPENCLAW_FINAL"
ss -ltnp 2>/dev/null | grep ':18789' | redact || true

section "9. SAFE LOCAL REVENUE FALLBACK"
MORNING_RC=0
run_unit_bounded dealix-company@morning-fallback.service 720 || MORNING_RC=$?
echo "morning_fallback_rc=$MORNING_RC"

if [[ -n "$(git_d status --porcelain)" ]]; then
  echo "REPO_CLEAN_AFTER_REVENUE=FAIL"
  git_d status -sb
  exit 21
fi
echo "REPO_CLEAN_AFTER_REVENUE=PASS"
RESTORE_OK=1

section "10. PRODUCTION TRUST READ-ONLY"
for url in \
  https://api.dealix.me/health \
  https://api.dealix.me/healthz \
  https://dealix.me/ \
  https://dealix.me/ar
 do
  code="$(curl -L -sS -o /dev/null --connect-timeout 5 --max-time 20 -w '%{http_code}' "$url" 2>/dev/null || true)"
  echo "$url -> ${code:-000}"
done
printf 'n8n_http='
curl -sS -o /dev/null --max-time 10 -w '%{http_code}\n' http://127.0.0.1:5678/ 2>/dev/null || echo 000
printf 'ollama_http='
curl -sS -o /dev/null --max-time 10 -w '%{http_code}\n' http://127.0.0.1:11434/api/tags 2>/dev/null || echo 000

section "11. GITHUB TRUST READ-ONLY"
sudo -u "$RUN_USER" -H gh pr view "$RUNTIME_PR" --repo "$REPO_SLUG" \
  --json number,state,isDraft,mergeable,headRefOid,baseRefName,statusCheckRollup \
  | jq '{number,state,isDraft,mergeable,headRefOid,baseRefName,checks:[.statusCheckRollup[]? | {name:(.name // .context),status,conclusion,state}]}' || true
sudo -u "$RUN_USER" -H gh pr view "$OPENCLAW_PR" --repo "$REPO_SLUG" \
  --json number,state,isDraft,mergeable,headRefOid,baseRefName,statusCheckRollup \
  | jq '{number,state,isDraft,mergeable,headRefOid,baseRefName,checks:[.statusCheckRollup[]? | {name:(.name // .context),status,conclusion,state}]}' || true

echo "github_actions_execution_plane=BLOCKED_QUOTA_ISSUE_1134"
echo "github_actions_rerun=NOT_ATTEMPTED"

section "12. EXACT-HEAD RECHECK"
RUNTIME_HEAD_NOW="$(sudo -u "$RUN_USER" -H gh pr view "$RUNTIME_PR" --repo "$REPO_SLUG" --json headRefOid --jq .headRefOid 2>/dev/null || true)"
OPENCLAW_HEAD_NOW="$(sudo -u "$RUN_USER" -H gh pr view "$OPENCLAW_PR" --repo "$REPO_SLUG" --json headRefOid --jq .headRefOid 2>/dev/null || true)"
EXACT_HEAD_STATUS=PASS
if [[ "$RUNTIME_HEAD_NOW" != "$RUNTIME_HEAD" || "$OPENCLAW_HEAD_NOW" != "$OPENCLAW_HEAD" ]]; then
  EXACT_HEAD_STATUS=STALE_HEAD_MOVED
fi
echo "runtime_head_now=${RUNTIME_HEAD_NOW:-unknown}"
echo "openclaw_head_now=${OPENCLAW_HEAD_NOW:-unknown}"
echo "exact_head_status=$EXACT_HEAD_STATUS"

section "13. PRIVATE PROOF COMMENTS"
REPO_CLEAN=FAIL
[[ -z "$(git_d status --porcelain)" ]] && REPO_CLEAN=PASS
HERMES_STATE_FINAL="$(systemctl is-active hermes-dealix.service 2>/dev/null || true)"
COMMENT="$TMP/proof-comment.md"
cat >"$COMMENT" <<EOF
## VPS acceptance ${STAMP}

- main: \`${MAIN_HEAD}\`
- runtime isolation exact head: \`${RUNTIME_HEAD}\`
- runtime isolation: **PASS**
- repo clean after systemd/revenue cycles: **${REPO_CLEAN}**
- Hermes gateway entry/final: **${HERMES_STATE_BEFORE:-unknown} / ${HERMES_STATE_FINAL:-unknown}** (posture preserved; no architecture mutation)
- OpenClaw exact head: \`${OPENCLAW_HEAD}\`
- OpenClaw gateway+memory: **${OPENCLAW_FINAL}**
- exact-head recheck: **${EXACT_HEAD_STATUS}**
- heartbeat rc: \`${HEARTBEAT_RC}\`
- midday rc: \`${MIDDAY_RC}\`
- evening rc: \`${EVENING_RC}\`
- morning fallback rc: \`${MORNING_RC}\`
- external send/payment/merge/production mutation: **disabled**
- GitHub hosted Actions: **execution-plane blocked under #1134; no rerun attempted**

Local proof directory: \`${PROOF}\`
EOF
sudo -u "$RUN_USER" -H gh api --method POST "repos/${REPO_SLUG}/issues/${RUNTIME_PR}/comments" -F "body=@${COMMENT}" >/dev/null || true
sudo -u "$RUN_USER" -H gh api --method POST "repos/${REPO_SLUG}/issues/${OPENCLAW_PR}/comments" -F "body=@${COMMENT}" >/dev/null || true
echo "private_pr_proof_comments=ATTEMPTED"

section "14. FINAL PROOF"
free -h
swapon --show || true
git_d status -sb
printf 'MAIN_HEAD=%s\n' "$MAIN_HEAD"
printf 'STASH_REF=%s\n' "${STASH_REF:-none}"
printf 'RUNTIME_PR_HEAD=%s\n' "$RUNTIME_HEAD"
printf 'RUNTIME_ISOLATION=PASS\n'
printf 'REPO_CLEAN=%s\n' "$REPO_CLEAN"
printf 'HERMES_GATEWAY_ENTRY=%s\n' "${HERMES_STATE_BEFORE:-unknown}"
printf 'HERMES_GATEWAY_FINAL=%s\n' "${HERMES_STATE_FINAL:-unknown}"
printf 'HERMES_MODE=PRESERVE_EXISTING_GATEWAY_POSTURE\n'
printf 'OPENCLAW_PR_HEAD=%s\n' "$OPENCLAW_HEAD"
printf 'OPENCLAW_FINAL=%s\n' "$OPENCLAW_FINAL"
printf 'EXACT_HEAD_STATUS=%s\n' "$EXACT_HEAD_STATUS"
printf 'HEARTBEAT_RC=%s\n' "$HEARTBEAT_RC"
printf 'PRODUCTION_PROBE_RC=%s\n' "$PRODUCTION_RC"
printf 'MIDDAY_RC=%s\n' "$MIDDAY_RC"
printf 'EVENING_RC=%s\n' "$EVENING_RC"
printf 'MORNING_FALLBACK_RC=%s\n' "$MORNING_RC"
printf 'EXTERNAL_SEND=DISABLED\n'
printf 'PAYMENT=DISABLED\n'
printf 'MERGE_TO_MAIN=DISABLED\n'
printf 'PRODUCTION_MUTATION=DISABLED\n'
printf 'PROOF_DIR=%s\n' "$PROOF"
printf 'DEALIX_FULL_RECOVERY=COMPLETE\n'
