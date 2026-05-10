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

# API health (must serve {"status":"ok"})
probe "API_HEALTH" "$BASE/health" '"status":"ok"'

# Landing pages — every public route the founder shares with prospects
for path in "" "launchpad.html" "customer-portal.html" \
            "executive-command-center.html" "diagnostic-real-estate.html" \
            "start.html" "proof.html"; do
  url="$SITE/$path"
  code=$(curl -sSk -o /dev/null -w "%{http_code}" --max-time 10 "$url")
  label="${path:-INDEX}"
  # Normalize label (strip .html, uppercase)
  label="$(echo "$label" | sed 's/\.html$//' | tr '[:lower:]' '[:upper:]' | tr '-' '_')"
  if [ "$code" = "200" ]; then
    results+=("LANDING_${label}=PASS")
  else
    results+=("LANDING_${label}=FAIL ($code)")
    ok=false
  fi
done

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
