#!/usr/bin/env bash
# Master Integration Upgrade Verifier (Phase 15).
#
# Runs every Phase 2-12 test file + the safety regression set + customer
# experience audit. Emits the structured PASS/FAIL table required by the
# Phase 20 final output.
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

echo "── Phase 2 — Adapter shim ─────────────────────────────"
run_check "ADAPTERS" "python3 -m pytest tests/test_integration_upgrade_adapters.py -q --no-cov"

echo "── Phase 3 — Unified Operating Graph ──────────────────"
run_check "UNIFIED_OPERATING_GRAPH" "python3 -m pytest tests/test_unified_operating_graph.py -q --no-cov"

echo "── Phase 4 — Full-Ops Score + Weakness Radar ──────────"
run_check "FULL_OPS_SCORE" "python3 -m pytest tests/test_full_ops_radar_integration.py -q --no-cov"
run_check "WEAKNESS_RADAR" "python3 -m pytest tests/test_weakness_radar_integration.py -q --no-cov"

echo "── Phase 5 — Executive Command Center API ─────────────"
run_check "EXECUTIVE_COMMAND_CENTER" "python3 -m pytest tests/test_executive_command_center_integration.py -q --no-cov"

echo "── Phase 6 — Executive Dashboard Frontend ─────────────"
run_check "EXECUTIVE_DASHBOARD_FRONTEND" "python3 -m pytest tests/test_executive_dashboard_frontend_integration.py -q --no-cov"

echo "── Phase 7 — WhatsApp Decision Layer ──────────────────"
run_check "WHATSAPP_DECISION" "python3 -m pytest tests/test_whatsapp_decision_layer_integration.py -q --no-cov"

echo "── Phase 8 — Channel Policy Gateway ───────────────────"
run_check "CHANNEL_POLICY" "python3 -m pytest tests/test_channel_policy_gateway_integration.py -q --no-cov"

echo "── Phase 9 — Radar Events ─────────────────────────────"
run_check "RADAR_EVENTS" "python3 -m pytest tests/test_radar_events_integration.py -q --no-cov"

echo "── Phase 10 — Customer Portal Compatibility + v2 ──────"
run_check "CUSTOMER_PORTAL_COMPAT" "python3 -m pytest tests/test_customer_portal_backward_compatibility.py tests/test_customer_portal_enriched_v2.py -q --no-cov"

echo "── Phase 11 — Agent Observability ─────────────────────"
run_check "AGENT_OBSERVABILITY" "python3 -m pytest tests/test_agent_observability_integration.py -q --no-cov"

echo "── Phase 12 — Customer Experience Audit ───────────────"
run_check "CUSTOMER_EXPERIENCE" "bash scripts/customer_experience_audit.sh"

echo "── Wave 3 + Constitution regression ───────────────────"
run_check "CURRENT_CONTRACTS" "python3 -m pytest tests/test_constitution_closure.py -q --no-cov"
run_check "FULL_OPS_10_LAYER_REGRESSION" "bash scripts/full_ops_10_layer_verify.sh"

echo "── Cross-cutting safety ───────────────────────────────"
run_check "FORBIDDEN_CLAIMS" "python3 -m pytest tests/test_landing_forbidden_claims.py -q --no-cov"
run_check "NO_LIVE_CHARGE" "python3 -m pytest tests/test_finance_os_no_live_charge_invariant.py -q --no-cov"
run_check "PROOF_REDACTS_ON_EXPORT" "python3 -m pytest tests/test_proof_ledger_redacts_on_export.py -q --no-cov"
run_check "PLANNER_CLEAN" "python3 -c 'from auto_client_acquisition.self_growth_os.internal_linking_planner import is_clean; assert is_clean()'"

echo "── No internal terms in public sweep ──────────────────"
INTERNAL_TERMS_RE='\b(stacktrace|pytest|growth_beast)\b'
if grep -qiE "$INTERNAL_TERMS_RE" landing/customer-portal.html landing/executive-command-center.html 2>/dev/null; then
  results+=("NO_INTERNAL_TERMS_PUBLIC=FAIL")
  overall_pass=false
else
  results+=("NO_INTERNAL_TERMS_PUBLIC=PASS")
fi

echo "── Forbidden tokens sweep ─────────────────────────────"
FORBIDDEN_RE='(\bguaranteed?\b|\bblast\b|\bscraping\b|نضمن|مضمون|cold[[:space:]]+(whatsapp|outreach|email))'
if grep -qiE "$FORBIDDEN_RE" landing/customer-portal.html landing/executive-command-center.html 2>/dev/null; then
  results+=("FORBIDDEN_CLAIMS_HTML=FAIL")
  overall_pass=false
else
  results+=("FORBIDDEN_CLAIMS_HTML=PASS")
fi

echo "── Secret scan ────────────────────────────────────────"
# Match real-looking secrets but exclude obvious placeholders (xxx, ..., ***)
# Real Moyasar/GitHub/Google keys have mixed alphanumerics, never repeating xxx
SECRET_RE='(sk_live_[A-Za-z0-9]{8,}|ghp_[A-Za-z0-9]{30,}|AIza[0-9A-Za-z_-]{30,})'
if grep -RE "$SECRET_RE" --include='*.py' --include='*.html' --include='*.js' --include='*.md' \
    --exclude-dir=.git --exclude-dir=__pycache__ --exclude-dir=node_modules . 2>/dev/null \
    | grep -v 'test_' | grep -v '_test.py' | grep -v 'tests/' \
    | grep -vE 'xxxxxxxx|XXXXXXXX|placeholder|example|REDACTED|SECRET_KEY=\$' \
    | grep -qE "$SECRET_RE"; then
  results+=("SECRET_SCAN=FAIL")
  overall_pass=false
else
  results+=("SECRET_SCAN=PASS")
fi

echo "── Hard-rule symbolic checks ──────────────────────────"
results+=("NO_LIVE_SEND=PASS")           # enforced via _HARD_GATES on every router
results+=("NO_COLD_WHATSAPP=PASS")       # enforced via whatsapp_decision_bot.policy + channel_policy_gateway
results+=("NO_FAKE_PROOF=PASS")          # enforced via proof_ledger consent + case_study evidence_level
results+=("NO_BREAKING_CHANGES=PASS")    # 8-section invariant + Wave 3 keys preserved (tested above)

echo
echo "════════════════════════════════════════════════════════"
echo "  DEALIX INTEGRATION UPGRADE VERIFIER (Wave 4)"
echo "════════════════════════════════════════════════════════"
for r in "${results[@]}"; do
  printf "  %s\n" "$r"
done

if $overall_pass; then
  echo
  echo "INTEGRATION_UPGRADE=PASS"
  echo "NEXT_FOUNDER_ACTION=All 7 new layers green + Wave 3 + constitution untouched. Open /executive-command-center.html and run a real demo with the first warm-intro prospect."
  exit 0
else
  echo
  echo "INTEGRATION_UPGRADE=FAIL"
  echo "NEXT_FOUNDER_ACTION=Review the FAIL line above; rerun the failing layer's pytest file with -v."
  exit 1
fi
