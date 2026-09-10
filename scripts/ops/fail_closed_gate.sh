#!/usr/bin/env bash
set -Eeuo pipefail

# Run one required acceptance command and emit PASS only when its real exit code
# is zero. This wrapper exists to make false-green labels structurally hard to
# produce in ad-hoc VPS/CI orchestration.
#
# Usage:
#   scripts/ops/fail_closed_gate.sh PYTHON_TESTS python -m pytest -q
#   scripts/ops/fail_closed_gate.sh WEB_ACCEPTANCE npm --prefix apps/web run verify

if [[ $# -lt 2 ]]; then
  echo "usage: $0 LABEL COMMAND [ARG ...]" >&2
  exit 64
fi

label="$1"
shift

if [[ ! "$label" =~ ^[A-Z][A-Z0-9_]*$ ]]; then
  echo "INVALID_GATE_LABEL=$label" >&2
  exit 64
fi

set +e
"$@"
rc=$?
set -e

if (( rc != 0 )); then
  printf '%s=FAIL rc=%d\n' "$label" "$rc" >&2
  exit "$rc"
fi

printf '%s=PASS\n' "$label"
