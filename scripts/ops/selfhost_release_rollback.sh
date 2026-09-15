#!/usr/bin/env bash
# Application-only rollback for Dealix self-host production.
# Database state is never rolled back by this script.
set -Eeuo pipefail
umask 077

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." >/dev/null 2>&1 && pwd -P)"
cd "$ROOT"
MODE="${1:---dry-run}"
ENV_FILE="${ENV_FILE:-$ROOT/.env.prod}"
COMPOSE_FILE="${COMPOSE_FILE:-$ROOT/deploy/selfhost/compose.yml}"
LAST_GOOD_FILE="${LAST_GOOD_FILE:-/opt/dealix/control/state/selfhost_last_good_sha}"

log(){ printf '[selfhost-rollback] %s\n' "$*"; }
die(){ log "FAIL: $*" >&2; exit 1; }

case "$MODE" in --dry-run|--record-last-good|--real) ;; *) die "invalid mode";; esac

if [[ "$MODE" == --record-last-good ]]; then
  SHA="${DEALIX_RELEASE_SHA:-}"
  [[ "$SHA" =~ ^[0-9a-f]{40}$ ]] || die "DEALIX_RELEASE_SHA must be exact"
  mkdir -p "$(dirname "$LAST_GOOD_FILE")"
  printf '%s\n' "$SHA" > "$LAST_GOOD_FILE"
  chmod 600 "$LAST_GOOD_FILE" 2>/dev/null || true
  log "LAST_GOOD_RECORDED=$SHA"
  exit 0
fi

TARGET_SHA="${DEALIX_ROLLBACK_SHA:-}"
if [[ -z "$TARGET_SHA" && -f "$LAST_GOOD_FILE" ]]; then
  TARGET_SHA="$(tr -d '[:space:]' < "$LAST_GOOD_FILE")"
fi
[[ "$TARGET_SHA" =~ ^[0-9a-f]{40}$ ]] || die "exact rollback SHA required"
[[ -f "$ENV_FILE" ]] || die "missing production env file"
TAG="${TARGET_SHA:0:12}"
docker image inspect "dealix-api:$TAG" >/dev/null 2>&1 || die "missing dealix-api:$TAG"
docker image inspect "dealix-web:$TAG" >/dev/null 2>&1 || die "missing dealix-web:$TAG"

log "target_sha=$TARGET_SHA image_tag=$TAG database_rollback=NEVER"
if [[ "$MODE" == --dry-run ]]; then
  log "ROLLBACK_DRY_RUN=PASS"
  exit 0
fi

[[ "${CONFIRM:-}" == YES ]] || die "--real requires CONFIRM=YES"
set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a
export DEALIX_ENV_FILE="$ENV_FILE"
export DEALIX_GIT_SHA="$TARGET_SHA"
export DEALIX_IMAGE_TAG="$TAG"
export DEALIX_APP_ENV=production
COMPOSE=(docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE")
"${COMPOSE[@]}" up -d --no-build api web
API_BODY="$("${COMPOSE[@]}" exec -T api curl -fsS http://localhost:8000/version)"
WEB_BODY="$("${COMPOSE[@]}" exec -T web wget -qO- http://localhost:3000/healthz)"
python3 - "$TARGET_SHA" "$API_BODY" "$WEB_BODY" <<'PY'
import json, sys
expected, api_raw, web_raw = sys.argv[1:]
api, web = json.loads(api_raw), json.loads(web_raw)
assert api.get('git_sha') == expected
assert web.get('git_sha') == expected
PY
log "APPLICATION_ROLLBACK=PASS sha=$TARGET_SHA database_rollback=NOT_EXECUTED"
