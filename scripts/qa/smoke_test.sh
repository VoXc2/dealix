#!/usr/bin/env bash
# Dealix — minimal smoke test
# Tests core backend endpoints + local AI health. Safe: read-only, no secrets in code.
#
# Usage:
#   BASE_URL=http://localhost:8000 bash scripts/qa/smoke_test.sh
#   BASE_URL=https://api.dealix.example bash scripts/qa/smoke_test.sh
#
# Exit 0 when all required checks pass, 1 otherwise.
# Local AI checks are soft-fail: they log but do not flip the exit code unless
# LOCAL_AI_REQUIRED=1 is set.

set -u
set -o pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"
LOCAL_AI_REQUIRED="${LOCAL_AI_REQUIRED:-0}"
TIMEOUT="${TIMEOUT:-10}"

PASS=0
FAIL=0
SOFT=0

c_green=$'\033[0;32m'
c_red=$'\033[0;31m'
c_yellow=$'\033[0;33m'
c_dim=$'\033[2m'
c_off=$'\033[0m'

log()   { printf '%s\n' "$*"; }
okay()  { PASS=$((PASS + 1)); printf '%sPASS%s  %s\n' "$c_green" "$c_off" "$1"; }
fail()  { FAIL=$((FAIL + 1)); printf '%sFAIL%s  %s %s(%s)%s\n' "$c_red" "$c_off" "$1" "$c_dim" "${2:-}" "$c_off"; }
soft()  { SOFT=$((SOFT + 1)); printf '%sSKIP%s  %s %s(%s)%s\n' "$c_yellow" "$c_off" "$1" "$c_dim" "${2:-}" "$c_off"; }

http_code() {
  local code
  code="$(curl -s -o /dev/null -w '%{http_code}' --max-time "$TIMEOUT" "$1" 2>/dev/null)"
  # On connection failure curl prints "000" and exits non-zero. Normalise either way.
  if [[ -z "$code" || "$code" == "000" ]]; then
    echo "000"
  else
    echo "$code"
  fi
}

http_body() {
  curl -s --max-time "$TIMEOUT" "$1" 2>/dev/null || true
}

http_post_code() {
  curl -s -o /dev/null -w '%{http_code}' --max-time "$TIMEOUT" \
    -X POST -H 'Content-Type: application/json' \
    -d "${2:-{}}" "$1" 2>/dev/null || echo "000"
}

check_required_http() {
  local name="$1" url="$2" expect="${3:-200}"
  local code
  code="$(http_code "$url")"
  if [[ "$code" == "$expect" ]]; then
    okay "$name"
  else
    fail "$name" "got $code, expected $expect — $url"
  fi
}

check_any_2xx() {
  local name="$1" url="$2"
  local code
  code="$(http_code "$url")"
  if [[ "$code" =~ ^2 ]]; then
    okay "$name"
  else
    fail "$name" "got $code — $url"
  fi
}

check_soft_http() {
  local name="$1" url="$2" expect="${3:-200}"
  local code
  code="$(http_code "$url")"
  if [[ "$code" == "$expect" ]]; then
    okay "$name"
  elif [[ "$LOCAL_AI_REQUIRED" == "1" ]]; then
    fail "$name" "got $code, expected $expect — $url"
  else
    soft "$name" "got $code — $url (not required)"
  fi
}

cat <<EOF
Dealix smoke test
  base url : $BASE_URL
  timeout  : ${TIMEOUT}s
  local-ai : $([ "$LOCAL_AI_REQUIRED" = "1" ] && echo required || echo optional)

EOF

if ! command -v curl >/dev/null 2>&1; then
  printf '%scurl is required%s\n' "$c_red" "$c_off" >&2
  exit 2
fi

# ── Core health ────────────────────────────────────────────────────
log "-- core health --"
check_required_http "GET /api/v1/health"        "$BASE_URL/api/v1/health"
check_any_2xx       "GET /api/v1/health/db"     "$BASE_URL/api/v1/health/db"
check_any_2xx       "GET /api/v1/health/redis"  "$BASE_URL/api/v1/health/redis"

# ── OpenAPI / docs ─────────────────────────────────────────────────
log
log "-- api surface --"
check_required_http "GET /openapi.json" "$BASE_URL/openapi.json"
check_required_http "GET /docs"         "$BASE_URL/docs"

# ── Public / unauth endpoints that should *reject* cleanly ─────────
log
log "-- auth surface (expect 401/422, not 500) --"
code_leads=$(http_code "$BASE_URL/api/v1/leads/")
if [[ "$code_leads" == "401" || "$code_leads" == "403" || "$code_leads" == "422" ]]; then
  okay "GET /api/v1/leads/ rejects unauth with $code_leads"
else
  fail "GET /api/v1/leads/ unauth handling" "got $code_leads"
fi

code_dash=$(http_code "$BASE_URL/api/v1/dashboard/")
if [[ "$code_dash" =~ ^(401|403|404|422)$ ]]; then
  okay "GET /api/v1/dashboard/ rejects unauth with $code_dash"
else
  fail "GET /api/v1/dashboard/ unauth handling" "got $code_dash"
fi

# ── Local AI layer (PR #16) ────────────────────────────────────────
log
log "-- local ai (Ollama) --"
check_soft_http "GET /api/v1/local-ai/status"   "$BASE_URL/api/v1/local-ai/status"
check_soft_http "GET /api/v1/local-ai/catalog"  "$BASE_URL/api/v1/local-ai/catalog"
check_soft_http "GET /api/v1/local-ai/tasks"    "$BASE_URL/api/v1/local-ai/tasks"

# Inspect status body when reachable.
status_body="$(http_body "$BASE_URL/api/v1/local-ai/status")"
if [[ -n "$status_body" ]]; then
  if echo "$status_body" | grep -q '"enabled"'; then
    if echo "$status_body" | grep -q '"enabled":[[:space:]]*true'; then
      okay "local-ai enabled=true in status"
    else
      soft "local-ai enabled=false" "set LOCAL_LLM_ENABLED=1 to activate"
    fi
  fi
  if echo "$status_body" | grep -q '"daemon_up":[[:space:]]*true'; then
    okay "local-ai daemon reachable"
  else
    soft "local-ai daemon reachable" "Ollama not responding"
  fi
fi

# ── Governance surfaces referenced in AGENTS.md ────────────────────
log
log "-- governance surfaces (expect reachable; auth may be required) --"
for path in \
  /api/v1/executive-room/snapshot \
  /api/v1/contradictions/ \
  /api/v1/evidence-packs/ \
  /api/v1/approval-center/ \
  /api/v1/connectors/governance \
  /api/v1/model-routing/dashboard \
  /api/v1/compliance/matrix/ \
  /api/v1/forecast-control/unified
do
  code="$(http_code "$BASE_URL$path")"
  if [[ "$code" =~ ^(200|401|403)$ ]]; then
    okay "GET $path reachable ($code)"
  else
    fail "GET $path" "got $code"
  fi
done

# ── Summary ────────────────────────────────────────────────────────
log
printf 'summary: %s%d passed%s, %s%d failed%s, %s%d skipped%s\n' \
  "$c_green" "$PASS" "$c_off" \
  "$c_red"   "$FAIL" "$c_off" \
  "$c_yellow" "$SOFT" "$c_off"

if [[ "$FAIL" -gt 0 ]]; then
  exit 1
fi
exit 0
