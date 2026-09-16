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
API_PORT="${DEALIX_SELFHOST_API_PORT:-18000}"
WEB_PORT="${DEALIX_SELFHOST_WEB_PORT:-13000}"
DB_PORT="${DEALIX_SELFHOST_DB_PORT:-15432}"

log(){ printf '[selfhost-cutover] %s\n' "$*"; }
hold(){ log "HOLD: $*" >&2; exit 78; }
[[ "$MODE" == --preflight || "$MODE" == --stage || "$MODE" == --cutover || "$MODE" == --verify-public ]] || hold "invalid mode"
[[ "$EXPECTED_SHA" =~ ^[0-9a-f]{40}$ ]] || hold "DEALIX_EXPECTED_SHA must be exact"
[[ "$(git rev-parse HEAD)" == "$EXPECTED_SHA" ]] || hold "exact-head mismatch"
[[ -z "$(git status --porcelain --untracked-files=no)" ]] || hold "tracked worktree is dirty"
[[ -f "$ENV_FILE" ]] || hold "missing production env file"
[[ -z "$(find "$ENV_FILE" -maxdepth 0 -perm /077 -print -quit)" ]] || hold "production env permissions too broad"

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
host = (u.hostname or "").lower()
if host != "postgres":
    raise SystemExit("production cutover DB must be canonical self-host postgres")
if any(marker in host for marker in ("railway", "rlwy.net")):
    raise SystemExit("Railway database cannot authorize self-host cutover")
if unquote(u.username or "") != expected_user or u.path.lstrip("/") != expected_db:
    raise SystemExit("production DB URL user/database mismatch")
if not unquote(u.password or ""):
    raise SystemExit("production DB URL password missing")
PY

export DEALIX_GIT_SHA="$EXPECTED_SHA"
export DEALIX_IMAGE_TAG="${EXPECTED_SHA:0:12}"
export DEALIX_APP_ENV=production
export DEALIX_SELFHOST_API_PORT="$API_PORT"
export DEALIX_SELFHOST_WEB_PORT="$WEB_PORT"
export DEALIX_SELFHOST_DB_PORT="$DB_PORT"
export COMPOSE_PROJECT_NAME="${DEALIX_PRODUCTION_PROJECT_NAME:-dealix-production}"
COMPOSE=(docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE")
"${COMPOSE[@]}" --profile production-db --profile public-cutover config >/dev/null
docker run --rm -v "$ROOT/ops/caddy/Caddyfile:/etc/caddy/Caddyfile:ro" \
  caddy:2.11.4-alpine caddy validate --config /etc/caddy/Caddyfile >/dev/null

# TLS bootstrap is part of the single canonical cutover plane. Public
# certificate material is inspected only for hostname/expiry metadata; private
# keys are never read. A random or expired .crt must never satisfy readiness.
PUBLIC_INGRESS_CID="$("${COMPOSE[@]}" --profile public-cutover ps -q public-ingress 2>/dev/null || true)"
ORIGIN_TLS_CERT_STORAGE="MISSING_OR_UNPROVEN"
ORIGIN_TLS_REQUIRED_HOSTS=("dealix.me" "www.dealix.me" "api.dealix.me")
cert_storage_covers_host(){
  local cid="$1" host="$2" cert_path
  while IFS= read -r cert_path; do
    [[ -n "$cert_path" ]] || continue
    if docker exec "$cid" cat "$cert_path" 2>/dev/null \
      | openssl x509 -noout -checkend 86400 -checkhost "$host" >/dev/null 2>&1; then
      return 0
    fi
  done < <(docker exec "$cid" sh -lc 'find /data/caddy/certificates -type f -name "*.crt" -print 2>/dev/null' 2>/dev/null || true)
  return 1
}
if [[ -n "$PUBLIC_INGRESS_CID" ]] && docker inspect -f '{{.State.Running}}' "$PUBLIC_INGRESS_CID" 2>/dev/null | grep -qx true; then
  ORIGIN_TLS_CERT_STORAGE="VALID_HOST_CERTS_PRESENT"
  for host in "${ORIGIN_TLS_REQUIRED_HOSTS[@]}"; do
    if ! cert_storage_covers_host "$PUBLIC_INGRESS_CID" "$host"; then
      ORIGIN_TLS_CERT_STORAGE="MISSING_OR_UNPROVEN"
      break
    fi
  done
fi
TLS_BOOTSTRAP_STRATEGY="${DEALIX_TLS_BOOTSTRAP_STRATEGY:-UNSET}"
case "$TLS_BOOTSTRAP_STRATEGY" in
  UNSET|managed_cert_present|public_acme_after_dns) ;;
  *) hold "invalid DEALIX_TLS_BOOTSTRAP_STRATEGY (allowed: managed_cert_present, public_acme_after_dns)" ;;
esac
log "ORIGIN_TLS_CERT_STORAGE=$ORIGIN_TLS_CERT_STORAGE"
log "TLS_BOOTSTRAP_STRATEGY=$TLS_BOOTSTRAP_STRATEGY"
if [[ "$ORIGIN_TLS_CERT_STORAGE" == VALID_HOST_CERTS_PRESENT ]]; then
  log "TLS_BOOTSTRAP_REQUIRED=NO"
else
  log "TLS_BOOTSTRAP_REQUIRED=YES"
fi
log "PREFLIGHT=PASS sha=$EXPECTED_SHA project=$COMPOSE_PROJECT_NAME public_bind=LOOPBACK_DEFAULT"

verify_public_json_sha(){
  local url="$1" service="$2" body
  body="$(curl --proto '=https' --tlsv1.2 -fsS --max-time 20 "$url")" || return 1
  python3 - "$EXPECTED_SHA" "$service" "$body" <<'PY2'
import json, sys
expected, service, raw = sys.argv[1:]
data = json.loads(raw)
if data.get("status") != "ok" or data.get("service") != service or data.get("git_sha") != expected:
    raise SystemExit(1)
PY2
}

if [[ "$MODE" == --verify-public ]]; then
  # Strict system trust is intentional: certificate-verification bypass is forbidden.
  # is the post-DNS proof gate, not a connectivity smoke test.
  PUBLIC_VERIFY_OK=1
  verify_public_json_sha "https://dealix.me/healthz" dealix-web || PUBLIC_VERIFY_OK=0
  verify_public_json_sha "https://api.dealix.me/version" dealix-api || PUBLIC_VERIFY_OK=0
  if ! curl --proto '=https' --tlsv1.2 -fsSL --max-time 20 -o /dev/null "https://www.dealix.me/"; then
    PUBLIC_VERIFY_OK=0
  fi
  if [[ "$PUBLIC_VERIFY_OK" != 1 ]]; then
    log "PUBLIC_TLS_EXACT_SHA=FAIL sha=$EXPECTED_SHA"
    log "ROLLBACK_REQUIRED=YES"
    log "ROLLBACK_ACTION=RESTORE_PREVIOUS_DNS_ORIGIN"
    hold "strict public TLS and exact-SHA verification failed"
  fi
  log "PUBLIC_TLS_EXACT_SHA=PASS sha=$EXPECTED_SHA"
  log "ROLLBACK_REQUIRED=NO"
  log "PRODUCTION_GREEN=NOT_PROVEN"
  exit 0
fi

if [[ "$MODE" == --preflight ]]; then
  log "PUBLIC_CUTOVER=NOT_EXECUTED"
  exit 0
fi

[[ "${DEALIX_STAGE_PRODUCTION:-}" == YES ]] || hold "$MODE requires DEALIX_STAGE_PRODUCTION=YES"
[[ "$CONFIRM_SHA" == "$EXPECTED_SHA" ]] || hold "CONFIRM_SHA must equal exact release SHA"
if [[ "$MODE" == --stage ]]; then
  ACTION_ID="dealix-production-stage-v1:${EXPECTED_SHA}"
else
  ACTION_ID="dealix-public-cutover-v1:${EXPECTED_SHA}"
fi
[[ "${DEALIX_L5_APPROVAL_ACTION:-}" == "$ACTION_ID" ]] || hold "exact action-bound approval required: DEALIX_L5_APPROVAL_ACTION=$ACTION_ID"
DATA_RECEIPT="${DEALIX_DATA_MIGRATION_RECEIPT:-}"
[[ -n "$DATA_RECEIPT" && -f "$DATA_RECEIPT" ]] || hold "production data migration receipt required"
mapfile -t MIGRATION < <(python3 - "$DATA_RECEIPT" "$EXPECTED_SHA" <<'PY'
import hashlib, json, os, stat, sys
from datetime import UTC, datetime
path, expected = sys.argv[1:]
if stat.S_IMODE(os.stat(path).st_mode) & 0o077:
    raise SystemExit("migration receipt permissions too broad")
data = json.load(open(path, encoding="utf-8")); signature = data.pop("payload_sha256", "")
canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
if signature != hashlib.sha256(canonical).hexdigest(): raise SystemExit("migration receipt integrity failure")
if data.get("schema_version") != "dealix.railway-data-migration-receipt.v1" or data.get("status") != "PASS": raise SystemExit("migration receipt invalid")
if data.get("migration_mode") != "production" or data.get("target_release_sha") != expected: raise SystemExit("migration receipt release/mode mismatch")
if data.get("publication_consent_inferred") is not False: raise SystemExit("publication consent invariant failed")
if int(data.get("public_consent_true", -1)) != 0 or int(data.get("approval_not_required", -1)) != 0: raise SystemExit("proof governance invariant failed")
if int(data.get("source_rows", -1)) != int(data.get("archived_rows", -2)): raise SystemExit("migration row parity failed")
expiry = datetime.fromisoformat(str(data["expires_at"]).replace("Z", "+00:00")).astimezone(UTC)
if datetime.now(UTC) > expiry: raise SystemExit("migration receipt expired")
print(data["archived_rows"]); print(data["typed_proof"]); print(data["typed_conversations"]); print(data["target_alembic_head"])
PY
)
[[ "${#MIGRATION[@]}" == 4 ]] || hold "migration receipt parse failed"
"${COMPOSE[@]}" --profile production-db up -d postgres
for _ in $(seq 1 30); do
  if "${COMPOSE[@]}" --profile production-db exec -T postgres \
    pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" >/dev/null 2>&1; then break; fi
  sleep 2
done
"${COMPOSE[@]}" --profile production-db exec -T postgres \
  pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" >/dev/null || hold "production postgres not ready"

DB_STATE="$("${COMPOSE[@]}" --profile production-db exec -T postgres \
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Atc \
  "select coalesce((select version_num from alembic_version limit 1),'')||'|'||(select count(*) from operational_event_streams where stream_id='railway_legacy_20260915')||'|'||(select count(*) from proof_events where evidence_source='railway_production_backup')||'|'||(select count(*) from conversations where id like 'legacy:%')")" || hold "production DB migration evidence query failed"
IFS='|' read -r DB_HEAD DB_ARCHIVED DB_PROOF DB_CONVERSATIONS <<< "$DB_STATE"
[[ "$DB_HEAD" == "${MIGRATION[3]}" ]] || hold "production DB Alembic head mismatch"
[[ "$DB_ARCHIVED" == "${MIGRATION[0]}" ]] || hold "production DB archived row mismatch"
[[ "$DB_PROOF" == "${MIGRATION[1]}" ]] || hold "production DB proof row mismatch"
[[ "$DB_CONVERSATIONS" == "${MIGRATION[2]}" ]] || hold "production DB conversation row mismatch"

"${COMPOSE[@]}" build --pull api web
"${COMPOSE[@]}" up -d api web
verify_json_sha(){
  local url="$1" service="$2" body
  body="$(curl -fsS "$url")" || hold "health request failed: $url"
  python3 - "$EXPECTED_SHA" "$service" "$body" <<'PY'
import json, sys
expected, service, raw = sys.argv[1:]
data = json.loads(raw)
if data.get("status") != "ok" or data.get("service") != service or data.get("git_sha") != expected:
    raise SystemExit(1)
PY
}
verify_json_sha "http://127.0.0.1:${API_PORT}/version" dealix-api
verify_json_sha "http://127.0.0.1:${WEB_PORT}/healthz" dealix-web
log "STAGE=PASS sha=$EXPECTED_SHA db_migration_receipt=PASS public_ingress=NOT_STARTED"
if [[ "$MODE" == --stage ]]; then
  log "PUBLIC_CUTOVER=NOT_EXECUTED"
  exit 0
fi

[[ "${DEALIX_PUBLIC_CUTOVER:-}" == YES ]] || hold "DEALIX_PUBLIC_CUTOVER=YES required"
# Public ingress may be exposed before DNS only when the TLS bootstrap state is
# explicit.  The controller still never mutates DNS.  With public ACME, Caddy
# can obtain a certificate only after the separately-authorized DNS move makes
# the hostname reach this origin, so strict --verify-public is mandatory next.
if [[ "$TLS_BOOTSTRAP_STRATEGY" == managed_cert_present ]]; then
  [[ "$ORIGIN_TLS_CERT_STORAGE" == VALID_HOST_CERTS_PRESENT ]] || hold "managed_cert_present requires unexpired hostname-matching certificates for dealix.me/www/api in Caddy storage"
elif [[ "$TLS_BOOTSTRAP_STRATEGY" == public_acme_after_dns ]]; then
  log "TLS_BOOTSTRAP_PHASE=PENDING_DNS"
else
  hold "cutover requires explicit DEALIX_TLS_BOOTSTRAP_STRATEGY=managed_cert_present|public_acme_after_dns"
fi
SOURCE_RECEIPT="${DEALIX_SOURCE_BACKUP_RECEIPT:-}"
TARGET_RECEIPT="${DEALIX_SELFHOST_BACKUP_RECEIPT:-}"
QUIET_RECEIPT="${DEALIX_QUIESCENCE_RECEIPT:-}"
for receipt in "$SOURCE_RECEIPT" "$TARGET_RECEIPT" "$QUIET_RECEIPT"; do
  [[ -n "$receipt" && -f "$receipt" ]] || hold "complete cutover receipt set required"
done
python3 scripts/ops/verify_selfhost_cutover_receipts.py \
  --expected-sha "$EXPECTED_SHA" \
  --source-backup-receipt "$SOURCE_RECEIPT" \
  --migration-receipt "$DATA_RECEIPT" \
  --selfhost-backup-receipt "$TARGET_RECEIPT" \
  --quiescence-receipt "$QUIET_RECEIPT" || hold "cutover receipts failed"

export DEALIX_PUBLIC_HTTP_BIND="0.0.0.0:80"
export DEALIX_PUBLIC_HTTPS_BIND="0.0.0.0:443"
"${COMPOSE[@]}" --profile public-cutover up -d public-ingress
ss -lntH | awk '{print $4}' | grep -Eq '(^|:)(80)$' || hold "public port 80 not listening"
ss -lntH | awk '{print $4}' | grep -Eq '(^|:)(443)$' || hold "public port 443 not listening"
log "PUBLIC_INGRESS_STARTED=YES sha=$EXPECTED_SHA http=0.0.0.0:80 https=0.0.0.0:443"
log "DNS_MUTATION=NOT_EXECUTED"
log "POST_DNS_PUBLIC_VERIFY=REQUIRED command=selfhost_public_cutover.sh--verify-public"
log "ROLLBACK_ON_TLS_OR_SHA_FAILURE=RESTORE_PREVIOUS_DNS_ORIGIN"
log "RAILWAY_DECOMMISSION=NOT_EXECUTED"
log "PRODUCTION_GREEN=NOT_PROVEN"
