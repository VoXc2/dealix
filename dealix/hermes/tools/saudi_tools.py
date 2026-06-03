"""Saudi-specific tool functions — CR validation, Hijri dates, ZATCA, Vision 2030."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Any

import structlog

logger = structlog.get_logger(__name__)

# Saudi commercial registration number pattern: 10 digits starting with 1, 2, or 7
_CR_PATTERN = re.compile(r'^[127]\d{9}$')


async def validate_cr_number(cr_number: str) -> dict[str, Any]:
    """Validate a Saudi commercial registration (CR) number format.

    Checks: 10-digit format, valid first digit (1, 2, or 7).
    Does not perform live registry lookup (requires MISA API credentials).

    Parameters
    ----------
    cr_number:
        The CR number string to validate.

    Returns
    -------
    dict
        Validation result with is_valid flag, format details, and region hint.
    """
    cleaned = cr_number.strip().replace("-", "").replace(" ", "")

    if not cleaned:
        return {"is_valid": False, "error": "empty_cr_number", "cr_number": cr_number}

    if not cleaned.isdigit():
        return {"is_valid": False, "error": "non_numeric_characters", "cr_number": cr_number}

    if len(cleaned) != 10:
        return {
            "is_valid": False,
            "error": f"invalid_length_{len(cleaned)}_expected_10",
            "cr_number": cr_number,
        }

    if not _CR_PATTERN.match(cleaned):
        return {
            "is_valid": False,
            "error": "invalid_first_digit_must_be_1_2_or_7",
            "cr_number": cr_number,
        }

    # Region hint from first digit
    region_hints = {"1": "riyadh_region", "2": "western_region", "7": "eastern_region"}
    region = region_hints.get(cleaned[0], "unknown")

    logger.info("cr_number_validated", cr_number=cleaned, valid=True, region=region)
    return {
        "is_valid": True,
        "cr_number": cleaned,
        "region_hint": region,
        "format": "10_digit_saudi_cr",
        "note": "Format validation only — live registry lookup requires MISA API.",
    }


async def get_hijri_date(gregorian_date: str = "") -> dict[str, Any]:
    """Convert a Gregorian date to Hijri calendar.

    Uses a simple algorithmic approximation. For official documents,
    use an authoritative conversion service.

    Parameters
    ----------
    gregorian_date:
        ISO date string (YYYY-MM-DD). Defaults to today if empty.

    Returns
    -------
    dict
        Gregorian and Hijri date strings with month names in AR/EN.
    """
    if gregorian_date:
        try:
            dt = datetime.strptime(gregorian_date, "%Y-%m-%d")
        except ValueError:
            return {"error": f"invalid_date_format: {gregorian_date!r}. Use YYYY-MM-DD."}
    else:
        dt = datetime.now(UTC)

    # Simplified Hijri conversion algorithm (Kuwaiti variant)
    # Accurate to +/- 1 day for most dates in the modern era
    jd = _gregorian_to_jdn(dt.year, dt.month, dt.day)
    hy, hm, hd = _jdn_to_hijri(jd)

    hijri_months_en = [
        "", "Muharram", "Safar", "Rabi al-Awwal", "Rabi al-Thani",
        "Jumada al-Awwal", "Jumada al-Thani", "Rajab", "Shaban",
        "Ramadan", "Shawwal", "Dhu al-Qadah", "Dhu al-Hijjah",
    ]
    hijri_months_ar = [
        "", "محرم", "صفر", "ربيع الأول", "ربيع الثاني",
        "جمادى الأولى", "جمادى الثانية", "رجب", "شعبان",
        "رمضان", "شوال", "ذو القعدة", "ذو الحجة",
    ]

    month_en = hijri_months_en[hm] if 1 <= hm <= 12 else "Unknown"
    month_ar = hijri_months_ar[hm] if 1 <= hm <= 12 else "غير معروف"

    return {
        "gregorian": dt.strftime("%Y-%m-%d"),
        "hijri": f"{hy}-{hm:02d}-{hd:02d}",
        "hijri_formatted_en": f"{hd} {month_en} {hy} AH",
        "hijri_formatted_ar": f"{hd} {month_ar} {hy} هـ",
        "hijri_year": hy,
        "hijri_month": hm,
        "hijri_day": hd,
        "month_name_en": month_en,
        "month_name_ar": month_ar,
        "note": "Algorithmic approximation — validate with official Saudi sources for legal documents.",
    }


def _gregorian_to_jdn(year: int, month: int, day: int) -> int:
    """Convert Gregorian date to Julian Day Number."""
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    return day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045


def _jdn_to_hijri(jdn: int) -> tuple[int, int, int]:
    """Convert Julian Day Number to Hijri (Islamic) date."""
    l = jdn - 1948440 + 10632
    n = (l - 1) // 10631
    l = l - 10631 * n + 354
    j = ((10985 - l) // 5316) * ((50 * l) // 17719) + (l // 5670) * ((43 * l) // 15238)
    l = l - ((10985 - l) // 5316) * ((l - 5772) // 3800) - (l // 5670) * ((l - 1800) // 2951) + 29
    hy = 30 * n + j - 30
    hm = (24 * l) // 709
    hd = l - (709 * hm) // 24
    return hy, hm, hd


async def classify_vat_treatment(
    transaction_type: str,
    amount: float,
) -> dict[str, Any]:
    """Classify VAT treatment for a transaction under ZATCA rules.

    Handles standard-rated, zero-rated, and exempt categories for
    Saudi Arabia's VAT regime (15% standard rate as of 2021).

    Parameters
    ----------
    transaction_type:
        Type of transaction (e.g., "b2b_service", "export", "healthcare",
        "education", "financial_service", "real_estate_residential").
    amount:
        Transaction amount in SAR before VAT.

    Returns
    -------
    dict
        VAT classification, applicable rate, VAT amount, and total.
    """
    vat_classifications: dict[str, dict[str, Any]] = {
        "b2b_service": {"category": "standard_rated", "rate": 0.15},
        "b2c_service": {"category": "standard_rated", "rate": 0.15},
        "goods_domestic": {"category": "standard_rated", "rate": 0.15},
        "export": {"category": "zero_rated", "rate": 0.00},
        "international_service": {"category": "zero_rated", "rate": 0.00},
        "healthcare": {"category": "exempt", "rate": 0.00},
        "education": {"category": "exempt", "rate": 0.00},
        "financial_service": {"category": "exempt", "rate": 0.00},
        "real_estate_residential": {"category": "exempt", "rate": 0.00},
        "real_estate_commercial": {"category": "standard_rated", "rate": 0.15},
        "government_supply": {"category": "zero_rated", "rate": 0.00},
    }

    txn_lower = transaction_type.lower().replace(" ", "_").replace("-", "_")
    classification = vat_classifications.get(txn_lower, {"category": "standard_rated", "rate": 0.15})

    rate = classification["rate"]
    category = classification["category"]
    vat_amount = round(amount * rate, 2)
    total_amount = round(amount + vat_amount, 2)

    zatca_ref = {
        "standard_rated": "VAT Law Article 70 — 15% standard rate applies.",
        "zero_rated": "VAT Law Article 79 — zero rate applies; input VAT recoverable.",
        "exempt": "VAT Law Article 82 — supply is exempt; input VAT not recoverable.",
    }

    logger.info("vat_classified", txn_type=transaction_type, category=category, rate=rate)
    return {
        "transaction_type": transaction_type,
        "vat_category": category,
        "vat_rate_pct": round(rate * 100, 1),
        "amount_before_vat_sar": amount,
        "vat_amount_sar": vat_amount,
        "total_amount_sar": total_amount,
        "zatca_reference": zatca_ref.get(category, ""),
        "requires_tax_invoice": amount >= 1000,
        "requires_simplified_invoice": amount < 1000 and category == "standard_rated",
    }


async def get_saudi_market_context(industry: str) -> dict[str, Any]:
    """Return Vision 2030 alignment and market context for a Saudi industry.

    Parameters
    ----------
    industry:
        Industry vertical string (e.g., "technology", "healthcare").

    Returns
    -------
    dict
        Vision 2030 programs, market size, growth drivers, and key players.
    """
    contexts: dict[str, dict[str, Any]] = {
        "technology": {
            "vision_2030_programs": ["NEOM", "SDAIA", "NTP", "Cloud First Policy"],
            "market_size_usd_b": 45,
            "cagr_pct": 14.5,
            "growth_drivers": [
                "Digital transformation mandates",
                "Cloud adoption push",
                "AI strategy (Saudi Data and AI Authority)",
                "Smart city initiatives",
            ],
            "key_opportunity_areas": ["AI/ML platforms", "Cybersecurity", "Cloud services", "ERP"],
            "regulatory_notes": "NDMO data residency requirements apply to sensitive data.",
        },
        "healthcare": {
            "vision_2030_programs": ["Vision 2030 Health Sector Transformation", "MOH digitization"],
            "market_size_usd_b": 65,
            "cagr_pct": 8.2,
            "growth_drivers": [
                "Population growth and aging",
                "Chronic disease burden",
                "Privatization of health services",
                "Telemedicine expansion",
            ],
            "key_opportunity_areas": ["Health IT", "Medical devices", "Pharma", "Telemedicine"],
            "regulatory_notes": "SFDA approval required for medical devices and pharma.",
        },
        "retail": {
            "vision_2030_programs": ["NRF Saudi", "Entertainment Authority expansion"],
            "market_size_usd_b": 95,
            "cagr_pct": 6.1,
            "growth_drivers": [
                "Young population (median age 29)",
                "E-commerce growth 30% YoY",
                "Tourism increase",
                "Giga-project retail",
            ],
            "key_opportunity_areas": ["E-commerce platforms", "Last-mile logistics", "PoS systems"],
            "regulatory_notes": "E-commerce Law and Consumer Protection Law apply.",
        },
        "financial_services": {
            "vision_2030_programs": ["Fintech Saudi", "SAMA Open Banking", "Tadawul expansion"],
            "market_size_usd_b": 90,
            "cagr_pct": 11.3,
            "growth_drivers": [
                "Fintech licensing surge",
                "BNPL adoption",
                "Open banking framework",
                "Digital-only bank licenses",
            ],
            "key_opportunity_areas": ["Payments", "Lending tech", "Wealth management", "Insurance tech"],
            "regulatory_notes": "SAMA and CMA licensing required for regulated activities.",
        },
    }

    ctx = contexts.get(
        industry.lower(),
        {
            "vision_2030_programs": ["Vision 2030 cross-sector initiatives"],
            "market_size_usd_b": 15,
            "cagr_pct": 7.0,
            "growth_drivers": ["Economic diversification", "Private sector growth target 65%"],
            "key_opportunity_areas": ["Digital transformation", "Automation", "Data analytics"],
            "regulatory_notes": "Consult relevant sector regulator for licensing requirements.",
        },
    )

    logger.info("saudi_market_context_retrieved", industry=industry)
    return {
        "industry": industry,
        "context": ctx,
        "vision_2030_target_year": 2030,
        "non_oil_gdp_target_pct": 50,
        "private_sector_gdp_target_pct": 65,
        "retrieved_at": datetime.now(UTC).isoformat(),
    }


async def format_arabic_proposal(data: dict[str, Any]) -> dict[str, Any]:
    """Format a bilingual AR/EN proposal structure.

    Generates structured proposal sections in both Arabic and English
    based on provided data. For production use, pass to a translation
    service for natural language refinement.

    Parameters
    ----------
    data:
        Dict with keys: client_name, service_name, value_proposition,
        price_sar, deliverables (list), timeline_days.

    Returns
    -------
    dict
        Bilingual proposal with sections in AR and EN.
    """
    client = data.get("client_name", "العميل")
    service = data.get("service_name", "الخدمة")
    value_prop = data.get("value_proposition", "تحسين الأداء التجاري")
    price = float(data.get("price_sar", 0))
    deliverables = data.get("deliverables", [])
    timeline = int(data.get("timeline_days", 30))

    deliverables_ar = "\n".join(f"- {d}" for d in deliverables) if deliverables else "- حسب الاتفاق"
    deliverables_en = "\n".join(f"- {d}" for d in deliverables) if deliverables else "- As agreed"

    proposal = {
        "ar": {
            "title": f"عرض خدمات: {service}",
            "greeting": f"السادة {client} المحترمون،",
            "intro": f"يسعدنا تقديم عرضنا لخدمة {service}.",
            "value_proposition": value_prop,
            "deliverables": deliverables_ar,
            "price": f"إجمالي الاستثمار: {price:,.0f} ريال سعودي",
            "timeline": f"المدة الزمنية: {timeline} يوماً",
            "closing": "نتطلع إلى شراكة مثمرة معكم.",
        },
        "en": {
            "title": f"Service Proposal: {service}",
            "greeting": f"Dear {client},",
            "intro": f"We are pleased to present our proposal for {service}.",
            "value_proposition": value_prop,
            "deliverables": deliverables_en,
            "price": f"Total investment: SAR {price:,.0f}",
            "timeline": f"Timeline: {timeline} days",
            "closing": "We look forward to a productive partnership.",
        },
        "metadata": {
            "client_name": client,
            "service_name": service,
            "price_sar": price,
            "timeline_days": timeline,
            "generated_at": datetime.now(UTC).isoformat(),
        },
    }

    logger.info("arabic_proposal_formatted", client=client, service=service)
    return {"proposal": proposal, "formatted": True}


__all__ = [
    "validate_cr_number",
    "get_hijri_date",
    "classify_vat_treatment",
    "get_saudi_market_context",
    "format_arabic_proposal",
]
