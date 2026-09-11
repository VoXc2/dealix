#!/usr/bin/env bash
set -Eeuo pipefail

REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
COMPOSE_FILE="$REPO/deploy/selfhost/compose.yml"
EXPECTED_SHA="${DEALIX_EXPECTED_SHA:-}"

if [[ -z "$EXPECTED_SHA" ]]; then
  echo "HOLD: DEALIX_EXPECTED_SHA is required" >&2
  exit 64
fi
if [[ "$(git -C "$REPO" rev-parse HEAD)" != "$EXPECTED_SHA" ]]; then
  echo "HOLD: exact-head mismatch" >&2
  exit 65
fi

export DEALIX_GIT_SHA="$EXPECTED_SHA"
docker compose -f "$COMPOSE_FILE" --profile ingress-canary up -d ingress

api_body="$(curl -fsS -H 'Host: api.dealix.me' http://127.0.0.1:18081/version)"
web_body="$(curl -fsS -H 'Host: dealix.me' http://127.0.0.1:18081/healthz)"
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

if ss -ltn | grep -Eq '(^|[[:space:]])0\.0\.0\.0:18081([[:space:]]|$)'; then
  echo "FAIL: ingress canary exposed publicly" >&2
  exit 67
fi

echo "SELFHOST_INGRESS_CANARY=PASS"
echo "INGRESS=http://127.0.0.1:18081"
echo "PUBLIC_PORTS_80_443=NOT_OPENED_BY_THIS_RUNNER"
