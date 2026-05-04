"""Forbidden-marketing-claims sweep across the static landing site.

Rule: customer-visible HTML must not contain unapproved instances of:
  Arabic — نضمن، مضمون
  English — guaranteed, blast, scrape, scraping, cold {whatsapp|outreach|email|messaging}

This guardrail mirrors the YAML validator
(scripts/verify_service_readiness_matrix.py) but acts on the published
landing pages so the *page surface* never claims more than the
service registry can prove.

Existing occurrences that appear in negation/disclaimer contexts
("لا scraping", "no scraping", "لا cold blast") are explicitly
allowlisted per file with the reason. Any *new* file that picks up
one of these phrases — or any new phrase in an existing file beyond
its allowlist — fails the test.

Founder-review items are recorded as ``REVIEW_PENDING`` reasons so
they show up in audits.
"""
from __future__ import annotations

import re
from pathlib import Path

LANDING = Path(__file__).resolve().parents[1] / "landing"

FORBIDDEN_PATTERNS = [
    ("نضمن", re.compile(r"نضمن")),
    ("مضمون", re.compile(r"مضمون")),
    ("guaranteed", re.compile(r"\bguaranteed?\b", re.IGNORECASE)),
    ("blast", re.compile(r"\bblast\b", re.IGNORECASE)),
    ("scrape", re.compile(r"\bscrape\b", re.IGNORECASE)),
    ("scraping", re.compile(r"\bscraping\b", re.IGNORECASE)),
    ("cold", re.compile(r"\bcold\s+(whatsapp|outreach|email|messaging)\b", re.IGNORECASE)),
]

# Per-file allowlist. Each entry is the set of forbidden tokens that may
# appear in that file because they are used in a *negation* or
# *disclaimer* context. New phrases not on this list will fail the test.
#
# Reason codes:
#   NEGATION         — phrase appears as "لا/no/never <term>"; used to
#                      describe what we don't do.
#   REVIEW_PENDING   — phrase appears in a positive context (e.g. a
#                      money-back wording on roi.html) and needs founder
#                      approval to either keep, qualify, or rephrase.
#                      We allow it here for now to avoid a destructive
#                      unilateral copy change; it is tracked explicitly.
ALLOWLIST: dict[str, dict[str, str]] = {
    "founder.html": {
        # "11 compliance gates… لا cold blast WhatsApp أو LinkedIn scraping أبداً"
        "blast": "NEGATION",
        "scraping": "NEGATION",
    },
    "academy.html": {
        # 'Cold Email Pro — Saudi' appears as a certificate / course name.
        # The product policy is no cold outreach for Dealix itself; the
        # academy curriculum teaching that topic needs founder review.
        "cold": "REVIEW_PENDING",
    },
    "roi.html": {
        # "لا وعود مضمونة" — explicit negation in disclaimer.
        "مضمون": "NEGATION",
        # "لا نضمن مبالغ معينة — نضمن استرجاع 100%" — refund guarantee
        # wording. Founder must decide between rephrase or approval.
        "نضمن": "REVIEW_PENDING",
    },
    "trust.html": {
        "scraping": "NEGATION",
    },
    # status.html (the new console) describes blocked actions in safety
    # copy ("Dealix never initiates cold outreach…") — negation only.
    "status.html": {
        "cold": "NEGATION",
    },
    # Newly authored legal pages — each describes the boundary of what
    # Dealix never does (no cold outreach, no scraping, no guaranteed
    # revenue/ranking). All NEGATION context only.
    "privacy.html": {
        "scraping": "NEGATION",
    },
    "subprocessors.html": {
        "cold": "NEGATION",
        "scraping": "NEGATION",
    },
    "terms.html": {
        "مضمون": "NEGATION",
    },
}


def _scan(html: str) -> set[str]:
    hits: set[str] = set()
    for token, pattern in FORBIDDEN_PATTERNS:
        if pattern.search(html):
            hits.add(token)
    return hits


def test_no_unallowlisted_forbidden_claims():
    violations: list[str] = []
    for path in sorted(LANDING.glob("*.html")):
        html = path.read_text(encoding="utf-8")
        hits = _scan(html)
        if not hits:
            continue
        allowed = set(ALLOWLIST.get(path.name, {}).keys())
        unexpected = hits - allowed
        if unexpected:
            for u in sorted(unexpected):
                violations.append(f"{path.name}: forbidden token {u!r} not allowlisted")
    assert not violations, (
        "Forbidden marketing claims found on the landing site. Either "
        "rephrase the copy or — if the term appears in a negation/disclaimer "
        "context — add it to ALLOWLIST in tests/test_landing_forbidden_claims.py.\n"
        + "\n".join(violations)
    )


def test_allowlist_entries_actually_present():
    """Catch stale allowlist entries: if we whitelisted a token but the
    page no longer contains it, drop the entry to keep the perimeter tight.
    """
    stale: list[str] = []
    for fname, tokens in ALLOWLIST.items():
        path = LANDING / fname
        if not path.exists():
            stale.append(f"{fname}: file not found")
            continue
        html = path.read_text(encoding="utf-8")
        hits = _scan(html)
        for token in tokens.keys():
            if token not in hits:
                stale.append(f"{fname}: {token!r} allowlisted but no longer in page")
    assert not stale, "stale allowlist entries:\n" + "\n".join(stale)


def test_review_pending_items_have_a_reason():
    """REVIEW_PENDING entries surface here so they cannot be silently
    forgotten. Update the reason in ALLOWLIST when the founder decides.
    """
    review_pending: list[str] = []
    for fname, tokens in ALLOWLIST.items():
        for token, reason in tokens.items():
            if reason == "REVIEW_PENDING":
                review_pending.append(f"{fname}: {token!r}")
    # This is informational, not a failure. We assert the *count* so
    # that whenever a founder rephrases or formally approves a phrase,
    # they remember to update this number too.
    assert len(review_pending) == 2, (
        "REVIEW_PENDING list changed; expected 2 "
        "(roi.html: 'نضمن'; academy.html: 'cold'). "
        "Update this assertion after the founder approves or rephrases. "
        f"Current: {review_pending}"
    )
