#!/usr/bin/env python3
"""Verify the Dealix V2 masterbrand authority and active public surfaces.

This verifier is intentionally bounded: it validates source-of-truth files,
machine-readable tokens, active public brand surfaces and visual invariants.
It does not publish assets, infer trademark status, rewrite historical
provenance, or grant any commercial/channel authority.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

AUTHORITY = ROOT / "data/brand/brand_authority.json"
SYSTEM = ROOT / "data/brand/dealix_brand_system_v2.json"
TOKENS_V21 = ROOT / "data/brand/design_tokens_v2_1.json"
GUIDE = ROOT / "brand/DEALIX_VISUAL_IDENTITY_GUIDE.md"
LOGO_DOC = ROOT / "business/brand/DEALIX_LOGO_AND_IDENTITY_SYSTEM.md"
READABLE_SYSTEM = ROOT / "business/brand/DEALIX_BRAND_SYSTEM.md"
BRAND_OS = ROOT / "docs/brand/DEALIX_BRAND_OS.md"
POSITIONING = ROOT / "docs/brand/POSITIONING.md"
MASTERBRAND_EXPANSION = ROOT / "docs/brand/DEALIX_MASTERBRAND_EXPANSION_V2_1.md"
LLMS = ROOT / "landing/llms.txt"
WEB_BRAND_PAGE = ROOT / "apps/web/app/brand/page.tsx"

LOGO = ROOT / "apps/web/public/dealix-logo.svg"
MARK = ROOT / "apps/web/public/dealix-mark.svg"
OG = ROOT / "apps/web/public/dealix-og.svg"
MONO_BLACK = ROOT / "brand/marks/dealix-mark-black.svg"
MONO_WHITE = ROOT / "brand/marks/dealix-mark-white.svg"
APP_ICON = ROOT / "brand/marks/dealix-app-icon.svg"

REQUIRED_COLORS = {"#0F172A", "#164E63", "#22D3EE", "#F8FAFC"}
CANONICAL_TEXT_FILES = (
    AUTHORITY,
    SYSTEM,
    TOKENS_V21,
    GUIDE,
    LOGO_DOC,
    READABLE_SYSTEM,
    BRAND_OS,
    POSITIONING,
    MASTERBRAND_EXPANSION,
    LLMS,
    WEB_BRAND_PAGE,
)
ASSET_FILES = (LOGO, MARK, OG, MONO_BLACK, MONO_WHITE, APP_ICON)
FORBIDDEN_POSITIONING_PHRASES = (
    "first Saudi AI Business Operating System",
    "Saudi-first AI Business Operating System",
    "first in Saudi Arabia",
)
FORBIDDEN_ACTIVE_VISUAL_PHRASES = (
    "Navy #001F3F",
    "#0E1A33 + Gold",
    "Poppins (display)",
    "Inter + Tajawal",
    "AI Operating Systems for Companies",
)
ACTIVE_PUBLIC_OR_READABLE = (WEB_BRAND_PAGE, READABLE_SYSTEM)


def fail(message: str) -> None:
    raise SystemExit(f"BRAND_IDENTITY_V2=FAIL reason={message}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # bounded verifier output; never print document contents
        fail(f"invalid_json:{path.relative_to(ROOT)}:{type(exc).__name__}")


def main() -> None:
    for path in (*CANONICAL_TEXT_FILES, *ASSET_FILES):
        if not path.is_file():
            fail(f"missing:{path.relative_to(ROOT)}")

    authority = load_json(AUTHORITY)
    system = load_json(SYSTEM)
    tokens = load_json(TOKENS_V21)

    if authority.get("schema") != "dealix.brand-authority.v2":
        fail("brand_authority_schema")
    if tokens.get("schema") != "dealix.design-tokens.v2.1":
        fail("design_tokens_schema")
    if tokens.get("extends") != "data/brand/dealix_brand_system_v2.json":
        fail("design_tokens_must_extend_v2")

    identity = authority.get("canonical_identity", {})
    if identity.get("masterbrand") != "Dealix":
        fail("masterbrand")
    if identity.get("category") != "AI Business Operating System":
        fail("category")
    if identity.get("commercial_wedge") != "Revenue + Proof + Command":
        fail("commercial_wedge")
    if identity.get("core_promise") != "Signals into Action. Execution with Governance. Measurable Outcomes.":
        fail("core_promise")

    claim_policy = authority.get("claim_policy", {})
    if claim_policy.get("first_in_market_claim_allowed") is not False:
        fail("first_in_market_claim_must_be_false")

    if system.get("source", {}).get("positioning") != "AI Business Operating System":
        fail("machine_brand_positioning")

    token_brand = tokens.get("color", {}).get("brand", {})
    expected_token_colors = {
        "ink_navy": "#0F172A",
        "deep_teal": "#164E63",
        "signal_cyan": "#22D3EE",
        "cloud": "#F8FAFC",
        "proof_gold": "#D4AF37",
    }
    if token_brand != expected_token_colors:
        fail("design_token_master_palette_drift")

    token_governance = tokens.get("governance", {})
    if token_governance.get("historical_palettes_are_authority") is not False:
        fail("historical_palette_authority")
    if token_governance.get("proof_gold_dominant_brand_color") is not False:
        fail("proof_gold_must_not_dominate")
    if token_governance.get("public_publish_authorized") is not False:
        fail("brand_tokens_must_not_grant_publish_authority")

    # Active positioning must use the approved category. Historical files are not
    # scanned because provenance is allowed to remain in the repository.
    for path in (BRAND_OS, POSITIONING, LLMS, READABLE_SYSTEM, WEB_BRAND_PAGE):
        text = path.read_text(encoding="utf-8")
        if "AI Business Operating System" not in text:
            fail(f"missing_active_category:{path.relative_to(ROOT)}")

    for path in ACTIVE_PUBLIC_OR_READABLE:
        text = path.read_text(encoding="utf-8")
        for phrase in FORBIDDEN_POSITIONING_PHRASES:
            if phrase in text:
                fail(f"unsupported_first_claim:{path.relative_to(ROOT)}")
        for phrase in FORBIDDEN_ACTIVE_VISUAL_PHRASES:
            if phrase in text:
                fail(f"legacy_brand_drift:{path.relative_to(ROOT)}:{phrase}")

    web_brand = WEB_BRAND_PAGE.read_text(encoding="utf-8")
    for required in (
        "Revenue + Proof + Command",
        "Signal → Decision → Action → Proof",
        "Proof Gold",
        "IBM Plex Sans Arabic",
        "Start the Execution Diagnostic",
    ):
        if required not in web_brand:
            fail(f"web_brand_missing:{required}")

    asset_blob = "\n".join(path.read_text(encoding="utf-8") for path in (LOGO, MARK, OG, APP_ICON))
    for color in REQUIRED_COLORS:
        if color not in asset_blob:
            fail(f"missing_color:{color}")

    if "AI BUSINESS OPERATING SYSTEM" not in LOGO.read_text(encoding="utf-8"):
        fail("logo_descriptor")
    if "Signals into Action." not in OG.read_text(encoding="utf-8"):
        fail("og_core_message")

    black = MONO_BLACK.read_text(encoding="utf-8")
    white = MONO_WHITE.read_text(encoding="utf-8")
    if "#0F172A" not in black:
        fail("monochrome_black")
    if "#F8FAFC" not in white:
        fail("monochrome_white")

    print("BRAND_IDENTITY_V2=PASS")
    print("CATEGORY=AI Business Operating System")
    print("MARK=D + Forward Signal")
    print("MASTERBRAND_EXPANSION=V2.1_DRAFT")
    print("FIRST_IN_MARKET_CLAIM=false")
    print("PUBLIC_PUBLISH_AUTHORIZED=false")


if __name__ == "__main__":
    main()
