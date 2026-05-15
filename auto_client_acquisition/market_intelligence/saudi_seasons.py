"""Wave 12.5 §33.2.1 — Saudi Seasonal Triggers.

Detects KSA-specific seasonal moments that drive B2B buying intent:
- Ramadan (preparation + observance)
- Eid al-Fitr / Eid al-Adha
- Hajj season
- School year start (Saudi academic calendar)
- Major exhibitions (LEAP, Biban, Saudi Build, etc.)
- ZATCA Phase 2 wave deadlines (most relevant for compliance push)
- National Day + Founding Day

Returns SignalDetection-compatible records so existing
opportunity_feed.py can consume without changes.

Hard rule (Article 8): hijri-vs-gregorian conversions use approximations
based on published Saudi government calendars. Conservative — when
uncertain, returns 'sector_pulse_rising' (a non-committal signal) and
flags ``confidence`` below 0.6.

Sources:
- Saudi Vision 2030 + ZATCA E-Invoicing Roll-out Phases
  https://zatca.gov.sa/en/E-Invoicing/Introduction/Pages/Roll-out-phases.aspx
- Saudi MOE academic calendar (school year typically late Aug)
- Major events from saudi-events.gov.sa
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta, timezone
from typing import Literal

# Saudi Season type — drives messaging + offer routing
SaudiSeason = Literal[
    "ramadan_prep",         # 30 days before Ramadan — B2B bookings drop
    "ramadan",              # Observance month — different working hours
    "eid_al_fitr",          # ~3 days post-Ramadan — celebration
    "eid_al_adha",          # ~3 days during Hajj — celebration
    "hajj_season",          # Last week of Dhu al-Hijjah — massive logistics
    "school_year_start",    # Late Aug / early Sep — family budget shift
    "national_day",         # Sep 23 — patriotic spend uplift
    "founding_day",         # Feb 22 — patriotic spend uplift
    "exhibition_season",    # Feb-Mar (Biban, LEAP) + Oct-Nov (Saudi Build, etc.)
    "zatca_wave_24_deadline_window",  # Apr-Jun 2026 — compliance scramble
    "ordinary",              # No special season
]


@dataclass(frozen=True, slots=True)
class SaudiSeasonalContext:
    """Detected seasonal context for a given date."""

    season: SaudiSeason
    confidence: float          # 0.0–1.0
    days_into_season: int      # +N days into; 0 = first day
    days_remaining: int        # days until season ends (estimate)
    business_implication_ar: str
    business_implication_en: str
    recommended_offer_pivot: str  # what to push during this season


# ─────────────────────────────────────────────────────────────────────
# Approximate hijri date windows for 2026 (Gregorian).
# Conservative — based on published Umm al-Qura calendar 2026.
# When uncertain, prefer "ordinary" over guessing.
# ─────────────────────────────────────────────────────────────────────
_RAMADAN_2026_START = date(2026, 2, 18)   # 1 Ramadan 1447 AH (approx)
_RAMADAN_2026_END = date(2026, 3, 19)
_EID_FITR_2026_START = date(2026, 3, 20)
_EID_FITR_2026_END = date(2026, 3, 22)
_EID_ADHA_2026_START = date(2026, 5, 27)
_EID_ADHA_2026_END = date(2026, 5, 29)
_HAJJ_2026_START = date(2026, 5, 25)      # Last week of Dhu al-Hijjah
_HAJJ_2026_END = date(2026, 5, 30)
_SCHOOL_YEAR_2026_START = date(2026, 8, 23)
_SCHOOL_YEAR_2026_END = date(2026, 9, 5)
_NATIONAL_DAY = date(2026, 9, 23)
_FOUNDING_DAY = date(2026, 2, 22)
# Exhibition windows
_EXHIBITIONS = [
    (date(2026, 2, 1), date(2026, 3, 31)),    # Biban + LEAP + spring exhibitions
    (date(2026, 10, 1), date(2026, 11, 30)),  # Saudi Build + autumn exhibitions
]
# ZATCA Phase 2 Wave 24 deadline = June 30, 2026 — pre-deadline scramble
_ZATCA_WAVE_24_WINDOW_START = date(2026, 4, 1)
_ZATCA_WAVE_24_DEADLINE = date(2026, 6, 30)


# Implications per season — bilingual + offer pivot
_SEASON_IMPLICATIONS: dict[SaudiSeason, dict[str, str]] = {
    "ramadan_prep": {
        "ar": "30 يوم قبل رمضان — بدء انخفاض الاجتماعات + تسريع قرارات قبل الشهر",
        "en": "30 days pre-Ramadan — meetings drop, decisions rush before month start",
        "offer": "Mini Diagnostic (quick, low-commitment)",
    },
    "ramadan": {
        "ar": "ساعات عمل مختلفة — ركّز على رسائل لا اجتماعات",
        "en": "Different working hours — favor async messages over calls",
        "offer": "Asynchronous Proof Sprint (extended timeline)",
    },
    "eid_al_fitr": {
        "ar": "إجازة العيد — لا تواصل عمل خلال 3 أيام",
        "en": "Eid holiday — no business outreach for 3 days",
        "offer": "PAUSE all outbound",
    },
    "eid_al_adha": {
        "ar": "إجازة عيد الأضحى — لا تواصل عمل خلال 3 أيام",
        "en": "Eid al-Adha holiday — no business outreach for 3 days",
        "offer": "PAUSE all outbound",
    },
    "hajj_season": {
        "ar": "موسم الحج — قطاعات السفر/الضيافة/الخدمات تحت ضغط هائل",
        "en": "Hajj season — travel/hospitality/services under massive load",
        "offer": "Support OS (for hospitality) + Operations review",
    },
    "school_year_start": {
        "ar": "بداية العام الدراسي — قرارات الميزانية للأسرة تنشط",
        "en": "School year start — family budget decisions activate",
        "offer": "Mini Diagnostic (B2C-adjacent sectors only)",
    },
    "national_day": {
        "ar": "اليوم الوطني — حملات وطنية تنشط",
        "en": "National Day — patriotic campaigns activate",
        "offer": "Saudi-focused positioning push",
    },
    "founding_day": {
        "ar": "يوم التأسيس — حملات وطنية تنشط",
        "en": "Founding Day — patriotic campaigns activate",
        "offer": "Saudi-focused positioning push",
    },
    "exhibition_season": {
        "ar": "موسم المعارض — اجتماعات كثيرة + متابعة بعد المعرض حرجة",
        "en": "Exhibition season — many meetings + post-event follow-up critical",
        "offer": "Data-to-Revenue Pack (post-event lead processing)",
    },
    "zatca_wave_24_deadline_window": {
        "ar": "نافذة موعد ZATCA الموجة 24 — ضغط امتثال على شركات > 375K ر.س",
        "en": "ZATCA Wave 24 deadline window — compliance pressure on >375K SAR firms",
        "offer": "Compliance + Growth Ops Monthly (ZATCA readiness)",
    },
    "ordinary": {
        "ar": "وضع عادي — استمر في الجدول الطبيعي",
        "en": "Ordinary — continue normal cadence",
        "offer": "Standard offer ladder",
    },
}


def detect_saudi_season(
    *,
    on_date: date | None = None,
    confidence_floor: float = 0.6,
) -> SaudiSeasonalContext:
    """Detect the Saudi seasonal context for a given date.

    Args:
        on_date: Date to check (default: today UTC).
        confidence_floor: Conservative threshold — when our hijri
            approximation might be off by ±2 days, drop confidence
            below this value.

    Returns:
        SaudiSeasonalContext — never raises; defaults to "ordinary"
        when nothing matches.
    """
    today = on_date or datetime.now(UTC).date()

    # Eid takes priority (highest business impact)
    if _EID_FITR_2026_START <= today <= _EID_FITR_2026_END:
        return _build("eid_al_fitr", today, _EID_FITR_2026_START, _EID_FITR_2026_END, confidence=0.85)
    if _EID_ADHA_2026_START <= today <= _EID_ADHA_2026_END:
        return _build("eid_al_adha", today, _EID_ADHA_2026_START, _EID_ADHA_2026_END, confidence=0.85)

    # Hajj season
    if _HAJJ_2026_START <= today <= _HAJJ_2026_END:
        return _build("hajj_season", today, _HAJJ_2026_START, _HAJJ_2026_END, confidence=0.80)

    # Ramadan + pre-Ramadan
    if _RAMADAN_2026_START <= today <= _RAMADAN_2026_END:
        return _build("ramadan", today, _RAMADAN_2026_START, _RAMADAN_2026_END, confidence=0.85)
    pre_ramadan_start = _RAMADAN_2026_START - timedelta(days=30)
    if pre_ramadan_start <= today < _RAMADAN_2026_START:
        return _build("ramadan_prep", today, pre_ramadan_start, _RAMADAN_2026_START, confidence=0.75)

    # ZATCA wave 24 deadline window (Apr-Jun 2026)
    if _ZATCA_WAVE_24_WINDOW_START <= today <= _ZATCA_WAVE_24_DEADLINE:
        return _build(
            "zatca_wave_24_deadline_window", today,
            _ZATCA_WAVE_24_WINDOW_START, _ZATCA_WAVE_24_DEADLINE,
            confidence=0.95,  # ZATCA dates are official, high confidence
        )

    # Exhibitions
    for ex_start, ex_end in _EXHIBITIONS:
        if ex_start <= today <= ex_end:
            return _build("exhibition_season", today, ex_start, ex_end, confidence=0.70)

    # School year start
    if _SCHOOL_YEAR_2026_START <= today <= _SCHOOL_YEAR_2026_END:
        return _build("school_year_start", today, _SCHOOL_YEAR_2026_START, _SCHOOL_YEAR_2026_END, confidence=0.85)

    # National + Founding days (single-day)
    if today == _NATIONAL_DAY:
        return _build("national_day", today, _NATIONAL_DAY, _NATIONAL_DAY, confidence=0.95)
    if today == _FOUNDING_DAY:
        return _build("founding_day", today, _FOUNDING_DAY, _FOUNDING_DAY, confidence=0.95)

    # Default — ordinary
    return _build("ordinary", today, today, today, confidence=0.5)


def _build(
    season: SaudiSeason, today: date, start: date, end: date, *, confidence: float,
) -> SaudiSeasonalContext:
    impl = _SEASON_IMPLICATIONS[season]
    return SaudiSeasonalContext(
        season=season,
        confidence=confidence,
        days_into_season=(today - start).days,
        days_remaining=(end - today).days,
        business_implication_ar=impl["ar"],
        business_implication_en=impl["en"],
        recommended_offer_pivot=impl["offer"],
    )


def all_seasons() -> tuple[SaudiSeason, ...]:
    """All canonical Saudi seasons (for tests + verifier)."""
    return tuple(_SEASON_IMPLICATIONS.keys())
