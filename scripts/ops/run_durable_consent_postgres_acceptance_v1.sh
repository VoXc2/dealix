#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

export TZ="${TZ:-Asia/Riyadh}"
export LC_ALL="${LC_ALL:-C.UTF-8}"
export LANG="${LANG:-C.UTF-8}"
export PYTHONNOUSERSITE=1

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)"
CANONICAL_REPO="${DEALIX_CANONICAL_REPO:-/opt/dealix/workspace/dealix}"
EXPECTED="${1:-${DEALIX_EXPECTED_SHA:-}}"
cd "$ROOT"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"

if [[ -z "$EXPECTED" ]]; then
  echo 'DEALIX_DURABLE_CONSENT_POSTGRES_ACCEPTANCE=BLOCKED_EXPECTED_SHA_REQUIRED'
  exit 2
fi

GIT_HEAD="$(git -c "safe.directory=$ROOT" -C "$ROOT" rev-parse HEAD)"
if [[ "$GIT_HEAD" != "$EXPECTED" ]]; then
  echo "EXPECTED_SHA=$EXPECTED"
  echo "ACTUAL_SHA=$GIT_HEAD"
  echo 'DEALIX_DURABLE_CONSENT_POSTGRES_ACCEPTANCE=BLOCKED_SHA_MISMATCH'
  exit 3
fi

PY="${DEALIX_AUTOMATION_PYTHON:-}"
if [[ -z "$PY" || ! -x "$PY" ]]; then
  if [[ -x "$CANONICAL_REPO/.venv/bin/python" ]]; then
    PY="$CANONICAL_REPO/.venv/bin/python"
  elif [[ -x "$ROOT/.venv/bin/python" ]]; then
    PY="$ROOT/.venv/bin/python"
  else
    PY="$(command -v python3 2>/dev/null || true)"
  fi
fi
[[ -n "$PY" && -x "$PY" ]] || {
  echo 'DEALIX_DURABLE_CONSENT_POSTGRES_ACCEPTANCE=HOLD_PYTHON_UNAVAILABLE'
  exit 4
}

command -v docker >/dev/null 2>&1 || {
  echo 'DEALIX_DURABLE_CONSENT_POSTGRES_ACCEPTANCE=HOLD_DOCKER_UNAVAILABLE'
  exit 5
}
docker info >/dev/null 2>&1 || {
  echo 'DEALIX_DURABLE_CONSENT_POSTGRES_ACCEPTANCE=HOLD_DOCKER_AUTHORITY_UNAVAILABLE'
  exit 6
}

export DEALIX_EXTERNAL_SEND=0
export DEALIX_EMAIL_LIVE_SEND=0
export DEALIX_WHATSAPP_OUTBOUND=0
export DEALIX_PUBLIC_PUBLISH=0
export DEALIX_PAID_SPEND=0
export DEALIX_PAYMENT_EXECUTION=0
export DEALIX_PRODUCTION_MUTATION=0
export DEALIX_DNS_MUTATION=0
export DEALIX_DB_MUTATION=0
export DEALIX_SECRET_MUTATION=0
export DEALIX_IDENTITY_MUTATION=0
export DEALIX_AGENT_SELF_AUTHORITY=0
export DEALIX_AUTONOMY_LEVEL=4
export DEALIX_MODE=draft-only
export WHATSAPP_ALLOW_LIVE_SEND=false
export VOICE_AI_ENABLED=false
export VOICE_OUTBOUND_ENABLED=false
export VOICE_RECORDING_ENABLED=false

IMAGE="${DEALIX_CONSENT_POSTGRES_IMAGE:-postgres:16-alpine}"
if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  if [[ "${DEALIX_ALLOW_TEST_IMAGE_PULL:-0}" != "1" ]]; then
    echo 'DEALIX_DURABLE_CONSENT_POSTGRES_ACCEPTANCE=HOLD_TEST_IMAGE_NOT_LOCAL'
    echo "required_image=$IMAGE"
    echo 'set DEALIX_ALLOW_TEST_IMAGE_PULL=1 only for an explicitly approved isolated test-image pull'
    exit 7
  fi
  docker pull "$IMAGE" >/dev/null
fi

STAMP="$(date '+%Y%m%dT%H%M%S%z')"
SUFFIX="$(printf '%s' "$STAMP-$$" | sha256sum | cut -c1-12)"
NAME="dealix-consent-pg-$SUFFIX"
VOLUME="dealix-consent-pg-vol-$SUFFIX"
DB="dealix_consent_acceptance_$SUFFIX"
USER="dealix_consent_test"
PASS="$($PY - <<'PY'
import secrets
print(secrets.token_urlsafe(24))
PY
)"
PORT="$($PY - <<'PY'
import socket
s = socket.socket()
s.bind(("127.0.0.1", 0))
print(s.getsockname()[1])
s.close()
PY
)"

cleanup() {
  set +e
  unset DEALIX_ALLOW_FRESH_DB_BOOTSTRAP
  docker rm -f "$NAME" >/dev/null 2>&1 || true
  docker volume rm -f "$VOLUME" >/dev/null 2>&1 || true
}
trap cleanup EXIT

IMAGE_ID="$(docker image inspect --format '{{.Id}}' "$IMAGE")"
echo '======================================================================'
echo 'DEALIX DURABLE CONSENT — EPHEMERAL REAL POSTGRES ACCEPTANCE V1'
echo '======================================================================'
echo "exact_sha=$EXPECTED"
echo "image=$IMAGE"
echo "image_id=$IMAGE_ID"
echo 'bind=127.0.0.1_only'
echo 'production_db=false'
echo 'material_effects=false'

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
    tries=$((tries + 1))
    if (( tries >= 60 )); then
      echo 'DEALIX_DURABLE_CONSENT_POSTGRES_ACCEPTANCE=FAIL_POSTGRES_NOT_READY'
      exit 8
    fi
    sleep 1
  done
}
wait_ready

URL="postgresql+asyncpg://${USER}:${PASS}@127.0.0.1:${PORT}/${DB}"

# Dealix historical migration roots begin with ALTER operations and cannot
# bootstrap a truly empty PostgreSQL database. The repository-owned bootstrap
# is the canonical contract: build current metadata, prove schema drift-free,
# then stamp the checkout's Alembic heads. This target is loopback-only and
# disposable, never Production.
"$PY" scripts/check_alembic_single_head.py
DEALIX_ALLOW_FRESH_DB_BOOTSTRAP=1 DATABASE_URL="$URL" APP_ENV=test \
  "$PY" "$ROOT/scripts/ops/bootstrap_fresh_database.py" --confirm-empty-bootstrap

DATABASE_URL="$URL" APP_ENV=test DEALIX_CONSENT_BACKEND=postgres \
  "$PY" "$ROOT/scripts/ops/verify_durable_consent_postgres_v1.py" --phase setup

echo '=== EPHEMERAL POSTGRES RESTART ==='
docker restart "$NAME" >/dev/null
wait_ready

DATABASE_URL="$URL" APP_ENV=test DEALIX_CONSENT_BACKEND=postgres \
  "$PY" "$ROOT/scripts/ops/verify_durable_consent_postgres_v1.py" --phase restart

END_HEAD="$(git -c "safe.directory=$ROOT" -C "$ROOT" rev-parse HEAD)"
[[ "$END_HEAD" == "$EXPECTED" ]] || {
  echo 'DEALIX_DURABLE_CONSENT_POSTGRES_ACCEPTANCE=BLOCKED_HEAD_MOVED'
  exit 9
}
[[ -z "$(git -c "safe.directory=$ROOT" -C "$ROOT" status --porcelain)" ]] || {
  echo 'DEALIX_DURABLE_CONSENT_POSTGRES_ACCEPTANCE=BLOCKED_DIRTY_WORKTREE'
  exit 10
}

cat <<EOF
EXACT_SHA=$EXPECTED
FRESH_DB_BOOTSTRAP=PASS
ALEMBIC_HEADS_STAMPED=PASS
CONSENT_REAL_POSTGRES_BEHAVIOR=PASS
RESTART_PERSISTENCE=PASS
PRODUCTION_DB=false
EXTERNAL_SEND=false
PAYMENT=false
PUBLIC_PUBLISH=false
CLEANUP=automatic
DEALIX_DURABLE_CONSENT_POSTGRES_FULL_ACCEPTANCE=PASS
EOF
