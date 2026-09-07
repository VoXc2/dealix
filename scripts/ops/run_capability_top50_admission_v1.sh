#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

# Dealix Top-50 Capability Admission V1
# Audits all 50 curated OSS/tool candidates against live Dealix source.
# No bulk installation. No L5 material effect. One benchmark at a time.

MODE="${1:-audit}"
case "$MODE" in audit|pilot) ;; *) echo "Usage: $0 [audit|pilot]" >&2; exit 2 ;; esac

export TZ=Asia/Riyadh
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export GH_PROMPT_DISABLED=1
export GIT_TERMINAL_PROMPT=0
export PYTHONNOUSERSITE=1

# Fail-closed material authority.
export DEALIX_EXTERNAL_SEND=0
export DEALIX_EMAIL_LIVE_SEND=0
export DEALIX_WHATSAPP_OUTBOUND=0
export DEALIX_PUBLIC_PUBLISH=0
export DEALIX_PAID_SPEND=0
export DEALIX_PAYMENT_EXECUTION=0
export DEALIX_PRODUCTION_MUTATION=0
export DEALIX_DNS_MUTATION=0
export DEALIX_DB_MUTATION=0
export DEALIX_SECRET_MUTATION=0
export DEALIX_IDENTITY_MUTATION=0
export DEALIX_AGENT_SELF_AUTHORITY=0
export DEALIX_AUTONOMY_LEVEL=4
export DEALIX_MODE=draft-only
export VOICE_AI_ENABLED=false
export VOICE_RECORDING_ENABLED=false
export VOICE_OUTBOUND_ENABLED=false

REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
CONTROL="${DEALIX_CONTROL:-/opt/dealix/control}"
RUN_USER="${DEALIX_RUN_USER:-dealix}"
RUN_GROUP="${DEALIX_RUN_GROUP:-dealix}"
REGISTRY_REL="config/oss/capability_top50_v1.tsv"
REGISTRY="$REPO/$REGISTRY_REL"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
PROOF="$CONTROL/proof/capability-top50/$STAMP"
RESULTS="$PROOF/results.tsv"
SUMMARY="$PROOF/summary.env"
JSON_OUT="$PROOF/top50.json"
SAFE_PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

need() {
  command -v "$1" >/dev/null 2>&1 || { echo "RESULT=HOLD_MISSING_COMMAND_$1" >&2; exit 10; }
}
need git
need python3
need timeout
need sha256sum
need awk

install -d -m 0750 -o "$RUN_USER" -g "$RUN_GROUP" "$PROOF"

safe_git() {
  sudo -u "$RUN_USER" env HOME="/home/$RUN_USER" PATH="$SAFE_PATH" \
    git -c safe.directory="$REPO" -C "$REPO" "$@"
}

[[ -f "$REGISTRY" ]] || {
  echo "RESULT=HOLD_REGISTRY_MISSING"
  echo "REGISTRY=$REGISTRY"
  exit 11
}

# Live source authority; never reset/clean/pull the canonical workspace.
safe_git fetch origin main --prune --quiet
LIVE_MAIN="$(safe_git rev-parse origin/main)"
LOCAL_HEAD="$(safe_git rev-parse HEAD 2>/dev/null || echo UNKNOWN)"
DIRTY_COUNT="$(safe_git status --porcelain=v1 2>/dev/null | wc -l | tr -d ' ')"

printf 'LIVE_MAIN=%s\nLOCAL_HEAD=%s\nLOCAL_DIRTY_COUNT=%s\nMODE=%s\n' \
  "$LIVE_MAIN" "$LOCAL_HEAD" "$DIRTY_COUNT" "$MODE" | tee "$PROOF/reconcile.env"

# Validate registry contract before any network probing.
python3 - "$REGISTRY" <<'PY'
import csv, sys
p=sys.argv[1]
with open(p, encoding='utf-8', newline='') as f:
    rows=list(csv.DictReader(f, delimiter='\t'))
ids=[r['id'] for r in rows]
ranks=[r['rank'] for r in rows]
assert len(rows)==50, f"expected 50 candidates, got {len(rows)}"
assert len(set(ids))==50, "duplicate capability id"
assert len(set(ranks))==50, "duplicate rank"
allowed={
 'ADOPT_NOW','ADOPT_NOW_BOUNDED','ADOPT_FOR_ACCEPTANCE','ALREADY_BOUNDED',
 'PILOT_ISOLATED','DEFER','DEFER_MEASURED_GAP','REJECT_DUPLICATE_DEFAULT'
}
unknown=sorted({r['decision'] for r in rows}-allowed)
assert not unknown, f"unknown decisions: {unknown}"
print('REGISTRY_CONTRACT=PASS')
PY

printf 'rank\tid\tcategory\tdecision\trepository\treachable\tduplicate_hits\tlocal_state\tprobe_result\n' > "$RESULTS"

local_tool_for() {
  case "$1" in
    osv_scanner) echo osv-scanner ;;
    syft) echo syft ;;
    grype) echo grype ;;
    trivy) echo trivy ;;
    gitleaks) echo gitleaks ;;
    detect_secrets) echo detect-secrets ;;
    semgrep) echo semgrep ;;
    zizmor) echo zizmor ;;
    actionlint) echo actionlint ;;
    openssf_scorecard) echo scorecard ;;
    cosign) echo cosign ;;
    checkov) echo checkov ;;
    trufflehog) echo trufflehog ;;
    clamav) echo clamscan ;;
    playwright) echo playwright ;;
    schemathesis) echo schemathesis ;;
    k6) echo k6 ;;
    hurl) echo hurl ;;
    ruff) echo ruff ;;
    uv) echo uv ;;
    pre_commit) echo pre-commit ;;
    pyright) echo pyright ;;
    otel_collector) echo otelcol ;;
    promptfoo) echo promptfoo ;;
    duckdb) echo duckdb ;;
    *) echo NONE ;;
  esac
}

probe_version() {
  local tool="$1"
  [[ "$tool" != NONE ]] || { echo NOT_APPLICABLE; return 0; }
  command -v "$tool" >/dev/null 2>&1 || { echo NOT_INSTALLED; return 0; }
  [[ "$MODE" == pilot ]] || { echo AVAILABLE_NOT_EXECUTED; return 0; }

  set +e
  local out rc
  out="$(timeout 15s "$tool" --version 2>&1 | head -n 2 | tr '\t\r\n' '   ')"
  rc=$?
  set -e
  if [[ $rc -eq 0 ]]; then
    printf 'PASS:%s' "$out"
  else
    printf 'HOLD_VERSION_PROBE_RC_%s:%s' "$rc" "$out"
  fi
}

# Sequential by design. The company law permits max one active benchmark.
tail -n +2 "$REGISTRY" | while IFS=$'\t' read -r rank id category decision repository purpose; do
  [[ -n "$rank" && -n "$id" && -n "$repository" ]] || continue

  reachable=NO
  if timeout 15s git ls-remote --exit-code "https://github.com/$repository.git" HEAD \
      >/dev/null 2>"$PROOF/${rank}-${id}-lsremote.err"; then
    reachable=YES
  fi

  # Zero matches is normal, not an error. This is only a duplication hint.
  duplicate_hits="$({
      safe_git grep -I -i -E "${id//_/[-_ ]}|$(basename "$repository")" "$LIVE_MAIN" -- \
        'docs/**' 'data/**' 'config/**' 'scripts/**' 2>/dev/null || true
    } | head -n 50 | wc -l | tr -d ' ')"

  tool="$(local_tool_for "$id")"
  if [[ "$tool" == NONE ]]; then
    local_state=LIBRARY_OR_SERVICE
  elif command -v "$tool" >/dev/null 2>&1; then
    local_state=AVAILABLE
  else
    local_state=ABSENT
  fi
  probe="$(probe_version "$tool")"

  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$rank" "$id" "$category" "$decision" "$repository" "$reachable" \
    "$duplicate_hits" "$local_state" "$probe" >> "$RESULTS"
done

chown "$RUN_USER:$RUN_GROUP" "$RESULTS"

python3 - "$REGISTRY" "$RESULTS" "$JSON_OUT" "$LIVE_MAIN" "$MODE" <<'PY'
import csv, json, sys
registry, results, out, main, mode=sys.argv[1:]
with open(registry, encoding='utf-8', newline='') as f:
    candidates=list(csv.DictReader(f, delimiter='\t'))
with open(results, encoding='utf-8', newline='') as f:
    audit={r['id']:r for r in csv.DictReader(f, delimiter='\t')}
for c in candidates:
    c['audit']=audit.get(c['id'], {})
payload={
  'schema':'dealix.capability_top50.v1',
  'live_main':main,
  'mode':mode,
  'north_star':'CASH_READY_AUTONOMOUS_DEALIX_COMPANY',
  'law':'REJECT_DUPLICATE_BY_DEFAULT; max one benchmark; no L5 material effects',
  'candidates':candidates,
}
with open(out,'w',encoding='utf-8') as f:
    json.dump(payload,f,ensure_ascii=False,indent=2)
PY
chown "$RUN_USER:$RUN_GROUP" "$JSON_OUT"

TOTAL="$(awk 'END{print NR-1}' "$REGISTRY")"
REACHABLE="$(awk -F '\t' 'NR>1 && $6=="YES"{n++} END{print n+0}' "$RESULTS")"
AVAILABLE="$(awk -F '\t' 'NR>1 && $8=="AVAILABLE"{n++} END{print n+0}' "$RESULTS")"
ABSENT="$(awk -F '\t' 'NR>1 && $8=="ABSENT"{n++} END{print n+0}' "$RESULTS")"
ADOPT="$(awk -F '\t' 'NR>1 && $4 ~ /^ADOPT/{n++} END{print n+0}' "$RESULTS")"
PILOT="$(awk -F '\t' 'NR>1 && $4=="PILOT_ISOLATED"{n++} END{print n+0}' "$RESULTS")"
DEFER="$(awk -F '\t' 'NR>1 && $4 ~ /^DEFER/{n++} END{print n+0}' "$RESULTS")"
REJECT="$(awk -F '\t' 'NR>1 && $4 ~ /^REJECT/{n++} END{print n+0}' "$RESULTS")"

cat > "$SUMMARY" <<EOF_SUM
LIVE_MAIN=$LIVE_MAIN
MODE=$MODE
TOP50_TOTAL=$TOTAL
REPOS_REACHABLE=$REACHABLE
LOCAL_TOOLS_AVAILABLE=$AVAILABLE
LOCAL_TOOLS_ABSENT=$ABSENT
DECISION_ADOPT=$ADOPT
DECISION_PILOT=$PILOT
DECISION_DEFER=$DEFER
DECISION_REJECT=$REJECT
ACTIVE_BENCHMARKS_MAX=1
AUTO_INSTALL_MISSING_TOOLS=false
MATERIAL_EFFECTS=false
MERGE=false
DEPLOY=false
DNS_MUTATION=false
DB_MUTATION=false
SECRET_MUTATION=false
EXTERNAL_SEND=false
PAYMENT=false
PUBLIC_PUBLISH=false
VERDICT=PASS_TOP50_ADMISSION_AUDIT
EOF_SUM
chown "$RUN_USER:$RUN_GROUP" "$SUMMARY"
sha256sum "$REGISTRY" "$RESULTS" "$JSON_OUT" "$SUMMARY" | tee "$PROOF/SHA256SUMS"

# Reuse the existing company controller if available; never create another scheduler.
if command -v dealix-president >/dev/null 2>&1; then
  set +e
  dealix-president reconcile >"$PROOF/president-reconcile.log" 2>&1
  PRESIDENT_RECONCILE_RC=$?
  dealix-president daily-dry >"$PROOF/president-daily-dry.log" 2>&1
  PRESIDENT_DRY_RC=$?
  set -e
  printf 'PRESIDENT_RECONCILE_RC=%s\nPRESIDENT_DRY_RC=%s\n' \
    "$PRESIDENT_RECONCILE_RC" "$PRESIDENT_DRY_RC" | tee "$PROOF/president.env"
fi

echo "======================================================================"
echo "DEALIX TOP-50 CAPABILITY ADMISSION COMPLETE"
echo "======================================================================"
cat "$SUMMARY"
echo "PROOF=$PROOF"
echo "NEXT=Use the evidence to select ONE measured-gap benchmark; do not bulk-install."
echo "L5_EXECUTED=NONE"
