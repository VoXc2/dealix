#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd -P)"
DEFAULT_REPO="$(cd -- "$SCRIPT_DIR/../.." >/dev/null 2>&1 && pwd -P)"
REPO="${DEALIX_REPO:-$DEFAULT_REPO}"
COMPOSE_FILE="$REPO/deploy/selfhost/compose.yml"
# shellcheck source=selfhost_canary_project_name.sh
source "$REPO/scripts/ops/selfhost_canary_project_name.sh"
EXPECTED_SHA="${DEALIX_EXPECTED_SHA:-}"
RUN_ID="${DEALIX_CANARY_RUN_ID:-}"
INGRESS_PORT="${DEALIX_SELFHOST_INGRESS_PORT:-18081}"

if [[ -z "$EXPECTED_SHA" ]]; then
  echo "HOLD: DEALIX_EXPECTED_SHA is required" >&2
  exit 64
fi
if [[ -z "$RUN_ID" ]]; then
  echo "HOLD: DEALIX_CANARY_RUN_ID is required; use run_selfhosted_private_release_canary.sh" >&2
  exit 64
fi
cd "$REPO"
if [[ "$(git rev-parse HEAD)" != "$EXPECTED_SHA" ]]; then
  echo "HOLD: exact-head mismatch" >&2
  exit 65
fi

export DEALIX_GIT_SHA="$EXPECTED_SHA"
COMPOSE_PROJECT_NAME="$(dealix_canary_project_name "$EXPECTED_SHA" "$RUN_ID")"
export COMPOSE_PROJECT_NAME
docker compose -f "$COMPOSE_FILE" --profile ingress-canary up -d ingress

probe_host() {
  local host="$1"
  local path="$2"
  local body=""
  for _ in $(seq 1 30); do
    if body="$(curl -fsS --max-time 3 -H "Host: $host" "http://127.0.0.1:$INGRESS_PORT$path" 2>/dev/null)"; then
      printf '%s' "$body"
      return 0
    fi
    sleep 1
  done
  echo "FAIL: ingress canary not ready host=$host path=$path" >&2
  docker compose -f "$COMPOSE_FILE" --profile ingress-canary ps >&2 || true
  return 66
}

api_body="$(probe_host api.dealix.me /version)"
web_body="$(probe_host dealix.me /healthz)"
python3 - "$EXPECTED_SHA" "$api_body" "$web_body" <<'PY'
import json, sys
expected, api_raw, web_raw = sys.argv[1:]
api = json.loads(api_raw)
web = json.loads(web_raw)
assert api.get("status") == "ok"
assert api.get("service") == "dealix-api"
assert api.get("git_sha") == expected
assert web.get("status") == "ok"
assert web.get("service") == "dealix-web"
assert web.get("git_sha") == expected
PY

if ss -ltn | grep -Eq "(^|[[:space:]])0\\.0\\.0\\.0:${INGRESS_PORT}([[:space:]]|$)"; then
  echo "FAIL: ingress canary exposed publicly" >&2
  exit 67
fi

echo "SELFHOST_INGRESS_CANARY=PASS"
echo "COMPOSE_PROJECT_NAME=$COMPOSE_PROJECT_NAME"
echo "DEALIX_CANARY_RUN_ID=$RUN_ID"
echo "INGRESS=http://127.0.0.1:$INGRESS_PORT"
echo "PUBLIC_PORTS_80_443=NOT_OPENED_BY_THIS_RUNNER"
