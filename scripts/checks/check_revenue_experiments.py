#!/usr/bin/env python3
"""
Dealix Check: Revenue Experimentation

Enforces the core rule: each experiment changes exactly one variable.
Validates that every experiment has the required fields and that
send-bearing experiments require approval.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import Reporter, load_json  # noqa: E402

REQUIRED_FIELDS = ["id", "type", "hypothesis", "variable",
                   "variables_changed", "metric", "status", "owner"]

REQUIRED_DOCS = [
    "docs/experiments/REVENUE_EXPERIMENTATION_SYSTEM_AR.md",
    "docs/experiments/EMAIL_ANGLE_TESTING_AR.md",
    "docs/experiments/SECTOR_TESTING_MATRIX_AR.md",
    "docs/experiments/OFFER_TESTING_POLICY_AR.md",
]


def run() -> bool:
    r = Reporter("DEALIX CHECK — REVENUE EXPERIMENTATION")

    data = load_json("company_os/experiments/experiments.json")
    if data is None:
        r.fail("experiments.json missing or invalid")
        return r.render()

    experiments = data.get("experiments", [])
    r.check(len(experiments) >= 1, f"{len(experiments)} experiments registered",
            "no experiments registered")

    for e in experiments:
        eid = e.get("id", "<unknown>")
        missing = [f for f in REQUIRED_FIELDS if f not in e]
        r.check(not missing, f"{eid}: required fields present",
                f"{eid}: missing fields {missing}")

        changed = e.get("variables_changed", [])
        r.check(len(changed) == 1,
                f"{eid}: changes exactly one variable ({changed})",
                f"{eid}: must change exactly one variable, got {changed}")

        r.check(e.get("requires_approval_for_send") is True,
                f"{eid}: send requires approval",
                f"{eid}: send must require approval", warn_only=True)

    r.require_files(REQUIRED_DOCS, label="experiment doc")
    return r.render()


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
