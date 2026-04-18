"""
Tech Stack Detection Source — BuiltWith / Wappalyzer Style
==========================================================
Detects technologies used by a target company's website.

Tech stack signals enable:
  1. Identifying competitors' customers (e.g. "using Shopify → potential Salla/Zid prospect")
  2. Assessing digital maturity (modern stack = higher willingness to buy SaaS)
  3. Finding integration opportunities (e.g. "using HubSpot → can connect to Dealix")
  4. Detecting tech changes (switching from X to Y = buying moment)

DATA SOURCES:
  - BuiltWith API (paid, most comprehensive)
  - Wappalyzer API / CLI (open source option)
  - Manual DNS/header inspection (free, partial)
  - SimilarWeb for traffic estimates (requires API key)

STATUS: Stub implementation.
TODO: Integrate BuiltWith or Wappalyzer API.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import httpx

from ..models import Company, Signal, SignalType


# ─────────────────────────── Tech Categories ─────────────────────────────────

TECH_CATEGORIES = {
    "ecommerce": ["Shopify", "WooCommerce", "Magento", "Salla", "Zid", "Hybris", "BigCommerce"],
    "crm": ["HubSpot", "Salesforce", "Zoho CRM", "Pipedrive", "Monday.com"],
    "marketing_automation": ["Klaviyo", "Mailchimp", "ActiveCampaign", "Marketo", "Braze"],
    "analytics": ["Google Analytics", "Mixpanel", "Amplitude", "Heap", "PostHog"],
    "cdn": ["Cloudflare", "Fastly", "Akamai", "CloudFront"],
    "hosting": ["AWS", "Azure", "GCP", "Hetzner", "DigitalOcean"],
    "chat": ["Zendesk", "Intercom", "LiveChat", "Freshdesk", "Tidio"],
    "payment": ["Stripe", "Moyasar", "Tap Payments", "PayPal", "Hyperpay"],
    "erp": ["SAP", "Oracle ERP", "Microsoft Dynamics", "Odoo"],
}

# Competitor tech → Dealix ICP relevance score boost
COMPETITOR_SIGNALS: dict[str, float] = {
    # If they use a competitor CRM → they understand CRM value → easier sell
    "HubSpot": 15.0,
    "Salesforce": 20.0,
    "Zoho CRM": 10.0,
    # If they're on a major ecommerce platform → need outreach automation
    "Shopify": 12.0,
    "Salla": 10.0,
    "Zid": 10.0,
    "WooCommerce": 8.0,
    # If they use marketing automation → they invest in martech
    "Klaviyo": 10.0,
    "Mailchimp": 8.0,
    "ActiveCampaign": 10.0,
}

# Seed tech stack data for demo
SEED_TECH_STACKS: dict[str, list[str]] = {
    "Salla": ["Laravel", "Vue.js", "AWS", "Redis", "Cloudflare", "Google Analytics", "Intercom"],
    "Foodics": ["React", "Ruby on Rails", "PostgreSQL", "AWS", "HubSpot", "Stripe"],
    "Tabby": ["React", "Node.js", "PostgreSQL", "AWS", "Stripe", "Braze", "Mixpanel"],
    "ROSHN": ["Salesforce", "Oracle", "SAP", "AWS", "Adobe Analytics", "Cloudflare"],
    "Noon Academy": ["React Native", "AWS", "Firebase", "Node.js", "Google Analytics", "Intercom"],
    "Jarir Marketing Company": ["Magento", "Salesforce", "SAP", "Akamai", "Google Analytics"],
    "Nahdi Medical Company": ["SAP", "Salesforce", "Oracle", "Custom Mobile App", "Google Analytics"],
}


class TechStackSource:
    """
    مصدر كشف التقنيات — Tech Stack Intelligence.

    يكتشف التقنيات التي تستخدمها الشركة عبر:
    1. BuiltWith API (الأشمل — مدفوع)
    2. Wappalyzer (مفتوح المصدر — مجاني جزئياً)
    3. فحص HTTP headers / DNS مباشر (مجاني، محدود)
    """

    BUILTWITH_BASE_URL = "https://api.builtwith.com/free1/api.json"
    WAPPALYZER_BASE_URL = "https://api.wappalyzer.com/v2"

    def __init__(
        self,
        builtwith_api_key: str | None = None,
        wappalyzer_api_key: str | None = None,
        session: httpx.AsyncClient | None = None,
    ) -> None:
        """
        Args:
            builtwith_api_key: مفتاح BuiltWith API — متغير البيئة: BUILTWITH_API_KEY
            wappalyzer_api_key: مفتاح Wappalyzer API — متغير البيئة: WAPPALYZER_API_KEY
            session: httpx.AsyncClient اختياري للمشاركة
        """
        self.builtwith_api_key = builtwith_api_key
        self.wappalyzer_api_key = wappalyzer_api_key
        self._session = session

    # ─────────────────────────── Public API ─────────────────────────────────

    async def detect(self, company: Company) -> list[str]:
        """
        اكتشف التقنيات المستخدمة في موقع الشركة.

        Returns:
            قائمة بأسماء التقنيات المكتشفة.
        """
        if not company.domain and not company.website:
            return company.tech_stack  # Return already-known stack

        # Use seed data if no API key
        if not self.builtwith_api_key and not self.wappalyzer_api_key:
            return self._get_seed_stack(company)

        # Try BuiltWith first, fall back to Wappalyzer
        if self.builtwith_api_key:
            return await self._fetch_builtwith(company)
        return await self._fetch_wappalyzer(company)

    async def get_signals(self, company: Company) -> list[Signal]:
        """
        تحويل التقنيات المكتشفة إلى إشارات بيعية.
        Convert tech stack into scored intent signals.
        """
        tech = await self.detect(company)
        signals: list[Signal] = []

        # Update company tech stack
        known_stack = set(company.tech_stack)
        new_tech = [t for t in tech if t not in known_stack]

        if new_tech:
            signals.append(
                Signal(
                    signal_type=SignalType.TECH_CHANGE,
                    title=f"تقنيات مكتشفة: {', '.join(new_tech[:5])}",
                    description=f"إجمالي التقنيات المكتشفة: {len(tech)}",
                    score_contribution=5.0,
                    source="tech_stack_detection",
                )
            )

        # Check for competitor/relevant tech
        for tech_name in tech:
            score = COMPETITOR_SIGNALS.get(tech_name)
            if score:
                signals.append(
                    Signal(
                        signal_type=SignalType.TECH_CHANGE,
                        title=f"يستخدم {tech_name}",
                        description=f"استخدام {tech_name} يشير إلى جاهزية لشراء SaaS مماثل",
                        score_contribution=score,
                        source="tech_stack_detection",
                        metadata={"tech": tech_name, "category": self._categorize(tech_name)},
                    )
                )

        # Digital maturity signal: cloud + modern stack
        cloud_providers = {"AWS", "Azure", "GCP", "Cloudflare"}
        if any(t in cloud_providers for t in tech):
            signals.append(
                Signal(
                    signal_type=SignalType.TECH_CHANGE,
                    title="بنية سحابية حديثة",
                    description="الشركة تستخدم خدمات سحابية → نضج رقمي عالٍ",
                    score_contribution=8.0,
                    source="tech_stack_detection",
                )
            )

        return signals

    async def estimate_digital_maturity(self, company: Company) -> float:
        """
        تقدير مستوى النضج الرقمي للشركة من 0 إلى 100.

        Scoring:
          - Modern cloud infra: +20
          - CRM presence: +20
          - Marketing automation: +15
          - Analytics tools: +15
          - Modern frontend (React/Vue/Next): +10
          - Payment integration: +10
          - Support tools (Intercom/Zendesk): +10
        """
        tech = await self.detect(company)
        tech_set = set(t.lower() for t in tech)

        score = 0.0

        # Cloud infra
        if any(t in tech_set for t in ["aws", "azure", "gcp", "cloudflare"]):
            score += 20

        # CRM
        if any(t in tech_set for t in ["hubspot", "salesforce", "zoho crm"]):
            score += 20

        # Marketing automation
        if any(t in tech_set for t in ["klaviyo", "mailchimp", "activecampaign", "braze"]):
            score += 15

        # Analytics
        if any(t in tech_set for t in ["google analytics", "mixpanel", "amplitude", "posthog"]):
            score += 15

        # Modern frontend
        if any(t in tech_set for t in ["react", "vue.js", "next.js", "angular"]):
            score += 10

        # Payment
        if any(t in tech_set for t in ["stripe", "moyasar", "tap payments"]):
            score += 10

        # Support
        if any(t in tech_set for t in ["intercom", "zendesk", "freshdesk"]):
            score += 10

        return min(100.0, score)

    # ─────────────────────────── Seed Data ───────────────────────────────────

    def _get_seed_stack(self, company: Company) -> list[str]:
        """استرجاع التقنيات من بيانات الـ seed."""
        for name, stack in SEED_TECH_STACKS.items():
            if company.name and name.lower() in company.name.lower():
                return stack
        return company.tech_stack or []

    # ─────────────────────────── BuiltWith (stub) ────────────────────────────

    async def _fetch_builtwith(self, company: Company) -> list[str]:
        """
        جلب التقنيات عبر BuiltWith API.

        TODO: Parse BuiltWith response structure.
        Response: { "Results": [{ "Result": { "Paths": [{ "Technologies": [...] }] } }] }
        Each technology: { "Name": "React", "Categories": ["JavaScript Framework"] }

        Rate limit: Depends on plan (Free = 1000 lookups/mo)
        """
        raise NotImplementedError(
            "TODO: Implement BuiltWith tech stack detection.\n"
            "Credential needed: BUILTWITH_API_KEY\n"
            "Set env var: BUILTWITH_API_KEY\n"
            "Get key: https://api.builtwith.com/signup\n"
            "Endpoint: GET https://api.builtwith.com/free1/api.json\n"
            "Params: KEY={BUILTWITH_API_KEY}&LOOKUP={domain}\n"
            "Pricing: Free tier (1k lookups/mo) | Pro from $295/mo"
        )

    # ─────────────────────────── Wappalyzer (stub) ───────────────────────────

    async def _fetch_wappalyzer(self, company: Company) -> list[str]:
        """
        جلب التقنيات عبر Wappalyzer API.

        TODO: Parse Wappalyzer response.
        Response: { "technologies": [{ "name": "React", "categories": [...] }] }

        Alternative: Use open-source Wappalyzer CLI locally (no API key needed).
        Command: wappalyzer https://example.com --pretty
        """
        raise NotImplementedError(
            "TODO: Implement Wappalyzer tech stack detection.\n"
            "Option 1 — Wappalyzer API:\n"
            "  Credential: WAPPALYZER_API_KEY\n"
            "  Get key: https://www.wappalyzer.com/api\n"
            "  Endpoint: GET https://api.wappalyzer.com/v2/lookup?urls={url}\n"
            "\n"
            "Option 2 — Open source CLI (free, no key needed):\n"
            "  Install: npm install -g wappalyzer\n"
            "  Usage: wappalyzer https://{domain} --pretty\n"
            "  Integrate via subprocess in Python"
        )

    # ─────────────────────────── Utils ───────────────────────────────────────

    def _categorize(self, tech_name: str) -> str:
        """تصنيف التقنية ضمن فئتها."""
        for category, techs in TECH_CATEGORIES.items():
            if tech_name in techs:
                return category
        return "other"
