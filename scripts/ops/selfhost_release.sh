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
log(){ printf "[selfhost-release] %s\n" "$*"; }
hold(){ log "HOLD: $*" >&2; exit 78; }
[[ "$MODE" == --preflight || "$MODE" == --deploy ]] || hold "invalid mode"
[[ "$EXPECTED_SHA" =~ ^[0-9a-f]{40}$ ]] || hold "DEALIX_EXPECTED_SHA must be exact"
[[ "$(git rev-parse HEAD)" == "$EXPECTED_SHA" ]] || hold "exact-head mismatch"
[[ -z "$(git status --porcelain --untracked-files=no)" ]] || hold "tracked worktree is dirty"
[[ -f "$ENV_FILE" ]] || hold "missing production env"
[[ -z "$(find "$ENV_FILE" -maxdepth 0 -perm /077 -print -quit)" ]] || hold "production env permissions too broad"
set -a; source "$ENV_FILE"; set +a
: "${POSTGRES_USER:?missing POSTGRES_USER}"; : "${POSTGRES_DB:?missing POSTGRES_DB}"; : "${POSTGRES_PASSWORD:?missing POSTGRES_PASSWORD}"; : "${DEALIX_DATABASE_URL:?missing DEALIX_DATABASE_URL}"
python3 - <<PY
import os
from urllib.parse import urlparse
u=urlparse(os.environ["DEALIX_DATABASE_URL"].replace("postgresql+asyncpg://","postgresql://",1))
if (u.hostname or "").lower() != "postgres": raise SystemExit("DEALIX_DATABASE_URL must use self-host postgres service")
PY
export DEALIX_GIT_SHA="$EXPECTED_SHA" DEALIX_RELEASE_SHA="$EXPECTED_SHA" DEALIX_IMAGE_TAG="${EXPECTED_SHA:0:12}" DEALIX_APP_ENV=production
export DEALIX_PUBLIC_HTTP_BIND="0.0.0.0:80" DEALIX_PUBLIC_HTTPS_BIND="0.0.0.0:443"
export COMPOSE_PROJECT_NAME="${DEALIX_PRODUCTION_PROJECT_NAME:-dealix-production}"
COMPOSE=(docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE")
"${COMPOSE[@]}" --profile production-db --profile public-cutover config >/dev/null
docker run --rm -v "$ROOT/ops/caddy/Caddyfile:/etc/caddy/Caddyfile:ro" caddy:2.11.4-alpine caddy validate --config /etc/caddy/Caddyfile >/dev/null
python3 scripts/ops/verify_selfhost_only_runtime.py
python3 scripts/ops/verify_selfhosted_production_plane.py
log "PREFLIGHT=PASS sha=$EXPECTED_SHA authority=selfhost-only"
[[ "$MODE" == --deploy ]] || exit 0
[[ "$CONFIRM_SHA" == "$EXPECTED_SHA" ]] || hold "CONFIRM_SHA must equal exact release SHA"
[[ "${DEALIX_L5_APPROVAL_ACTION:-}" == "dealix-selfhost-release-v1:${EXPECTED_SHA}" ]] || hold "exact release approval missing"
PREV_API="$(curl -fsS http://127.0.0.1:${DEALIX_SELFHOST_API_PORT:-18000}/version 2>/dev/null || true)"
PREV_SHA="$(python3 -c 'import json,sys; print(json.loads(sys.stdin.read()).get("git_sha", ""))' <<<"$PREV_API" 2>/dev/null || true)"
if [[ "$PREV_SHA" =~ ^[0-9a-f]{40}$ ]]; then DEALIX_RELEASE_SHA="$PREV_SHA" bash scripts/ops/selfhost_release_rollback.sh --record-last-good; fi
"${COMPOSE[@]}" --profile production-db up -d postgres
for _ in $(seq 1 30); do "${COMPOSE[@]}" exec -T postgres pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" >/dev/null 2>&1 && break; sleep 2; done
"${COMPOSE[@]}" exec -T postgres pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" >/dev/null || hold "postgres not ready"
"${COMPOSE[@]}" build --pull api web
"${COMPOSE[@]}" up -d api web
"${COMPOSE[@]}" --profile public-cutover up -d public-ingress
python3 - "$EXPECTED_SHA" <<PY
import json,sys,urllib.request,time
expected=sys.argv[1]
def get(url):
    for _ in range(30):
        try:
            with urllib.request.urlopen(url, timeout=5) as r: return json.load(r)
        except Exception: time.sleep(2)
    raise SystemExit("health timeout: "+url)
api=get("http://127.0.0.1:18000/version"); web=get("http://127.0.0.1:13000/healthz")
assert api.get("git_sha")==expected, api
assert web.get("git_sha")==expected, web
PY
python3 - "$EXPECTED_SHA" "${DEALIX_DOMAIN:-dealix.me}" "${DEALIX_API_DOMAIN:-api.dealix.me}" <<'PY_PUBLIC'
import json, sys, urllib.request
expected, web_domain, api_domain = sys.argv[1:4]
def exact(url):
    with urllib.request.urlopen(url, timeout=10) as r:
        payload = json.load(r)
    actual = payload.get("git_sha")
    if actual != expected:
        raise SystemExit(f"public exact-SHA mismatch: {url} expected={expected} actual={actual}")
exact(f"https://{web_domain}/healthz")
exact(f"https://{api_domain}/version")
PY_PUBLIC
log "SELFHOST_RELEASE=PASS sha=$EXPECTED_SHA previous_sha=${PREV_SHA:-unknown} public_exact_sha=PASS"
