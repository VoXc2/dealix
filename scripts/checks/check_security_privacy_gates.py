#!/usr/bin/env python3
"""Security + privacy gates: required policies exist, suppression list honored,
no invented contacts anywhere in the prospect data."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import CheckResult, load_jsonl, main, rel  # noqa: E402

REQUIRED_SECURITY_DOCS = [
    "docs/security/EXTERNAL_CONTENT_UNTRUSTED_DATA_POLICY.md",
    "docs/security/AGENT_PROMPT_INJECTION_GATE.md",
    "docs/security/TOOL_EXECUTION_ALLOWLIST_POLICY.md",
    "docs/security/AGENT_TOOL_USE_BOUNDARIES.md",
]
REQUIRED_PRIVACY_DOCS = [
    "docs/privacy/PROSPECT_DATA_MINIMIZATION_AR.md",
    "docs/privacy/DO_NOT_CONTACT_AND_SUPPRESSION_POLICY_AR.md",
    "docs/privacy/CLIENT_DATA_HANDLING_AR.md",
    "docs/privacy/SECRET_HANDLING_POLICY_AR.md",
]


def check() -> CheckResult:
    r = CheckResult("security_privacy_gates")
    for doc in REQUIRED_SECURITY_DOCS + REQUIRED_PRIVACY_DOCS:
        if not rel(doc).exists():
            r.error(f"missing policy doc: {doc}")

    # external-content policy must actually frame external data as untrusted
    ext = rel("docs/security/EXTERNAL_CONTENT_UNTRUSTED_DATA_POLICY.md")
    if ext.exists():
        text = ext.read_text(encoding="utf-8")
        if "غير موثوق" not in text and "untrusted" not in text.lower():
            r.error("external-content policy does not frame external data as untrusted")

    # suppression list present and well-formed
    sup = load_jsonl("data/suppression/do_not_contact.jsonl")
    r.require(len(sup) > 0, "do_not_contact suppression list is empty")
    suppressed = set()
    for row in sup:
        if not row.get("domain") or not row.get("reason"):
            r.error("suppression row missing domain/reason")
        suppressed.add(row.get("domain"))

    # no invented contacts: discovery + targets must declare invented=False and a source
    discovery = load_jsonl("data/contacts/contact_discovery.jsonl")
    channels = load_jsonl("data/contacts/contact_channels.jsonl")
    targets = load_jsonl("data/acquisition/contact_targets.jsonl")
    for d in discovery:
        if d.get("invented") is not False or not d.get("source"):
            r.error(f"discovery for {d.get('company_name')} not sourced / invented flag wrong")
    for c in channels:
        # sample channels must not fabricate a value
        if c.get("record_type") == "sample" and c.get("value") not in (None, ""):
            r.error(f"channel for {c.get('company_name')} fabricates a contact value")
        if not c.get("source"):
            r.error(f"channel for {c.get('company_name')} has no source")
    for t in targets:
        if t.get("invented") is not False or not t.get("source"):
            r.error(f"contact target for {t.get('company_name')} not sourced")

    # suppression honored: no suppressed domain appears as an outreach target
    drafts = load_jsonl("data/outreach/email_drafts.jsonl")
    refs = {d.get("account_ref", "") for d in drafts}
    for dom in suppressed:
        if any(dom and dom in ref for ref in refs):
            r.error(f"suppressed domain {dom} appears in outreach targets")

    r.note(f"{len(REQUIRED_SECURITY_DOCS)} security + {len(REQUIRED_PRIVACY_DOCS)} privacy docs, "
           f"{len(sup)} suppression entries, {len(discovery)} sourced discovery rows")
    return r


if __name__ == "__main__":
    main(check)
