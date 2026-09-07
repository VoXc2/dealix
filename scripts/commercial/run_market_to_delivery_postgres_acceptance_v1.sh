#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

export TZ="${TZ:-Asia/Riyadh}"
export LC_ALL="${LC_ALL:-C.UTF-8}"
export LANG="${LANG:-C.UTF-8}"

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)"

# Keep pydantic-settings env_file=".env" and any other relative runtime reads
# scoped to the isolated exact-head worktree, never to the caller's cwd.
cd "$ROOT"

PY="${DEALIX_AUTOMATION_PYTHON:-}"
if [[ -z "$PY" || ! -x "$PY" ]]; then
  if [[ -x "$ROOT/.venv/bin/python" ]]; then
    PY="$ROOT/.venv/bin/python"
  else
    PY="$(command -v python3 2>/dev/null || true)"
  fi
fi

[[ -n "$PY" && -x "$PY" ]] || {
  echo 'DEALIX_MTD_POSTGRES_ACCEPTANCE=HOLD_PYTHON_UNAVAILABLE'
  exit 2
}

command -v docker >/dev/null 2>&1 || {
  echo 'DEALIX_MTD_POSTGRES_ACCEPTANCE=HOLD_DOCKER_UNAVAILABLE'
  exit 2
}

docker info >/dev/null 2>&1 || {
  echo 'DEALIX_MTD_POSTGRES_ACCEPTANCE=HOLD_DOCKER_AUTHORITY_UNAVAILABLE'
  exit 2
}

IMAGE="${DEALIX_MTD_POSTGRES_IMAGE:-postgres:16-alpine}"
if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  if [[ "${DEALIX_ALLOW_TEST_IMAGE_PULL:-0}" != "1" ]]; then
    echo 'DEALIX_MTD_POSTGRES_ACCEPTANCE=HOLD_TEST_IMAGE_NOT_LOCAL'
    echo "required_image=$IMAGE"
    echo 'set DEALIX_ALLOW_TEST_IMAGE_PULL=1 only for an explicitly approved isolated test-image pull'
    exit 2
  fi
  docker pull "$IMAGE" >/dev/null
fi

STAMP="$(date '+%Y%m%dT%H%M%S%z')"
SUFFIX="$(printf '%s' "$STAMP-$$" | sha256sum | cut -c1-12)"
NAME="dealix-mtd-pg-$SUFFIX"
VOLUME="dealix-mtd-pg-vol-$SUFFIX"
DB="dealix_mtd_acceptance_$SUFFIX"
USER="dealix_mtd_test"
PASS="$($PY - <<'PY'
import secrets
print(secrets.token_urlsafe(24))
PY
)"
PORT="$($PY - <<'PY'
import socket
s=socket.socket()
s.bind(('127.0.0.1',0))
print(s.getsockname()[1])
s.close()
PY
)"

cleanup() {
  set +e
  docker rm -f "$NAME" >/dev/null 2>&1 || true
  docker volume rm -f "$VOLUME" >/dev/null 2>&1 || true
}
trap cleanup EXIT

IMAGE_ID="$(docker image inspect --format '{{.Id}}' "$IMAGE")"

echo '======================================================================'
echo 'DEALIX MARKET-TO-DELIVERY — EPHEMERAL POSTGRES ACCEPTANCE V1'
echo '======================================================================'
echo "image=$IMAGE"
echo "image_id=$IMAGE_ID"
echo 'bind=127.0.0.1_only'
echo 'production_db=false'
echo 'customer_effects=false'
echo

docker volume create "$VOLUME" >/dev/null

docker run -d --name "$NAME" \
  --restart=no \
  -e POSTGRES_USER="$USER" \
  -e POSTGRES_PASSWORD="$PASS" \
  -e POSTGRES_DB="$DB" \
  -p "127.0.0.1:${PORT}:5432" \
  -v "$VOLUME:/var/lib/postgresql/data" \
  "$IMAGE" >/dev/null

wait_ready() {
  local tries=0
  until docker exec "$NAME" pg_isready -U "$USER" -d "$DB" >/dev/null 2>&1; do
    tries=$((tries+1))
    if (( tries >= 60 )); then
      echo 'DEALIX_MTD_POSTGRES_ACCEPTANCE=FAIL_POSTGRES_NOT_READY'
      exit 3
    fi
    sleep 1
  done
}
wait_ready

URL="postgresql+asyncpg://${USER}:${PASS}@127.0.0.1:${PORT}/${DB}"

DEALIX_MTD_POSTGRES_URL="$URL" \
  "$PY" "$ROOT/scripts/commercial/verify_market_to_delivery_postgres_v1.py" \
  --phase setup-race

echo
echo '=== EPHEMERAL POSTGRES RESTART ==='
docker restart "$NAME" >/dev/null
wait_ready

DEALIX_MTD_POSTGRES_URL="$URL" \
  "$PY" "$ROOT/scripts/commercial/verify_market_to_delivery_postgres_v1.py" \
  --phase replay-after-restart

echo
echo 'DEALIX_MTD_POSTGRES_FULL_ACCEPTANCE=PASS'
echo 'real_postgres=true'
echo 'restart_persistence=true'
echo 'concurrent_idempotency=true'
echo 'changed_payload_conflict=true'
echo 'production_db=false'
echo 'external_send=false'
echo 'payment=false'
echo 'cleanup=automatic'
