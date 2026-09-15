#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." >/dev/null 2>&1 && pwd -P)"
cd "$ROOT"
MODE="${1:---preflight}"
EXPECTED_SHA="${DEALIX_EXPECTED_SHA:-}"
CONFIRM_SHA="${CONFIRM_SHA:-}"
ENV_FILE="${DEALIX_ENV_FILE:-$ROOT/.env.prod}"
COMPOSE_FILE="$ROOT/deploy/selfhost/compose.yml"
DB_PORT="${DEALIX_SELFHOST_DB_PORT:-15432}"

log(){ printf '[selfhost-db] %s\n' "$*"; }
hold(){ log "HOLD: $*" >&2; exit 78; }
[[ "$MODE" == --preflight || "$MODE" == --execute ]] || hold "mode must be --preflight or --execute"
[[ "$EXPECTED_SHA" =~ ^[0-9a-f]{40}$ ]] || hold "DEALIX_EXPECTED_SHA must be exact"
[[ "$(git rev-parse HEAD)" == "$EXPECTED_SHA" ]] || hold "exact-head mismatch"
[[ -z "$(git status --porcelain --untracked-files=no)" ]] || hold "tracked worktree is dirty"
[[ -f "$ENV_FILE" ]] || hold "missing production env file"
[[ -z "$(find "$ENV_FILE" -maxdepth 0 -perm /077 -print -quit)" ]] || hold "production env permissions too broad"
[[ "$DB_PORT" =~ ^[0-9]+$ ]] && (( DB_PORT >= 1024 && DB_PORT <= 65535 )) || hold "invalid DB port"

set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a
for key in POSTGRES_USER POSTGRES_DB POSTGRES_PASSWORD DEALIX_DATABASE_URL; do
  value="${!key:-}"
  [[ -n "$value" ]] || hold "missing $key"
  case "$value" in *CHANGE_ME*|*change-me*|*REPLACE*) hold "placeholder $key" ;; esac
done
python3 - <<'PY'
import os
from urllib.parse import unquote, urlparse
url = os.environ["DEALIX_DATABASE_URL"]
expected_user = os.environ["POSTGRES_USER"]
expected_db = os.environ["POSTGRES_DB"]
u = urlparse(url.replace("postgresql+asyncpg://", "postgresql://", 1))
if u.scheme != "postgresql":
    raise SystemExit("production DB URL must be PostgreSQL")
if (u.hostname or "").lower() != "postgres":
    raise SystemExit("production app DB host must be canonical self-host postgres")
if unquote(u.username or "") != expected_user or u.path.lstrip("/") != expected_db:
    raise SystemExit("production DB URL user/database mismatch")
if not unquote(u.password or ""):
    raise SystemExit("production DB URL password missing")
PY

export DEALIX_GIT_SHA="$EXPECTED_SHA"
export DEALIX_IMAGE_TAG="${EXPECTED_SHA:0:12}"
export DEALIX_APP_ENV=production
export DEALIX_SELFHOST_DB_PORT="$DB_PORT"
export COMPOSE_PROJECT_NAME="${DEALIX_PRODUCTION_PROJECT_NAME:-dealix-production}"
COMPOSE=(docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE")
"${COMPOSE[@]}" --profile production-db config >/dev/null
log "PREFLIGHT=PASS sha=$EXPECTED_SHA project=$COMPOSE_PROJECT_NAME db_bind=127.0.0.1:$DB_PORT"
if [[ "$MODE" == --preflight ]]; then
  log "PRODUCTION_DB_MUTATION=NOT_EXECUTED"
  exit 0
fi

[[ "${DEALIX_PREPARE_PRODUCTION_DB:-}" == YES ]] || hold "DEALIX_PREPARE_PRODUCTION_DB=YES required"
[[ "$CONFIRM_SHA" == "$EXPECTED_SHA" ]] || hold "CONFIRM_SHA must equal exact release SHA"
PREPARE_ACTION_ID="dealix-production-db-prepare-v1:${EXPECTED_SHA}"
[[ "${DEALIX_L5_APPROVAL_ACTION:-}" == "$PREPARE_ACTION_ID" ]] || hold "exact action-bound approval required: DEALIX_L5_APPROVAL_ACTION=$PREPARE_ACTION_ID"
"${COMPOSE[@]}" build --pull api
"${COMPOSE[@]}" --profile production-db up -d postgres
for _ in $(seq 1 30); do
  if "${COMPOSE[@]}" --profile production-db exec -T postgres \
    pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" >/dev/null 2>&1; then
    break
  fi
  sleep 2
done
"${COMPOSE[@]}" --profile production-db exec -T postgres \
  pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" >/dev/null || hold "postgres not ready"

TABLES="$("${COMPOSE[@]}" --profile production-db exec -T postgres \
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Atc \
  "select count(*) from information_schema.tables where table_schema='public' and table_type='BASE TABLE'")"
HAS_ALEMBIC="$("${COMPOSE[@]}" --profile production-db exec -T postgres \
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Atc \
  "select to_regclass('public.alembic_version') is not null")"
if [[ "$TABLES" == 0 ]]; then
  [[ "${DEALIX_BOOTSTRAP_PRODUCTION_DB:-}" == YES ]] || hold "empty DB requires DEALIX_BOOTSTRAP_PRODUCTION_DB=YES"
  "${COMPOSE[@]}" --profile production-db run --rm \
    -e DEALIX_ALLOW_FRESH_DB_BOOTSTRAP=1 \
    api python /app/scripts/ops/bootstrap_fresh_database.py --confirm-empty-bootstrap
elif [[ "$HAS_ALEMBIC" != t ]]; then
  hold "non-empty DB without alembic_version"
fi

CURRENT_OUT="$("${COMPOSE[@]}" --profile production-db run --rm api alembic current 2>&1)"
printf '%s\n' "$CURRENT_OUT" | grep -q '(head)' || hold "production DB is not at source Alembic head"
"${COMPOSE[@]}" --profile production-db run --rm \
  api python /app/scripts/ops/check_alembic_version_capacity.py

log "PRODUCTION_DB_PREP=PASS sha=$EXPECTED_SHA db_bind=127.0.0.1:$DB_PORT"
log "RAILWAY_DATA_MIGRATION=NOT_EXECUTED"
log "PUBLIC_CUTOVER=NOT_EXECUTED"
