#!/usr/bin/env bash
# Dealix Master Strategy — unified verification bundle (merge-stack gate).
set -euo pipefail
cd "$(dirname "$0")/.."
export DEALIX_INITIATIVE_TARGET="${DEALIX_INITIATIVE_TARGET:-200}"

echo "=== Master Strategy Verify ==="
python3 scripts/verify_global_ai_transformation.py
python3 scripts/verify_global_ai_transformation.py --check-initiatives
python3 scripts/verify_os_tier_registry.py
python3 scripts/report_initiative_coverage.py
bash scripts/run_phase2_top10_bundle.sh
python3 scripts/check_alembic_single_head.py
echo "DEALIX_MASTER_STRATEGY_VERIFY: PASS"
