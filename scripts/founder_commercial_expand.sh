#!/usr/bin/env bash
# Expand commercial ops — expand_commercial_ops_all + gates
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PYTHON_BIN="${PYTHON_BIN:-python3}"
MIN_ROWS=120
WAVE2=0
WAVE3=0
WAVE4=0
FULL=0
SKIP_GO_LIVE=0
DRY_RUN=0
for arg in "$@"; do
  case "$arg" in
    --min-rows=*) MIN_ROWS="${arg#*=}" ;;
    --wave2) WAVE2=1 ;;
    --wave3) WAVE3=1 ;;
    --skip-go-live) SKIP_GO_LIVE=1 ;;
    --dry-run) DRY_RUN=1 ;;
  esac
done

echo "== founder_commercial_expand (all angles) =="

EXPAND_ARGS=(
  "$PYTHON_BIN" "$ROOT/scripts/expand_commercial_ops_all.py"
  --cycle-weeks 28 --meetings 10 --touch-drafts 15 --enrich-warm
)
if [[ "$WAVE4" -eq 1 ]]; then
  EXPAND_ARGS+=(--wave4)
elif [[ "$WAVE3" -eq 1 ]]; then
  EXPAND_ARGS+=(--wave3)
elif [[ "$WAVE2" -eq 1 ]]; then
  EXPAND_ARGS+=(--wave2)
else
  EXPAND_ARGS+=(--min-rows "$MIN_ROWS")
fi
if [[ "$DRY_RUN" -eq 1 ]]; then
  EXPAND_ARGS+=(--skip-import --skip-war-room)
fi

echo "== 1/4 expand_commercial_ops_all =="
"${EXPAND_ARGS[@]}"

echo ""
echo "== 2/4 Expansion status =="
"$PYTHON_BIN" "$ROOT/scripts/founder_expansion_status.py"

echo ""
echo "== 3/4 Gates =="
"$PYTHON_BIN" "$ROOT/scripts/verify_commercial_launch_ready.py" --strict
"$PYTHON_BIN" "$ROOT/scripts/verify_commercial_fe_be.py"
bash "$ROOT/scripts/founder_soft_to_paid_verify.sh"

if [[ "$SKIP_GO_LIVE" -eq 0 ]]; then
  echo ""
  echo "== 4/4 Unified go-live =="
  bash "$ROOT/scripts/verify_dealix_commercial_go_live.sh"
else
  echo ""
  echo "== 4/4 Unified go-live (skipped) =="
fi

echo ""
echo "FOUNDER_COMMERCIAL_EXPAND=OK"
