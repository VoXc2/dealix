#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

BLOCKED_INTERNAL = ["/control-plane", "/agents", "/approvals", "/sandbox", "/self-evolving"]
REQUIRED_PUBLIC = ["/pricing", "/services", "/cases", "/book", "/safety"]
LEGACY_REDIRECTS = ["/pricing.html", "/academy.html", "/checkout.html"]
RETIRED_PUBLIC_MARKERS = [
    "تشخيص مدفوع",
    "خلال أسبوع واحد",
    "AI يكتب، أنت ترسل",
]


def verify(root: Path) -> list[str]:
    failures: list[str] = []
    sitemap = (root / "apps/web/app/sitemap.ts").read_text(encoding="utf-8")
    robots = (root / "apps/web/app/robots.ts").read_text(encoding="utf-8")
    layout = (root / "apps/web/app/layout.tsx").read_text(encoding="utf-8")
    pricing = (root / "apps/web/app/pricing/page.tsx").read_text(encoding="utf-8")
    next_config = (root / "apps/web/next.config.js").read_text(encoding="utf-8")
    legacy_pricing = (root / "landing/pricing.html").read_text(encoding="utf-8")
    academy = (root / "landing/academy.html").read_text(encoding="utf-8")

    for path in BLOCKED_INTERNAL:
        if path not in robots:
            failures.append(f"ROBOTS_MISSING_BLOCK:{path}")
        if f'path: "{path}"' in sitemap:
            failures.append(f"SITEMAP_ADVERTISES_INTERNAL:{path}")

    for path in REQUIRED_PUBLIC:
        if f'path: "{path}"' not in sitemap:
            failures.append(f"SITEMAP_MISSING_PUBLIC:{path}")

    if "alternates: { languages:" in sitemap or "languages:" in layout:
        failures.append("REDIRECTING_HREFLANG_ADVERTISED")
    if "alternateLocale" in layout:
        failures.append("UNSERVED_ALTERNATE_LOCALE_ADVERTISED")

    if "Dealix — AI Business Operating System" not in layout:
        failures.append("CANONICAL_POSITIONING_MISSING")
    for marker in RETIRED_PUBLIC_MARKERS:
        if marker in layout:
            failures.append(f"RETIRED_METADATA:{marker}")

    required_pricing_markers = [
        "Execution Diagnostic",
        "Customer-Specific Quote",
        "Outcome Sprint",
        "لا سعر عام",
        "Quote ليست Invoice",
    ]
    for marker in required_pricing_markers:
        if marker not in pricing:
            failures.append(f"PRICING_TRUTH_MISSING:{marker}")

    for legacy in LEGACY_REDIRECTS:
        if f'source: "{legacy}"' not in next_config:
            failures.append(f"LEGACY_REDIRECT_MISSING:{legacy}")

    if "لا يوجد سعر عام أو Checkout ذاتي" not in legacy_pricing:
        failures.append("LEGACY_PRICING_NOT_QUOTE_ONLY")
    if "noindex,nofollow" not in academy or "url=/pricing.html" not in academy:
        failures.append("LEGACY_ACADEMY_NOT_RETIRED")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=str(Path(__file__).resolve().parents[2]))
    args = parser.parse_args()
    root = Path(args.repo)
    failures = verify(root)
    if failures:
        print("DEALIX_PUBLIC_TRUTH_SEO_VERIFY=FAIL")
        for failure in failures:
            print(f"FAIL:{failure}")
        return 2
    print("DEALIX_PUBLIC_TRUTH_SEO_VERIFY=PASS")
    print("POSITIONING=AI_BUSINESS_OPERATING_SYSTEM")
    print("PUBLIC_PRICING=QUOTE_ONLY_CUSTOMER_SPECIFIC")
    print("SITEMAP_ROBOTS=CONSISTENT")
    print("LEGACY_HTML=REDIRECTED_OR_NOINDEX")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
