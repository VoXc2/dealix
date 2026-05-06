#!/usr/bin/env bash
# Unified Company OS verification: RX (V11+V12+pytest) + Company Growth Beast.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

OVERALL_OK=1

echo "== [1/3] revenue_execution_verify (RX bundle + V11 + V12) =="
if bash scripts/revenue_execution_verify.sh; then
  echo "RX_OK=pass"
else
  echo "RX_OK=fail"
  OVERALL_OK=0
fi

echo ""
echo "== [2/3] company_growth_beast_verify =="
if bash scripts/company_growth_beast_verify.sh; then
  echo "CGB_OK=pass"
else
  echo "CGB_OK=fail"
  OVERALL_OK=0
fi

echo ""
echo "== [3/3] beast_level_verify (V12.5 closure) =="
if bash scripts/beast_level_verify.sh; then
  echo "BEAST_OK=pass"
else
  echo "BEAST_OK=fail"
  OVERALL_OK=0
fi

echo ""
if [[ $OVERALL_OK -eq 1 ]]; then
  echo "DEALIX_COMPANY_OS=PASS"
  echo "DEALIX_BEAST_LEVEL=PASS"
  echo "COMPANY_SERVICE_ROUTER=verify_via_RX_tests_if_listed"
else
  echo "DEALIX_COMPANY_OS=FAIL"
  echo "DEALIX_BEAST_LEVEL=FAIL"
fi
echo "NEXT_FOUNDER_ACTION=Merge to main if branch open; curl api.dealix.me/health; warm intros + diagnostics."

# OVERALL_OK=1 means success → shell exit 0
if [[ $OVERALL_OK -eq 1 ]]; then exit 0; else exit 1; fi
