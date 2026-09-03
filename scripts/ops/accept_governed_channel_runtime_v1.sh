#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

PYTHON_BIN="${DEALIX_AUTOMATION_PYTHON:-${ROOT}/.venv/bin/python}"
if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="$(command -v python3 || true)"
fi
[[ -n "$PYTHON_BIN" && -x "$PYTHON_BIN" ]] || {
  echo "GOVERNED_CHANNEL_RUNTIME_ACCEPTANCE_FAIL: python runtime unavailable" >&2
  exit 2
}

"$PYTHON_BIN" -m py_compile \
  scripts/verify_governed_channel_runtime_v1.py \
  scripts/ops/dealix_slack_founder_bridge.py \
  scripts/ops/verify_slack_founder_bridge_receipt.py \
  tests/test_governed_channel_runtime_v1.py \
  tests/test_slack_founder_bridge_policy_v2.py

bash -n scripts/ops/install_slack_founder_bridge_v2.sh

"$PYTHON_BIN" scripts/verify_governed_channel_runtime_v1.py
"$PYTHON_BIN" -m pytest -q \
  tests/test_governed_channel_runtime_v1.py \
  tests/test_slack_founder_bridge_policy_v2.py

if git rev-parse --git-dir >/dev/null 2>&1; then
  git diff --check
fi

echo "GOVERNED_CHANNEL_RUNTIME_ACCEPTANCE_PASS"
