#!/usr/bin/env bash
# Pre-scale gate bundle: category expansion YAML gates + CEO category_gates helper.
# Run before sector/regional expansion; see dealix/transformation/category_expansion_gates.yaml
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="$(command -v python3)"

bash "${ROOT}/scripts/verify_category_expansion_before_scale.sh"
bash "${ROOT}/scripts/verify_ceo_signal_readiness.sh" category_gates

echo ""
echo "PRE_SCALE_GATE_BUNDLE: PASS"
echo "Optional: bash scripts/verify_ceo_signal_readiness.sh all"
