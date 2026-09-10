import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANDING = ROOT / "landing"
MANIFEST = json.loads((LANDING / "public-surface-manifest.json").read_text(encoding="utf-8"))

CANONICAL = set(MANIFEST["canonical_indexable"])
SUPPORTING = set(MANIFEST["reviewed_fail_closed_or_supporting"])
MACHINE = set(MANIFEST.get("canonical_machine_assets", []))
RETIRED = dict(MANIFEST["retired_redirect"])

FIXED_PRICE_PATTERNS = [
    re.compile(r"(?i)(?:499|999|1[\s,]?500|2[\s,]?500|2[\s,]?999|7[\s,]?500|7[\s,]?999|12[\s,]?000)\s*(?:SAR|ر\.?س|ريال)"),
    re.compile(r"(?i)\$\s*299\b"),
]
OVERCLAIM_PATTERNS = [
    re.compile(r"47\+"), re.compile(r"12\s*شهادة"),
    re.compile(r"شهاد(?:ة|ات)\s+معتمدة"), re.compile(r"(?i)\b(?:certified|accredited)\b"),
    re.compile(r"(?i)Saudi data residency"), re.compile(r"كل\s+البيانات\s+في\s+KSA", re.I),
    re.compile(r"(?i)\bSLA\s*99(?:\.\d+)?%"), re.compile(r"(?i)price[- ]?lock"),
    re.compile(r"(?i)(?:100%|75%)\s*(?:refund|استرجاع)"),
    re.compile(r"(?i)guaranteed\s+(?:revenue|ROI|result)"),
    re.compile(r"(?i)\btestimonial(?:s)?\b"), re.compile(r"(?i)\bKPI\s+lift\b"),
    re.compile(r"(?i)\b(?:\d{2,}|\d+\+)\s+(?:customers?|clients?)\b"),
    re.compile(r"(?:\d{2,}|\d+\+)\s*(?:عميل|عملاء)"),
]
LIVE_CHECKOUT_PATTERNS = [
    re.compile(r"(?i)<a\b[^>]*href=[\"'][^\"']*(?:checkout|payment|pay-now)[^\"']*[\"']"),
    re.compile(r"(?i)action=[\"'][^\"']*(?:checkout|payment|pay-now)[^\"']*[\"']"),
    re.compile(r"(?i)\b(?:buy now|pay now|start checkout)\b"),
    re.compile(r"(?:ادفع الآن|اشتر الآن|ابدأ الدفع)"),
]
EVIDENCE_LANGUAGE_PAGES = {"proof.html", "trust-center.html", "llms.txt"}


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _hits(text: str, patterns: list[re.Pattern[str]]) -> list[str]:
    return [p.pattern for p in patterns if p.search(text)]


def test_manifest_paths_exist() -> None:
    for name in CANONICAL | SUPPORTING | MACHINE | set(RETIRED):
        assert (LANDING / name).is_file(), f"manifest path missing: landing/{name}"


def test_canonical_pages_have_no_fixed_public_prices_or_live_checkout() -> None:
    violations: dict[str, list[str]] = {}
    for name in sorted(CANONICAL | SUPPORTING):
        path = LANDING / name
        if path.suffix not in {".html", ".txt"}:
            continue
        hits = _hits(_text(path), FIXED_PRICE_PATTERNS + LIVE_CHECKOUT_PATTERNS)
        if hits:
            violations[name] = hits
    assert not violations, f"public commercial drift: {violations}"


def test_public_machine_catalog_is_only_canonical_path() -> None:
    path = LANDING / "assets/data/services-catalog.json"
    data = json.loads(_text(path))
    ids = [item["id"] for item in data["offerings"]]
    assert ids == ["free_mini_diagnostic", "revenue_command_pilot_30d"]
    assert data["offerings"][0]["pricing"] == "free"
    pilot = data["offerings"][1]
    assert pilot["pricing"] == "customer_specific_quote_after_qualified_discovery"
    assert pilot["public_checkout"] is False
    assert pilot["customer_result_guarantee"] is False
    raw = _text(path)
    assert "price_sar" not in raw
    assert not _hits(raw, FIXED_PRICE_PATTERNS + OVERCLAIM_PATTERNS + LIVE_CHECKOUT_PATTERNS)


def test_retired_surfaces_are_fail_closed_redirect_stubs() -> None:
    violations: dict[str, list[str]] = {}
    for name, target in RETIRED.items():
        text = _text(LANDING / name)
        problems: list[str] = []
        if "DEALIX_RETIRED_PUBLIC_SURFACE" not in text:
            problems.append("missing retired marker")
        if "noindex,nofollow" not in text.replace(" ", "").lower():
            problems.append("missing noindex,nofollow")
        if f"url={target}" not in text:
            problems.append(f"missing redirect target {target}")
        if _hits(text, FIXED_PRICE_PATTERNS + OVERCLAIM_PATTERNS + LIVE_CHECKOUT_PATTERNS):
            problems.append("contains retired commercial/proof claim")
        if len(text) > 4000:
            problems.append("stub unexpectedly large")
        if problems:
            violations[name] = problems
    assert not violations, f"retired public surfaces not fail-closed: {violations}"


def test_all_unclassified_deployable_html_fails_closed_on_high_risk_claims() -> None:
    classified = CANONICAL | SUPPORTING | set(RETIRED)
    violations: dict[str, list[str]] = {}
    for path in sorted(LANDING.rglob("*.html")):
        rel = path.relative_to(LANDING).as_posix()
        if rel in classified:
            continue
        hits = _hits(_text(path), FIXED_PRICE_PATTERNS + OVERCLAIM_PATTERNS + LIVE_CHECKOUT_PATTERNS)
        if hits:
            violations[rel] = hits
    assert not violations, (
        "unclassified deployable HTML contains commercial-risk claims; classify or retire: "
        + repr(violations)
    )


def test_unclassified_json_cannot_publish_fixed_price_or_overclaim() -> None:
    violations: dict[str, list[str]] = {}
    for path in sorted(LANDING.rglob("*.json")):
        rel = path.relative_to(LANDING).as_posix()
        if rel in MACHINE:
            continue
        hits = _hits(_text(path), FIXED_PRICE_PATTERNS + OVERCLAIM_PATTERNS + LIVE_CHECKOUT_PATTERNS)
        if hits:
            violations[rel] = hits
    assert not violations, "unclassified deployable JSON drift: " + repr(violations)


def test_reviewed_non_evidence_pages_have_no_high_confidence_overclaims() -> None:
    violations: dict[str, list[str]] = {}
    for name in sorted((CANONICAL | SUPPORTING) - EVIDENCE_LANGUAGE_PAGES):
        path = LANDING / name
        if path.suffix not in {".html", ".txt"}:
            continue
        hits = _hits(_text(path), OVERCLAIM_PATTERNS)
        if hits:
            violations[name] = hits
    assert not violations, f"reviewed public overclaim drift: {violations}"


def _sitemap_paths(name: str) -> set[str]:
    actual = set(re.findall(r"<loc>https://dealix\.me/(.*?)</loc>", _text(LANDING / name)))
    return {"index.html" if item == "" else item for item in actual}


def test_both_sitemaps_only_promote_canonical_indexable_surfaces() -> None:
    for name in ("sitemap.xml", "sitemap_dealix.xml"):
        assert _sitemap_paths(name) == CANONICAL


def test_robots_blocks_every_retired_surface() -> None:
    robots = _text(LANDING / "robots.txt")
    missing = [name for name in sorted(RETIRED) if f"Disallow: /{name}" not in robots]
    assert not missing, f"robots.txt missing retired surfaces: {missing}"
