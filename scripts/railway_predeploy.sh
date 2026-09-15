#!/usr/bin/env bash
set -Eeuo pipefail

cd /app 2>/dev/null || cd "$(dirname "$0")/.." || exit 1

migration_intent="${RUN_RAILWAY_PRE_DEPLOY_MIGRATE:-0}"

if [ "$migration_intent" = "1" ]; then
  echo "RAILWAY_PREDEPLOY: HOLD migrations - persistent Railway variables are not action-bound L5 authority" >&2
  echo "RAILWAY_PREDEPLOY: MIGRATION_EXECUTION=NOT_EXECUTED" >&2
  echo "RAILWAY_PREDEPLOY: use a separately authorized one-shot migration executor bound to the exact environment, revision payload, expiry, idempotency key, and ACTION_HASH" >&2
  exit 0
fi

echo "RAILWAY_PREDEPLOY: SKIP migrations (no exact action-bound migration authority)"
echo "RAILWAY_PREDEPLOY: MIGRATION_EXECUTION=NOT_EXECUTED"
exit 0
