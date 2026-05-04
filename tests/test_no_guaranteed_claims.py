"""Phase D — extend the forbidden-claims sweep to *customer-facing*
documentation.

Scope rationale: ``docs/`` contains many internal playbooks, post-
mortems, and governance/safety catalogues that legitimately mention
the forbidden vocabulary while *describing what we don't do*. Trying
to allowlist every internal doc is brittle and adds no real safety.

This test scopes the sweep to documentation that is **customer-facing
or near-customer-facing**:

  - top-level ``docs/*.md`` files that are linked from the marketing
    site or shared with prospects, plus
  - everything under ``docs/sales-kit/`` (sales collateral).

Inside that scope:
  - A frozen allowlist pins ``REVIEW_PENDING`` items the founder
    must decide on (rephrase / qualify / approve).
  - New occurrences fail the test until either rephrased or added
    to the allowlist with an explicit reason.

Internal playbooks (``docs/ops/``, ``docs/business/``,
``docs/launch/``, etc.) are out of scope — they're audited by the
internal `test_landing_forbidden_claims.py` perimeter on the
website, not by this test.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOCS = REPO / "docs"

# Top-level customer-facing or near-customer-facing markdown.
CUSTOMER_FACING_TOP = {
    "pricing.md",
    "CUSTOMER_JOURNEYS.md",
    "ROI_PROOF_PACK.md",
    "OFFER_LADDER.md",
    "PUBLIC_LAUNCH_CHECKLIST.md",
}

# Subtrees scanned in full (every .md inside).
CUSTOMER_FACING_SUBTREES = {
    "sales-kit",
}

# Same vocabulary as scripts/verify_service_readiness_matrix.py.
FORBIDDEN_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("نضمن", re.compile(r"نضمن")),
    ("مضمون", re.compile(r"مضمون")),
    ("guaranteed", re.compile(r"\bguaranteed?\b", re.IGNORECASE)),
    ("blast", re.compile(r"\bblast\b", re.IGNORECASE)),
    ("scrape", re.compile(r"\bscrape\b", re.IGNORECASE)),
    ("scraping", re.compile(r"\bscraping\b", re.IGNORECASE)),
    ("cold", re.compile(r"\bcold\s+(whatsapp|outreach|email|messaging)\b", re.IGNORECASE)),
]

# Per-file allowlist with reason codes:
#   NEGATION       — "no/never/don't <term>" — describes what we don't do
#   REVIEW_PENDING — positive context; founder decision needed before
#                    rephrasing or approving
ALLOWLIST: dict[str, dict[str, str]] = {
    "sales-kit/README.md": {"cold": "NEGATION"},
    "sales-kit/MULTI_CHANNEL_OUTREACH_PACK.md": {"cold": "NEGATION"},
    "sales-kit/dealix_leads_50_expanded.md": {"cold": "NEGATION"},
    "sales-kit/dealix_marketing_full_playbook.md": {"cold": "NEGATION"},
    "sales-kit/dealix_referral_program.md": {
        "cold": "NEGATION",
        "مضمون": "REVIEW_PENDING",
    },
    "sales-kit/dealix_security_faq.md": {"guaranteed": "REVIEW_PENDING"},
    "sales-kit/dealix_demo_transcript_ar.md": {"نضمن": "REVIEW_PENDING"},
    "sales-kit/dealix_terms_of_service_ar.md": {"نضمن": "REVIEW_PENDING"},
}


def _scan(text: str) -> set[str]:
    return {tok for tok, pat in FORBIDDEN_PATTERNS if pat.search(text)}


def _files_in_scope() -> list[Path]:
    out: list[Path] = []
    for name in CUSTOMER_FACING_TOP:
        p = DOCS / name
        if p.exists():
            out.append(p)
    for subtree in CUSTOMER_FACING_SUBTREES:
        d = DOCS / subtree
        if d.is_dir():
            out.extend(sorted(d.rglob("*.md")))
    return sorted(out)


def _rel(p: Path) -> str:
    return str(p.relative_to(DOCS))


def test_no_unallowlisted_forbidden_claims_in_customer_facing_docs():
    violations: list[str] = []
    for path in _files_in_scope():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        hits = _scan(text)
        if not hits:
            continue
        rel = _rel(path)
        allowed = set(ALLOWLIST.get(rel, {}).keys())
        unexpected = hits - allowed
        for u in sorted(unexpected):
            violations.append(f"{rel}: forbidden token {u!r} not allowlisted")
    assert not violations, (
        "Forbidden claims found in customer-facing docs. Either "
        "rephrase the copy or — if it appears in a negation/disclaimer "
        "context — add to ALLOWLIST in tests/test_no_guaranteed_claims.py "
        "with reason=NEGATION. Use REVIEW_PENDING for items needing "
        "founder decision.\n"
        + "\n".join(violations)
    )


def test_allowlist_entries_actually_present_in_customer_facing_docs():
    """Stale entries are dropped to keep the perimeter tight."""
    stale: list[str] = []
    for fname, tokens in ALLOWLIST.items():
        path = DOCS / fname
        if not path.exists():
            stale.append(f"{fname}: file not found")
            continue
        try:
            hits = _scan(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, OSError):
            continue
        for token in tokens.keys():
            if token not in hits:
                stale.append(f"{fname}: {token!r} allowlisted but not in file")
    assert not stale, (
        "stale customer-facing-docs allowlist entries:\n" + "\n".join(stale)
    )


def test_review_pending_items_count_is_pinned():
    """Each REVIEW_PENDING item is a deliberate founder TODO.
    Pinning the count means founder approvals/rephrasings are
    visible in the diff."""
    pending: list[str] = []
    for fname, tokens in ALLOWLIST.items():
        for token, reason in tokens.items():
            if reason == "REVIEW_PENDING":
                pending.append(f"{fname}: {token!r}")
    # Update this number when the founder approves or rephrases an item.
    expected = 4
    assert len(pending) == expected, (
        f"REVIEW_PENDING list changed; expected {expected}, found "
        f"{len(pending)}. Update this assertion when the founder "
        f"resolves an item.\n"
        f"Currently pending:\n  " + "\n  ".join(pending)
    )
