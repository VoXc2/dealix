#!/usr/bin/env bash
# Dealix — Inbound flow verifier
#
# Submits a test demo-request against the public API and confirms:
#   1. /api/v1/public/demo-request returns 200 + ok=true + lead_id
#   2. /api/v1/founder/today shows the new lead in the inbound counter
#
# Read-only against prod EXCEPT for the test demo-request itself, which
# uses a clearly-namespaced demo email so the founder can identify and
# clean up if needed:  demo+test+<timestamp>@dealix-test.sa
#
# Never sends an external message. Never charges anything. Never enables
# any live gate. Used by docs/LAUNCH_CHECKLIST_GO_LIVE.md.

set -u
B="${BASE_URL:-${STAGING_URL:-https://api.dealix.me}}"
TS=$(date +%s)
TEST_EMAIL="demo+test+${TS}@dealix-test.sa"
TEST_COMPANY="DealixInboundVerify-${TS}"

ok()   { echo "  ✓ $1"; }
fail() { echo "  ✗ $1"; }
hr()   { echo "────────────────────────────────────────────────────────────"; }

echo "Dealix — Inbound Flow Verifier"
echo "  base:        $B"
echo "  test email:  $TEST_EMAIL"
echo "  test company: $TEST_COMPANY"
hr

# 1. Submit a test demo-request.
echo "[1/2] POST /api/v1/public/demo-request"
BODY=$(python -c "
import json, sys
print(json.dumps({
  'name': 'InboundVerify',
  'company': sys.argv[1],
  'email': sys.argv[2],
  'phone': '+966500000000',
  'sector': 'saas',
  'size': '11-50',
  'message': 'inbound verifier test (demo namespace)',
  'consent': True,
}, ensure_ascii=False))
" "$TEST_COMPANY" "$TEST_EMAIL")

RESP=$(curl -sS -m 15 -X POST "$B/api/v1/public/demo-request" \
  -H "Content-Type: application/json" \
  --data-binary "$BODY" 2>/dev/null || echo "")

OK=$(echo "$RESP" | python -c "import json,sys; d=json.loads(sys.stdin.read() or '{}'); print('1' if d.get('ok') is True else '0')" 2>/dev/null || echo "0")
LEAD_ID=$(echo "$RESP" | python -c "import json,sys; d=json.loads(sys.stdin.read() or '{}'); print(d.get('lead_id') or '')" 2>/dev/null || echo "")

if [ "$OK" = "1" ]; then
  ok "demo-request returned ok=true"
else
  fail "demo-request did NOT return ok=true (response: $(echo "$RESP" | head -c 200))"
  hr
  echo "INBOUND_FLOW: RED"
  exit 1
fi

if [ -n "$LEAD_ID" ]; then
  ok "lead_id surfaced in response: $LEAD_ID"
else
  fail "lead_id missing from response — DB write skipped or endpoint not yet deployed"
  echo "  (continuing — the founder/today aggregator may still pick it up)"
fi
hr

# 2. Poll /api/v1/founder/today for up to 30s for the new lead to appear.
echo "[2/2] GET /api/v1/founder/today (polling for inbound counter)"
deadline=$((SECONDS + 30))
seen=0
while [ "$SECONDS" -lt "$deadline" ]; do
  TODAY=$(curl -sS -m 15 "$B/api/v1/founder/today" 2>/dev/null || echo "{}")
  COUNT=$(echo "$TODAY" | python -c "
import json, sys
try:
    d = json.loads(sys.stdin.read() or '{}')
    print(d.get('inbound_demo_requests', {}).get('count', 0))
except Exception:
    print(0)
" 2>/dev/null || echo "0")
  MATCH=$(echo "$TODAY" | python -c "
import json, sys
try:
    d = json.loads(sys.stdin.read() or '{}')
    recent = d.get('inbound_demo_requests', {}).get('recent', [])
    target = sys.argv[1]
    print('1' if any((r.get('company') or '') == target for r in recent) else '0')
except Exception:
    print(0)
" "$TEST_COMPANY" 2>/dev/null || echo "0")
  if [ "$MATCH" = "1" ]; then
    ok "test company appears in /founder/today inbound list (count=$COUNT)"
    seen=1
    break
  fi
  sleep 3
done

if [ "$seen" != "1" ]; then
  fail "test company NOT seen in /founder/today within 30s"
  echo "  Possible causes:"
  echo "    - /api/v1/founder/today is not yet deployed with the new"
  echo "      inbound_demo_requests block (Railway redeploy needed)"
  echo "    - DB write failed silently (check api logs)"
  hr
  echo "INBOUND_FLOW: RED"
  exit 1
fi

hr
echo "INBOUND_FLOW: GREEN"
echo "  test lead: $TEST_EMAIL ($LEAD_ID)"
echo "  Founder will see it in /founder/today; safe to delete from DB if desired."
exit 0
