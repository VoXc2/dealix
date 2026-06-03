#!/usr/bin/env python3
"""Email Quality Gate.

Fails a draft if it: lacks a need-card ref / core system / sector sprint / CTA,
contains a guaranteed claim, uses a fake Re:/Fwd: subject, states pain as fact
(no question/hedge), targets a suppressed company, or is not approval-gated.
"""
import _bootstrap  # noqa: F401
from dealix.lib import CheckResult, load_jsonl
from dealix import seeds

GUARANTEE_TERMS = ["نضمن", "مضمون", "ضمان كامل", "نعدك", "guarantee", "guaranteed", "100%", "نضاعف أرباحك"]
FAKE_PREFIXES = ("re:", "re :", "fwd:", "fw:", "رد:", "إعادة توجيه:")


def main():
    r = CheckResult("email_quality_gate")
    drafts = load_jsonl("data/outreach/email_drafts.jsonl")
    packs = load_jsonl("data/account_intelligence/account_packs.jsonl")
    domain_by_name = {p["company_name"]: p.get("domain", "") for p in packs}
    suppressed = {row["domain"].lower() for row in load_jsonl("data/suppression/do_not_contact.jsonl")}

    failures = 0
    for d in drafts:
        subj = (d.get("subject") or "").strip()
        body = d.get("body") or ""
        text = subj + " " + body
        problems = []
        if not d.get("client_need_card_ref"):
            problems.append("no client_need_card_ref")
        if d.get("core_system") not in seeds.CORE_SYSTEM_IDS:
            problems.append("no valid core_system")
        if not d.get("sector_specific_sprint"):
            problems.append("no sector_specific_sprint")
        if not d.get("cta"):
            problems.append("no CTA")
        if d.get("approval_required") is not True:
            problems.append("approval_required must be true")
        if any(t.lower() in text.lower() for t in GUARANTEE_TERMS):
            problems.append("guaranteed claim")
        if subj.lower().startswith(FAKE_PREFIXES):
            problems.append("fake Re/Fwd subject")
        if "؟" not in body:
            problems.append("pain stated as fact (no question/hedge)")
        if domain_by_name.get(d.get("company_name", ""), "").lower() in suppressed:
            problems.append("company in suppression list")
        if problems:
            failures += 1
            if failures <= 5:
                r.fail(f"{d.get('company_name')}: " + ", ".join(problems))

    if failures:
        r.fail(f"{failures}/{len(drafts)} drafts failed the email gate")
    else:
        r.ok(f"all {len(drafts)} email drafts pass the gate (approval-gated, no guarantees, no spoofed subjects)")
    return r.finish()


if __name__ == "__main__":
    main()
