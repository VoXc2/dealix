#!/usr/bin/env bash
# Dealix DesignOps verifier — local-only sanity check.

set -uo pipefail

PASS=0
FAIL=0

ok() { printf "  ✅ %s\n" "$1"; PASS=$((PASS+1)); }
fail() { printf "  ❌ %s — %s\n" "$1" "$2"; FAIL=$((FAIL+1)); }

echo "═══════════════════════════════════════════════════════════════"
echo " Dealix DesignOps — Local Verification"
echo " Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "═══════════════════════════════════════════════════════════════"

# 1. Design system file present
echo ""
echo " 1. Design system"
echo "───────────────────────────────────────────────────────────────"
[ -f "design-systems/dealix/DESIGN.md" ] && ok "DESIGN.md present" || fail "DESIGN.md" "missing"
[ -f "docs/DEALIX_DESIGN_LANGUAGE.md" ] && ok "DEALIX_DESIGN_LANGUAGE.md present" || fail "DEALIX_DESIGN_LANGUAGE.md" "missing"

# 2. Skill registry — count SKILL.md files
echo ""
echo " 2. Skill registry"
echo "───────────────────────────────────────────────────────────────"
SKILL_COUNT=$(find design-skills -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
if [ "$SKILL_COUNT" -ge "8" ]; then
  ok "design-skills count = $SKILL_COUNT (≥ 8)"
else
  fail "design-skills count" "$SKILL_COUNT (expected ≥ 8)"
fi

# 3. Module structure
echo ""
echo " 3. Module structure"
echo "───────────────────────────────────────────────────────────────"
for f in __init__.py schemas.py skill_registry.py safety_gate.py brief_builder.py exporter.py; do
  if [ -f "auto_client_acquisition/designops/$f" ]; then
    ok "auto_client_acquisition/designops/$f"
  else
    fail "auto_client_acquisition/designops/$f" "missing"
  fi
done

# 4. Generators
echo ""
echo " 4. Generators"
echo "───────────────────────────────────────────────────────────────"
for f in mini_diagnostic.py proof_pack.py executive_weekly_pack.py proposal_page.py pricing_page.py customer_room_dashboard.py html_renderer.py markdown_renderer.py; do
  if [ -f "auto_client_acquisition/designops/generators/$f" ]; then
    ok "generators/$f"
  else
    fail "generators/$f" "missing"
  fi
done

# 5. Router
echo ""
echo " 5. API routes"
echo "───────────────────────────────────────────────────────────────"
[ -f "api/routers/designops.py" ] && ok "api/routers/designops.py present" || fail "api/routers/designops.py" "missing"

# 6. Forbidden claims sweep on DESIGN.md + skills
echo ""
echo " 6. Forbidden claims sweep"
echo "───────────────────────────────────────────────────────────────"
HITS=$(grep -rE 'نضمن|guaranteed' design-systems/ design-skills/ 2>/dev/null | grep -vE 'forbidden|negation|do not|never|❌|reject' | head -1)
if [ -z "$HITS" ]; then
  ok "no positive-context forbidden tokens in design-systems/ or design-skills/"
else
  fail "forbidden token leak" "$HITS"
fi

# 7. Tests
echo ""
echo " 7. Tests"
echo "───────────────────────────────────────────────────────────────"
TEST_FILES=(
  "tests/test_dealix_design_system.py"
  "tests/test_designops_skill_registry.py"
  "tests/test_designops_artifact_safety_gate.py"
  "tests/test_designops_brief_builder.py"
  "tests/test_designops_generators.py"
  "tests/test_designops_proposal_pricing.py"
  "tests/test_designops_customer_room_dashboard.py"
  "tests/test_designops_exporter.py"
)
for t in "${TEST_FILES[@]}"; do
  [ -f "$t" ] && ok "$t" || fail "$t" "missing"
done

# 8. Verdict
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo " Verdict"
echo "═══════════════════════════════════════════════════════════════"
echo " PASSED: $PASS"
echo " FAILED: $FAIL"
if [ "$FAIL" -eq 0 ]; then
  echo " DESIGNOPS_VERIFY=pass"
  exit 0
else
  echo " DESIGNOPS_VERIFY=fail"
  exit 1
fi
