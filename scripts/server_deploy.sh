#!/usr/bin/env bash
# Dealix self-host production deploy. Safe default: preflight only.
set -Eeuo pipefail
umask 077
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." >/dev/null 2>&1 && pwd -P)"
cd "$ROOT"
MODE="${1:---preflight}"
ENV_FILE="${ENV_FILE:-$ROOT/.env.prod}"
COMPOSE_FILE="${COMPOSE_FILE:-$ROOT/docker-compose.prod.yml}"
EXPECTED_SHA="${DEALIX_EXPECTED_SHA:-}"
log(){ printf '[selfhost-deploy] %s\n' "$*"; }
die(){ log "FAIL: $*" >&2; exit 1; }
case "$MODE" in --preflight|--stage|--cutover) ;; *) die "mode must be --preflight, --stage, or --cutover";; esac
[[ "$EXPECTED_SHA" =~ ^[0-9a-f]{40}$ ]] || die "DEALIX_EXPECTED_SHA must be an exact 40-char SHA"
CURRENT_SHA="$(git rev-parse HEAD)"
[[ "$CURRENT_SHA" == "$EXPECTED_SHA" ]] || die "exact-head mismatch current=$CURRENT_SHA expected=$EXPECTED_SHA"
[[ -f "$ENV_FILE" ]] || die "missing $ENV_FILE; copy .env.prod.example and populate secrets outside Git"
[[ -f "$COMPOSE_FILE" ]] || die "missing $COMPOSE_FILE"
set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a
required=(APP_SECRET_KEY JWT_SECRET_KEY API_KEYS ADMIN_API_KEYS POSTGRES_PASSWORD REDIS_PASSWORD)
for key in "${required[@]}"; do
  value="${!key:-}"
  [[ -n "$value" ]] || die "$key is empty"
  [[ "$value" != *CHANGE_ME* ]] || die "$key still contains CHANGE_ME"
done
[[ "${#APP_SECRET_KEY}" -ge 32 ]] || die "APP_SECRET_KEY must be at least 32 chars"
[[ "${#JWT_SECRET_KEY}" -ge 32 ]] || die "JWT_SECRET_KEY must be at least 32 chars"
[[ "${APP_ENV:-}" == production ]] || die "APP_ENV must be production"
[[ "${EXTERNAL_SEND_ENABLED:-false}" == false ]] || die "EXTERNAL_SEND_ENABLED must remain false for cutover"
[[ "${WHATSAPP_ALLOW_LIVE_SEND:-false}" == false ]] || die "WHATSAPP_ALLOW_LIVE_SEND must remain false for cutover"
[[ "${PAYMENT_EXECUTION:-0}" == 0 ]] || die "PAYMENT_EXECUTION must remain 0 for cutover"
export DEALIX_ENV_FILE="$ENV_FILE"
export GIT_SHA="$EXPECTED_SHA"
export IMAGE_TAG="${EXPECTED_SHA:0:12}"
COMPOSE=(docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE")
log "mode=$MODE sha=$EXPECTED_SHA image_tag=$IMAGE_TAG"
"${COMPOSE[@]}" config -q
"${COMPOSE[@]}" run --rm --no-deps --entrypoint caddy caddy validate --config /etc/caddy/Caddyfile >/dev/null
"${COMPOSE[@]}" build api web
log "PREFLIGHT=PASS"
if [[ "$MODE" == --preflight ]]; then log "PUBLIC_CUTOVER=NOT_EXECUTED"; exit 0; fi
"${COMPOSE[@]}" up -d postgres redis pgbouncer api web
for _ in $(seq 1 60); do
  if "${COMPOSE[@]}" exec -T api curl -fsS http://localhost:8000/healthz >/dev/null 2>&1 && "${COMPOSE[@]}" exec -T web wget -qO- http://localhost:3000/healthz >/dev/null 2>&1; then break; fi
  sleep 2
done
API_BODY="$("${COMPOSE[@]}" exec -T api curl -fsS http://localhost:8000/version)"
WEB_BODY="$("${COMPOSE[@]}" exec -T web wget -qO- http://localhost:3000/healthz)"
python3 - "$EXPECTED_SHA" "$API_BODY" "$WEB_BODY" <<'PY'
import json, sys
expected, api_raw, web_raw = sys.argv[1:]
api, web = json.loads(api_raw), json.loads(web_raw)
assert api.get('status') == 'ok' and api.get('service') == 'dealix-api'
assert web.get('status') == 'ok' and web.get('service') == 'dealix-web'
assert api.get('git_sha') == expected
assert web.get('git_sha') == expected
PY
"${COMPOSE[@]}" exec -T postgres pg_isready -U "${POSTGRES_USER:-dealix}" -d "${POSTGRES_DB:-dealix}" >/dev/null
"${COMPOSE[@]}" exec -T redis redis-cli -a "$REDIS_PASSWORD" ping 2>/dev/null | grep -qx PONG
log "SELFHOST_STAGE=PASS sha=$EXPECTED_SHA"
if [[ "$MODE" == --stage ]]; then log "PUBLIC_CUTOVER=NOT_EXECUTED"; exit 0; fi
[[ "${DEALIX_PUBLIC_CUTOVER:-}" == YES ]] || die "--cutover requires DEALIX_PUBLIC_CUTOVER=YES"
"${COMPOSE[@]}" up -d caddy
log "PUBLIC_INGRESS_STARTED=PASS"
log "PUBLIC_CUTOVER=EXECUTED_REQUIRES_DNS_AND_EXTERNAL_PARITY_VERIFICATION"
