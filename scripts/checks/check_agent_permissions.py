#!/usr/bin/env python3
"""
Dealix Check: Agent Permissions (safety red-lines)

Enforces the hard rule: agents may NOT externally send, call, change price,
contract, or start delivery without founder approval. L5 agents must be
internal-only. Draft-producing agents (L3/L4) must require approval.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import Reporter, load_json  # noqa: E402

# Capabilities that no agent may hold autonomously.
RED_LINE_CAPS = [
    "can_send_external",
    "can_call",
    "can_change_price",
    "can_contract",
    "can_start_delivery",
]


def run() -> bool:
    r = Reporter("DEALIX CHECK — AGENT PERMISSIONS (RED LINES)")

    data = load_json("company_os/agents/agent_registry.json")
    if data is None:
        r.fail("agent_registry.json missing or invalid")
        return r.render()

    agents = data.get("agents", [])
    for a in agents:
        name = a.get("name", a.get("id", "<unknown>"))

        for cap in RED_LINE_CAPS:
            r.check(a.get(cap) is not True,
                    f"{name}: {cap} = false",
                    f"{name}: RED LINE — {cap} is enabled for an agent")

        if a.get("level") == "L5":
            r.check(a.get("internal_only") is True,
                    f"{name}: L5 agent is internal-only",
                    f"{name}: L5 agent must be internal_only")

        # L3/L4 agents prepare things that get sent/acted on -> need approval.
        if a.get("level") in ("L3", "L4"):
            r.check(a.get("requires_approval") is True,
                    f"{name}: requires explicit approval before action",
                    f"{name}: L3/L4 agent must require approval")

    r.require_files(["docs/agents/AGENT_PERMISSION_MATRIX_AR.md",
                     "reports/agents/AGENT_PERMISSION_AUDIT.md"],
                    label="permission doc")
    return r.render()


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
