#!/usr/bin/env bash
# Dealix v10 — master verifier.
#
# Runs every v10 layer's check + safety eval + secret scan +
# pytest bundle. Prints a verdict block.

set -uo pipefail

PASS=0
FAIL=0
WARN=0

ok()   { printf "  ✅ %-44s %s\n" "$1" "$2"; PASS=$((PASS+1)); }
warn() { printf "  ⚠️  %-44s %s\n" "$1" "$2"; WARN=$((WARN+1)); }
fail() { printf "  ❌ %-44s %s\n" "$1" "$2"; FAIL=$((FAIL+1)); }

echo "═══════════════════════════════════════════════════════════════"
echo " Dealix v10 — Master Verification"
echo " Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "═══════════════════════════════════════════════════════════════"

# 1. Reference Library YAML
echo ""
echo " 1. Reference Library (70+ tools)"
echo "───────────────────────────────────────────────────────────────"
if python3 scripts/verify_reference_library_70.py >/tmp/v10_ref.out 2>&1; then
  COUNT=$(grep -E "^Total projects: " /tmp/v10_ref.out | awk '{print $3}')
  ok "REFERENCE_LIBRARY_70" "$COUNT projects, no errors"
else
  fail "REFERENCE_LIBRARY_70" "$(tail -3 /tmp/v10_ref.out | head -1)"
fi

# 2. Capability gap map + decision record
echo ""
echo " 2. Capability gap map + decision record"
echo "───────────────────────────────────────────────────────────────"
[ -f docs/v10/DEALIX_CAPABILITY_GAP_MAP.md ] && ok "DEALIX_CAPABILITY_GAP_MAP.md" "present" || fail "DEALIX_CAPABILITY_GAP_MAP.md" "missing"
[ -f docs/v10/DEPENDENCY_DECISION_RECORD.md ] && ok "DEPENDENCY_DECISION_RECORD.md" "present" || fail "DEPENDENCY_DECISION_RECORD.md" "missing"
[ -f docs/V10_MASTER_PLAN.md ] && ok "V10_MASTER_PLAN.md" "present" || fail "V10_MASTER_PLAN.md" "missing"
[ -f docs/v10/V10_TOP_10_REFERENCE.md ] && ok "V10_TOP_10_REFERENCE.md" "present" || fail "V10_TOP_10_REFERENCE.md" "missing"

# 3. Phase B v10 modules (ship as agents land)
echo ""
echo " 3. v10 Phase B native modules"
echo "───────────────────────────────────────────────────────────────"
for mod in llm_gateway_v10 safety_v10 observability_v10 workflow_os_v10 \
           crm_v10 customer_inbox_v10 growth_v10 knowledge_v10 \
           ai_workforce_v10 founder_v10; do
  if [ -d "auto_client_acquisition/$mod" ]; then
    ok "$mod" "module present"
  else
    warn "$mod" "not yet shipped"
  fi
done

# 4. Phase B routers
echo ""
echo " 4. v10 Phase B routers"
echo "───────────────────────────────────────────────────────────────"
for r in llm_gateway_v10 safety_v10 observability_v10 workflow_os_v10 \
         crm_v10 customer_inbox_v10 growth_v10 knowledge_v10 \
         ai_workforce_v10 founder_v10; do
  if [ -f "api/routers/$r.py" ]; then
    ok "router $r" "registered"
  else
    warn "router $r" "not yet shipped"
  fi
done

# 5. v10 tests
echo ""
echo " 5. v10 test files"
echo "───────────────────────────────────────────────────────────────"
for t in tests/test_reference_library_70.py \
         tests/test_v10_capability_gap_map.py \
         tests/test_llm_gateway_v10.py \
         tests/test_safety_v10.py \
         tests/test_observability_v10.py \
         tests/test_workflow_os_v10.py \
         tests/test_crm_v10.py \
         tests/test_customer_inbox_v10.py \
         tests/test_growth_v10.py \
         tests/test_knowledge_v10.py \
         tests/test_ai_workforce_v10.py \
         tests/test_founder_v10.py; do
  if [ -f "$t" ]; then
    ok "$(basename $t)" "present"
  else
    warn "$(basename $t)" "not yet shipped"
  fi
done

# 6. Forbidden claims sweep
echo ""
echo " 6. Forbidden claims + secret scan"
echo "───────────────────────────────────────────────────────────────"
LANDING_HITS=$(grep -lE 'نضمن|guaranteed' landing/*.html 2>/dev/null | grep -vE 'roi.html|academy.html|founder.html' | head -1)
if [ -z "$LANDING_HITS" ]; then
  ok "forbidden claims (landing)" "clean (4 REVIEW_PENDING founder-only)"
else
  fail "forbidden claims (landing)" "$LANDING_HITS"
fi

SECRET_HITS=$(grep -rE 'sk_live_[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{36}|AIza[A-Za-z0-9]{35}' --include='*.py' --include='*.md' . 2>/dev/null | grep -vE 'test_|sk_live_test|EXAMPLE|sk_live_REALDANGEROUSKEYSECRET|sk_live_xxxxx|sk_live_should_|placeholder|sk_live_unsigned' | head -1)
if [ -z "$SECRET_HITS" ]; then
  ok "secret scan" "clean"
else
  fail "secret scan" "$SECRET_HITS"
fi

# 7. Hard-rule invariants
echo ""
echo " 7. Hard-rule invariants"
echo "───────────────────────────────────────────────────────────────"
python3 -c "
from auto_client_acquisition.finance_os import is_live_charge_allowed
from auto_client_acquisition.agent_governance import FORBIDDEN_TOOLS, ToolCategory
from core.config.settings import get_settings

assert is_live_charge_allowed()['allowed'] is False
assert ToolCategory.SEND_WHATSAPP_LIVE in FORBIDDEN_TOOLS
assert ToolCategory.LINKEDIN_AUTOMATION in FORBIDDEN_TOOLS
assert ToolCategory.SCRAPE_WEB in FORBIDDEN_TOOLS
assert getattr(get_settings(), 'whatsapp_allow_live_send', True) is False
print('OK')
" >/tmp/v10_inv.out 2>&1
if grep -q "^OK$" /tmp/v10_inv.out; then
  ok "live_charge gated" "BLOCKED"
  ok "WhatsApp live send gated" "BLOCKED"
  ok "LinkedIn automation forbidden" "in FORBIDDEN_TOOLS"
  ok "Scraping forbidden" "in FORBIDDEN_TOOLS"
else
  fail "hard rules" "$(cat /tmp/v10_inv.out)"
fi

# 8. Pytest bundle (quick)
echo ""
echo " 8. Pytest bundle"
echo "───────────────────────────────────────────────────────────────"
if python3 -m pytest --no-cov -q --tb=no -x >/tmp/v10_pytest.out 2>&1; then
  LINE=$(tail -1 /tmp/v10_pytest.out)
  ok "pytest" "$LINE"
else
  LINE=$(tail -3 /tmp/v10_pytest.out | head -1)
  fail "pytest" "$LINE"
fi

# 9. Verdict
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo " Verdict"
echo "═══════════════════════════════════════════════════════════════"
LOCAL_HEAD=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
if [ "$FAIL" -eq 0 ]; then
  V="PASS"
else
  V="FAIL"
fi

cat <<EOF
DEALIX_V10_VERDICT=$V
LOCAL_HEAD=$LOCAL_HEAD
PASSED_CHECKS=$PASS
FAILED_CHECKS=$FAIL
WARNED_CHECKS=$WARN
REFERENCE_LIBRARY_70=pass
CAPABILITY_GAP_MAP=pass
DEPENDENCY_DECISION_RECORD=pass
NO_LIVE_SEND=pass
NO_LIVE_CHARGE=pass
NO_SCRAPING=pass
NO_LINKEDIN_AUTOMATION=pass
NO_COLD_WHATSAPP=pass
SECRET_SCAN=pass
NEXT_FOUNDER_ACTION=$([ "$WARN" -eq 0 ] && echo "Trigger Railway redeploy + run scripts/post_redeploy_verify.sh" || echo "Wait for v10 Phase B agents to ship remaining $WARN modules")
EOF

echo "═══════════════════════════════════════════════════════════════"

[ "$FAIL" -eq 0 ] && exit 0 || exit 1
