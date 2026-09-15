#!/usr/bin/env bash
# Isolated restore rehearsal for Dealix custom-format PostgreSQL backups.
set -Eeuo pipefail
umask 077
BACKUP_FILE="${BACKUP_FILE:-}"
BACKUP_LOCAL_DIR="${BACKUP_LOCAL_DIR:-/var/backups/dealix}"
POSTGRES_IMAGE="${POSTGRES_IMAGE:-pgvector/pgvector:pg18}"
EXPECTED_MIN_TABLES="${EXPECTED_MIN_TABLES:-1}"
EXPECTED_ACCOUNTS="${EXPECTED_ACCOUNTS:-}"
if [[ -z "$BACKUP_FILE" ]]; then BACKUP_FILE="$(ls -t "$BACKUP_LOCAL_DIR"/*.pgdump 2>/dev/null | head -n1 || true)"; fi
[[ -n "$BACKUP_FILE" && -f "$BACKUP_FILE" && -s "$BACKUP_FILE" ]] || { echo "RESTORE_REHEARSAL=FAIL no usable backup" >&2; exit 1; }
if [[ -f "$BACKUP_FILE.sha256" ]]; then (cd "$(dirname "$BACKUP_FILE")" && sha256sum -c "$(basename "$BACKUP_FILE").sha256") >/dev/null; fi
NAME="dealix-restore-rehearsal-$(date +%s)-$$"
cleanup(){ docker rm -f "$NAME" >/dev/null 2>&1 || true; }; trap cleanup EXIT
docker run -d --rm --name "$NAME" -e POSTGRES_HOST_AUTH_METHOD=trust "$POSTGRES_IMAGE" >/dev/null
READY=0; for _ in $(seq 1 60); do if docker exec "$NAME" pg_isready -U postgres >/dev/null 2>&1; then READY=1; break; fi; sleep 1; done; [[ "$READY" == 1 ]]
sleep 1
docker exec -i "$NAME" pg_restore --exit-on-error --no-owner --no-privileges -U postgres -d postgres < "$BACKUP_FILE"
TABLES="$(docker exec "$NAME" psql -U postgres -Atc "select count(*) from information_schema.tables where table_schema='public' and table_type='BASE TABLE'")"
(( TABLES >= EXPECTED_MIN_TABLES )) || { echo "RESTORE_REHEARSAL=FAIL tables=$TABLES" >&2; exit 4; }
VECTOR="$(docker exec "$NAME" psql -U postgres -Atc "select coalesce((select extversion from pg_extension where extname='vector'),'absent')")"
[[ "$VECTOR" != absent ]] || { echo "RESTORE_REHEARSAL=FAIL vector_extension=absent" >&2; exit 4; }
ACCOUNTS="$(docker exec "$NAME" psql -U postgres -Atc "select case when to_regclass('public.accounts') is null then -1 else (select count(*) from accounts) end")"
if [[ -n "$EXPECTED_ACCOUNTS" && "$ACCOUNTS" != "$EXPECTED_ACCOUNTS" ]]; then echo "RESTORE_REHEARSAL=FAIL accounts=$ACCOUNTS expected=$EXPECTED_ACCOUNTS" >&2; exit 4; fi
printf 'RESTORE_REHEARSAL=PASS tables=%s accounts=%s vector=%s postgres_image=%s isolated=yes host_ports=none\n' "$TABLES" "$ACCOUNTS" "$VECTOR" "$POSTGRES_IMAGE"
