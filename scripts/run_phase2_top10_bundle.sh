#!/usr/bin/env bash
# Dealix 200 — Top 10 phase-2 verification bundle (initiative 200).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export DEALIX_INITIATIVE_TARGET=200
python3 scripts/verify_global_ai_transformation.py --check-initiatives
python3 scripts/report_initiative_coverage.py
APP_ENV=test pytest \
  tests/test_strategic_initiatives_registry.py \
  tests/test_dealix_200_phase2.py \
  tests/test_ai_unit_economics.py \
  tests/test_unified_readiness.py \
  tests/test_ltv_from_events.py \
  tests/test_grounding_score.py \
  tests/test_partner_sandbox.py \
  tests/test_customer_health_v2.py \
  -q --no-cov
echo "DEALIX_200_PHASE2_TOP10: PASS"
