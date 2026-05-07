#!/usr/bin/env bash
# V11 master verifier — runs every V11 closure check and prints a verdict.
#
# Usage:
#   bash scripts/v11_customer_closure_verify.sh
#   BASE_URL=https://api.dealix.me bash scripts/v11_customer_closure_verify.sh
#
# Exit code: 0 if all PASS, 1 if any FAIL. Verdict block always printed.
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# --- Result trackers ---------------------------------------------------------
declare -A RESULTS

mark() {
  RESULTS["$1"]="$2"
}

OVERALL_OK=1

# --- 1. compileall -----------------------------------------------------------
echo "[v11] 1/9 compileall…"
if python3 -m compileall -q api auto_client_acquisition db scripts \
    >/tmp/v11_compileall.log 2>&1; then
  mark COMPILEALL pass
else
  mark COMPILEALL fail
  OVERALL_OK=0
fi

# --- 2. V11 targeted tests ---------------------------------------------------
echo "[v11] 2/9 V11 targeted tests…"
V11_TESTS=(
  tests/test_founder_dashboard_performance_v11.py
  tests/test_status_aliases_v11.py
  tests/test_runtime_paths_v11.py
  tests/test_delivery_factory_status_v11.py
  tests/test_first3_board_v11.py
  tests/test_dealix_diagnostic_v11.py
  tests/test_payment_fallback_v11.py
  tests/test_proof_pack_v11.py
  tests/test_phase_e_today_v11.py
  tests/test_truth_labels_v11.py
)
if python3 -m pytest -q --no-cov "${V11_TESTS[@]}" \
    >/tmp/v11_targeted_tests.log 2>&1; then
  mark V11_TARGETED_TESTS pass
else
  mark V11_TARGETED_TESTS fail
  OVERALL_OK=0
fi

# --- 3. Phase E docs presence ------------------------------------------------
echo "[v11] 3/9 Phase E docs presence…"
PHASE_E_DOCS=(
  README.md 00_GO_NO_GO.md 01_FIRST_3_WARM_INTROS_BOARD.md
  02_FIRST_10_WARM_MESSAGES_AR_EN.md 03_MINI_DIAGNOSTIC_TEMPLATE.md
  04_DIAGNOSTIC_SCRIPT_USAGE.md 05_PILOT_499_OFFER.md
  06_MANUAL_PAYMENT_FALLBACK.md 07_7_DAY_PILOT_DELIVERY_PLAN.md
  08_PROOF_PACK_TEMPLATE.md 09_CUSTOMER_REVIEW_AND_UPSELL.md
  10_DAILY_FOUNDER_LOOP.md 11_FIRST_CUSTOMER_EVIDENCE_TABLE.md
)
PHASE_E_PASS=1
for d in "${PHASE_E_DOCS[@]}"; do
  if [[ ! -f "docs/phase-e/$d" ]]; then
    PHASE_E_PASS=0
    echo "[v11]   missing: docs/phase-e/$d" >&2
  fi
done
if [[ $PHASE_E_PASS -eq 1 ]]; then
  mark PHASE_E_DOCS pass
else
  mark PHASE_E_DOCS fail
  OVERALL_OK=0
fi

# --- 4. Diagnostic CLI smoke -------------------------------------------------
echo "[v11] 4/9 Diagnostic CLI smoke…"
if python3 scripts/dealix_diagnostic.py --company "Customer-Slot-A" \
    --sector b2b_services --region riyadh \
    --pipeline-state "smoke test" >/tmp/v11_diag.log 2>&1; then
  mark DIAGNOSTIC_CLI pass
else
  mark DIAGNOSTIC_CLI fail
  OVERALL_OK=0
fi

# --- 5. First-3 board generator ----------------------------------------------
echo "[v11] 5/9 First-3 board generator…"
if python3 scripts/dealix_first3_board.py --dry-run \
    >/tmp/v11_first3.log 2>&1; then
  mark FIRST3_BOARD pass
else
  mark FIRST3_BOARD fail
  OVERALL_OK=0
fi

# --- 6. Proof pack empty template --------------------------------------------
echo "[v11] 6/9 Proof pack empty template…"
TMPDIR_PP="$(mktemp -d)"
if python3 scripts/dealix_proof_pack.py --customer-handle Customer-Slot-A \
    --events-dir "$TMPDIR_PP" --allow-empty \
    >/tmp/v11_pp.log 2>&1; then
  mark PROOF_PACK_TEMPLATE pass
else
  mark PROOF_PACK_TEMPLATE fail
  OVERALL_OK=0
fi
rm -rf "$TMPDIR_PP"

# --- 7. Payment fallback dry-run ---------------------------------------------
echo "[v11] 7/9 Payment fallback dry-run…"
if python3 scripts/dealix_invoice.py --email test@example.sa \
    --amount-sar 499 --description "v11 verify" --dry-run \
    >/tmp/v11_pay.log 2>&1; then
  mark PAYMENT_FALLBACK pass
else
  mark PAYMENT_FALLBACK fail
  OVERALL_OK=0
fi

# --- 8. Phase E today script -------------------------------------------------
echo "[v11] 8/9 Phase E today script…"
if python3 scripts/dealix_phase_e_today.py --json \
    >/tmp/v11_today.log 2>&1; then
  mark PHASE_E_TODAY pass
else
  mark PHASE_E_TODAY fail
  OVERALL_OK=0
fi

# --- 9. Forbidden-claims + secret scan --------------------------------------
echo "[v11] 9/9 Forbidden-claims + secret scan…"
if python3 -m pytest -q --no-cov tests/test_landing_forbidden_claims.py \
    >/tmp/v11_forbidden.log 2>&1; then
  mark FORBIDDEN_CLAIMS pass
else
  mark FORBIDDEN_CLAIMS fail
  OVERALL_OK=0
fi
# Secret scan — block real-looking secret prefixes outside test fixtures.
SECRET_HITS=$(
  grep -REn 'sk_live_[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{36}|AIza[0-9A-Za-z_-]{35}' \
    --include='*.py' --include='*.md' . \
    --exclude-dir=.git --exclude-dir=.claude --exclude-dir=__pycache__ 2>/dev/null \
  | grep -vE 'test_|EXAMPLE|placeholder|dummy|sk_live_xxxxx|sk_live_should_|sk_live_x{10,}|allowlist|fixture|bogus|never_land' \
  | head -3
)
if [[ -z "$SECRET_HITS" ]]; then
  mark SECRET_SCAN pass
else
  mark SECRET_SCAN fail
  OVERALL_OK=0
  echo "[v11] secret hits:" >&2
  echo "$SECRET_HITS" >&2
fi

# --- Optional production smoke -----------------------------------------------
PROD_SMOKE_RESULT="not_run"
if [[ -n "${BASE_URL:-}" ]]; then
  echo "[v11] (optional) production smoke against $BASE_URL…"
  if python3 scripts/dealix_smoke_test.py --base-url "$BASE_URL" --json \
      >/tmp/v11_prod_smoke.json 2>/dev/null; then
    PASSED=$(python3 -c "import json; print(json.load(open('/tmp/v11_prod_smoke.json'))['passed'])")
    TOTAL=$(python3 -c "import json; print(json.load(open('/tmp/v11_prod_smoke.json'))['total'])")
    PROD_SMOKE_RESULT="$PASSED/$TOTAL"
    if [[ "$PASSED" == "$TOTAL" ]]; then
      mark PROD_SMOKE pass
    else
      mark PROD_SMOKE partial
    fi
  else
    mark PROD_SMOKE fail
    PROD_SMOKE_RESULT="failed"
  fi
fi

# --- Verdict block -----------------------------------------------------------
echo ""
echo "================== V11 CUSTOMER CLOSURE VERDICT =================="
if [[ $OVERALL_OK -eq 1 ]]; then
  echo "V11_CUSTOMER_CLOSURE=PASS"
else
  echo "V11_CUSTOMER_CLOSURE=FAIL"
fi
for k in COMPILEALL V11_TARGETED_TESTS PHASE_E_DOCS DIAGNOSTIC_CLI \
         FIRST3_BOARD PROOF_PACK_TEMPLATE PAYMENT_FALLBACK \
         PHASE_E_TODAY FORBIDDEN_CLAIMS SECRET_SCAN; do
  echo "${k}=${RESULTS[$k]:-not_run}"
done
echo "PROD_SMOKE=${PROD_SMOKE_RESULT}"
echo "LIVE_GATES=blocked"
echo "OUTREACH_GO=yes"
if [[ $OVERALL_OK -eq 1 ]]; then
  echo "NEXT_ACTION=Merge V11 PR + Railway redeploy + start Phase E with first warm intro"
else
  echo "NEXT_ACTION=Inspect failed checks above; logs in /tmp/v11_*.log"
fi
echo "==================================================================="

if [[ $OVERALL_OK -eq 1 ]]; then
  exit 0
else
  exit 1
fi
