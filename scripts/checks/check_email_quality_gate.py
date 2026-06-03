#!/usr/bin/env python3
"""Email quality gate: one system per draft, evidence present, no guaranteed claims."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (  # noqa: E402
    CheckResult, EMAIL_DRAFT_FIELDS, FAKE_THREAD_PREFIXES, GUARANTEE_BANNED,
    VALID_EVIDENCE_LEVELS, core_system_names, find_banned, load_jsonl, main, rel,
)


def check() -> CheckResult:
    r = CheckResult("email_quality_gate")
    drafts = load_jsonl("data/outreach/email_drafts.jsonl")
    if not drafts:
        r.error("no email drafts found")
        return r

    valid_systems = set(core_system_names().values())
    for i, d in enumerate(drafts):
        for f in EMAIL_DRAFT_FIELDS:
            if f not in d:
                r.error(f"draft[{i}] missing field '{f}'")
        system = d.get("system")
        if not isinstance(system, str) or system not in valid_systems:
            r.error(f"draft[{i}] system '{system}' is not exactly one of the 5 core systems")
        if d.get("evidence_level") not in VALID_EVIDENCE_LEVELS:
            r.error(f"draft[{i}] missing/invalid evidence_level")
        if d.get("approval_required") is not True:
            r.error(f"draft[{i}] approval_required must be true (no auto-send)")
        subject = (d.get("subject") or "").strip().lower()
        for pre in FAKE_THREAD_PREFIXES:
            if subject.startswith(pre):
                r.error(f"draft[{i}] subject uses fake thread prefix '{pre}'")
        banned = find_banned(d.get("subject", ""), GUARANTEE_BANNED) + \
            find_banned(d.get("body", ""), GUARANTEE_BANNED)
        if banned:
            r.error(f"draft[{i}] contains guaranteed-claim phrases: {banned}")

    # 400/day contract documented + Top 100 queue present and bounded
    if not rel("docs/outreach/DAILY_400_SYSTEM_DRAFT_FACTORY_AR.md").exists():
        r.error("missing 400/day draft factory contract doc")
    queue = load_jsonl("data/outreach/top_100_approval_queue.jsonl")
    r.require(0 < len(queue) <= 100, f"top-100 queue must have 1..100 rows, got {len(queue)}")
    draft_ids = {d.get("draft_id") for d in drafts}
    if not all(q.get("draft_id") in draft_ids for q in queue):
        r.error("top-100 queue contains drafts not present in the draft set")

    r.note(f"validated {len(drafts)} drafts and a top-{len(queue)} approval queue")
    return r


if __name__ == "__main__":
    main(check)
