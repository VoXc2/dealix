#!/usr/bin/env bash
set -Eeuo pipefail

cd /app 2>/dev/null || cd "$(dirname "$0")/.." || exit 1

run_step() {
  local step="$1"
  shift
  echo "RAILWAY_PREDEPLOY: START step=${step}"
  if "$@"; then
    echo "RAILWAY_PREDEPLOY: PASS step=${step}"
    return 0
  else
    local rc=$?
    echo "RAILWAY_PREDEPLOY: FAIL step=${step} rc=${rc}" >&2
    return "$rc"
  fi
}

if [ "${RUN_RAILWAY_PRE_DEPLOY_MIGRATE:-0}" != "1" ]; then
  echo "RAILWAY_PREDEPLOY: SKIP migrations (RUN_RAILWAY_PRE_DEPLOY_MIGRATE must equal 1)"
  exit 0
fi

if [ "${DEALIX_DB_MIGRATION_AUTHORIZED:-0}" != "1" ]; then
  echo "RAILWAY_PREDEPLOY: HOLD migrations — DEALIX_DB_MIGRATION_AUTHORIZED must equal 1"
  exit 0
fi

if [ -z "${DATABASE_URL:-}" ]; then
  echo "RAILWAY_PREDEPLOY: SKIP — DATABASE_URL unset"
  exit 0
fi

run_step capacity_check python scripts/ops/check_alembic_version_capacity.py

echo "RAILWAY_PREDEPLOY: alembic upgrade head"
if command -v alembic >/dev/null 2>&1; then
  run_step alembic_upgrade alembic upgrade head
elif command -v python >/dev/null 2>&1; then
  run_step alembic_upgrade python -m alembic upgrade head
else
  run_step alembic_upgrade python3 -m alembic upgrade head
fi

echo "RAILWAY_PREDEPLOY: OK"
