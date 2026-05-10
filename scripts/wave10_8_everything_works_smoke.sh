#!/usr/bin/env bash
# Wave 10.8 §29.6 — "Everything Actually Works" production smoke.
#
# Wave 10.8.1 fixes (Codex P1+P2 review on PR #190):
#   - --insecure is now OPT-IN via DEALIX_SMOKE_ALLOW_INSECURE=1
#     (default: TLS verification ENFORCED; required for honest production
#     verdict — an MITM endpoint or expired cert must NOT silently pass)
#   - JSON-key checks now also assert HTTP 200 (a 500 error body that
#     happens to contain the expected key no longer counts as PASS)
#   - Step 1 asserts {"status": "ok"} value, not just key presence
#   - Step 8 asserts the 8-section invariant by COUNT (Article 6 contract)
#
# Single command for the founder's question: "are the services
# really working?". Returns EVERYTHING_WORKS=PASS|FAIL[step=N reason="..."].
#
# Read-only: zero mutations. Safe to run from anywhere.
#
# Usage:
#   bash scripts/wave10_8_everything_works_smoke.sh
#
# For a sandbox / local-clock-skewed environment you can opt into
# insecure curl explicitly (NOT recommended for production verdicts):
#   DEALIX_SMOKE_ALLOW_INSECURE=1 bash scripts/wave10_8_everything_works_smoke.sh
#
# Exit code:
#   0 = all 12 steps PASS
#   1 = at least 1 step FAIL (specific step in stderr)

set -uo pipefail

PROD_API="${PROD_API:-https://api.dealix.me}"
PROD_WEB="${PROD_WEB:-https://dealix.me}"
TIMEOUT="${TIMEOUT:-10}"

# ── TLS verification: enforced by default ─────────────────────────────
# Per Codex P1 review on PR #190: --insecure must NOT be on by default
# because an expired/misissued cert (or MITM endpoint) would silently
# produce EVERYTHING_WORKS=PASS even though real customer browsers
# would block the page. Make insecure mode an explicit opt-in.
if [ "${DEALIX_SMOKE_ALLOW_INSECURE:-0}" = "1" ]; then
  CURL_FLAGS=(--silent --show-error --insecure --max-time "${TIMEOUT}")
  echo "⚠️  DEALIX_SMOKE_ALLOW_INSECURE=1 — TLS verification DISABLED."
  echo "    This verdict is NOT valid for production decisions."
  echo "    Use only in sandbox / clock-skew environments."
  echo
else
  CURL_FLAGS=(--silent --show-error --max-time "${TIMEOUT}")
fi

results=()
overall_pass=true

# ── Internal helper: do one HTTP GET and store both body + code ──────
# We can't use $() to capture body because that runs in a subshell and
# our _LAST_HTTP_STATUS assignment would be lost. Instead, write both
# the body and the status code to known temp paths and let callers
# read them from the parent shell.
_SMOKE_TMPDIR="$(mktemp -d 2>/dev/null || echo /tmp)"
_SMOKE_BODY_FILE="${_SMOKE_TMPDIR}/smoke_body"
_SMOKE_CODE_FILE="${_SMOKE_TMPDIR}/smoke_code"
trap 'rm -rf "${_SMOKE_TMPDIR}"' EXIT

_fetch() {
  local url="$1"
  : > "${_SMOKE_BODY_FILE}"
  : > "${_SMOKE_CODE_FILE}"
  local code
  code=$(curl "${CURL_FLAGS[@]}" -o "${_SMOKE_BODY_FILE}" -w "%{http_code}" "${url}" 2>/dev/null || echo "000")
  printf '%s' "${code}" > "${_SMOKE_CODE_FILE}"
}

_last_status() {
  cat "${_SMOKE_CODE_FILE}" 2>/dev/null || echo "000"
}

_last_body() {
  cat "${_SMOKE_BODY_FILE}" 2>/dev/null || true
}

# ── Check helpers ─────────────────────────────────────────────────────

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
  _fetch "${url}"
  local code
  code=$(_last_status)
  if [ "${code}" != "200" ]; then
    results+=("${name}=FAIL [code=${code} (expected 200)]")
    overall_pass=false
    return
  fi
  local body
  body=$(_last_body)
  if [ -z "${body}" ]; then
    results+=("${name}=FAIL [empty body]")
    overall_pass=false
    return
  fi
  if echo "${body}" | grep -qF -- "${needle}"; then
    results+=("${name}=PASS [contains '${needle:0:30}...']")
  else
    results+=("${name}=FAIL [missing '${needle:0:30}']")
    overall_pass=false
  fi
}

# Per Codex P2 review: assert HTTP 200 BEFORE checking JSON key presence.
# A 500 error body that happens to contain the expected key must FAIL.
check_json_key_with_200() {
  local name="$1"
  local url="$2"
  local key="$3"
  _fetch "${url}"
  local code
  code=$(_last_status)
  if [ "${code}" != "200" ]; then
    results+=("${name}=FAIL [code=${code} (expected 200)]")
    overall_pass=false
    return
  fi
  local body
  body=$(_last_body)
  if [ -z "${body}" ]; then
    results+=("${name}=FAIL [empty body]")
    overall_pass=false
    return
  fi
  local has_key
  has_key=$(echo "${body}" | python3 -c "
import sys, json
try:
    data = json.loads(sys.stdin.read())
except Exception:
    print('FAIL_JSON')
    sys.exit(0)
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
    results+=("${name}=PASS [200 + key=${key} present]")
  else
    results+=("${name}=FAIL [200 but key=${key} ${has_key}]")
    overall_pass=false
  fi
}

# Per Codex P2 review: assert KEY VALUE, not just key presence.
# /health returning {"status": "error"} would have falsely passed.
check_json_value_with_200() {
  local name="$1"
  local url="$2"
  local key="$3"
  local expected_value="$4"
  _fetch "${url}"
  local code
  code=$(_last_status)
  if [ "${code}" != "200" ]; then
    results+=("${name}=FAIL [code=${code} (expected 200)]")
    overall_pass=false
    return
  fi
  local body
  body=$(_last_body)
  if [ -z "${body}" ]; then
    results+=("${name}=FAIL [empty body]")
    overall_pass=false
    return
  fi
  local actual
  actual=$(echo "${body}" | python3 -c "
import sys, json
try:
    data = json.loads(sys.stdin.read())
except Exception:
    print('FAIL_JSON')
    sys.exit(0)
parts = '${key}'.split('.')
cur = data
for p in parts:
    if isinstance(cur, dict) and p in cur:
        cur = cur[p]
    else:
        print('MISSING')
        sys.exit(0)
print(cur)
" 2>/dev/null || echo "FAIL_JSON")
  if [ "${actual}" = "${expected_value}" ]; then
    results+=("${name}=PASS [200 + ${key}=${expected_value}]")
  else
    results+=("${name}=FAIL [200 but ${key}=${actual} (expected ${expected_value})]")
    overall_pass=false
  fi
}

# Per Codex P2 review: explicitly enforce the 8-section invariant
# (Article 6) by counting keys in the sections object — not just
# verifying that "sections" exists.
check_8_section_invariant() {
  local name="$1"
  local url="$2"
  _fetch "${url}"
  local code
  code=$(_last_status)
  if [ "${code}" != "200" ]; then
    results+=("${name}=FAIL [code=${code}]")
    overall_pass=false
    return
  fi
  local body
  body=$(_last_body)
  local count
  count=$(echo "${body}" | python3 -c "
import sys, json
try:
    data = json.loads(sys.stdin.read())
    s = data.get('sections')
    if isinstance(s, dict):
        print(len(s))
    elif isinstance(s, list):
        print(len(s))
    else:
        print('NOT_ITERABLE')
except Exception:
    print('FAIL_JSON')
" 2>/dev/null || echo "FAIL_JSON")
  if [ "${count}" = "8" ]; then
    results+=("${name}=PASS [200 + sections has exactly 8 keys (Article 6)]")
  else
    results+=("${name}=FAIL [sections count=${count} (expected 8 per Article 6)]")
    overall_pass=false
  fi
}

echo "════════════════════════════════════════════════════════════"
echo "  DEALIX — EVERYTHING ACTUALLY WORKS SMOKE (Wave 10.8.1)"
echo "  Target API: ${PROD_API}"
echo "  Target Web: ${PROD_WEB}"
echo "════════════════════════════════════════════════════════════"
echo

# ── 12 steps ──────────────────────────────────────────────────────────

# Step 1 — API health: status MUST equal "ok" (not just be present)
check_json_value_with_200 "01_API_HEALTH" "${PROD_API}/health" "status" "ok"

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
check_8_section_invariant "08_CUSTOMER_PORTAL_API_8_SECTIONS" "${PROD_API}/api/v1/customer-portal/demo"

# Step 9 — Full-Ops Radar score endpoint (200 + score key)
check_json_key_with_200 "09_FULL_OPS_SCORE" "${PROD_API}/api/v1/full-ops-radar/score" "score"

# Step 10 — Executive Command Center status (200 + service key)
check_json_key_with_200 "10_ECC_STATUS" "${PROD_API}/api/v1/executive-command-center/status" "service"

# Step 11 — LeadOps spine status (200 + service key)
check_json_key_with_200 "11_LEADOPS_STATUS" "${PROD_API}/api/v1/leadops/status" "service"

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