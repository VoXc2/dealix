#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

export TZ="${TZ:-Asia/Riyadh}"
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export PYTHONNOUSERSITE=1

LAB_ROOT="${DEALIX_OSS_ROOT:-/opt/dealix/labs/oss}"
CONTROL="${DEALIX_CONTROL:-/opt/dealix/control}"
DEALIX_USER="${DEALIX_USER:-dealix}"
DEALIX_GROUP="${DEALIX_GROUP:-dealix}"
STAMP="$(date +%Y%m%d-%H%M%S)"
PROOF="$CONTROL/proof/oss-extended-smoke/$STAMP"

install -d -o root -g "$DEALIX_GROUP" -m 0750 "$PROOF"
exec > >(tee -a "$PROOF/smoke.log") 2>&1

PASS=0
FAIL=0
HOLD=0
RESULTS="$PROOF/results.tsv"
printf 'component\tstatus\tdetail\n' > "$RESULTS"

pass(){ PASS=$((PASS+1)); printf '%s\tPASS\t%s\n' "$1" "${2:-ok}" >> "$RESULTS"; echo "[PASS] $1 ${2:-}"; }
fail(){ FAIL=$((FAIL+1)); printf '%s\tFAIL\t%s\n' "$1" "${2:-failed}" >> "$RESULTS"; echo "[FAIL] $1 ${2:-}"; }
hold(){ HOLD=$((HOLD+1)); printf '%s\tHOLD\t%s\n' "$1" "${2:-hold}" >> "$RESULTS"; echo "[HOLD] $1 ${2:-}"; }
as_dealix(){ sudo -u "$DEALIX_USER" -H "$@"; }

check_import(){
  local name="$1" module="$2" py="$LAB_ROOT/$name/venv/bin/python"
  if [[ ! -x "$py" ]]; then hold "$name" "not_installed"; return 0; fi
  if as_dealix "$py" -c "import $module" >"$PROOF/$name.out" 2>"$PROOF/$name.err"; then
    pass "$name" "import_ok_no_model_load"
  else
    fail "$name" "import_failed"
  fi
}

check_import crawl4ai crawl4ai
check_import paddleocr paddleocr
check_import flagembedding FlagEmbedding
check_import splink splink

# Safety assertions: bootstrap/smoke must not create listening sockets or services
# for these package-only candidates. We only record a coarse before/after-free state.
ss -lntup > "$PROOF/listeners.txt" 2>/dev/null || true
ps -eo pid,user,args | grep -E '[c]rawl4ai|[p]addleocr|[F]lagEmbedding|[s]plink' \
  > "$PROOF/processes.txt" || true

if [[ -s "$PROOF/processes.txt" ]]; then
  hold package-processes "matching_process_text_present_review_required"
else
  pass package-processes "no_candidate_runtime_processes"
fi

cat > "$PROOF/receipt.json" <<EOF
{
  "schema_version": 1,
  "timestamp": "$STAMP",
  "pass": $PASS,
  "fail": $FAIL,
  "hold": $HOLD,
  "services_started_by_smoke": false,
  "ports_exposed_by_smoke": false,
  "models_loaded_by_smoke": false,
  "crawls_executed": false,
  "customer_effects": false
}
EOF
chmod 0640 "$PROOF/receipt.json"

cat "$RESULTS"
echo "PASS=$PASS"
echo "FAIL=$FAIL"
echo "HOLD=$HOLD"
echo "PROOF_ROOT=$PROOF"
echo "NEXT=BENCHMARK_ONLY_WHERE_A_MEASURED_GAP_EXISTS"

[[ "$FAIL" -eq 0 ]]
