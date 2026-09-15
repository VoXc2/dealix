#!/usr/bin/env bash
# Source-owned controller for the single canonical self-host graph.
# Safe default: --preflight. --stage/--cutover are material L5 operations and are never auto-executed.
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

log(){ printf '[selfhost-cutover] %s\n' "$*"; }
die(){ log "HOLD: $*" >&2; exit 78; }
[[ "$MODE" == --preflight || "$MODE" == --stage || "$MODE" == --cutover ]] || die "mode must be --preflight, --stage, or --cutover"
[[ "$EXPECTED_SHA" =~ ^[0-9a-f]{40}$ ]] || die "DEALIX_EXPECTED_SHA must be an exact 40-char SHA"
CURRENT_SHA="$(git rev-parse HEAD)"
[[ "$CURRENT_SHA" == "$EXPECTED_SHA" ]] || die "exact-head mismatch current=$CURRENT_SHA expected=$EXPECTED_SHA"
[[ -z "$(git status --porcelain --untracked-files=no)" ]] || die "tracked worktree is dirty"
[[ -f "$ENV_FILE" ]] || die "missing production env file: $ENV_FILE"
if [[ -n "$(find "$ENV_FILE" -maxdepth 0 -perm /077 -print -quit)" ]]; then die "production env must not be group/world accessible"; fi

set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a
export DEALIX_GIT_SHA="$EXPECTED_SHA"
export DEALIX_IMAGE_TAG="${EXPECTED_SHA:0:12}"
export DEALIX_APP_ENV=production
export DEALIX_SELFHOST_API_PORT="$API_PORT"
export DEALIX_SELFHOST_WEB_PORT="$WEB_PORT"
export COMPOSE_PROJECT_NAME="dealix-selfhost-${EXPECTED_SHA:0:12}"
COMPOSE=(docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE")

# Configuration stays safe by default because public-ingress binds loopback high ports unless --cutover explicitly overrides them.
"${COMPOSE[@]}" --profile public-cutover config >/dev/null
docker run --rm -v "$ROOT/ops/caddy/Caddyfile:/etc/caddy/Caddyfile:ro" caddy:2.11.4-alpine caddy validate --config /etc/caddy/Caddyfile >/dev/null
log "PREFLIGHT=PASS sha=$EXPECTED_SHA canonical_compose=deploy/selfhost/compose.yml public_bind=LOOPBACK_DEFAULT"
if [[ "$MODE" == --preflight ]]; then
  log "PUBLIC_CUTOVER=NOT_EXECUTED"
  exit 0
fi

[[ "${DEALIX_STAGE_PRODUCTION:-}" == YES ]] || die "$MODE requires DEALIX_STAGE_PRODUCTION=YES"
[[ "$CONFIRM_SHA" == "$EXPECTED_SHA" ]] || die "$MODE requires CONFIRM_SHA to equal DEALIX_EXPECTED_SHA"
"${COMPOSE[@]}" build --pull api web
"${COMPOSE[@]}" up -d api web

verify_json_sha(){
  local url="$1" service="$2" body
  body="$(curl -fsS "$url")" || die "health request failed: $url"
  python3 - "$EXPECTED_SHA" "$service" "$body" <<'PY'
import json, sys
sha, service, raw = sys.argv[1:]
data = json.loads(raw)
assert data.get("status") == "ok", data
assert data.get("service") == service, data
assert data.get("git_sha") == sha, data
PY
}
verify_json_sha "http://127.0.0.1:${API_PORT}/version" dealix-api
verify_json_sha "http://127.0.0.1:${WEB_PORT}/healthz" dealix-web
log "STAGE=PASS sha=$EXPECTED_SHA public_ingress=NOT_STARTED"
if [[ "$MODE" == --stage ]]; then
  log "PUBLIC_CUTOVER=NOT_EXECUTED"
  exit 0
fi

[[ "${DEALIX_PUBLIC_CUTOVER:-}" == YES ]] || die "--cutover requires DEALIX_PUBLIC_CUTOVER=YES"
export DEALIX_PUBLIC_HTTP_BIND="0.0.0.0:80"
export DEALIX_PUBLIC_HTTPS_BIND="0.0.0.0:443"
"${COMPOSE[@]}" --profile public-cutover up -d public-ingress
log "PUBLIC_INGRESS_STARTED=YES sha=$EXPECTED_SHA http=0.0.0.0:80 https=0.0.0.0:443"
log "DNS_MUTATION=NOT_EXECUTED"
log "PRODUCTION_GREEN=NOT_PROVEN"
