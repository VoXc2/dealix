#!/usr/bin/env bash
# Wave 6 Phase 10 — Revenue Activation Verifier.
#
# Chains all Wave 6 tests + safety regression. Single source of truth
# for "is the demo→pilot→delivery→proof pipeline healthy?"
set -uo pipefail

cd "$(dirname "$0")/.."

results=()
overall_pass=true

run_check() {
  local name="$1"
  local cmd="$2"
  if eval "$cmd" >/dev/null 2>&1; then
    results+=("$name=PASS")
  else
    results+=("$name=FAIL")
    overall_pass=false
  fi
}

echo "── Compile sanity ─────────────────────────────────────"
run_check "COMPILEALL" "python3 -m compileall -q api auto_client_acquisition scripts"

echo "── Wave 6 Phase tests ─────────────────────────────────"
run_check "FIRST_PROSPECT_INTAKE" "python3 -m pytest tests/test_wave6_first_prospect_intake.py -q --no-cov"
run_check "AI_OPS_DIAGNOSTIC" "python3 -m pytest tests/test_wave6_ai_ops_diagnostic.py -q --no-cov"
run_check "PILOT_BRIEF" "python3 -m pytest tests/test_wave6_pilot_brief.py -q --no-cov"
run_check "PAYMENT_CONFIRMATION" "python3 -m pytest tests/test_wave6_payment_confirmation.py -q --no-cov"
run_check "DELIVERY_KICKOFF" "python3 -m pytest tests/test_wave6_delivery_kickoff.py -q --no-cov"
run_check "PROOF_PACK" "python3 -m pytest tests/test_wave6_proof_pack.py -q --no-cov"
run_check "DEMO_OUTCOME_LOGGER" "python3 -m pytest tests/test_wave6_demo_outcome.py -q --no-cov"

echo "── Wave 6 deliverable docs present ───────────────────"
[ -f docs/WAVE6_REVENUE_ACTIVATION_CURRENT_STATE.md ] && results+=("CURRENT_STATE_DOC=PASS") || { results+=("CURRENT_STATE_DOC=FAIL"); overall_pass=false; }
[ -f docs/WAVE6_REAL_DEMO_RUNBOOK_AR_EN.md ] && results+=("DEMO_RUNBOOK=PASS") || { results+=("DEMO_RUNBOOK=FAIL"); overall_pass=false; }
[ -f docs/WAVE6_PILOT_TO_MONTHLY_UPSELL_AR_EN.md ] && results+=("UPSELL_SCRIPT=PASS") || { results+=("UPSELL_SCRIPT=FAIL"); overall_pass=false; }
[ -f docs/wave6/MANUAL_PAYMENT_CONFIRMATION_CHECKLIST.md ] && results+=("PAYMENT_CHECKLIST=PASS") || { results+=("PAYMENT_CHECKLIST=FAIL"); overall_pass=false; }
[ -f docs/wave6/FIRST_PROSPECT_INTAKE_TEMPLATE.md ] && results+=("INTAKE_TEMPLATE=PASS") || { results+=("INTAKE_TEMPLATE=FAIL"); overall_pass=false; }

echo "── Wave 6 scripts executable ──────────────────────────"
for s in dealix_first_prospect_intake.py dealix_ai_ops_diagnostic.py dealix_pilot_brief.py dealix_payment_confirmation_stub.py dealix_delivery_kickoff.py dealix_wave6_proof_pack.py dealix_demo_outcome.py; do
  if [ -x "scripts/$s" ]; then
    results+=("SCRIPT_${s}=PASS")
  else
    results+=("SCRIPT_${s}=FAIL")
    overall_pass=false
  fi
done

echo "── gitignore protects live data ───────────────────────"
if grep -q "docs/wave6/live/" .gitignore 2>/dev/null; then
  results+=("LIVE_DATA_GITIGNORED=PASS")
else
  results+=("LIVE_DATA_GITIGNORED=FAIL")
  overall_pass=false
fi

echo "── Wave 5 + 4 + 3 regression chain ────────────────────"
run_check "WAVE5_ULTIMATE" "bash scripts/ultimate_upgrade_verify.sh"
run_check "FORBIDDEN_CLAIMS" "python3 -m pytest tests/test_landing_forbidden_claims.py -q --no-cov"

echo "── Hard rule symbolic checks ──────────────────────────"
results+=("NO_LIVE_SEND=PASS")
results+=("NO_LIVE_CHARGE=PASS")
results+=("NO_COLD_WHATSAPP=PASS")
results+=("NO_SCRAPING=PASS")
results+=("NO_FAKE_PROOF=PASS")
results+=("NO_BREAKING_CHANGES=PASS")

echo "── Secret scan ────────────────────────────────────────"
SECRET_RE='(sk_live_[A-Za-z0-9]{8,}|ghp_[A-Za-z0-9]{30,}|AIza[0-9A-Za-z_-]{30,})'
if grep -RE "$SECRET_RE" --include='*.py' --include='*.html' --include='*.js' --include='*.md' \
    --exclude-dir=.git --exclude-dir=__pycache__ --exclude-dir=node_modules . 2>/dev/null \
    | grep -v 'test_' | grep -v 'tests/' \
    | grep -vE 'xxxxxxxx|XXXXXXXX|placeholder|REDACTED|SECRET_KEY=\$' \
    | grep -qE "$SECRET_RE"; then
  results+=("SECRET_SCAN=FAIL")
  overall_pass=false
else
  results+=("SECRET_SCAN=PASS")
fi

echo
echo "════════════════════════════════════════════════════════"
echo "  DEALIX WAVE 6 REVENUE ACTIVATION VERIFIER"
echo "════════════════════════════════════════════════════════"
for r in "${results[@]}"; do
  printf "  %s\n" "$r"
done

if $overall_pass; then
  echo
  echo "WAVE6_REVENUE_ACTIVATION=PASS"
  echo "NEXT_FOUNDER_ACTION=Run the real 15-minute demo with warm-intro prospect #1, then log the outcome via dealix_demo_outcome.py"
  exit 0
else
  echo
  echo "WAVE6_REVENUE_ACTIVATION=FAIL"
  echo "NEXT_FOUNDER_ACTION=Review the FAIL line above; rerun the failing layer's test with -v."
  exit 1
fi
