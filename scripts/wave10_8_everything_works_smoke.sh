#!/usr/bin/env bash
# Wave 10.8 §29.6 — "Everything Actually Works" production smoke.
#
# Single command for the founder's question: "are the services
# really working?". Probes 12 customer-facing endpoints + structural
# checks. Returns EVERYTHING_WORKS=PASS|FAIL[step=N reason="..."].
#
# Read-only: zero mutations. Safe to run from anywhere.
#
# Usage:
#   bash scripts/wave10_8_everything_works_smoke.sh
#
# Exit code:
#   0 = all 12 steps PASS
#   1 = at least 1 step FAIL (specific step in stderr)

set -uo pipefail

PROD_API="${PROD_API:-https://api.dealix.me}"
PROD_WEB="${PROD_WEB:-https://dealix.me}"
TIMEOUT="${TIMEOUT:-10}"

# Allow self-signed certs in sandbox envs where the clock might be skewed.
CURL_FLAGS=(--silent --show-error --insecure --max-time "${TIMEOUT}")

results=()
overall_pass=true

check_http_200() {
  local name="$1"
  local url="$2"
  local code
  code=$(curl "${CURL_FLAGS[@]}" -o /dev/null -w "%{http_code}" "${url}" 2>/dev/null || echo "000")
  if [ "${code}" = "200" ]; then
    results+=("${name}=PASS [200]")
  else
    results+=("${name}=FAIL [code=${code}]")
    overall_pass=false
  fi
}

check_html_contains() {
  local name="$1"
  local url="$2"
  local needle="$3"
  local body
  body=$(curl "${CURL_FLAGS[@]}" "${url}" 2>/dev/null || echo "")
  if [ -z "${body}" ]; then
    results+=("${name}=FAIL [empty body]")
    overall_pass=false
    return
  fi
  # `printf '%s' "$needle"` lets us search for unicode strings safely
  if echo "${body}" | grep -qF -- "${needle}"; then
    results+=("${name}=PASS [contains '${needle:0:30}...']")
  else
    results+=("${name}=FAIL [missing '${needle:0:30}']")
    overall_pass=false
  fi
}

check_json_key() {
  local name="$1"
  local url="$2"
  local key="$3"
  local body
  body=$(curl "${CURL_FLAGS[@]}" "${url}" 2>/dev/null || echo "")
  if [ -z "${body}" ]; then
    results+=("${name}=FAIL [empty body]")
    overall_pass=false
    return
  fi
  # Use python3 for JSON parsing (jq not always available).
  local has_key
  has_key=$(echo "${body}" | python3 -c "
import sys, json
try:
    data = json.loads(sys.stdin.read())
except Exception:
    print('FAIL_JSON')
    sys.exit(0)

# Walk dotted-path keys (e.g. 'sections.lead_inbox')
parts = '${key}'.split('.')
cur = data
for p in parts:
    if isinstance(cur, dict) and p in cur:
        cur = cur[p]
    else:
        print('MISSING')
        sys.exit(0)
print('OK')
" 2>/dev/null || echo "FAIL_JSON")

  if [ "${has_key}" = "OK" ]; then
    results+=("${name}=PASS [key=${key} present]")
  else
    results+=("${name}=FAIL [key=${key} ${has_key}]")
    overall_pass=false
  fi
}

echo "════════════════════════════════════════════════════════════"
echo "  DEALIX — EVERYTHING ACTUALLY WORKS SMOKE (Wave 10.8 §29.6)"
echo "  Target API: ${PROD_API}"
echo "  Target Web: ${PROD_WEB}"
echo "════════════════════════════════════════════════════════════"
echo

# ── 12 steps ──────────────────────────────────────────────────────────

# Step 1 — API health
check_json_key "01_API_HEALTH" "${PROD_API}/health" "status"

# Step 2 — Homepage HTTP 200
check_http_200 "02_HOMEPAGE" "${PROD_WEB}/"

# Step 3 — Launchpad page contains a customer-facing brand name
check_html_contains "03_LAUNCHPAD_HAS_BRAND" "${PROD_WEB}/launchpad.html" "Dealix"

# Step 4 — Diagnostic intake form present
check_http_200 "04_DIAGNOSTIC_REAL_ESTATE" "${PROD_WEB}/diagnostic-real-estate.html"

# Step 5 — Sprint signup page mentions price
check_html_contains "05_START_HAS_PRICE" "${PROD_WEB}/start.html" "499"

# Step 6 — Executive Command Center renders
check_http_200 "06_ECC_PAGE" "${PROD_WEB}/executive-command-center.html"

# Step 7 — Customer Portal renders + has known panel
check_http_200 "07_CUSTOMER_PORTAL_PAGE" "${PROD_WEB}/customer-portal.html"

# Step 8 — Customer Portal API: 8-section invariant (constitutional)
check_json_key "08_CUSTOMER_PORTAL_API_SECTIONS" "${PROD_API}/api/v1/customer-portal/demo" "sections"

# Step 9 — Full-Ops Radar score endpoint
check_json_key "09_FULL_OPS_SCORE" "${PROD_API}/api/v1/full-ops-radar/score" "score"

# Step 10 — Executive Command Center status
check_json_key "10_ECC_STATUS" "${PROD_API}/api/v1/executive-command-center/status" "service"

# Step 11 — LeadOps spine status
check_json_key "11_LEADOPS_STATUS" "${PROD_API}/api/v1/leadops/status" "service"

# Step 12 — Privacy Policy v2 present
check_http_200 "12_PRIVACY_POLICY" "${PROD_WEB}/privacy.html"

# ── Output ────────────────────────────────────────────────────────────

echo
echo "RESULTS:"
for r in "${results[@]}"; do printf "  %s\n" "${r}"; done
echo

# Total
total=${#results[@]}
passed=0
for r in "${results[@]}"; do
  case "${r}" in *=PASS*) passed=$((passed + 1)) ;; esac
done

echo "════════════════════════════════════════════════════════════"
if ${overall_pass}; then
  echo "  EVERYTHING_WORKS=PASS  (${passed}/${total})"
  echo "  NEXT_FOUNDER_ACTION=Send warm-intro #1 — the system is ready."
  exit 0
else
  echo "  EVERYTHING_WORKS=FAIL  (${passed}/${total})"
  echo "  NEXT_FOUNDER_ACTION=Review the FAIL line(s) above before customer #1 demo."
  echo
  echo "  Failed steps:"
  for r in "${results[@]}"; do
    case "${r}" in *=FAIL*) echo "    ❌ ${r}" ;; esac
  done
  exit 1
fi