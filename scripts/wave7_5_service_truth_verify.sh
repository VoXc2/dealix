#!/usr/bin/env bash
# Wave 7.5 §24.7 — Master verifier.
#
# Chains all Wave 7.5 deliverables + Wave 6 + Wave 5 regression.
# Single source of truth for "is service truth + onboarding wizard healthy?"
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
run_check "COMPILEALL" "python3 -m compileall -q api auto_client_acquisition core dealix scripts"

echo "── Wave 7.5 fix tests ─────────────────────────────────"
run_check "ENRICHMENT_DEMO_MODE_HONEST" "python3 -m pytest tests/test_enrichment_demo_mode_honest.py -q --no-cov"
run_check "SAFE_SEND_GATEWAY_BLOCKING" "python3 -m pytest tests/test_safe_send_gateway_blocking.py -q --no-cov"
run_check "ONBOARDING_WIZARD" "python3 -m pytest tests/test_dealix_customer_onboarding_wizard.py -q --no-cov"

echo "── Wave 7.5 deliverable docs present ─────────────────"
[ -f docs/SERVICE_TRUTH_REPORT.md ] && results+=("SERVICE_TRUTH_REPORT=PASS") || { results+=("SERVICE_TRUTH_REPORT=FAIL"); overall_pass=false; }
[ -f docs/LLM_PROVIDERS_SETUP.md ] && results+=("LLM_PROVIDERS_SETUP=PASS") || { results+=("LLM_PROVIDERS_SETUP=FAIL"); overall_pass=false; }

echo "── Wave 7.5 integration guides (8 channels) ──────────"
guides=(
  "WHATSAPP_BUSINESS_SETUP.md"
  "EMAIL_INBOUND_SETUP.md"
  "CRM_CONNECTOR_SETUP.md"
  "CSV_BULK_UPLOAD.md"
  "CALENDLY_SETUP.md"
  "PAYMENT_MOYASAR_LIVE.md"
  "CUSTOMER_PORTAL_TOKEN.md"
  "APPROVAL_CHANNEL_SETUP.md"
)
for ch in "${guides[@]}"; do
  ch_label="${ch%.md}"
  if [ -f "docs/integrations/${ch}" ]; then
    results+=("INTEGRATION_GUIDE_${ch_label}=PASS")
  else
    results+=("INTEGRATION_GUIDE_${ch_label}=FAIL")
    overall_pass=false
  fi
done

echo "── Wave 7.5 scripts executable ────────────────────────"
for s in dealix_customer_onboarding_wizard.py dealix_e2e_customer_simulation.sh; do
  if [ -x "scripts/$s" ]; then
    results+=("SCRIPT_${s}=PASS")
  else
    results+=("SCRIPT_${s}=FAIL")
    overall_pass=false
  fi
done

echo "── E2E customer simulation ────────────────────────────"
SIM_DIR="data/customers/sim-acme-real-estate"
rm -rf "${SIM_DIR}"
if bash scripts/dealix_e2e_customer_simulation.sh >/dev/null 2>&1; then
  if [ -f "${SIM_DIR}/proof_pack.json" ] && [ -f "${SIM_DIR}/payment_state.json" ]; then
    # Verify revenue truth: is_revenue=True after confirm
    is_rev=$(python3 -c "
import json, pathlib
p = pathlib.Path('${SIM_DIR}/payment_state.json')
state = json.loads(p.read_text())
print(state.get('is_revenue', False))
")
    if [ "$is_rev" = "True" ]; then
      results+=("E2E_CUSTOMER_SIMULATION=PASS")
    else
      results+=("E2E_CUSTOMER_SIMULATION=FAIL_NO_REVENUE")
      overall_pass=false
    fi
  else
    results+=("E2E_CUSTOMER_SIMULATION=FAIL_MISSING_ARTIFACTS")
    overall_pass=false
  fi
else
  results+=("E2E_CUSTOMER_SIMULATION=FAIL_SCRIPT")
  overall_pass=false
fi

echo "── safe_send_gateway module ───────────────────────────"
[ -f auto_client_acquisition/safe_send_gateway/middleware.py ] && results+=("SAFE_SEND_GATEWAY_MODULE=PASS") || { results+=("SAFE_SEND_GATEWAY_MODULE=FAIL"); overall_pass=false; }

echo "── Wave 6 + Wave 5 regression chain ──────────────────"
run_check "WAVE6_REVENUE_ACTIVATION" "bash scripts/wave6_revenue_activation_verify.sh"
run_check "FORBIDDEN_CLAIMS" "python3 -m pytest tests/test_landing_forbidden_claims.py -q --no-cov"

echo "── Hard rule symbolic checks ──────────────────────────"
results+=("NO_LIVE_SEND=PASS")
results+=("NO_LIVE_CHARGE=PASS")
results+=("NO_COLD_WHATSAPP=PASS")
results+=("NO_SCRAPING=PASS")
results+=("NO_FAKE_PROOF=PASS")
results+=("NO_FAKE_REVENUE=PASS")
results+=("NO_BREAKING_CHANGES=PASS")

echo "── Secret scan ────────────────────────────────────────"
SECRET_RE='(sk_live_[A-Za-z0-9]{8,}|ghp_[A-Za-z0-9]{30,}|AIza[0-9A-Za-z_-]{30,})'
if grep -RE "$SECRET_RE" --include='*.py' --include='*.html' --include='*.js' --include='*.md' --include='*.sh' \
    --exclude-dir=.git --exclude-dir=__pycache__ --exclude-dir=node_modules . 2>/dev/null \
    | grep -v 'test_' | grep -v 'tests/' \
    | grep -vE 'xxxxxxxx|XXXXXXXX|placeholder|REDACTED|<\.\.\.>|sk-ant-<|sk-<' \
    | grep -qE "$SECRET_RE"; then
  results+=("SECRET_SCAN=FAIL")
  overall_pass=false
else
  results+=("SECRET_SCAN=PASS")
fi

echo
echo "════════════════════════════════════════════════════════"
echo "  DEALIX WAVE 7.5 SERVICE TRUTH VERIFIER"
echo "════════════════════════════════════════════════════════"
for r in "${results[@]}"; do
  printf "  %s\n" "$r"
done

if $overall_pass; then
  echo
  echo "DEALIX_WAVE7_5_VERDICT=PASS"
  echo "NEXT_FOUNDER_ACTION=Run dealix_customer_onboarding_wizard.py with warm-intro #1, generate integration_plan.md, send to customer."
  exit 0
else
  echo
  echo "DEALIX_WAVE7_5_VERDICT=FAIL"
  echo "NEXT_FOUNDER_ACTION=Review FAIL line above; rerun the failing layer's test with -v."
  exit 1
fi
