#!/usr/bin/env bash
# Founder production smoke — Railway verify + live trust endpoints (api.dealix.me).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

API_BASE="${DEALIX_API_BASE:-https://api.dealix.me}"
PY="$(command -v python3 2>/dev/null || echo "py -3")"

echo "== 1/4 Railway config-as-code =="
$PY scripts/verify_railway_production_config.py --api-base "$API_BASE" \
  ${RAILWAY_UI_START_COMMAND:+--ui-start-command "$RAILWAY_UI_START_COMMAND"} \
  ${RAILWAY_UI_PREDEPLOY:+--ui-predeploy "$RAILWAY_UI_PREDEPLOY"}

echo ""
echo "== 2/4 GTM public surfaces (repo) =="
$PY scripts/verify_gtm_public_surfaces.py --skip-live

echo ""
echo "== 3/4 Live curls (founder checklist) =="
curl -fsS "${API_BASE}/healthz" && echo ""
curl -fsS "${API_BASE}/version" && echo "" || echo "WARN: /version not live yet (deploy pending)"
curl -fsS "${API_BASE}/api/v1/meta" && echo "" || echo "WARN: /api/v1/meta not live yet"
curl -fsS "${API_BASE}/health" && echo ""

echo ""
echo "== 4/4 Unified production gates =="
$PY scripts/run_founder_production_gates.py --api-base "$API_BASE" \
  ${RAILWAY_UI_START_COMMAND:+--ui-start-command "$RAILWAY_UI_START_COMMAND"} \
  ${RAILWAY_UI_PREDEPLOY:+--ui-predeploy "$RAILWAY_UI_PREDEPLOY"}

echo "FOUNDER_PRODUCTION_SMOKE=PASS"
