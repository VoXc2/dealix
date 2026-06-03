#!/usr/bin/env python3
"""
Dealix Check: Agent Governance

Validates the agent registry against the workflow-first policy:
every agent must define a workflow, input contract, output contract,
permission level, quality gate, audit log, owner, and stop rule.
Also validates autonomy levels and that governance docs exist.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import Reporter, load_json  # noqa: E402

VALID_LEVELS = {"L1", "L2", "L3", "L4", "L5"}

REQUIRED_DOCS = [
    "docs/agents/AGENT_REGISTRY_AR.md",
    "docs/agents/AGENT_PERMISSION_MATRIX_AR.md",
    "docs/agents/AGENT_RUNBOOKS_AR.md",
    "docs/agents/WORKFLOW_FIRST_AGENT_POLICY_AR.md",
    "docs/scale/AGENT_AUTONOMY_LEVELS_AR.md",
]


def run() -> bool:
    r = Reporter("DEALIX CHECK — AGENT GOVERNANCE")

    data = load_json("company_os/agents/agent_registry.json")
    if data is None:
        r.fail("agent_registry.json missing or invalid")
        return r.render()

    required_fields = data.get("required_fields", [])
    r.check(len(required_fields) == 8,
            f"workflow-first contract defines {len(required_fields)} required fields",
            "required_fields must list the 8 workflow-first fields")

    r.check(len(data.get("hard_rules", [])) >= 4,
            "hard rules declared (generate/recommend/prepare/no external action)",
            "hard_rules missing from registry")

    agents = data.get("agents", [])
    r.check(len(agents) >= 1, f"{len(agents)} agents registered",
            "no agents registered")

    for a in agents:
        name = a.get("name", a.get("id", "<unknown>"))

        # Every workflow-first field must be present and truthy
        # (audit_log must be True, owner/workflow/etc. non-empty strings).
        missing = [f for f in required_fields if not a.get(f)]
        r.check(not missing,
                f"{name}: workflow-first contract complete",
                f"{name}: missing fields {missing}")

        r.check(a.get("level") in VALID_LEVELS,
                f"{name}: valid autonomy level {a.get('level')}",
                f"{name}: invalid autonomy level {a.get('level')}")

        r.check(a.get("audit_log") is True,
                f"{name}: audit logging enabled",
                f"{name}: audit logging NOT enabled")

    r.require_files(REQUIRED_DOCS, label="governance doc")
    return r.render()


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
