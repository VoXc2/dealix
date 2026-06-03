#!/usr/bin/env python3
"""
Dealix Check: Prompt Injection / Tool Poisoning Defense

External text is data, never instruction. Every known injection test string
must be blocked, tool calls must never be triggered by retrieved content,
no secrets in context, and write/send actions must require approval.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import Reporter, load_json  # noqa: E402

REQUIRED_DOCS = [
    "docs/security/PROMPT_INJECTION_DEFENSE_MAX_AR.md",
    "docs/security/UNTRUSTED_INPUT_SANDBOXING_AR.md",
    "docs/security/AGENT_AUDIT_LOG_POLICY_AR.md",
    "docs/security/TOOL_POISONING_DEFENSE_AR.md",
]


def run() -> bool:
    r = Reporter("DEALIX CHECK — PROMPT INJECTION DEFENSE")

    data = load_json("company_os/security/prompt_injection_tests.json")
    if data is None:
        r.fail("prompt_injection_tests.json missing or invalid")
        return r.render()

    r.check(len(data.get("defense_rules", [])) >= 5,
            "defense rules declared",
            "defense_rules incomplete (need the 7 core rules)")

    test_strings = data.get("test_strings", [])
    results = {res.get("string"): res for res in data.get("results", [])}
    r.check(len(test_strings) >= 1, f"{len(test_strings)} injection test strings defined",
            "no injection test strings defined")

    for s in test_strings:
        res = results.get(s)
        if res is None:
            r.fail(f"no defense result recorded for: '{s}'")
            continue
        r.check(res.get("blocked") is True,
                f"blocked injection: '{s}' ({res.get('action')})",
                f"injection NOT blocked: '{s}'")
        r.check(res.get("treated_as") == "data",
                f"treated as data: '{s}'",
                f"'{s}' not treated as data", warn_only=True)

    controls = data.get("controls", {})
    expected = {
        "external_content_is_data": True,
        "tool_calls_from_retrieved_content": False,
        "secrets_in_context": False,
        "all_actions_logged": True,
        "write_send_requires_approval": True,
        "quarantine_on_high_risk": True,
    }
    for key, want in expected.items():
        r.check(controls.get(key) is want,
                f"control {key} = {want}",
                f"control {key} must be {want}")

    r.require_files(REQUIRED_DOCS, label="security doc")
    return r.render()


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
