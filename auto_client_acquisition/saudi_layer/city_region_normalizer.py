"""Expanded city/region normalizer — 46+ cities across all 13 Saudi regions."""

from __future__ import annotations

from typing import Any

SAUDI_REGIONS: dict[str, dict[str, Any]] = {
    "riyadh": {
        "name_ar": "منطقة الرياض",
        "name_en": "Riyadh Region",
        "cities": [
            {"name_ar": "الرياض", "name_en": "Riyadh", "lat": 24.7136, "lng": 46.6753, "postal_prefix": "11"},
            {"name_ar": "الخرج", "name_en": "Al Kharj", "lat": 24.1554, "lng": 47.3121, "postal_prefix": "11"},
            {"name_ar": "المجمعة", "name_en": "Al Majma'ah", "lat": 25.9021, "lng": 45.3452, "postal_prefix": "15"},
            {"name_ar": "الدوادمي", "name_en": "Al Dawadmi", "lat": 24.4883, "lng": 44.3929, "postal_prefix": "11"},
            {"name_ar": "الزلفي", "name_en": "Az Zulfi", "lat": 26.2995, "lng": 44.8154, "postal_prefix": "15"},
            {"name_ar": "شقراء", "name_en": "Shaqra", "lat": 25.2481, "lng": 45.2519, "postal_prefix": "11"},
            {"name_ar": "حوطة بني تميم", "name_en": "Hotat Bani Tamim", "lat": 23.5271, "lng": 46.7864, "postal_prefix": "11"},
            {"name_ar": "القويعية", "name_en": "Al Quway'iyah", "lat": 24.0737, "lng": 45.2823, "postal_prefix": "11"},
            {"name_ar": "عفيف", "name_en": "Afif", "lat": 23.9074, "lng": 42.9172, "postal_prefix": "11"},
        ],
    },
    "makkah": {
        "name_ar": "منطقة مكة المكرمة",
        "name_en": "Makkah Region",
        "cities": [
            {"name_ar": "مكة المكرمة", "name_en": "Makkah", "lat": 21.3891, "lng": 39.8579, "postal_prefix": "24"},
            {"name_ar": "جدة", "name_en": "Jeddah", "lat": 21.5433, "lng": 39.1728, "postal_prefix": "23"},
            {"name_ar": "الطائف", "name_en": "Taif", "lat": 21.4370, "lng": 40.5103, "postal_prefix": "26"},
            {"name_ar": "القنفذة", "name_en": "Al Qunfudhah", "lat": 19.1262, "lng": 41.0789, "postal_prefix": "26"},
            {"name_ar": "الليث", "name_en": "Al Lith", "lat": 20.1497, "lng": 40.2741, "postal_prefix": "24"},
            {"name_ar": "رابغ", "name_en": "Rabigh", "lat": 22.7986, "lng": 39.0353, "postal_prefix": "24"},
            {"name_ar": "بحرة", "name_en": "Bahra", "lat": 21.3833, "lng": 39.4500, "postal_prefix": "24"},
            {"name_ar": "الجموم", "name_en": "Al Jumum", "lat": 21.6167, "lng": 39.7000, "postal_prefix": "24"},
        ],
    },
    "eastern": {
        "name_ar": "المنطقة الشرقية",
        "name_en": "Eastern Region",
        "cities": [
            {"name_ar": "الدمام", "name_en": "Dammam", "lat": 26.4207, "lng": 50.0888, "postal_prefix": "31"},
            {"name_ar": "الخبر", "name_en": "Al Khobar", "lat": 26.2792, "lng": 50.2083, "postal_prefix": "31"},
            {"name_ar": "الظهران", "name_en": "Dhahran", "lat": 26.2644, "lng": 50.1518, "postal_prefix": "31"},
            {"name_ar": "الأحساء", "name_en": "Al Ahsa", "lat": 25.3577, "lng": 49.5988, "postal_prefix": "31"},
            {"name_ar": "حفر الباطن", "name_en": "Hafar Al Batin", "lat": 28.4340, "lng": 45.9591, "postal_prefix": "31"},
            {"name_ar": "الجبيل", "name_en": "Jubail", "lat": 27.0046, "lng": 49.6460, "postal_prefix": "31"},
            {"name_ar": "القطيف", "name_en": "Al Qatif", "lat": 26.5573, "lng": 50.0026, "postal_prefix": "31"},
            {"name_ar": "رأس تنورة", "name_en": "Ras Tanura", "lat": 26.6438, "lng": 50.1574, "postal_prefix": "31"},
            {"name_ar": "النعيرية", "name_en": "Al Nairyah", "lat": 27.4761, "lng": 48.3687, "postal_prefix": "31"},
        ],
    },
    "madinah": {
        "name_ar": "منطقة المدينة المنورة",
        "name_en": "Madinah Region",
        "cities": [
            {"name_ar": "المدينة المنورة", "name_en": "Madinah", "lat": 24.4672, "lng": 39.6112, "postal_prefix": "42"},
            {"name_ar": "ينبع", "name_en": "Yanbu", "lat": 24.0898, "lng": 38.0633, "postal_prefix": "42"},
            {"name_ar": "العلا", "name_en": "Al Ula", "lat": 26.6085, "lng": 37.9262, "postal_prefix": "42"},
            {"name_ar": "بدر", "name_en": "Badr", "lat": 23.7802, "lng": 38.7903, "postal_prefix": "42"},
            {"name_ar": "المهد", "name_en": "Al Mahd", "lat": 23.3553, "lng": 40.2901, "postal_prefix": "42"},
            {"name_ar": "الحناكية", "name_en": "Al Hanakiyah", "lat": 24.8833, "lng": 40.5000, "postal_prefix": "42"},
        ],
    },
    "qassim": {
        "name_ar": "منطقة القصيم",
        "name_en": "Qassim Region",
        "cities": [
            {"name_ar": "بريدة", "name_en": "Buraydah", "lat": 26.3592, "lng": 43.9805, "postal_prefix": "51"},
            {"name_ar": "عنيزة", "name_en": "Unaizah", "lat": 26.0843, "lng": 43.9932, "postal_prefix": "51"},
            {"name_ar": "الرس", "name_en": "Ar Rass", "lat": 25.8666, "lng": 43.4978, "postal_prefix": "51"},
            {"name_ar": "المذنب", "name_en": "Al Mithnab", "lat": 26.1833, "lng": 43.9500, "postal_prefix": "51"},
            {"name_ar": "البكيرية", "name_en": "Al Bukayriyah", "lat": 26.1536, "lng": 43.6603, "postal_prefix": "51"},
            {"name_ar": "رياض الخبراء", "name_en": "Riyad Al Khabra", "lat": 26.0667, "lng": 43.4833, "postal_prefix": "51"},
        ],
    },
    "asir": {
        "name_ar": "منطقة عسير",
        "name_en": "Asir Region",
        "cities": [
            {"name_ar": "أبها", "name_en": "Abha", "lat": 18.2164, "lng": 42.5051, "postal_prefix": "61"},
            {"name_ar": "خميس مشيط", "name_en": "Khamis Mushait", "lat": 18.3081, "lng": 42.7340, "postal_prefix": "61"},
            {"name_ar": "محايل", "name_en": "Muhayil", "lat": 18.5458, "lng": 42.0411, "postal_prefix": "61"},
            {"name_ar": "بيشة", "name_en": "Bisha", "lat": 20.0011, "lng": 42.6072, "postal_prefix": "61"},
            {"name_ar": "النماص", "name_en": "Al Namas", "lat": 19.1109, "lng": 42.1279, "postal_prefix": "61"},
            {"name_ar": "سراة عبيدة", "name_en": "Sarat Abidah", "lat": 18.7283, "lng": 42.9550, "postal_prefix": "61"},
        ],
    },
    "tabuk": {
        "name_ar": "منطقة تبوك",
        "name_en": "Tabuk Region",
        "cities": [
            {"name_ar": "تبوك", "name_en": "Tabuk", "lat": 28.3835, "lng": 36.5661, "postal_prefix": "71"},
            {"name_ar": "ضباء", "name_en": "Duba", "lat": 27.3453, "lng": 35.6937, "postal_prefix": "71"},
            {"name_ar": "الوجه", "name_en": "Al Wajh", "lat": 26.2455, "lng": 36.4523, "postal_prefix": "71"},
            {"name_ar": "تيماء", "name_en": "Tayma", "lat": 27.6253, "lng": 38.5099, "postal_prefix": "71"},
            {"name_ar": "أملج", "name_en": "Umluj", "lat": 25.0214, "lng": 37.2781, "postal_prefix": "71"},
        ],
    },
    "hail": {
        "name_ar": "منطقة حائل",
        "name_en": "Hail Region",
        "cities": [
            {"name_ar": "حائل", "name_en": "Hail", "lat": 27.5114, "lng": 41.7208, "postal_prefix": "81"},
            {"name_ar": "بقعاء", "name_en": "Baqaa", "lat": 28.0594, "lng": 42.1294, "postal_prefix": "81"},
            {"name_ar": "الغزالة", "name_en": "Al Ghazalah", "lat": 27.4167, "lng": 41.6833, "postal_prefix": "81"},
            {"name_ar": "الشنان", "name_en": "Al Shinan", "lat": 27.5833, "lng": 41.8000, "postal_prefix": "81"},
        ],
    },
    "northern_borders": {
        "name_ar": "منطقة الحدود الشمالية",
        "name_en": "Northern Borders Region",
        "cities": [
            {"name_ar": "عرعر", "name_en": "Arar", "lat": 30.9749, "lng": 41.0295, "postal_prefix": "91"},
            {"name_ar": "رفحاء", "name_en": "Rafha", "lat": 29.6194, "lng": 43.4896, "postal_prefix": "91"},
            {"name_ar": "طريف", "name_en": "Turaif", "lat": 31.6737, "lng": 38.7524, "postal_prefix": "91"},
        ],
    },
    "jazan": {
        "name_ar": "منطقة جازان",
        "name_en": "Jazan Region",
        "cities": [
            {"name_ar": "جازان", "name_en": "Jazan", "lat": 16.8892, "lng": 42.5611, "postal_prefix": "82"},
            {"name_ar": "صبياء", "name_en": "Sabya", "lat": 17.1485, "lng": 42.6300, "postal_prefix": "82"},
            {"name_ar": "أبو عريش", "name_en": "Abu Arish", "lat": 16.9687, "lng": 42.8325, "postal_prefix": "82"},
            {"name_ar": "بيش", "name_en": "Baysh", "lat": 17.3806, "lng": 42.6775, "postal_prefix": "82"},
            {"name_ar": "فرسان", "name_en": "Farasan", "lat": 16.7000, "lng": 42.1167, "postal_prefix": "82"},
            {"name_ar": "الداير", "name_en": "Al Dayir", "lat": 17.2333, "lng": 42.5833, "postal_prefix": "82"},
        ],
    },
    "najran": {
        "name_ar": "منطقة نجران",
        "name_en": "Najran Region",
        "cities": [
            {"name_ar": "نجران", "name_en": "Najran", "lat": 17.4912, "lng": 44.1305, "postal_prefix": "81"},
            {"name_ar": "شرورة", "name_en": "Sharurah", "lat": 17.4714, "lng": 47.1054, "postal_prefix": "81"},
            {"name_ar": "حبونا", "name_en": "Habuna", "lat": 17.8333, "lng": 44.1167, "postal_prefix": "81"},
            {"name_ar": "يدمه", "name_en": "Yadamah", "lat": 17.3500, "lng": 44.2500, "postal_prefix": "81"},
        ],
    },
    "baha": {
        "name_ar": "منطقة الباحة",
        "name_en": "Al Baha Region",
        "cities": [
            {"name_ar": "الباحة", "name_en": "Al Baha", "lat": 20.0126, "lng": 41.4677, "postal_prefix": "65"},
            {"name_ar": "بلجرشي", "name_en": "Baljurashi", "lat": 19.8581, "lng": 41.5575, "postal_prefix": "65"},
            {"name_ar": "المندق", "name_en": "Al Mandaq", "lat": 20.1167, "lng": 41.2167, "postal_prefix": "65"},
            {"name_ar": "المخواة", "name_en": "Al Makhwah", "lat": 19.7833, "lng": 41.4500, "postal_prefix": "65"},
        ],
    },
    "jouf": {
        "name_ar": "منطقة الجوف",
        "name_en": "Al Jouf Region",
        "cities": [
            {"name_ar": "سكاكا", "name_en": "Sakaka", "lat": 29.9697, "lng": 40.2064, "postal_prefix": "72"},
            {"name_ar": "دومة الجندل", "name_en": "Dumat Al Jandal", "lat": 29.8118, "lng": 39.8640, "postal_prefix": "72"},
            {"name_ar": "الطوير", "name_en": "Al Tuwayr", "lat": 29.8833, "lng": 40.1000, "postal_prefix": "72"},
            {"name_ar": "صوير", "name_en": "Suwayr", "lat": 30.1167, "lng": 40.3833, "postal_prefix": "72"},
        ],
    },
}

# Alias map for fuzzy matching
_CITY_ALIASES: dict[str, str] = {
    # Riyadh region
    "riyadh": "riyadh",
    "الرياض": "riyadh",
    "al khafj": "al kharj",
    "الخرج": "al kharj",
    "majmaah": "al majma'ah",
    "majma": "al majma'ah",
    "المجمعة": "al majma'ah",
    "dawadmi": "al dawadmi",
    "الدوادمي": "al dawadmi",
    "zulfi": "az zulfi",
    "الزلفي": "az zulfi",
    "shaqra": "shaqra",
    "شقراء": "shaqra",
    # Makkah
    "makkah": "makkah",
    "mecca": "makkah",
    "مكة": "makkah",
    "مكة المكرمة": "makkah",
    "jeddah": "jeddah",
    "جدة": "jeddah",
    "taif": "taif",
    "الطائف": "taif",
    "qunfudhah": "al qunfudhah",
    "القنفذة": "al qunfudhah",
    # Eastern
    "dammam": "dammam",
    "الدمام": "dammam",
    "khobar": "al khobar",
    "الخبر": "al khobar",
    "dhahran": "dhahran",
    "الظهران": "dhahran",
    "ahsa": "al ahsa",
    "الاحساء": "al ahsa",
    "الأحساء": "al ahsa",
    "hafr albatin": "hafar al batin",
    "حفر الباطن": "hafar al batin",
    "jubail": "jubail",
    "الجبيل": "jubail",
    # Madinah
    "madinah": "madinah",
    "medina": "madinah",
    "المدينة": "madinah",
    "المدينة المنورة": "madinah",
    "yanbu": "yanbu",
    "ينبع": "yanbu",
    "al ula": "al ula",
    "العلا": "al ula",
    # Qassim
    "buraydah": "buraydah",
    "بريدة": "buraydah",
    "unaizah": "unaizah",
    "عنيزة": "unaizah",
    # Asir
    "abha": "abha",
    "أبها": "abha",
    "khamis mushait": "khamis mushait",
    "خميس مشيط": "khamis mushait",
    # Tabuk
    "tabuk": "tabuk",
    "تبوك": "tabuk",
    # Hail
    "hail": "hail",
    "حائل": "hail",
    # Northern borders
    "arar": "arar",
    "عرعر": "arar",
    "rafha": "rafha",
    "رفحاء": "rafha",
    # Jazan
    "jazan": "jazan",
    "جازان": "jazan",
    # Najran
    "najran": "najran",
    "نجران": "najran",
    # Baha
    "albaha": "al baha",
    "baha": "al baha",
    "الباحة": "al baha",
    # Jouf
    "sakaka": "sakaka",
    "سكاكا": "sakaka",
    "dumat al jandal": "dumat al jandal",
    "دومة الجندل": "dumat al jandal",
}


def get_all_cities() -> list[dict[str, Any]]:
    """Return a flat list of all cities with region info."""
    cities: list[dict[str, Any]] = []
    for region_key, region_data in SAUDI_REGIONS.items():
        for city in region_data["cities"]:
            cities.append({
                **city,
                "region_key": region_key,
                "region_ar": region_data["name_ar"],
                "region_en": region_data["name_en"],
            })
    return cities


def get_region_for_city(city_name: str) -> str | None:
    """Return the region key for a given city (Arabic or English name)."""
    normalized = normalize_city_name(city_name)
    for region_key, region_data in SAUDI_REGIONS.items():
        for city in region_data["cities"]:
            if city["name_en"].lower() == normalized or city["name_ar"] == city_name.strip():
                return region_key
    return None


def get_cities_in_region(region: str) -> list[dict[str, Any]]:
    """Return all cities for a given region key."""
    region_data = SAUDI_REGIONS.get(region.strip().lower())
    if region_data is None:
        return []
    return list(region_data["cities"])


def is_valid_city(city_name: str) -> bool:
    """Check if a city name exists in the taxonomy."""
    normalized = normalize_city_name(city_name)
    if not normalized:
        return False
    for region_data in SAUDI_REGIONS.values():
        for city in region_data["cities"]:
            if city["name_en"].lower() == normalized:
                return True
    return False


def normalize_city_name(name: str) -> str:
    """Normalize a city name to lowercase English slug."""
    s = name.strip().lower()
    if s in _CITY_ALIASES:
        return _CITY_ALIASES[s]
    # Check if it's an Arabic name directly
    for region_data in SAUDI_REGIONS.values():
        for city in region_data["cities"]:
            if city["name_ar"] == name.strip():
                return city["name_en"].lower()
    return s


def get_city_coordinates(city_name: str) -> tuple[float, float] | None:
    """Return (lat, lng) for a city if found."""
    normalized = normalize_city_name(city_name)
    for region_data in SAUDI_REGIONS.values():
        for city in region_data["cities"]:
            if city["name_en"].lower() == normalized:
                return (city["lat"], city["lng"])
    return None


def get_all_region_names_ar() -> list[str]:
    return [r["name_ar"] for r in SAUDI_REGIONS.values()]


def get_all_region_names_en() -> list[str]:
    return [r["name_en"] for r in SAUDI_REGIONS.values()]


__all__ = [
    "SAUDI_REGIONS",
    "get_all_cities",
    "get_all_region_names_ar",
    "get_all_region_names_en",
    "get_cities_in_region",
    "get_city_coordinates",
    "get_region_for_city",
    "is_valid_city",
    "normalize_city_name",
]
