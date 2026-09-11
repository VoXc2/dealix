#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
COMPOSE_FILE="$REPO/deploy/selfhost/compose.yml"
EXPECTED_SHA="${DEALIX_EXPECTED_SHA:-}"
USE_LOCAL_DB="${DEALIX_SELFHOST_LOCAL_DB:-0}"

if [[ -z "$EXPECTED_SHA" ]]; then
  echo "HOLD: DEALIX_EXPECTED_SHA is required" >&2
  exit 64
fi

cd "$REPO"
CURRENT_SHA="$(git rev-parse HEAD)"
if [[ "$CURRENT_SHA" != "$EXPECTED_SHA" ]]; then
  echo "HOLD: exact-head mismatch current=$CURRENT_SHA expected=$EXPECTED_SHA" >&2
  exit 65
fi

required=(
  /opt/dealix/control/secrets/selfhost.env
  /opt/dealix/control/secrets/selfhost-web.env
)
if [[ "$USE_LOCAL_DB" == "1" ]]; then
  required+=(/opt/dealix/control/secrets/selfhost-postgres.env)
fi
for f in "${required[@]}"; do
  if [[ ! -s "$f" ]]; then
    echo "HOLD: required runtime env file missing: $f" >&2
    exit 66
  fi
done

export DEALIX_GIT_SHA="$CURRENT_SHA"
docker compose -f "$COMPOSE_FILE" build --pull api web

if [[ "$USE_LOCAL_DB" == "1" ]]; then
  docker compose -f "$COMPOSE_FILE" --profile local-db up -d postgres
  for _ in $(seq 1 30); do
    if docker compose -f "$COMPOSE_FILE" --profile local-db exec -T postgres pg_isready >/dev/null 2>&1; then
      break
    fi
    sleep 2
  done
  docker compose -f "$COMPOSE_FILE" --profile local-db exec -T postgres pg_isready >/dev/null
  docker compose -f "$COMPOSE_FILE" --profile local-db run --rm \
    -e RUN_RAILWAY_PRE_DEPLOY_MIGRATE=1 \
    -e DEALIX_DB_MIGRATION_AUTHORIZED=1 \
    api bash /app/scripts/railway_predeploy.sh
fi

docker compose -f "$COMPOSE_FILE" up -d api web

for url in http://127.0.0.1:18000/healthz http://127.0.0.1:13000/healthz; do
  ok=0
  for _ in $(seq 1 30); do
    if curl -fsS "$url" >/dev/null; then ok=1; break; fi
    sleep 2
  done
  if [[ "$ok" != 1 ]]; then
    echo "FAIL: canary health failed: $url" >&2
    docker compose -f "$COMPOSE_FILE" ps >&2 || true
    exit 67
  fi
done

END_SHA="$(git rev-parse HEAD)"
if [[ "$END_SHA" != "$EXPECTED_SHA" ]]; then
  echo "HOLD: head moved during canary start/end=$EXPECTED_SHA/$END_SHA" >&2
  exit 68
fi

echo "SELFHOST_CANARY=PASS"
echo "GIT_SHA=$CURRENT_SHA"
echo "WEB=http://127.0.0.1:13000"
echo "API=http://127.0.0.1:18000"
echo "PUBLIC_CUTOVER=NOT_EXECUTED"
if [[ "$USE_LOCAL_DB" == "1" ]]; then
  echo "LOCAL_POSTGRES=CANARY_ONLY"
else
  echo "LOCAL_POSTGRES=NOT_EXECUTED"
fi
