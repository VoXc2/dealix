import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "config/company/dealix_brand_architecture_v1.json"
GTM = ROOT / "config/growth/dealix_gtm_social_engine_v1.json"
LAUNCH = ROOT / "config/growth/dealix_market_launch_waves_v1.json"
HOME = ROOT / "apps/web/components/landing/InteractiveHome.tsx"
SERVICES = ROOT / "apps/web/app/services/page.tsx"
PUBLIC_CATALOG = ROOT / "apps/web/lib/public-catalog.ts"
COMPANY = ROOT / "apps/web/app/company/page.tsx"
PRODUCT = ROOT / "apps/web/app/dealix-os/page.tsx"
CONTENT_FACTORY = ROOT / "scripts/dealix_content_factory_daily.py"
VERIFIER = ROOT / "scripts/commercial/verify_dealix_corporate_brand_gtm_v1.py"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_parent_brand_is_broader_than_flagship_product():
    brand = _json(BRAND)
    assert brand["brand_architecture"]["parent_brand"] == "Dealix"
    assert brand["brand_architecture"]["product_layer"]["flagship"] == "Dealix OS"
    assert brand["brand_architecture"]["product_layer"]["category"] == "AI Business Operating System"
    assert any("single software product" in item for item in brand["company"]["company_is_not"])


def test_public_site_exposes_company_practices_and_product_separately():
    home = HOME.read_text(encoding="utf-8")
    services = SERVICES.read_text(encoding="utf-8")
    public_catalog = PUBLIC_CATALOG.read_text(encoding="utf-8")
    company = COMPANY.read_text(encoding="utf-8")
    product = PRODUCT.read_text(encoding="utf-8")

    assert "Dealix OS هو منتجنا الرئيسي" in home
    assert "Strategy & Transformation" in company
    assert "Systems & Automation" in company
    assert "Intelligence & Market Access" in company
    assert "Products & Ventures" in company
    assert "capabilityCatalog" in services
    assert "Strategy & Transformation" in public_catalog
    assert "AI Governance & Reliability" in public_catalog
    assert "Saudi Market Access & Partner Intelligence" in public_catalog
    assert "Dealix OS & Productization" in public_catalog
    assert "AI Business Operating System" in product


def test_social_engine_optimizes_for_business_movement_not_post_volume():
    gtm = _json(GTM)
    assert gtm["north_star"] == "CASH_READY_AUTONOMOUS_DEALIX_COMPANY"
    assert "verified payments" in gtm["measurement"]["primary"]
    assert "posting volume" in gtm["measurement"]["vanity_only"]
    assert gtm["content_factory"]["default_external_action"] == "DRAFT_ONLY"


def test_social_engine_preserves_consent_and_platform_boundaries():
    gtm = _json(GTM)
    channels = {item["channel"]: item for item in gtm["priority_channels"]}

    assert channels["Founder LinkedIn"]["execution"] == "MANUAL_OR_APPROVAL_ASSISTED"
    assert channels["WhatsApp Business"]["execution"] == "INBOUND_FIRST_EXACT_ACTION_GATED"
    assert channels["Dealix LinkedIn Page"]["execution"] == "DRAFT_READY_PROVIDER_UNPROVEN"
    assert "cold WhatsApp blast" in gtm["forbidden_shortcuts"]
    assert "mass LinkedIn connect/DM automation" in gtm["forbidden_shortcuts"]


def test_market_launch_is_90_day_evidence_led_and_paid_media_off_by_default():
    launch = _json(LAUNCH)
    assert launch["launch_window_days"] == 90
    assert len(launch["waves"]) >= 6
    wave_ids = {wave["id"] for wave in launch["waves"]}
    assert "W1_FOUNDER_CATEGORY" in wave_ids
    assert "W2_GOVERNED_AI" in wave_ids
    assert "W3_MARKET_ACCESS_PARTNERS" in wave_ids
    assert "W4_FATOORA_TECHNICAL_OPS" in wave_ids
    assert launch["channel_allocation"]["paid_media"].startswith("off by default")
    assert "verified_payments" in launch["scorecard"]
    assert "customer_validated_proof" in launch["scorecard"]


def test_daily_content_factory_is_multi_channel_draft_only():
    text = CONTENT_FACTORY.read_text(encoding="utf-8")
    assert "generate_weekly_pack" in text
    assert "get_post_for_date" in text
    assert '"flagship_product": "Dealix OS"' in text
    assert '"external_publish_executed": False' in text
    assert '"paid_spend_executed": False' in text
    assert "DRAFT_ONLY_APPROVAL_FIRST" in text
    assert "Most companies do not need more leads first" not in text


def test_verifier_passes_current_contract():
    spec = importlib.util.spec_from_file_location("dealix_corporate_brand_gtm_v1", VERIFIER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.main() == 0
