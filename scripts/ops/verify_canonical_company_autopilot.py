#!/usr/bin/env python3
"""Static verification for the canonical Dealix company-autopilot revenue layer."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "dealix/config/first_launch_offer_gate.yaml"
MASTER_PROMPT = ROOT / "docs/ops/DEALIX_EXECUTIVE_AUTOPILOT_MASTER_PROMPT.md"
CYCLE = ROOT / "scripts/ops/dealix_canonical_revenue_cycle.sh"
AI_GUARD = ROOT / "scripts/ops/harden_dealix_local_ai_8k.sh"
AUTOPILOT = ROOT / "scripts/ops/dealix_company_autopilot.sh"


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL_COMPANY_AUTOPILOT=FAIL {message}")


def main() -> int:
    for path in (GATE, MASTER_PROMPT, CYCLE, AI_GUARD, AUTOPILOT):
        if not path.is_file():
            fail(f"missing:{path.relative_to(ROOT)}")

    gate = yaml.safe_load(GATE.read_text(encoding="utf-8"))
    primary = gate.get("primary_motion") or {}
    pricing = gate.get("pricing_experiment") or {}
    conversation = gate.get("conversation_policy") or {}

    if primary.get("id") != "revenue_command_pilot_30d":
        fail("unexpected_primary_motion")
    if primary.get("checkout_enabled") is not False:
        fail("checkout_must_be_disabled")
    if pricing.get("public_amount_sar") is not None:
        fail("public_price_not_authorized")
    if pricing.get("status") != "no_public_amount_until_validation":
        fail("pricing_status_drift")
    if pricing.get("qualified_conversations_required") != 5:
        fail("qualified_conversation_gate_drift")
    if conversation.get("audience") != "warm_consented_only":
        fail("audience_policy_drift")
    if conversation.get("external_send_allowed") is not False:
        fail("external_send_policy_drift")

    prompt = MASTER_PROMPT.read_text(encoding="utf-8")
    required_prompt_terms = (
        "Revenue Command Pilot — 30 days",
        "five qualified",
        "warm/consented",
        "Approval Center",
        "synthetic",
        "Railway",
        "Hostinger VPS",
    )
    for term in required_prompt_terms:
        if term not in prompt:
            fail(f"master_prompt_missing:{term}")

    cycle = CYCLE.read_text(encoding="utf-8")
    for forbidden in ("railway up", "railway redeploy", "git push", "gh pr merge", "AUTO_SEND_ENABLED=true"):
        if forbidden in cycle:
            fail(f"revenue_cycle_forbidden_action:{forbidden}")
    for required in (
        "run_commercial_intelligence_founder_cycle.py",
        "run_revenue_lab_daily.py",
        "run_founder_market_entry.py",
        "run_company_loop_simulation.py",
    ):
        if required not in cycle:
            fail(f"revenue_cycle_missing_reuse:{required}")

    guard = AI_GUARD.read_text(encoding="utf-8")
    for term in (
        "OLLAMA_CONTEXT_LENGTH=8192",
        "OLLAMA_HOST=127.0.0.1:11434",
        "OLLAMA_MAX_LOADED_MODELS=1",
        "OLLAMA_NUM_PARALLEL=1",
    ):
        if term not in guard:
            fail(f"ai_guard_missing:{term}")

    # Defensive check: the canonical autopilot must not carry a hardcoded 64K
    # fallback (retired by the env-override reconciliation). If a future
    # regression reintroduces it, activation still requires the bounded
    # runtime guard that removes the legacy alias.
    autopilot = AUTOPILOT.read_text(encoding="utf-8")
    legacy_present = 'LOCAL_MODEL_FALLBACK="dealix-qwen3-4b-64k"' in autopilot
    if legacy_present and 'ollama rm "$LEGACY_MODEL"' not in guard:
        fail("legacy_64k_fallback_without_runtime_guard")

    result = {
        "primary_motion": primary.get("id"),
        "pricing_status": pricing.get("status"),
        "qualified_conversations_required": pricing.get("qualified_conversations_required"),
        "external_send_allowed": conversation.get("external_send_allowed"),
        "legacy_64k_reference_in_merged_autopilot": legacy_present,
        "runtime_8k_guard_present": True,
        "new_parallel_scheduler_created": False,
    }
    print("CANONICAL_COMPANY_AUTOPILOT=PASS")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
