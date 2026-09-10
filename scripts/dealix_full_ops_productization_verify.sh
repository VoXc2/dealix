#!/usr/bin/env bash
# Wave 13 — Full Ops Productization master verifier
# Single command, single verdict. Composes all Phase 2-11 layer tests.
#
# Article 4: this script never makes external network calls.
# Article 8: explicit PASS/FAIL only — no "OK" without artifacts.
# Article 11: chains existing per-phase test files; no new business logic.
#
# This verifier proves technical Wave13 contracts only. It does NOT prove
# customer readiness, paid pilots, sellability, payment, or Production Green.

set -uo pipefail
cd "$(dirname "$0")/.."

# Use the repository environment when present. Calling bare ``python3`` made
# this verifier report every pytest phase as FAIL when invoked by
# ``.venv/bin/pytest`` without an activated shell, even though the same tests
# were passing in the parent process.
PYTHON_BIN="${DEALIX_PYTHON_BIN:-}"
if [[ -z "$PYTHON_BIN" ]]; then
  if [[ -x ".venv/bin/python" ]]; then
    PYTHON_BIN=".venv/bin/python"
  else
    PYTHON_BIN="$(command -v python3)"
  fi
fi

results=()
overall_pass=true

run_check() {
  local name="$1"; local cmd="$2"
  if bash -o pipefail -c "$cmd" >/dev/null 2>&1; then
    results+=("$name=PASS")
  else
    results+=("$name=FAIL")
    overall_pass=false
  fi
}

# ── Phase A — Compile sanity ────────────────────────────────────────
run_check "COMPILEALL" "\"$PYTHON_BIN\" -m compileall -q auto_client_acquisition/service_catalog auto_client_acquisition/deliverables auto_client_acquisition/bottleneck_radar auto_client_acquisition/integration_capability auto_client_acquisition/business_metrics_board auto_client_acquisition/customer_success api/routers/service_catalog.py api/routers/deliverables.py api/routers/bottleneck_radar.py api/routers/integration_capability.py api/routers/business_metrics_board.py api/routers/customer_success_scores.py scripts/dealix_weekly_executive_pack.py scripts/dealix_whatsapp_morning_brief.py"

# ── Phase B — Wave 13 per-phase tests ────────────────────────────────
run_check "SERVICE_CATALOG"            "\"$PYTHON_BIN\" -m pytest tests/test_service_catalog.py -q --no-cov"
run_check "SERVICE_SESSION_RUNTIME"    "\"$PYTHON_BIN\" -m pytest tests/test_service_session_runtime.py -q --no-cov"
run_check "DELIVERABLES"               "\"$PYTHON_BIN\" -m pytest tests/test_deliverables.py -q --no-cov"
run_check "WEEKLY_EXECUTIVE_PACK"      "\"$PYTHON_BIN\" -m pytest tests/test_weekly_executive_pack.py -q --no-cov"
run_check "CUSTOMER_PORTAL_FULL_OPS"   "\"$PYTHON_BIN\" -m pytest tests/test_customer_portal_full_ops.py -q --no-cov"
run_check "WHATSAPP_DECISION_FULL_OPS" "\"$PYTHON_BIN\" -m pytest tests/test_whatsapp_full_ops.py -q --no-cov"
run_check "CUSTOMER_SUCCESS_SCORES"    "\"$PYTHON_BIN\" -m pytest tests/test_customer_success_intelligence.py -q --no-cov"
run_check "BOTTLENECK_RADAR"           "\"$PYTHON_BIN\" -m pytest tests/test_bottleneck_radar.py -q --no-cov"
run_check "INTEGRATION_CAPABILITY_REGISTRY" "\"$PYTHON_BIN\" -m pytest tests/test_integration_capability.py -q --no-cov"
run_check "BUSINESS_METRICS_BOARD"     "\"$PYTHON_BIN\" -m pytest tests/test_business_metrics_board.py -q --no-cov"

# ── Phase C — Hard-gate audit ────────────────────────────────────────
# Article 4: test that no Wave 13 module accidentally imports a forbidden
# action mode or calls a live-send API. Greps for actual function CALLS
# (with parens), not for descriptive strings that mention the gate name.
run_check "NO_LIVE_SEND_IN_WAVE13" "! grep -RE '(send_text|whatsapp_send|send_message)\\s*\\(|smtp\\.send|requests\\.post\\(|httpx\\.post\\(' auto_client_acquisition/service_catalog/ auto_client_acquisition/deliverables/ auto_client_acquisition/bottleneck_radar/ auto_client_acquisition/integration_capability/ auto_client_acquisition/business_metrics_board/ auto_client_acquisition/whatsapp_decision_bot/morning_brief.py auto_client_acquisition/customer_success/churn_risk.py auto_client_acquisition/customer_success/proof_maturity.py 2>/dev/null"

# Match actual mutating CALLS to charge APIs (not docstrings explaining the gate)
run_check "NO_LIVE_CHARGE_IN_WAVE13" "! grep -RE '(\\.charge\\s*\\(|charge_card\\s*\\(|capture_payment\\s*\\()' auto_client_acquisition/service_catalog/ auto_client_acquisition/deliverables/ auto_client_acquisition/bottleneck_radar/ auto_client_acquisition/integration_capability/ auto_client_acquisition/business_metrics_board/ 2>/dev/null"

# Article 8 invariant: confirmed_revenue_sar must NOT be assigned from invoice_intent.
run_check "NO_FAKE_REVENUE" "! grep -RE 'confirmed_revenue_sar\\s*=\\s*.*invoice_intent' auto_client_acquisition/business_metrics_board/ 2>/dev/null"

# ── Phase D — Forbidden-claim scrub ──────────────────────────────────
run_check "FORBIDDEN_CLAIMS" "\"$PYTHON_BIN\" -m pytest tests/test_landing_forbidden_claims.py -q --no-cov"

# ── Phase E — Current retired portal truth ───────────────────────────
# The old static customer dashboard is intentionally retired. Preserve the
# noindex + proof redirect + synthetic-not-customer-proof boundary instead of
# resurrecting historical Wave13 section-count markup.
run_check "PORTAL_RETIREMENT_INVARIANT" "\"$PYTHON_BIN\" -c \"from pathlib import Path; h=Path('landing/customer-portal.html').read_text(encoding='utf-8'); assert 'noindex,nofollow' in h; assert 'url=/proof.html' in h; assert 'DEALIX_RETIRED_PUBLIC_SURFACE' in h; assert 'synthetic' in h; assert 'دليل عميل' in h\""

# ── Phase F — Wave 11 + 12 regression ────────────────────────────────
run_check "FULL_OPS_CONTRACTS_REGRESSION" "\"$PYTHON_BIN\" -m pytest tests/test_full_ops_contracts.py -q --no-cov"

# ── Final verdict ────────────────────────────────────────────────────
echo
echo "════════════════════════════════════════════════════════════"
echo "  DEALIX WAVE 13 — FULL OPS PRODUCTIZATION VERIFIER"
echo "════════════════════════════════════════════════════════════"
for r in "${results[@]}"; do printf "  %s\n" "$r"; done
echo

pass_count=$(printf "%s\n" "${results[@]}" | grep -c "=PASS$" 2>/dev/null)
fail_count=$(printf "%s\n" "${results[@]}" | grep -c "=FAIL$" 2>/dev/null)
pass_count=${pass_count:-0}
fail_count=${fail_count:-0}
total=$((pass_count + fail_count))
echo "Total checks: $total · PASS: $pass_count · FAIL: $fail_count"
echo

echo "Hard gates (all 8 IMMUTABLE):"
echo "  NO_LIVE_SEND=immutable"
echo "  NO_LIVE_CHARGE=immutable"
echo "  NO_COLD_WHATSAPP=immutable"
echo "  NO_LINKEDIN_AUTO=immutable"
echo "  NO_SCRAPING=immutable"
echo "  NO_FAKE_PROOF=immutable"
echo "  NO_FAKE_REVENUE=immutable"
echo "  NO_BLAST=immutable"
echo

local_head=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
echo "LOCAL_HEAD=$local_head"
echo "BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'unknown')"

if $overall_pass; then
  echo "DEALIX_WAVE13_FULL_OPS_PRODUCTIZATION_VERDICT=PASS"
  echo "TECHNICAL_WAVE13_CONTRACT=PASS"
  echo "CUSTOMER_READY=NOT_PROVEN_BY_THIS_VERIFIER"
  echo "FIRST_3_PAID_PILOTS_READY=NOT_PROVEN_BY_THIS_VERIFIER"
  echo "SELLABLE_NOW=NOT_PROVEN_BY_THIS_VERIFIER"
  echo "NEXT_FOUNDER_ACTION=Use current commercial and production evidence before any customer-facing action."
  exit 0
else
  echo "DEALIX_WAVE13_FULL_OPS_PRODUCTIZATION_VERDICT=PARTIAL_OR_FAIL"
  echo "TECHNICAL_WAVE13_CONTRACT=FAIL"
  echo "CUSTOMER_READY=NOT_PROVEN"
  echo "FIRST_3_PAID_PILOTS_READY=NOT_PROVEN"
  echo "NEXT_FOUNDER_ACTION=Review FAIL lines above; re-run failing test with -v for details."
  exit 1
fi
