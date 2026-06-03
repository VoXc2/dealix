#!/usr/bin/env python3
"""Mini Proposal Gate: price, deliverables, timeline, inputs, closed scope,
approval required, and no guaranteed claims."""
import _bootstrap  # noqa: F401
from dealix.lib import CheckResult, load_jsonl

GUARANTEE_TERMS = ["نضمن", "مضمون", "ضمان كامل", "نعدك", "guarantee", "guaranteed", "100%"]


def main():
    r = CheckResult("proposal_gate")
    proposals = load_jsonl("data/proposals/mini_proposals.jsonl")
    failures = 0
    for p in proposals:
        problems = []
        if not p.get("starter_price_sar") or p["starter_price_sar"] <= 0:
            problems.append("no starter_price")
        if len(p.get("deliverables", [])) < 2:
            problems.append("needs >= 2 deliverables")
        if not p.get("timeline_days") or p["timeline_days"] <= 0:
            problems.append("no timeline")
        if len(p.get("required_inputs", [])) < 1:
            problems.append("no required_inputs")
        if p.get("open_scope") is not False:
            problems.append("scope must be closed (open_scope=false)")
        if p.get("approval_required") is not True:
            problems.append("approval_required must be true")
        text = " ".join([p.get("title", "")] + p.get("deliverables", []))
        if any(t.lower() in text.lower() for t in GUARANTEE_TERMS):
            problems.append("guaranteed claim")
        if problems:
            failures += 1
            if failures <= 5:
                r.fail(f"{p.get('company_name')}: " + ", ".join(problems))
    if failures:
        r.fail(f"{failures}/{len(proposals)} proposals failed the gate")
    else:
        r.ok(f"all {len(proposals)} mini proposals pass the gate (priced, scoped, approval-gated)")
    return r.finish()


if __name__ == "__main__":
    main()
