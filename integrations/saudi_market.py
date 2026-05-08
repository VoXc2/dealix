"""
Saudi Arabia market context — constants, helpers, and calendar utilities.
سياق السوق السعودي — الثوابت والمساعدات وأدوات التقويم.

Additions (Saudi-specific compliance):
  - Hijri calendar conversion and display (via ummalqura when available)
  - Prayer time windows for Riyadh (scheduling blackout)
  - Ramadan mode detection and adjusted outreach cadence
  - Saudi public holidays (National Day, Founding Day, Eid windows)
  - Business day calculation (Sun–Thu, excl. Saudi holidays)
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from typing import NamedTuple

# ── Hijri calendar (ummalqura) ─────────────────────────────────────────────
# The ummalqura library provides accurate Hijri date conversion for KSA.
# Falls back to a simplified Gregorian-to-Hijri estimate if not installed.
try:
    from ummalqura.hijri_date import HijriDate as _UmmalquraHijriDate  # type: ignore[import-untyped]
    _UMMALQURA_AVAILABLE = True
except ImportError:
    _UMMALQURA_AVAILABLE = False


# ── Constants ──────────────────────────────────────────────────────────────

KSA_TIMEZONE = "Asia/Riyadh"          # UTC+3 (no DST)
KSA_UTC_OFFSET_HOURS = 3

# Saudi work week: Sunday–Thursday (Friday–Saturday = weekend)
KSA_WORKDAYS: set[int] = {6, 0, 1, 2, 3}  # weekday() 6=Sun, 0=Mon, 1=Tue, 2=Wed, 3=Thu

GCC_COUNTRIES: list[str] = [
    "Saudi Arabia",
    "UAE",
    "Kuwait",
    "Bahrain",
    "Qatar",
    "Oman",
]

VISION_2030_PROGRAMS: list[str] = [
    "National Transformation Program",
    "Housing Program",
    "Quality of Life Program",
    "Public Investment Fund Program",
    "Financial Sector Development Program",
    "Human Capability Development Program",
    "Digital Transformation Program",
    "Health Sector Transformation Program",
    "National Industrial Development and Logistics Program (NIDLP)",
    "Privatization Program",
]

SAUDI_REGULATORS: dict[str, str] = {
    "SAMA": "Central Bank — banking & fintech",
    "CMA": "Capital Market Authority",
    "MOH": "Ministry of Health",
    "SCFHS": "Saudi Commission for Health Specialties",
    "CCHI": "Council of Cooperative Health Insurance",
    "MoCI": "Ministry of Commerce",
    "MoE": "Ministry of Education",
    "SDAIA": "Saudi Data and AI Authority",
    "NCA": "National Cybersecurity Authority",
    "REGA": "Real Estate General Authority",
    "STA": "Saudi Tourism Authority",
    "MoMRA": "Ministry of Municipal and Rural Affairs",
    "MODON": "Saudi Industrial Property Authority",
    "SASO": "Saudi Standards Authority",
    "ZATCA": "Zakat, Tax and Customs Authority",
}

# ── Prayer Time Windows (approximate for Riyadh) ──────────────────────────
# Prayer blackout windows (start_offset_min, duration_min) relative to
# Fajr/Dhuhr/Asr/Maghrib/Isha — +/- 15 minutes around each prayer.
PRAYER_BLACKOUT_MINUTES = 15

# Riyadh coordinates for prayer time calculation
RIYADH_LATITUDE = 24.7136
RIYADH_LONGITUDE = 46.6753
RIYADH_ELEVATION = 612  # meters above sea level

# ── Saudi Holidays ──────────────────────────────────────────────────────────

@dataclass(frozen=True)
class SaudiHoliday:
    """Major Saudi public holidays (approximate, Gregorian)."""

    name_ar: str
    name_en: str
    month: int
    day: int


STATIC_HOLIDAYS: list[SaudiHoliday] = [
    SaudiHoliday("اليوم الوطني", "Saudi National Day", 9, 23),
    SaudiHoliday("يوم التأسيس", "Founding Day", 2, 22),
]

# Eid windows are approximate (vary by moon sighting ±1 day)
# Eid Al-Fitr ≈ end of Ramadan, Eid Al-Adha ≈ 70 days after Eid Al-Fitr
# These Gregorian estimates are for 2024–2026; update annually.
EID_WINDOWS_GREGORIAN: list[tuple[date, date, str]] = [
    (date(2024, 4, 8), date(2024, 4, 13), "Eid Al-Fitr 2024"),
    (date(2024, 6, 15), date(2024, 6, 19), "Eid Al-Adha 2024"),
    (date(2025, 3, 29), date(2025, 4, 3), "Eid Al-Fitr 2025"),
    (date(2025, 6, 5), date(2025, 6, 10), "Eid Al-Adha 2025"),
    (date(2026, 3, 19), date(2026, 3, 24), "Eid Al-Fitr 2026"),
    (date(2026, 5, 26), date(2026, 5, 31), "Eid Al-Adha 2026"),
]

# Ramadan windows (approximate, update annually)
RAMADAN_WINDOWS_GREGORIAN: list[tuple[date, date, str]] = [
    (date(2024, 3, 10), date(2024, 4, 8), "Ramadan 2024"),
    (date(2025, 3, 1), date(2025, 3, 30), "Ramadan 2025"),
    (date(2026, 2, 18), date(2026, 3, 19), "Ramadan 2026"),
]


# ── Hijri Calendar ─────────────────────────────────────────────────────────

@dataclass
class HijriDate:
    """Hijri (Islamic) calendar date."""

    year: int
    month: int
    day: int
    month_name_ar: str = ""
    month_name_en: str = ""

    MONTH_NAMES_AR = [
        "محرم", "صفر", "ربيع الأول", "ربيع الثاني",
        "جمادى الأولى", "جمادى الآخرة", "رجب", "شعبان",
        "رمضان", "شوال", "ذو القعدة", "ذو الحجة",
    ]
    MONTH_NAMES_EN = [
        "Muharram", "Safar", "Rabi' al-Awwal", "Rabi' al-Thani",
        "Jumada al-Awwal", "Jumada al-Thani", "Rajab", "Sha'ban",
        "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah",
    ]

    def __post_init__(self) -> None:
        if self.month_name_ar == "":
            self.month_name_ar = self.MONTH_NAMES_AR[self.month - 1]
        if self.month_name_en == "":
            self.month_name_en = self.MONTH_NAMES_EN[self.month - 1]

    def __str__(self) -> str:
        return f"{self.day} {self.month_name_ar} {self.year}هـ"

    def to_str_en(self) -> str:
        return f"{self.day} {self.month_name_en} {self.year} AH"

    @property
    def is_ramadan(self) -> bool:
        return self.month == 9

    @property
    def is_eid_al_fitr(self) -> bool:
        return self.month == 10 and self.day <= 3

    @property
    def is_eid_al_adha(self) -> bool:
        return self.month == 12 and 10 <= self.day <= 13


def gregorian_to_hijri(greg_date: date) -> HijriDate:
    """
    Convert a Gregorian date to Hijri.
    يحوّل تاريخاً ميلادياً إلى هجري.

    Uses ummalqura library if available (accurate KSA Um Al-Qura calendar);
    otherwise falls back to the standard astronomical algorithm.
    """
    if _UMMALQURA_AVAILABLE:
        try:
            h = _UmmalquraHijriDate(greg_date.year, greg_date.month, greg_date.day)
            return HijriDate(year=h.year, month=h.month, day=h.day)
        except Exception:
            pass
    return _gregorian_to_hijri_fallback(greg_date)


def _gregorian_to_hijri_fallback(greg_date: date) -> HijriDate:
    """
    Approximate Gregorian → Hijri conversion (Tabular Islamic Calendar).
    دقة ±1 يوم — استخدم ummalqura للدقة الكاملة.
    """
    # Julian day number
    y, m, d = greg_date.year, greg_date.month, greg_date.day
    jd = (
        367 * y
        - int(7 * (y + int((m + 9) / 12)) / 4)
        + int(275 * m / 9)
        + d
        + 1721013.5
    )
    # Convert JD to Hijri
    jd = jd - 0.5
    z = math.floor(jd + 0.5)
    a = math.floor((z - 1867216.25) / 36524.25)
    b = z + 1 + a - math.floor(a / 4)
    c = b + 1524
    dd = math.floor((c - 122.1) / 365.25)
    e = math.floor(365.25 * dd)
    f = math.floor((c - e) / 30.6001)
    # Hijri calculation via epoch
    # Muharram 1, 1 AH = July 16, 622 CE (Julian)
    l = z - 1948440 + 10632
    n = math.floor((l - 1) / 10631)
    l = l - 10631 * n + 354
    j = (math.floor((10985 - l) / 5316)) * (math.floor((50 * l) / 17719)) + (
        math.floor(l / 5670)
    ) * (math.floor((43 * l) / 15238))
    l = l - (math.floor((30 - j) / 15)) * (math.floor((17719 * j) / 50)) - (
        math.floor(j / 16)
    ) * (math.floor((15238 * j) / 43)) + 29
    month = math.floor((24 * l) / 709)
    day = l - math.floor((709 * month) / 24)
    year = 30 * n + j - 30
    return HijriDate(year=int(year), month=int(month), day=int(day))


def ksa_today_hijri() -> HijriDate:
    """Return today's Hijri date in KSA (UTC+3)."""
    ksa_now = datetime.now(timezone.utc) + timedelta(hours=KSA_UTC_OFFSET_HOURS)
    return gregorian_to_hijri(ksa_now.date())


# ── Prayer Times ───────────────────────────────────────────────────────────

class PrayerTimes(NamedTuple):
    """Prayer times for a given day and location."""

    fajr: time
    sunrise: time
    dhuhr: time
    asr: time
    maghrib: time
    isha: time
    date: date


def _hours_to_time(hours: float) -> time:
    """Convert decimal hours (e.g. 14.5 = 14:30) to time object."""
    hours = hours % 24
    h = int(hours)
    m = int((hours - h) * 60)
    s = int(((hours - h) * 60 - m) * 60)
    return time(h, m, s)


def _julian_day(d: date) -> float:
    """Calculate Julian Day Number for a date."""
    y, mo, day = d.year, d.month, d.day
    if mo <= 2:
        y -= 1
        mo += 12
    a = math.floor(y / 100)
    b = 2 - a + math.floor(a / 4)
    return math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (mo + 1)) + day + b - 1524.5


def calculate_prayer_times(
    calc_date: date,
    latitude: float = RIYADH_LATITUDE,
    longitude: float = RIYADH_LONGITUDE,
    elevation: float = RIYADH_ELEVATION,
    fajr_angle: float = 18.5,   # Muslim World League (used in KSA)
    isha_angle: float = 17.0,   # Muslim World League
) -> PrayerTimes:
    """
    Calculate Islamic prayer times using the Muslim World League method.
    حساب أوقات الصلاة بطريقة رابطة العالم الإسلامي المعتمدة في المملكة.

    Accurate to within ±5 minutes for Riyadh.
    For production use, consider an API like api.aladhan.com.
    """
    jd = _julian_day(calc_date)
    d = jd - 2451545.0  # Days since J2000

    # Solar coordinates
    g = 357.529 + 0.98560028 * d  # Mean anomaly (degrees)
    q = 280.459 + 0.98564736 * d  # Mean longitude (degrees)
    l = q + 1.915 * math.sin(math.radians(g)) + 0.020 * math.sin(math.radians(2 * g))
    e = 23.439 - 0.00000036 * d   # Obliquity

    ra = math.degrees(math.atan2(math.cos(math.radians(e)) * math.sin(math.radians(l)), math.cos(math.radians(l)))) / 15
    decl = math.degrees(math.asin(math.sin(math.radians(e)) * math.sin(math.radians(l))))
    eq_t = q / 15 - ra  # Equation of time (hours)

    # Transit (solar noon)
    transit_hours = 12 + (longitude / 15) - eq_t
    # Adjust for UTC+3
    transit_local = transit_hours - longitude / 15 + 3 + (longitude / 15) - eq_t
    # Simplified: dhuhr = 12 + eq_t offset + timezone correction
    dhuhr_ut = 12 - longitude / 15 - eq_t
    dhuhr_local = dhuhr_ut + KSA_UTC_OFFSET_HOURS

    def _hour_angle(angle: float, decl_deg: float, lat: float) -> float:
        """Hour angle for a solar altitude angle."""
        cos_val = (
            (-math.sin(math.radians(angle)) - math.sin(math.radians(lat)) * math.sin(math.radians(decl_deg)))
            / (math.cos(math.radians(lat)) * math.cos(math.radians(decl_deg)))
        )
        cos_val = max(-1.0, min(1.0, cos_val))
        return math.degrees(math.acos(cos_val)) / 15

    # Sunrise / Sunset
    sunrise_hours = dhuhr_local - _hour_angle(-0.8333, decl, latitude)
    sunset_hours = dhuhr_local + _hour_angle(-0.8333, decl, latitude)

    # Fajr / Isha (angle-based)
    fajr_hours = dhuhr_local - _hour_angle(-fajr_angle, decl, latitude)
    isha_hours = dhuhr_local + _hour_angle(-isha_angle, decl, latitude)

    # Asr (Shafi'i: shadow factor = 1; Hanafi: shadow factor = 2)
    shadow_factor = 1  # Shafi'i method (common in Saudi Arabia)
    asr_angle = math.degrees(math.atan(1 / (shadow_factor + math.tan(math.radians(abs(latitude - decl))))))
    asr_hours = dhuhr_local + _hour_angle(asr_angle, decl, latitude)

    # Maghrib (immediately after sunset, add ~3 minutes safety margin)
    maghrib_hours = sunset_hours + 0.05

    return PrayerTimes(
        fajr=_hours_to_time(fajr_hours),
        sunrise=_hours_to_time(sunrise_hours),
        dhuhr=_hours_to_time(dhuhr_local),
        asr=_hours_to_time(asr_hours),
        maghrib=_hours_to_time(maghrib_hours),
        isha=_hours_to_time(isha_hours),
        date=calc_date,
    )


def get_prayer_blackout_windows(calc_date: date) -> list[tuple[time, time, str]]:
    """
    Get prayer time blackout windows for outreach scheduling.
    يجلب نوافذ التوقف عن إرسال الرسائل خلال أوقات الصلاة.

    Returns list of (start_time, end_time, prayer_name) tuples.
    """
    pt = calculate_prayer_times(calc_date)
    blackout_min = PRAYER_BLACKOUT_MINUTES

    def _window(prayer_time: time, name: str) -> tuple[time, time, str]:
        dt_base = datetime.combine(calc_date, prayer_time)
        start = (dt_base - timedelta(minutes=blackout_min)).time()
        end = (dt_base + timedelta(minutes=blackout_min)).time()
        return (start, end, name)

    return [
        _window(pt.fajr, "Fajr / الفجر"),
        _window(pt.dhuhr, "Dhuhr / الظهر"),
        _window(pt.asr, "Asr / العصر"),
        _window(pt.maghrib, "Maghrib / المغرب"),
        _window(pt.isha, "Isha / العشاء"),
    ]


def is_prayer_time(check_datetime: datetime | None = None) -> tuple[bool, str]:
    """
    Check if the current KSA time falls within a prayer window.
    يتحقق إذا كان الوقت الحالي في نافذة وقت الصلاة.

    Returns (is_blackout: bool, prayer_name: str)
    """
    if check_datetime is None:
        ksa_now = datetime.now(timezone.utc) + timedelta(hours=KSA_UTC_OFFSET_HOURS)
    else:
        ksa_now = check_datetime + timedelta(hours=KSA_UTC_OFFSET_HOURS)

    current_time = ksa_now.time()
    current_date = ksa_now.date()
    windows = get_prayer_blackout_windows(current_date)

    for start, end, name in windows:
        if start <= current_time <= end:
            return True, name
    return False, ""


# ── Ramadan Mode ───────────────────────────────────────────────────────────

def is_ramadan(check_date: date | None = None) -> bool:
    """
    Check if a date falls within the Ramadan period.
    يتحقق إذا كان التاريخ يقع ضمن شهر رمضان المبارك.

    Uses Hijri calendar — month 9.
    """
    if check_date is None:
        ksa_now = datetime.now(timezone.utc) + timedelta(hours=KSA_UTC_OFFSET_HOURS)
        check_date = ksa_now.date()
    hijri = gregorian_to_hijri(check_date)
    return hijri.is_ramadan


def ramadan_adjusted_send_time(
    original_time: time,
    check_date: date | None = None,
) -> time:
    """
    Adjust outreach send time for Ramadan cadence.
    يضبط وقت إرسال الرسائل التسويقية خلال رمضان.

    Ramadan rules:
    - Prefer after Iftar (≈ 30 min after Maghrib) until 10pm
    - Avoid Suhoor time (3am–5am)
    - Morning slots: 9am–11am (pre-Dhuhr is acceptable)
    """
    if not is_ramadan(check_date):
        return original_time

    d = check_date or datetime.now(timezone.utc).date()
    pt = calculate_prayer_times(d)
    iftar_dt = datetime.combine(d, pt.maghrib) + timedelta(minutes=30)
    iftar_time = iftar_dt.time()

    # After iftar until 10pm → use iftar+30min slot
    end_evening = time(22, 0)
    if iftar_time <= original_time <= end_evening:
        return original_time  # already in valid window
    # Morning window 9am–11am
    if time(9, 0) <= original_time <= time(11, 0):
        return original_time
    # Default: post-iftar slot
    return iftar_time


@dataclass
class RamadanConfig:
    """
    Ramadan outreach configuration.
    إعدادات التواصل التسويقي خلال رمضان.
    """

    is_active: bool
    iftar_time: time | None = None
    suhoor_blackout_start: time = time(3, 0)
    suhoor_blackout_end: time = time(5, 30)
    preferred_morning_start: time = time(9, 0)
    preferred_morning_end: time = time(11, 30)
    preferred_evening_start: time | None = None  # set to iftar+30
    preferred_evening_end: time = time(22, 0)
    # Reduced cadence during Ramadan (more respectful)
    max_touches_per_week: int = 2  # vs. normal 4-5
    use_ramadan_templates: bool = True


def get_ramadan_config(check_date: date | None = None) -> RamadanConfig:
    """
    Get the Ramadan mode configuration for a given date.
    يجلب إعدادات وضع رمضان لتاريخ معين.
    """
    if check_date is None:
        ksa_now = datetime.now(timezone.utc) + timedelta(hours=KSA_UTC_OFFSET_HOURS)
        check_date = ksa_now.date()

    active = is_ramadan(check_date)
    if not active:
        return RamadanConfig(is_active=False)

    pt = calculate_prayer_times(check_date)
    iftar_dt = datetime.combine(check_date, pt.maghrib) + timedelta(minutes=30)
    return RamadanConfig(
        is_active=True,
        iftar_time=pt.maghrib,
        preferred_evening_start=iftar_dt.time(),
    )


# ── Saudi Holidays ─────────────────────────────────────────────────────────

def is_saudi_holiday(check_date: date | None = None) -> tuple[bool, str]:
    """
    Check if a date is a Saudi public holiday.
    يتحقق إذا كان التاريخ يوم عطلة رسمية سعودية.

    Returns (is_holiday: bool, holiday_name: str)
    """
    if check_date is None:
        ksa_now = datetime.now(timezone.utc) + timedelta(hours=KSA_UTC_OFFSET_HOURS)
        check_date = ksa_now.date()

    # Eid windows
    for start, end, name in EID_WINDOWS_GREGORIAN:
        if start <= check_date <= end:
            return True, name

    # Static holidays (National Day, Founding Day)
    for holiday in STATIC_HOLIDAYS:
        if check_date.month == holiday.month and check_date.day == holiday.day:
            return True, holiday.name_en

    return False, ""


def is_saudi_weekend(check_date: date | None = None) -> bool:
    """
    Check if a date is a Saudi weekend (Friday or Saturday).
    يتحقق إذا كان التاريخ يوم إجازة نهاية الأسبوع السعودية (الجمعة أو السبت).
    """
    if check_date is None:
        ksa_now = datetime.now(timezone.utc) + timedelta(hours=KSA_UTC_OFFSET_HOURS)
        check_date = ksa_now.date()
    return check_date.weekday() in (4, 5)  # 4=Friday, 5=Saturday


def is_saudi_business_day(check_date: date | None = None) -> bool:
    """
    Check if a date is a Saudi business day.
    يتحقق إذا كان التاريخ يوم عمل رسمياً في المملكة.

    Business days: Sunday–Thursday, excluding Saudi holidays.
    """
    if check_date is None:
        ksa_now = datetime.now(timezone.utc) + timedelta(hours=KSA_UTC_OFFSET_HOURS)
        check_date = ksa_now.date()
    if is_saudi_weekend(check_date):
        return False
    is_holiday, _ = is_saudi_holiday(check_date)
    return not is_holiday


def next_saudi_business_day(from_date: date | None = None) -> date:
    """
    Return the next Saudi business day after the given date.
    يُعيد يوم العمل السعودي التالي بعد التاريخ المحدد.
    """
    if from_date is None:
        ksa_now = datetime.now(timezone.utc) + timedelta(hours=KSA_UTC_OFFSET_HOURS)
        from_date = ksa_now.date()
    candidate = from_date + timedelta(days=1)
    while not is_saudi_business_day(candidate):
        candidate += timedelta(days=1)
    return candidate


def add_saudi_business_days(start_date: date, n_days: int) -> date:
    """
    Add n business days to a date (Saudi calendar).
    يضيف n يوم عمل إلى تاريخ (التقويم السعودي).
    """
    current = start_date
    added = 0
    while added < n_days:
        current += timedelta(days=1)
        if is_saudi_business_day(current):
            added += 1
    return current


def get_best_outreach_time(check_date: date | None = None) -> dict:
    """
    Get the best outreach time for a given date considering all Saudi factors.
    يجلب أفضل وقت للتواصل التسويقي مع مراعاة جميع العوامل السعودية.

    Returns a dict with recommended_time, is_valid, reason.
    """
    if check_date is None:
        ksa_now = datetime.now(timezone.utc) + timedelta(hours=KSA_UTC_OFFSET_HOURS)
        check_date = ksa_now.date()

    # Not a business day
    if not is_saudi_business_day(check_date):
        is_holiday, holiday_name = is_saudi_holiday(check_date)
        reason = holiday_name if is_holiday else "Saudi weekend (Fri–Sat)"
        return {
            "is_valid": False,
            "reason": f"Not a business day — {reason}",
            "recommended_time": None,
            "next_business_day": next_saudi_business_day(check_date).isoformat(),
        }

    ramadan_cfg = get_ramadan_config(check_date)
    prayer_times = calculate_prayer_times(check_date)

    if ramadan_cfg.is_active:
        # Post-Iftar slot
        iftar_slot = ramadan_cfg.preferred_evening_start or time(19, 0)
        return {
            "is_valid": True,
            "is_ramadan": True,
            "recommended_time": iftar_slot.strftime("%H:%M"),
            "morning_slot": "09:00–11:30",
            "evening_slot": f"{iftar_slot.strftime('%H:%M')}–22:00",
            "max_touches_per_week": ramadan_cfg.max_touches_per_week,
            "use_ramadan_templates": True,
            "reason": "Ramadan mode — reduced cadence, post-Iftar preferred",
        }

    return {
        "is_valid": True,
        "is_ramadan": False,
        "recommended_time": "10:00",
        "recommended_window": "09:00–11:30 or 13:30–16:00",
        "prayer_blackouts": [
            f"{w[0].strftime('%H:%M')}–{w[1].strftime('%H:%M')} ({w[2]})"
            for w in get_prayer_blackout_windows(check_date)
        ],
        "fajr": prayer_times.fajr.strftime("%H:%M"),
        "dhuhr": prayer_times.dhuhr.strftime("%H:%M"),
        "asr": prayer_times.asr.strftime("%H:%M"),
        "maghrib": prayer_times.maghrib.strftime("%H:%M"),
        "isha": prayer_times.isha.strftime("%H:%M"),
        "reason": "Normal business day",
    }


# ── GCC Helpers (preserved from v1) ───────────────────────────────────────

def is_gcc_country(country: str) -> bool:
    """Return True if country is in the GCC | هل الدولة من دول الخليج؟"""
    if not country:
        return False
    normalized = country.strip().lower()
    gcc_variants = {
        "saudi arabia", "sa", "ksa", "السعودية", "المملكة العربية السعودية",
        "uae", "ae", "الإمارات", "الامارات",
        "kuwait", "kw", "الكويت",
        "bahrain", "bh", "البحرين",
        "qatar", "qa", "قطر",
        "oman", "om", "عمان",
    }
    return normalized in gcc_variants


def region_tier(region: str | None) -> str:
    """Classify a region into our pricing tiers | صنّف المنطقة إلى طبقة سعرية."""
    if not region:
        return "global"
    lower = region.lower().strip()
    if any(t in lower for t in ("saudi", "ksa", "sa", "riyadh", "jeddah", "dammam", "السعودية")):
        return "saudi"
    if is_gcc_country(region):
        return "gcc"
    return "global"
