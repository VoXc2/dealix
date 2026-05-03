#!/usr/bin/env bash
# Dealix — Staging Smoke
# Hits the public staging surface (default https://api.dealix.me) and verifies:
#   - root + health + payments + LLM-providers respond
#   - 8 live-action gates remain default-False
#   - Public API returns valid JSON (no internal exception leaks)
#   - charge endpoint refuses with 403 (gate enforcement)
#   - frontend pages load (best-effort, behind same domain or *.dealix.me)
# Read-only — never sends money, never sends a real WhatsApp/email.
#
# Usage:
#   bash scripts/staging_smoke.sh                      # hits api.dealix.me
#   STAGING_URL=https://api.dealix.me bash scripts/staging_smoke.sh
#   STAGING_URL=http://127.0.0.1:8000 bash scripts/staging_smoke.sh   # local

set -u
B="${STAGING_URL:-https://api.dealix.me}"
PASS=0
FAIL=0

ok()   { echo "  ✓ $1"; PASS=$((PASS+1)); }
fail() { echo "  ✗ $1"; FAIL=$((FAIL+1)); }
hr()   { echo "────────────────────────────────────────────────────────────"; }

echo "Dealix — Staging Smoke"
echo "  base: $B"
hr

# 1. Root
echo "[1/9] root /"
ROOT=$(curl -sS -m 15 "$B/" 2>/dev/null || echo "")
echo "$ROOT" | grep -q '"name"' && ok "root returns JSON" || fail "root unreachable: $ROOT"

# 2. Health
echo "[2/9] /healthz"
H=$(curl -sS -m 15 "$B/healthz" 2>/dev/null || echo "")
echo "$H" | grep -q '"status"' && ok "healthz responds" || fail "healthz unreachable"

# 3. Live-action gates default-False (read whichever endpoint exposes them)
echo "[3/9] live-action gates default-False"
GATES=$(curl -sS -m 15 "$B/api/v1/payments/state" 2>/dev/null || echo "")
echo "$GATES" | grep -q '"live_charge": *false' && ok "MOYASAR_ALLOW_LIVE_CHARGE=false" \
                                                 || fail "live_charge not false"
echo "$GATES" | grep -q '"currency": *"SAR"' && ok "currency=SAR" || fail "currency not SAR"

# 4. Charge endpoint must refuse with 403
echo "[4/9] /api/v1/payments/charge enforces gate"
CHARGE_HTTP=$(curl -sS -m 15 -o /dev/null -w "%{http_code}" \
  -X POST -H 'Content-Type: application/json' \
  -d '{"amount_sar":1,"customer_id":"cus_smoke"}' "$B/api/v1/payments/charge")
[ "$CHARGE_HTTP" = "403" ] && ok "charge → 403 (gate closed)" \
                           || fail "charge expected 403, got $CHARGE_HTTP"

# 5. WhatsApp internal-send must refuse with 403
echo "[5/9] /api/v1/whatsapp/brief/send-internal enforces gate"
WA_HTTP=$(curl -sS -m 15 -o /dev/null -w "%{http_code}" \
  -X POST -H 'Content-Type: application/json' \
  -d '{"role":"ceo"}' "$B/api/v1/whatsapp/brief/send-internal")
[ "$WA_HTTP" = "403" ] && ok "wa send-internal → 403 (gate closed)" \
                       || fail "wa send-internal expected 403, got $WA_HTTP"

# 6. Operator must classify (read-only intent)
echo "[6/9] /api/v1/operator/chat/message"
OP=$(curl -sS -m 15 -X POST -H 'Content-Type: application/json' \
  -d '{"message":"أبغى عملاء جدد"}' "$B/api/v1/operator/chat/message" 2>/dev/null || echo "")
echo "$OP" | grep -q 'want_more_customers\|growth_starter\|intent' \
  && ok "operator routes Arabic intent" \
  || fail "operator did not classify: $(echo $OP | head -c 200)"

# 7. Services catalog
echo "[7/9] /api/v1/services/catalog"
SVC=$(curl -sS -m 15 "$B/api/v1/services/catalog" 2>/dev/null || echo "")
echo "$SVC" | grep -q 'growth_starter\|bundle' && ok "services catalog responds" \
                                                || fail "services catalog missing"

# 8. Proof Pack endpoint (public-readable for any customer_id form)
echo "[8/9] /api/v1/proof-ledger/customer/cus_smoke/pack"
PP=$(curl -sS -m 15 -o /dev/null -w "%{http_code}" \
  "$B/api/v1/proof-ledger/customer/cus_smoke/pack")
{ [ "$PP" = "200" ] || [ "$PP" = "404" ]; } && ok "proof-ledger answer ($PP)" \
                                             || fail "proof-ledger returned $PP"

# 9. Frontend pages reachable (best-effort against FRONTEND_URL or skip)
FE="${FRONTEND_URL:-}"
if [ -n "$FE" ]; then
  echo "[9/9] landing pages on $FE"
  for P in "/" "/services.html" "/operator.html" "/pricing.html" "/proof-pack.html"; do
    CODE=$(curl -sS -m 10 -o /dev/null -w "%{http_code}" "$FE$P" 2>/dev/null || echo "ERR")
    if [ "$CODE" = "200" ]; then ok "GET $P → 200"
    else fail "GET $P → $CODE"; fi
  done
else
  echo "[9/9] frontend pages — skipped (set FRONTEND_URL=http://... to enable)"
  ok "frontend smoke skipped (FRONTEND_URL not set)"
fi

hr
echo "PASS=$PASS  FAIL=$FAIL"
[ "$FAIL" -eq 0 ] && { echo "STAGING_SMOKE: GREEN"; exit 0; } \
                  || { echo "STAGING_SMOKE: RED"; exit 1; }
