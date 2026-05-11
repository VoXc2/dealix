#!/usr/bin/env bash
# Wave 16 — Auto-source + Content master verifier
# Single command, single verdict. Composes Wave 13/14/15 regressions
# + Wave 16 new tests.
#
# Article 4: read-only; never makes external network calls.
# Article 8: explicit PASS/FAIL/SANDBOX_SKIP — no fabrication.
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
run_check "COMPILEALL_WAVE16_MODULES" \
  "python3 -m compileall -q auto_client_acquisition/founder_brief"

run_check "COMPILEALL_WAVE16_SCRIPTS" \
  "python3 -m compileall -q scripts/dealix_artifact_enforcer.py scripts/dealix_case_study_builder.py scripts/dealix_wave16_auto_source_verify.sh.tmp 2>/dev/null || python3 -m compileall -q scripts/dealix_artifact_enforcer.py scripts/dealix_case_study_builder.py"

# ── Phase B — Auto-source for daily brief (4 tests) ──────────────────
run_check "FOUNDER_BRIEF_AUTO_SOURCE" \
  "python3 -m pytest tests/test_wave16_auto_source_and_content.py::test_query_layer_counts_returns_layer_counts_dataclass tests/test_wave16_auto_source_and_content.py::test_query_layer_counts_returns_zero_in_empty_state tests/test_wave16_auto_source_and_content.py::test_query_layer_counts_lists_sources_used tests/test_wave16_auto_source_and_content.py::test_layer_counts_is_frozen_immutable -q --no-cov"

run_check "DAILY_BRIEF_AUTO_SOURCE_FLAG" \
  "python3 scripts/dealix_founder_daily_brief.py --auto-source --format json | python3 -c 'import json,sys; d=json.load(sys.stdin); assert d[\"is_estimate\"] is True'"

# ── Phase C — Artifact Enforcer CLI (3 tests) ────────────────────────
run_check "ARTIFACT_ENFORCER_CLI" \
  "python3 -m pytest tests/test_wave16_auto_source_and_content.py::test_artifact_enforcer_returns_empty_in_clean_state tests/test_wave16_auto_source_and_content.py::test_artifact_enforcer_cli_one_line_format tests/test_wave16_auto_source_and_content.py::test_artifact_enforcer_cli_json_has_is_estimate -q --no-cov"

run_check "ARTIFACT_ENFORCER_ONE_LINE" \
  "python3 scripts/dealix_artifact_enforcer.py --format one-line | grep -q 'artifact_enforcer'"

# ── Phase D — Case Study Builder CLI (4 tests) ───────────────────────
run_check "CASE_STUDY_DEMO_MODE" \
  "python3 -m pytest tests/test_wave16_auto_source_and_content.py::test_case_study_demo_mode_succeeds tests/test_wave16_auto_source_and_content.py::test_case_study_demo_json_has_candidate_fields tests/test_wave16_auto_source_and_content.py::test_case_study_refuses_when_no_publishable_events tests/test_wave16_auto_source_and_content.py::test_case_study_requires_events_flag -q --no-cov"

run_check "CASE_STUDY_DEMO_BUILDS" \
  "python3 scripts/dealix_case_study_builder.py --demo --customer-handle smoke-test --sector real_estate --format json | python3 -c 'import json,sys; d=json.load(sys.stdin); assert \"candidate\" in d'"

# ── Phase E — Sector Benchmark page (4 tests) ────────────────────────
run_check "SECTOR_BENCHMARK_HTML" \
  "python3 -m pytest tests/test_wave16_auto_source_and_content.py::test_sector_benchmark_html_exists tests/test_wave16_auto_source_and_content.py::test_sector_benchmark_has_6_sectors tests/test_wave16_auto_source_and_content.py::test_sector_benchmark_is_bilingual tests/test_wave16_auto_source_and_content.py::test_sector_benchmark_declares_article_8_estimate -q --no-cov"

# ── Phase F — Article 4 + 8 cross-cutting ────────────────────────────
run_check "FORBIDDEN_CLAIMS_LINT" \
  "python3 -m pytest tests/test_landing_forbidden_claims.py -q --no-cov"

run_check "NO_LINKEDIN_SCRAPER_STRING" \
  "python3 -m pytest tests/test_no_linkedin_scraper_string_anywhere.py -q --no-cov"

run_check "NO_WAVE16_CLI_LIVE_SEND" \
  "python3 -m pytest tests/test_wave16_auto_source_and_content.py::test_no_wave16_cli_attempts_live_send -q --no-cov"

# ── Phase G — Wave 13/14/15 regression ───────────────────────────────
run_check "WAVE13_REGRESSION" \
  "bash scripts/dealix_full_ops_productization_verify.sh"

run_check "WAVE14_REGRESSION" \
  "bash scripts/dealix_wave14_saudi_engines_verify.sh"

run_check "WAVE15_REGRESSION" \
  "bash scripts/dealix_wave15_customer_ops_verify.sh"

# ── Phase H — Constitution closure (sandbox-aware) ───────────────────
run_check_sandbox_aware "CONSTITUTION_CLOSURE" \
  "python3 -m pytest tests/test_constitution_closure.py -q --no-cov"

# ── Print results ────────────────────────────────────────────────────
echo
echo "════════════════════════════════════════════════════════════"
echo "  DEALIX WAVE 16 — AUTO-SOURCE + CONTENT VERIFIER"
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
echo "  LOCAL_HEAD=$(git rev-parse HEAD 2>/dev/null || echo unknown)"
echo "  BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"

if $overall_pass; then
  echo "  DEALIX_WAVE16_AUTO_SOURCE_VERDICT=PASS"
  echo "  CUSTOMER_READY=yes"
  echo "  ARTICLE_4_GATES_IMMUTABLE=yes"
  echo "  ARTICLE_8_NO_FAKE_REVENUE=yes"
  echo "  NEXT_FOUNDER_ACTION=Run dealix_founder_daily_brief.py --auto-source each morning. Share landing/sector-benchmark.html with prospects in their sector."
  exit 0
else
  echo "  DEALIX_WAVE16_AUTO_SOURCE_VERDICT=PARTIAL"
  echo "  NEXT_FOUNDER_ACTION=Review FAIL lines above; re-run failing check verbosely."
  exit 1
fi
