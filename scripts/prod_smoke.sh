#!/usr/bin/env bash
#
# Dealix production smoke — verifies the 14J commercial wiring lands on a
# real Railway deploy. Usage:
#
#   bash scripts/prod_smoke.sh https://your-railway-url
#
# Exits 0 if every check passes, non-zero with a summary if anything fails.
# Reads optional ADMIN_KEY env var for admin-gated endpoints.
#
# Honors the 11 non-negotiables: never sends to external addresses,
# never POSTs cold outreach, never tries to charge a real card. The
# `demo-request` POST uses a synthetic 'founder+smoke@…' address so the
# transactional confirmation email is auditable.
set -u

BASE="${1:-http://localhost:8000}"
ADMIN="${ADMIN_KEY:-}"
FAIL=0
PASS=0
TOTAL=0

color_ok() { printf "\033[32m%s\033[0m" "$1"; }
color_fail() { printf "\033[31m%s\033[0m" "$1"; }
color_dim() { printf "\033[2m%s\033[0m" "$1"; }

check() {
    local name="$1"
    local url="$2"
    local expect="${3:-200}"
    local extra="${4:-}"
    TOTAL=$((TOTAL + 1))
    local code
    code=$(curl -s -o /tmp/dealix_smoke_body -w '%{http_code}' $extra "$url" || echo 000)
    if [[ "$code" == "$expect" ]]; then
        echo "$(color_ok '✓') $name $(color_dim "($code)")"
        PASS=$((PASS + 1))
    else
        echo "$(color_fail '✗') $name $(color_dim "expected $expect got $code") — $url"
        head -c 200 /tmp/dealix_smoke_body 2>/dev/null && echo
        FAIL=$((FAIL + 1))
    fi
}

echo "━━ Dealix production smoke — $BASE ━━"
echo

# 1. Healthcheck (Railway requires this)
check "healthz"                  "$BASE/healthz"
check "root /"                   "$BASE/"

# 2. Commercial map (Wave 14J)
check "commercial-map JSON"      "$BASE/api/v1/commercial-map"
check "commercial-map markdown"  "$BASE/api/v1/commercial-map/markdown"

# 3. Wave 14C sprint orchestrator
check "sprint sample"            "$BASE/api/v1/sprint/sample"

# 4. Wave 14D.3 sector intel sample
check "sector intel sample"      "$BASE/api/v1/sector-intel/sample/b2b_services"

# 5. Wave 14B trust pack
check "trust pack JSON"          "$BASE/api/v1/value/trust-pack/smoke-handle"
check "trust pack markdown"      "$BASE/api/v1/value/trust-pack/smoke-handle/markdown"

# 6. Wave 14C audit chain
check "audit chain markdown"     "$BASE/api/v1/audit/smoke-handle/markdown"
check "evidence control graph"   "$BASE/api/v1/audit/smoke-handle/control-graph"

# 7. Wave 14B sales qualification
check "qualification (good)"     "$BASE/api/v1/service-setup/qualify" 200 \
    "-X POST -H Content-Type:application/json -d {\"pain_clear\":true,\"owner_present\":true,\"data_available\":true,\"accepts_governance\":true,\"has_budget\":true}"

check "qualification (reject)"   "$BASE/api/v1/service-setup/qualify" 200 \
    "-X POST -H Content-Type:application/json -d {\"pain_clear\":true,\"owner_present\":true,\"data_available\":true,\"accepts_governance\":true,\"has_budget\":true,\"wants_safe_methods\":true,\"proof_path_visible\":true,\"retainer_path_visible\":true,\"raw_request_text\":\"we want cold WhatsApp automation\"}"

# 8. Wave 14B proposal endpoint
check "proposal render"          "$BASE/api/v1/service-setup/proposal/smoke" 200 \
    "-X POST -H Content-Type:application/json -d {\"customer_name\":\"Smoke\",\"customer_handle\":\"smoke\",\"sector\":\"b2b_services\",\"city\":\"Riyadh\",\"engagement_id\":\"eng_smoke\",\"price_sar\":499}"

# 9. Wave 14B data_os CSV preview
check "data-os preview"          "$BASE/api/v1/data-os/import-preview" 200 \
    "-X POST -H Content-Type:application/json -d {\"customer_handle\":\"smoke\",\"raw_csv\":\"company_name,sector,city\\nشركة,b2b_services,Riyadh\\n\"}"

# 10. Wave 14A friction log + value
check "friction-log emit"        "$BASE/api/v1/friction-log/event" 200 \
    "-X POST -H Content-Type:application/json -d {\"customer_id\":\"smoke\",\"kind\":\"approval_delay\",\"severity\":\"low\"}"
check "friction-log aggregate"   "$BASE/api/v1/friction-log/smoke"

check "value monthly markdown"   "$BASE/api/v1/value/smoke/report/monthly/markdown"

# 11. Wave 14A customer workspace
check "customer workspace"       "$BASE/api/v1/customer-portal/smoke/workspace"
check "adoption score"           "$BASE/api/v1/customer-success/smoke/adoption-score"

# 12. Wave 14D.2 case-safe export
check "case-safe summary"        "$BASE/api/v1/proof-to-market/case-safe/eng_smoke?customer_id=smoke&sector=b2b_services"

# 13. Demo-request lead capture + transactional email (REAL email send if Gmail configured)
check "demo-request"             "$BASE/api/v1/public/demo-request" 200 \
    "-X POST -H Content-Type:application/json -d {\"name\":\"Smoke\",\"company\":\"Dealix Internal\",\"email\":\"founder+smoke@dealix.sa\",\"phone\":\"+966500000000\",\"sector\":\"b2b_services\",\"consent\":true}"

# 14. Wave 14F agent OS (admin-gated; only runs if ADMIN_KEY set)
if [[ -n "$ADMIN" ]]; then
    check "agents list"          "$BASE/api/v1/agents" 200 "-H X-Admin-API-Key:$ADMIN"
    check "founder dashboard"    "$BASE/api/v1/founder/dashboard" 200 "-H X-Admin-API-Key:$ADMIN"
else
    echo "$(color_dim '·') agents/founder-dashboard skipped (ADMIN_KEY unset)"
fi

echo
echo "━━ summary ━━"
echo "passed: $PASS / $TOTAL"
echo "failed: $FAIL"
echo

# Last verification: governance_decision envelope present on the
# commercial-map response.
if curl -s "$BASE/api/v1/commercial-map" | grep -q '"governance_decision"'; then
    echo "$(color_ok '✓') commercial-map carries governance_decision envelope"
    PASS=$((PASS + 1))
else
    echo "$(color_fail '✗') commercial-map missing governance_decision"
    FAIL=$((FAIL + 1))
fi

if [[ $FAIL -gt 0 ]]; then
    echo
    echo "$(color_fail 'FAIL') — $FAIL check(s) failed. Inspect Railway logs."
    exit 1
fi

echo
echo "$(color_ok 'PASS') — every commercial endpoint reachable on $BASE"
echo
echo "Next steps:"
echo "  1. Verify the founder inbox received the diagnostic_intake_confirmation."
echo "  2. Open $BASE/diagnostic.html in a browser and submit a real intake."
echo "  3. Open $BASE/sprint-sample.html to view the synthetic Proof Pack."
echo "  4. Review docs/RAILWAY_DEPLOY_CHECKLIST.md for the deploy SOP."
echo "  5. Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة."
