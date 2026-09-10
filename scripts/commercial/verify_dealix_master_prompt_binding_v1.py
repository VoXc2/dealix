#!/usr/bin/env python3
"""Fail-closed verifier for the Dealix Omega founder command-room master prompt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BINDING = ROOT / "config" / "company" / "dealix_master_prompt_binding_v1.json"

CANONICAL_AGENTS = {
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    try:
        require(BINDING.is_file(), "master prompt binding missing")
        binding = json.loads(BINDING.read_text(encoding="utf-8"))
        require(binding.get("schema_version") == 1, "unsupported binding schema")
        require(binding.get("north_star") == "CASH_READY_AUTONOMOUS_DEALIX_COMPANY", "north star drift")
        require(binding.get("mode") == "AGENT_FIRST_FOUNDER_EXCEPTION_ONLY", "agent-first mode required")
        require(set(binding.get("permanent_agents", [])) == CANONICAL_AGENTS, "permanent agent set drift")
        require(binding.get("deep_wip_max") == 3, "deep WIP drift")
        require(binding.get("l0_l4_autonomous") is True, "L0-L4 autonomy must be enabled")
        require(binding.get("l5_exact_action_bound") is True, "L5 must remain exact-action-bound")
        for key in (
            "external_send_default",
            "public_publish_default",
            "payment_execution_default",
            "production_mutation_default",
            "scheduler_created",
        ):
            require(binding.get(key) is False, f"unsafe default drift: {key}")
        require(binding.get("canonical_scheduler_reused") is True, "canonical scheduler must be reused")
        prompt_ref = str(binding.get("prompt_ref", ""))
        prompt = ROOT / prompt_ref
        require(prompt.is_file(), f"master prompt missing: {prompt_ref}")
        text = prompt.read_text(encoding="utf-8")
        require(len(text) >= 12000, "master prompt unexpectedly small")
        for marker in binding.get("required_prompt_markers", []):
            require(marker in text, f"master prompt marker missing: {marker}")
        for agent in CANONICAL_AGENTS:
            require(agent in text, f"master prompt missing canonical agent: {agent}")
        require("cold WhatsApp" in text, "cold WhatsApp prohibition missing")
        require("mass LinkedIn" in text, "mass LinkedIn prohibition missing")
        require("quote == invoice" in text, "economic truth firewall missing")
        require("invoice == payment" in text, "payment truth firewall missing")
        require("merge == deployed" in text, "release truth firewall missing")
        digest = hashlib.sha256(prompt.read_bytes()).hexdigest()
        print("DEALIX_MASTER_PROMPT_BINDING_V1=PASS")
        print(f"MASTER_PROMPT_REF={prompt_ref}")
        print(f"MASTER_PROMPT_SHA256={digest}")
        print("PERMANENT_AGENTS=5")
        print("DEEP_WIP_MAX=3")
        print("L5_EXACT_ACTION_BOUND=true")
        print("SCHEDULER_CREATED=false")
        return 0
    except Exception as exc:  # noqa: BLE001 - one bounded verifier failure
        print(f"DEALIX_MASTER_PROMPT_BINDING_V1=FAIL reason={exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
