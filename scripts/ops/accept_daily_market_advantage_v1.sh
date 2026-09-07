#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
EXPECTED="${1:-${DEALIX_EXPECTED_SHA:-}}"
PY="${DEALIX_AUTOMATION_PYTHON:-python3}"

if [[ -z "$EXPECTED" ]]; then
  echo "DEALIX_DAILY_MARKET_ADVANTAGE_ACCEPTANCE=FAIL: expected SHA required"
  exit 2
fi

if ! [[ "$EXPECTED" =~ ^[0-9a-f]{40}$ ]]; then
  echo "DEALIX_DAILY_MARKET_ADVANTAGE_ACCEPTANCE=FAIL: expected SHA must be 40 lowercase hex chars"
  exit 2
fi

ACTUAL="$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || true)"
if [[ "$ACTUAL" != "$EXPECTED" ]]; then
  echo "DEALIX_DAILY_MARKET_ADVANTAGE_ACCEPTANCE=FAIL: exact-head mismatch"
  echo "expected_sha=$EXPECTED"
  echo "actual_sha=${ACTUAL:-UNKNOWN}"
  exit 3
fi

for path in \
  data/commercial/daily_market_advantage_v1.json \
  scripts/commercial/run_daily_market_advantage_v1.py \
  scripts/verify_daily_market_advantage_v1.py; do
  [[ -f "$ROOT/$path" ]] || {
    echo "DEALIX_DAILY_MARKET_ADVANTAGE_ACCEPTANCE=FAIL: missing $path"
    exit 4
  }
done

"$PY" -m json.tool "$ROOT/data/commercial/daily_market_advantage_v1.json" >/dev/null
"$PY" -m py_compile \
  "$ROOT/scripts/commercial/run_daily_market_advantage_v1.py" \
  "$ROOT/scripts/verify_daily_market_advantage_v1.py"
"$PY" "$ROOT/scripts/verify_daily_market_advantage_v1.py"

echo "DEALIX_DAILY_MARKET_ADVANTAGE_ACCEPTANCE=PASS"
echo "source_sha=$ACTUAL"
echo "external_send=false"
echo "spend=false"
echo "production_mutation=false"
echo "new_scheduler=false"
echo "new_permanent_agent=false"
