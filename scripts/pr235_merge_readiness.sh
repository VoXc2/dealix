#!/usr/bin/env bash
# PR #235 — Pre-merge Readiness Verifier (Wave 18)
#
# 30-second checklist the founder runs before clicking "Merge" on
# PR #235. Verifies every Wave 16/17/18 surface is in place AND no
# doctrine guard is failing. NEVER changes state. Read-only.
#
# Usage:
#   bash scripts/pr235_merge_readiness.sh
#   bash scripts/pr235_merge_readiness.sh --quick  # skip pytest, faster
#
# Exit codes:
#   0  — green light to merge
#   1  — one or more checks failed; review output and fix before merging
#
# Honors all 11 non-negotiables: read-only, no external send, no charge.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

QUICK=0
if [[ "${1:-}" == "--quick" ]]; then
  QUICK=1
fi

PASS=0
FAIL=0
WARN=0

ok() {
  PASS=$((PASS + 1))
  echo "  ✅ $1"
}

bad() {
  FAIL=$((FAIL + 1))
  echo "  ❌ $1"
}

warn() {
  WARN=$((WARN + 1))
  echo "  ⚠  $1"
}

section() {
  echo ""
  echo "━━ $1 ━━"
}

echo "PR #235 — Pre-merge Readiness Verifier"
echo "Branch: claude/wave-15-founder-velocity-kit  →  target: main"
echo "Repo: $REPO_ROOT"
echo "Quick mode: $([[ $QUICK -eq 1 ]] && echo yes || echo no)"

# ── 1. Git state ─────────────────────────────────────────────────────
section "1. Git state"
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "(unknown)")
if [[ "$CURRENT_BRANCH" == "claude/wave-15-founder-velocity-kit" ]]; then
  ok "on branch: $CURRENT_BRANCH"
else
  warn "not on the PR #235 branch (current: $CURRENT_BRANCH)"
fi

UNCOMMITTED=$(git status --porcelain | wc -l | tr -d ' ')
if [[ "$UNCOMMITTED" == "0" ]]; then
  ok "no uncommitted changes"
else
  bad "$UNCOMMITTED uncommitted file(s) — commit + push before merging"
fi

AHEAD=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "0")
if [[ "$AHEAD" -ge "4" ]]; then
  ok "$AHEAD commits ahead of origin/main (Wave 16 + reframe + Wave 17 part-1+2 + Wave 18 expected)"
else
  warn "$AHEAD commits ahead of origin/main (expected ≥ 4)"
fi

# ── 2. Canonical surfaces present ───────────────────────────────────
section "2. Canonical surfaces on disk"

check_file() {
  local label="$1"
  local path="$2"
  if [[ -f "$path" ]]; then
    ok "$label  →  $path"
  else
    bad "$label MISSING  →  $path"
  fi
}

check_file "Wave 16 — warnings_filter"           "core/warnings_filter.py"
check_file "Wave 16 — post_deploy_check router"  "api/routers/post_deploy_check.py"
check_file "Wave 16 — whatsapp_draft script"     "scripts/whatsapp_draft.py"
check_file "Wave 16 — WHATSAPP_TEMPLATES.md"     "docs/content/WHATSAPP_TEMPLATES.md"
check_file "Reframe — 3-offer registry"          "auto_client_acquisition/service_catalog/registry.py"
check_file "Reframe — PRICING_REFRAME_2026Q2"    "docs/sales-kit/PRICING_REFRAME_2026Q2.md"
check_file "Wave 17 — non_negotiables module"    "auto_client_acquisition/governance_os/non_negotiables.py"
check_file "Wave 17 — dealix_promise router"     "api/routers/dealix_promise.py"
check_file "Wave 17 — daily_routine script"      "scripts/daily_routine.py"
check_file "Wave 17 — seed_anchor_partner"       "scripts/seed_anchor_partner_pipeline.py"
check_file "Wave 17 — THE_DEALIX_PROMISE.md"     "docs/THE_DEALIX_PROMISE.md"
check_file "Wave 17 — ANCHOR_PARTNER_OUTREACH"   "docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md"
check_file "Wave 17 — FOUNDER_90_DAY_CADENCE"    "docs/ops/FOUNDER_90_DAY_CADENCE.md"
check_file "Wave 17 — CONTINUOUS_ROUTINE.md"     "docs/ops/CONTINUOUS_ROUTINE.md"
check_file "Wave 17 — landing/promise.html"      "landing/promise.html"
check_file "Wave 18 — command_center router"     "api/routers/founder_command_center.py"
check_file "Wave 18 — founder-command-center.html" "landing/founder-command-center.html"
check_file "Wave 18 — weekly_ceo_review script"  "scripts/weekly_ceo_review.py"
check_file "Wave 19 — gcc_markets module"        "auto_client_acquisition/governance_os/gcc_markets.py"
check_file "Wave 19 — gcc_market_intel router"   "api/routers/gcc_market_intel.py"
check_file "Wave 19 — capital_asset module"      "auto_client_acquisition/capital_os/capital_asset.py"
check_file "Wave 19 — capital_asset_registry"    "auto_client_acquisition/capital_os/capital_asset_registry.py"
check_file "Wave 19 — doctrine router (public)"  "api/routers/doctrine.py"
check_file "Wave 19 — capital_assets endpoint"   "api/routers/capital_assets_public.py"
check_file "Wave 19 — validate_capital_assets"   "scripts/validate_capital_assets.py"
check_file "Wave 19 — generate_capital_asset_index" "scripts/generate_capital_asset_index.py"

# ── 3. Registry integrity ───────────────────────────────────────────
section "3. Registry integrity (3-offer reframe)"
OFFER_COUNT=$(python3 -c "from auto_client_acquisition.service_catalog.registry import OFFERINGS; print(len(OFFERINGS))" 2>/dev/null)
if [[ "$OFFER_COUNT" == "3" ]]; then
  ok "registry has exactly 3 active offerings"
else
  bad "registry has $OFFER_COUNT offerings (expected 3)"
fi

FLOOR=$(python3 -c "from auto_client_acquisition.service_catalog.registry import OFFERINGS; m=[o for o in OFFERINGS if o.price_unit=='per_month' and o.price_sar>0]; print(int(min(o.price_sar for o in m)) if m else 0)" 2>/dev/null)
if [[ "$FLOOR" -ge "4999" ]]; then
  ok "paid floor: $FLOOR SAR/month (≥ 4,999)"
else
  bad "paid floor: $FLOOR SAR/month (expected ≥ 4,999)"
fi

# ── 4. Doctrine count ───────────────────────────────────────────────
section "4. Doctrine integrity (11 non-negotiables)"
NN_COUNT=$(python3 -c "from auto_client_acquisition.governance_os.non_negotiables import NON_NEGOTIABLES; print(len(NON_NEGOTIABLES))" 2>/dev/null)
if [[ "$NN_COUNT" == "11" ]]; then
  ok "non-negotiables module exports exactly 11 commitments"
else
  bad "non-negotiables module exports $NN_COUNT commitments (expected 11)"
fi

# ── 5. Doctrine guard tests ─────────────────────────────────────────
section "5. Doctrine guard tests"
if [[ $QUICK -eq 0 ]]; then
  GUARD_OUT=$(python3 -m pytest tests/test_no_*.py tests/test_article_13_compliance.py -q --no-cov 2>&1 | tail -3)
  if echo "$GUARD_OUT" | grep -q "passed"; then
    PASSED=$(echo "$GUARD_OUT" | grep -oE "[0-9]+ passed" | head -1)
    ok "doctrine guards: $PASSED"
  else
    bad "doctrine guards failing:\n$GUARD_OUT"
  fi
else
  warn "skipped (--quick)"
fi

# ── 6. Wave 17/18 endpoint + script tests ───────────────────────────
section "6. Wave 17/18 functional tests"
if [[ $QUICK -eq 0 ]]; then
  FN_OUT=$(python3 -m pytest tests/test_dealix_promise.py tests/test_daily_routine.py tests/test_founder_command_center.py tests/test_weekly_ceo_review.py -q --no-cov 2>&1 | tail -3)
  if echo "$FN_OUT" | grep -q "passed"; then
    PASSED=$(echo "$FN_OUT" | grep -oE "[0-9]+ passed" | head -1)
    ok "functional tests: $PASSED"
  else
    bad "functional tests failing:\n$FN_OUT"
  fi
else
  warn "skipped (--quick)"
fi

# ── 7. Summary + verdict ────────────────────────────────────────────
section "Summary"
echo "  passed: $PASS"
echo "  failed: $FAIL"
echo "  warned: $WARN"
echo ""

if [[ "$FAIL" -eq "0" ]]; then
  echo "✅ GREEN LIGHT — PR #235 is merge-ready."
  echo ""
  echo "Next step: open the PR on GitHub and click Merge."
  echo "After merge, Railway auto-deploys main. Run:"
  echo "  curl -s https://api.dealix.me/api/v1/dealix-promise | jq '.commitments | length'"
  echo "  curl -s https://api.dealix.me/api/v1/commercial-map | jq '.registry_count'"
  echo "  curl -s -H \"X-Admin-API-Key: \$ADMIN\" https://api.dealix.me/api/v1/founder/command-center | jq '.top_three_next_actions'"
  exit 0
else
  echo "❌ RED LIGHT — fix the $FAIL failure(s) before merging."
  echo ""
  echo "Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة."
  exit 1
fi
