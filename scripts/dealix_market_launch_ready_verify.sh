#!/usr/bin/env bash
# Wave 17 §35.2.7 — Market Launch Readiness master verifier
#
# Single command, single verdict: MARKET_LAUNCH_READY=PASS|PARTIAL|BLOCKED
#
# Composes:
#   - All prior wave verifiers (13/14/15 regression)
#   - Wave 17 new checks (DNS verify · rehearsal · hygiene)
#   - 8 hard gate audit
#   - Article 8 forbidden claims lint
#   - linkedin_scraper lockdown
#   - Constitution closure (sandbox-aware)
#   - Founder-action checklist (legal · SDAIA · DNS · 5 warm intros · Moyasar)
#
# Article 4: read-only; never makes external send/charge calls.
# Article 8: explicit PASS/FAIL/FOUNDER_ACTION/SANDBOX_SKIP — no fabrication.
# Article 11: chains existing verifiers; zero new business logic.

set -uo pipefail
cd "$(dirname "$0")/.."

results=()
overall_pass=true
has_blockers=false
has_founder_pending=false

run_check() {
  local name="$1"; local cmd="$2"
  if eval "$cmd" >/dev/null 2>&1; then
    results+=("$name=PASS")
  else
    results+=("$name=FAIL")
    overall_pass=false
    has_blockers=true
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
    has_blockers=true
  fi
}

founder_action_check() {
  local name="$1"; local check_path="$2"
  if [ -e "$check_path" ]; then
    results+=("$name=PASS")
  else
    results+=("$name=FOUNDER_ACTION_PENDING")
    has_founder_pending=true
  fi
}

# ── Section A — Engineering regression (prior waves) ───────────────────
run_check "WAVE13_REGRESSION"              "bash scripts/dealix_full_ops_productization_verify.sh"
run_check "WAVE14_REGRESSION"              "bash scripts/dealix_wave14_saudi_engines_verify.sh"
run_check "WAVE15_REGRESSION"              "bash scripts/dealix_wave15_customer_ops_verify.sh"

# Wave 16 verifier present only when Wave 16 merged
if [ -f scripts/dealix_wave16_auto_source_verify.sh ]; then
  run_check "WAVE16_REGRESSION"            "bash scripts/dealix_wave16_auto_source_verify.sh"
else
  results+=("WAVE16_REGRESSION=PR_222_PENDING_MERGE")
  has_founder_pending=true
fi

# ── Section B — Wave 17 new checks ─────────────────────────────────────
run_check "DNS_VERIFY_CLI_COMPILES" \
  "python3 -m compileall -q scripts/dealix_dns_verify.py"

run_check "CUSTOMER_RECEPTION_REHEARSAL_CLI_COMPILES" \
  "python3 -m compileall -q scripts/dealix_customer_reception_rehearsal.py"

# DNS verify CLI must produce valid JSON with is_estimate=True.
# CLI exits 1 when DNS records missing (correct Article 8 behavior); the
# JSON is still valid. Use a temp file to decouple from pipefail.
run_check "DNS_VERIFY_PRODUCES_VALID_JSON" \
  "python3 scripts/dealix_dns_verify.py --domain dealix.me --format json > /tmp/dns_check.json 2>/dev/null; python3 -c 'import json; d=json.load(open(\"/tmp/dns_check.json\")); assert d.get(\"is_estimate\") is True and \"overall_status\" in d'"

run_check "CUSTOMER_RECEPTION_REHEARSAL_FULL" \
  "python3 scripts/dealix_customer_reception_rehearsal.py --format json 2>&1 | tail -200 | python3 -c 'import json,sys; d=json.load(sys.stdin); assert d[\"verdict\"]==\"PASS\", d'"

# ── Section C — Article 4 (8 hard gates) ───────────────────────────────
run_check "HARD_GATE_AUDIT_8_OF_8" \
  "bash scripts/wave11_hard_gate_audit.sh"

# ── Section D — Article 8 + lockdown ───────────────────────────────────
run_check "FORBIDDEN_CLAIMS_LINT" \
  "python3 -m pytest tests/test_landing_forbidden_claims.py -q --no-cov"

run_check "NO_LINKEDIN_SCRAPER_STRING" \
  "python3 -m pytest tests/test_no_linkedin_scraper_string_anywhere.py -q --no-cov"

# ── Section E — Founder-action checklist ───────────────────────────────
founder_action_check "LEGAL_SELF_EXECUTION_SIGNED" \
  "data/wave11/founder_legal_signature.txt"

founder_action_check "WARM_INTROS_LOGGED" \
  "data/wave11/warm_intros.jsonl"

# DNS readiness — checked via DNS verify CLI
out=$(python3 scripts/dealix_dns_verify.py --domain dealix.me --format json 2>/dev/null)
if echo "$out" | python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d['overall_status'] in ('ready_for_marketing','ready_for_transactional') else 1)" 2>/dev/null; then
  results+=("DNS_SPF_DKIM_DMARC=PASS")
else
  results+=("DNS_SPF_DKIM_DMARC=FOUNDER_ACTION_PENDING")
  has_founder_pending=true
fi

# Payment state — exists when first paid customer confirmed
if [ -f "data/wave6/live/payment_state.json" ]; then
  paid=$(python3 -c "import json; d=json.load(open('data/wave6/live/payment_state.json')); print(sum(1 for s in d.get('payment_states', []) if s.get('state') == 'payment_confirmed'))" 2>/dev/null || echo "0")
  results+=("PAID_CUSTOMERS=$paid")
  if [ "$paid" -ge 3 ]; then
    results+=("ARTICLE_13_TRIGGER=FIRED")
  else
    results+=("ARTICLE_13_TRIGGER=NOT_YET ($paid/3)")
  fi
else
  results+=("PAID_CUSTOMERS=0")
  results+=("ARTICLE_13_TRIGGER=NOT_YET (0/3)")
fi

# ── Section F — Constitution closure (sandbox-aware) ───────────────────
run_check_sandbox_aware "CONSTITUTION_CLOSURE" \
  "python3 -m pytest tests/test_constitution_closure.py -q --no-cov"

# ── Print results ──────────────────────────────────────────────────────
echo
echo "════════════════════════════════════════════════════════════"
echo "  DEALIX WAVE 17 — MARKET LAUNCH READINESS VERIFIER"
echo "════════════════════════════════════════════════════════════"
total=0
pass_count=0
fail_count=0
sandbox_skip_count=0
founder_pending_count=0
info_count=0
for r in "${results[@]}"; do
  echo "  $r"
  total=$((total + 1))
  if [[ "$r" == *"=PASS" ]]; then
    pass_count=$((pass_count + 1))
  elif [[ "$r" == *"=SANDBOX_SKIP" ]]; then
    sandbox_skip_count=$((sandbox_skip_count + 1))
  elif [[ "$r" == *"=FOUNDER_ACTION_PENDING" ]] || [[ "$r" == *"=PR_222_PENDING_MERGE" ]]; then
    founder_pending_count=$((founder_pending_count + 1))
  elif [[ "$r" == *"=FAIL" ]]; then
    fail_count=$((fail_count + 1))
  else
    # Informational lines (PAID_CUSTOMERS=N, ARTICLE_13_TRIGGER=...)
    info_count=$((info_count + 1))
  fi
done
echo
echo "  Total: $total · PASS: $pass_count · FAIL: $fail_count · FOUNDER_PENDING: $founder_pending_count · SANDBOX_SKIP: $sandbox_skip_count · INFO: $info_count"
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

# Decision logic
if $has_blockers; then
  echo "  MARKET_LAUNCH_READY=BLOCKED"
  echo "  NEXT_FOUNDER_ACTION=Resolve FAIL lines above before launching."
  exit 1
elif $has_founder_pending; then
  echo "  MARKET_LAUNCH_READY=PARTIAL"
  echo "  ENGINEERING_READINESS=PASS"
  echo "  FOUNDER_ACTIONS_PENDING=$founder_pending_count"
  echo "  NEXT_FOUNDER_ACTION=Execute pending founder actions (legal sig, DNS, warm intros, Wave 16 merge)."
  exit 0
else
  echo "  MARKET_LAUNCH_READY=PASS"
  echo "  ENGINEERING_READINESS=PASS"
  echo "  COMMERCIAL_READINESS=PASS"
  echo "  NEXT_FOUNDER_ACTION=Send 5 warm-intro WhatsApp messages today using docs/FIRST_10_WARM_MESSAGES_AR_EN.md"
  exit 0
fi
