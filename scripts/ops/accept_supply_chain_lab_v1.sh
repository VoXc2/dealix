#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

export TZ="${TZ:-Asia/Riyadh}"
export LC_ALL="${LC_ALL:-C.UTF-8}"
export LANG="${LANG:-C.UTF-8}"
export GH_PROMPT_DISABLED=1
export GIT_TERMINAL_PROMPT=0

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
EXPECTED="${DEALIX_EXPECTED_SHA:-${1:-}}"

ACTUAL="$(git -c safe.directory="$ROOT" -C "$ROOT" rev-parse HEAD 2>/dev/null || true)"

if [[ -z "$ACTUAL" ]]; then
  echo "DEALIX_SUPPLY_CHAIN_LAB_ACCEPTANCE=FAIL"
  echo "reason=exact_head_unreadable"
  exit 2
fi

if [[ -n "$EXPECTED" && "$ACTUAL" != "$EXPECTED" ]]; then
  echo "DEALIX_SUPPLY_CHAIN_LAB_ACCEPTANCE=FAIL"
  echo "reason=exact_head_mismatch"
  echo "expected=$EXPECTED"
  echo "actual=$ACTUAL"
  exit 3
fi

PY="${DEALIX_AUTOMATION_PYTHON:-}"
if [[ -z "$PY" || ! -x "$PY" ]]; then
  for candidate in "$ROOT/.venv/bin/python" "$(command -v python3 2>/dev/null || true)"; do
    if [[ -n "$candidate" && -x "$candidate" ]]; then
      PY="$candidate"
      break
    fi
  done
fi

if [[ -z "$PY" || ! -x "$PY" ]]; then
  echo "DEALIX_SUPPLY_CHAIN_LAB_ACCEPTANCE=FAIL"
  echo "reason=python_unavailable"
  exit 4
fi

"$PY" "$ROOT/scripts/ops/verify_supply_chain_lab_v1.py"
"$PY" -m py_compile "$ROOT/scripts/ops/verify_supply_chain_lab_v1.py"
bash -n "$ROOT/scripts/ops/bootstrap_supply_chain_lab_v1.sh"
bash -n "$ROOT/scripts/ops/run_supply_chain_evidence_v1.sh"

if "$PY" -m pytest --version >/dev/null 2>&1; then
  "$PY" -m pytest -q \
    "$ROOT/tests/test_supply_chain_lab_v1.py" \
    "$ROOT/tests/test_market_signal_sources_v3.py"
else
  echo "PYTEST=HOLD_UNAVAILABLE"
fi

python3 - "$ROOT/config/oss/supply_chain_lab_v1.json" <<'PY'
import json,sys
p=sys.argv[1]
d=json.load(open(p,encoding='utf-8'))
a=d['authority']
assert a['isolated_lab_only'] is True
assert a['reject_duplicate_by_default'] is True
assert a['promotion_requires_benchmark'] is True
for key in ('production_runtime','production_mutation','deployment_authority','network_target_scanning','customer_effects'):
    assert a[key] is False, key
print('AUTHORITY_FAIL_CLOSED=PASS')
PY

echo "DEALIX_SUPPLY_CHAIN_LAB_ACCEPTANCE=PASS"
echo "source_sha=$ACTUAL"
echo "runtime_scan_executed=false"
echo "production_install=false"
echo "production_mutation=false"
echo "dependency_mutation=false"
echo "customer_effects=false"
echo "safe_directory_scope=process_exact_repo_only"
