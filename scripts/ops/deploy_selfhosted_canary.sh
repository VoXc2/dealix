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

export DEALIX_GIT_SHA="$CURRENT_SHA"
export DEALIX_APP_ENV="${DEALIX_APP_ENV:-development}"
export DEALIX_ORCHESTRATOR_BACKEND="${DEALIX_ORCHESTRATOR_BACKEND:-postgres}"
export DEALIX_DATABASE_URL="${DEALIX_DATABASE_URL:-postgresql+asyncpg://dealix_canary@postgres:5432/dealix_canary}"

docker compose -f "$COMPOSE_FILE" build --pull api web

if [[ "$USE_LOCAL_DB" == "1" ]]; then
  docker compose -f "$COMPOSE_FILE" --profile local-db up -d postgres
  for _ in $(seq 1 30); do
    if docker compose -f "$COMPOSE_FILE" --profile local-db exec -T postgres \
      pg_isready -U dealix_canary -d dealix_canary >/dev/null 2>&1; then
      break
    fi
    sleep 2
  done
  docker compose -f "$COMPOSE_FILE" --profile local-db exec -T postgres \
    pg_isready -U dealix_canary -d dealix_canary >/dev/null

  if ! docker compose -f "$COMPOSE_FILE" --profile local-db exec -T postgres \
    psql -U dealix_canary -d dealix_canary -Atc \
    "select to_regclass('public.alembic_version') is not null" | grep -qx t; then
    docker compose -f "$COMPOSE_FILE" --profile local-db run --rm \
      -e DEALIX_ALLOW_FRESH_DB_BOOTSTRAP=1 \
      api python /app/scripts/ops/bootstrap_fresh_database.py --confirm-empty-bootstrap
  fi

  docker compose -f "$COMPOSE_FILE" --profile local-db run --rm \
    api python /app/scripts/ops/check_alembic_version_capacity.py
fi

docker compose -f "$COMPOSE_FILE" up -d api web

wait_liveness() {
  local url="$1"
  for _ in $(seq 1 30); do
    if curl -fsS "$url" >/dev/null 2>&1; then
      printf 'CANARY_LIVENESS=PASS url=%s\n' "$url"
      return 0
    fi
    sleep 2
  done
  echo "FAIL: canary liveness timeout: $url" >&2
  docker compose -f "$COMPOSE_FILE" ps >&2 || true
  return 67
}

verify_release() {
  local url="$1"
  local service="$2"
  local body=""
  for _ in $(seq 1 30); do
    if body="$(curl -fsS "$url" 2>/dev/null)"; then
      if python3 - "$EXPECTED_SHA" "$service" "$body" <<'PY'
import json, sys
expected, service, raw = sys.argv[1:]
try:
    data = json.loads(raw)
except Exception:
    raise SystemExit(1)
if data.get("status") != "ok" or data.get("service") != service or data.get("git_sha") != expected:
    raise SystemExit(1)
PY
      then
        printf 'CANARY_RELEASE=PASS service=%s sha=%s\n' "$service" "$EXPECTED_SHA"
        return 0
      fi
    fi
    sleep 2
  done
  echo "FAIL: canary release mismatch: $url expected_service=$service expected_sha=$EXPECTED_SHA" >&2
  docker compose -f "$COMPOSE_FILE" ps >&2 || true
  return 67
}

wait_liveness http://127.0.0.1:18000/healthz
verify_release http://127.0.0.1:18000/version dealix-api
verify_release http://127.0.0.1:13000/healthz dealix-web

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
