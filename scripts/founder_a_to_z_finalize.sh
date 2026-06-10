#!/usr/bin/env bash
# Dealix founder A-to-Z finalizer.
# Runs repository launch gates, optional Docker image builds, and optional live health probes.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

RUN_DOCKER="${RUN_DOCKER:-0}"
RUN_LIVE="${RUN_LIVE:-0}"
API_BASE="${DEALIX_API_BASE:-https://api.dealix.me}"
FRONTEND_BASE="${DEALIX_FRONTEND_BASE:-${DEALIX_FRONTEND_URL:-https://dealix.me}}"
APPS_WEB_BASE="${DEALIX_APPS_WEB_BASE:-${DEALIX_WEB_BASE:-${DEALIX_WEB_URL:-}}}"

echo "=== 1/6 Railway surface contract ==="
python3 scripts/verify_railway_surfaces.py

echo "=== 2/6 Environment contract ==="
python3 scripts/check_env_contract.py

echo "=== 3/6 OpenAPI contract ==="
python3 scripts/check_openapi_contract.py

echo "=== 4/6 Python compile smoke ==="
python3 -m compileall api auto_client_acquisition autonomous_growth core db integrations dealix scripts >/tmp/dealix_compileall.log
cat /tmp/dealix_compileall.log | tail -n 20

if [[ "$RUN_DOCKER" == "1" ]]; then
  echo "=== 5/6 Docker builds ==="
  docker build -t dealix-api-final .
  docker build -t dealix-frontend-final frontend
  docker build -t dealix-apps-web-final apps/web
else
  echo "=== 5/6 Docker builds skipped ==="
  echo "Set RUN_DOCKER=1 to verify all Railway Docker images locally."
fi

if [[ "$RUN_LIVE" == "1" ]]; then
  echo "=== 6/6 Live Railway smoke ==="
  args=(--live --api-base "$API_BASE" --frontend-base "$FRONTEND_BASE")
  if [[ -n "$APPS_WEB_BASE" ]]; then
    args+=(--apps-web-base "$APPS_WEB_BASE")
  fi
  python3 scripts/founder_launch_final_check.py "${args[@]}"
else
  echo "=== 6/6 Live smoke skipped ==="
  echo "Set RUN_LIVE=1 after Railway redeploys are complete."
fi

echo "FOUNDER_A_TO_Z_FINALIZE=ok"
