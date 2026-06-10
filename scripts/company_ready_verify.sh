#!/usr/bin/env bash
# Company ready verify — docs, commercial pytest, orchestrator imports.
# Usage:
#   bash scripts/company_ready_verify.sh
#   bash scripts/company_ready_verify.sh --docs-only
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export APP_ENV=test

DOCS_ONLY=0
SKIP_GO_LIVE=0
for arg in "$@"; do
  case "$arg" in
    --docs-only) DOCS_ONLY=1 ;;
    --skip-go-live) SKIP_GO_LIVE=1 ;;
  esac
done

PYTHON_BIN="$(command -v python3 2>/dev/null || true)"
if [[ -z "${PYTHON_BIN}" ]] && command -v py >/dev/null 2>&1; then
  PYTHON_BIN="py -3"
fi
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "COMPANY_READY: FAIL — python3 not found"
  exit 1
fi
FAIL=0

echo "== Company ready: required docs =="
REQUIRED_DOCS=(
  "docs/company/DEALIX_COMPANY_READY_MASTER_AR.md"
  "docs/commercial/DEALIX_UNIFIED_REVENUE_ATLAS_AR.md"
  "docs/commercial/DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md"
  "docs/commercial/DEALIX_COMPANY_DAILY_AUTOPILOT_AR.md"
  "docs/ops/FOUNDER_REVENUE_DAY_ONE_AR.md"
  "docs/ops/FOUNDER_OPERATING_SYSTEM_AR.md"
  "scripts/run_founder_revenue_day.sh"
  "scripts/run_founder_commercial_day.sh"
  "scripts/verify_dealix_commercial_go_live.sh"
  "scripts/official_launch_verify.sh"
  "scripts/railway_prod_bootstrap.sh"
  ".github/workflows/daily-revenue-machine.yml"
  ".github/workflows/founder_commercial_daily.yml"
  ".github/workflows/official-launch-verify.yml"
)
for f in "${REQUIRED_DOCS[@]}"; do
  if [[ -f "${ROOT}/${f}" ]]; then
    echo "  ok: ${f}"
  else
    echo "  MISSING: ${f}"
    FAIL=1
  fi
done

if [[ "$DOCS_ONLY" -eq 1 ]]; then
  if [[ "$FAIL" -eq 0 ]]; then
    echo "COMPANY_READY_VERDICT: PASS (docs-only)"
    exit 0
  fi
  echo "COMPANY_READY_VERDICT: FAIL (docs-only)"
  exit 1
fi

echo ""
echo "== Company ready: commercial_ops + orchestrator =="
if $PYTHON_BIN -c "
from dealix.commercial_ops.digest import build_commercial_digest
from dealix.revenue_ops_autopilot.orchestrator import get_default_orchestrator
get_default_orchestrator()
build_commercial_digest(skip_no_build=True)
"; then
  echo "  imports: PASS"
else
  echo "  imports: FAIL"
  FAIL=1
fi

echo ""
echo "== Company ready: commercial pytest slice =="
if $PYTHON_BIN -m pytest \
  tests/test_founder_commercial_digest.py \
  tests/test_founder_commercial_day_script.py \
  tests/test_generate_weekly_content_drafts.py \
  tests/test_company_ready_verify.py \
  tests/test_revenue_ops_autopilot.py \
  tests/test_commercial_objections.py \
  tests/test_gtm_commercial_stack.py \
  -q --no-cov; then
  echo "  pytest: PASS"
else
  echo "  pytest: FAIL"
  FAIL=1
fi

if [[ -n "${DEALIX_API_BASE:-}" ]]; then
  echo ""
  echo "== Company ready: production smoke (DEALIX_API_BASE) =="
  if $PYTHON_BIN "${ROOT}/scripts/prod_smoke_check.py" --base "${DEALIX_API_BASE}"; then
    echo "  prod_smoke: PASS"
  else
    echo "  prod_smoke: FAIL"
    FAIL=1
  fi
else
  echo ""
  echo "== Company ready: prod smoke skipped (set DEALIX_API_BASE for live check) =="
fi

if [[ "$SKIP_GO_LIVE" -ne 1 ]]; then
  echo ""
  echo "== Company ready: founder go-live (optional long) =="
  if bash "${ROOT}/scripts/founder_go_live_verify.sh"; then
    echo "  founder_go_live: PASS"
  else
    echo "  founder_go_live: FAIL (set --skip-go-live to ignore)"
    FAIL=1
  fi
fi

echo ""
if [[ "$FAIL" -eq 0 ]]; then
  echo "COMPANY_READY_VERDICT: PASS"
  echo "Next: bash scripts/run_founder_commercial_day.sh"
  echo "Go-live: bash scripts/verify_dealix_commercial_go_live.sh"
  echo "Doc: docs/company/DEALIX_COMPANY_READY_MASTER_AR.md"
  exit 0
fi
echo "COMPANY_READY_VERDICT: FAIL"
exit 1
