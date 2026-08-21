#!/usr/bin/env python3
"""Fail-closed verifier for the Dealix company agent operating registry."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "dealix/registers/company_agent_operating_registry.json"
HERMES_REGISTRY = ROOT / "dealix/hermes/registry.py"

EXPECTED_RUNTIME_AGENTS = {
    "company_brain",
    "sprint_orchestrator",
    "governance",
    "market_intel",
    "lead_intelligence",
    "revenue_intelligence",
    "sales_intelligence",
    "customer_acquisition",
    "diagnostic_agent",
    "data_architect",
    "managed_ops",
}

FORBIDDEN_L5 = {
    "external_send",
    "external_publish",
    "merge_to_main",
    "production_mutation",
    "dns_mutation",
    "payment_or_refund",
    "secret_rotation_or_write",
    "data_deletion",
    "legal_commitment",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL company_agent_operating_registry: {message}")


def main() -> None:
    if not REGISTRY.is_file():
        fail(f"missing {REGISTRY.relative_to(ROOT)}")
    if not HERMES_REGISTRY.is_file():
        fail(f"missing {HERMES_REGISTRY.relative_to(ROOT)}")

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    agents = data.get("agents")
    if not isinstance(agents, list) or not agents:
        fail("agents must be a non-empty list")

    runtime_names = [a.get("runtime_name") for a in agents]
    if len(runtime_names) != len(set(runtime_names)):
        fail("duplicate runtime_name")
    if set(runtime_names) != EXPECTED_RUNTIME_AGENTS:
        missing = sorted(EXPECTED_RUNTIME_AGENTS - set(runtime_names))
        extra = sorted(set(runtime_names) - EXPECTED_RUNTIME_AGENTS)
        fail(f"Hermes agent mismatch missing={missing} extra={extra}")

    for agent in agents:
        for field in ("runtime_name", "class_name", "executive_role", "mission", "autonomy_ceiling"):
            if not agent.get(field):
                fail(f"agent missing required field {field}: {agent}")
        if agent["autonomy_ceiling"] not in {"L0", "L1", "L2", "L3", "L4"}:
            fail(f"invalid autonomy ceiling for {agent['runtime_name']}")

    # The production Hermes registry imports/constructs classes, while runtime
    # names come from each instance's agent.name. Verify against class names so
    # this gate follows the real registry implementation instead of string luck.
    hermes_source = HERMES_REGISTRY.read_text(encoding="utf-8")
    for agent in agents:
        class_name = agent["class_name"]
        if class_name not in hermes_source:
            fail(
                f"Hermes class {class_name!r} for runtime {agent['runtime_name']!r} "
                "not discoverable in dealix/hermes/registry.py"
            )

    authority = data.get("authority", {})
    if authority.get("external_send_enabled") is not False:
        fail("external_send_enabled must be false")
    if authority.get("production_mutation_enabled") is not False:
        fail("production_mutation_enabled must be false")
    if authority.get("merge_to_main_enabled") is not False:
        fail("merge_to_main_enabled must be false")
    if authority.get("payment_execution_enabled") is not False:
        fail("payment_execution_enabled must be false")

    required_approval = set(authority.get("founder_approval_actions", []))
    if not FORBIDDEN_L5.issubset(required_approval):
        fail(f"missing L5 approval actions: {sorted(FORBIDDEN_L5 - required_approval)}")

    canonical = data.get("canonical_systems", {})
    for key in ("company_context", "opportunities", "actions", "approvals", "proof", "learning"):
        value = str(canonical.get(key, ""))
        if not value.startswith("Dealix"):
            fail(f"canonical system {key!r} must remain owned by Dealix")

    openclaw = data.get("openclaw", {})
    blocked = set(openclaw.get("blocked", []))
    for action in (
        "arbitrary_shell",
        "production_mutation",
        "merge_to_main",
        "payments",
        "secret_access",
        "automatic_external_send",
    ):
        if action not in blocked:
            fail(f"OpenClaw missing block for {action}")
    if openclaw.get("ordinary_prose_is_not_l5_approval") is not True:
        fail("ordinary prose must not count as L5 approval")

    council = data.get("agent_council", {})
    if council.get("external_actions_executed") != 0:
        fail("Agent Council must execute zero external actions")

    proof = data.get("proof_contract", {})
    if proof.get("synthetic_is_commercial_proof") is not False:
        fail("synthetic evidence must not count as commercial proof")
    if proof.get("revenue_requires_payment_evidence") is not True:
        fail("revenue must require payment evidence")
    if proof.get("delivery_requires_delivery_evidence") is not True:
        fail("delivery must require delivery evidence")

    print(
        "PASS company_agent_operating_registry "
        f"agents={len(agents)} workstreams={len(data.get('department_workstreams', []))}"
    )


if __name__ == "__main__":
    main()
