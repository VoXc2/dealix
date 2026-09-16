#!/usr/bin/env bash
# Wave 10.5 §26.4 Phase G — Production smoke (read-only).
#
# Standalone read-only smoke probe against api.dealix.me + dealix.me.
# Invoked either directly or by dealix_master_full_execution_verify.sh
# when RUN_PROD_SMOKE=1 is set.
#
# Saudi-Arabic note:
#   فحص حي على الإنتاج، قراءة فقط — لا يكتب أي شيء، لا يلمس بيانات.
#
# Usage:
#   bash scripts/production_smoke.sh
#   BASE_URL=https://staging.api.dealix.me SITE_URL=https://staging.dealix.me \
#     bash scripts/production_smoke.sh
#
# Exit codes:
#   0 = all probes PASS
#   1 = at least one probe FAIL
set -uo pipefail

BASE="${BASE_URL:-https://api.dealix.me}"
SITE="${SITE_URL:-https://dealix.me}"

echo "── Production smoke ───────────────────────────────────"
echo "  api: $BASE"
echo "  site: $SITE"

results=()
ok=true

probe() {
  local name="$1"; local url="$2"; local match="$3"
  local out
  out=$(curl -sSk --max-time 10 "$url" 2>&1 || echo "")
  if echo "$out" | grep -q "$match"; then
    results+=("$name=PASS")
  else
    results+=("$name=FAIL ($url)")
    ok=false
  fi
}

probe_status() {
  local name="$1"; local url="$2"; local expected_code="$3"
  local code
  code=$(curl -sSk -o /dev/null -w "%{http_code}" --max-time 10 "$url" 2>&1 || echo "000")
  if [ "$code" = "$expected_code" ]; then
    results+=("$name=PASS ($code)")
  else
    results+=("$name=FAIL ($code, expected $expected_code) ($url)")
    ok=false
  fi
}

# API trust layer — must serve expected payloads
probe "API_HEALTHZ" "$BASE/healthz" '"status":"ok"'
probe "API_HEALTH" "$BASE/health" '"status":"ok"'
probe "API_VERSION" "$BASE/version" '"git_sha"'
probe "API_META" "$BASE/api/v1/meta" '"surfaces"'

# Canonical public frontend routes (aligned with gtm_public_surfaces.yaml + sitemap.ts)
# These are the authoritative public routes that prospects and partners land on.
declare -A PUBLIC_ROUTES=(
  ["INDEX"]="/"
  ["EN_HOME"]="/en"
  ["COMPANY"]="/company"
  ["SERVICES"]="/services"
  ["SECTORS"]="/sectors"
  ["PRODUCTS"]="/products"
  ["DEALIX_OS"]="/dealix-os"
  ["BOOK"]="/book"
  ["SAUDI_RADAR"]="/saudi-opportunity-radar"
  ["SAFETY"]="/safety"
  ["CASES"]="/cases"
  ["PRICING"]="/pricing"
  ["CLIENT_PORTAL_DEMO"]="/client-portal/demo"
)

for name in "${!PUBLIC_ROUTES[@]}"; do
  path="${PUBLIC_ROUTES[$name]}"
  url="$SITE$path"
  probe_status "LANDING_${name}" "$url" "200"
done

# Internal/admin routes must 404 (fail-closed) in production
# Sample check — not exhaustive; full guard is in middleware.ts
declare -A INTERNAL_ROUTES=(
  ["FOUNDER"]="/ops/founder"
  ["WAR_ROOM"]="/ops/war-room"
  ["CRM"]="/crm"
  ["DASHBOARD"]="/dashboard"
)

for name in "${!INTERNAL_ROUTES[@]}"; do
  path="${INTERNAL_ROUTES[$name]}"
  url="$SITE$path"
  probe_status "INTERNAL_${name}_404" "$url" "404"
done

# Retired compatibility route must redirect to the canonical public surface.
pipeline_code=$(curl -sSk -o /dev/null -w "%{http_code}" --max-time 10 "$SITE/pipeline")
pipeline_location=$(curl -sSkI --max-time 10 "$SITE/pipeline" | tr -d "\r" | awk 'tolower($1)=="location:" {print $2; exit}')
if [ "$pipeline_code" = "308" ] && [ "$pipeline_location" = "/dealix-os" ]; then
  results+=("COMPAT_PIPELINE_REDIRECT=PASS (308 -> /dealix-os)")
else
  results+=("COMPAT_PIPELINE_REDIRECT=FAIL ($pipeline_code -> ${pipeline_location:-missing})")
  ok=false
fi

# Production API documentation is intentionally fail-closed.
probe_status "API_DOCS_404" "$BASE/docs" "404"
probe_status "API_OPENAPI_404" "$BASE/openapi.json" "404"

echo
for r in "${results[@]}"; do printf "  %s\n" "$r"; done
echo
if $ok; then
  echo "PRODUCTION_SMOKE=PASS"
  exit 0
else
  echo "PRODUCTION_SMOKE=FAIL"
  exit 1
fi
