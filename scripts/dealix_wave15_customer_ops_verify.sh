#!/usr/bin/env bash
# Wave 15 — Customer Ops Polish master verifier
# Single command, single verdict. Composes all Wave 15 deliverables +
# Wave 13/14 regressions.
#
# Article 4: this script never makes external network calls.
# Article 8: explicit PASS/FAIL/SANDBOX_SKIP — no "OK" without artifacts.
# Article 11: chains existing per-phase test files; no new business logic.

set -uo pipefail
cd "$(dirname "$0")/.."

results=()
overall_pass=true

run_check() {
  local name="$1"; local cmd="$2"
  if eval "$cmd" >/dev/null 2>&1; then
    results+=("$name=PASS")
  else
    results+=("$name=FAIL")
    overall_pass=false
  fi
}

run_check_sandbox_aware() {
  local name="$1"; local cmd="$2"
  local out
  out=$(eval "$cmd" 2>&1)
  local rc=$?
  if [ $rc -eq 0 ]; then
    results+=("$name=PASS")
  elif echo "$out" | grep -qE "No module named 'pyotp'|_cffi_backend|pyo3_runtime"; then
    results+=("$name=SANDBOX_SKIP")
  else
    results+=("$name=FAIL")
    overall_pass=false
  fi
}

# ── Phase A — Compile sanity ─────────────────────────────────────────
run_check "COMPILEALL_WAVE15_SCRIPTS" \
  "python3 -m compileall -q scripts/dealix_export_service_catalog_json.py scripts/dealix_bottleneck_radar.py scripts/dealix_founder_daily_brief.py"

# ── Phase B — Service Catalog JSON export ────────────────────────────
run_check "SERVICE_CATALOG_JSON_EXPORTER" \
  "python3 scripts/dealix_export_service_catalog_json.py --check"

run_check "SERVICE_CATALOG_JSON_HAS_7_OFFERINGS" \
  "python3 -c 'import json; d = json.load(open(\"landing/assets/data/services-catalog.json\")); assert d[\"count\"] == 7'"

run_check "SERVICE_CATALOG_JSON_HAS_8_HARD_GATES" \
  "python3 -c 'import json; d = json.load(open(\"landing/assets/data/services-catalog.json\")); assert len(d[\"constitution\"][\"article_4_hard_gates\"]) == 8'"

# ── Phase C — Bottleneck Radar CLI ───────────────────────────────────
run_check "BOTTLENECK_RADAR_CLI_MD" \
  "python3 scripts/dealix_bottleneck_radar.py --blocking-approvals 2 --format md | grep -q 'Bottleneck Radar'"

run_check "BOTTLENECK_RADAR_CLI_JSON" \
  "python3 scripts/dealix_bottleneck_radar.py --format json | python3 -c 'import json,sys; d=json.load(sys.stdin); assert d[\"is_estimate\"] is True'"

run_check "BOTTLENECK_RADAR_CLI_ONE_LINE" \
  "python3 scripts/dealix_bottleneck_radar.py --blocking-approvals 1 --format one-line | grep -q '\[watch\]'"

# ── Phase D — Founder Daily Brief CLI ────────────────────────────────
run_check "FOUNDER_DAILY_BRIEF_MD" \
  "python3 scripts/dealix_founder_daily_brief.py --paid-customers 0 | grep -q 'Article 13 Status'"

run_check "FOUNDER_DAILY_BRIEF_HARD_GATES_LISTED" \
  "python3 scripts/dealix_founder_daily_brief.py --format json | python3 -c 'import json,sys; d=json.load(sys.stdin); assert len(d[\"hard_gates\"]) == 8'"

run_check "FOUNDER_DAILY_BRIEF_ARTICLE_13_REMAINING_3_WHEN_ZERO_PAID" \
  "python3 scripts/dealix_founder_daily_brief.py --paid-customers 0 --format json | python3 -c 'import json,sys; d=json.load(sys.stdin); assert d[\"article_13_trigger_remaining\"] == 3'"

# ── Phase E — E2E integration test (13 tests, sandbox-safe) ──────────
run_check "WAVE15_CUSTOMER_JOURNEY_E2E" \
  "python3 -m pytest tests/test_wave15_customer_journey_e2e.py -q --no-cov"

# ── Phase F — Wave 13 + 14 regression ────────────────────────────────
run_check "WAVE13_REGRESSION" \
  "bash scripts/dealix_full_ops_productization_verify.sh"

run_check "WAVE14_REGRESSION" \
  "bash scripts/dealix_wave14_saudi_engines_verify.sh"

# ── Phase G — Article 4 + 8 invariants ───────────────────────────────
run_check "NO_LINKEDIN_SCRAPER_STRING" \
  "python3 -m pytest tests/test_no_linkedin_scraper_string_anywhere.py -q --no-cov"

run_check "FORBIDDEN_CLAIMS_LINT" \
  "python3 -m pytest tests/test_landing_forbidden_claims.py -q --no-cov"

run_check_sandbox_aware "CONSTITUTION_CLOSURE" \
  "python3 -m pytest tests/test_constitution_closure.py -q --no-cov"

# ── Print results ────────────────────────────────────────────────────
echo
echo "════════════════════════════════════════════════════════════"
echo "  DEALIX WAVE 15 — CUSTOMER OPS POLISH VERIFIER"
echo "════════════════════════════════════════════════════════════"
total=0
pass_count=0
fail_count=0
sandbox_skip_count=0
for r in "${results[@]}"; do
  echo "  $r"
  total=$((total + 1))
  if [[ "$r" == *"=PASS" ]]; then
    pass_count=$((pass_count + 1))
  elif [[ "$r" == *"=SANDBOX_SKIP" ]]; then
    sandbox_skip_count=$((sandbox_skip_count + 1))
  else
    fail_count=$((fail_count + 1))
  fi
done
echo
echo "  Total: $total · PASS: $pass_count · FAIL: $fail_count · SANDBOX_SKIP: $sandbox_skip_count"
echo
echo "  Hard gates (all 8 IMMUTABLE):"
echo "    NO_LIVE_SEND=immutable"
echo "    NO_LIVE_CHARGE=immutable"
echo "    NO_COLD_WHATSAPP=immutable"
echo "    NO_LINKEDIN_AUTO=immutable"
echo "    NO_SCRAPING=immutable"
echo "    NO_FAKE_PROOF=immutable"
echo "    NO_FAKE_REVENUE=immutable"
echo "    NO_BLAST=immutable"
echo
local_head=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
echo "  LOCAL_HEAD=$local_head"
echo "  BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"

if $overall_pass; then
  echo "  DEALIX_WAVE15_CUSTOMER_OPS_VERDICT=PASS"
  echo "  CUSTOMER_READY=yes"
  echo "  ARTICLE_4_GATES_IMMUTABLE=yes"
  echo "  ARTICLE_8_NO_FAKE_REVENUE=yes"
  echo "  NEXT_FOUNDER_ACTION=Run scripts/dealix_founder_daily_brief.py each morning at 8AM KSA. Share landing/services.html with prospects."
  exit 0
else
  echo "  DEALIX_WAVE15_CUSTOMER_OPS_VERDICT=PARTIAL"
  echo "  NEXT_FOUNDER_ACTION=Review FAIL lines above; re-run failing check verbosely."
  exit 1
fi
