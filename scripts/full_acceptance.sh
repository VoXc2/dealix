#!/usr/bin/env bash
# full_acceptance.sh — single-command, end-to-end acceptance test of Dealix.
#
# Boots the API on a free port (with SQLite for self-containment), runs every
# acceptance check from docs/ACCEPTANCE_REPORT_2026-05-03.md, and exits 0 only
# if all 4 gates (Frontend, Backend, Safety, Business) pass.
#
# Usage:
#   bash scripts/full_acceptance.sh                    # local SQLite + ports 8770/8771
#   BASE_URL=https://api.dealix.me bash scripts/full_acceptance.sh   # against prod
#
# Exit codes:
#   0  ALL 4 GATES PASS
#   1  At least one gate failed (output shows which)
#
set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

# Colors
G=$'\033[32m'; R=$'\033[31m'; Y=$'\033[33m'; C=$'\033[36m'; B=$'\033[1m'; N=$'\033[0m'

# Counters
PASS=0
FAIL=0
FAILS=()

ok()   { printf "  ${G}✓${N} %s\n" "$1"; PASS=$((PASS+1)); }
fail() { printf "  ${R}✗${N} %s\n" "$1"; FAIL=$((FAIL+1)); FAILS+=("$1"); }
hdr()  { printf "\n${C}════ %s ════${N}\n" "$1"; }

# ── Boot (or use external URL) ────────────────────────────────────
PORT=${PORT:-8770}
FRONT_PORT=${FRONT_PORT:-8771}
BASE_URL=${BASE_URL:-"http://127.0.0.1:$PORT"}
FRONT_URL=${FRONT_URL:-"http://127.0.0.1:$FRONT_PORT"}
SPAWN_API=true
SPAWN_FRONT=true

if [[ "$BASE_URL" != http://127.0.0.1:* ]]; then
  SPAWN_API=false
  echo "${B}Using external BASE_URL=$BASE_URL${N}"
fi
if [[ "$FRONT_URL" != http://127.0.0.1:* ]]; then
  SPAWN_FRONT=false
fi

cleanup() {
  if [[ "$SPAWN_API" == true ]]; then
    [[ -n "${API_PID:-}" ]] && kill "$API_PID" 2>/dev/null || true
  fi
  if [[ "$SPAWN_FRONT" == true ]]; then
    [[ -n "${FRONT_PID:-}" ]] && kill "$FRONT_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

if [[ "$SPAWN_API" == true ]]; then
  echo "${B}Booting API on $BASE_URL …${N}"
  rm -f /tmp/dealix_acceptance.db
  APP_ENV=test APP_SECRET_KEY=test \
    ANTHROPIC_API_KEY=x DEEPSEEK_API_KEY=x GROQ_API_KEY=x GLM_API_KEY=x GOOGLE_API_KEY=x \
    DATABASE_URL="sqlite+aiosqlite:////tmp/dealix_acceptance.db" \
    WHATSAPP_ALLOW_LIVE_SEND=false WHATSAPP_ALLOW_INTERNAL_SEND=false \
    WHATSAPP_ALLOW_CUSTOMER_SEND=false CALLS_ALLOW_LIVE_DIAL=false \
    GMAIL_ALLOW_LIVE_SEND=false MOYASAR_ALLOW_LIVE_CHARGE=false \
    uvicorn api.main:app --host 127.0.0.1 --port "$PORT" --log-level error \
    > /tmp/dealix_acceptance_api.log 2>&1 &
  API_PID=$!
  for _ in $(seq 1 30); do
    sleep 1
    curl -sf --max-time 1 "$BASE_URL/healthz" > /dev/null && break
  done
fi

if [[ "$SPAWN_FRONT" == true ]]; then
  cd "$REPO/landing"
  python -m http.server "$FRONT_PORT" --bind 127.0.0.1 > /dev/null 2>&1 &
  FRONT_PID=$!
  cd "$REPO"
  sleep 1
fi

# ── 1. Backend Gate ───────────────────────────────────────────────
hdr "1. BACKEND GATE — 16 endpoints must return 200"
BACKEND_PATHS=(
  "/healthz"
  "/api/v1/services/catalog"
  "/api/v1/role-briefs/daily?role=sales_manager"
  "/api/v1/role-briefs/daily?role=growth_manager"
  "/api/v1/role-briefs/daily?role=ceo"
  "/api/v1/whatsapp/brief?role=sales_manager"
  "/api/v1/whatsapp/brief?role=growth_manager"
  "/api/v1/sales-os/pipeline-snapshot"
  "/api/v1/growth-os/daily-plan"
  "/api/v1/revops/funnel"
  "/api/v1/customer-success/health"
  "/api/v1/compliance/blocked-actions"
  "/api/v1/prospects/standup"
  "/api/v1/payments/state"
  "/api/v1/meetings/brief?role=meeting_intelligence"
  "/api/v1/proof-ledger/units"
)
for path in "${BACKEND_PATHS[@]}"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL$path")
  if [[ "$code" == "200" ]]; then
    ok "[$code] $path"
  else
    fail "[$code] $path"
  fi
done

# ── 2. Frontend Gate ──────────────────────────────────────────────
if [[ "$SPAWN_FRONT" == true ]]; then
  hdr "2. FRONTEND GATE — 17 pages must return 200"
  FRONT_PAGES=(
    "/index.html" "/services.html" "/command-center.html" "/operator.html"
    "/proof-pack.html" "/pricing.html" "/trust-center.html" "/support.html"
    "/onboarding.html"
    "/role/ceo.html" "/role/sales.html" "/role/growth.html" "/role/revops.html"
    "/role/cs.html" "/role/finance.html" "/role/compliance.html" "/role/partner.html"
  )
  for page in "${FRONT_PAGES[@]}"; do
    code=$(curl -s -o /dev/null -w "%{http_code}" "$FRONT_URL$page")
    if [[ "$code" == "200" ]]; then
      ok "[$code] $page"
    else
      fail "[$code] $page"
    fi
  done
else
  hdr "2. FRONTEND GATE — skipped (FRONT_URL is external)"
fi

# ── 3. Safety Gate ────────────────────────────────────────────────
hdr "3. SAFETY GATE — gates + 403s + audit"

GATES_JSON=$(curl -s "$BASE_URL/api/v1/founder/today")
GATE_FALSE_COUNT=$(echo "$GATES_JSON" | python -c "
import sys, json
try:
    d = json.load(sys.stdin)
    g = (d.get('policy') or {}).get('live_action_gates') or {}
    print(sum(1 for v in g.values() if not v))
except Exception: print(0)
")
[[ "$GATE_FALSE_COUNT" == "8" ]] && ok "8/8 live-action gates FALSE" || fail "Only $GATE_FALSE_COUNT/8 gates FALSE"

c=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/api/v1/whatsapp/brief/send-internal" \
       -H 'Content-Type: application/json' -d '{"role":"ceo"}')
[[ "$c" == "403" ]] && ok "WhatsApp internal-send returns 403" || fail "WhatsApp internal-send returned $c (expect 403)"

c=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/api/v1/payments/charge" \
       -H 'Content-Type: application/json' -d '{}')
[[ "$c" == "403" ]] && ok "Live charge returns 403" || fail "Live charge returned $c (expect 403)"

c=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/api/v1/calls/dial-live" \
       -H 'Content-Type: application/json' -d '{}')
[[ "$c" == "403" ]] && ok "Live call dial returns 403" || fail "Live call dial returned $c (expect 403)"

c=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/api/v1/payments/charge" \
       -H 'Content-Type: application/json' -H 'X-Dealix-Role: sales_manager' -d '{}')
[[ "$c" == "403" ]] && ok "Role guard blocks sales_manager from /payments/charge" || fail "Role guard returned $c (expect 403)"

# Operator bot blocks unsafe ask
RESP=$(curl -s -X POST "$BASE_URL/api/v1/operator/chat/message" \
       -H 'Content-Type: application/json' -d '{"text":"أبغى أرسل واتساب لأرقام مشتراة"}')
BLOCKED=$(echo "$RESP" | python -c "import sys,json; print(json.load(sys.stdin).get('blocked', False))")
[[ "$BLOCKED" == "True" ]] && ok "Operator bot blocks 'send WhatsApp to purchased numbers'" \
                           || fail "Operator bot did NOT block unsafe ask (blocked=$BLOCKED)"

# Forbidden claims audit
if APP_ENV=test ANTHROPIC_API_KEY=x APP_SECRET_KEY=test python scripts/forbidden_claims_audit.py > /tmp/dealix_fc.log 2>&1; then
  ok "forbidden_claims_audit: $(tail -3 /tmp/dealix_fc.log | head -1 | tr -s ' ')"
else
  fail "forbidden_claims_audit failed (see /tmp/dealix_fc.log)"
fi

# ── 4. Business Gate (E2E) ────────────────────────────────────────
hdr "4. BUSINESS GATE — E2E flow Lead → Pilot → Proof Pack"

# Run the 8-step flow
P=$(curl -s -X POST "$BASE_URL/api/v1/prospects" -H 'Content-Type: application/json' \
    -d '{"name":"acceptance test","company":"Acme","relationship_type":"warm_1st_degree","expected_value_sar":499}')
PID=$(echo "$P" | python -c "import sys,json; print(json.load(sys.stdin).get('id',''))")
[[ -n "$PID" ]] && ok "[1/8] prospect created: $PID" || { fail "[1/8] create prospect failed"; PID=""; }

if [[ -n "$PID" ]]; then
  for stage in messaged replied meeting pilot; do
    A=$(curl -s -X POST "$BASE_URL/api/v1/prospects/$PID/advance" \
        -H 'Content-Type: application/json' -d "{\"target_status\":\"$stage\"}")
    TO=$(echo "$A" | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('to',''))")
    [[ "$TO" == "$stage" ]] && ok "advance → $stage  (RWU: $(echo "$A" | python -c 'import sys,json;print(json.load(sys.stdin).get("rwu_emitted",""))'))" \
                            || fail "advance → $stage failed (got $TO)"
  done

  INV=$(curl -s -X POST "$BASE_URL/api/v1/payments/invoice" -H 'Content-Type: application/json' \
        -d "{\"amount_sar\":499,\"customer_id\":\"$PID\"}")
  INVID=$(echo "$INV" | python -c "import sys,json; print(json.load(sys.stdin).get('invoice_id',''))")
  [[ -n "$INVID" ]] && ok "[6/8] invoice 499 SAR created: $INVID" || fail "invoice creation failed"

  if [[ -n "$INVID" ]]; then
    CF=$(curl -s -X POST "$BASE_URL/api/v1/payments/confirm" -H 'Content-Type: application/json' \
         -d "{\"invoice_id\":\"$INVID\"}")
    STATUS=$(echo "$CF" | python -c "import sys,json; print(json.load(sys.stdin).get('status',''))")
    [[ "$STATUS" == "paid" ]] && ok "[7/8] payment confirmed (paid)" || fail "payment confirm failed (status=$STATUS)"
  fi

  CW=$(curl -s -X POST "$BASE_URL/api/v1/prospects/$PID/advance" \
       -H 'Content-Type: application/json' -d '{"target_status":"closed_won"}')
  CW_TO=$(echo "$CW" | python -c "import sys,json; print(json.load(sys.stdin).get('to',''))")
  [[ "$CW_TO" == "closed_won" ]] && ok "[8/8] advance → closed_won (RWU: meeting_closed)" || fail "closed_won failed"

  # Proof Pack HTML must render
  PACK_HTML=$(curl -s "$BASE_URL/api/v1/proof-ledger/customer/$PID/pack.html")
  PACK_SIZE=$(echo -n "$PACK_HTML" | wc -c)
  if [[ "$PACK_SIZE" -gt 1000 ]]; then
    ok "Proof Pack HTML rendered: $PACK_SIZE bytes"
  else
    fail "Proof Pack HTML too small: $PACK_SIZE bytes"
  fi
fi

# ── Summary ───────────────────────────────────────────────────────
hdr "RESULT"
TOTAL=$((PASS + FAIL))
printf "  ${B}%d/%d checks passed${N}\n" "$PASS" "$TOTAL"

if [[ "$FAIL" -eq 0 ]]; then
  printf "\n  ${G}${B}✅ ALL 4 GATES PASS — system is launch-ready.${N}\n\n"
  exit 0
else
  printf "\n  ${R}${B}✗ ${FAIL} check(s) failed:${N}\n"
  for f in "${FAILS[@]}"; do printf "    - %s\n" "$f"; done
  printf "\n"
  exit 1
fi
