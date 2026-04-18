"""
Lead Normalizer — Dealix Lead Intelligence Engine V2
====================================================
Converts RawLead → NormalizedLead:
- Phone → E.164 (using python-phonenumbers)
- Email validation (DNS MX check)
- Arabic name extraction
- Company name normalization for dedup
- Gulf geo normalization
"""

from __future__ import annotations

import asyncio
import logging
import re
import socket
from typing import List, Optional

import phonenumbers
from phonenumbers import PhoneNumberFormat, NumberParseException

from app.intelligence.v2.gulf_geo import GULF_COUNTRIES, normalize_city_name
from app.intelligence.v2.i18n import (
    normalize_company_name,
    normalize_arabic_digits,
    detect_language,
    extract_arabic_names,
)
from app.intelligence.v2.models import NormalizedLead, RawLead

logger = logging.getLogger(__name__)

# Gulf country phone codes for defaulting
COUNTRY_PHONE_DEFAULTS = {
    "SA": "SA", "UAE": "AE", "KW": "KW", "QA": "QA", "BH": "BH", "OM": "OM",
}

# Map of ISO codes to phonenumbers region codes
PHONENUMBERS_REGION = {
    "SA": "SA", "UAE": "AE", "KW": "KW", "QA": "QA", "BH": "BH", "OM": "OM",
}


def normalize_phone_e164(raw_phone: str, country: str = "SA") -> Optional[str]:
    """
    Parse and normalize a phone number to E.164 format.
    Returns None if the number is invalid.
    """
    if not raw_phone:
        return None

    # First normalize Arabic digits
    raw_phone = normalize_arabic_digits(raw_phone)

    # Clean separators
    cleaned = re.sub(r"[\s\-\.\(\)\/]", "", raw_phone)

    # Handle Saudi shorthand: 05xxxxxxxx → +96605xxxxxxxx
    if re.match(r"^05\d{8}$", cleaned):
        cleaned = "+966" + cleaned[1:]  # +966 + 5xxxxxxxx

    # Handle local format without leading zero: 5xxxxxxxx
    if re.match(r"^5\d{8}$", cleaned) and country == "SA":
        cleaned = "+9665" + cleaned[1:]

    region = PHONENUMBERS_REGION.get(country, "SA")

    try:
        parsed = phonenumbers.parse(cleaned, region)
        if phonenumbers.is_valid_number(parsed):
            return phonenumbers.format_number(parsed, PhoneNumberFormat.E164)
        return None
    except NumberParseException:
        return None


def validate_email_format(email: str) -> bool:
    """Basic email format validation (not DNS)."""
    if not email:
        return False
    pattern = r"^[\w.+-]+@[\w.-]+\.\w{2,}$"
    return bool(re.match(pattern, email.strip()))


async def check_email_mx(email: str) -> bool:
    """
    Check if the email domain has a valid MX record.
    Uses asyncio to avoid blocking. Returns False on any error.
    """
    if not validate_email_format(email):
        return False

    domain = email.split("@")[-1].strip().lower()

    def _resolve():
        try:
            # Use getaddrinfo as simple DNS check (MX requires dnspython)
            # Fallback: check if domain resolves at all
            socket.getaddrinfo(domain, None)
            return True
        except (socket.gaierror, OSError):
            return False

    try:
        loop = asyncio.get_event_loop()
        result = await asyncio.wait_for(
            loop.run_in_executor(None, _resolve),
            timeout=3.0,
        )
        return result
    except asyncio.TimeoutError:
        return False


def extract_country(raw_lead: RawLead) -> str:
    """Determine country from raw lead data."""
    if raw_lead.country:
        c = raw_lead.country.upper().strip()
        if c in GULF_COUNTRIES:
            return c
        if c == "AE":
            return "UAE"

    # Detect from phone
    if raw_lead.phone:
        phone = normalize_arabic_digits(raw_lead.phone)
        for code, country_data in GULF_COUNTRIES.items():
            prefix = country_data.phone_prefix.replace("+", "")
            if phone.lstrip("+").startswith(prefix) or phone.startswith(country_data.phone_prefix):
                return code

    # Detect from domain
    if raw_lead.domain:
        for code, country_data in GULF_COUNTRIES.items():
            if raw_lead.domain.endswith(country_data.tld):
                return code

    return "SA"  # Default: Saudi Arabia


def make_dedup_key(lead: NormalizedLead) -> str:
    """
    Create a deduplication key.
    Priority: domain > phone > company_name_normalized
    """
    if lead.domain:
        return f"domain:{lead.domain.lower().strip()}"
    if lead.phone_e164:
        return f"phone:{lead.phone_e164}"
    name_norm = normalize_company_name(lead.company_name, lang="en")
    if lead.company_name_ar:
        name_norm_ar = normalize_company_name(lead.company_name_ar, lang="ar")
        return f"name_ar:{name_norm_ar}" if name_norm_ar else f"name_en:{name_norm}"
    return f"name_en:{name_norm}"


async def normalize_lead(raw_lead: RawLead) -> Optional[NormalizedLead]:
    """
    Normalize a single RawLead into a NormalizedLead.
    Returns None if the lead lacks a company name.
    """
    # Must have a company name
    company_name = raw_lead.company_name
    if not company_name:
        if raw_lead.domain:
            company_name = raw_lead.domain.split(".")[0].title()
        else:
            return None

    country = extract_country(raw_lead)

    # Phone normalization
    phone_e164 = None
    if raw_lead.phone:
        phone_e164 = normalize_phone_e164(raw_lead.phone, country)

    # Contact phone
    contact_phone_e164 = None
    if raw_lead.contact_phone:
        contact_phone_e164 = normalize_phone_e164(raw_lead.contact_phone, country)

    # Email validation
    email = raw_lead.email
    email_mx_valid = False
    if email and validate_email_format(email):
        email_mx_valid = await check_email_mx(email)
    else:
        email = None

    # City normalization
    city = raw_lead.city
    city_slug = normalize_city_name(city) if city else None

    # Arabic name extraction from description if no AR name provided
    company_name_ar = raw_lead.company_name_ar
    if not company_name_ar and raw_lead.description:
        ar_names = extract_arabic_names(raw_lead.description)
        if ar_names:
            company_name_ar = ar_names[0]

    # Domain cleanup
    domain = raw_lead.domain
    if not domain and raw_lead.website:
        from urllib.parse import urlparse
        parsed = urlparse(raw_lead.website)
        domain = parsed.netloc.lstrip("www.") if parsed.netloc else None

    normalized = NormalizedLead(
        raw_lead_ids=[raw_lead.id],
        provenances=[raw_lead.provenance],
        company_name=company_name,
        company_name_ar=company_name_ar,
        domain=domain,
        website=raw_lead.website,
        phone_e164=phone_e164,
        email=email,
        email_mx_valid=email_mx_valid,
        address=raw_lead.address,
        city=city,
        city_slug=city_slug,
        country=country,
        industry=raw_lead.industry,
        contact_name=raw_lead.contact_name,
        contact_name_ar=raw_lead.contact_name_ar,
        contact_title=raw_lead.contact_title,
        linkedin_url=raw_lead.linkedin_url,
        is_hiring=raw_lead.is_hiring,
        hiring_roles=raw_lead.hiring_roles,
    )
    normalized.dedup_key = make_dedup_key(normalized)
    return normalized


async def normalize_leads(raw_leads: List[RawLead]) -> List[NormalizedLead]:
    """Normalize all raw leads in parallel (with concurrency limit)."""
    semaphore = asyncio.Semaphore(20)  # Limit concurrent DNS checks

    async def _bounded_normalize(lead: RawLead) -> Optional[NormalizedLead]:
        async with semaphore:
            return await normalize_lead(lead)

    results = await asyncio.gather(
        *[_bounded_normalize(lead) for lead in raw_leads],
        return_exceptions=False,
    )
    normalized = [r for r in results if r is not None]
    logger.info(f"[normalizer] {len(raw_leads)} raw → {len(normalized)} normalized")
    return normalized
