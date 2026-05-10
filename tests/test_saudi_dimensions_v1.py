"""Wave 12.5 §33.2.2 (Engine 2) — 6 Saudi-specific scoring dimensions tests.

Validates each dimension scorer + the composer:
- arabic_readiness: domain/country/city/text/locale signals
- decision_maker_access: title + warm route
- whatsapp_dependency_risk: phone-only / no website / WhatsApp-only
- saudi_compliance_sensitivity: sector + ZATCA bracket
- seasonality: Saudi season → favorability
- relationship_strength: source priority

All pure functions, deterministic, no I/O.
"""
from __future__ import annotations

from datetime import date

import pytest

from auto_client_acquisition.pipelines.saudi_dimensions import (
    SaudiScoreBoard,
    compute_saudi_score_board,
    score_arabic_readiness,
    score_decision_maker_access,
    score_relationship_strength,
    score_saudi_compliance_sensitivity,
    score_seasonality,
    score_whatsapp_dependency_risk,
)


# ─────────────────────────────────────────────────────────────────────
# Arabic readiness (3 tests)
# ─────────────────────────────────────────────────────────────────────


def test_arabic_readiness_high_for_full_saudi_signals() -> None:
    """KSA domain + country + city + Arabic name + ar locale → high."""
    score, notes = score_arabic_readiness({
        "domain": "acme.com.sa",
        "country": "SA",
        "city": "Riyadh",
        "name": "شركة أكمي",
        "locale": "ar-SA",
    })
    assert score >= 0.8, f"all-Saudi signals → high; got {score}"
    assert "ksa_domain" in notes
    assert "arabic_text_present" in notes


def test_arabic_readiness_zero_for_no_signals() -> None:
    """No Saudi signals → 0.0."""
    score, notes = score_arabic_readiness({
        "domain": "example.us",
        "country": "USA",
        "city": "New York",
        "name": "Generic Inc",
    })
    assert score == 0.0


def test_arabic_readiness_partial_credit() -> None:
    """Domain only → partial credit."""
    score, _ = score_arabic_readiness({"domain": "acme.sa"})
    assert 0.2 <= score <= 0.5


# ─────────────────────────────────────────────────────────────────────
# Decision maker access (3 tests)
# ─────────────────────────────────────────────────────────────────────


def test_dm_access_high_for_ceo_with_warm_route() -> None:
    """CEO title + warm route → high."""
    score, notes = score_decision_maker_access(
        {"contact_name": "Sami", "contact_title": "CEO"},
        has_warm_route=True,
    )
    assert score >= 0.8
    assert "decision_maker_title" in notes
    assert "warm_route_available" in notes


def test_dm_access_low_for_no_title_no_route() -> None:
    """No title + no warm route → low."""
    score, _ = score_decision_maker_access({"contact_name": "X"})
    assert score < 0.3


def test_dm_access_arabic_titles_recognized() -> None:
    """Arabic decision-maker title patterns recognized."""
    score, notes = score_decision_maker_access(
        {"contact_name": "أحمد", "contact_title": "المدير التنفيذي"},
        has_warm_route=True,
    )
    assert score >= 0.8
    assert "decision_maker_title" in notes


# ─────────────────────────────────────────────────────────────────────
# WhatsApp dependency risk (2 tests)
# ─────────────────────────────────────────────────────────────────────


def test_whatsapp_risk_high_for_phone_only_no_website() -> None:
    """Phone but no email + no website → high risk."""
    score, notes = score_whatsapp_dependency_risk({
        "phone": "+966...",
    })
    assert score >= 0.5
    assert "phone_only_no_email" in notes


def test_whatsapp_risk_zero_for_full_channels() -> None:
    """Email + website + email-as-channel → no WhatsApp risk."""
    score, _ = score_whatsapp_dependency_risk({
        "email": "x@y.com",
        "website": "https://y.com",
        "preferred_channels": ["email"],
    })
    assert score == 0.0


# ─────────────────────────────────────────────────────────────────────
# Saudi compliance sensitivity (3 tests)
# ─────────────────────────────────────────────────────────────────────


def test_compliance_high_for_healthcare_sector() -> None:
    """Healthcare = high regulatory sensitivity."""
    score, notes = score_saudi_compliance_sensitivity({"sector": "healthcare"})
    assert score >= 0.7
    assert any("high_sensitivity" in n for n in notes)


def test_compliance_baseline_for_unknown_sector() -> None:
    """Every B2B has baseline PDPL — never zero."""
    score, notes = score_saudi_compliance_sensitivity({})
    assert score >= 0.05
    assert "baseline_pdpl" in notes


def test_compliance_zatca_wave_24_uplift() -> None:
    """Turnover > 375K SAR → ZATCA Wave 24 uplift."""
    base, _ = score_saudi_compliance_sensitivity({"sector": "retail"})
    with_zatca, notes = score_saudi_compliance_sensitivity({
        "sector": "retail", "annual_turnover_sar": 500_000,
    })
    assert with_zatca > base
    assert any("zatca_wave_24" in n for n in notes)


# ─────────────────────────────────────────────────────────────────────
# Seasonality (3 tests)
# ─────────────────────────────────────────────────────────────────────


def test_seasonality_eid_is_low() -> None:
    """Eid → very low favorability (PAUSE)."""
    score, _ = score_seasonality({}, on_date=date(2026, 3, 21))  # Eid al-Fitr
    assert score < 0.2


def test_seasonality_zatca_window_is_high() -> None:
    """ZATCA Wave 24 window → very high (compliance scramble)."""
    score, _ = score_seasonality({}, on_date=date(2026, 4, 15))
    assert score >= 0.85


def test_seasonality_ordinary_neutral() -> None:
    """Random non-season date → ~0.5 neutral."""
    score, _ = score_seasonality({}, on_date=date(2026, 7, 15))
    assert 0.4 <= score <= 0.6


# ─────────────────────────────────────────────────────────────────────
# Relationship strength (3 tests)
# ─────────────────────────────────────────────────────────────────────


def test_relationship_warm_intro_max() -> None:
    """warm_intro → 1.0 (highest)."""
    score, _ = score_relationship_strength({"source": "warm_intro"})
    assert score == 1.0


def test_relationship_blocked_source_returns_low_with_flag() -> None:
    """cold_outreach / scraping should be blocked upstream; if slips through,
    score as low + flag."""
    for bad_source in ("cold_outreach", "scraping", "purchased_list", "linkedin_automation"):
        score, notes = score_relationship_strength({"source": bad_source})
        assert score <= 0.1, f"{bad_source} should be near-zero; got {score}"
        assert any("BLOCKED_SOURCE" in n for n in notes)


def test_relationship_unknown_source_neutral_but_flagged() -> None:
    """Unknown source → 0.30 + flagged."""
    score, notes = score_relationship_strength({"source": "completely_new_thing"})
    assert score == 0.30
    assert any("unknown_source" in n for n in notes)


# ─────────────────────────────────────────────────────────────────────
# Composer (3 tests)
# ─────────────────────────────────────────────────────────────────────


def test_compose_saudi_score_board_returns_all_6_dims() -> None:
    """Composer returns SaudiScoreBoard with all 6 dimensions populated."""
    board = compute_saudi_score_board(
        {"domain": "acme.com.sa", "country": "SA", "sector": "real_estate",
         "source": "warm_intro", "contact_title": "CEO"},
        has_warm_route=True,
        on_date=date(2026, 7, 15),
    )
    assert isinstance(board, SaudiScoreBoard)
    assert 0.0 <= board.arabic_readiness <= 1.0
    assert 0.0 <= board.decision_maker_access <= 1.0
    assert 0.0 <= board.whatsapp_dependency_risk <= 1.0
    assert 0.0 <= board.saudi_compliance_sensitivity <= 1.0
    assert 0.0 <= board.seasonality <= 1.0
    assert 0.0 <= board.relationship_strength <= 1.0


def test_compose_marks_is_estimate_true() -> None:
    """Article 8: SaudiScoreBoard always is_estimate=True."""
    board = compute_saudi_score_board({})
    assert board.is_estimate is True


def test_compose_strong_saudi_warm_intro_high_overall_signals() -> None:
    """Strong Saudi context + warm intro → high relationship + arabic + dm."""
    board = compute_saudi_score_board(
        {
            "domain": "alacme.com.sa", "country": "SA", "city": "Riyadh",
            "name": "شركة الأكمي", "locale": "ar-SA",
            "source": "warm_intro", "contact_name": "Sami",
            "contact_title": "Founder",
        },
        has_warm_route=True,
        on_date=date(2026, 7, 15),
    )
    assert board.arabic_readiness >= 0.8
    assert board.relationship_strength == 1.0
    assert board.decision_maker_access >= 0.8


# ─────────────────────────────────────────────────────────────────────
# Total: 17 tests (3 arabic + 3 dm + 2 wa + 3 compliance + 3 season +
#                  3 relationship + 3 composer)
# ─────────────────────────────────────────────────────────────────────
