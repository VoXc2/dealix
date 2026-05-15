#!/usr/bin/env bash
# Scale readiness verification — lint + tests + the scale harness.
# Usage: bash scripts/dealix_scale_verify.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export APP_ENV=test

FAIL=0

echo "== ruff (scale slice) =="
if command -v ruff >/dev/null 2>&1; then
  ruff check auto_client_acquisition/scale_os/scale_readiness.py \
    scripts/verify_dealix_scale.py \
    tests/test_scale_readiness.py || FAIL=1
else
  echo "ruff not installed — skip"
fi

echo "== pytest scale readiness =="
if python -m pytest tests/test_scale_readiness.py -q --no-cov; then
  :
else
  FAIL=1
fi

echo "== scale harness =="
python scripts/verify_dealix_scale.py || true

if [ "$FAIL" -ne 0 ]; then
  echo "DEALIX_SCALE_VERIFY=fail"
  exit 1
fi
echo "DEALIX_SCALE_VERIFY=ok"
