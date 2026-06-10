#!/usr/bin/env bash
# Soft Launch PASS → Paid Launch readiness (no Moyasar claim until FOUNDER_ACTION)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export APP_ENV=test

PYTHON_BIN="$(command -v python3 2>/dev/null || echo "py -3")"

echo "== founder_soft_to_paid_verify =="
echo ""

echo "== 1/3 Commercial strict (targeting >= 80) =="
$PYTHON_BIN "$ROOT/scripts/verify_commercial_launch_ready.py" --strict

echo ""
echo "== 2/3 Paid launch roadmap =="
$PYTHON_BIN "$ROOT/scripts/verify_paid_launch_readiness.py"

echo ""
echo "== 3/3 First paid Diagnostic pipeline =="
$PYTHON_BIN "$ROOT/scripts/verify_first_paid_diagnostic_tracker.py"

echo ""
echo "FOUNDER_SOFT_TO_PAID=ROADMAP_OK"
echo "Next: docs/commercial/PAID_LAUNCH_AFTER_SOFT_PASS_AR.md"
echo "Production: bash scripts/official_launch_verify.sh (Moyasar + Railway)"
