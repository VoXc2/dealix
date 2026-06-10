#!/usr/bin/env bash
# Run before sector/regional expansion motion (gates-only check).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-$(command -v python3 2>/dev/null || command -v py 2>/dev/null || true)}"
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "python3/py not found" >&2
  exit 1
fi
if [[ "${PYTHON_BIN}" == *py ]]; then
  PYTHON_BIN="py -3"
fi
"$PYTHON_BIN" "${ROOT}/scripts/verify_global_ai_transformation.py" --check-category-expansion
echo "CATEGORY_EXPANSION_GATES: PASS"
