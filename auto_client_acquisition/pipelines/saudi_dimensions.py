"""Wave 12.5 §33.2.2 — Lead Intelligence v2: 6 Saudi-specific scoring dimensions.

Adds 6 dimensions on top of the existing 7-dim ``pipelines/scoring.py``
to bring total to 13. Pure functions — no LLM, no I/O, deterministic.

Article 11: doesn't mutate existing ``scoring.py``; new module composes
on top via ``compute_saudi_score_board()``. Existing callers unchanged.

The 6 new dimensions (per plan §33.2.2):
1. arabic_readiness_score      — does the lead's locale + name suggest Saudi/GCC?
2. decision_maker_access_score  — title hints + warm-route presence
3. whatsapp_dependency_risk    — sole-channel-on-WhatsApp risk
4. saudi_compliance_sensitivity — sector regulatory sensitivity
5. seasonality_score             — Saudi season alignment (Ramadan, Hajj, etc.)
6. relationship_strength_score   — warm intro / partner ref / inbound vs cold
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Any, Literal

from auto_client_acquisition.market_intelligence.saudi_seasons import (
    detect_saudi_season,
)


@dataclass(frozen=True, slots=True)
class SaudiScoreBoard:
    """6 Saudi-specific dimensions (each 0.0-1.0).

    Combined with existing 7-dim ScoreBreakdown to form the full
    13-dim Wave 12.5 §33.2.2 board.
    """

    arabic_readiness: float
    decision_maker_access: float
    whatsapp_dependency_risk: float
    saudi_compliance_sensitivity: float
    seasonality: float
    relationship_strength: float
    is_estimate: bool = True  # Article 8 — never claim certainty
    notes: tuple[str, ...] = ()


# ─────────────────────────────────────────────────────────────────────
# Individual dimension scorers (pure, deterministic)
# ─────────────────────────────────────────────────────────────────────


# Arabic alphabet pattern (basic + extended)
_ARABIC_RE = re.compile(r"[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]")
# Common Saudi cities + indicators
_SAUDI_CITIES = frozenset({
    "riyadh", "jeddah", "dammam", "khobar", "mecca", "medina", "makkah", "madinah",
    "tabuk", "abha", "taif", "buraidah", "jubail", "yanbu", "qatif", "hail",
    "الرياض", "جدة", "الدمام", "الخبر", "مكة", "المدينة", "تبوك",
    "أبها", "الطائف", "بريدة", "الجبيل", "ينبع", "القطيف", "حائل",
})
# Common Saudi country indicators
_SAUDI_COUNTRY = frozenset({"sa", "saudi arabia", "saudi", "ksa", "السعودية"})


def score_arabic_readiness(account: dict[str, Any]) -> tuple[float, list[str]]:
    """Higher when the lead is clearly Saudi-context (Arabic content,
    Saudi city, .sa domain, KSA country)."""
    score = 0.0
    notes: list[str] = []

    # Domain hint
    domain = str(account.get("domain") or "").lower()
    if domain.endswith(".sa") or domain.endswith(".com.sa"):
        score += 0.30
        notes.append("ksa_domain")

    # Country / city
    country = str(account.get("country") or "").lower()
    if country in _SAUDI_COUNTRY:
        score += 0.20
        notes.append("ksa_country")
    city = str(account.get("city") or "").lower()
    if any(c in city for c in _SAUDI_CITIES):
        score += 0.15
        notes.append("ksa_city")

    # Arabic content presence
    text_blob = " ".join(filter(None, [
        str(account.get("name") or ""),
        str(account.get("contact_name") or ""),
        str(account.get("description") or ""),
    ]))
    if _ARABIC_RE.search(text_blob):
        score += 0.25
        notes.append("arabic_text_present")

    # Locale preference declared
    locale = str(account.get("locale") or "").lower()
    if locale.startswith("ar"):
        score += 0.10
        notes.append("locale_ar_declared")

    return (round(min(1.0, score), 3), notes)


# Title patterns that suggest decision-making authority
_DECISION_MAKER_TITLES = (
    # English
    "ceo", "founder", "cofounder", "co-founder", "owner", "managing director",
    "md", "general manager", "gm", "vp", "vice president", "head of", "director",
    "partner",
    # Arabic
    "مدير عام", "مالك", "مؤسس", "شريك", "نائب", "رئيس", "المدير التنفيذي",
)


def score_decision_maker_access(
    account: dict[str, Any], *, has_warm_route: bool = False,
) -> tuple[float, list[str]]:
    """Higher when contact has decision-making title + warm route exists."""
    score = 0.0
    notes: list[str] = []

    title = str(account.get("contact_title") or "").lower()
    if any(t in title for t in _DECISION_MAKER_TITLES):
        score += 0.55
        notes.append("decision_maker_title")
    elif title:
        score += 0.20  # has some title (better than empty)
        notes.append("non_dm_title")

    if has_warm_route:
        score += 0.35
        notes.append("warm_route_available")

    # Penalty: contact_name missing entirely
    if not account.get("contact_name"):
        score = max(0.0, score - 0.10)
        notes.append("no_contact_name")

    return (round(min(1.0, score), 3), notes)


def score_whatsapp_dependency_risk(account: dict[str, Any]) -> tuple[float, list[str]]:
    """Higher = MORE risky (sole WhatsApp dependency).

    Risk scenarios:
    - Only WhatsApp number provided (no email)
    - Channel marked as WhatsApp-only in CRM
    - WhatsApp Business detected but no formal email/CRM signal
    """
    score = 0.0
    notes: list[str] = []

    has_email = bool(account.get("email"))
    has_phone = bool(account.get("phone") or account.get("whatsapp"))
    has_website = bool(account.get("website") or account.get("domain"))
    channels = account.get("preferred_channels") or []

    if not has_email and has_phone:
        score += 0.50
        notes.append("phone_only_no_email")
    if not has_website:
        score += 0.20
        notes.append("no_website")
    if isinstance(channels, list) and len(channels) == 1 and "whatsapp" in [c.lower() for c in channels]:
        score += 0.30
        notes.append("whatsapp_only_channel")

    return (round(min(1.0, score), 3), notes)


# Sectors with high regulatory sensitivity in KSA
_HIGH_SENSITIVITY_SECTORS = frozenset({
    "healthcare", "health", "pharma", "medical",
    "finance", "banking", "fintech", "insurance",
    "legal", "law",
    "education", "schools",
    "government", "public_sector",
    "oil_gas", "energy", "petrochemical",
    "telecom",
})
_MEDIUM_SENSITIVITY_SECTORS = frozenset({
    "real_estate", "property",
    "retail", "ecommerce",
    "logistics", "shipping",
    "food", "fnb", "restaurant",
})


def score_saudi_compliance_sensitivity(account: dict[str, Any]) -> tuple[float, list[str]]:
    """Higher = MORE compliance attention required (PDPL, ZATCA, sector regs).

    Used by Engine 4 (Decision Passport) to elevate compliance_risk_score
    when targeting regulated sectors.
    """
    score = 0.1  # baseline — every B2B touches PDPL
    notes: list[str] = ["baseline_pdpl"]

    sector = str(account.get("sector") or "").lower()
    if sector in _HIGH_SENSITIVITY_SECTORS:
        score += 0.65
        notes.append(f"high_sensitivity_{sector}")
    elif sector in _MEDIUM_SENSITIVITY_SECTORS:
        score += 0.30
        notes.append(f"medium_sensitivity_{sector}")

    # ZATCA Wave 24 trigger — turnover above SAR 375K → June 2026 deadline pressure
    turnover = account.get("annual_turnover_sar") or 0
    if isinstance(turnover, (int, float)) and turnover > 375_000:
        score += 0.20
        notes.append("zatca_wave_24_eligible")

    return (round(min(1.0, score), 3), notes)


def score_seasonality(
    account: dict[str, Any], *, on_date: date | None = None,
) -> tuple[float, list[str]]:
    """Score reflects how favorable the current Saudi season is for outreach.

    Higher = better timing. Eid → very low (PAUSE). Ordinary → neutral.
    Pre-Ramadan → high urgency (close before month). Exhibitions → high.
    """
    today = on_date or datetime.now(timezone.utc).date()
    season_ctx = detect_saudi_season(on_date=today)

    # Map each season to a favorability score
    season_to_score = {
        "ordinary": 0.5,
        "ramadan_prep": 0.85,         # high urgency to close
        "ramadan": 0.30,              # async only, slow
        "eid_al_fitr": 0.05,          # PAUSE
        "eid_al_adha": 0.05,          # PAUSE
        "hajj_season": 0.20,          # most B2B paused
        "school_year_start": 0.55,    # mild uplift
        "national_day": 0.65,         # patriotic uplift
        "founding_day": 0.65,         # patriotic uplift
        "exhibition_season": 0.80,    # very active
        "zatca_wave_24_deadline_window": 0.90,  # compliance scramble = high demand
    }
    score = season_to_score.get(season_ctx.season, 0.5)
    notes = [f"season={season_ctx.season}", f"confidence={season_ctx.confidence}"]
    return (round(score, 3), notes)


def score_relationship_strength(account: dict[str, Any]) -> tuple[float, list[str]]:
    """Higher = warmer relationship.

    Source priorities:
    - warm_intro / partner_referral → 1.0
    - inbound_form / inbound_whatsapp → 0.85
    - customer_uploaded_csv / crm_import → 0.55 (consented but not new)
    - manual_linkedin_research → 0.40 (still cold-ish)
    - cold_outreach → BLOCKED upstream; this returns 0.05 if it slips through
    """
    source = str(account.get("source") or "").lower()
    notes: list[str] = []

    if source in ("warm_intro", "partner_referral", "founder_intro"):
        score = 1.0
        notes.append(f"warm_source_{source}")
    elif source in ("inbound_form", "inbound_whatsapp", "website_inquiry"):
        score = 0.85
        notes.append(f"inbound_source_{source}")
    elif source in ("event_list_with_permission", "public_business_info_allowed"):
        score = 0.65
        notes.append(f"consented_source_{source}")
    elif source in ("customer_uploaded_csv", "crm_import", "google_sheet"):
        score = 0.55
        notes.append(f"customer_data_source_{source}")
    elif source == "manual_linkedin_research":
        score = 0.40
        notes.append("manual_research_source")
    elif source in ("cold_outreach", "scraping", "purchased_list", "linkedin_automation"):
        # Should be blocked upstream; if it slips through, score as low + flag
        score = 0.05
        notes.append(f"BLOCKED_SOURCE_{source}_should_be_filtered")
    else:
        # Unknown source — neutral but flagged
        score = 0.30
        notes.append("unknown_source")

    return (round(score, 3), notes)


# ─────────────────────────────────────────────────────────────────────
# Composer — produces full SaudiScoreBoard
# ─────────────────────────────────────────────────────────────────────


def compute_saudi_score_board(
    account: dict[str, Any],
    *,
    has_warm_route: bool = False,
    on_date: date | None = None,
) -> SaudiScoreBoard:
    """Compose all 6 Saudi-specific dimensions for one account.

    Args:
        account: Normalized account dict (from existing pipeline).
        has_warm_route: From decision_passport.builder — caller decides.
        on_date: Override date (for tests + seasonality determinism).

    Returns:
        SaudiScoreBoard — never raises; always is_estimate=True.
    """
    arabic, n1 = score_arabic_readiness(account)
    dm, n2 = score_decision_maker_access(account, has_warm_route=has_warm_route)
    wa_risk, n3 = score_whatsapp_dependency_risk(account)
    compliance, n4 = score_saudi_compliance_sensitivity(account)
    season, n5 = score_seasonality(account, on_date=on_date)
    relationship, n6 = score_relationship_strength(account)

    all_notes = tuple(n1 + n2 + n3 + n4 + n5 + n6)
    return SaudiScoreBoard(
        arabic_readiness=arabic,
        decision_maker_access=dm,
        whatsapp_dependency_risk=wa_risk,
        saudi_compliance_sensitivity=compliance,
        seasonality=season,
        relationship_strength=relationship,
        is_estimate=True,
        notes=all_notes,
    )
