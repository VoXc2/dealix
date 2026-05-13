#!/usr/bin/env python3
"""Verify catalog ↔ service-folder coherence.

سكربت التحقق من تطابق كاتالوج الخدمات مع مجلدات docs/services/.

Usage:
    python scripts/verify_service_catalog.py

For every offering named in the canonical catalog (docs/company/SERVICE_CATALOG.md
when present, otherwise docs/strategy/service_portfolio_catalog.md), confirm
that a matching folder exists under `docs/services/`. We require at minimum
the 3 starting offers + 2 expansion offers. Exits 0 on PASS, non-zero on FAIL.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SERVICES_ROOT = REPO / "docs" / "services"

PRIMARY_CATALOG = REPO / "docs" / "company" / "SERVICE_CATALOG.md"
FALLBACK_CATALOG = REPO / "docs" / "strategy" / "service_portfolio_catalog.md"

# At minimum these 5 must have folders.
REQUIRED_OFFERS: tuple[str, ...] = (
    "lead_intelligence_sprint",
    "ai_quick_win_sprint",
    "company_brain_sprint",
    "ai_support_desk_sprint",
    "ai_governance_program",
)

# Catalog text → expected folder slug. Lower-cased substring match.
NAME_TO_SLUG: dict[str, str] = {
    "lead intelligence sprint": "lead_intelligence_sprint",
    "revenue intelligence sprint": "lead_intelligence_sprint",
    "ai quick win sprint": "ai_quick_win_sprint",
    "company brain sprint": "company_brain_sprint",
    "ai support desk sprint": "ai_support_desk_sprint",
    "ai governance program": "ai_governance_program",
}


def _select_catalog() -> Path | None:
    if PRIMARY_CATALOG.is_file():
        return PRIMARY_CATALOG
    if FALLBACK_CATALOG.is_file():
        return FALLBACK_CATALOG
    return None


def _mentioned_offers(catalog: Path) -> set[str]:
    """Return the set of slugs the catalog references."""
    text = catalog.read_text(encoding="utf-8").lower()
    # Strip markdown formatting so 'Lead Intelligence Sprint' still matches inside **...**.
    flat = re.sub(r"[*`_]", "", text)
    found: set[str] = set()
    for human, slug in NAME_TO_SLUG.items():
        if human in flat:
            found.add(slug)
    return found


def main() -> int:
    print("== Dealix Service Catalog Coherence ==")
    catalog = _select_catalog()
    if catalog is None:
        print("[FAIL] no catalog file found")
        print("       missing: docs/company/SERVICE_CATALOG.md")
        print("       missing: docs/strategy/service_portfolio_catalog.md")
        print("--")
        print("SERVICE_CATALOG_PASS=false")
        return 1

    print(f"[INFO] catalog source: {catalog.relative_to(REPO)}")
    mentioned = _mentioned_offers(catalog)
    print(f"[INFO] offers mentioned in catalog: {', '.join(sorted(mentioned)) or '<none>'}")

    if not SERVICES_ROOT.is_dir():
        print(f"[FAIL] services root missing: {SERVICES_ROOT.relative_to(REPO)}")
        print("--")
        print("SERVICE_CATALOG_PASS=false")
        return 1

    missing_folders: list[str] = []
    for slug in REQUIRED_OFFERS:
        folder = SERVICES_ROOT / slug
        if not folder.is_dir():
            missing_folders.append(slug)

    # Cross-check: anything catalog mentions should have a folder too.
    catalog_orphans: list[str] = []
    for slug in mentioned:
        if not (SERVICES_ROOT / slug).is_dir():
            catalog_orphans.append(slug)

    all_ok = True
    for slug in REQUIRED_OFFERS:
        if slug in missing_folders:
            print(f"[FAIL] required offer folder missing: {slug}")
            all_ok = False
        else:
            print(f"[PASS] required offer folder present: {slug}")

    for slug in sorted(set(catalog_orphans) - set(missing_folders)):
        print(f"[FAIL] catalog mentions '{slug}' but no folder under docs/services/")
        all_ok = False

    print("--")
    print(f"SERVICE_CATALOG_PASS={'true' if all_ok else 'false'}")
    print(f"REQUIRED_COVERED={sum(1 for s in REQUIRED_OFFERS if s not in missing_folders)}/{len(REQUIRED_OFFERS)}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
