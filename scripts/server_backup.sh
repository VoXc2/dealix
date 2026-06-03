#!/usr/bin/env bash
# Backup Dealix Docker volumes and database dumps on a self-hosted Docker server.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ENV_FILE="${ENV_FILE:-.env.prod}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.prod.yml}"
BACKUP_DIR="${BACKUP_DIR:-/srv/dealix/backups}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
TARGET="$BACKUP_DIR/$STAMP"

mkdir -p "$TARGET"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing $ENV_FILE"
  exit 1
fi

set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a

POSTGRES_USER="${POSTGRES_USER:-dealix}"
POSTGRES_DB="${POSTGRES_DB:-dealix}"

echo "=== Postgres dump ==="
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" exec -T postgres \
  pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > "$TARGET/postgres.sql"

echo "=== Redis snapshot copy ==="
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" exec -T redis redis-cli -a "$REDIS_PASSWORD" SAVE >/dev/null || true
docker cp dealix-redis:/data "$TARGET/redis-data" || true

echo "=== Metadata ==="
{
  echo "stamp=$STAMP"
  echo "git_sha=$(git rev-parse HEAD 2>/dev/null || echo unknown)"
  docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" ps
} > "$TARGET/metadata.txt"

tar -C "$BACKUP_DIR" -czf "$BACKUP_DIR/dealix-backup-$STAMP.tar.gz" "$STAMP"
rm -rf "$TARGET"

echo "DEALIX_BACKUP_OK $BACKUP_DIR/dealix-backup-$STAMP.tar.gz"
