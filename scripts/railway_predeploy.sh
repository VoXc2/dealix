#!/usr/bin/env sh
# Railway pre-deploy — run Alembic when DATABASE_URL is available (production).
# Policy: docs/ops/RAILWAY_PRODUCTION_POLICY_AR.md
# Override skip (emergency only): RUN_RAILWAY_PRE_DEPLOY_MIGRATE=0
set -e

cd /app 2>/dev/null || cd "$(dirname "$0")/.." || exit 1

if [ "${RUN_RAILWAY_PRE_DEPLOY_MIGRATE:-0}" = "0" ]; then
  echo "RAILWAY_PREDEPLOY: SKIP migrations (set RUN_RAILWAY_PRE_DEPLOY_MIGRATE=1 to run alembic upgrade head)"
  exit 0
fi

if [ -z "${DATABASE_URL:-}" ]; then
  echo "RAILWAY_PREDEPLOY: SKIP — DATABASE_URL unset (build/pre-deploy without DB)"
  exit 0
fi

echo "RAILWAY_PREDEPLOY: alembic upgrade head"
if command -v alembic >/dev/null 2>&1; then
  alembic upgrade head
else
  python -m alembic upgrade head 2>/dev/null || python3 -m alembic upgrade head
fi
echo "RAILWAY_PREDEPLOY: OK"
