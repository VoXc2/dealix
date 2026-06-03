#!/usr/bin/env bash
# CEO Master Plan — one-shot morning bundle (no external sends)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== CEO Master Plan Morning =="
python3 scripts/bootstrap_founder_kpi_import.py || true
python3 scripts/founder_daily_five_metrics.py
python3 scripts/run_ceo_master_plan_status.py
python3 scripts/verify_first_paid_diagnostic_tracker.py
python3 scripts/ceo_production_trust_bundle.py || true
