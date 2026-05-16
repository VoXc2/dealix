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
    # Styleguide demo — feature card example reads
    # "تجارب أسبوعيّة محكومة، لا scraping، لا cold blast". Pure
    # NEGATION context, same pattern as founder.html.
    "styleguide.html": {
        "blast": "NEGATION",
        "scraping": "NEGATION",
    },
    # Homepage hero — Wave 5 rephrased anti-claims to pure Saudi Arabic
    # ("صفر تواصل بارد · صفر سحب بيانات · صفر إرسال حيّ بدون موافقتك").
    # Allowlist entries removed because the literal English forbidden
    # tokens are no longer present.
    # AI Operating Team positioning page — anti-claim banner explicitly
    # rejects "guaranteed-revenue" and lists every immutable hard gate
    # ("لا cold WhatsApp"، "لا scraping"). Pure NEGATION throughout.
    "ai-team.html": {
        "cold": "NEGATION",
        "guaranteed": "NEGATION",
        "scraping": "NEGATION",
        "مضمون": "NEGATION",
    },
    # Pilot signup page — "what we will NOT do" section enumerates
    # forbidden actions we explicitly reject. Pure NEGATION.
    "start.html": {
        "cold": "NEGATION",
        "scraping": "NEGATION",
    },
    # Diagnostic intake — "صفر cold outreach" promise. Pure NEGATION.
    "diagnostic.html": {
        "cold": "NEGATION",
    },
    # Founder leads inbox — footer states "لا cold outreach من النظام"
    # as a privacy promise. Pure NEGATION.
    "founder-leads.html": {
        "cold": "NEGATION",
    },
    # Pilot Day 0 customer kickoff — describes "صفر cold outreach، صفر
    # cold blast، صفر scraping" as part of the safety contract. Pure NEGATION.
    "pilot-day-0.html": {
        "blast": "NEGATION",
        "cold": "NEGATION",
        "scraping": "NEGATION",
    },
    # Compare page — describes competitor behavior ("Encourages cold
    # sequences", "Sales Engagement = cold") + Dealix's anti-cold/anti-
    # scraping stance. Pure NEGATION context.
    "compare.html": {
        "cold": "NEGATION",
        "scraping": "NEGATION",
    },
    # Real-estate diagnostic — "صفر cold WhatsApp · لا scraping" promise
    # to the broker. Pure NEGATION.
    "diagnostic-real-estate.html": {
        "cold": "NEGATION",
    },
    # Trust Center (Tier-1 redesign) — frames the 8 hard gates as features.
    # Copy explicitly states what Dealix DOES NOT do: "لا scraping",
    # "لا يبيع لك «نضمن نتائج»". Pure NEGATION throughout.
    "trust-center.html": {
        "scraping": "NEGATION",
        "نضمن": "NEGATION",
    },
    # Agency Partner page (Tier-1 redesign) — agency-facing positioning
    # repeats the safety promise: "بدون cold WhatsApp" so partners can
    # reassure their clients. Pure NEGATION.
    "agency-partner.html": {
        "cold": "NEGATION",
    },
    # Homepage (Tier-1 redesign) — hero subheadline and #for-who NOT-FOR
    # list explicitly state "بدون cold WhatsApp ولا scraping" as part of
    # the safety promise. Pure NEGATION throughout.
    "index.html": {
        "cold": "NEGATION",
        "scraping": "NEGATION",
    },
    # Comparison pages (Track D3) — describe competitor mechanics
    # ("blast model", "cold sequences") explicitly as anti-patterns
    # Dealix rejects. Pure NEGATION context throughout.
    "compare-hubspot.html": {
        "blast": "NEGATION",
    },
    "compare-salesloft.html": {
        "blast": "NEGATION",
        "cold": "NEGATION",
    },
    # Data Pack page — "السياسات · Policies" card explicitly states
    # "صفر cold WhatsApp / LinkedIn" and "لا scraping. لا إرسال آلي."
    # Pure NEGATION context (what Dealix does not do).
    "data-pack.html": {
        "cold": "NEGATION",
        "scraping": "NEGATION",
    },
    # Roadmap page — "الأشياء التي رفضنا بناؤها" (things we refused to
    # build) section lists "LinkedIn scraping automation — policy-blocked"
    # as a rejected anti-pattern. Pure NEGATION context.
    "roadmap.html": {
        "scraping": "NEGATION",
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
