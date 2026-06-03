#!/usr/bin/env bash
# Railway UI alignment — repo config-as-code + optional live /healthz + prod smoke.
# Founder: fix Railway UI drift before blaming app code.
#
# Usage:
#   bash scripts/railway_ui_alignment.sh
#   bash scripts/railway_ui_alignment.sh --with-smoke
#   RAILWAY_UI_START_COMMAND='./start.sh' RAILWAY_UI_PREDEPLOY='echo "no migration needed"' \
#     bash scripts/railway_ui_alignment.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

WITH_SMOKE=0
for arg in "$@"; do
  case "$arg" in
    --with-smoke) WITH_SMOKE=1 ;;
  esac
done

API_BASE="${DEALIX_API_BASE:-https://api.dealix.me}"
UI_START="${RAILWAY_UI_START_COMMAND:-}"
UI_PREDEPLOY="${RAILWAY_UI_PREDEPLOY:-}"

echo "== Railway UI alignment (api.dealix.me) =="
echo "  canonical: dealix/config/railway_ui_canonical.yaml"
echo "  settings:  docs/ops/RAILWAY_PRODUCTION_SETTINGS_AR.md"
echo ""

PY="$(command -v python3 2>/dev/null || true)"
if [[ -z "$PY" ]] && command -v py >/dev/null 2>&1; then
  PY="py -3"
fi

ARGS=(scripts/verify_railway_production_config.py --api-base "$API_BASE")
if [[ -n "$UI_START" ]]; then
  ARGS+=(--ui-start-command "$UI_START")
fi
if [[ -n "$UI_PREDEPLOY" ]]; then
  ARGS+=(--ui-predeploy "$UI_PREDEPLOY")
fi

$PY "${ARGS[@]}"
RC=$?

if [[ "$RC" -ne 0 ]]; then
  echo ""
  echo "FOUNDER_ACTION:"
  echo "  1. Railway → Deploy → Start Command: CLEAR (or /app/start.sh only)"
  echo "  2. Railway → Deploy → Pre-deploy: CLEAR (uses railway.toml) or sh /app/scripts/railway_predeploy.sh"
  echo "  3. Enable Wait for CI on main"
  echo "  4. Re-deploy after fixing UI"
  exit "$RC"
fi

if [[ "$WITH_SMOKE" -eq 1 ]]; then
  echo ""
  echo "== prod_smoke =="
  bash "$ROOT/scripts/prod_smoke.sh" "$API_BASE"
fi

echo ""
echo "RAILWAY_UI_ALIGNMENT=PASS"
