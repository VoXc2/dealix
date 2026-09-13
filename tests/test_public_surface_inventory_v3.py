from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANDING = ROOT / "landing"
MANIFEST = json.loads((LANDING / "public-surface-manifest.json").read_text(encoding="utf-8"))

CANONICAL = set(MANIFEST["canonical_indexable"])
SUPPORTING = set(MANIFEST["reviewed_fail_closed_or_supporting"])
QUARANTINED = set(MANIFEST["quarantined_noncanonical"])
RETIRED = set(MANIFEST["retired_redirect"])


def test_every_top_level_html_is_explicitly_classified() -> None:
    actual = {path.name for path in LANDING.glob("*.html")}
    classified = CANONICAL | SUPPORTING | QUARANTINED | RETIRED
    assert actual == classified, {
        "unclassified": sorted(actual - classified),
        "missing_files": sorted(classified - actual),
    }


def test_route_classes_are_mutually_exclusive() -> None:
    buckets = {
        "canonical": CANONICAL,
        "supporting": SUPPORTING,
        "quarantined": QUARANTINED,
        "retired": RETIRED,
    }
    collisions: dict[str, list[str]] = {}
    names = list(buckets)
    for index, left in enumerate(names):
        for right in names[index + 1 :]:
            overlap = buckets[left] & buckets[right]
            if overlap:
                collisions[f"{left}:{right}"] = sorted(overlap)
    assert not collisions, collisions


def test_canonical_indexable_routes_are_not_retired_redirect_stubs() -> None:
    violations: dict[str, list[str]] = {}
    for name in sorted(CANONICAL):
        text = (LANDING / name).read_text(encoding="utf-8", errors="replace")
        lowered = text.lower()
        hits: list[str] = []
        if "noindex" in lowered:
            hits.append("noindex")
        if 'http-equiv="refresh"' in lowered or "http-equiv='refresh'" in lowered:
            hits.append("meta_refresh")
        if "dealix_retired_public_surface" in lowered:
            hits.append("retired_marker")
        if hits:
            violations[name] = hits
    assert not violations, violations


def test_quarantined_routes_are_not_promoted_and_are_robots_blocked() -> None:
    robots = (LANDING / "robots.txt").read_text(encoding="utf-8")
    sitemap_text = "\n".join(
        (LANDING / name).read_text(encoding="utf-8")
        for name in ("sitemap.xml", "sitemap_dealix.xml")
    )
    errors: dict[str, list[str]] = {}
    for name in sorted(QUARANTINED):
        problems: list[str] = []
        if f"Disallow: /{name}" not in robots:
            problems.append("not_robots_blocked")
        if f"https://dealix.me/{name}" in sitemap_text:
            problems.append("promoted_in_sitemap")
        if problems:
            errors[name] = problems
    assert not errors, errors


def test_quarantined_routes_do_not_gain_public_fixed_price_authority() -> None:
    fixed_price = re.compile(
        r"(?i)(?:499|999|1[\s,]?500|2[\s,]?500|2[\s,]?999|7[\s,]?500|7[\s,]?999|12[\s,]?000)\s*(?:SAR|ر\.?س|ريال)"
    )
    live_checkout = re.compile(
        r"(?i)(?:href|action)=[\"'][^\"']*(?:checkout|payment|pay-now)[^\"']*[\"']"
    )
    violations: dict[str, list[str]] = {}
    for name in sorted(QUARANTINED):
        text = (LANDING / name).read_text(encoding="utf-8", errors="replace")
        hits: list[str] = []
        if fixed_price.search(text):
            hits.append("fixed_price")
        if live_checkout.search(text):
            hits.append("live_checkout_link")
        if hits:
            violations[name] = hits
    assert not violations, violations


def test_canonical_public_surfaces_do_not_use_fixed_agent_count_as_authority() -> None:
    # Historical executor aliases/counts may remain in internal provenance, but a
    # public canonical page must not sell Dealix as a fixed five-agent product.
    fixed_agent_count = re.compile(
        r"(?i)(?:\b5\s+(?:AI\s+)?agents?\b|\bfive\s+(?:AI\s+)?agents?\b|5\s*وكلاء|خمسة\s+وكلاء|٥\s*وكلاء)"
    )
    violations: dict[str, list[str]] = {}
    for name in sorted(CANONICAL):
        text = (LANDING / name).read_text(encoding="utf-8", errors="replace")
        matches = sorted({match.group(0) for match in fixed_agent_count.finditer(text)})
        if matches:
            violations[name] = matches
    assert not violations, violations


def test_manifest_declares_current_agentic_public_authority() -> None:
    rules = MANIFEST["rules"]
    assert rules["public_fixed_agent_count_authority"] is False
    architecture = rules["canonical_agent_architecture"]
    assert "Sector Companies" in architecture
    assert "Arm Pods" in architecture
    assert "Specialist Logical Agents" in architecture
    assert "resource-governed runtime workers" in architecture


def test_manifest_declares_quarantine_non_authority() -> None:
    rules = MANIFEST["rules"]
    assert rules["every_top_level_html_must_be_classified"] is True
    assert rules["quarantined_noncanonical_is_current_marketing_authority"] is False
    assert rules["quarantined_noncanonical_must_be_disallowed_in_robots"] is True
    assert rules["quarantine_requires_route_specific_review_before_promotion"] is True
