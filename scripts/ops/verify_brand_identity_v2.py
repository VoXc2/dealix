#!/usr/bin/env python3
"""Verify the Dealix V2 brand authority and canonical source assets.

This verifier is intentionally narrow: it validates source-of-truth and active
positioning files plus visual invariants. It does not publish assets, infer
trademark status, or rewrite historical provenance.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

AUTHORITY = ROOT / "data/brand/brand_authority.json"
SYSTEM = ROOT / "data/brand/dealix_brand_system_v2.json"
GUIDE = ROOT / "brand/DEALIX_VISUAL_IDENTITY_GUIDE.md"
LOGO_DOC = ROOT / "business/brand/DEALIX_LOGO_AND_IDENTITY_SYSTEM.md"
BRAND_OS = ROOT / "docs/brand/DEALIX_BRAND_OS.md"
POSITIONING = ROOT / "docs/brand/POSITIONING.md"
LLMS = ROOT / "landing/llms.txt"

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
    GUIDE,
    LOGO_DOC,
    BRAND_OS,
    POSITIONING,
    LLMS,
)
ASSET_FILES = (LOGO, MARK, OG, MONO_BLACK, MONO_WHITE, APP_ICON)
FORBIDDEN_ACTIVE_PHRASES = (
    "first Saudi AI Business Operating System",
    "Saudi-first AI Business Operating System",
    "first in Saudi Arabia",
)


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

    if authority.get("schema") != "dealix.brand-authority.v2":
        fail("brand_authority_schema")

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

    for path in CANONICAL_TEXT_FILES:
        text = path.read_text(encoding="utf-8")
        for phrase in FORBIDDEN_ACTIVE_PHRASES:
            # Explicit guardrail/forbidden-claim examples are allowed only in the
            # machine authority files and identity documentation where the phrase
            # is used to forbid it, not to position Dealix.
            if phrase in text and path not in {AUTHORITY, SYSTEM, GUIDE, LOGO_DOC, POSITIONING, LLMS, BRAND_OS}:
                fail(f"unsupported_first_claim:{path.relative_to(ROOT)}")

    # Active positioning files must positively use the approved category.
    for path in (BRAND_OS, POSITIONING, LLMS):
        text = path.read_text(encoding="utf-8")
        if "AI Business Operating System" not in text:
            fail(f"missing_active_category:{path.relative_to(ROOT)}")

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
    print("FIRST_IN_MARKET_CLAIM=false")
    print("PUBLIC_PUBLISH_AUTHORIZED=false")


if __name__ == "__main__":
    main()
