#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd -P)"
DEFAULT_REPO="$(cd -- "$SCRIPT_DIR/../.." >/dev/null 2>&1 && pwd -P)"
REPO="${DEALIX_REPO:-$DEFAULT_REPO}"
COMPOSE_FILE="$REPO/deploy/selfhost/compose.yml"
# shellcheck source=selfhost_canary_project_name.sh
source "$SCRIPT_DIR/selfhost_canary_project_name.sh"

EXPECTED_SHA="${DEALIX_EXPECTED_SHA:-}"
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

RUN_ID="${DEALIX_CANARY_RUN_ID:-run-$(date -u +%H%M%S)-$$}"
export DEALIX_CANARY_RUN_ID="$RUN_ID"
COMPOSE_PROJECT_NAME="$(dealix_canary_project_name "$CURRENT_SHA" "$RUN_ID")"
export COMPOSE_PROJECT_NAME
export DEALIX_GIT_SHA="$CURRENT_SHA"
export DEALIX_IMAGE_TAG="${CURRENT_SHA:0:12}"
read -r AUTO_API_PORT AUTO_WEB_PORT AUTO_DB_PORT AUTO_INGRESS_PORT < <(python3 - <<'PY'
import socket
sockets = []
ports = []
for _ in range(4):
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    sockets.append(sock)
    ports.append(str(sock.getsockname()[1]))
print(" ".join(ports))
PY
)
export DEALIX_SELFHOST_API_PORT="${DEALIX_SELFHOST_API_PORT:-$AUTO_API_PORT}"
export DEALIX_SELFHOST_WEB_PORT="${DEALIX_SELFHOST_WEB_PORT:-$AUTO_WEB_PORT}"
export DEALIX_SELFHOST_DB_PORT="${DEALIX_SELFHOST_DB_PORT:-$AUTO_DB_PORT}"
export DEALIX_SELFHOST_INGRESS_PORT="${DEALIX_SELFHOST_INGRESS_PORT:-$AUTO_INGRESS_PORT}"
export DEALIX_SELFHOST_LOCAL_DB="${DEALIX_SELFHOST_LOCAL_DB:-1}"
export DEALIX_APP_ENV="${DEALIX_APP_ENV:-production}"
export DEALIX_INTERNAL_SURFACE_MODE="${DEALIX_INTERNAL_SURFACE_MODE:-closed}"

if [[ "${DEALIX_CANARY_PLAN_ONLY:-0}" == "1" ]]; then
  echo "CANARY_PLAN_ONLY=PASS"
  echo "COMPOSE_PROJECT_NAME=$COMPOSE_PROJECT_NAME"
  echo "DEALIX_CANARY_RUN_ID=$DEALIX_CANARY_RUN_ID"
  echo "PORTS=$DEALIX_SELFHOST_API_PORT,$DEALIX_SELFHOST_WEB_PORT,$DEALIX_SELFHOST_DB_PORT,$DEALIX_SELFHOST_INGRESS_PORT"
  exit 0
fi
if [[ "$DEALIX_SELFHOST_LOCAL_DB" == "1" && -z "${DEALIX_CANARY_POSTGRES_PASSWORD:-}" ]]; then
  export DEALIX_CANARY_POSTGRES_PASSWORD="$(python3 -c 'import secrets; print(secrets.token_urlsafe(24))')"
fi
if [[ "$DEALIX_SELFHOST_LOCAL_DB" == "1" ]]; then
  export POSTGRES_USER="${POSTGRES_USER:-dealix_canary}"
  export POSTGRES_DB="${POSTGRES_DB:-dealix_canary}"
  export POSTGRES_PASSWORD="$DEALIX_CANARY_POSTGRES_PASSWORD"
  export DEALIX_DATABASE_URL="postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}"
fi
if [[ "$DEALIX_APP_ENV" == "production" ]]; then
  export APP_SECRET_KEY="${APP_SECRET_KEY:-$(python3 -c 'import secrets; print(secrets.token_hex(32))')}"
  export JWT_SECRET_KEY="${JWT_SECRET_KEY:-$(python3 -c 'import secrets; print(secrets.token_hex(32))')}"
  export API_KEYS="${API_KEYS:-canary-$(python3 -c 'import secrets; print(secrets.token_urlsafe(24))')}"
  export ADMIN_API_KEYS="${ADMIN_API_KEYS:-canary-admin-$(python3 -c 'import secrets; print(secrets.token_urlsafe(24))')}"
fi

cleanup() {
  docker compose -f "$COMPOSE_FILE" --profile local-db --profile ingress-canary \
    down -v --remove-orphans >/dev/null 2>&1 || true
}
trap cleanup EXIT

bash "$SCRIPT_DIR/deploy_selfhosted_canary.sh"
bash "$SCRIPT_DIR/verify_selfhosted_ingress_canary.sh"

echo "PRIVATE_RELEASE_CANARY=PASS"
echo "GIT_SHA=$CURRENT_SHA"
echo "COMPOSE_PROJECT_NAME=$COMPOSE_PROJECT_NAME"
echo "DEALIX_CANARY_RUN_ID=$DEALIX_CANARY_RUN_ID"
echo "PUBLIC_CUTOVER=NOT_EXECUTED"
