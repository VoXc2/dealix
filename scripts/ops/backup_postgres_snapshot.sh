#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

URL_FILE="${DEALIX_DATABASE_URL_FILE:-}"
OUT_DIR="${DEALIX_POSTGRES_BACKUP_DIR:-/opt/dealix/control/backups/postgres}"
CLIENT_IMAGE="${DEALIX_POSTGRES_CLIENT_IMAGE:-postgres:18-alpine}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"

if [[ -z "$URL_FILE" || ! -f "$URL_FILE" ]]; then
  echo "HOLD: DEALIX_DATABASE_URL_FILE must name an existing secret file" >&2
  exit 64
fi
if [[ -n "$(find "$URL_FILE" -maxdepth 0 -perm /077 -print -quit)" ]]; then
  echo "HOLD: database URL file must not be group/world accessible" >&2
  exit 65
fi
if ! command -v docker >/dev/null 2>&1; then
  echo "HOLD: docker is required for the pinned PostgreSQL client" >&2
  exit 69
fi

mkdir -p "$OUT_DIR"
TMP_BASE="${DEALIX_SECURE_TMP_DIR:-/opt/dealix/control/tmp}"
mkdir -p "$TMP_BASE"
chmod 700 "$TMP_BASE"
TMP_DIR="$(mktemp -d "$TMP_BASE/postgres-backup.XXXXXX")"
chmod 700 "$TMP_DIR"
cleanup() { rm -rf "$TMP_DIR"; }
trap cleanup EXIT
PASSWORD_FILE="$TMP_DIR/password"
mapfile -d '' -t PARTS < <(python3 - "$URL_FILE" "$PASSWORD_FILE" <<'PY'
import pathlib, sys, urllib.parse
url_path, password_path = map(pathlib.Path, sys.argv[1:])
raw = url_path.read_text(encoding="utf-8").strip()
u = urllib.parse.urlparse(raw)
if not u.scheme.startswith("postgresql") or not u.hostname or not u.username or not u.path.strip("/"):
    raise SystemExit("invalid PostgreSQL URL")
host = u.hostname
port = str(u.port or 5432)
user = urllib.parse.unquote(u.username)
password = urllib.parse.unquote(u.password or "")
database = u.path.lstrip("/")
query = urllib.parse.parse_qs(u.query)
sslmode = (query.get("sslmode") or ["prefer"])[0]
password_path.write_text(password, encoding="utf-8")
password_path.chmod(0o600)
for value in (host, port, user, database, sslmode):
    sys.stdout.buffer.write(value.encode() + b"\0")
PY
)
if (( ${#PARTS[@]} != 5 )); then
  echo "HOLD: database URL parsing failed" >&2
  exit 66
fi
PGHOST="${PARTS[0]}"; PGPORT="${PARTS[1]}"; PGUSER="${PARTS[2]}"; PGDATABASE="${PARTS[3]}"; PGSSLMODE="${PARTS[4]}"
export PGHOST PGPORT PGUSER PGDATABASE PGSSLMODE
FINAL="$OUT_DIR/postgres-$STAMP.pgdump"
TMP_DUMP="$OUT_DIR/.postgres-$STAMP.pgdump.tmp"
HOST_UID="$(id -u)"
HOST_GID="$(id -g)"

docker run --rm --network host --user "$HOST_UID:$HOST_GID" \
  -e PGHOST -e PGPORT -e PGUSER -e PGDATABASE -e PGSSLMODE \
  -v "$TMP_DIR:/run/dealix-secrets:ro" \
  "$CLIENT_IMAGE" sh -ceu 'export PGPASSWORD="$(cat /run/dealix-secrets/password)"; exec pg_dump -Fc --no-owner --no-acl' > "$TMP_DUMP"

test -s "$TMP_DUMP"
chmod 600 "$TMP_DUMP"
mv "$TMP_DUMP" "$FINAL"
sha256sum "$FINAL" > "$FINAL.sha256"
chmod 600 "$FINAL.sha256"
sha256sum -c "$FINAL.sha256" >/dev/null

docker run --rm --user "$HOST_UID:$HOST_GID" -v "$OUT_DIR:/backup:ro" "$CLIENT_IMAGE" \
  pg_restore --list "/backup/$(basename "$FINAL")" > "$TMP_DIR/toc"
ENTRIES="$(grep -vc '^;' "$TMP_DIR/toc" || true)"
BYTES="$(stat -c %s "$FINAL")"

echo "POSTGRES_BACKUP=PASS file=$(basename "$FINAL") bytes=$BYTES toc_entries=$ENTRIES checksum=$(basename "$FINAL").sha256 external_effect=READ_ONLY_DB"
