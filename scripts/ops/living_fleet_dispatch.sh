#!/usr/bin/env bash
# =============================================================================
# Dealix Living Fleet Dispatcher v2 — truthful lifecycle foundation.
#
# Lifecycle truth:
#   QUEUED → HANDOFF_PENDING → RUNNING → SUCCEEDED|FAILED|DEGRADED|TIMEOUT
#   WAITING_EXTERNAL / WAITING_APPROVAL are owner-declared states, never set
#   by this router on enqueue.
#
#   A job is NOT successful because it was queued. Only a VALID OWNER
#   COMPLETION RECEIPT advances LAST_SUCCESS_AT / useful_count / LAST_PROOF.
#
# Safety (pinned by tests/test_living_fleet_guards.py):
#   - No L5 verbs: never send/publish/merge/deploy/mutate DNS/DB/pay/rotate.
#   - Runtime state OUTSIDE the git checkout.
#   - SKIP_UNCHANGED fingerprints; atomic JSON writes; per-role flock.
#   - Routing derived from ONE source: the registry events field.
#     Unknown event = honest no-op. Unknown seat = DEGRADED evidence.
#   - Owner commands come from a strict allowlist of VERIFIED-EXISTING
#     canonical scripts. No event-controlled shell interpolation. Ever.
# =============================================================================
set -Eeuo pipefail

EVENT="${1:-heartbeat}"
MODE="${2:-dispatch}" # dispatch | collect
case "$MODE" in dispatch|collect) ;; *) log "BLOCKED unknown mode=${MODE}"; exit 2 ;; esac
REPO_ROOT="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
FLEET_STATE_DIR="${DEALIX_FLEET_STATE_DIR:-/opt/dealix/control/state/living_fleet}"
FOUNDER_PERSONAL_STATE_DIR="${DEALIX_FOUNDER_PERSONAL_STATE_DIR:-/opt/dealix/control/state/founder_personal}"
MIN_MEM_MB="${DEALIX_FLEET_MIN_MEM_MB:-3500}"
STAMP="$(date -Is)"
DAY="$(date +%F)"
mkdir -p "$FLEET_STATE_DIR"
install -d -m 700 "$FOUNDER_PERSONAL_STATE_DIR" 2>/dev/null \
  || { mkdir -p "$FOUNDER_PERSONAL_STATE_DIR" && chmod 700 "$FOUNDER_PERSONAL_STATE_DIR"; }

log() { printf '[%s] [fleet:%s] %s\n' "$(date -Is)" "$EVENT" "$*"; }

mem_available_mb() { awk '/MemAvailable:/ {print int($2/1024)}' /proc/meminfo; }

latest_artifact() {
  local pattern="$1" best="" best_ts=0 f ts
  for f in $REPO_ROOT/$pattern; do
    [[ -f "$f" ]] || continue
    ts="$(stat -c %Y "$f" 2>/dev/null || echo 0)"
    (( ts > best_ts )) && { best_ts=$ts; best="$f"; }
  done
  echo "$best"
}

resolve_watch() {
  local tok="$1"
  case "$tok" in
    latest:*)          latest_artifact "${tok#latest:}" ;;
    git:*)             git -C "$REPO_ROOT" rev-parse HEAD 2>/dev/null || echo "missing:${tok}" ;;
    file:*|dir:*)      echo "$REPO_ROOT/${tok#*:}" ;;
    rtfile:*|rtdir:*)  echo "${tok#*:}" ;;
    /*)                echo "$tok" ;;
    *)                 echo "$REPO_ROOT/$tok" ;;
  esac
}

fp_of() {
  local role="$1"; shift
  {
    echo "$role"
    local p
    for tok in "$@"; do
      if [[ "$tok" == git:* ]]; then
        printf 'git=%s\n' "$(git -C "$REPO_ROOT" rev-parse HEAD 2>/dev/null || echo unknown)"
        continue
      fi
      p="$(resolve_watch "$tok")"
      if [[ -z "$p" ]]; then echo "missing:${tok}"
      elif [[ -d "$p" ]]; then
        find "$p" -maxdepth 1 -type f -printf '%f %s %T@\n' 2>/dev/null | sort
      else
        stat -c '%n %s %Y' "$p" 2>/dev/null || echo "missing:${tok}"
      fi
    done
  } | sha256sum | cut -c1-16
}

atomic_json_set() {
  python3 - "$@" <<'PY'
import json, os, sys
path, rest = sys.argv[1], sys.argv[2:]
try:
    with open(path) as fh: d = json.load(fh)
except Exception:
    d = {}
for kv in rest:
    k, _, v = kv.partition("=")
    d[k] = v
tmp = f"{path}.tmp.{os.getpid()}"
with open(tmp, "w") as fh:
    json.dump(d, fh, ensure_ascii=False, indent=1)
    fh.flush()
    os.fsync(fh.fileno())
os.replace(tmp, path)
PY
}
json_get() { python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));print(d.get(sys.argv[2],""))' "$1" "$2" 2>/dev/null || true; }

atomic_cat_json() {
  python3 - "$1" "$2" <<'PY'
import json, os, sys
path, payload = sys.argv[1], json.loads(sys.argv[2])
tmp = f"{path}.tmp.{os.getpid()}"
with open(tmp, "w") as fh:
    json.dump(payload, fh, ensure_ascii=False, indent=1)
    fh.flush(); os.fsync(fh.fileno())
os.replace(tmp, path)
PY
}

bump() {
  local f="$1" cur=0
  case "$(cat "$f" 2>/dev/null)" in ''|*[!0-9]*) cur=0 ;; *) cur="$(cat "$f")" ;; esac
  mkdir -p "$(dirname "$f")"
  printf '%s\n' "$((cur + 1))" >"$f"
}

counter_value() {
  local f="$1" value
  value="$(cat "$f" 2>/dev/null || true)"
  case "$value" in ''|*[!0-9]*) echo 0 ;; *) echo "$value" ;; esac
}

atomic_write_number() {
  python3 - "$1" "$2" <<'PY'
import os, sys
path, value = sys.argv[1], sys.argv[2]
os.makedirs(os.path.dirname(path), exist_ok=True)
tmp = f"{path}.tmp.{os.getpid()}"
with open(tmp, "w") as fh:
    fh.write(value + "\n")
    fh.flush()
    os.fsync(fh.fileno())
os.replace(tmp, path)
PY
}

# Idempotent counter decision. The durable marker is prepared before the
# counter update. A per-counter transaction state records the applied marker
# atomically before the compatibility plain-number counter is synchronized.
# Recovery can therefore distinguish "not applied" from "already applied"
# even after another job advances the same role counter before this job's
# pending-file move.
counter_once() {
  local counter="$1" marker="$2" before after current state_file marker_counter
  mkdir -p "$(dirname "$counter")" "$(dirname "$marker")"
  if [[ -f "$marker" ]]; then
    marker_counter="$(json_get "$marker" COUNTER_FILE)"
    before="$(json_get "$marker" COUNTER_BEFORE)"
    after="$(json_get "$marker" COUNTER_AFTER)"
    [[ "$marker_counter" == "$counter" ]] || {
      log "TERMINAL_MARKER_COUNTER_MISMATCH marker=$marker expected=$counter actual=$marker_counter"
      return 1
    }
    [[ "$before" =~ ^[0-9]+$ && "$after" =~ ^[0-9]+$ && "$after" == "$((before + 1))" ]] || {
      log "TERMINAL_MARKER_INVALID marker=$marker"
      return 1
    }
  else
    before="$(counter_value "$counter")"
    after="$((before + 1))"
    atomic_cat_json "$marker" "{\"COUNTER_FILE\":\"$counter\",\"COUNTER_BEFORE\":$before,\"COUNTER_AFTER\":$after,\"STATE\":\"PREPARED\"}"
  fi
  state_file="${counter}.state.json"
  # The JSON state is the recovery authority. It is atomically replaced as a
  # single file, so a crash cannot leave an applied job indistinguishable from
  # a job whose counter increment never happened. The plain file remains for
  # existing readers and is repaired from this state on every invocation.
  local state_count
  state_count="$(python3 - "$state_file" "$counter" "$marker" <<'PY'
import glob
import json
import os
import sys

state_path, counter_path, marker_path = sys.argv[1:]

def number(path):
    try:
        value = open(path).read().strip()
    except OSError:
        return 0
    return int(value) if value.isdigit() else 0

def atomic_json(path, value):
    tmp = f"{path}.tmp.{os.getpid()}"
    with open(tmp, "w") as fh:
        json.dump(value, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)

marker_key = os.path.basename(marker_path)
try:
    state = json.load(open(state_path))
    count = state["COUNT"]
    applied = set(state["APPLIED_MARKERS"])
    if not isinstance(count, int) or count < 0 or not all(isinstance(x, str) for x in applied):
        raise ValueError("invalid counter state")
except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
    # One-time migration for pre-state PREPARED/COMMITTED markers. A duplicate
    # before/after pair is irreducibly ambiguous (one job may have been
    # applied while another was not), so fail closed instead of guessing.
    count = number(counter_path)
    applied = set()
    seen_ranges = {}
    for path in glob.glob(os.path.join(os.path.dirname(marker_path), "*.json")):
        try:
            item = json.load(open(path))
            if item.get("COUNTER_FILE") != counter_path:
                continue
            b = item.get("COUNTER_BEFORE")
            a = item.get("COUNTER_AFTER")
            if not isinstance(b, int) or not isinstance(a, int) or a != b + 1:
                continue
            key = (b, a)
            prior = seen_ranges.get(key)
            if prior is not None and prior != os.path.basename(path):
                print("TERMINAL_COUNTER_MIGRATION_AMBIGUOUS", file=sys.stderr)
                sys.exit(42)
            seen_ranges[key] = os.path.basename(path)
            if a <= count:
                applied.add(os.path.basename(path))
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
            continue

if marker_key not in applied:
    applied.add(marker_key)
    count += 1

os.makedirs(os.path.dirname(state_path), exist_ok=True)
atomic_json(state_path, {"COUNT": count, "APPLIED_MARKERS": sorted(applied), "VERSION": 1})
print(count)
PY
)" || {
    log "TERMINAL_COUNTER_DRIFT counter=$counter before=$before after=$after current=$(counter_value "$counter")"
    return 1
  }
  current="$(counter_value "$counter")"
  [[ "$current" =~ ^[0-9]+$ && "$state_count" =~ ^[0-9]+$ ]] || return 1
  atomic_write_number "$counter" "$state_count"
}

# ---- REGISTRY: single routing source of truth ------------------------------
# role|comma-event-list|kind|comma-watch-tokens|owner-cmd(NONE=handoff only)
# owner commands are VERIFIED-EXISTING canonical repo scripts, executed with
# the canonical .venv when required. No event data ever reaches the command.
REGISTRY=(
  "EXEC_PM|morning,midday,evening,strategic|det|rtfile:/opt/dealix/company-autopilot/logs/evening-latest.log|.venv/bin/python scripts/run_dealix_daily_ops.py --skip-api"
  "REVENUE_INTEL|gmail_reply,tender_change,morning,midday|llm|file:business/_data/outreach_review_queue.json,file:business/_data/proposals.index.json|.venv/bin/python scripts/commercial/run_commercial_intelligence_founder_cycle.py"
  "SALES_NEGOTIATION|gmail_reply|llm|file:business/_data/outreach_review_queue.json|.venv/bin/python scripts/commercial/run_negotiation_operator_day.py --dry-run --skip-api"
  "MARKET_INTEL|market_signal,tender_change|llm|latest:reports/founder/MARKET_SIGNALS_*.md|NONE"
  "LEAD_INTEL|morning|det|file:business/_data/proposals.index.json|NONE"
  "CUSTOMER_ACQ|opportunity_signal|llm|file:business/_data/outreach_review_queue.json|NONE"
  "DIAGNOSTIC|opportunity_signal|llm|latest:reports/founder/MINI_DIAGNOSTICS_DRAFT_*.md|NONE"
  "DELIVERY|evening,delivery_evidence|det|rtfile:/opt/dealix/company-autopilot/state/commercial/evidence_events_tracker.csv|NONE"
  "ENGINEERING|repo_watch,ci_failure|det|git:HEAD|NONE"
  "GOVERNANCE|nightly,approval_changed|det|file:docs/ops/APPROVAL_FINGERPRINT_CONTRACT.md|.venv/bin/python scripts/security_smoke.py"
  "DATA_BRAIN|nightly,strategic,proof_event|det|file:dealix/transformation/business_now_cache.yaml|.venv/bin/python scripts/export_service_readiness_json.py"
  "CONTENT|proof_event,evening|llm|latest:reports/founder/PROOF_LOG_*.md|NONE"
  "DAILY_BUILDER_RND|new_oss_candidate|llm|file:docs/ops/DAILY_BUILDER_CONTRACT.md|NONE"
  "CAREER_INTELLIGENCE|career_reply,personal_deadline|llm|rtfile:$FOUNDER_PERSONAL_STATE_DIR/career.index.json|NONE"
  "PRIVATE_FOUNDER_OPS|personal_deadline|det|rtfile:$FOUNDER_PERSONAL_STATE_DIR/admin.index.json|NONE"
)

roles_for_event() {
  local out=()
  for row in "${REGISTRY[@]}"; do
    IFS='|' read -r _r ev _k _w _o <<<"$row"
    IFS=',' read -r -a evs <<<"$ev"
    for e in "${evs[@]}"; do
      [[ "$e" == "$EVENT" ]] && out+=("$_r") && break
    done
  done
  [[ ${#out[@]} -eq 0 ]] && echo "" || echo "${out[*]}"
}

registry_row() {
  for row in "${REGISTRY[@]}"; do
    [[ "${row%%|*}" == "$1" ]] && { echo "$row"; return 0; }
  done
  return 1
}

run_owner() {
  local owner_cmd="$1" output_path="$2"
  local -a argv=()
  read -r -a argv <<<"$owner_cmd"

  # Registry owner commands are fixed repo-controlled argv, never event input.
  # Require the canonical interpreter token and a concrete script argument so
  # no arbitrary shell string, eval, or accidental word splitting can execute.
  [[ "${argv[0]:-}" == ".venv/bin/python" && "${argv[1]:-}" == scripts/*.py ]] || {
    log "BLOCKED invalid_owner_command"
    return 64
  }

  (
    cd "$REPO_ROOT"
    set +e
    timeout --kill-after=15 --signal=TERM 300 \
      ./.venv/bin/python "${argv[@]:1}" >"$output_path" 2>&1
    rc=$?
    set -e
    exit "$rc"
  )
}

# ---- COLLECT MODE: consume owner completion receipts -----------------------
# Collect and dispatch share the same per-role lock. This makes terminal state,
# counters and pending-file mutation serializable for a seat.
if [[ "$MODE" == "collect" ]]; then
  for jf in "$FLEET_STATE_DIR"/*/pending/*.json; do
    [[ -f "$jf" ]] || continue
    ROLE="$(json_get "$jf" ROLE)"
    [[ -n "$ROLE" ]] || continue
    JOB_ID="$(json_get "$jf" JOB_ID)"
    role_lock="$FLEET_STATE_DIR/${ROLE}.lock"
    exec 8>"$role_lock"
    if ! flock -n 8; then
      log "COLLECT_SKIP_LOCKED role=${ROLE} job=${JOB_ID}"
      exec 8>&-
      continue
    fi
    # Dispatch may have consumed/moved the job after glob expansion but before
    # collect acquired the lock; recheck under the shared lock.
    if [[ ! -f "$jf" ]]; then
      exec 8>&-
      continue
    fi
    rcpt="$FLEET_STATE_DIR/${ROLE}/receipts/${JOB_ID}.json"
    sf="$FLEET_STATE_DIR/${ROLE}.state.json"
    if [[ ! -f "$rcpt" ]]; then
      exec 8>&-
      continue
    fi
    RESULT="$(json_get "$rcpt" RESULT)"
    OWNER="$(json_get "$rcpt" OWNER)"
    USEFUL="$(json_get "$rcpt" USEFUL_OUTPUT)"
    case "$RESULT" in
      SUCCEEDED)
        terminal_marker="$FLEET_STATE_DIR/${ROLE}/terminal/${JOB_ID}.useful.json"
        if [[ "$USEFUL" == "true" ]]; then
          counter_once "$FLEET_STATE_DIR/${ROLE}.useful_count" "$terminal_marker" || {
            log "TERMINALIZATION_BLOCKED role=${ROLE} job=${JOB_ID}"
            exec 8>&-
            exit 1
          }
        fi
        atomic_json_set "$sf" "STATUS=SUCCEEDED" "LAST_SUCCESS_AT=$(date -Is)" \
          "LAST_PROOF=${rcpt}" "LAST_RESULT=SUCCEEDED" "OWNER=${OWNER}"
        [[ "$USEFUL" == "true" ]] && atomic_json_set "$terminal_marker" "STATE=COMMITTED" "TERMINAL_RESULT=SUCCEEDED"
        mkdir -p "$(dirname "$jf")/consumed"; mv "$jf" "$(dirname "$jf")/consumed/$(basename "$jf")"
        log "RECEIPT_OK role=${ROLE} job=${JOB_ID} result=SUCCEEDED"
        ;;
      FAILED|DEGRADED)
        terminal_marker="$FLEET_STATE_DIR/${ROLE}/terminal/${JOB_ID}.failure.json"
        counter_once "$FLEET_STATE_DIR/${ROLE}.failure_count" "$terminal_marker" || {
          log "TERMINALIZATION_BLOCKED role=${ROLE} job=${JOB_ID}"
          exec 8>&-
          exit 1
        }
        atomic_json_set "$sf" "STATUS=${RESULT}" "LAST_RESULT=${RESULT}" \
          "BLOCKER=$(json_get "$rcpt" BLOCKER)" "OWNER=${OWNER}"
        atomic_json_set "$terminal_marker" "STATE=COMMITTED" "TERMINAL_RESULT=${RESULT}"
        mkdir -p "$(dirname "$jf")/consumed"; mv "$jf" "$(dirname "$jf")/consumed/$(basename "$jf")"
        log "RECEIPT_FAIL role=${ROLE} job=${JOB_ID} result=${RESULT}"
        ;;
      TIMEOUT)
        terminal_marker="$FLEET_STATE_DIR/${ROLE}/terminal/${JOB_ID}.timeout.json"
        counter_once "$FLEET_STATE_DIR/${ROLE}.timeout_count" "$terminal_marker" || {
          log "TERMINALIZATION_BLOCKED role=${ROLE} job=${JOB_ID}"
          exec 8>&-
          exit 1
        }
        atomic_json_set "$sf" "STATUS=TIMEOUT" "LAST_RESULT=TIMEOUT" \
          "BLOCKER=$(json_get "$rcpt" BLOCKER)" "OWNER=${OWNER}"
        atomic_json_set "$terminal_marker" "STATE=COMMITTED" "TERMINAL_RESULT=TIMEOUT"
        mkdir -p "$(dirname "$jf")/consumed"; mv "$jf" "$(dirname "$jf")/consumed/$(basename "$jf")"
        log "RECEIPT_FAIL role=${ROLE} job=${JOB_ID} result=TIMEOUT"
        ;;
      *) log "RECEIPT_INVALID role=${ROLE} job=${JOB_ID} result=${RESULT}" ;;
    esac
    exec 8>&-
  done
  exit 0
fi

# ---- DISPATCH MODE ---------------------------------------------------------
# ---- CANARY: end-to-end internal proof that the fleet fabric is alive ----
if [[ "$EVENT" == "dealix_internal_canary" ]]; then
  CANARY_DIR="$FLEET_STATE_DIR/canary/$DAY"
  mkdir -p "$CANARY_DIR"
  CANARY_ID="canary-$(date +%s)-$$"
  log "CANARY_START id=${CANARY_ID}"
  api_code="$(curl -sS -o /dev/null -w '%{http_code}' --max-time 10 https://api.dealix.me/health 2>/dev/null || echo 000)"
  root_code="$(curl -sS -o /dev/null -w '%{http_code}' --max-time 10 https://dealix.me 2>/dev/null || echo 000)"
  ollama_ok="$(curl -sS -o /dev/null -w '%{http_code}' --max-time 5 http://127.0.0.1:11434/api/tags 2>/dev/null || echo 000)"
  state_readable=false
  for sf in "$FLEET_STATE_DIR"/*.state.json; do
    [[ -f "$sf" ]] || continue
    python3 -c 'import json,sys;json.load(open(sys.argv[1]))' "$sf" 2>/dev/null && { state_readable=true; break; }
  done
  stale_locks=0
  now=$(date +%s)
  for lf in "$FLEET_STATE_DIR"/*.lock; do
    [[ -f "$lf" ]] || continue
    fage=$(( now - $(stat -c %Y "$lf" 2>/dev/null || echo "$now") ))
    (( fage > 3600 )) && stale_locks=$(( stale_locks + 1 ))
  done
  cat >"${CANARY_DIR}/${CANARY_ID}.json" <<CEOF
{
  "canary_id": "${CANARY_ID}",
  "timestamp": "$(date -Is)",
  "api_health": "${api_code}",
  "root_health": "${root_code}",
  "ollama_responsive": ${ollama_ok},
  "fleet_state_readable": ${state_readable},
  "stale_locks": ${stale_locks},
  "result": "$([[ "$api_code" == "200" && "$root_code" == "200" && "$state_readable" == true ]] && echo PASS || echo FAIL)"
}
CEOF
  chmod 0640 "${CANARY_DIR}/${CANARY_ID}.json"
  RESULT="$([[ "$api_code" == "200" && "$root_code" == "200" ]] && echo PASS || echo FAIL)"
  log "CANARY_COMPLETE id=${CANARY_ID} result=${RESULT} api=${api_code} root=${root_code} ollama=${ollama_ok} state_readable=${state_readable} stale_locks=${stale_locks}"
  exit 0
fi
WANTED="$(roles_for_event)"
log "dispatch start event=${EVENT} wanted=[${WANTED:-none}] mem=$(mem_available_mb)MB"
if [[ -z "$WANTED" ]]; then
  log "NO_OP unknown-or-sensor event (honest no-op)"
  exit 0
fi

for role in $WANTED; do
  row="$(registry_row "$role")" || { log "DEGRADED unknown_seat=${role}"; continue; }
  IFS='|' read -r _r ev kind watches owner <<<"$row"
  IFS=',' read -r -a WATCHES <<<"$watches"

  sf="$FLEET_STATE_DIR/${role}.state.json"
  lock="$FLEET_STATE_DIR/${role}.lock"
  mkdir -p "$FLEET_STATE_DIR"

  exec 9>"$lock"
  if ! flock -n 9; then
    log "SKIP_LOCKED role=${role} (another dispatch holds the seat)"
    continue
  fi

  fp="$(fp_of "$role" "${WATCHES[@]}")"
  OWNER_SIGNATURE="$(printf '%s|%s|%s|%s' "$role" "$kind" "$watches" "$owner" | sha256sum | cut -c1-16)"
  EFFECTIVE_FINGERPRINT="$(printf '%s|%s' "$fp" "$OWNER_SIGNATURE" | sha256sum | cut -c1-16)"
  last_efp="$(json_get "$sf" EFFECTIVE_FINGERPRINT)"

  if [[ -n "$last_efp" && "$last_efp" == "$EFFECTIVE_FINGERPRINT" && "${DEALIX_FLEET_FORCE:-0}" != "1" ]]; then
    bump "$FLEET_STATE_DIR/${role}.skip_count"
    cur_status="$(json_get "$sf" STATUS)"
    cur_blocker="$(json_get "$sf" BLOCKER)"
    if [[ "$cur_status" == "BLOCKED" && -n "$cur_blocker" ]]; then
      atomic_json_set "$sf" "STATUS=BLOCKED" "BLOCKER=$cur_blocker" \
        "INPUT_FINGERPRINT=$fp" "OWNER_SIGNATURE=$OWNER_SIGNATURE" \
        "EFFECTIVE_FINGERPRINT=$EFFECTIVE_FINGERPRINT" "LAST_RESULT=SKIP_UNCHANGED_BLOCKED"
      log "SKIP_UNCHANGED_BLOCKED role=${role} blocker=${cur_blocker}"
    else
      atomic_json_set "$sf" "STATUS=IDLE_HEALTHY" "INPUT_FINGERPRINT=$fp" \
        "OWNER_SIGNATURE=$OWNER_SIGNATURE" "EFFECTIVE_FINGERPRINT=$EFFECTIVE_FINGERPRINT" \
        "LAST_RESULT=SKIP_UNCHANGED"
      log "SKIP_UNCHANGED role=${role} fp=${fp}"
    fi
    continue
  fi

  if [[ "$owner" == "NONE" ]]; then
    JOB_ID="JOB-${role}-$(date +%s)-$$"
    pending_dir="$FLEET_STATE_DIR/${role}/pending"
    mkdir -p "$pending_dir"
    atomic_json_set "$sf" "STATUS=BLOCKED" "BLOCKER=owner_missing" \
      "INPUT_FINGERPRINT=$fp" "OWNER_SIGNATURE=$OWNER_SIGNATURE" \
      "EFFECTIVE_FINGERPRINT=$EFFECTIVE_FINGERPRINT" "OWNER=NONE"
    atomic_cat_json "${pending_dir}/${JOB_ID}.json" '{"JOB_ID":"'"${JOB_ID}"'","ROLE":"'"${role}"'","EVENT":"'"${EVENT}"'","INPUT_FINGERPRINT":"'"${fp}"'","OWNER":"NONE","STARTED_AT":"'"$STAMP"'","STATUS":"HANDOFF_PENDING"}'
    bump "$FLEET_STATE_DIR/${role}.queued_count"
    log "HANDOFF_PENDING role=${role} job=${JOB_ID} blocker=owner_missing"
    continue
  fi

  if [[ "$kind" == "llm" ]] && (( $(mem_available_mb) < MIN_MEM_MB )); then
    log "RESOURCE_GUARD role=${role} available=$(mem_available_mb)MB min=${MIN_MEM_MB}MB"
    atomic_json_set "$sf" "STATUS=DEGRADED" "BLOCKER=memory_guard" "LAST_RESULT=SKIP_RESOURCE"
    continue
  fi

  JOB_ID="JOB-${role}-$(date +%s)-$$"
  pending_dir="$FLEET_STATE_DIR/${role}/pending"
  mkdir -p "$pending_dir"
  for old_jf in "$pending_dir"/*.json; do
    [[ -f "$old_jf" ]] || continue
    python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));sys.exit(0 if d.get("STATUS")=="HANDOFF_PENDING" else 1)' "$old_jf" 2>/dev/null || continue
    OLD_ID="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1])).get("JOB_ID",""))' "$old_jf" 2>/dev/null || true)"
    python3 - "$old_jf" "$JOB_ID" "$OWNER_SIGNATURE" <<'PY'
import json,sys
p=sys.argv[1]
try: d=json.load(open(p))
except Exception: sys.exit(0)
d["STATUS"]="SUPERSEDED_BY_OWNER_ACTIVATION"
d["SUPERSEDED_AT"]=__import__("datetime").datetime.now().isoformat()
d["NEW_OWNER_SIGNATURE"]=sys.argv[3]
d["NEW_JOB_ID"]=sys.argv[2]
json.dump(d,open(p,"w"),indent=1)
PY
    log "SUPERSEDED ownerless_handoff job=${OLD_ID} by=${JOB_ID}"
    mv "$old_jf" "${old_jf%.json}.superseded.json"
  done
  atomic_json_set "$sf" "STATUS=QUEUED" "CURRENT_JOB=${JOB_ID}" \
    "INPUT_FINGERPRINT=$fp" "OWNER_SIGNATURE=$OWNER_SIGNATURE" \
    "EFFECTIVE_FINGERPRINT=$EFFECTIVE_FINGERPRINT" "LAST_STARTED_AT=$STAMP" "OWNER=${owner}"
  atomic_json_set "$sf" "STATUS=RUNNING"
  out_dir="$FLEET_STATE_DIR/${role}/$DAY"
  mkdir -p "$out_dir"
  t0="$(date +%s)"
  set +e
  run_owner "$owner" "${out_dir}/owner_output.txt"
  rc=$?
  set -e
  duration=$(( $(date +%s) - t0 ))

  atomic_cat_json "${pending_dir}/${JOB_ID}.json" '{"JOB_ID":"'"${JOB_ID}"'","ROLE":"'"${role}"'","EVENT":"'"${EVENT}"'","INPUT_FINGERPRINT":"'"${fp}"'","OWNER":"'"${owner}"'","STARTED_AT":"'"$STAMP"'","STATUS":"RUNNING"}'

  RECEIPT="${FLEET_STATE_DIR}/${role}/receipts/${JOB_ID}.json"
  mkdir -p "$(dirname "$RECEIPT")"
  if [[ $rc -eq 0 ]]; then
    RESULT="SUCCEEDED"; USEFUL="true"
  elif [[ $rc -eq 124 ]] || [[ $rc -eq 137 ]]; then
    RESULT="TIMEOUT"; USEFUL="false"
  else
    RESULT="FAILED"; USEFUL="false"
  fi
  COMPLETED="$(date -Is)"
  atomic_cat_json "$RECEIPT" '{"JOB_ID":"'"${JOB_ID}"'","ROLE":"'"${role}"'","EVENT":"'"${EVENT}"'","INPUT_FINGERPRINT":"'"${fp}"'","OWNER":"'"${owner}"'","STARTED_AT":"'"${STAMP}"'","COMPLETED_AT":"'"${COMPLETED}"'","RESULT":"'"${RESULT}"'","EXIT_CODE":'"${rc}"',"DURATION_S":'"${duration}"',"OUTPUT_REF":"'"${out_dir}/owner_output.txt"'","USEFUL_OUTPUT":"'"${USEFUL}"'","NEXT_ACTION":"","BLOCKER":""}'
  chmod 0640 "$RECEIPT"
  if [[ "$RESULT" == "SUCCEEDED" ]]; then
    terminal_marker="$FLEET_STATE_DIR/${role}/terminal/${JOB_ID}.useful.json"
    if [[ "$USEFUL" == "true" ]]; then
      counter_once "$FLEET_STATE_DIR/${role}.useful_count" "$terminal_marker" || {
        log "TERMINALIZATION_BLOCKED role=${role} job=${JOB_ID}"
        exit 1
      }
    fi
    atomic_json_set "$sf" "STATUS=SUCCEEDED" "LAST_SUCCESS_AT=$COMPLETED" \
      "LAST_PROOF=$RECEIPT" "LAST_RESULT=SUCCEEDED"
    [[ "$USEFUL" == "true" ]] && atomic_json_set "$terminal_marker" "STATE=COMMITTED" "TERMINAL_RESULT=SUCCEEDED"
  elif [[ "$RESULT" == "TIMEOUT" ]]; then
    terminal_marker="$FLEET_STATE_DIR/${role}/terminal/${JOB_ID}.timeout.json"
    counter_once "$FLEET_STATE_DIR/${role}.timeout_count" "$terminal_marker" || {
      log "TERMINALIZATION_BLOCKED role=${role} job=${JOB_ID}"
      exit 1
    }
    atomic_json_set "$sf" "STATUS=TIMEOUT" "BLOCKER=owner_timeout"
    atomic_json_set "$terminal_marker" "STATE=COMMITTED" "TERMINAL_RESULT=TIMEOUT"
  else
    terminal_marker="$FLEET_STATE_DIR/${role}/terminal/${JOB_ID}.failure.json"
    counter_once "$FLEET_STATE_DIR/${role}.failure_count" "$terminal_marker" || {
      log "TERMINALIZATION_BLOCKED role=${role} job=${JOB_ID}"
      exit 1
    }
    atomic_json_set "$sf" "STATUS=FAILED" "BLOCKER=owner_failed_rc_${rc}"
    atomic_json_set "$terminal_marker" "STATE=COMMITTED" "TERMINAL_RESULT=FAILED"
  fi

  pending_job="$pending_dir/${JOB_ID}.json"
  consumed_dir="$pending_dir/consumed"
  mkdir -p "$consumed_dir"
  mv -- "$pending_job" "$consumed_dir/$(basename "$pending_job")"
  log "OWNER_EXECUTED role=${role} job=${JOB_ID} result=${RESULT} duration=${duration}s"
done

exec 9>&-
log "dispatch complete event=${EVENT}"
