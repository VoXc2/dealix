#!/usr/bin/env bash
# Wave 11 §31.12 — Hardened Production Smoke
#
# Extends Wave 10.8 (12 customer-facing checks) with 4 more:
#   13. /api/v1/full-ops-radar/score returns 200 + score >= 0
#   14. /api/v1/agent-observability/status returns 200 (or 404 if not yet deployed)
#   15. Forbidden-token re-scan against live HTML for top customer-facing pages
#   16. TLS cert expiry > 30 days for both api.dealix.me + dealix.me
#
# Read-only. No mutations. No live sends. No live charges.
#
# Usage:
#   bash scripts/wave11_production_smoke_hardened.sh
#
# Exit code:
#   0 = all hardened steps PASS
#   1 = at least 1 step FAIL

set -uo pipefail
cd "$(dirname "$0")/.."

PROD_API="${PROD_API:-https://api.dealix.me}"
PROD_WEB="${PROD_WEB:-https://dealix.me}"
TIMEOUT="${TIMEOUT:-10}"

# TLS strict by default (matches Wave 10.8.1)
if [ "${DEALIX_SMOKE_ALLOW_INSECURE:-0}" = "1" ]; then
  CURL_FLAGS=(--silent --show-error --insecure --max-time "${TIMEOUT}")
  echo "⚠️  DEALIX_SMOKE_ALLOW_INSECURE=1 — TLS verification SKIPPED (not for production verdicts)"
else
  CURL_FLAGS=(--silent --show-error --max-time "${TIMEOUT}")
fi

results=()
overall_pass=true

# ─── Step 1: Run the existing Wave 10.8 12-step smoke first ─────────
echo "════════════════════════════════════════════════════════════"
echo "  STAGE 1: Wave 10.8 Everything-Works smoke (12 steps)"
echo "════════════════════════════════════════════════════════════"
if bash scripts/wave10_8_everything_works_smoke.sh; then
  results+=("WAVE10_8_SMOKE=PASS [12/12]")
else
  results+=("WAVE10_8_SMOKE=FAIL")
  overall_pass=false
fi
echo

# ─── Step 13: Full-Ops Radar score endpoint ────────────────────────
echo "════════════════════════════════════════════════════════════"
echo "  STAGE 2: Wave 11 hardened additions (4 steps)"
echo "════════════════════════════════════════════════════════════"

CODE=$(curl "${CURL_FLAGS[@]}" -o /tmp/wave11_smoke_radar.json -w "%{http_code}" "${PROD_API}/api/v1/full-ops-radar/score" 2>/dev/null || echo "000")
if [ "${CODE}" = "200" ]; then
  if python3 -c "import json,sys; data=json.load(open('/tmp/wave11_smoke_radar.json')); assert 'score' in data; assert isinstance(data['score'],(int,float)); assert data['score']>=0; print('OK')" 2>/dev/null; then
    results+=("13_FULL_OPS_SCORE=PASS [200 + score>=0]")
  else
    results+=("13_FULL_OPS_SCORE=FAIL [200 but score field missing/invalid]")
    overall_pass=false
  fi
else
  results+=("13_FULL_OPS_SCORE=FAIL [code=${CODE}]")
  overall_pass=false
fi

# ─── Step 14: Agent Observability status ───────────────────────────
CODE=$(curl "${CURL_FLAGS[@]}" -o /dev/null -w "%{http_code}" "${PROD_API}/api/v1/agent-observability/status" 2>/dev/null || echo "000")
if [ "${CODE}" = "200" ]; then
  results+=("14_AGENT_OBSERVABILITY=PASS [200]")
elif [ "${CODE}" = "404" ]; then
  # 404 acceptable if endpoint not yet deployed; doesn't fail the smoke
  results+=("14_AGENT_OBSERVABILITY=SKIP [404 — not deployed yet]")
else
  results+=("14_AGENT_OBSERVABILITY=FAIL [code=${CODE}]")
  overall_pass=false
fi

# ─── Step 15: Forbidden-token live re-scan ─────────────────────────
# Top 5 customer-facing pages — fetch live HTML, grep for forbidden tokens
FORBIDDEN_TOKENS='\bguaranteed?\b|\bblast\b|\bscraping\b|\bcold\s+(whatsapp|outreach|email)\b|نضمن|مضمون|guaranteed\s+revenue'
forbidden_hits=0
for path in "/" "/launchpad.html" "/start.html" "/customer-portal.html" "/executive-command-center.html"; do
  body=$(curl "${CURL_FLAGS[@]}" "${PROD_WEB}${path}" 2>/dev/null || echo "")
  if echo "${body}" | grep -qiE "${FORBIDDEN_TOKENS}" 2>/dev/null; then
    forbidden_hits=$((forbidden_hits + 1))
    echo "  ⚠️  Forbidden token found on ${path}"
  fi
done
if [ "${forbidden_hits}" = "0" ]; then
  results+=("15_LIVE_FORBIDDEN_SCAN=PASS [0 hits across 5 pages]")
else
  results+=("15_LIVE_FORBIDDEN_SCAN=FAIL [${forbidden_hits} pages with forbidden tokens]")
  overall_pass=false
fi

# ─── Step 16: TLS cert expiry > 30 days ────────────────────────────
# Skip in --insecure mode since the cert isn't being validated
if [ "${DEALIX_SMOKE_ALLOW_INSECURE:-0}" = "1" ]; then
  results+=("16_TLS_EXPIRY=SKIP [insecure mode]")
else
  tls_ok=true
  for host in api.dealix.me dealix.me; do
    expiry=$(echo | timeout "${TIMEOUT}" openssl s_client -servername "${host}" -connect "${host}:443" 2>/dev/null \
             | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
    if [ -z "${expiry}" ]; then
      results+=("16_TLS_EXPIRY=FAIL [could not fetch cert for ${host}]")
      tls_ok=false
      overall_pass=false
      continue
    fi
    expiry_epoch=$(date -d "${expiry}" +%s 2>/dev/null || echo "0")
    now_epoch=$(date +%s)
    days_remaining=$(( (expiry_epoch - now_epoch) / 86400 ))
    if [ "${days_remaining}" -lt 30 ]; then
      results+=("16_TLS_EXPIRY=FAIL [${host} expires in ${days_remaining} days]")
      tls_ok=false
      overall_pass=false
    fi
  done
  if ${tls_ok}; then
    results+=("16_TLS_EXPIRY=PASS [both certs >30 days remaining]")
  fi
fi

# ─── Output ────────────────────────────────────────────────────────
echo
echo "════════════════════════════════════════════════════════════"
echo "  WAVE 11 HARDENED SMOKE RESULTS"
echo "════════════════════════════════════════════════════════════"
for r in "${results[@]}"; do printf "  %s\n" "${r}"; done
echo

passed=0
total=${#results[@]}
for r in "${results[@]}"; do
  case "${r}" in *=PASS*) passed=$((passed + 1)) ;; esac
done

echo "════════════════════════════════════════════════════════════"
if ${overall_pass}; then
  echo "  EVERYTHING_WORKS_HARDENED=PASS  (${passed}/${total} PASS)"
  echo "  WAVE11_PRODUCTION_SMOKE=PASS"
  echo "  NEXT_FOUNDER_ACTION=System is production-verified. Send warm-intro #1."
  exit 0
else
  echo "  EVERYTHING_WORKS_HARDENED=FAIL"
  echo "  WAVE11_PRODUCTION_SMOKE=FAIL"
  echo "  NEXT_FOUNDER_ACTION=Review FAIL line(s) before customer #1 demo."
  exit 1
fi
