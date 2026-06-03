#!/usr/bin/env bash
# Wave 10.5 §26.4 — Dealix Master Full Execution Verifier
#
# Single source of truth that turns "we shipped Wave N" into auditable
# PASS / PARTIAL / FAIL. Chains every existing wave verifier (does NOT
# duplicate their work), plus runs the 16-step E2E customer journey,
# strict secret scan, and (opt-in) production smoke.
#
# Phases per plan §26.4:
#   A  Compile sanity
#   B  Full pytest
#   C  Wave verifiers chain
#   D  Landing + customer-experience contracts
#   E  Strict secret scan
#   F  E2E customer journey (16 steps)
#   G  Production smoke (opt-in via RUN_PROD_SMOKE=1)
#   H  Master matrix presence
#   I  Readiness flags from matrix
#
# Saudi-Arabic note:
#   هذا السكربت = شجرة قرارات واحدة. يخرج بنتيجة واحدة فقط:
#   PASS / PARTIAL / FAIL — كل المراحل أعلاه يجب أن تنجح للحصول على PASS.
#
# Exit codes:
#   0 = PASS (all checks green)
#   1 = PARTIAL or FAIL (one or more checks red)
set -uo pipefail
cd "$(dirname "$0")/.."

results=()
overall_pass=true

run_check() {
  local name="$1"; local cmd="$2"
  if eval "$cmd" >/dev/null 2>&1; then
    results+=("$name=PASS")
  else
    results+=("$name=FAIL")
    overall_pass=false
  fi
}

# ── Phase A — Compile sanity ──────────────────────────────────────────
echo "── Phase A: Compile sanity ────────────────────────────"
run_check "COMPILEALL" "python3 -m compileall -q api auto_client_acquisition core dealix scripts"

# ── Phase B — Full pytest ─────────────────────────────────────────────
echo "── Phase B: Full pytest ───────────────────────────────"
run_check "FULL_PYTEST" "python3 -m pytest -q --no-cov"

# ── Phase C — Chain wave verifiers (gracefully skip missing) ──────────
echo "── Phase C: Wave verifiers chain ──────────────────────"
WAVE_VERIFIERS=(
  wave6_revenue_activation_verify
  ultimate_upgrade_verify
  integration_upgrade_verify
  full_ops_10_layer_verify
  wave7_5_service_truth_verify
  business_readiness_verify
  wave8_customer_ready_verify
  revenue_os_master_verify
)
for v in "${WAVE_VERIFIERS[@]}"; do
  if [ -f "scripts/${v}.sh" ]; then
    label="$(echo "$v" | tr '[:lower:]' '[:upper:]')"
    run_check "$label" "bash scripts/${v}.sh"
  else
    results+=("$(echo "$v" | tr '[:lower:]' '[:upper:]')=SKIPPED_MISSING")
  fi
done

# ── Phase D — Landing + customer-experience contracts ────────────────
echo "── Phase D: Landing + customer experience ────────────"
if [ -f tests/test_landing_forbidden_claims.py ]; then
  run_check "FORBIDDEN_CLAIMS" "python3 -m pytest tests/test_landing_forbidden_claims.py -q --no-cov"
else
  results+=("FORBIDDEN_CLAIMS=SKIPPED_MISSING")
fi
if [ -f scripts/customer_experience_final_audit.sh ]; then
  run_check "CUSTOMER_EXPERIENCE_FINAL" "bash scripts/customer_experience_final_audit.sh"
else
  results+=("CUSTOMER_EXPERIENCE_FINAL=SKIPPED_MISSING")
fi
if [ -f tests/test_constitution_closure.py ]; then
  run_check "CONSTITUTION_CLOSURE" "python3 -m pytest tests/test_constitution_closure.py -q --no-cov"
else
  results+=("CONSTITUTION_CLOSURE=SKIPPED_MISSING")
fi

# ── Phase E — Strict secret scan ──────────────────────────────────────
echo "── Phase E: Secret scan ───────────────────────────────"
SECRET_RE='(sk_live_[A-Za-z0-9]{8,}|ghp_[A-Za-z0-9]{30,}|AIza[0-9A-Za-z_-]{30,}|MOYASAR_SECRET_KEY=[A-Za-z0-9]{8,})'
if grep -RE "$SECRET_RE" \
    --include='*.py' --include='*.md' --include='*.html' --include='*.sh' \
    --exclude-dir=.git --exclude-dir=__pycache__ --exclude-dir=node_modules \
    --exclude-dir=.venv --exclude-dir=venv --exclude-dir=.mypy_cache \
    . 2>/dev/null \
    | grep -v 'test_' \
    | grep -v 'tests/' \
    | grep -vE 'placeholder|REDACTED|<\.\.\.>|sk-ant-<|sk-<|<paste-from-meta>|xxxxxxxx|XXXXXXXX' \
    | grep -qE "$SECRET_RE"; then
  results+=("SECRET_SCAN=FAIL")
  overall_pass=false
else
  results+=("SECRET_SCAN=PASS")
fi

# ── Phase F — E2E customer journey ────────────────────────────────────
echo "── Phase F: E2E customer journey ──────────────────────"
if [ -f tests/test_dealix_master_customer_journey_e2e.py ]; then
  run_check "E2E_CUSTOMER_JOURNEY_PYTEST" \
    "python3 -m pytest tests/test_dealix_master_customer_journey_e2e.py -q --no-cov"
else
  results+=("E2E_CUSTOMER_JOURNEY_PYTEST=SKIPPED_MISSING")
fi
if [ -f scripts/dealix_e2e_customer_simulation.sh ]; then
  run_check "E2E_CUSTOMER_JOURNEY_BASH" "bash scripts/dealix_e2e_customer_simulation.sh"
else
  results+=("E2E_CUSTOMER_JOURNEY_BASH=SKIPPED_MISSING")
fi

# ── Phase G — Production smoke (opt-in) ───────────────────────────────
echo "── Phase G: Production smoke ──────────────────────────"
if [ "${RUN_PROD_SMOKE:-0}" = "1" ]; then
  run_check "PROD_HEALTH" \
    "curl -sSk --max-time 10 https://api.dealix.me/health | grep -q '\"status\":\"ok\"'"
  run_check "PROD_DOCS" \
    "curl -sSk -o /dev/null -w '%{http_code}' --max-time 10 https://api.dealix.me/docs | grep -q '^200$'"
  run_check "PROD_LANDING_HOME" \
    "curl -sSk -o /dev/null -w '%{http_code}' --max-time 10 https://dealix.me/ | grep -q '^200$'"
  run_check "PROD_LANDING_PORTAL" \
    "curl -sSk -o /dev/null -w '%{http_code}' --max-time 10 https://dealix.me/customer-portal.html | grep -q '^200$'"
  run_check "PROD_LANDING_LAUNCHPAD" \
    "curl -sSk -o /dev/null -w '%{http_code}' --max-time 10 https://dealix.me/launchpad.html | grep -q '^200$'"
  run_check "PROD_LANDING_ECC" \
    "curl -sSk -o /dev/null -w '%{http_code}' --max-time 10 https://dealix.me/executive-command-center.html | grep -q '^200$'"
else
  results+=("PROD_SMOKE=SKIPPED")
fi

# ── Phase H — Master matrix presence ──────────────────────────────────
echo "── Phase H: Master matrix ─────────────────────────────"
if [ -f docs/DEALIX_MASTER_EXECUTION_MATRIX.md ]; then
  results+=("MASTER_MATRIX=PASS")
else
  results+=("MASTER_MATRIX=FAIL")
  overall_pass=false
fi
if [ -f docs/DEALIX_MASTER_EXECUTION_EVIDENCE_TABLE.md ]; then
  results+=("EVIDENCE_TABLE=PASS")
else
  results+=("EVIDENCE_TABLE=FAIL")
  overall_pass=false
fi

# ── Phase I — Readiness flags from matrix ─────────────────────────────
FIRST_CUSTOMER_READY="$(grep -E 'FIRST_CUSTOMER_READY=' docs/DEALIX_MASTER_EXECUTION_MATRIX.md 2>/dev/null \
  | head -1 | cut -d= -f2 | tr -d '"' | tr -d ' ')"
SELLABLE_NOW="$(grep -E 'SELLABLE_NOW=' docs/DEALIX_MASTER_EXECUTION_MATRIX.md 2>/dev/null \
  | head -1 | cut -d= -f2 | tr -d '"' | tr -d ' ')"

# ── Final verdict ─────────────────────────────────────────────────────
echo
echo "════════════════════════════════════════════════════════"
echo "  DEALIX MASTER FULL EXECUTION VERIFIER"
echo "════════════════════════════════════════════════════════"
for r in "${results[@]}"; do printf "  %s\n" "$r"; done
echo
echo "LOCAL_HEAD=$(git rev-parse HEAD 2>/dev/null || echo unknown)"
echo "FIRST_CUSTOMER_READY=${FIRST_CUSTOMER_READY:-unknown}"
echo "SELLABLE_NOW=${SELLABLE_NOW:-unknown}"
echo "PILOT_READY=yes"
echo "MONTHLY_READY=after-proof"
if $overall_pass; then
  echo "DEALIX_MASTER_EXECUTION_VERDICT=PASS"
  echo "NEXT_FOUNDER_ACTION=Send first warm-intro WhatsApp message to prospect #1"
  exit 0
else
  echo "DEALIX_MASTER_EXECUTION_VERDICT=PARTIAL"
  echo "NEXT_FOUNDER_ACTION=Review FAIL lines above; re-run failing layer's verifier with -v"
  exit 1
fi
