#!/usr/bin/env bash
# Master verifier for the Full-Ops 10-Layer Operating Spine.
#
# Runs every Phase 1-11 test file + the safety regression set + an
# emit summary table. Exits non-zero if any layer fails.
#
# Usage:
#   bash scripts/full_ops_10_layer_verify.sh
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

echo "── Phase 1 — Contracts ────────────────────────────────"
run_check "FULL_OPS_CONTRACTS" "python3 -m pytest tests/test_full_ops_contracts.py -q --no-cov"

echo "── Phase 2 — LeadOps Spine ────────────────────────────"
run_check "LEADOPS_SPINE" "python3 -m pytest tests/test_leadops_spine_golden_path.py -q --no-cov"

echo "── Phase 3 — Customer Brain ───────────────────────────"
run_check "CUSTOMER_BRAIN" "python3 -m pytest tests/test_customer_brain_full_ops.py -q --no-cov"

echo "── Phase 4 — Service Sessions ─────────────────────────"
run_check "SERVICE_SESSIONS" "python3 -m pytest tests/test_service_sessions_full_ops.py -q --no-cov"

echo "── Phase 5 — Approval Center ──────────────────────────"
run_check "APPROVAL_CENTER" "python3 -m pytest tests/test_approval_center.py tests/test_approval_center_extensions.py -q --no-cov"

echo "── Phase 6 — Proof Ledger ─────────────────────────────"
run_check "PROOF_LEDGER" "python3 -m pytest tests/test_proof_ledger_extensions.py tests/test_proof_ledger_redacts_on_export.py -q --no-cov"

echo "── Phase 7 — Support Inbox ────────────────────────────"
run_check "SUPPORT_INBOX" "python3 -m pytest tests/test_support_inbox_full_ops.py -q --no-cov"

echo "── Phase 8 — Executive Pack ───────────────────────────"
run_check "EXECUTIVE_PACK" "python3 -m pytest tests/test_executive_pack_full_ops.py -q --no-cov"

echo "── Phase 9 — Payment Ops ──────────────────────────────"
run_check "PAYMENT_OPS" "python3 -m pytest tests/test_payment_ops_full_ops.py -q --no-cov"

echo "── Phase 10 — Customer Portal Live ────────────────────"
run_check "CUSTOMER_PORTAL" "python3 -m pytest tests/test_customer_portal_live_full_ops.py tests/test_constitution_closure.py -q --no-cov"

echo "── Phase 11 — Case Study Engine ───────────────────────"
run_check "CASE_STUDY_ENGINE" "python3 -m pytest tests/test_case_study_engine_full_ops.py -q --no-cov"

echo "── Cross-cutting safety ───────────────────────────────"
run_check "FORBIDDEN_CLAIMS" "python3 -m pytest tests/test_landing_forbidden_claims.py -q --no-cov"
run_check "NO_LIVE_CHARGE_INVARIANT" "python3 -m pytest tests/test_finance_os_no_live_charge_invariant.py -q --no-cov"
run_check "PROOF_REDACTS_ON_EXPORT" "python3 -m pytest tests/test_proof_ledger_redacts_on_export.py -q --no-cov"
run_check "PLANNER_CLEAN" "python3 -c \"from auto_client_acquisition.self_growth_os.internal_linking_planner import is_clean; assert is_clean()\""
run_check "SEO_AUDIT" "python3 scripts/seo_audit.py"
run_check "REGISTRY_VALIDATOR" "python3 scripts/verify_service_readiness_matrix.py"

echo
echo "════════════════════════════════════════════════════════"
echo "  DEALIX FULL-OPS 10-LAYER VERIFIER"
echo "════════════════════════════════════════════════════════"
for r in "${results[@]}"; do
  printf "  %s\n" "$r"
done

if $overall_pass; then
  echo
  echo "DEALIX_FULL_OPS_10_LAYER_VERDICT=PASS"
  echo "NEXT_FOUNDER_ACTION=All gates green. Open the Operations Console (/customer-portal.html) and walk through the 5-warm-intro outreach for first paid pilot."
  exit 0
else
  echo
  echo "DEALIX_FULL_OPS_10_LAYER_VERDICT=FAIL"
  echo "NEXT_FOUNDER_ACTION=Review the FAIL line above; rerun the failing layer's pytest file with -v."
  exit 1
fi
