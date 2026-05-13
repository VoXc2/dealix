#!/usr/bin/env bash
# Post-deploy smoke — exits 0 when every critical endpoint answers
# correctly; non-zero with a green/red dashboard otherwise.
#
# Usage:
#     bash scripts/ops/post_deploy_smoke.sh --base-url https://api.dealix.me
#     VERBOSE=1 bash scripts/ops/post_deploy_smoke.sh --base-url https://api.dealix.me
#
# What it checks:
#   1. /healthz             — lightweight health (always green when running).
#   2. /health/deep         — vendors block, configured count.
#   3. /api/v1/skills       — catalogue count == 12 (regression for d45d347).
#   4. /api/v1/skills/handlers
#   5. /api/v1/verticals    — 8 sectors registered.
#   6. /api/v1/marketing/brochure/real-estate.html
#   7. /api/v1/billing/health + /api/v1/billing/gcc/health
#   8. POST /api/v1/skills/sales_qualifier/run — end-to-end skill exec.
#   9. POST /api/v1/payment-ops/invoice-intent — landing checkout contract.
#  10. moyasar_live without DEALIX_MOYASAR_MODE=live MUST 403 (constitutional).

set -euo pipefail

BASE=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --base-url) BASE="$2"; shift 2 ;;
    -h|--help)
      sed -n '1,20p' "$0"
      exit 0
      ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done
[[ -z "$BASE" ]] && { echo "usage: $0 --base-url <https://api.host>"; exit 2; }
BASE="${BASE%/}"

GREEN="\033[32m✓\033[0m"
RED="\033[31m✗\033[0m"
fails=0

check() {
  local name="$1" cmd="$2"
  if out="$(eval "$cmd" 2>&1)"; then
    printf "%b %s\n" "$GREEN" "$name"
    [[ "${VERBOSE:-}" = "1" ]] && echo "    → $out"
  else
    printf "%b %s\n      %s\n" "$RED" "$name" "$out"
    fails=$((fails+1))
  fi
}

echo "── Smoking ${BASE} ──"

check "GET /healthz" \
  "curl -fsS '${BASE}/healthz' | grep -q '\"status\":\"ok\"'"

check "GET /health/deep (vendors block present)" \
  "curl -fsS '${BASE}/health/deep' | python3 -c 'import sys,json; d=json.load(sys.stdin); assert d.get(\"checks\",{}).get(\"vendors\"), \"no vendors block\"; print(len(d[\"checks\"][\"vendors\"]),\"vendors\")'"

check "GET /api/v1/skills (count=12)" \
  "curl -fsS '${BASE}/api/v1/skills' | python3 -c 'import sys,json; d=json.load(sys.stdin); assert d[\"count\"]==12, f\"got count={d[\\\"count\\\"]}\"'"

check "GET /api/v1/skills/handlers (12 registered)" \
  "curl -fsS '${BASE}/api/v1/skills/handlers' | python3 -c 'import sys,json; d=json.load(sys.stdin); assert len(d[\"handlers\"])==12, len(d[\"handlers\"])'"

check "GET /api/v1/verticals (8 sectors)" \
  "curl -fsS '${BASE}/api/v1/verticals' | python3 -c 'import sys,json; d=json.load(sys.stdin); assert d[\"count\"]==8'"

check "GET /api/v1/marketing/brochure/real-estate.html" \
  "curl -fsSI '${BASE}/api/v1/marketing/brochure/real-estate.html' | grep -qi 'content-type:.*html'"

check "GET /api/v1/billing/health" \
  "curl -fsS '${BASE}/api/v1/billing/health' >/dev/null"

check "GET /api/v1/billing/gcc/health (available array)" \
  "curl -fsS '${BASE}/api/v1/billing/gcc/health' | python3 -c 'import sys,json; d=json.load(sys.stdin); assert \"available\" in d'"

check "POST /api/v1/skills/sales_qualifier/run → score=1.0" \
  "curl -fsS -X POST '${BASE}/api/v1/skills/sales_qualifier/run' -H 'Content-Type: application/json' -d '{\"inputs\":{\"lead_snapshot\":{\"budget\":\"y\",\"authority\":\"y\",\"need\":\"y\",\"timeline\":\"y\"},\"compliance_signals\":{\"has_pdpl_consent\":true}}}' | python3 -c 'import sys,json; d=json.load(sys.stdin); assert d[\"result\"][\"score\"]==1.0, d[\"result\"][\"score\"]'"

check "POST /api/v1/payment-ops/invoice-intent → payment_id pay_*" \
  "curl -fsS -X POST '${BASE}/api/v1/payment-ops/invoice-intent' -H 'Content-Type: application/json' -d '{\"customer_handle\":\"smoke@dealix.sa\",\"amount_sar\":499,\"method\":\"moyasar_test\",\"service_session_id\":\"sprint_499\"}' | python3 -c 'import sys,json; d=json.load(sys.stdin); pid=d[\"payment\"][\"payment_id\"]; assert pid.startswith(\"pay_\"), pid'"

check "Constitution: moyasar_live without env → 403" \
  "curl -fsS -X POST '${BASE}/api/v1/payment-ops/invoice-intent' -H 'Content-Type: application/json' -d '{\"customer_handle\":\"smoke@dealix.sa\",\"amount_sar\":1,\"method\":\"moyasar_live\",\"service_session_id\":\"sprint_499\"}' -o /dev/null -w '%{http_code}' | grep -q 403"

echo
if [[ $fails -eq 0 ]]; then
  printf "%b  All smoke checks passed — you are live.\n" "$GREEN"
  exit 0
else
  printf "%b  %d check(s) failed — see lines above + docs/ops/troubleshooting.md.\n" "$RED" "$fails"
  exit 1
fi
