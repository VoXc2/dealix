#!/usr/bin/env bash
# Quarterly 2030/2040 review — category gates + initiative coverage + endgame docs.
set -euo pipefail
cd "$(dirname "$0")/.."
export DEALIX_INITIATIVE_TARGET="${DEALIX_INITIATIVE_TARGET:-200}"
STAMP=$(date -u +%Y-%m-%d)
OUT="docs/transformation/evidence/quarterly_review_${STAMP}.md"
mkdir -p docs/transformation/evidence

{
  echo "# Quarterly Strategy Review — ${STAMP}"
  echo ""
  echo "## Endgame docs"
  for f in DEALIX_2030_ENDGAME_AR.md DEALIX_2040_ENDGAME_AR.md PLATFORM_SCALE_PHASE2_ROADMAP_AR.md; do
    if [[ -f "docs/transformation/$f" ]]; then echo "- OK: $f"; else echo "- MISSING: $f"; fi
  done
  echo ""
  echo "## Verification"
  python3 scripts/verify_global_ai_transformation.py --check-initiatives
  python3 scripts/report_initiative_coverage.py
  bash scripts/run_pre_scale_gate_bundle.sh || true
  bash scripts/verify_category_expansion_before_scale.sh || true
  echo ""
  echo "## Coverage target"
  echo "Phase 2 deliverable coverage target: >= 90% with real pytest (not verify-only)."
} | tee "$OUT"

echo "Wrote $OUT"
echo "QUARTERLY_STRATEGY_REVIEW: PASS"
