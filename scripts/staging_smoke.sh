#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# Dealix staging / production smoke
# Usage:
#   BASE_URL=https://api.dealix.me bash scripts/staging_smoke.sh
# Default BASE_URL = https://api.dealix.me
# ═══════════════════════════════════════════════════════════════

set -u
BASE="${BASE_URL:-https://api.dealix.me}"
PASS=0
FAIL=0
FAILED_PATHS=()

probe() {
  local name="$1"; local path="$2"; local expected="${3:-200}"
  local code
  code=$(curl -s -o /dev/null --max-time 12 -w "%{http_code}" "$BASE$path")
  if [ "$code" = "$expected" ]; then
    echo "  OK  $code $path  ($name)"
    PASS=$((PASS+1))
  else
    echo "  FAIL $code (expected $expected) $path  ($name)"
    FAIL=$((FAIL+1)); FAILED_PATHS+=("$path:$code")
  fi
}

probe_post() {
  local name="$1"; local path="$2"; local body="$3"; local expected="${4:-200}"
  local code
  code=$(curl -s -o /dev/null --max-time 12 -w "%{http_code}" -X POST "$BASE$path" \
        -H "Content-Type: application/json" -d "$body")
  if [ "$code" = "$expected" ]; then
    echo "  OK  $code $path  ($name)"
    PASS=$((PASS+1))
  else
    echo "  FAIL $code (expected $expected) $path  ($name)"
    FAIL=$((FAIL+1)); FAILED_PATHS+=("$path:$code")
  fi
}

echo "════ Dealix smoke against $BASE ════"
echo "[1] Public surface"
probe "root JSON"             "/"                                          200
probe "/health"               "/health"                                    200
probe "/docs"                 "/docs"                                      200
probe "/openapi.json"         "/openapi.json"                              200

echo "[2] Pricing & business"
probe "business pricing"      "/api/v1/business/pricing"                   200
probe "pricing plans"         "/api/v1/pricing/plans"                      200
probe "verticals"             "/api/v1/business/verticals"                 200
probe "gtm first 10"          "/api/v1/business/gtm/first-10"              200
probe "sales script"          "/api/v1/business/sales-script"              200

echo "[3] Operator / Command Center / Briefs"
probe "personal-operator daily-brief"   "/api/v1/personal-operator/daily-brief"     200
probe "personal-operator launch-report" "/api/v1/personal-operator/launch-report"   200
probe "v3 command-center snapshot"      "/api/v1/v3/command-center/snapshot"        200
probe "v3 stack"                        "/api/v1/v3/stack"                          200
probe "v3 agents list"                  "/api/v1/v3/agents"                         200
probe "v3 market radar"                 "/api/v1/v3/market-radar"                   200
probe "v3 revenue-science demo"         "/api/v1/v3/revenue-science/demo"           200

echo "[4] Proof / catalog"
probe "proof-pack demo"       "/api/v1/business/proof-pack/demo"           200
probe "data sources catalog"  "/api/v1/data/sources/catalog"               200
probe "objections bank"       "/api/v1/objections/bank"                    200

echo "[5] Safety: live actions are blocked / signed"
# WhatsApp test-send should be blocked by policy gate (returns 200 with body status=blocked)
probe "whatsapp inbound verify (no token)" "/api/v1/webhooks/whatsapp"     422
# Moyasar webhook unsigned must be rejected (401 = bad_signature) — gate enforced
probe_post "moyasar webhook unsigned" "/api/v1/webhooks/moyasar" '{"type":"payment_paid"}' 401

# WhatsApp send gated check (read body)
echo -n "  WA test-send body: "
curl -s --max-time 12 -X POST "$BASE/api/v1/os/test-send?phone=%2B966500000000&body=hi" | head -c 200
echo ""

echo "[6] Compliance gate (campaign risk — no DB needed)"
probe_post "campaign-risk safe" "/api/v1/revenue-os/compliance/campaign-risk" \
  '{"channel":"whatsapp","audience":"cold_purchased","consent":false,"region":"sa"}' 200

echo ""
echo "════ result ════"
echo "  PASS=$PASS  FAIL=$FAIL"
if [ "$FAIL" -gt 0 ]; then
  printf '  failed: %s\n' "${FAILED_PATHS[@]}"
  exit 1
fi
exit 0
