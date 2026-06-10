"""Gulf phone number validation and formatting for all GCC countries."""

from __future__ import annotations

import re
from dataclasses import dataclass

# Country code to ISO country mapping
GULF_COUNTRY_CODES: dict[str, str] = {
    "+966": "SA",
    "+971": "AE",
    "+974": "QA",
    "+965": "KW",
    "+973": "BH",
    "+968": "OM",
}

# Country information
GULF_COUNTRIES: dict[str, dict[str, str | int]] = {
    "SA": {
        "name_ar": "المملكة العربية السعودية",
        "name_en": "Saudi Arabia",
        "code": "+966",
        "min_length": 9,
        "max_length": 9,
    },
    "AE": {
        "name_ar": "الإمارات العربية المتحدة",
        "name_en": "United Arab Emirates",
        "code": "+971",
        "min_length": 9,
        "max_length": 9,
    },
    "QA": {
        "name_ar": "قطر",
        "name_en": "Qatar",
        "code": "+974",
        "min_length": 8,
        "max_length": 8,
    },
    "KW": {
        "name_ar": "الكويت",
        "name_en": "Kuwait",
        "code": "+965",
        "min_length": 8,
        "max_length": 8,
    },
    "BH": {
        "name_ar": "البحرين",
        "name_en": "Bahrain",
        "code": "+973",
        "min_length": 8,
        "max_length": 8,
    },
    "OM": {
        "name_ar": "عمان",
        "name_en": "Oman",
        "code": "+968",
        "min_length": 8,
        "max_length": 8,
    },
}

# Mobile prefixes per country
MOBILE_PREFIXES: dict[str, list[str]] = {
    "SA": ["050", "053", "054", "055", "056", "057", "058", "059"],
    "AE": ["050", "052", "054", "055", "056", "058"],
    "QA": ["33", "50", "55", "66", "77"],
    "KW": ["50", "51", "52", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "69"],
    "BH": ["33", "34", "35", "36", "37", "38", "39", "66", "663"],
    "OM": ["71", "72", "74", "77", "78", "79", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99"],
}


@dataclass
class PhoneValidation:
    """Gulf phone number validation result."""
    phone: str
    is_valid: bool
    country: str = ""
    country_code: str = ""
    national_number: str = ""
    is_mobile: bool = False
    is_saudi: bool = False
    carrier: str = ""
    formatted_international: str = ""
    errors: list[str] = list()

    def format_whatsapp(self) -> str:
        """Format number for WhatsApp (no + prefix)."""
        return self.formatted_international.replace("+", "")


def _clean_phone(phone: str) -> str:
    """Remove all non-digit characters except leading +."""
    phone = phone.strip()
    if phone.startswith("+"):
        return "+" + re.sub(r"\D", "", phone[1:])
    return re.sub(r"\D", "", phone)


def _get_carrier_sa(prefix: str) -> str:
    """Identify Saudi mobile carrier from prefix."""
    carriers = {
        "050": "STC", "053": "STC", "055": "STC",
        "054": "Mobily", "056": "Mobily",
        "057": "Zain", "058": "Zain", "059": "Zain",
        "051": "Virgin Mobile",
    }
    return carriers.get(prefix, "Unknown")


def validate_gulf_phone(phone: str) -> PhoneValidation:
    """Validate a phone number from any Gulf country.

    Args:
        phone: Phone number (with or without country code).

    Returns:
        PhoneValidation with status and details.
    """
    original = phone.strip()

    # Check if number already has a Gulf country code
    country_code = ""
    national = _clean_phone(phone)

    # Try to detect country code
    for code, iso in sorted(GULF_COUNTRY_CODES.items(), key=lambda x: -len(x[0])):
        if national.startswith(code.replace("+", "")):
            country_code = code
            national = national[len(code.replace("+", "")):]
            break
        # Also try with +
        if national.startswith(code):
            national = national[len(code):]
            country_code = code
            break

    if not country_code:
        # Try to guess from length
        for iso, info in GULF_COUNTRIES.items():
            min_l = int(info["min_length"])
            max_l = int(info["max_length"])
            if min_l <= len(national) <= max_l:
                country_code = str(info["code"])
                break

        if not country_code:
            return PhoneValidation(
                phone=original,
                is_valid=False,
                errors=["لا يمكن تحديد الدولة — أضف مفتاح الدولة"],
            )

    country_iso = GULF_COUNTRY_CODES.get(country_code, "")
    country_info = GULF_COUNTRIES.get(country_iso)

    if not country_info:
        return PhoneValidation(
            phone=original,
            is_valid=False,
            errors=["مفتاح الدولة غير معروف"],
        )

    min_len = int(country_info["min_length"])
    max_len = int(country_info["max_length"])

    if len(national) < min_len or len(national) > max_len:
        return PhoneValidation(
            phone=original,
            is_valid=False,
            country=country_iso,
            country_code=country_code,
            national_number=national,
            errors=[
                f"يجب أن يكون طول الرقم بين {min_len} و {max_len} أرقام"
            ],
        )

    # Check if mobile
    is_mobile = False
    carrier = ""
    prefixes = MOBILE_PREFIXES.get(country_iso, [])
    for prefix in prefixes:
        if national.startswith(prefix):
            is_mobile = True
            if country_iso == "SA":
                carrier = _get_carrier_sa(prefix)
            break

    formatted_international = f"{country_code}{national}"

    return PhoneValidation(
        phone=original,
        is_valid=True,
        country=country_iso,
        country_code=country_code,
        national_number=national,
        is_mobile=is_mobile,
        is_saudi=(country_iso == "SA"),
        carrier=carrier,
        formatted_international=formatted_international,
    )


def is_gulf_phone(phone: str) -> bool:
    """Quick check if a phone number is from the Gulf region."""
    result = validate_gulf_phone(phone)
    return result.is_valid


def get_country_from_phone(phone: str) -> str | None:
    """Get the ISO country code from a phone number."""
    result = validate_gulf_phone(phone)
    return result.country if result.is_valid else None


def validate_saudi_phone(phone: str) -> PhoneValidation:
    """Validate a Saudi phone number specifically.

    Saudi numbers: +966 5X XXX XXXX (9 digits after code)
    """
    result = validate_gulf_phone(phone)
    if result.is_valid and not result.is_saudi:
        result.is_valid = False
        result.errors.append("الرقم ليس رقماً سعودياً")
    return result


__all__ = [
    "GULF_COUNTRY_CODES",
    "GULF_COUNTRIES",
    "MOBILE_PREFIXES",
    "PhoneValidation",
    "get_country_from_phone",
    "is_gulf_phone",
    "validate_gulf_phone",
    "validate_saudi_phone",
]
