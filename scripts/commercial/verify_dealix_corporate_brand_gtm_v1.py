#!/usr/bin/env python3
"""Fail-closed verifier for Dealix corporate brand + governed GTM V1."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BRAND = ROOT / "config/company/dealix_brand_architecture_v1.json"
GTM = ROOT / "config/growth/dealix_gtm_social_engine_v1.json"
LAUNCH = ROOT / "config/growth/dealix_market_launch_waves_v1.json"
HOME = ROOT / "apps/web/components/landing/InteractiveHome.tsx"
COMPANY = ROOT / "apps/web/app/company/page.tsx"
SERVICES = ROOT / "apps/web/app/services/page.tsx"
PUBLIC_CATALOG = ROOT / "apps/web/lib/public-catalog.ts"
PRODUCT = ROOT / "apps/web/app/dealix-os/page.tsx"
LAYOUT = ROOT / "apps/web/app/layout.tsx"
CORPORATE_CSS = ROOT / "apps/web/app/corporate-pages.css"
OG = ROOT / "apps/web/public/dealix-og.svg"
SOCIAL_QUEUE = ROOT / "dealix/commercial_ops/social_queue.py"
SOCIAL_EXPANDER = ROOT / "scripts/expand_social_queue_12w.py"
MARKETING_API = ROOT / "api/routers/marketing_ops.py"
WEEKLY_PACK = ROOT / "dealix/marketing_factory/weekly_pack.py"
DAILY_CONTENT = ROOT / "scripts/dealix_content_factory_daily.py"


def load(path: Path) -> dict:
    if not path.exists():
        raise AssertionError(f"missing required file: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    brand = load(BRAND)
    gtm = load(GTM)
    launch = load(LAUNCH)
    home = read(HOME)
    company = read(COMPANY)
    services = read(SERVICES)
    public_catalog = read(PUBLIC_CATALOG)
    product = read(PRODUCT)
    layout = read(LAYOUT)
    corporate_css = read(CORPORATE_CSS)
    og = read(OG)
    social_queue = read(SOCIAL_QUEUE)
    social_expander = read(SOCIAL_EXPANDER)
    marketing_api = read(MARKETING_API)
    weekly_pack = read(WEEKLY_PACK)
    daily_content = read(DAILY_CONTENT)

    assert brand["brand_architecture"]["model"] == "BRANDED_HOUSE_WITH_FLAGSHIP_PRODUCT"
    assert brand["brand_architecture"]["parent_brand"] == "Dealix"
    assert brand["brand_architecture"]["product_layer"]["flagship"] == "Dealix OS"
    assert brand["brand_architecture"]["product_layer"]["category"] == "AI Business Operating System"
    assert len(brand["brand_architecture"]["practices"]) == 4

    for required in [
        "Dealix شركة B2B",
        "Dealix OS",
        "AI Business Operating System",
        "Strategy + Systems + Intelligence + Products",
        "Revenue + Proof + Command",
        "/company",
        "/services",
        "/dealix-os",
    ]:
        assert required in home, f"homepage missing corporate contract: {required}"

    for required in [
        "Strategy & Transformation",
        "Systems & Automation",
        "Intelligence & Market Access",
        "Products & Ventures",
        "dx-corporate-page",
    ]:
        assert required in company, f"company page missing contract: {required}"

    for required in [
        "capabilityCatalog",
        "item.nameEn",
        "item.nameAr",
        "Free Execution Diagnostic",
        "Customer-Specific Outcome Sprint",
        "/book",
    ]:
        assert required in services, f"services page missing current capability contract: {required}"

    for required in [
        "Strategy & Transformation",
        "AI Governance & Reliability",
        "Saudi Market Access & Partner Intelligence",
        "Dealix OS & Productization",
    ]:
        assert required in public_catalog, f"public catalog missing current capability: {required}"

    for required in ["Company Brain", "Opportunity Graph", "Action + Approval", "Proof Ledger", "dx-corporate-page"]:
        assert required in product, f"Dealix OS page missing layer: {required}"

    assert "Dealix — AI Business Operating System" in layout
    assert "Strategy, Systems & Proof" in layout
    assert "corporate-pages.css" in layout
    assert "Dealix OS" in layout

    for token in ["#0f172a", "#164e63", "#22d3ee", ".dx-corporate-page"]:
        assert token in corporate_css.lower(), f"corporate CSS missing identity token: {token}"
    assert "#d4af37" not in corporate_css.lower(), "public corporate CSS must remain navy/cyan without gold authority"
    assert "STRATEGY · SYSTEMS · INTELLIGENCE · PRODUCTS" in og
    assert "Dealix OS" in og

    channels = {item["channel"]: item for item in gtm["priority_channels"]}
    assert channels["Founder LinkedIn"]["execution"] == "MANUAL_OR_APPROVAL_ASSISTED"
    assert channels["Gmail"]["execution"] == "DRAFT_ONLY_UNLESS_EXACT_SEND_AUTHORITY"
    assert channels["WhatsApp Business"]["execution"] == "INBOUND_FIRST_EXACT_ACTION_GATED"
    assert gtm["content_factory"]["default_external_action"] == "DRAFT_ONLY"
    assert "cold WhatsApp blast" in gtm["forbidden_shortcuts"]
    assert "mass LinkedIn connect/DM automation" in gtm["forbidden_shortcuts"]
    assert any("guaranteed revenue" in item.lower() for item in gtm["forbidden_shortcuts"])
    assert any("auto-publish" in item.lower() for item in gtm["forbidden_shortcuts"])
    assert "verified payments" in gtm["measurement"]["primary"]

    assert launch["launch_window_days"] == 90
    wave_ids = {wave["id"] for wave in launch["waves"]}
    for required_wave in [
        "W0_FOUNDATION",
        "W1_FOUNDER_CATEGORY",
        "W2_GOVERNED_AI",
        "W3_MARKET_ACCESS_PARTNERS",
        "W4_FATOORA_TECHNICAL_OPS",
        "W5_PROOF_EXPANSION",
    ]:
        assert required_wave in wave_ids, f"missing market launch wave: {required_wave}"
    assert launch["channel_allocation"]["paid_media"].startswith("off by default")

    assert 'CURRENT_LAUNCH_AUTHORITY = "corporate_brand_gtm_v1"' in social_queue
    assert 'LAUNCH_AUTHORITY = "corporate_brand_gtm_v1"' in social_expander
    assert '"surface": surface' in social_expander
    assert '"external_publish_allowed": False' in social_expander
    assert 'default="https://dealix.me"' in marketing_api
    assert 'post.get("surface") or "linkedin"' in marketing_api
    assert '"/book"' in weekly_pack
    assert "generate_weekly_pack" in daily_content
    assert "get_post_for_date" in daily_content
    assert '"external_publish_executed": False' in daily_content
    assert '"paid_spend_executed": False' in daily_content

    for legacy_runtime_token in ["https://dealix.ai", "Risk Score مجاني", "10-Lead Audit — 499 SAR"]:
        assert legacy_runtime_token not in marketing_api + weekly_pack + social_expander + daily_content, (
            f"legacy marketing runtime token remains: {legacy_runtime_token}"
        )

    public_surfaces = "\n".join([home, company, services, product, layout, og]).lower()
    for forbidden_positive_claim in [
        "production ready",
        "guaranteed revenue",
        "first saudi ai business operating system",
        "first in saudi arabia",
    ]:
        assert forbidden_positive_claim not in public_surfaces, (
            f"forbidden public claim found: {forbidden_positive_claim}"
        )

    print("DEALIX_CORPORATE_BRAND_GTM_V1=PASS")
    print("PARENT_BRAND=Dealix")
    print("FLAGSHIP_PRODUCT=Dealix OS")
    print("SOCIAL_AUTHORITY=corporate_brand_gtm_v1")
    print("MARKET_LAUNCH_WAVES=6")
    print("EXTERNAL_ACTION_DEFAULT=DRAFT_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
