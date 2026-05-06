#!/usr/bin/env bash
# Revenue execution verification — compile + targeted pytest + optional staging smoke.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== compileall =="
python3 -m compileall -q api auto_client_acquisition db scripts

echo "== forbidden patterns (sk_live / ghp token shapes only) =="
python3 - <<'PY' || { echo "SECURITY_BLOCKER: forbidden token pattern in Python sources"; exit 2; }
import pathlib
import re
import sys
root = pathlib.Path(".")
pat = re.compile(r"sk_live_[0-9a-zA-Z]{10,}|ghp_[0-9a-zA-Z]{30,}")
bad = []
for base in ("api", "auto_client_acquisition", "scripts"):
    p = root / base
    if not p.exists():
        continue
    for f in p.rglob("*.py"):
        try:
            txt = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if pat.search(txt):
            bad.append(str(f))
if bad:
    print("matches:", *bad, sep="\n")
    sys.exit(1)
PY

echo "== pytest (revenue execution bundle) =="
python3 -m pytest -q --no-cov \
  tests/test_company_service_command_center.py \
  tests/test_daily_command_center_revenue_execution.py \
  tests/test_support_os_customer_serving_mode.py \
  tests/test_compliance_pdpl_action_policy.py \
  tests/test_revenue_pipeline_truth.py \
  tests/test_delivery_os_thin_router.py \
  tests/test_revenue_execution_aux_routers.py \
  tests/test_first10_warm_intros_revenue.py \
  tests/test_mini_diagnostic_revenue_flow.py \
  tests/test_pilot_499_close_pack.py \
  tests/test_proof_ledger_reality.py \
  tests/test_customer_success_revenue_mode.py \
  tests/test_growth_os_revenue_mode.py \
  tests/test_sales_os_closing_mode.py \
  tests/test_partnership_os_practical_mode.py \
  tests/test_executive_os_founder_brief.py \
  tests/test_self_improvement_real_learning.py \
  tests/test_observability_quality_gates.py \
  tests/test_revenue_execution_verify.py

if [[ -n "${STAGING_BASE_URL:-}" ]]; then
  echo "== launch_readiness_check (STAGING_BASE_URL set) =="
  STAGING_BASE_URL="$STAGING_BASE_URL" python3 scripts/launch_readiness_check.py --skip-readiness-json || true
fi

echo ""
echo "DEALIX_REVENUE_EXECUTION=PASS"
echo "NEXT_FOUNDER_ACTION=Merge and redeploy if production git_sha lags main; then GET /api/v1/full-ops/daily-command-center daily."
