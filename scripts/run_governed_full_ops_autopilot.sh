#!/usr/bin/env bash
# Governed full-ops autopilot — morning / evening / weekly (draft-only)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PYTHON_BIN="$(command -v python3 2>/dev/null || true)"
[[ -z "${PYTHON_BIN}" ]] && command -v py >/dev/null 2>&1 && PYTHON_BIN="py -3"
[[ -z "${PYTHON_BIN}" ]] && { echo "python not found"; exit 1; }

ARGS=()
case "${1:-morning}" in
  morning|--morning) ARGS+=(--morning) ;;
  evening|--evening) ARGS+=(--evening) ;;
  full|--full) ARGS+=(--full) ;;
  dry-run|--dry-run) ARGS+=(--dry-run) ;;
  *) ARGS+=(--morning) ;;
esac
shift || true
for a in "$@"; do
  case "$a" in
    --evening) ARGS+=(--evening) ;;
    --full) ARGS+=(--full) ;;
    --dry-run) ARGS+=(--dry-run) ;;
    --skip-gates) ARGS+=(--skip-gates) ;;
    --json) ARGS+=(--json) ;;
  esac
done

exec $PYTHON_BIN "$ROOT/scripts/run_governed_full_ops_autopilot.py" "${ARGS[@]}"
