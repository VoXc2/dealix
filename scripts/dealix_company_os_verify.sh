#!/usr/bin/env bash
# Unified Company OS verifier.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

OVERALL_OK=1

echo "== [1/3] revenue_execution_verify =="
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
echo "== [3/3] beast_level_verify =="
if bash scripts/beast_level_verify.sh; then
  echo "BEAST_OK=pass"
else
  echo "BEAST_OK=fail"
  OVERALL_OK=0
fi

echo ""
if [[ $OVERALL_OK -eq 1 ]]; then
  echo "DEALIX_COMPANY_OS=PASS"
else
  echo "DEALIX_COMPANY_OS=FAIL"
fi

if [[ $OVERALL_OK -eq 1 ]]; then
  exit 0
else
  exit 1
fi
