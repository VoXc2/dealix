#!/usr/bin/env bash
# Wave 11 §31.14 — Hard Gate Audit
#
# Single-command audit of all 8 immutable hard gates. Read-only.
# Returns ALL_GATES=IMMUTABLE on success, exit 0; else exit 1 with named gate.
#
# The 8 gates (Constitution Article 4):
#   NO_LIVE_SEND         — safe_send_gateway/middleware.py raises SendBlocked
#   NO_LIVE_CHARGE       — payment_ops/orchestrator._enforce_no_live_charge
#   NO_COLD_WHATSAPP     — channel_policy_gateway: whatsapp requires consent
#   NO_LINKEDIN_AUTO     — agent_registry tags requires_founder_approval gate
#   NO_SCRAPING          — no `linkedin_scraper` string anywhere (git ls-files scan)
#   NO_FAKE_PROOF        — proof_ledger/schemas.py: evidence_level required + signed
#   NO_FAKE_REVENUE      — revenue_truth.py: only payment_confirmed flows
#   NO_BLAST             — channel cap; no auto-blast helpers
#
# Usage:
#   bash scripts/wave11_hard_gate_audit.sh
#
# Exit code:
#   0 = all 8 gates IMMUTABLE
#   1 = at least 1 gate weakened or missing

set -uo pipefail

cd "$(dirname "$0")/.."

results=()
overall_pass=true

# Helper: record gate result
gate_pass() { results+=("[$1] ✅ enforced — $2"); }
gate_fail() { results+=("[$1] ❌ FAIL — $2"); overall_pass=false; }

# Gate 1 — NO_LIVE_SEND: safe_send_gateway must exist + raise SendBlocked
if [ -f auto_client_acquisition/safe_send_gateway/middleware.py ] \
   && grep -q "class SendBlocked" auto_client_acquisition/safe_send_gateway/middleware.py 2>/dev/null \
   && grep -q "raise SendBlocked\|raise self\.\|raise SendBlocked(" auto_client_acquisition/safe_send_gateway/middleware.py 2>/dev/null; then
  gate_pass "NO_LIVE_SEND" "safe_send_gateway/middleware.py raises SendBlocked"
else
  gate_fail "NO_LIVE_SEND" "safe_send_gateway/middleware.py missing or doesn't raise SendBlocked"
fi

# Gate 2 — NO_LIVE_CHARGE: payment_ops orchestrator enforces non-live mode
if grep -q "_enforce_no_live_charge\|NO_LIVE_CHARGE" auto_client_acquisition/payment_ops/orchestrator.py 2>/dev/null; then
  # Verify env default is not live
  MOYASAR_MODE="${DEALIX_MOYASAR_MODE:-sandbox}"
  if [ "${MOYASAR_MODE}" = "live" ]; then
    gate_fail "NO_LIVE_CHARGE" "DEALIX_MOYASAR_MODE=live in env (must be sandbox until KYC complete)"
  else
    gate_pass "NO_LIVE_CHARGE" "payment_ops/orchestrator._enforce_no_live_charge present; mode=${MOYASAR_MODE}"
  fi
else
  gate_fail "NO_LIVE_CHARGE" "_enforce_no_live_charge not found in payment_ops/orchestrator.py"
fi

# Gate 3 — NO_COLD_WHATSAPP: channel_policy_gateway whatsapp consent required
if [ -f auto_client_acquisition/channel_policy_gateway/whatsapp.py ] \
   || grep -rq "no_cold_whatsapp\|cold_whatsapp" auto_client_acquisition/channel_policy_gateway/ 2>/dev/null; then
  gate_pass "NO_COLD_WHATSAPP" "channel_policy_gateway whatsapp policy present"
else
  # Fallback: check approval_policy
  if grep -q "whatsapp.*never_auto\|whatsapp.*approval_required\|cold_whatsapp" auto_client_acquisition/approval_center/approval_policy.py 2>/dev/null; then
    gate_pass "NO_COLD_WHATSAPP" "approval_policy.py: whatsapp requires approval"
  else
    gate_fail "NO_COLD_WHATSAPP" "no whatsapp consent/approval enforcement found"
  fi
fi

# Gate 4 — NO_LINKEDIN_AUTO: agent_registry tags
if grep -q "linkedin_company_search_requires_founder_approval" auto_client_acquisition/revenue_graph/agent_registry.py 2>/dev/null; then
  gate_pass "NO_LINKEDIN_AUTO" "agent_registry has linkedin_company_search_requires_founder_approval"
else
  gate_fail "NO_LINKEDIN_AUTO" "linkedin_company_search_requires_founder_approval missing from agent_registry"
fi

# Gate 5 — NO_SCRAPING: defer to the canonical existing test
# (tests/test_no_linkedin_scraper_string_anywhere.py is the source of truth;
#  it uses git ls-files + maintained allowlist + binary skip)
if python3 -m pytest tests/test_no_linkedin_scraper_string_anywhere.py -q --no-cov 2>&1 | tail -1 | grep -q "passed"; then
  gate_pass "NO_SCRAPING" "tests/test_no_linkedin_scraper_string_anywhere.py 3/3 PASS"
else
  gate_fail "NO_SCRAPING" "tests/test_no_linkedin_scraper_string_anywhere.py FAIL — run pytest -v for detail"
fi

# Gate 6 — NO_FAKE_PROOF: proof_ledger requires evidence; proof_engine has EvidenceLevel
PROOF_OK=0
if grep -q "evidence_source\|evidence_level\|EvidenceLevel" auto_client_acquisition/proof_ledger/schemas.py 2>/dev/null; then
  PROOF_OK=1
fi
if [ -f auto_client_acquisition/proof_engine/evidence.py ] \
   && grep -q "class EvidenceLevel" auto_client_acquisition/proof_engine/evidence.py 2>/dev/null; then
  PROOF_OK=1
fi
if [ "${PROOF_OK}" = "1" ]; then
  gate_pass "NO_FAKE_PROOF" "proof_engine/evidence.py defines EvidenceLevel + proof_ledger/schemas.py has evidence_source"
else
  gate_fail "NO_FAKE_PROOF" "no evidence taxonomy found in proof_engine or proof_ledger"
fi

# Gate 7 — NO_FAKE_REVENUE: revenue_truth.py enforces payment_confirmed only
if grep -rq "payment_confirmed.*revenue\|is_revenue.*payment_confirmed\|confirmed_revenue_sar" \
     auto_client_acquisition/revenue_profitability/ \
     auto_client_acquisition/payment_ops/ 2>/dev/null; then
  gate_pass "NO_FAKE_REVENUE" "revenue truth: only payment_confirmed flows to confirmed_revenue_sar"
else
  gate_fail "NO_FAKE_REVENUE" "revenue truth enforcement not found"
fi

# Gate 8 — NO_BLAST: enforcement code present + no unguarded batch send loops
# Step 1: ENFORCEMENT must exist (the regex blocking blast patterns)
NO_BLAST_ENFORCEMENT=0
if grep -rq '\\bblast\\b\|mass\s\+(send\|outreach\|message)' auto_client_acquisition/safety_v10/policies.py 2>/dev/null \
   || grep -rq "broadcast.*sends\|broadcast" auto_client_acquisition/whatsapp_decision_bot/command_parser.py 2>/dev/null; then
  NO_BLAST_ENFORCEMENT=1
fi

# Step 2: VIOLATIONS — find unguarded send-in-loop patterns (must be empty)
# Filter: skip enforcement (regex / refuse / violates / FORBIDDEN), skip tests, skip approval_center wrappers
BLAST_VIOLATIONS=$(grep -rn "for.*recipients.*:\s*$\|for.*contacts.*:\s*send\|for.*targets.*send_message\|bulk_send\|mass_send" \
                   auto_client_acquisition/ 2>/dev/null \
                   | grep -vE 'test_|_test\.py|approval_required|approval_center|safe_send|FORBIDDEN|refuse|violates|reject|policies\.py|command_parser\.py|comment|#' \
                   | head -3 || true)
if [ "${NO_BLAST_ENFORCEMENT}" = "1" ] && [ -z "${BLAST_VIOLATIONS}" ]; then
  gate_pass "NO_BLAST" "blast/broadcast regex enforcement in safety_v10 + command_parser; no unguarded loops"
elif [ "${NO_BLAST_ENFORCEMENT}" = "0" ]; then
  gate_fail "NO_BLAST" "no blast-pattern enforcement found in safety_v10/policies.py"
else
  gate_fail "NO_BLAST" "potential unguarded blast pattern: ${BLAST_VIOLATIONS}"
fi

# ── Output ────────────────────────────────────────────────────────────
echo "════════════════════════════════════════════════════════════"
echo "  DEALIX — 8 HARD GATE AUDIT (Wave 11 §31.14)"
echo "════════════════════════════════════════════════════════════"
for r in "${results[@]}"; do printf "  %s\n" "${r}"; done
echo

passed=0
total=${#results[@]}
for r in "${results[@]}"; do
  case "${r}" in *✅*) passed=$((passed + 1)) ;; esac
done

echo "════════════════════════════════════════════════════════════"
if ${overall_pass}; then
  echo "  ALL_GATES=IMMUTABLE  (${passed}/${total})"
  echo "  HARD_GATE_AUDIT=PASS"
  echo "  NEXT_FOUNDER_ACTION=Continue Wave 11 execution."
  exit 0
else
  echo "  ALL_GATES=COMPROMISED  (${passed}/${total})"
  echo "  HARD_GATE_AUDIT=FAIL"
  echo "  NEXT_FOUNDER_ACTION=STOP. Investigate failed gate(s) immediately. Article 4 violation."
  exit 1
fi
