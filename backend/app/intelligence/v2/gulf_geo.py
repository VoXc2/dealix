"""
Gulf Geographic Constants — Dealix Lead Intelligence Engine V2
==============================================================
Saudi-first Gulf constants: cities, bounding boxes, phone prefixes, country TLDs.
All city names in English + Arabic. Bounding boxes are (lat_min, lon_min, lat_max, lon_max).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

# ─────────────────────────── Country Metadata ────────────────────────────────

@dataclass
class GulfCountry:
    code: str          # ISO 3166-1 alpha-2
    name_en: str
    name_ar: str
    phone_prefix: str  # E.164 country code
    tld: str           # country-code TLD
    bbox: Tuple[float, float, float, float]  # (lat_min, lon_min, lat_max, lon_max)


GULF_COUNTRIES: Dict[str, GulfCountry] = {
    "SA": GulfCountry(
        code="SA", name_en="Saudi Arabia", name_ar="المملكة العربية السعودية",
        phone_prefix="+966", tld=".sa",
        bbox=(16.3, 34.5, 32.2, 55.7),
    ),
    "UAE": GulfCountry(
        code="UAE", name_en="United Arab Emirates", name_ar="الإمارات العربية المتحدة",
        phone_prefix="+971", tld=".ae",
        bbox=(22.6, 51.5, 26.1, 56.4),
    ),
    "KW": GulfCountry(
        code="KW", name_en="Kuwait", name_ar="الكويت",
        phone_prefix="+965", tld=".kw",
        bbox=(28.5, 46.5, 30.1, 48.5),
    ),
    "QA": GulfCountry(
        code="QA", name_en="Qatar", name_ar="قطر",
        phone_prefix="+974", tld=".qa",
        bbox=(24.4, 50.7, 26.2, 51.7),
    ),
    "BH": GulfCountry(
        code="BH", name_en="Bahrain", name_ar="البحرين",
        phone_prefix="+973", tld=".bh",
        bbox=(25.5, 50.3, 26.4, 50.8),
    ),
    "OM": GulfCountry(
        code="OM", name_en="Oman", name_ar="عُمان",
        phone_prefix="+968", tld=".om",
        bbox=(16.6, 51.8, 26.4, 59.8),
    ),
}

# Convenience lookups
PHONE_PREFIX_TO_COUNTRY: Dict[str, str] = {c.phone_prefix: k for k, c in GULF_COUNTRIES.items()}
TLD_TO_COUNTRY: Dict[str, str] = {c.tld: k for k, c in GULF_COUNTRIES.items()}
COUNTRY_CODES = list(GULF_COUNTRIES.keys())

# ─────────────────────────── Saudi Cities ────────────────────────────────────

@dataclass
class SaudiCity:
    name_en: str
    name_ar: str
    region: str           # administrative region
    region_ar: str
    bbox: Tuple[float, float, float, float]  # (lat_min, lon_min, lat_max, lon_max)
    population_est: int   # rough estimate
    priority: int         # 1=highest lead density


SAUDI_CITIES: Dict[str, SaudiCity] = {
    "riyadh": SaudiCity(
        name_en="Riyadh", name_ar="الرياض",
        region="Riyadh Region", region_ar="منطقة الرياض",
        bbox=(24.45, 46.45, 24.90, 47.10), population_est=7_700_000, priority=1,
    ),
    "jeddah": SaudiCity(
        name_en="Jeddah", name_ar="جدة",
        region="Makkah Region", region_ar="منطقة مكة المكرمة",
        bbox=(21.27, 39.05, 21.72, 39.35), population_est=4_700_000, priority=1,
    ),
    "dammam": SaudiCity(
        name_en="Dammam", name_ar="الدمام",
        region="Eastern Province", region_ar="المنطقة الشرقية",
        bbox=(26.28, 49.92, 26.50, 50.20), population_est=1_200_000, priority=1,
    ),
    "makkah": SaudiCity(
        name_en="Makkah", name_ar="مكة المكرمة",
        region="Makkah Region", region_ar="منطقة مكة المكرمة",
        bbox=(21.32, 39.77, 21.52, 39.98), population_est=2_000_000, priority=2,
    ),
    "madinah": SaudiCity(
        name_en="Madinah", name_ar="المدينة المنورة",
        region="Madinah Region", region_ar="منطقة المدينة المنورة",
        bbox=(24.35, 39.50, 24.60, 39.75), population_est=1_300_000, priority=2,
    ),
    "khobar": SaudiCity(
        name_en="Al Khobar", name_ar="الخبر",
        region="Eastern Province", region_ar="المنطقة الشرقية",
        bbox=(26.20, 50.15, 26.35, 50.25), population_est=400_000, priority=2,
    ),
    "taif": SaudiCity(
        name_en="Taif", name_ar="الطائف",
        region="Makkah Region", region_ar="منطقة مكة المكرمة",
        bbox=(21.22, 40.35, 21.55, 40.60), population_est=700_000, priority=3,
    ),
    "buraydah": SaudiCity(
        name_en="Buraydah", name_ar="بريدة",
        region="Al Qassim Region", region_ar="منطقة القصيم",
        bbox=(26.27, 43.89, 26.45, 44.10), population_est=600_000, priority=3,
    ),
    "tabuk": SaudiCity(
        name_en="Tabuk", name_ar="تبوك",
        region="Tabuk Region", region_ar="منطقة تبوك",
        bbox=(28.33, 36.50, 28.55, 36.75), population_est=650_000, priority=3,
    ),
    "abha": SaudiCity(
        name_en="Abha", name_ar="أبها",
        region="Asir Region", region_ar="منطقة عسير",
        bbox=(18.18, 42.47, 18.35, 42.65), population_est=400_000, priority=3,
    ),
    "hail": SaudiCity(
        name_en="Hail", name_ar="حائل",
        region="Ha'il Region", region_ar="منطقة حائل",
        bbox=(27.48, 41.61, 27.65, 41.82), population_est=350_000, priority=3,
    ),
    "jubail": SaudiCity(
        name_en="Al Jubail", name_ar="الجبيل",
        region="Eastern Province", region_ar="المنطقة الشرقية",
        bbox=(27.00, 49.60, 27.10, 49.78), population_est=250_000, priority=2,
    ),
    "yanbu": SaudiCity(
        name_en="Yanbu", name_ar="ينبع",
        region="Madinah Region", region_ar="منطقة المدينة المنورة",
        bbox=(24.04, 38.00, 24.18, 38.10), population_est=300_000, priority=3,
    ),
}

# Priority-1 cities (highest commercial density)
PRIORITY_CITIES = [k for k, v in SAUDI_CITIES.items() if v.priority == 1]

# All city names for search (both languages)
ALL_CITY_NAMES_AR = [c.name_ar for c in SAUDI_CITIES.values()]
ALL_CITY_NAMES_EN = [c.name_en for c in SAUDI_CITIES.values()]

# ─────────────────────────── Search Helpers ──────────────────────────────────

def get_country_bbox(country_code: str) -> Tuple[float, float, float, float] | None:
    """Return bounding box for a Gulf country."""
    country = GULF_COUNTRIES.get(country_code.upper())
    return country.bbox if country else None


def get_city_bbox(city_slug: str) -> Tuple[float, float, float, float] | None:
    """Return bounding box for a Saudi city slug."""
    city = SAUDI_CITIES.get(city_slug.lower())
    return city.bbox if city else None


def normalize_city_name(name: str) -> str | None:
    """Map a city name (AR or EN) to its canonical slug."""
    name_lower = name.lower().strip()
    for slug, city in SAUDI_CITIES.items():
        if name_lower in (city.name_en.lower(), city.name_ar):
            return slug
    return None


def phone_prefix_for_country(country_code: str) -> str | None:
    c = GULF_COUNTRIES.get(country_code.upper())
    return c.phone_prefix if c else None


# ─────────────────────────── OSM Nominatim Params ────────────────────────────

NOMINATIM_COUNTRY_CODES: Dict[str, str] = {
    "SA": "sa", "UAE": "ae", "KW": "kw", "QA": "qa", "BH": "bh", "OM": "om",
}
