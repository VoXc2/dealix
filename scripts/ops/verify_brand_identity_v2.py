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
ASSET_REGISTRY = ROOT / "data/brand/asset_template_registry_v1.json"
GUIDE = ROOT / "brand/DEALIX_VISUAL_IDENTITY_GUIDE.md"
LOGO_DOC = ROOT / "business/brand/DEALIX_LOGO_AND_IDENTITY_SYSTEM.md"
READABLE_SYSTEM = ROOT / "business/brand/DEALIX_BRAND_SYSTEM.md"
BRAND_OS = ROOT / "docs/brand/DEALIX_BRAND_OS.md"
POSITIONING = ROOT / "docs/brand/POSITIONING.md"
MASTERBRAND_EXPANSION = ROOT / "docs/brand/DEALIX_MASTERBRAND_EXPANSION_V2_1.md"
ENTERPRISE_ASSET_SYSTEM = ROOT / "docs/brand/DEALIX_ENTERPRISE_ASSET_SYSTEM_V1.md"
PRESS_KIT = ROOT / "docs/BRAND_PRESS_KIT.md"
LLMS = ROOT / "landing/llms.txt"
WEB_BRAND_PAGE = ROOT / "apps/web/app/brand/page.tsx"
PUBLIC_TERMS = ROOT / "landing/terms.html"
SALES_AGENT = ROOT / ".claude/agents/dealix-sales.md"
PROOF_TEMPLATE = ROOT / "data/templates/proof_pack_ar.md"

LOGO = ROOT / "apps/web/public/dealix-logo.svg"
MARK = ROOT / "apps/web/public/dealix-mark.svg"
OG = ROOT / "apps/web/public/dealix-og.svg"
MONO_BLACK = ROOT / "brand/marks/dealix-mark-black.svg"
MONO_WHITE = ROOT / "brand/marks/dealix-mark-white.svg"
APP_ICON = ROOT / "brand/marks/dealix-app-icon.svg"

REQUIRED_COLORS = {"#0F172A", "#164E63", "#22D3EE", "#F8FAFC"}
EXACT_AGENTS = {
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
}
CANONICAL_TEXT_FILES = (
    AUTHORITY,
    SYSTEM,
    TOKENS_V21,
    ASSET_REGISTRY,
    GUIDE,
    LOGO_DOC,
    READABLE_SYSTEM,
    BRAND_OS,
    POSITIONING,
    MASTERBRAND_EXPANSION,
    ENTERPRISE_ASSET_SYSTEM,
    PRESS_KIT,
    LLMS,
    WEB_BRAND_PAGE,
    PUBLIC_TERMS,
    SALES_AGENT,
    PROOF_TEMPLATE,
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
FORBIDDEN_LEGACY_COMMERCIAL_PHRASES = (
    "499 SAR Sprint",
    "12,000 SAR/month",
    "first paid pilots are running",
    "first three hires",
    "replaces the first 3 hires",
)
ACTIVE_PUBLIC_OR_READABLE = (
    WEB_BRAND_PAGE,
    READABLE_SYSTEM,
    PRESS_KIT,
    PUBLIC_TERMS,
    SALES_AGENT,
    PROOF_TEMPLATE,
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
    tokens = load_json(TOKENS_V21)
    asset_registry = load_json(ASSET_REGISTRY)

    if authority.get("schema") != "dealix.brand-authority.v2":
        fail("brand_authority_schema")
    if tokens.get("schema") != "dealix.design-tokens.v2.1":
        fail("design_tokens_schema")
    if tokens.get("extends") != "data/brand/dealix_brand_system_v2.json":
        fail("design_tokens_must_extend_v2")
    if asset_registry.get("schema") != "dealix.brand-asset-registry.v1":
        fail("brand_asset_registry_schema")
    if asset_registry.get("masterbrand") != "Dealix":
        fail("brand_asset_registry_masterbrand")
    if set(asset_registry.get("allowed_owner_agents", [])) != EXACT_AGENTS:
        fail("brand_asset_registry_agent_set")

    registry_governance = asset_registry.get("governance", {})
    for flag in (
        "second_masterbrand",
        "second_proof_system",
        "second_agent_fleet",
        "auto_publication",
        "auto_external_send",
        "auto_supplier_registration",
        "auto_bid_submission",
        "auto_binding_quote",
        "auto_customer_proof",
    ):
        if registry_governance.get(flag) is not False:
            fail(f"brand_asset_registry_governance:{flag}")

    template_ids = {item.get("id") for item in asset_registry.get("templates", [])}
    required_templates = {
        "company_profile_v2_1",
        "execution_diagnostic",
        "customer_specific_proposal",
        "weekly_proof_pack",
        "trust_security_appendix",
        "supplier_readiness_passport",
        "rfp_tender_decision_pack",
        "partner_subcontract_pack",
    }
    if not required_templates.issubset(template_ids):
        fail("brand_asset_registry_required_templates")

    for template in asset_registry.get("templates", []):
        if template.get("owner_agent") not in EXACT_AGENTS:
            fail(f"brand_asset_registry_unknown_owner:{template.get('id')}")
        if not set(template.get("support_agents", [])).issubset(EXACT_AGENTS):
            fail(f"brand_asset_registry_unknown_support_agent:{template.get('id')}")
        for key, value in template.items():
            if key.endswith("_authority") and value is not False:
                fail(f"brand_asset_registry_authority_escalation:{template.get('id')}:{key}")

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
    for path in (
        BRAND_OS,
        POSITIONING,
        LLMS,
        READABLE_SYSTEM,
        PRESS_KIT,
        WEB_BRAND_PAGE,
        PUBLIC_TERMS,
        SALES_AGENT,
        PROOF_TEMPLATE,
    ):
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
        for phrase in FORBIDDEN_LEGACY_COMMERCIAL_PHRASES:
            if phrase in text:
                fail(f"legacy_commercial_drift:{path.relative_to(ROOT)}:{phrase}")

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

    press = PRESS_KIT.read_text(encoding="utf-8")
    for required in (
        "PRESS_KIT_PUBLICATION_AUTHORITY=false",
        "CUSTOMER_PROOF_AUTO_GRANT=false",
        "MARKETING_CONSENT_AUTO_GRANT=false",
        "LEGAL_CLEARANCE_PENDING",
    ):
        if required not in press:
            fail(f"press_kit_missing_guardrail:{required}")

    enterprise_assets = ENTERPRISE_ASSET_SYSTEM.read_text(encoding="utf-8")
    for required in (
        "Dealix Supplier Readiness Passport",
        "Supplier Registration != Tender Invitation",
        "Tender Publication != Dealix Eligibility",
        "No sixth permanent brand/marketing agent is created.",
        "L5_EXECUTED=NONE",
    ):
        if required not in enterprise_assets:
            fail(f"enterprise_asset_system_missing:{required}")

    sales_agent = SALES_AGENT.read_text(encoding="utf-8")
    for required in (
        "data/brand/brand_authority.json",
        "data/brand/asset_template_registry_v1.json",
        "docs/brand/DEALIX_ENTERPRISE_ASSET_SYSTEM_V1.md",
        "Public Contact",
    ):
        if required not in sales_agent:
            # 'Public Contact' may remain implicit in older safe phrasing; keep a
            # specific failure so the authority surface cannot silently weaken.
            if required == "Public Contact" and "public contact data as consent" in sales_agent:
                continue
            fail(f"sales_agent_missing_brand_contract:{required}")

    proof_template = PROOF_TEMPLATE.read_text(encoding="utf-8")
    for required in (
        "brand_version: V2.1_DRAFT",
        "template_version: proof_pack_ar_v2_1",
        "Dealix — AI Business Operating System · Revenue + Proof + Command",
        "Publication Permission",
    ):
        if required not in proof_template:
            fail(f"proof_template_missing_brand_contract:{required}")

    public_terms = PUBLIC_TERMS.read_text(encoding="utf-8")
    if "مبني للتنفيذ المحكوم مع سياق السوق السعودي عند الحاجة" not in public_terms:
        fail("terms_missing_current_market_context")

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
    print("ENTERPRISE_ASSET_REGISTRY=PASS")
    print("PERMANENT_AGENT_COUNT=5")
    print("ACTIVE_BRAND_SURFACE_MIGRATION=PASS")
    print("FIRST_IN_MARKET_CLAIM=false")
    print("PUBLIC_PUBLISH_AUTHORIZED=false")


if __name__ == "__main__":
    main()
