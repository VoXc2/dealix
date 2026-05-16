#!/usr/bin/env bash
# Run before sector/regional expansion motion (gates-only check).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="$(command -v python3)"
"$PYTHON_BIN" "${ROOT}/scripts/verify_global_ai_transformation.py" --check-category-expansion
echo "CATEGORY_EXPANSION_GATES: PASS"
