#!/usr/bin/env bash
# Backup self-hosted Dealix PostgreSQL + Redis with a restoreable archive.
set -Eeuo pipefail
umask 077
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." >/dev/null 2>&1 && pwd -P)"
cd "$ROOT"
ENV_FILE="${ENV_FILE:-$ROOT/.env.prod}"
COMPOSE_FILE="${COMPOSE_FILE:-$ROOT/docker-compose.prod.yml}"
BACKUP_DIR="${BACKUP_DIR:-/var/backups/dealix}"
EXPECTED_SHA="${DEALIX_EXPECTED_SHA:-}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
[[ -f "$ENV_FILE" ]] || { echo "Missing $ENV_FILE" >&2; exit 1; }
[[ "$EXPECTED_SHA" =~ ^[0-9a-f]{40}$ ]] || { echo "DEALIX_EXPECTED_SHA must be exact" >&2; exit 1; }
[[ "$(git rev-parse HEAD)" == "$EXPECTED_SHA" ]] || { echo "exact-head mismatch" >&2; exit 1; }
set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a
: "${POSTGRES_PASSWORD:?POSTGRES_PASSWORD required}"
: "${REDIS_PASSWORD:?REDIS_PASSWORD required}"
mkdir -p "$BACKUP_DIR"; chmod 700 "$BACKUP_DIR" 2>/dev/null || true
export DEALIX_ENV_FILE="$ENV_FILE"
COMPOSE=(docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE")
PGDUMP="$BACKUP_DIR/dealix-$STAMP.pgdump"
META="$BACKUP_DIR/dealix-$STAMP.metadata.txt"
REDIS_TAR="$BACKUP_DIR/dealix-$STAMP.redis-data.tar.gz"
"${COMPOSE[@]}" exec -T postgres pg_dump -Fc --no-owner --no-acl -U "${POSTGRES_USER:-dealix}" "${POSTGRES_DB:-dealix}" > "$PGDUMP"
chmod 600 "$PGDUMP"
"${COMPOSE[@]}" exec -T postgres pg_restore --list < "$PGDUMP" >/dev/null
sha256sum "$PGDUMP" > "$PGDUMP.sha256"; chmod 600 "$PGDUMP.sha256"
"${COMPOSE[@]}" exec -T redis redis-cli -a "$REDIS_PASSWORD" SAVE >/dev/null 2>&1 || true
TMPDIR="$(mktemp -d)"; trap 'rm -rf "$TMPDIR"' EXIT
docker cp dealix-redis:/data "$TMPDIR/redis-data" >/dev/null 2>&1 || true
if [[ -d "$TMPDIR/redis-data" ]]; then
  tar -C "$TMPDIR" -czf "$REDIS_TAR" redis-data; chmod 600 "$REDIS_TAR"
  sha256sum "$REDIS_TAR" > "$REDIS_TAR.sha256"; chmod 600 "$REDIS_TAR.sha256"
fi
printf 'stamp=%s\ngit_sha=%s\npostgres_image=pgvector/pgvector:pg18\nformat=pg_dump_custom\n' "$STAMP" "$EXPECTED_SHA" > "$META"
chmod 600 "$META"
printf 'DEALIX_BACKUP_OK pgdump=%s checksum=%s metadata=%s\n' "$PGDUMP" "$PGDUMP.sha256" "$META"
