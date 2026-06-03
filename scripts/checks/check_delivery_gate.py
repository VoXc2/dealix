#!/usr/bin/env python3
"""Delivery Readiness Gate: a pipeline must have a selected system, scope,
required inputs, success metric, acceptance criteria, and owner — and must NOT
advance past 'intake' until inputs_received is true."""
import _bootstrap  # noqa: F401
from dealix.lib import CheckResult, load_jsonl
from dealix import seeds

POST_INTAKE = {"build", "review", "handoff", "value_report", "closed"}


def main():
    r = CheckResult("delivery_gate")
    pipelines = load_jsonl("data/delivery/pipelines.jsonl")
    failures = 0
    for p in pipelines:
        problems = []
        if p.get("selected_system") not in seeds.CORE_SYSTEM_IDS:
            problems.append("no valid selected_system")
        if not p.get("scope"):
            problems.append("no scope")
        if len(p.get("required_inputs", [])) < 1:
            problems.append("no required_inputs")
        if not p.get("success_metric"):
            problems.append("no success_metric")
        if len(p.get("acceptance_criteria", [])) < 1:
            problems.append("no acceptance_criteria")
        if not p.get("owner"):
            problems.append("no owner")
        if p.get("stage") in POST_INTAKE and not p.get("inputs_received"):
            problems.append("delivery started before inputs_received")
        if problems:
            failures += 1
            if failures <= 5:
                r.fail(f"{p.get('client')}: " + ", ".join(problems))
    if failures:
        r.fail(f"{failures}/{len(pipelines)} pipelines failed the delivery gate")
    else:
        r.ok(f"all {len(pipelines)} pipelines pass the delivery gate (no delivery before inputs)")
    return r.finish()


if __name__ == "__main__":
    main()
