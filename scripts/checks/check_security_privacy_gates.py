#!/usr/bin/env python3
"""Security & Privacy Gate.

Enforces:
  - external content is documented as untrusted data (policy present)
  - account-pack evidence levels are constrained (no executed instructions)
  - the agent never auto-sends: every email draft + proposal is approval-gated
    and none are in a 'sent' state
  - contact discovery never invents contacts
  - no obvious secrets are committed under data/ reports/ docs/
"""
import re

import _bootstrap  # noqa: F401
from dealix.lib import ROOT, CheckResult, load_jsonl

ALLOWED_EVIDENCE = {"public", "founder_provided", "inferred"}
SECRET_PATTERNS = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key id"),
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"), "private key"),
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "secret API token"),
    (re.compile(r"(?i)(password|passwd|secret)\s*[:=]\s*['\"][^'\"]{6,}['\"]"), "inline credential"),
]


def main():
    r = CheckResult("security_privacy_gates")

    # 1) untrusted-data policy present
    sec = ROOT / "docs/security/EXTERNAL_CONTENT_UNTRUSTED_DATA_POLICY.md"
    if sec.exists() and "untrusted" in sec.read_text(encoding="utf-8").lower():
        r.ok("external-content untrusted-data policy present")
    else:
        r.fail("missing/incomplete untrusted-data policy")

    priv = ROOT / "docs/privacy/DO_NOT_CONTACT_AND_SUPPRESSION_POLICY_AR.md"
    r.ok("suppression/do-not-contact policy present") if priv.exists() else r.fail("missing suppression policy")

    # 2) evidence levels constrained
    packs = load_jsonl("data/account_intelligence/account_packs.jsonl")
    bad_ev = [p["company_name"] for p in packs if p.get("evidence_level") not in ALLOWED_EVIDENCE]
    r.fail(f"packs with disallowed evidence_level: {bad_ev[:3]}") if bad_ev else r.ok("all packs use constrained evidence levels")

    # 3) agent never auto-sends
    drafts = load_jsonl("data/outreach/email_drafts.jsonl")
    sent = [d for d in drafts if d.get("status") == "sent" or d.get("approval_required") is not True]
    r.fail(f"{len(sent)} email drafts are sent/not approval-gated") if sent else r.ok("no email is auto-sent; all approval-gated")
    proposals = load_jsonl("data/proposals/mini_proposals.jsonl")
    psent = [p for p in proposals if p.get("status") == "sent" or p.get("approval_required") is not True]
    r.fail(f"{len(psent)} proposals sent/not approval-gated") if psent else r.ok("no proposal is auto-sent; all approval-gated")

    # 4) no invented contacts
    contacts = load_jsonl("data/contacts/contact_discovery.jsonl")
    invented = [c["company_name"] for c in contacts if c.get("invented") is not False]
    r.fail(f"invented contacts present: {invented[:3]}") if invented else r.ok("contact discovery: zero invented contacts")

    # 5) secret scan
    hits = []
    for sub in ("data", "reports", "docs"):
        base = ROOT / sub
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".json", ".jsonl", ".yaml", ".yml", ".txt", ".csv"}:
                try:
                    text = path.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue
                for pat, label in SECRET_PATTERNS:
                    if pat.search(text):
                        hits.append(f"{path.relative_to(ROOT)}: {label}")
    if hits:
        for h in hits[:5]:
            r.fail(f"possible secret committed: {h}")
    else:
        r.ok("no obvious secrets committed under data/ reports/ docs/")

    return r.finish()


if __name__ == "__main__":
    main()
