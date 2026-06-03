#!/usr/bin/env python3
"""Delivery gate: pipelines have owners + inputs, every system has acceptance criteria,
every client gets a weekly value report, delivery never starts without inputs."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import CheckResult, core_system_names, load_jsonl, main  # noqa: E402


def check() -> CheckResult:
    r = CheckResult("delivery_gate")
    pipelines = load_jsonl("data/delivery/pipelines.jsonl")
    weekly = load_jsonl("data/delivery/weekly_value_reports.jsonl")
    gates = load_jsonl("data/delivery/acceptance_gates.jsonl")
    if not pipelines:
        r.error("no delivery pipelines found")
        return r

    core_names = set(core_system_names().values())
    reported_clients = {w.get("client") for w in weekly}

    for p in pipelines:
        pid = p.get("pipeline_id", "<no-id>")
        if not p.get("owner"):
            r.error(f"pipeline {pid} has no owner")
        if not p.get("required_inputs"):
            r.error(f"pipeline {pid} has no required_inputs")
        # delivery must not be active without satisfied inputs
        if p.get("status") == "active" and not p.get("required_inputs_satisfied", False):
            r.error(f"pipeline {pid} is active but required_inputs_satisfied is false")
        if p.get("client") not in reported_clients:
            r.error(f"pipeline {pid} client '{p.get('client')}' has no weekly value report")

    # every core system must have an acceptance gate
    gated_systems = {g.get("system") for g in gates}
    missing = core_names - gated_systems
    if missing:
        r.error(f"systems without an acceptance gate: {missing}")
    for g in gates:
        if g.get("required") is not True:
            r.error(f"acceptance gate for {g.get('system')} must be required")
        if not g.get("criteria"):
            r.error(f"acceptance gate for {g.get('system')} has no criteria")

    r.note(f"{len(pipelines)} pipelines, {len(weekly)} weekly reports, {len(gates)} acceptance gates")
    return r


if __name__ == "__main__":
    main(check)
