#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

# Dealix Capability Frontier V2 (ranks 51-100)
# Research/admission only. No bulk install. No L5 material action.

MODE="${1:-audit}"
case "$MODE" in audit|pilot) ;; *) echo "Usage: $0 [audit|pilot]" >&2; exit 2 ;; esac

export TZ=Asia/Riyadh
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export GH_PROMPT_DISABLED=1
export GIT_TERMINAL_PROMPT=0
export PYTHONNOUSERSITE=1

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
V1="$REPO/config/oss/capability_top50_v1.tsv"
REGISTRY="$REPO/config/oss/capability_frontier_v2.tsv"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
PROOF="$CONTROL/proof/capability-frontier-v2/$STAMP"
RESULTS="$PROOF/results.tsv"
SUMMARY="$PROOF/summary.env"
SAFE_PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

need() { command -v "$1" >/dev/null 2>&1 || { echo "RESULT=HOLD_MISSING_COMMAND_$1" >&2; exit 10; }; }
need git
need python3
need timeout
need sha256sum

install -d -m 0750 -o "$RUN_USER" -g "$RUN_GROUP" "$PROOF"

safe_git() {
  sudo -u "$RUN_USER" env HOME="/home/$RUN_USER" PATH="$SAFE_PATH" \
    git -c safe.directory="$REPO" -C "$REPO" "$@"
}

[[ -f "$V1" ]] || { echo "RESULT=HOLD_V1_REGISTRY_MISSING"; exit 11; }
[[ -f "$REGISTRY" ]] || { echo "RESULT=HOLD_V2_REGISTRY_MISSING"; exit 12; }

safe_git fetch origin main --prune --quiet
LIVE_MAIN="$(safe_git rev-parse origin/main)"
LOCAL_HEAD="$(safe_git rev-parse HEAD 2>/dev/null || echo UNKNOWN)"
DIRTY_COUNT="$(safe_git status --porcelain=v1 2>/dev/null | wc -l | tr -d ' ')"
printf 'LIVE_MAIN=%s\nLOCAL_HEAD=%s\nLOCAL_DIRTY_COUNT=%s\nMODE=%s\n' \
  "$LIVE_MAIN" "$LOCAL_HEAD" "$DIRTY_COUNT" "$MODE" | tee "$PROOF/reconcile.env"

python3 - "$V1" "$REGISTRY" <<'PY'
import csv, sys
v1, v2 = sys.argv[1:]
with open(v1, encoding='utf-8', newline='') as f:
    old=list(csv.DictReader(f, delimiter='\t'))
with open(v2, encoding='utf-8', newline='') as f:
    rows=list(csv.DictReader(f, delimiter='\t'))
assert len(old)==50, f'expected v1 50 rows, got {len(old)}'
assert len(rows)==50, f'expected v2 50 rows, got {len(rows)}'
assert [int(r['rank']) for r in rows] == list(range(51,101)), 'v2 ranks must be 51..100'
assert len({r['id'] for r in rows})==50, 'duplicate v2 id'
assert len({r['repository'].lower() for r in rows})==50, 'duplicate v2 repository'
old_ids={r['id'].lower() for r in old}; old_repos={r['repository'].lower() for r in old}
assert not (old_ids & {r['id'].lower() for r in rows}), 'v1/v2 duplicate id'
assert not (old_repos & {r['repository'].lower() for r in rows}), 'v1/v2 duplicate repository'
allowed={'ADOPT_NOW','ADOPT_NOW_BOUNDED','ADOPT_FOR_ACCEPTANCE','ALREADY_BOUNDED','PILOT_ISOLATED','DEFER','DEFER_MEASURED_GAP','REJECT_DUPLICATE_DEFAULT'}
unknown=sorted({r['decision'] for r in rows}-allowed)
assert not unknown, f'unknown decisions: {unknown}'
owners={'dealix-pm','dealix-sales','dealix-delivery','dealix-engineer','dealix-content'}
unknown_owners=sorted({r['owner'] for r in rows}-owners)
assert not unknown_owners, f'unknown owners: {unknown_owners}'
required=('problem_solved','duplication_guard','benchmark','acceptance','rollback')
for r in rows:
    for key in required:
        assert r.get(key,'').strip(), f"{r['id']} missing {key}"
print('FRONTIER_V2_CONTRACT=PASS')
PY

printf 'rank\tid\tcategory\tdecision\trepository\towner\treachable\tduplicate_hits\tlocal_state\tprobe_result\n' > "$RESULTS"

local_tool_for() {
  case "$1" in
    garak) echo garak ;;
    trafilatura) echo trafilatura ;;
    pip_audit) echo pip-audit ;;
    bandit) echo bandit ;;
    reuse_tool) echo reuse ;;
    nektos_act) echo act ;;
    hyperfine) echo hyperfine ;;
    sqlfluff) echo sqlfluff ;;
    checkdmarc) echo checkdmarc ;;
    pa11y) echo pa11y ;;
    sentry_cli) echo sentry-cli ;;
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
  if [[ $rc -eq 0 ]]; then printf 'PASS:%s' "$out"; else printf 'HOLD_VERSION_PROBE_RC_%s:%s' "$rc" "$out"; fi
}

while IFS=$'\t' read -r rank id category decision repository owner problem duplication benchmark acceptance rollback; do
  [[ "$rank" == rank ]] && continue
  [[ -n "$rank" && -n "$id" && -n "$repository" ]] || continue

  reachable=NO
  if timeout 15s git ls-remote --exit-code "https://github.com/$repository.git" HEAD \
      >/dev/null 2>"$PROOF/${rank}-${id}-lsremote.err"; then
    reachable=YES
  fi

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

  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$rank" "$id" "$category" "$decision" "$repository" "$owner" "$reachable" \
    "$duplicate_hits" "$local_state" "$probe" >> "$RESULTS"
done < "$REGISTRY"

python3 - "$RESULTS" "$SUMMARY" <<'PY'
import csv, sys
src, out = sys.argv[1:]
rows=list(csv.DictReader(open(src, encoding='utf-8'), delimiter='\t'))
reach=sum(r['reachable']=='YES' for r in rows)
adopt=sum(r['decision'].startswith('ADOPT') for r in rows)
pilot=sum(r['decision']=='PILOT_ISOLATED' for r in rows)
defer=sum(r['decision'].startswith('DEFER') for r in rows)
with open(out,'w',encoding='utf-8') as f:
    f.write(f'FRONTIER_ROWS={len(rows)}\n')
    f.write(f'REACHABLE={reach}\n')
    f.write(f'ADOPT_CANDIDATES={adopt}\n')
    f.write(f'PILOT_CANDIDATES={pilot}\n')
    f.write(f'DEFER_CANDIDATES={defer}\n')
    f.write('MAX_ACTIVE_BENCHMARKS=1\n')
    f.write('BULK_INSTALL=false\n')
    f.write('L5_EXECUTED=NONE\n')
print(f'FRONTIER_ROWS={len(rows)} REACHABLE={reach} ADOPT={adopt} PILOT={pilot} DEFER={defer}')
PY

sha256sum "$V1" "$REGISTRY" "$RESULTS" "$SUMMARY" > "$PROOF/SHA256SUMS"
chown -R "$RUN_USER:$RUN_GROUP" "$PROOF"

echo "PROOF=$PROOF"
echo "NEXT=Select ONE measured-gap benchmark from the frontier; do not bulk-install."
echo "L5_EXECUTED=NONE"
echo "RESULT=PASS_CAPABILITY_FRONTIER_V2_AUDIT"
