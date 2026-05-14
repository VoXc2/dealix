"""GCC regulatory market posture — Wave 19.

Single source of truth for Dealix's expansion across the 4 priority GCC
markets. The Saudi beachhead (2026-Q2) is the live anchor; UAE / Qatar /
Kuwait are mapped here so the governance pack can extend with a 1-line
edit when each market opens.

Every entry carries:
- `country`: ISO 3166-1 alpha-2 (SA, AE, QA, KW)
- `country_ar` / `country_en`: bilingual labels
- `regulator`: the data-protection authority (NDMO Saudi, ADGM/DIFC UAE,
  NPC Qatar, CITRA Kuwait)
- `framework`: the canonical PDPL-equivalent statute
- `framework_articles`: the specific articles Dealix maps to the
  governance pack (Saudi anchor = PDPL Article 5/13/14/18/21)
- `dealix_status`: one of {active, pilot_ready, future_market}
- `local_payment_processor`: the named local processor we'd integrate
- `local_invoicing_standard`: e-invoicing equivalent of Saudi ZATCA
- `language_priority`: dialect/MSA priority (Khaleeji for Saudi/UAE/Qatar/Kuwait)

NEVER claims a market is `active` without a passing test reference.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

MarketStatus = Literal["active", "pilot_ready", "future_market"]


@dataclass(frozen=True)
class GCCMarket:
    country: str
    country_ar: str
    country_en: str
    regulator: str
    framework: str
    framework_articles: tuple[str, ...]
    dealix_status: MarketStatus
    local_payment_processor: str
    local_invoicing_standard: str
    language_priority: str
    notes: str


GCC_MARKETS: tuple[GCCMarket, ...] = (
    GCCMarket(
        country="SA",
        country_ar="المملكة العربية السعودية",
        country_en="Kingdom of Saudi Arabia",
        regulator="NDMO + SDAIA",
        framework="PDPL — Royal Decree M/19 (2021), Implementing Regulation (2023)",
        framework_articles=(
            "Article 5 (lawful basis)",
            "Article 13 (data subject rights)",
            "Article 14 (consent)",
            "Article 18 (data transfers)",
            "Article 21 (penalties)",
        ),
        dealix_status="active",
        local_payment_processor="Moyasar",
        local_invoicing_standard="ZATCA Phase 2 (e-invoicing)",
        language_priority="Khaleeji Arabic (Saudi) primary; MSA + EN secondary",
        notes=(
            "The active beachhead. 2026-Q2 reframe targets 50–500-employee "
            "B2B services. Live invoicing via Moyasar (cutover script ready). "
            "Audit chain + Trust Pack accepted by Saudi CISOs out of the box."
        ),
    ),
    GCCMarket(
        country="AE",
        country_ar="الإمارات العربية المتحدة",
        country_en="United Arab Emirates",
        regulator="UAE Data Office + ADGM + DIFC (free-zone variants)",
        framework="UAE Federal Decree-Law No. 45 of 2021 on the Protection of Personal Data",
        framework_articles=(
            "Article 5 (data controller obligations)",
            "Article 9 (consent)",
            "Article 13 (cross-border transfers)",
            "Article 18 (data subject rights)",
            "Article 22 (penalties)",
        ),
        dealix_status="pilot_ready",
        local_payment_processor="Telr / Network International / Checkout.com",
        local_invoicing_standard="FTA e-invoicing (rollout 2026+)",
        language_priority="Khaleeji Arabic (UAE) primary; English equal weight (per market)",
        notes=(
            "Pilot-ready: governance pack maps 1:1 to UAE Federal Decree-Law "
            "No. 45 of 2021. ADGM/DIFC free-zone deviations documented per "
            "engagement. NOT yet active — Dealix has no UAE retainer signed. "
            "Opens after 1 Saudi flagship Sprint case study is published."
        ),
    ),
    GCCMarket(
        country="QA",
        country_ar="دولة قطر",
        country_en="State of Qatar",
        regulator="National Cyber Security Agency (NCSA) + Ministry of Transport",
        framework="Qatar PDPPL — Law No. 13 of 2016 on Personal Data Protection",
        framework_articles=(
            "Article 4 (consent)",
            "Article 6 (data minimisation)",
            "Article 7 (purpose limitation)",
            "Article 14 (special categories)",
            "Article 18 (cross-border transfers)",
        ),
        dealix_status="future_market",
        local_payment_processor="QPay / SkipCash / Doha Bank",
        local_invoicing_standard="No mandatory e-invoicing yet (manual + VAT pending)",
        language_priority="Khaleeji Arabic (Qatari) primary; English secondary",
        notes=(
            "Future market: Qatar PDPPL is the oldest GCC PDPL (2016) and the "
            "most permissive. Dealix governance pack exceeds the floor "
            "comfortably. Activation gated on a Qatari B2B services anchor "
            "customer + a local legal entity (not Saudi-Article-18 transferable "
            "without DPA)."
        ),
    ),
    GCCMarket(
        country="KW",
        country_ar="دولة الكويت",
        country_en="State of Kuwait",
        regulator="CITRA (Communications and Information Technology Regulatory Authority)",
        framework="Data Privacy Protection Regulation (DPPR) No. 26 of 2024 (CITRA)",
        framework_articles=(
            "Article 4 (consent + lawful basis)",
            "Article 6 (DPO requirement)",
            "Article 9 (data subject rights)",
            "Article 13 (cross-border transfers)",
            "Article 17 (breach notification)",
        ),
        dealix_status="future_market",
        local_payment_processor="KNET (the only domestic processor)",
        local_invoicing_standard="No mandatory e-invoicing standard",
        language_priority="Khaleeji Arabic (Kuwaiti) primary; English secondary",
        notes=(
            "Future market: Kuwait DPPR landed in 2024 and is still maturing. "
            "DPO requirement plus tight cross-border restrictions make the "
            "Dealix governance pack particularly relevant. Activation gated "
            "on the same revenue milestone as Qatar."
        ),
    ),
)


def list_markets() -> tuple[GCCMarket, ...]:
    """All 4 priority GCC markets in canonical order (Saudi anchor first)."""
    return GCC_MARKETS


def get_market(country: str) -> GCCMarket | None:
    """Resolve a market by ISO 3166-1 alpha-2 code (case-insensitive)."""
    code = (country or "").upper()
    for m in GCC_MARKETS:
        if m.country == code:
            return m
    return None


__all__ = [
    "MarketStatus",
    "GCCMarket",
    "GCC_MARKETS",
    "list_markets",
    "get_market",
]
