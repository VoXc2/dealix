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

latest_artifact() { # newest file matching a repo-relative glob, else empty
  local pattern="$1" best="" best_ts=0 f ts
  for f in $REPO_ROOT/$pattern; do
    [[ -f "$f" ]] || continue
    ts="$(stat -c %Y "$f" 2>/dev/null || echo 0)"
    (( ts > best_ts )) && { best_ts=$ts; best="$f"; }
  done
  echo "$best"
}

resolve_watch() { # token -> absolute path (or empty)
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

# Deterministic fingerprint over resolved watch paths (path|size|mtime), or
# content hash for small dirs. Volatile dirs (.git/node_modules/caches) are
# never traversed because watches are explicit.
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

atomic_json_set() { # FILE key=value... (atomic tmp+rename, never partial)
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


atomic_cat_json() { # FILE single-quoted-json-string -> atomic write
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

roles_for_event() { # derived from REGISTRY — the ONLY routing table
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

run_owner() { # executes the allowlisted canonical command; returns exit code
  local cmd="$1" out="$2"
  (
    cd "$REPO_ROOT"
    set +e
    timeout --kill-after=15 --signal=TERM 300 \
      ./.venv/bin/python ${cmd#.venv/bin/python } >"$out" 2>&1
    rc=$?
    set -e
    exit "$rc"
  )
}

# ---- COLLECT MODE: consume owner completion receipts -----------------------
if [[ "$MODE" == "collect" ]]; then
  for jf in "$FLEET_STATE_DIR"/*/pending/*.json; do
    [[ -f "$jf" ]] || continue
    ROLE="$(json_get "$jf" ROLE)"
    JOB_ID="$(json_get "$jf" JOB_ID)"
    rcpt="$FLEET_STATE_DIR/${ROLE}/receipts/${JOB_ID}.json"
    sf="$FLEET_STATE_DIR/${ROLE}.state.json"
    [[ -f "$rcpt" ]] || continue
    RESULT="$(json_get "$rcpt" RESULT)"
    OWNER="$(json_get "$rcpt" OWNER)"
    USEFUL="$(json_get "$rcpt" USEFUL_OUTPUT)"
    case "$RESULT" in
      SUCCEEDED)
        atomic_json_set "$sf" "STATUS=SUCCEEDED" "LAST_SUCCESS_AT=$(date -Is)" \
          "LAST_PROOF=${rcpt}" "LAST_RESULT=SUCCEEDED" "OWNER=${OWNER}"
        [[ "$USEFUL" == "true" ]] && bump "$FLEET_STATE_DIR/${ROLE}.useful_count"
        mkdir -p "$(dirname "$jf")/consumed"; mv "$jf" "$(dirname "$jf")/consumed/$(basename "$jf")"
        log "RECEIPT_OK role=${ROLE} job=${JOB_ID} result=SUCCEEDED"
        ;;
      FAILED|DEGRADED|TIMEOUT)
        atomic_json_set "$sf" "STATUS=${RESULT}" "LAST_RESULT=${RESULT}" \
          "BLOCKER=$(json_get "$rcpt" BLOCKER)" "OWNER=${OWNER}"
        bump "$FLEET_STATE_DIR/${ROLE}.failure_count"
        mkdir -p "$(dirname "$jf")/consumed"; mv "$jf" "$(dirname "$jf")/consumed/$(basename "$jf")"
        log "RECEIPT_FAIL role=${ROLE} job=${JOB_ID} result=${RESULT}"
        ;;
      *) log "RECEIPT_INVALID role=${ROLE} job=${JOB_ID} result=${RESULT}" ;;
    esac
  done
  exit 0
fi

# ---- DISPATCH MODE ---------------------------------------------------------
WANTED="$(roles_for_event)"
log "dispatch start event=${EVENT} wanted=[${WANTED:-none}] mem=$(mem_available_mb)MB"
if [[ -z "$WANTED" ]]; then
  log "NO_OP unknown-or-sensor event (honest no-op)"
  exit 0
fi

COUNCIL_T0="$(date +%s)"
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
  # Execution identity: changing kind/watches-declaration/owner invalidates
  # dedupe even when business inputs are unchanged (NONE→REAL transitions,
  # owner command rotations, contract changes).
  OWNER_SIGNATURE="$(printf '%s|%s|%s|%s' "$role" "$kind" "$watches" "$owner" | sha256sum | cut -c1-16)"
  EFFECTIVE_FINGERPRINT="$(printf '%s|%s' "$fp" "$OWNER_SIGNATURE" | sha256sum | cut -c1-16)"
  last_efp="$(json_get "$sf" EFFECTIVE_FINGERPRINT)"

  if [[ -n "$last_efp" && "$last_efp" == "$EFFECTIVE_FINGERPRINT" && "${DEALIX_FLEET_FORCE:-0}" != "1" ]]; then
    bump "$FLEET_STATE_DIR/${role}.skip_count"
    # Dedupe must never erase structural truth: an ownerless seat stays
    # BLOCKED across identical re-events (SKIP_UNCHANGED_BLOCKED).
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

  # OWNER_MISSING is structural truth: it must precede host-resource
  # semantics so RAM availability never changes owner-state honesty.
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
  # Supersede unresolved ownerless handoffs — preserve history, never delete.
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

  # Enqueue the job so collect-mode can pair it with the receipt.
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
  # Synchronous owners complete within this dispatch: advance state NOW from
  # the receipt truth (async owners would rely on collect-mode instead).
  if [[ "$RESULT" == "SUCCEEDED" ]]; then
    atomic_json_set "$sf" "STATUS=SUCCEEDED" "LAST_SUCCESS_AT=$COMPLETED" \
      "LAST_PROOF=$RECEIPT" "LAST_RESULT=SUCCEEDED"
    [[ "$USEFUL" == "true" ]] && bump "$FLEET_STATE_DIR/${role}.useful_count"
  elif [[ "$RESULT" == "TIMEOUT" ]]; then
    atomic_json_set "$sf" "STATUS=TIMEOUT" "BLOCKER=owner_timeout"
    bump "$FLEET_STATE_DIR/${role}.timeout_count"
  else
    atomic_json_set "$sf" "STATUS=FAILED" "BLOCKER=owner_failed_rc_${rc}"
    bump "$FLEET_STATE_DIR/${role}.failure_count"
  fi
  # Atomically consume the pending job: sync terminalization is the ONLY
  # authority. Collect-mode will never see this job again.
  for pj in "$pending_dir/${JOB_ID}.json"; do
    mkdir -p "$(dirname "$pj")/consumed"; mv "$pj" "$(dirname "$pj")/consumed/$(basename "$pj")"
  done
  log "OWNER_EXECUTED role=${role} job=${JOB_ID} result=${RESULT} duration=${duration}s"
done

exec 9>&-
log "dispatch complete event=${EVENT}"
