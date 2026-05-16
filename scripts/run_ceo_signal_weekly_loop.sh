#!/usr/bin/env bash
# Weekly CEO operating loop: emit dated Weekly Proof Pack markdown under docs/transformation/evidence/
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="$(command -v python3)"
DATE="$(date -u +%Y-%m-%d)"
OUT="${ROOT}/docs/transformation/evidence/weekly_proof_${DATE}.md"
mkdir -p "${ROOT}/docs/transformation/evidence"
"$PYTHON_BIN" "${ROOT}/scripts/generate_weekly_operating_proof_pack.py" --repo-root "$ROOT" --out "$OUT"
echo "CEO weekly proof pack written: $OUT"
echo "Reference taxonomy: dealix/transformation/ceo_signal_os.yaml"
echo "Next: refresh numeric baselines in dealix/transformation/kpi_baselines.yaml (source_ref required)."
echo "Gates: bash scripts/verify_ceo_signal_readiness.sh  |  bash scripts/verify_global_ai_transformation.sh"
