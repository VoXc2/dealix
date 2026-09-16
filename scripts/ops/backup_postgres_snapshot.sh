#!/usr/bin/env bash
# shellcheck disable=SC2016
set -Eeuo pipefail
umask 077

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." >/dev/null 2>&1 && pwd -P)"
URL_FILE="${DEALIX_DATABASE_URL_FILE:-}"
OUT_DIR="${DEALIX_POSTGRES_BACKUP_DIR:-/opt/dealix/control/backups/postgres}"
ROLE="${DEALIX_BACKUP_ROLE:-}"
RELEASE_SHA="${DEALIX_BACKUP_RELEASE_SHA:-}"
CLIENT_IMAGE="${DEALIX_POSTGRES_CLIENT_IMAGE:-pgvector/pgvector:pg18@sha256:2ba9ca5f2e7daa0f0e7723cba1ee9167bab54efd3640516a44ac1a928dd67e7a}"
FINGERPRINT_SQL="$ROOT/scripts/ops/postgres_database_fingerprint.sql"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
STARTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

fail(){ echo "POSTGRES_BACKUP=HOLD reason=$1" >&2; exit "${2:-64}"; }
[[ "$ROLE" == railway-source || "$ROLE" == selfhost-target ]] || fail "invalid_backup_role"
[[ "$RELEASE_SHA" =~ ^[0-9a-f]{40}$ ]] || fail "invalid_release_sha"
[[ -n "$URL_FILE" && -f "$URL_FILE" ]] || fail "database_url_file_missing"
[[ -z "$(find "$URL_FILE" -maxdepth 0 -perm /077 -print -quit)" ]] || fail "database_url_file_permissions_too_broad" 65
command -v docker >/dev/null 2>&1 || fail "docker_required" 69
[[ -f "$FINGERPRINT_SQL" ]] || fail "fingerprint_sql_missing" 69

mkdir -p "$OUT_DIR"; chmod 700 "$OUT_DIR" 2>/dev/null || true
TMP_BASE="${DEALIX_SECURE_TMP_DIR:-/opt/dealix/control/tmp}"
mkdir -p "$TMP_BASE"; chmod 700 "$TMP_BASE"
TMP_DIR="$(mktemp -d "$TMP_BASE/postgres-backup.XXXXXX")"; chmod 700 "$TMP_DIR"
cleanup(){ rm -rf "$TMP_DIR"; }
trap cleanup EXIT
PASSWORD_FILE="$TMP_DIR/password"
mapfile -d '' -t PARTS < <(python3 - "$URL_FILE" "$PASSWORD_FILE" <<'PY'
import pathlib, sys, urllib.parse
url_path, password_path = map(pathlib.Path, sys.argv[1:])
raw = url_path.read_text(encoding="utf-8").strip()
u = urllib.parse.urlparse(raw)
if not u.scheme.startswith("postgresql") or not u.hostname or not u.username or not u.path.strip("/"):
    raise SystemExit("invalid PostgreSQL URL")
query = urllib.parse.parse_qs(u.query)
password_path.write_text(urllib.parse.unquote(u.password or ""), encoding="utf-8")
password_path.chmod(0o600)
values = (
    u.hostname,
    str(u.port or 5432),
    urllib.parse.unquote(u.username),
    u.path.lstrip("/"),
    (query.get("sslmode") or ["prefer"])[0],
)
for value in values:
    sys.stdout.buffer.write(value.encode() + b"\0")
PY
)
(( ${#PARTS[@]} == 5 )) || fail "database_url_parse_failed" 66
PGHOST="${PARTS[0]}"; PGPORT="${PARTS[1]}"; PGUSER="${PARTS[2]}"
PGDATABASE="${PARTS[3]}"; PGSSLMODE="${PARTS[4]}"
if [[ "$ROLE" == selfhost-target && "$PGHOST" == postgres ]]; then
  PGHOST="${DEALIX_SELFHOST_DB_HOST:-127.0.0.1}"
  PGPORT="${DEALIX_SELFHOST_DB_PORT:-15432}"
  case "$PGHOST" in
    127.0.0.1|::1|localhost) ;;
    *) fail "selfhost_backup_host_must_be_loopback" 67 ;;
  esac
fi
export PGHOST PGPORT PGUSER PGDATABASE PGSSLMODE
HOST_UID="$(id -u)"; HOST_GID="$(id -g)"
DOCKER_BASE=(
  docker run --rm --network host --user "$HOST_UID:$HOST_GID"
  -e PGHOST -e PGPORT -e PGUSER -e PGDATABASE -e PGSSLMODE
  -v "$TMP_DIR:/run/dealix-secrets:ro"
)

psql_safe(){
  "${DOCKER_BASE[@]}" "$CLIENT_IMAGE" sh -ceu \
    'export PGPASSWORD="$(cat /run/dealix-secrets/password)"; exec psql -X -qAt "$@"' sh "$@"
}
fingerprint(){
  local lines
  lines="$("${DOCKER_BASE[@]}" -v "$FINGERPRINT_SQL:/fingerprint.sql:ro" "$CLIENT_IMAGE" sh -ceu \
    'export PGPASSWORD="$(cat /run/dealix-secrets/password)"; exec psql -X -qAt -f /fingerprint.sql')"
  printf '%s\n' "$lines" | sha256sum | cut -d' ' -f1
}

SAFE_META="$(psql_safe -c "select current_setting('server_version_num')||'|'||current_setting('server_version')||'|'||(select count(*) from information_schema.tables where table_schema='public' and table_type='BASE TABLE')||'|'||coalesce((select extversion from pg_extension where extname='vector'),'')")"
IFS='|' read -r SERVER_VERSION_NUM SERVER_VERSION PUBLIC_TABLES PGVECTOR_VERSION <<< "$SAFE_META"
POSTGRES_MAJOR="$((10#$SERVER_VERSION_NUM / 10000))"
[[ "$POSTGRES_MAJOR" == 18 ]] || fail "postgres_major_must_be_18_got_${POSTGRES_MAJOR}" 67
[[ -n "$PGVECTOR_VERSION" ]] || fail "pgvector_extension_missing" 67

FINGERPRINT_BEFORE="$(fingerprint)"
FINAL="$OUT_DIR/postgres-$ROLE-$STAMP.pgdump"
TMP_DUMP="$OUT_DIR/.postgres-$ROLE-$STAMP.pgdump.tmp"
"${DOCKER_BASE[@]}" "$CLIENT_IMAGE" sh -ceu \
  'export PGPASSWORD="$(cat /run/dealix-secrets/password)"; exec pg_dump -Fc --no-owner --no-acl' \
  > "$TMP_DUMP"
test -s "$TMP_DUMP" || fail "empty_dump" 68
FINGERPRINT_AFTER="$(fingerprint)"
if [[ "$FINGERPRINT_BEFORE" != "$FINGERPRINT_AFTER" ]]; then
  rm -f "$TMP_DUMP"
  fail "database_changed_during_backup_capture" 68
fi
chmod 600 "$TMP_DUMP"; mv "$TMP_DUMP" "$FINAL"
sha256sum "$FINAL" > "$FINAL.sha256"
chmod 600 "$FINAL.sha256"
sha256sum -c "$FINAL.sha256" >/dev/null

docker run --rm --user "$HOST_UID:$HOST_GID" \
  -v "$OUT_DIR:/backup:ro" "$CLIENT_IMAGE" \
  pg_restore --list "/backup/$(basename "$FINAL")" > "$TMP_DIR/toc"
ENTRIES="$(grep -vc '^;' "$TMP_DIR/toc" || true)"
BYTES="$(stat -c %s "$FINAL")"
SHA="$(cut -d' ' -f1 "$FINAL.sha256")"

migration_count(){
  local table="$1" required_column="$2" predicate="$3"
  local table_exists column_exists
  table_exists="$(psql_safe -c "select to_regclass('public.${table}') is not null")"
  if [[ "$table_exists" != t ]]; then
    printf '%s\n' -1
    return
  fi
  column_exists="$(psql_safe -c "select exists(select 1 from information_schema.columns where table_schema='public' and table_name='${table}' and column_name='${required_column}')")"
  if [[ "$column_exists" != t ]]; then
    printf '%s\n' -1
    return
  fi
  psql_safe -c "select count(*) from public.${table} where ${predicate}"
}
RAILWAY_ARCHIVED_ROWS="$(migration_count operational_event_streams stream_id "stream_id='railway_legacy_20260915'")"
RAILWAY_PROOF_ROWS="$(migration_count proof_events evidence_source "evidence_source='railway_production_backup'")"
RAILWAY_CONVERSATION_ROWS="$(migration_count conversations id "id like 'legacy:%'")"
COMPLETED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RECEIPT="$FINAL.receipt.json"
python3 - "$RECEIPT" "$ROLE" "$RELEASE_SHA" "$STARTED_AT" "$COMPLETED_AT" \
  "$SERVER_VERSION" "$SERVER_VERSION_NUM" "$POSTGRES_MAJOR" "$PUBLIC_TABLES" \
  "$PGVECTOR_VERSION" "$SHA" "$BYTES" "$ENTRIES" "$(basename "$FINAL")" \
  "$FINGERPRINT_AFTER" "$RAILWAY_ARCHIVED_ROWS" "$RAILWAY_PROOF_ROWS" \
  "$RAILWAY_CONVERSATION_ROWS" <<'PY'
import hashlib, json, os, sys
(
    path, role, release, started, completed, version, version_num, major,
    tables, vector, sha, size, entries, filename, fingerprint, archived,
    proof, conversations,
) = sys.argv[1:]
schema = (
    "dealix.railway-source-backup-receipt.v1"
    if role == "railway-source"
    else "dealix.selfhost-backup-receipt.v1"
)
payload = {
    "schema_version": schema,
    "status": "PASS",
    "backup_role": role,
    "release_sha": release,
    "snapshot_started_at": started,
    "capture_completed_at": completed,
    "server_version": version,
    "server_version_num": int(version_num),
    "postgres_major": int(major),
    "public_tables": int(tables),
    "pgvector_version": vector,
    "pgvector_required": True,
    "database_fingerprint_sha256": fingerprint,
    "toc_entries": int(entries),
    "external_effect": "READ_ONLY_DB",
    "railway_archived_rows": int(archived),
    "railway_proof_rows": int(proof),
    "railway_conversation_rows": int(conversations),
}
if role == "railway-source":
    payload.update({
        "source_snapshot_started_at": started,
        "dump_file": filename,
        "dump_sha256": sha,
        "dump_bytes": int(size),
        "pg_restore_list": "PASS",
    })
else:
    payload.update({
        "created_at": completed,
        "archive_file": filename,
        "archive_sha256": sha,
        "archive_bytes": int(size),
        "postgres_restore_list": "PASS",
    })
canonical = json.dumps(
    payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
).encode()
payload["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
tmp = path + ".tmp"
with open(tmp, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
    handle.write("\n")
os.chmod(tmp, 0o600)
os.replace(tmp, path)
os.chmod(path, 0o600)
PY

echo "POSTGRES_BACKUP=PASS role=$ROLE file=$(basename "$FINAL") receipt=$(basename "$RECEIPT") bytes=$BYTES toc_entries=$ENTRIES fingerprint=$FINGERPRINT_AFTER external_effect=READ_ONLY_DB"
