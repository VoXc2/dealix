#!/usr/bin/env bash
# Master orchestrator: Launch Execution Railway plan (A–D).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SKIP_BOOTSTRAP="${SKIP_BOOTSTRAP:-0}"
SKIP_VERIFY="${SKIP_VERIFY:-0}"
SKIP_WARM="${SKIP_WARM:-0}"
SKIP_REVENUE_DAY="${SKIP_REVENUE_DAY:-0}"
ALLOW_REPLACE_TOP="${ALLOW_REPLACE_TOP:-1}"

echo "=== A: Railway env check ==="
python3 scripts/railway_launch_env_check.py || true

if [[ "$SKIP_BOOTSTRAP" != "1" ]] && [[ -n "${DATABASE_URL:-}" ]]; then
  echo "=== A4: Production bootstrap ==="
  bash scripts/railway_prod_bootstrap.sh
else
  echo "SKIP bootstrap (set DATABASE_URL to run)"
fi

if [[ "$SKIP_VERIFY" != "1" ]]; then
  echo "=== B: Official launch verify ==="
  bash scripts/official_launch_verify.sh
fi

if [[ "$SKIP_WARM" != "1" ]]; then
  echo "=== C: Warm CSV validation ==="
  extra=()
  if [[ "$ALLOW_REPLACE_TOP" == "1" ]]; then
    extra+=(--max-replace-top 99)
  fi
  python3 scripts/validate_warm_targeting_csv.py "${extra[@]}"
  if [[ -n "${DEALIX_API_BASE:-}" ]] && [[ -n "${DEALIX_ADMIN_API_KEY:-}" ]]; then
    python3 scripts/sync_war_room_targets_api.py
  fi
fi

if [[ "$SKIP_REVENUE_DAY" != "1" ]]; then
  echo "=== D: Founder revenue day ==="
  bash scripts/run_founder_revenue_day.sh
fi

echo "LAUNCH_EXECUTION_RAILWAY=done"
