#!/usr/bin/env bash
# Value Plan day — expand pool + snapshot + founder commercial loop
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

WAVE2=0
SKIP=0
for arg in "$@"; do
  case "$arg" in
    --wave2) WAVE2=1 ;;
    --skip-commercial-day) SKIP=1 ;;
  esac
done

PYTHON_BIN="$(command -v python3 2>/dev/null || echo "py -3")"

echo "== Dealix Value Plan Day =="
EXP_ARGS=()
[[ "$WAVE2" -eq 1 ]] && EXP_ARGS+=(--wave2)
$PYTHON_BIN "$ROOT/scripts/expand_commercial_ops_all.py" "${EXP_ARGS[@]}"

if [[ "$SKIP" -ne 1 ]]; then
  bash "$ROOT/scripts/run_founder_commercial_day.sh"
fi

$PYTHON_BIN "$ROOT/scripts/founder_paid_launch_gate.py"
echo "VALUE_PLAN_DAY=OK"
