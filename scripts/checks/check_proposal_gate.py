#!/usr/bin/env python3
"""Mini-proposal gate: every proposal has price + scope + inputs, approval required, never auto-sent."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import CheckResult, MINI_PROPOSAL_FIELDS, load_jsonl, main  # noqa: E402


def check() -> CheckResult:
    r = CheckResult("proposal_gate")
    proposals = load_jsonl("data/proposals/mini_proposals.jsonl")
    if not proposals:
        r.error("no mini proposals found")
        return r

    for i, p in enumerate(proposals):
        for f in MINI_PROPOSAL_FIELDS:
            if f not in p:
                r.error(f"proposal[{i}] missing field '{f}'")
        if not isinstance(p.get("price"), (int, float)) or p.get("price", 0) <= 0:
            r.error(f"proposal[{i}] price must be a positive number")
        if not p.get("scope"):
            r.error(f"proposal[{i}] missing scope")
        if not p.get("required_inputs"):
            r.error(f"proposal[{i}] missing required_inputs")
        if not p.get("acceptance_criteria"):
            r.error(f"proposal[{i}] missing acceptance_criteria")
        if p.get("approval_required") is not True:
            r.error(f"proposal[{i}] approval_required must be true")
        if p.get("status") == "sent":
            r.error(f"proposal[{i}] status 'sent' — proposals must not be auto-sent")
        if p.get("status") not in ("draft", "approved", "won", "lost"):
            r.error(f"proposal[{i}] invalid status '{p.get('status')}'")

    r.note(f"validated {len(proposals)} mini proposals — all require approval, none auto-sent")
    return r


if __name__ == "__main__":
    main(check)
