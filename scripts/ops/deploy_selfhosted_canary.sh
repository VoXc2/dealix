#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd -P)"
DEFAULT_REPO="$(cd -- "$SCRIPT_DIR/../.." >/dev/null 2>&1 && pwd -P)"
REPO="${DEALIX_REPO:-$DEFAULT_REPO}"
COMPOSE_FILE="$REPO/deploy/selfhost/compose.yml"
# shellcheck source=selfhost_canary_project_name.sh
source "$REPO/scripts/ops/selfhost_canary_project_name.sh"
EXPECTED_SHA="${DEALIX_EXPECTED_SHA:-}"
RUN_ID="${DEALIX_CANARY_RUN_ID:-}"
USE_LOCAL_DB="${DEALIX_SELFHOST_LOCAL_DB:-0}"
API_PORT="${DEALIX_SELFHOST_API_PORT:-18000}"
WEB_PORT="${DEALIX_SELFHOST_WEB_PORT:-13000}"
DB_PORT="${DEALIX_SELFHOST_DB_PORT:-15432}"

if ! [[ "$API_PORT" =~ ^[0-9]+$ ]] || (( API_PORT < 1024 || API_PORT > 65535 )); then
  echo "HOLD: invalid DEALIX_SELFHOST_API_PORT=$API_PORT" >&2
  exit 64
fi
if ! [[ "$WEB_PORT" =~ ^[0-9]+$ ]] || (( WEB_PORT < 1024 || WEB_PORT > 65535 )); then
  echo "HOLD: invalid DEALIX_SELFHOST_WEB_PORT=$WEB_PORT" >&2
  exit 64
fi
if ! [[ "$DB_PORT" =~ ^[0-9]+$ ]] || (( DB_PORT < 1024 || DB_PORT > 65535 )); then
  echo "HOLD: invalid DEALIX_SELFHOST_DB_PORT=$DB_PORT" >&2
  exit 64
fi
export DEALIX_SELFHOST_API_PORT="$API_PORT"
export DEALIX_SELFHOST_WEB_PORT="$WEB_PORT"
export DEALIX_SELFHOST_DB_PORT="$DB_PORT"

if [[ -z "$EXPECTED_SHA" ]]; then
  echo "HOLD: DEALIX_EXPECTED_SHA is required" >&2
  exit 64
fi
if [[ -z "$RUN_ID" ]]; then
  echo "HOLD: DEALIX_CANARY_RUN_ID is required; use run_selfhosted_private_release_canary.sh" >&2
  exit 64
fi

cd "$REPO"
CURRENT_SHA="$(git rev-parse HEAD)"
if [[ "$CURRENT_SHA" != "$EXPECTED_SHA" ]]; then
  echo "HOLD: exact-head mismatch current=$CURRENT_SHA expected=$EXPECTED_SHA" >&2
  exit 65
fi

export DEALIX_GIT_SHA="$CURRENT_SHA"
export DEALIX_IMAGE_TAG="${CURRENT_SHA:0:12}"
COMPOSE_PROJECT_NAME="$(dealix_canary_project_name "$CURRENT_SHA" "$RUN_ID")"
export COMPOSE_PROJECT_NAME
export DEALIX_APP_ENV="${DEALIX_APP_ENV:-development}"
export DEALIX_ORCHESTRATOR_BACKEND="${DEALIX_ORCHESTRATOR_BACKEND:-postgres}"
if [[ "$USE_LOCAL_DB" == "1" ]]; then
  : "${DEALIX_CANARY_POSTGRES_PASSWORD:?set DEALIX_CANARY_POSTGRES_PASSWORD for local-db canary}"
  if ! [[ "$DEALIX_CANARY_POSTGRES_PASSWORD" =~ ^[A-Za-z0-9._~-]{16,128}$ ]]; then
    echo "HOLD: DEALIX_CANARY_POSTGRES_PASSWORD must be 16-128 URL-safe unreserved characters" >&2
    exit 64
  fi
  export POSTGRES_USER=dealix_canary
  export POSTGRES_DB=dealix_canary
  export POSTGRES_PASSWORD="$DEALIX_CANARY_POSTGRES_PASSWORD"
  export DEALIX_DATABASE_URL="postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}"
else
  : "${DEALIX_DATABASE_URL:?set DEALIX_DATABASE_URL when local-db canary is disabled}"
fi

echo "CANARY_POSTGRES_PASSWORD_CONTRACT=PASS"

docker compose -f "$COMPOSE_FILE" build --pull api web

if [[ "$USE_LOCAL_DB" == "1" ]]; then
  docker compose -f "$COMPOSE_FILE" --profile local-db up -d postgres
  for _ in $(seq 1 30); do
    if docker compose -f "$COMPOSE_FILE" --profile local-db exec -T postgres \
      pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" >/dev/null 2>&1; then
      break
    fi
    sleep 2
  done
  docker compose -f "$COMPOSE_FILE" --profile local-db exec -T postgres \
    pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" >/dev/null

  if ! docker compose -f "$COMPOSE_FILE" --profile local-db exec -T postgres \
    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Atc \
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

wait_liveness "http://127.0.0.1:${API_PORT}/healthz"
verify_release "http://127.0.0.1:${API_PORT}/version" dealix-api
verify_release "http://127.0.0.1:${WEB_PORT}/healthz" dealix-web

END_SHA="$(git rev-parse HEAD)"
if [[ "$END_SHA" != "$EXPECTED_SHA" ]]; then
  echo "HOLD: head moved during canary start/end=$EXPECTED_SHA/$END_SHA" >&2
  exit 68
fi

echo "SELFHOST_CANARY=PASS"
echo "GIT_SHA=$CURRENT_SHA"
echo "COMPOSE_PROJECT_NAME=$COMPOSE_PROJECT_NAME"
echo "DEALIX_CANARY_RUN_ID=$RUN_ID"
echo "WEB=http://127.0.0.1:${WEB_PORT}"
echo "API=http://127.0.0.1:${API_PORT}"
echo "PUBLIC_CUTOVER=NOT_EXECUTED"
if [[ "$USE_LOCAL_DB" == "1" ]]; then
  echo "LOCAL_POSTGRES=CANARY_ONLY"
else
  echo "LOCAL_POSTGRES=NOT_EXECUTED"
fi
