#!/usr/bin/env bash
# Founder weekly loop — offline gates + GTM/Railway + weekly metrics + strongest plan.
# Used by founder_weekly_verify CI and local Sunday retro prep.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PY="$(command -v python3 2>/dev/null || echo "py -3")"
API_BASE="${DEALIX_API_BASE:-https://api.dealix.me}"

echo "== Founder operating system =="
bash scripts/verify_founder_operating_system.sh

echo "== GTM public surfaces (repo) =="
$PY scripts/verify_gtm_public_surfaces.py --skip-live

echo "== Railway production config (repo + live trust) =="
$PY scripts/verify_railway_production_config.py --api-base "$API_BASE" \
  ${RAILWAY_UI_START_COMMAND:+--ui-start-command "$RAILWAY_UI_START_COMMAND"} \
  ${RAILWAY_UI_PREDEPLOY:+--ui-predeploy "$RAILWAY_UI_PREDEPLOY"} \
  || true

echo "== Founder weekly metrics bundle =="
$PY scripts/founder_weekly_metrics_bundle.py --write || true

echo "== Founder production gates (unified) =="
$PY scripts/run_founder_production_gates.py --api-base "$API_BASE" \
  ${RAILWAY_UI_START_COMMAND:+--ui-start-command "$RAILWAY_UI_START_COMMAND"} \
  ${RAILWAY_UI_PREDEPLOY:+--ui-predeploy "$RAILWAY_UI_PREDEPLOY"} \
  || true

echo "== Commercial launch readiness =="
$PY scripts/verify_commercial_launch_ready.py

echo "== Strongest plan checklist =="
$PY scripts/founder_strongest_plan_status.py

echo "== Comprehensive plan =="
$PY scripts/founder_comprehensive_plan_status.py

echo "== CEO weekly retro =="
$PY scripts/founder_weekly_ceo_retro.py

echo "== Dogfooding war room =="
$PY scripts/founder_dogfooding_war_room_sync.py

echo "FOUNDER_WEEKLY_LOOP=PASS"
