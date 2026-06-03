#!/usr/bin/env bash
# Dealix — post-redeploy verification.
#
# Run after merging claude/service-activation-console-IA2JK and the
# Railway redeploy completes. Hits every endpoint the branch added,
# asserts the safety perimeter is intact, and prints a one-line
# verdict block at the end.
#
# Usage:
#   bash scripts/post_redeploy_verify.sh
#   BASE_URL=https://api.dealix.me LANDING_URL=https://dealix.me bash scripts/post_redeploy_verify.sh
#
# Exit codes:
#   0  all green
#   1  any required check failed
#   2  bash/curl missing

set -uo pipefail

BASE_URL="${BASE_URL:-https://api.dealix.me}"
LANDING_URL="${LANDING_URL:-https://dealix.me}"

if ! command -v curl >/dev/null 2>&1; then
  echo "FAIL: curl not installed" >&2
  exit 2
fi
if ! command -v python3 >/dev/null 2>&1 && ! command -v python >/dev/null 2>&1; then
  echo "FAIL: python3 not installed" >&2
  exit 2
fi
PY="$(command -v python3 || command -v python)"

PASS=0
FAIL=0
WARN=0

# --------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------
say() { printf '%s\n' "$*"; }
ok()   { say "  ✅ $*"; PASS=$((PASS+1)); }
bad()  { say "  ❌ $*"; FAIL=$((FAIL+1)); }
warn() { say "  ⚠️  $*"; WARN=$((WARN+1)); }

curl_status() {
  curl -fsS -o /dev/null -w '%{http_code}' --max-time 8 "$1" 2>/dev/null
}
curl_body() {
  curl -fsS --max-time 8 "$1" 2>/dev/null
}

json_get() {
  # json_get '<dotted.path>' '<json>'
  printf '%s' "$2" | "$PY" -c "
import json, sys
d = json.loads(sys.stdin.read() or 'null')
keys = '''$1'''.split('.')
try:
    for k in keys:
        d = d[k]
    print(d)
except Exception:
    print('')
"
}

# --------------------------------------------------------------------
say "════════ 1. Liveness + git_sha ════════"
HEALTH="$(curl_body "$BASE_URL/health")"
if [ -z "$HEALTH" ]; then
  bad "GET $BASE_URL/health → no response"
else
  STATUS="$(json_get status "$HEALTH")"
  GIT_SHA="$(json_get git_sha "$HEALTH")"
  PROVIDERS="$(json_get providers "$HEALTH")"
  if [ "$STATUS" = "ok" ]; then ok "/health status=ok"; else bad "/health status=$STATUS"; fi
  case "$GIT_SHA" in
    ""|unknown|None)
      warn "/health git_sha=$GIT_SHA (Railway should expose RAILWAY_GIT_COMMIT_SHA — set it if missing)";;
    *)
      ok "/health git_sha=$GIT_SHA";;
  esac
  ok "/health providers=$PROVIDERS"
fi

# --------------------------------------------------------------------
say
say "════════ 2. Self-Growth read-only endpoints ════════"
for path in \
  "/api/v1/self-growth/status" \
  "/api/v1/self-growth/service-activation" \
  "/api/v1/self-growth/seo/audit" \
  "/api/v1/self-growth/seo/audit/summary" \
  "/api/v1/self-growth/tooling" \
  "/api/v1/self-growth/service-activation-candidates" \
  "/api/v1/self-growth/service-activation/lead_intake_whatsapp"
do
  CODE="$(curl_status "$BASE_URL$path")"
  if [ "$CODE" = "200" ]; then ok "$path → 200"; else bad "$path → $CODE"; fi
done

# --------------------------------------------------------------------
say
say "════════ 3. Service Activation Matrix counts ════════"
MATRIX="$(curl_body "$BASE_URL/api/v1/self-growth/service-activation")"
if [ -n "$MATRIX" ]; then
  TOTAL="$(json_get counts.total "$MATRIX")"
  LIVE="$(json_get counts.live "$MATRIX")"
  PILOT="$(json_get counts.pilot "$MATRIX")"
  PARTIAL="$(json_get counts.partial "$MATRIX")"
  TARGET="$(json_get counts.target "$MATRIX")"
  BLOCKED="$(json_get counts.blocked "$MATRIX")"
  EXPECTED="total=32 live=0 pilot=1 partial=7 target=24 blocked=0"
  ACTUAL="total=$TOTAL live=$LIVE pilot=$PILOT partial=$PARTIAL target=$TARGET blocked=$BLOCKED"
  if [ "$ACTUAL" = "$EXPECTED" ]; then
    ok "counts match expected: $EXPECTED"
  else
    bad "counts drift — expected $EXPECTED, got $ACTUAL"
  fi
else
  bad "matrix payload empty"
fi

# --------------------------------------------------------------------
say
say "════════ 4. Safety guardrails (publishing/check) ════════"
RESP="$(curl -fsS --max-time 8 -X POST "$BASE_URL/api/v1/self-growth/publishing/check" \
  -H 'Content-Type: application/json' \
  -d '{"text":"We guarantee revenue","language":"en"}' 2>/dev/null)"
DECISION="$(json_get decision "$RESP")"
if [ "$DECISION" = "blocked" ]; then
  ok "publishing/check blocks 'We guarantee revenue' → blocked"
else
  bad "publishing/check did NOT block 'We guarantee revenue' (decision=$DECISION)"
fi

# Arabic clean text should pass through
RESP2="$(curl -fsS --max-time 8 -X POST "$BASE_URL/api/v1/self-growth/publishing/check" \
  -H 'Content-Type: application/json' \
  -d '{"text":"صفحة هبوط آمنة جاهزة للمراجعة","language":"ar"}' 2>/dev/null)"
DECISION2="$(json_get decision "$RESP2")"
if [ "$DECISION2" = "allowed_draft" ]; then
  ok "publishing/check allows clean Arabic draft → allowed_draft"
else
  bad "publishing/check did NOT allow clean Arabic draft (decision=$DECISION2)"
fi

# --------------------------------------------------------------------
say
say "════════ 5. Static landing site ════════"
STATUS_HTML="$(curl_body "$LANDING_URL/status.html")"
if [ -z "$STATUS_HTML" ]; then
  bad "GET $LANDING_URL/status.html → no response"
else
  if printf '%s' "$STATUS_HTML" | grep -q 'services-mount'; then
    ok "/status.html mounts the new console (services-mount present)"
  else
    bad "/status.html is OLD version (no services-mount)"
  fi
  if printf '%s' "$STATUS_HTML" | grep -q 'service-console.js'; then
    ok "/status.html loads service-console.js"
  else
    bad "/status.html does NOT load service-console.js"
  fi
fi

JSON_CODE="$(curl_status "$LANDING_URL/assets/data/service-readiness.json")"
if [ "$JSON_CODE" = "200" ]; then
  ok "/assets/data/service-readiness.json → 200"
else
  bad "/assets/data/service-readiness.json → $JSON_CODE"
fi

# --------------------------------------------------------------------
say
say "════════ 6. Guardrails introspection ════════"
GUARDRAILS="$(curl_body "$BASE_URL/api/v1/self-growth/status")"
NO_LIVE_SEND="$(json_get guardrails.no_live_send "$GUARDRAILS")"
NO_SCRAPING="$(json_get guardrails.no_scraping "$GUARDRAILS")"
NO_COLD="$(json_get guardrails.no_cold_outreach "$GUARDRAILS")"
APPROVAL="$(json_get guardrails.approval_required_for_external_actions "$GUARDRAILS")"
[ "$NO_LIVE_SEND" = "True" ] && ok "no_live_send=True" || bad "no_live_send=$NO_LIVE_SEND"
[ "$NO_SCRAPING" = "True" ] && ok "no_scraping=True" || bad "no_scraping=$NO_SCRAPING"
[ "$NO_COLD" = "True" ] && ok "no_cold_outreach=True" || bad "no_cold_outreach=$NO_COLD"
[ "$APPROVAL" = "True" ] && ok "approval_required_for_external_actions=True" || bad "approval_required_for_external_actions=$APPROVAL"

# --------------------------------------------------------------------
say
say "════════ Verdict ════════"
say "PASS=$PASS  FAIL=$FAIL  WARN=$WARN"
if [ "$FAIL" -eq 0 ]; then
  say
  say "DEALIX_POST_REDEPLOY_VERDICT=green"
  exit 0
fi
say
say "DEALIX_POST_REDEPLOY_VERDICT=red ($FAIL failed checks)"
exit 1
