#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

PROJECT="${DEALIX_RAILWAY_PROJECT:?set DEALIX_RAILWAY_PROJECT}"
ENVIRONMENT="${DEALIX_RAILWAY_ENVIRONMENT:?set DEALIX_RAILWAY_ENVIRONMENT}"
SERVICE="${DEALIX_RAILWAY_POSTGRES_SERVICE:?set DEALIX_RAILWAY_POSTGRES_SERVICE}"
SOURCE_RECEIPT="${DEALIX_SOURCE_BACKUP_RECEIPT:?set DEALIX_SOURCE_BACKUP_RECEIPT}"
OUT="${DEALIX_QUIESCENCE_RECEIPT_PATH:?set DEALIX_QUIESCENCE_RECEIPT_PATH}"
EXPECTED_SHA="${DEALIX_EXPECTED_SHA:?set DEALIX_EXPECTED_SHA}"
PG_IMAGE="pgvector/pgvector:pg18@sha256:2ba9ca5f2e7daa0f0e7723cba1ee9167bab54efd3640516a44ac1a928dd67e7a"
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." >/dev/null 2>&1 && pwd -P)"
SQL="$ROOT/scripts/ops/postgres_database_fingerprint.sql"

hold(){ echo "RAILWAY_QUIESCENCE=HOLD reason=$1" >&2; exit "${2:-64}"; }
[[ "$EXPECTED_SHA" =~ ^[0-9a-f]{40}$ ]] || hold "invalid_expected_sha"
[[ "$(cd "$ROOT" && git rev-parse HEAD)" == "$EXPECTED_SHA" ]] || hold "exact_head_mismatch" 65
[[ -f "$SOURCE_RECEIPT" ]] || hold "source_receipt_missing" 66
[[ -f "$SQL" ]] || hold "fingerprint_sql_missing" 66
command -v railway >/dev/null 2>&1 || hold "railway_cli_missing" 69
command -v docker >/dev/null 2>&1 || hold "docker_missing" 69

mapfile -t SOURCE < <(python3 - "$SOURCE_RECEIPT" "$EXPECTED_SHA" <<'PY'
import hashlib, json, os, stat, sys
from datetime import UTC, datetime, timedelta
p, expected = sys.argv[1:]
mode = stat.S_IMODE(os.stat(p).st_mode)
if mode & 0o077:
    raise SystemExit("source receipt permissions are too broad")
data = json.load(open(p, encoding="utf-8"))
sig = str(data.pop("payload_sha256", ""))
canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
if sig != hashlib.sha256(canonical).hexdigest():
    raise SystemExit("source receipt integrity failure")
if data.get("schema_version") != "dealix.railway-source-backup-receipt.v1":
    raise SystemExit("source receipt schema mismatch")
if data.get("status") != "PASS" or data.get("backup_role") != "railway-source":
    raise SystemExit("source receipt not PASS")
if data.get("release_sha") != expected:
    raise SystemExit("source receipt release mismatch")
if data.get("pg_restore_list") != "PASS" or int(data.get("postgres_major", 0)) != 18:
    raise SystemExit("source receipt restore/version invalid")
if data.get("pgvector_required") is not True:
    raise SystemExit("source receipt pgvector authority missing")
text = str(data.get("source_snapshot_started_at") or "").replace("Z", "+00:00")
started = datetime.fromisoformat(text).astimezone(UTC)
now = datetime.now(UTC)
if started > now + timedelta(minutes=1) or now - started > timedelta(minutes=30):
    raise SystemExit("source receipt outside 30-minute cutover window")
fp = str(data.get("database_fingerprint_sha256") or "")
sha = str(data.get("dump_sha256") or "")
if len(fp) != 64 or len(sha) != 64:
    raise SystemExit("source receipt lacks fingerprint/sha")
print(fp); print(sha)
PY
)
[[ "${#SOURCE[@]}" == 2 ]] || hold "source_receipt_invalid" 66
EXPECTED_FINGERPRINT="${SOURCE[0]}"; SOURCE_SHA="${SOURCE[1]}"
TMP_JSON="$(mktemp)"; TMP_ENV="$(mktemp)"
cleanup(){ rm -f "$TMP_JSON" "$TMP_ENV"; }
trap cleanup EXIT
chmod 600 "$TMP_JSON" "$TMP_ENV"
railway variable list -p "$PROJECT" -e "$ENVIRONMENT" -s "$SERVICE" --json > "$TMP_JSON"
python3 - "$TMP_JSON" "$TMP_ENV" <<'PY'
import json, sys
from urllib.parse import parse_qs, unquote, urlparse
data = json.load(open(sys.argv[1], encoding="utf-8"))
url = data.get("DATABASE_PUBLIC_URL") or data.get("DATABASE_URL") or ""
u = urlparse(url); query = parse_qs(u.query)
values = {
    "PGHOST": u.hostname or "",
    "PGPORT": str(u.port or 5432),
    "PGUSER": unquote(u.username or ""),
    "PGPASSWORD": unquote(u.password or ""),
    "PGDATABASE": u.path.lstrip("/"),
    "PGSSLMODE": query.get("sslmode", ["prefer"])[0],
}
if not all(values[k] for k in ("PGHOST", "PGUSER", "PGPASSWORD", "PGDATABASE")):
    raise SystemExit("incomplete Railway DB connection")
with open(sys.argv[2], "w", encoding="utf-8") as handle:
    for key, value in values.items():
        if "\n" in value:
            raise SystemExit("invalid DB connection field")
        handle.write(f"{key}={value}\n")
PY
chmod 600 "$TMP_ENV"
LINES="$(docker run --rm --env-file "$TMP_ENV" -v "$SQL:/fingerprint.sql:ro" "$PG_IMAGE" psql -X -qAt -f /fingerprint.sql)"
LIVE_FINGERPRINT="$(printf '%s\n' "$LINES" | sha256sum | cut -d' ' -f1)"
[[ "$LIVE_FINGERPRINT" == "$EXPECTED_FINGERPRINT" ]] || hold "live_source_changed" 67
python3 - "$OUT" "$EXPECTED_SHA" "$SOURCE_SHA" "$LIVE_FINGERPRINT" <<'PY'
import hashlib, json, os, sys
from datetime import UTC, datetime, timedelta
path, release, source_sha, fingerprint = sys.argv[1:]
now = datetime.now(UTC)
payload = {
    "schema_version": "dealix.railway-quiescence-receipt.v1",
    "status": "PASS",
    "target_release_sha": release,
    "source_backup_sha256": source_sha,
    "database_fingerprint_sha256": fingerprint,
    "checked_at": now.isoformat().replace("+00:00", "Z"),
    "expires_at": (now + timedelta(minutes=5)).isoformat().replace("+00:00", "Z"),
}
canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
payload["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
tmp = path + ".tmp"
with open(tmp, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2, sort_keys=True)
    handle.write("\n")
os.chmod(tmp, 0o600); os.replace(tmp, path); os.chmod(path, 0o600)
PY

echo "RAILWAY_QUIESCENCE=PASS fingerprint=$LIVE_FINGERPRINT receipt=$OUT"
