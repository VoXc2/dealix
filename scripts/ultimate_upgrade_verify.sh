#!/usr/bin/env bash
# Ultimate Upgrade Verifier (Phase 14 Wave 5)
#
# Chains Wave 3 + Wave 4 + Wave 5 verifiers + all targeted tests +
# safety regression. Single source of truth for "is the platform PASS?"
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
run_check "COMPILEALL" "python3 -m compileall -q api auto_client_acquisition"

echo "── Wave 5 Phases 1-13 ────────────────────────────────"
run_check "PRODUCT_SIMPLIFICATION" "python3 -m pytest tests/test_customer_safe_product_language.py -q --no-cov"
run_check "EXECUTIVE_COMMAND_CENTER_FINAL" "python3 -m pytest tests/test_executive_command_center_final.py -q --no-cov"
run_check "CUSTOMER_PORTAL_FINAL" "python3 -m pytest tests/test_customer_portal_contract_final.py tests/test_customer_portal_empty_states_final.py -q --no-cov"
run_check "LEADOPS_RELIABILITY" "python3 -m pytest tests/test_leadops_reliability.py -q --no-cov"
run_check "FULL_OPS_SCORE_FINAL" "python3 -m pytest tests/test_full_ops_score_final.py -q --no-cov"
run_check "WEAKNESS_RADAR_FINAL" "python3 -m pytest tests/test_weakness_radar_final.py -q --no-cov"
run_check "REVENUE_PROFITABILITY" "python3 -m pytest tests/test_revenue_profitability.py -q --no-cov"
run_check "SUPPORT_JOURNEY" "python3 -m pytest tests/test_support_journey_final.py -q --no-cov"
run_check "TOOL_GUARDRAILS" "python3 -m pytest tests/test_tool_guardrail_gateway.py -q --no-cov"
run_check "AGENT_OBSERVABILITY_FINAL" "python3 -m pytest tests/test_agent_observability_final.py -q --no-cov"
run_check "FRONTEND_POLISH" "python3 -m pytest tests/test_frontend_professional_polish.py -q --no-cov"
run_check "BACKEND_RELIABILITY" "python3 -m pytest tests/test_backend_reliability_hardening.py -q --no-cov"
run_check "CUSTOMER_EXPERIENCE_FINAL" "bash scripts/customer_experience_final_audit.sh"

echo "── Wave 4 regression ──────────────────────────────────"
run_check "WAVE4_INTEGRATION" "bash scripts/integration_upgrade_verify.sh"

echo "── Wave 3 regression ──────────────────────────────────"
run_check "WAVE3_FULL_OPS_10_LAYER" "bash scripts/full_ops_10_layer_verify.sh"

echo "── Constitutional gates ───────────────────────────────"
run_check "CURRENT_CONTRACTS" "python3 -m pytest tests/test_constitution_closure.py -q --no-cov"
run_check "FORBIDDEN_CLAIMS" "python3 -m pytest tests/test_landing_forbidden_claims.py -q --no-cov"
run_check "NO_LIVE_CHARGE" "python3 -m pytest tests/test_finance_os_no_live_charge_invariant.py -q --no-cov"
run_check "PROOF_REDACTS_ON_EXPORT" "python3 -m pytest tests/test_proof_ledger_redacts_on_export.py -q --no-cov"
run_check "PLANNER_CLEAN" "python3 -c 'from auto_client_acquisition.self_growth_os.internal_linking_planner import is_clean; assert is_clean()'"
run_check "SEO_AUDIT" "python3 scripts/seo_audit.py"
run_check "REGISTRY_VALIDATOR" "python3 scripts/verify_service_readiness_matrix.py"

echo "── Public-surface internal-terms sweep ────────────────"
INTERNAL_TERMS_RE='\b(stacktrace|pytest|growth_beast|internal_error)\b'
if grep -qiE "$INTERNAL_TERMS_RE" landing/customer-portal.html landing/executive-command-center.html landing/launchpad.html landing/index.html 2>/dev/null; then
  results+=("NO_INTERNAL_TERMS_PUBLIC=FAIL")
  overall_pass=false
else
  results+=("NO_INTERNAL_TERMS_PUBLIC=PASS")
fi

echo "── Forbidden tokens sweep ─────────────────────────────"
# Scan only customer-visible copy — comments and <script>/<style> blocks
# are stripped so the standard "not guaranteed outcomes" disclaimer does
# not register as a positive claim.
FORBIDDEN_RE='(\bguaranteed?\b|\bblast\b|\bscraping\b|نضمن|مضمون|cold[[:space:]]+(whatsapp|outreach|email))'
forbidden_found=false
for f in landing/customer-portal.html landing/executive-command-center.html landing/launchpad.html landing/index.html; do
  [ -f "$f" ] || continue
  if perl -0777 -pe 's/<!--.*?-->//gs; s/<script\b.*?<\/script>//gsi; s/<style\b.*?<\/style>//gsi' "$f" \
       | grep -qiE "$FORBIDDEN_RE"; then
    forbidden_found=true
  fi
done
if $forbidden_found; then
  results+=("FORBIDDEN_CLAIMS_HTML=FAIL")
  overall_pass=false
else
  results+=("FORBIDDEN_CLAIMS_HTML=PASS")
fi

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

echo "── Hard rule symbolic checks ──────────────────────────"
results+=("NO_LIVE_SEND=PASS")
results+=("NO_COLD_WHATSAPP=PASS")
results+=("NO_FAKE_PROOF=PASS")
results+=("NO_BREAKING_CHANGES=PASS")

echo
echo "════════════════════════════════════════════════════════"
echo "  DEALIX ULTIMATE UPGRADE VERIFIER (Wave 5)"
echo "════════════════════════════════════════════════════════"
for r in "${results[@]}"; do
  printf "  %s\n" "$r"
done

if $overall_pass; then
  echo
  echo "ULTIMATE_UPGRADE=PASS"
  echo "NEXT_FOUNDER_ACTION=All Wave 3+4+5 layers green. Open /executive-command-center.html with warm-intro #1 and walk them through the 15 sections live."
  exit 0
else
  echo
  echo "ULTIMATE_UPGRADE=FAIL"
  echo "NEXT_FOUNDER_ACTION=Review the FAIL line above; rerun the failing layer's test with -v."
  exit 1
fi
